from local_hive.skills import load_skills_folder
from ovos_utils import wait_for_exit_signal
from os.path import join, dirname

path = join(dirname(__file__), "test_skills")

for skill in load_skills_folder(path):
    print(skill.skill_id)

wait_for_exit_signal()

"""
2021-05-14 03:23:50.059 | INFO     | 44310 | HiveMind-websocket-client | Connected
2021-05-14 03:23:50.111 | INFO     | 44310 | mycroft.skills.settings:get_local_settings:83 | /home/user/.config/mycroft/skills/mycroft-joke.mycroftai/settings.json
"""
