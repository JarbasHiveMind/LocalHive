from jarbas_hive_mind.exceptions import ConnectionError


class NonLocalConnectionError(ConnectionError):
    """ this connection does not originate from host machine """
