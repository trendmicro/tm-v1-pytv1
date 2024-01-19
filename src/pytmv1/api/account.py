from pytmv1.core import Core
from pytmv1.model.enum import Api

from ..model.request import AccountRequest
from ..model.response import MultiResp
from ..result import MultiResult


class Account:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def disable(self, *accounts: AccountRequest) -> MultiResult[MultiResp]:
        """Signs the user out of all active application and browser sessions,
        and prevents the user from signing in any new session.

        :param accounts: Account(s) to disable.
        :type accounts: Tuple[AccountTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.DISABLE_ACCOUNT,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in accounts
            ],
        )

    def enable(self, *accounts: AccountRequest) -> MultiResult[MultiResp]:
        """Allows the user to sign in to new application and browser sessions.

        :param accounts: Account(s) to enable.
        :type accounts: Tuple[AccountTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.ENABLE_ACCOUNT,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in accounts
            ],
        )

    def reset(self, *accounts: AccountRequest) -> MultiResult[MultiResp]:
        """Signs the user out of all active application and browser sessions,
        and forces the user to create a new password during the next sign-in
        attempt.

        :param accounts: Account(s) to reset.
        :type accounts: Tuple[AccountTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.RESET_PASSWORD,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in accounts
            ],
        )

    def sign_out(self, *accounts: AccountRequest) -> MultiResult[MultiResp]:
        """Signs the user out of all active application and browser sessions.

        :param accounts: Account(s) to sign out.
        :type accounts: Tuple[AccountTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.SIGN_OUT_ACCOUNT,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in accounts
            ],
        )
