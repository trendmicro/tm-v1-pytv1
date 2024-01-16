from __future__ import annotations

import logging
import threading
from functools import lru_cache
from logging import Logger
from typing import Any, Type

from . import api
from .core import Core
from .model.enums import Api
from .model.responses import BaseTaskResp, ConnectivityResp, T
from .results import Result

log: Logger = logging.getLogger(__name__)
lock = threading.Lock()


def init(
    name: str,
    token: str,
    url: str,
    pool_connections: int = 1,
    pool_maxsize: int = 1,
    connect_timeout: int = 30,
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
        self.alert = api.Alert(self._core)
        self.api_key = api.ApiKey(self._core)
        self.note = api.Note(self._core)
        self.script = api.CustomScript(self._core)
        self.object = api.Object(self._core)
        self.account = api.Account(self._core)
        self.email = api.Email(self._core)
        self.endpoint = api.Endpoint(self._core)
        self.sandbox = api.Sandbox(self._core)

    def check_connectivity(self) -> Result[ConnectivityResp]:
        """Checks the connection to the API service
        and verifies if your authentication token is valid.

        :rtype: Result[ConnectivityResp]
        """
        return self._core.send(ConnectivityResp, Api.CONNECTIVITY)

    def get_base_task_result(
        self,
        task_id: str,
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[BaseTaskResp]:
        """Retrieves the result of a response task.

        :param task_id: Task id.
        :type task_id: str
        :param poll: If we should wait until the task is finished before
         to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result
        to be available.
        :type poll_time_sec: float
        :rtype: Result[BaseTaskResultResp]:
        """
        return self._core.send_task_result(
            BaseTaskResp, task_id, poll, poll_time_sec
        )

    def get_task_result(
        self,
        task_id: str,
        class_: Type[T],
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[T]:
        """Retrieves the result of a response task.

        :param task_id: Task id.
        :type task_id: str
        :param class_: Expected task result class.
        :type class_: Type[T]
        :param poll: If we should wait until the task is finished before
         to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result
        to be available.
        :type poll_time_sec: float
        :rtype: Result[T]:
        """
        return self._core.send_task_result(
            class_, task_id, poll, poll_time_sec
        )
