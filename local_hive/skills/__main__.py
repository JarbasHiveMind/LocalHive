from local_hive import get_listener
from mycroft.skills.msm_wrapper import get_skills_directory

if __name__ == "__main__":
    localmind = get_listener()
    localmind.hive.load_system_skills_folder(get_skills_directory())
    localmind.listen()
