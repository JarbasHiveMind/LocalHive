from local_hive.skills import LocalHiveListener


def get_listener(port=6989):
    localmind = LocalHiveListener(port)
    return localmind
