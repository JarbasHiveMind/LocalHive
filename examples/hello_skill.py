from local_hive.skills import HiveMindExternalSkillWrapper
from ovos_utils import wait_for_exit_signal
from os.path import join, dirname

path = join(dirname(__file__), "test_skills", "mycroft-hello-world.mycroftai")

skill = HiveMindExternalSkillWrapper(path)

wait_for_exit_signal()

"""
2021-05-14 03:21:14.258 | INFO     | 42880 | HiveMind-websocket-client | Connected
2021-05-14 03:21:14.262 | INFO     | 42880 | mycroft.skills.settings:get_local_settings:83 | /home/user/.config/mycroft/skills/mycroft-hello-world.mycroftai/settings.json
2021-05-14 03:21:44.885 | INFO     | 42880 | HelloWorldSkill | There are five types of log messages: info, debug, warning, error, and exception.
"""