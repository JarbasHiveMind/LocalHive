from local_hive.skill import HiveMindExternalSkillWrapper

path = "/home/user/my_code/HiveMind/LocalMind/examples/test_skills/mycroft-hello-world.mycroftai"
skill = HiveMindExternalSkillWrapper(path).load()
skill.run()

