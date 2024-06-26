import typing
from typing import Any

from requests.adapters import DEFAULT_POOLBLOCK
from requests.adapters import HTTPAdapter as AdapterUrllib
from urllib3.connectionpool import HTTPConnectionPool as HTTPUrllib
from urllib3.connectionpool import HTTPSConnectionPool as HTTPSUrllib
from urllib3.poolmanager import PoolManager as ManagerUrllib


class HTTPConnectionPool(HTTPUrllib):
    @typing.no_type_check
    def urlopen(self, method, url, **kwargs):
        return super().urlopen(
            method,
            url,
            pool_timeout=5,
            **kwargs,
        )


class HTTPSConnectionPool(HTTPSUrllib, HTTPConnectionPool): ...


class PoolManager(ManagerUrllib):
    def __init__(
        self,
        **connection_pool_kw: Any,
    ):
        super().__init__(**connection_pool_kw)
        self.pool_classes_by_scheme = {
            "http": HTTPConnectionPool,
            "https": HTTPSConnectionPool,
        }


class HTTPAdapter(AdapterUrllib):
    @typing.no_type_check
    def init_poolmanager(
        self, connections, maxsize, block=DEFAULT_POOLBLOCK, **pool_kwargs
    ) -> None:
        super().init_poolmanager(connections, maxsize, block, **pool_kwargs)
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            **pool_kwargs,
        )
