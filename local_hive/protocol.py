from hivemind_bus_client.message import HiveMessage, HiveMessageType
from hivemind_core.protocol import HiveMindListenerProtocol, HiveMindClientConnection, \
    HiveMindListenerInternalProtocol
from json_database import JsonConfigXDG
from ovos_bus_client import Message
from ovos_core.intent_services import IntentService
from ovos_utils.log import LOG
from ovos_utils.messagebus import FakeBus

import local_hive.permissions as Permissions


class LocalHiveInternalProtocol(HiveMindListenerInternalProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intent_service = None
        self.intent2skill = {}

    def register_bus_handlers(self):
        self.intent_service = IntentService(self.bus)
        self.bus.on("message", self.handle_internal_mycroft)  # catch all

    def skill2peer(self, skill_id):
        for peer, client in self.clients.items():
            if client.key == skill_id:
                return peer
        return None

    # mycroft handlers  - from LocalHive -> skill
    def handle_internal_mycroft(self, message: str):
        """ forward internal messages to clients if they are the target
        here is where the client isolation happens,
        clients only get responses to their own messages"""

        # "message" event is a special case in ovos-bus-client that is not deserialized
        message = Message.deserialize(message)

        if message.msg_type in ["skill.converse.ping"]:
            LOG.info("Converse ping")
            # TODO - careful to avoid infinite loop
            # for client in self.clients.values():
            #    client.send(
            #        HiveMessage(HiveMessageType.BUS, message)
            #    )
            # return

        skill_id = message.context.get("skill_id")

        skill_peer = self.skill2peer(skill_id)
        if not skill_peer:
            return

        client = self.clients[skill_peer]

        peers = message.context.get("destination") or []

        # converse method handling
        if message.msg_type in ["skill.converse.request"]:
            LOG.info(f"Converse: {message.msg_type} "
                     f"Skill: {skill_id} "
                     f"Peer: {skill_peer}")
            # client.send(
            #    HiveMessage(HiveMessageType.BUS, message)
            # )
        elif message.msg_type in ["skill.converse.response"]:
            response = message.data.get("result")
            LOG.info(f"Converse Response: {response} "
                     f"Skill: {skill_id} "
                     f"Peer: {skill_peer}")
        # intent found
        elif message.msg_type in self.intent2skill:
            LOG.info(f"Intent: {message.msg_type} "
                     f"Skill: {skill_id} "
                     f"Source: {peers} "
                     f"Target: {skill_peer}")
            # trigger the skill
            LOG.debug(f"Triggering intent: {skill_peer}")
            client.send(
                HiveMessage(HiveMessageType.BUS, message)
            )
            return
        # skill registering intent - keep track internally
        elif message.msg_type in ["register_intent",
                                  "padatious:register_intent"]:
            LOG.info(f"Register Intent: {message.data['name']} "
                     f"Skill: {message.context['skill_id']}")
            self.intent2skill[message.data["name"]] = skill_id
            # print(self.intent_service.__dict__)

        for peer, client in self.clients.items():
            if peer in peers and peer != skill_peer:
                client.send(HiveMessage(HiveMessageType.BUS, message))


class LocalHiveProtocol(HiveMindListenerProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_overrides = JsonConfigXDG("skill_permissions", subfolder="LocalHive")

    def handle_new_client(self, client: HiveMindClientConnection):
        LOG.info(f"new client: {client.peer}")
        self.clients[client.peer] = client
        message = Message("hive.client.connect",
                          {"ip": client.ip, "session_id": client.sess.session_id},
                          {"source": client.peer})
        self.internal_protocol.bus.emit(message)

        msg = HiveMessage(HiveMessageType.HELLO,
                          payload={"handshake": False,
                                   "crypto": False,
                                   "peer": client.peer,  # this identifies the connected client in ovos message.context
                                   "node_id": self.peer})
        # LOG.debug(f"saying HELLO to: {client.peer}")
        client.send(msg)

        # request client to start handshake (by sending client pubkey)
        payload = {
            "handshake": False,  # tell the client it must do a handshake or connection will be dropped
            "binarize": False,  # report we support the binarization scheme
            "preshared_key": False,  # do we have a pre-shared key (V0 proto)
            "password": False,  # is password available (V1 proto, replaces pre-shared key)
            "crypto_required": False  # do we allow unencrypted payloads
        }
        msg = HiveMessage(HiveMessageType.HANDSHAKE, payload)
        LOG.debug(f"starting {client.peer} HANDSHAKE: {payload}")
        client.send(msg)
        # if client is in protocol V1 -> self.handle_handshake_message
        # clients can rotate their pubkey or session_key by sending a new handshake

    def handle_handshake_message(self, message: HiveMessage,
                                 client: HiveMindClientConnection):
        payload = {
            "handshake": False,  # tell the client it must do a handshake or connection will be dropped
            "binarize": False,  # report we support the binarization scheme
            "preshared_key": False,  # do we have a pre-shared key (V0 proto)
            "password": False,  # is password available (V1 proto, replaces pre-shared key)
            "crypto_required": False  # do we allow unencrypted payloads
        }
        msg = HiveMessage(HiveMessageType.HANDSHAKE, payload)
        LOG.debug(f"skipping {client.peer} HANDSHAKE: {payload}")
        client.send(msg)

    @property
    def intent_service(self):
        return self.internal_protocol.intent_service

    def bind(self, websocket, bus=None):
        websocket.protocol = self
        if bus is None:
            bus = FakeBus()
        self.internal_protocol = LocalHiveInternalProtocol(bus)
        self.internal_protocol.register_bus_handlers()

    # messages from skill -> LocalHive
    def handle_inject_mycroft_msg(self, message: Message, client: HiveMindClientConnection):
        """
        message (Message): mycroft bus message object
        """
        # message from a terminal
        if message.msg_type in Permissions.UTTERANCES:
            LOG.info(f"Utterance: {message.data['utterances']} "
                     f"Peer: {client.peer}")
            message.context["source"] = client.peer
            self.internal_protocol.bus.emit(message)
        # message from a skill
        elif message.context.get("skill_id"):
            message.context["source"] = client.peer
            self.handle_skill_message(message)

    def handle_skill_message(self, message):
        """ message sent by skill"""
        if isinstance(message, str):
            message = Message.deserialize(message)

        is_intent_for_skill = self.internal_protocol.intent2skill.get(message.msg_type)
        skill_id = message.context.get("skill_id") or is_intent_for_skill or ""
        permitted = False

        # skill intents
        if is_intent_for_skill:
            permitted = True
        # skill_id permission override
        elif skill_id in self.permission_overrides:
            if message.msg_type in self.permission_overrides[skill_id]:
                permitted = True
        # default permissions
        elif message.msg_type in Permissions.DEFAULT:
            permitted = True

        LOG.debug(f"{message.msg_type} allowed for {skill_id}: {permitted}")
        message.context["skill_id"] = skill_id
        if permitted:  # forward to intent service
            self.internal_protocol.bus.emit(message)
        else:
            self.handle_ignored_message(message)

    def handle_ignored_message(self, message):
        pass
