import asyncio
from threading import Thread
from typing import Callable, Dict, Any, Optional

from hivemind_bus_client.identity import NodeIdentity
from hivemind_core.protocol import HiveMindClientConnection
from hivemind_core.service import MessageBusEventHandler
from ovos_bus_client.session import Session
from ovos_config import Configuration
from ovos_utils.log import LOG
from ovos_utils.process_utils import ProcessStatus, StatusCallbackMap
from tornado import web, ioloop
from tornado.platform.asyncio import AnyThreadEventLoopPolicy

from local_hive.fakebus import FakeBus
from local_hive.protocol import LocalHiveProtocol


def on_ready():
    LOG.info('LocalHive service ready!')


def on_alive():
    LOG.info('LocalHive service alive')


def on_started():
    LOG.info('LocalHive service started!')


def on_error(e='Unknown'):
    LOG.info('LocalHive failed to start ({})'.format(repr(e)))


def on_stopping():
    LOG.info('LocalHive is shutting down...')


class LocalHiveBusEventHandler(MessageBusEventHandler):

    def open(self):

        auth = self.request.uri.split("/?authorization=")[-1]
        name, key = self.decode_auth(auth)
        LOG.info(f"authorizing skill_id: {key}")

        # the key is the skill_id and used as an auxiliary data point to
        # target messages, this changes the paradigm of the regular
        # hivemind, but its perfectly valid and convenient way to pass this
        # info around
        # repo.author convention is unimportant if it catches false positives
        self.client = HiveMindClientConnection(key=key, name=name,
                                               ip="127.0.0.1",
                                               socket=self, sess=Session(),
                                               loop=self.protocol.loop)
        self.protocol.handle_new_client(self.client)
        # self.write_message(Message("connected").serialize())

    def on_close(self):
        LOG.info(f"disconnecting client: {self.client.peer}")
        self.protocol.handle_client_disconnected(self.client)

    def check_origin(self, origin) -> bool:
        # blocks any connection not from localhost
        ip = origin.split("://")[-1].split(":")[0]
        return ip == "127.0.0.1"


class LocalHiveService(Thread):

    def __init__(self,
                 alive_hook: Callable = on_alive,
                 started_hook: Callable = on_started,
                 ready_hook: Callable = on_ready,
                 error_hook: Callable = on_error,
                 stopping_hook: Callable = on_stopping,
                 websocket_config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.identity = NodeIdentity()
        websocket_config = websocket_config or \
                           Configuration().get('localhive_websocket', {})
        callbacks = StatusCallbackMap(on_started=started_hook,
                                      on_alive=alive_hook,
                                      on_ready=ready_hook,
                                      on_error=error_hook,
                                      on_stopping=stopping_hook)

        self.status = ProcessStatus('LocalHive', callback_map=callbacks)
        self.host = websocket_config.get('host') or "0.0.0.0"
        self.port = websocket_config.get('port') or 6989

        self.bus = FakeBus()

    def run(self):
        self.status.set_alive()
        asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
        loop = ioloop.IOLoop.current()

        self.protocol = LocalHiveProtocol(loop=loop)  # TODO
        self.protocol.bind(LocalHiveBusEventHandler, self.bus)
        self.status.bind(self.bus)
        self.status.set_started()

        routes: list = [("/", LocalHiveBusEventHandler)]
        application = web.Application(routes)

        LOG.info("ws connection started")
        application.listen(self.port, self.host)

        self.status.set_ready()

        loop.start()

        self.status.set_stopping()
