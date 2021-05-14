from mycroft.skills.skill_loader import SKILL_MAIN_MODULE, load_skill_module
from hivemind_bus_client import HiveMessageBusClient
from ovos_utils.log import LOG
from ovos_utils.messagebus import FakeBus, Message
from jarbas_hive_mind.message import HiveMessage, HiveMessageType
import os
import json


class HiveMindLocalSkillWrapper:
    def __init__(self, hive, skill_directory):
        self.hive = hive
        self.path = skill_directory
        self.skill_id = os.path.basename(skill_directory)
        self.instance = None
        self.bus = FakeBus()

    def reset_bus(self):
        self.bus = FakeBus()
        self.bus.on("message", self.handle_skill_emit)
        self.bus.bind(self.skill_id)
        if self.instance:
            self.instance.bind(self.bus)

    def load(self):
        skill_module = self.load_skill_source(self.path)
        self.instance = self.create_skill_instance(skill_module)
        return self

    def handle_skill_emit(self, message):
        self.hive.handle_skill_message(message)

    @staticmethod
    def load_skill_source(skill_directory):
        """Use Python's import library to load a skill's source code."""
        main_file_path = os.path.join(skill_directory, SKILL_MAIN_MODULE)
        skill_id = os.path.basename(skill_directory)
        if not os.path.isfile(main_file_path):
            LOG.error(f'Failed to load {skill_id} due to a missing file.')
        else:
            try:
                skill_module = load_skill_module(main_file_path, skill_id)
            except Exception as e:
                LOG.exception('Failed to load skill: '
                              '{} ({})'.format(skill_id, repr(e)))
            else:
                module_is_skill = (
                        hasattr(skill_module, 'create_skill') and
                        callable(skill_module.create_skill)
                )
                if module_is_skill:
                    return skill_module
        return None  # Module wasn't loaded

    def create_skill_instance(self, skill_module):
        """Use v2 skills framework to create the skill."""
        try:
            instance = skill_module.create_skill()
        except Exception as e:
            log_msg = 'Skill __init__ failed with {}'
            LOG.exception(log_msg.format(repr(e)))
            instance = None

        if instance:
            self.reset_bus()
            instance.skill_id = self.skill_id
            instance.bind(self.bus)

            # (eg skill_id( into message context
            try:
                instance.load_data_files()
                # Set up intent handlers
                # TODO: can this be a public method?
                instance._register_decorated()
                instance.register_resting_screen()
                instance.initialize()
            except Exception as e:
                # If an exception occurs, make sure to clean up the skill
                instance.default_shutdown()
                instance = None
                log_msg = 'Skill initialization failed with {}'
                LOG.exception(log_msg.format(repr(e)))
        return instance


class HiveMindExternalSkillWrapper(HiveMindLocalSkillWrapper):
    def __init__(self, skill_directory, port=6989, host="0.0.0.0", *args,
                 **kwargs):
        skill_id = os.path.basename(skill_directory)
        hive = HiveMessageBusClient(skill_id, port=port, host=host, ssl=False)
        super().__init__(hive=hive, skill_directory=skill_directory)
        self.hive.on("open", self.load)
        self.hive.on_close = self.handle_shutdown
        self.hive.on("message", self.handle_hive_message)

    def handle_shutdown(self):
        try:
            self.instance.default_shutdown()
        except:
            pass
        try:
            self.instance.shutdown()
        except:
            pass

    def connect_to_hive(self):
        self.hive.run_in_thread()

    def handle_skill_emit(self, message):
        if isinstance(message, str):
            message = Message.deserialize(message)
        message.context["skill_id"] = self.skill_id
        if not message.context.get("source"):
            message.context["source"] = self.skill_id
        msg = HiveMessage(HiveMessageType.BUS, payload=message)
        #LOG.debug(f"SkillMessage: {msg}")
        self.hive.emit(msg)

    def handle_hive_message(self, message):
        #LOG.debug(f"HiveMessage: {message}")
        if isinstance(message, str):
            message = json.loads(message)
        if isinstance(message, dict):
            message = HiveMessage(**message)
        if message.msg_type == HiveMessageType.BUS:
            self.bus.emit(message.payload)
