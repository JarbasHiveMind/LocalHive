from local_hive.skill import HiveMindExternalSkillWrapper
from ovos_utils import wait_for_exit_signal
from os.path import join, dirname

path = join(dirname(__file__), "test_skills", "mycroft-hello-world.mycroftai")

skill = HiveMindExternalSkillWrapper(path)
skill.connect_to_hive()  # connect to hive

wait_for_exit_signal()

