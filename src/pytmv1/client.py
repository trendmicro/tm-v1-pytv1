from __future__ import annotations

import logging
import threading
from functools import lru_cache
from logging import Logger
from typing import Any

from . import api
from .core import Core

log: Logger = logging.getLogger(__name__)
lock = threading.Lock()


def init(
    name: str,
    token: str,
    url: str,
    pool_connections: int = 1,
    pool_maxsize: int = 1,
    connect_timeout: int = 10,
    read_timeout: int = 30,
) -> Client:
    """Synchronized Helper function to initialize a :class:`Client`.

    :param name: Identify the application using this library.
    :type name: str
    :param token: Authentication token created for your account.
    :type token: str
    :param url: Vision One API url this client connects to.
    :type url: str
    :param pool_connections: (optional) Number of connection to cache.
    :type pool_connections: int
    :param pool_maxsize: (optional) Maximum size of the pool.
    :type pool_maxsize: int
    :param connect_timeout: (optional) Seconds before connection timeout.
    :type connect_timeout: int
    :param read_timeout: (optional) Seconds before read timeout.
    :type connect_timeout: int
    :rtype: Client
    """
    lock.acquire()
    _cl = _client(
        appname=name,
        token=token,
        url=url,
        pool_connections=pool_connections,
        pool_maxsize=pool_maxsize,
        connect_timeout=connect_timeout,
        read_timeout=read_timeout,
    )
    lock.release()
    return _cl


@lru_cache(maxsize=1)
def _client(**kwargs: Any) -> Client:
    log.debug(
        "Initializing new client with [Appname=%s, Token=*****, URL=%s]",
        kwargs["appname"],
        kwargs["url"],
    )
    return Client(Core(**kwargs))


class Client:
    def __init__(self, core: Core):
        self._core = core
        self.account = api.Account(self._core)
        self.alert = api.Alert(self._core)
        self.api_key = api.ApiKey(self._core)
        self.email = api.Email(self._core)
        self.endpoint = api.Endpoint(self._core)
        self.note = api.Note(self._core)
        self.oat = api.Oat(self._core)
        self.object = api.Object(self._core)
        self.sandbox = api.Sandbox(self._core)
        self.script = api.CustomScript(self._core)
        self.system = api.System(self._core)
        self.task = api.Task(self._core)
