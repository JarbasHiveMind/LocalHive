import os
from time import sleep

from ovos_workshop.skill_launcher import SkillLoader
from ovos_bus_client import Message
from ovos_utils.log import LOG

from hivemind_bus_client import HiveMessageBusClient, HiveMessage, HiveMessageType
from local_hive.fakebus import FakeBus


class HiveMindExternalSkillWrapper:
    def __init__(self, skill_directory, port=6989, host="127.0.0.1"):
        skill_id = os.path.basename(skill_directory)

        self.path = skill_directory
        self.skill_id = skill_id

        # fakebus so we can intercept and modify before sending to hivemind
        # we could technically pass the hivemind connection directly,
        # especially since ovos-core ensures the skill_id is present in the context
        # however this makes it easier to expand functionality in the future
        self.bus = FakeBus()
        self.bus.on("message", self.handle_skill_emit)
        self.bus.bind(self.skill_id)

        self.hive = HiveMessageBusClient(self.skill_id, port=port, host=host)
        self.hive.connect(self.bus)

        self.hive.on_close = self.handle_shutdown
        self.hive.on(HiveMessageType.BUS, self.handle_hive_message)

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

    def connect_to_hive(self):
        self.hive.run_in_thread()
        while not self.hive.connected_event.is_set():
            sleep(0.1)

    def load(self):
        self.connect_to_hive()
        self.skill_loader.load()
        return self

    def handle_skill_emit(self, message):
        if isinstance(message, str):
            message = Message.deserialize(message)
        message.context["skill_id"] = self.skill_id
        if not message.context.get("source"):
            message.context["source"] = self.skill_id
        msg = HiveMessage(HiveMessageType.BUS, payload=message)
        LOG.debug(f"<<: {message.msg_type}")
        self.hive.emit(msg)

    def handle_hive_message(self, message):
        LOG.debug(f">>: {message.payload.msg_type}")
        self.bus.emit(message.payload)


def load_skills_folder(folder):
    for f in os.listdir(folder):
        if f.startswith("_") or f.startswith("."):
            continue
        path = os.path.join(folder, f)
        if os.path.isdir(path):
            yield HiveMindExternalSkillWrapper(os.path.join(folder, f))
