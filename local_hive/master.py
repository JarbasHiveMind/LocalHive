from jarbas_hive_mind.nodes.fakecroft import FakeCroftMind, \
    FakeCroftMindProtocol
from jarbas_hive_mind.message import HiveMessage, HiveMessageType
from local_hive.exceptions import NonLocalConnectionError
from mycroft.skills.skill_loader import SKILL_MAIN_MODULE, load_skill_module
from hivemind_bus_client import HiveMessageBusClient
from ovos_utils.log import LOG
from ovos_utils.messagebus import FakeBus, Message
from os.path import join, isdir
from os import listdir
import os


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
        self.allowed_messages = {
            "mycroft-hello-world.mycroftai": self.default_permissions + ["test"]
        }

    def load_system_skills_folder(self, folder):
        for f in listdir(folder):
            path = join(folder, f)
            if isdir(path):
                self.load_system_skill(path)
        return self.system_skills

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

    def _create_skill_instance(self, skill_module, skill_id):
        """Use v2 skills framework to create the skill."""
        try:
            instance = skill_module.create_skill()
        except Exception as e:
            log_msg = 'Skill __init__ failed with {}'
            LOG.exception(log_msg.format(repr(e)))
            instance = None

        if instance:
            bus = FakeBus()
            bus.on("message", self.handle_skill_emit)

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

    def handle_skill_emit(self, message):
        message = Message.deserialize(message)
        skill_id = message.context.get("skill_id")
        permitted = False
        if skill_id:
            # skill_id permission override
            if skill_id in self.allowed_messages:
                if message.msg_type in self.allowed_messages[skill_id]:
                    permitted = True
            # no override for skill_id
            else:
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

        skill_id = os.path.basename(skill_directory)
        skill_module = self._load_skill_source(skill_directory)
        instance = self._create_skill_instance(skill_module, skill_id)
        self.system_skills[skill_id] = instance
        return instance
