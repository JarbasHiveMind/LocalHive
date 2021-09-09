from os import listdir
from os.path import join, isdir

from jarbas_hive_mind import HiveMindListener
from jarbas_hive_mind.message import HiveMessage, HiveMessageType
from jarbas_hive_mind.nodes.fakecroft import FakeCroftMind, \
    FakeCroftMindProtocol
from local_hive.exceptions import NonLocalConnectionError
from local_hive.fakebus import FakeBus
from local_hive.skills.loader import HiveMindLocalSkillWrapper
from mycroft.skills.intent_service import IntentService
from mycroft_bus_client import Message
from ovos_utils.log import LOG
from pyee import ExecutorEventEmitter


class LocalHiveProtocol(FakeCroftMindProtocol):
    platform = "LocalHiveV0.1"
    crypto_key = None

    def onConnect(self, request):
        LOG.info("Client connecting: {0}".format(request.peer))
        ip = request.peer.split(":")[1]

        self.platform = request.headers.get("platform", "unknown")

        if ip not in ["0.0.0.0", "127.0.0.1"]:
            raise NonLocalConnectionError

        # the key is the skill_id and used as an auxiliary data point to
        # target messages, this changes the paradigm of the regular
        # hivemind, but its perfectly valid and convenient way to pass this
        # info around
        name, key = self.decode_auth(request)
        # repo.author, unimportant if it catches false positives
        LOG.info(f"HiveSkill connected {key}")
        context = {"source": self.peer, "skill_id": key}
        self.skill_id = key

        # send message to internal mycroft bus
        data = {"ip": ip, "headers": request.headers}
        self.factory.mycroft_send("hive.client.connect", data, context)
        # return a pair with WS protocol spoken (or None for any) and
        # custom headers to send in initial WS opening handshake HTTP response
        headers = {"server": self.platform}

        return (None, headers)


