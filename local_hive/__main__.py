from local_hive import LocalHiveListener


skills_folder = "/home/user/my_code/HiveMind/LocalMind/test_skills"


def get_listener(port=6989):
    return LocalHiveListener(port=port)


if __name__ == "__main__":
    localmind = get_listener()
    localmind.hive.load_system_skills_folder(skills_folder)
    localmind.listen()
