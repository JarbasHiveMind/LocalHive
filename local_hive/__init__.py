from jarbas_hive_mind import HiveMindListener
from local_hive.master import LocalHive, LocalHiveProtocol


class LocalHiveListener(HiveMindListener):
    def __init__(self, port, *args, **kwargs):
        super(LocalHiveListener, self).__init__(port=port, *args, **kwargs)
        self.hive = LocalHive(port=port)

    def secure_listen(self, *args, **kwargs):
        return super().secure_listen(key=None, cert=None, factory=self.hive,
                                     protocol=LocalHiveProtocol)

    def unsafe_listen(self, *args, **kwargs):
        return super().unsafe_listen(factory=self.hive,
                                     protocol=LocalHiveProtocol)

    def listen(self, *args, **kwargs):
        return super().listen(factory=self.hive, protocol=LocalHiveProtocol)


def get_listener(port=6989):
    localmind = LocalHiveListener(port)
    return localmind
