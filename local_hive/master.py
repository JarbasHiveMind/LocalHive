from jarbas_hive_mind.nodes.fakecroft import FakeCroftMind, \
    FakeCroftMindProtocol
from jarbas_hive_mind.message import HiveMessage, HiveMessageType
from local_hive.exceptions import NonLocalConnectionError
from ovos_utils.log import LOG
from ovos_utils.messagebus import FakeBus, Message
from os.path import join, isdir
from os import listdir

from local_hive.skill import HiveMindLocalSkillWrapper


class LocalHiveProtocol(FakeCroftMindProtocol):
    platform = "LocalHiveV0.1"

    def onConnect(self, request):
        LOG.info("Client connecting: {0}".format(request.peer))
        print(request.peer)
        ip = request.peer.split(":")[1]
        context = {"source": self.peer}
        self.platform = request.headers.get("platform", "unknown")

        if ip not in ["0.0.0.0", "127.0.0.1"]:
            raise NonLocalConnectionError

        # send message to internal mycroft bus
        data = {"ip": ip, "headers": request.headers}
        self.factory.mycroft_send("hive.client.connect", data, context)
        # return a pair with WS protocol spoken (or None for any) and
        # custom headers to send in initial WS opening handshake HTTP response
        headers = {"server": self.platform}
        return (None, headers)


class LocalHive(FakeCroftMind):
    protocol = LocalHiveProtocol
    default_permissions = [
        "register_vocab",
        "register_intent",
        "padatious:register_intent",
        "speak"
    ]

    def __init__(self, port=6989, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bus_port = port
        # these are "system" skills, for the most part skills should be
        # external clients instead connected by hivemind bus
        self.system_skills = {}
        self.permission_overrides = {
            "mycroft-hello-world.mycroftai":
                self.default_permissions + ["test"]
        }

    # external skills
    def handle_incoming_mycroft(self, message, client):
        """
        external skill client sent a message

        message (Message): mycroft bus message object
        """
        self.handle_skill_message(message)

    # locally managed skills
    def handle_skill_message(self, message):
        """ message sent by local/system skill"""
        message = Message.deserialize(message)
        skill_id = message.context.get("skill_id")
        permitted = False
        if skill_id and skill_id in self.permission_overrides:
            # skill_id permission override
            if message.msg_type in self.permission_overrides[skill_id]:
                permitted = True
        # default permissions
        elif message.msg_type in self.default_permissions:
            permitted = True

        if permitted:
            LOG.debug(f"Mycroft bus message received: {message.msg_type}")
        else:
            LOG.error("forbidden bus message!!!")
            LOG.debug(f"Mycroft bus message received: {message.msg_type}")
            LOG.debug(f"data: {message.data}")
            LOG.debug(f"context: {message.context}")

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
            path = join(folder, f)
            if isdir(path):
                self.load_system_skill(path)
        return self.system_skills
