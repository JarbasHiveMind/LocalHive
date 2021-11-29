from local_hive.protocol import LocalHiveListener


def get_listener(port=6989):
    localmind = LocalHiveListener(port)
    return localmind
