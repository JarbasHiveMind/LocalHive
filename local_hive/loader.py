import os

from hivemind_bus_client import HiveMessageBusClient, HiveMessage, HiveMessageType
from hivemind_bus_client.protocol import HiveMindSlaveProtocol
from ovos_utils.log import LOG
from ovos_utils.messagebus import FakeBus
from ovos_workshop.skill_launcher import SkillLoader


class SkillProtocol(HiveMindSlaveProtocol):

    def handle_bus(self, message):
        LOG.debug(f">>: {message.payload.msg_type}")
        # inject the hivemind to the skill FakeBus
        # flag SkillBus to not re-emit it to HM connection
        message.payload.context["source"] = "IntentService"
        self.internal_protocol.bus.emit(message.payload, send2hm=False)


class SkillBus(FakeBus):

    def __init__(self, skill_id, hive, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill_id = skill_id
        self.hive = hive

    def emit(self, message, send2hm=True):
        # ensure skill_id in all messages
        message.context["skill_id"] = self.skill_id
        if not message.context.get("source"):
            message.context["source"] = self.skill_id

        super().emit(message)

        if send2hm:
            msg = HiveMessage(HiveMessageType.BUS, payload=message)
            LOG.debug(f"<<: {message.msg_type}")
            self.hive.emit(msg)


class HiveMindExternalSkillWrapper:
    def __init__(self, skill_directory, port=6989, host="127.0.0.1"):
        skill_id = os.path.basename(skill_directory)

        self.path = skill_directory
        self.skill_id = skill_id

        self.hive = HiveMessageBusClient(self.skill_id, port=port, host=host)
        self.hive.on_close = self.handle_shutdown

        self.bus = SkillBus(self.skill_id, self.hive)

        protocol = SkillProtocol(self.hive)

        protocol.bind(self.bus)
        self.hive.connect(self.bus, protocol=protocol)

        self.skill_loader = SkillLoader(self.bus, self.path)
        self.load()

    @property
    def instance(self):
        return self.skill_loader.instance

    def handle_shutdown(self):
        try:
            self.instance.shutdown()
        except:
            pass

    def load(self):
        self.skill_loader.load()
        return self


def load_skills_folder(folder):
    for f in os.listdir(folder):
        if f.startswith("_") or f.startswith("."):
            continue
        path = os.path.join(folder, f)
        if os.path.isdir(path):
            yield HiveMindExternalSkillWrapper(os.path.join(folder, f))
