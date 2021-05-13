from mycroft.skills.skill_loader import SKILL_MAIN_MODULE, load_skill_module
from hivemind_bus_client import HiveMessageBusClient
from ovos_utils.log import LOG
from ovos_utils.messagebus import FakeBus, Message
import os


class HiveMindSkillWrapper:
    def __init__(self, hive, skill_directory):
        self.hive = hive
        self.path = skill_directory
        self.skill_id = os.path.basename(skill_directory)
        self.instance = None

    def load(self):
        skill_module = self._load_skill_source(self.path)
        self.instance = self._create_skill_instance(
            skill_module, self.skill_id, self.hive.handle_skill_emit)
        return self

    @staticmethod
    def _load_skill_source(skill_directory):
        """Use Python's import library to load a skill's source code."""
        main_file_path = os.path.join(skill_directory, SKILL_MAIN_MODULE)
        skill_id = os.path.basename(skill_directory)
        if not os.path.exists(main_file_path):
            error_msg = 'Failed to load {} due to a missing file.'
            LOG.error(error_msg.format(skill_id))
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

    @staticmethod
    def _create_skill_instance(skill_module, skill_id, bus_handler):
        """Use v2 skills framework to create the skill."""
        try:
            instance = skill_module.create_skill()
        except Exception as e:
            log_msg = 'Skill __init__ failed with {}'
            LOG.exception(log_msg.format(repr(e)))
            instance = None

        if instance:
            bus = FakeBus()
            bus.on("message", bus_handler)

            instance.skill_id = skill_id
            instance.bind(bus)
            bus.bind(skill_id)  # FakeBus method to allow injecting metadata
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