class LocalHive(FakeCroftMind):
    protocol = LocalHiveProtocol
    intent_messages = [
        "recognizer_loop:utterance",
        "intent.service.intent.get",
        "intent.service.skills.get",
        "intent.service.active_skills.get",
        "intent.service.adapt.get",
        "intent.service.padatious.get",
        "intent.service.adapt.manifest.get",
        "intent.service.padatious.manifest.get",
        "intent.service.adapt.vocab.manifest.get",
        "intent.service.padatious.entities.manifest.get",
        "register_vocab",
        "register_intent",
        "detach_intent",
        "detach_skill",
        "add_context",
        "remove_context",
        "clear_context",
        "mycroft.skills.loaded",
        "active_skill_request",
        'mycroft.speech.recognition.unknown',
        'padatious:register_intent',
        'padatious:register_entity',
        'mycroft.skills.initialized'
    ]
    default_permissions = intent_messages + [
        "speak",
        "mycroft.skill.handler.start",
        "mycroft.skill.handler.complete",
        "skill.converse.request",
        "skill.converse.response"
    ]

    def __init__(self, port=6989, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bus_port = port
        intentbus = FakeBus()
        intentbus.on("message", self.handle_intent_service_message)
        self.intent_service = IntentService(intentbus)
        self.intent2skill = {}
        # these are "system" skills, for the most part skills should be
        # external clients instead connected by hivemind bus
        self.system_skills = {}
        self.permission_overrides = {
            "mycroft-hello-world.mycroftai":
                self.default_permissions + ["test"]
        }
        self.ee = ExecutorEventEmitter()
        self.ee.on("localhive.skill", self.handle_skill_message)
        self.ee.on("localhive.utterance", self.intent_service.handle_utterance)

    # intent service is answering a skill / client
    def skill2peer(self, skill_id):
        for peer, client in self.clients.items():
            if not client.get("instance"):
                continue
            if client["instance"].skill_id == skill_id:
                return peer
        return None

    def handle_intent_service_message(self, message):
        if isinstance(message, str):
            message = Message.deserialize(message)
        skill_id = message.context.get("skill_id")
        peers = message.context.get("destination") or []

        # converse method handling
        if message.msg_type in ["skill.converse.request"]:
            skill_id = message.data.get("skill_id")
            message.context["skill_id"] = skill_id
            skill_peer = self.skill2peer(skill_id)
            LOG.info(f"Converse: {message.msg_type} "
                     f"Skill: {skill_id} "
                     f"Peer: {skill_peer}")
            message.context['source'] = "IntentService"
            message.context['destination'] = peers
            if skill_id in self.system_skills:
                self.system_skills[skill_id].bus.emit(message)
            else:
                self.send2peer(message, skill_peer)
        elif message.msg_type in ["skill.converse.response"]:
            # just logging that it was received, converse method handled by
            # skill
            skill_id = message.data.get("skill_id")
            response = message.data.get("result")
            message.context["skill_id"] = skill_id
            skill_peer = self.skill2peer(skill_id)
            LOG.info(f"Converse Response: {response} "
                     f"Skill: {skill_id} "
                     f"Peer: {skill_peer}")
            message.context['source'] = skill_id
            message.context['destination'] = peers
        # intent found
        elif message.msg_type in self.intent2skill:
            skill_id = self.intent2skill[message.msg_type]
            skill_peer = self.skill2peer(skill_id)
            message.context["skill_id"] = skill_id

            LOG.info(f"Intent: {message.msg_type} "
                     f"Skill: {skill_id} "
                     f"Source: {peers} "
                     f"Target: {skill_peer}")

            # trigger the skill
            message.context['source'] = "IntentService"
            if skill_id in self.system_skills:
                self.system_skills[skill_id].bus.emit(message)
            else:
                # LOG.debug(f"Triggering intent: {skill_peer}")
                self.send2peer(message, skill_peer)

        # skill registering intent
        elif message.msg_type in ["register_intent",
                                  "padatious:register_intent"]:
            LOG.info(f"Register Intent: {message.data['name']} "
                     f"Skill: {message.context['skill_id']}")
            self.intent2skill[message.data["name"]] = skill_id

    def send2peer(self, message, peer):
        if peer in self.clients:
            LOG.debug(f"sending to: {peer}")
            client = self.clients[peer].get("instance")
            msg = HiveMessage(HiveMessageType.BUS,
                              source_peer=self.peer,
                              payload=message)
            self.interface.send(msg, client)

    # external skills / clients
    def handle_incoming_mycroft(self, message, client):
        """
        external skill client sent a message

        message (Message): mycroft bus message object
        """
        # message from a skill
        if message.context.get("skill_id"):
            self.ee.emit("localhive.skill", message)
        # message from a terminal
        if message.msg_type == "recognizer_loop:utterance":
            LOG.info(f"Utterance: {message.data['utterances']} "
                     f"Peer: {client.peer}")
            message.context["source"] = client.peer
            self.ee.emit("localhive.utterance", message)

    def handle_skill_message(self, message):
        """ message sent by local/system skill"""
        if isinstance(message, str):
            message = Message.deserialize(message)

        skill_id = message.context.get("skill_id")
        intent_skill = self.intent2skill.get(message.msg_type)
        permitted = False

        # skill intents
        if intent_skill:
            permitted = True
        # skill_id permission override
        elif skill_id and skill_id in self.permission_overrides:
            if message.msg_type in self.permission_overrides[skill_id]:
                permitted = True
        # default permissions
        elif message.msg_type in self.default_permissions:
            permitted = True

        if permitted:
            peers = message.context.get('destination') or []
            if isinstance(peers, str):
                peers = [peers]

            # check if it should be forwarded to some peer (skill/terminal)
            for peer in peers:
                if peer in self.clients:
                    LOG.debug(f"destination: {message.context['destination']} "
                              f"skill:{skill_id} "
                              f"type:{message.msg_type}")
                    self.send2peer(message, peer)

            # check if this message should be forwarded to intent service
            if message.msg_type in self.intent_messages or \
                    "IntentService" in peers:
                self.intent_service.bus.emit(message)

        else:
            self.handle_ignored_message(message)

    def handle_ignored_message(self, message):
        pass

    # locally managed skills
    def load_system_skill(self, skill_directory):
        if skill_directory in self.system_skills:
            LOG.error("Already loaded!")
            return self.system_skills[skill_directory]
        skill = HiveMindLocalSkillWrapper(self, skill_directory)
        LOG.info(f"Loading skill {skill.skill_id}")
        self.system_skills[skill.skill_id] = skill.load()
        return skill

    def load_system_skills_folder(self, folder):
        for f in listdir(folder):
            if f.startswith("_"):
                continue
            path = join(folder, f)
            if isdir(path):
                self.load_system_skill(path)
        return self.system_skills


class LocalHiveListener(HiveMindListener):
    def __init__(self, port, *args, **kwargs):
        super(LocalHiveListener, self).__init__(port=port, *args, **kwargs)
        self.hive = LocalHive(port=port)

    def secure_listen(self, *args, **kwargs):
        return super().secure_listen(key=None, cert=None, factory=self.hive,
                                     protocol=LocalHiveProtocol)

    def unsafe_listen(self, *args, **kwargs):
        return super().unsafe_listen(factory=self.hive,
                                     protocol=LocalHiveProtocol)

    def listen(self, *args, **kwargs):
        return super().listen(factory=self.hive, protocol=LocalHiveProtocol)
