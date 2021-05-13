from local_hive.skill import HiveMindExternalSkillWrapper

path = "/examples/test_skills/mycroft-hello-world.mycroftai"
skill = HiveMindExternalSkillWrapper(path).load()
skill.run()

