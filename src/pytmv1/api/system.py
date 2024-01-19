from ..core import Core
from ..model.enum import Api
from ..model.response import ConnectivityResp
from ..result import Result


class System:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def check_connectivity(self) -> Result[ConnectivityResp]:
        """Checks the connection to the API service
        and verifies if your authentication token is valid.

        :rtype: Result[ConnectivityResp]
        """
        return self._core.send(ConnectivityResp, Api.CONNECTIVITY)
