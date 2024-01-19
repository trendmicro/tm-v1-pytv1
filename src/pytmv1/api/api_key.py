from __future__ import annotations

from typing import Callable, Optional

from .. import utils
from ..core import Core
from ..model.common import ApiKey as Apk
from ..model.enum import Api, ApiStatus, HttpMethod, QueryOp
from ..model.request import ApiKeyRequest
from ..model.response import (
    ConsumeLinkableResp,
    GetApiKeyResp,
    ListApiKeyResp,
    MultiApiKeyResp,
    MultiResp,
    NoContentResp,
)
from ..result import MultiResult, Result


class ApiKey:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def create(
        self,
        *keys: ApiKeyRequest,
    ) -> MultiResult[MultiApiKeyResp]:
        """Generates API keys designed to access Trend Vision One APIs.

        :param keys: API Key(s) to create.
        :type keys: Tuple[ApiKeyTask, ...]
        :return: MultiResult[MultiApiKeyResp]
        """
        return self._core.send_multi(
            MultiApiKeyResp,
            Api.CREATE_API_KEYS,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in keys
            ],
        )

    def get(self, key_id: str) -> Result[GetApiKeyResp]:
        """Retrieves the specified API key.

        :param key_id: Identifier of the API key.
        :type key_id: str
        :return: Result[GetApiKeyDetailsResp]
        """
        return self._core.send(
            GetApiKeyResp, Api.GET_API_KEY.value.format(key_id)
        )

    def update(
        self,
        key_id: str,
        etag: str,
        role: Optional[str] = None,
        name: Optional[str] = None,
        status: Optional[ApiStatus] = None,
        description: Optional[str] = None,
    ) -> Result[NoContentResp]:
        """Updates the specified API key.

        :param key_id: Identifier of the API key.
        :type key_id: str
        :param etag: ETag of the resource you want to update.
        :type etag: str
        :param role: User role assigned to the API key.
        :type role: Optional[str]
        :param name: Unique name of the API key.
        :type name: Optional[str]
        :param status: Status of an API key.
        :type status: Optional[ApiStatus]
        :param description: A brief note about the API key
        :type description: str
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.UPDATE_API_KEY.value.format(key_id),
            HttpMethod.PATCH,
            headers={
                "If-Match": etag if not etag.startswith('"') else etag[1:-1]
            },
            json=utils.filter_none(
                {
                    "role": role,
                    "name": name,
                    "status": status,
                    "description": description,
                }
            ),
        )

    def delete(self, *key_ids: str) -> MultiResult[MultiResp]:
        """Deletes the specified API keys.

        :param key_ids: Identifier of the API keys.
        :type key_ids: List[str]
        :return: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.DELETE_API_KEYS,
            json=[{"id": key_id} for key_id in key_ids],
        )

    def list(
        self, top: int = 50, op: QueryOp = QueryOp.AND, **fields: str
    ) -> Result[ListApiKeyResp]:
        """Retrieves API keys in a paginated list.

        :param top: Number of records displayed on a page.
        :type top: int
        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: id="...")
        :type fields: Dict[str, str]
        check Vision One API documentation for full list of supported fields.
        :return: Result[GetApiKeyListResp]
        """
        return self._core.send(
            ListApiKeyResp,
            Api.GET_API_KEY_LIST,
            params={"orderBy": "createdDateTime desc", "top": top},
            headers=utils.tmv1_filter(op, fields),
        )

    def consume(
        self,
        consumer: Callable[[Apk], None],
        top: int = 50,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume API keys.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[ApiKey], None]
        :param top: Number of records displayed on a page.
        :type top: int
        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: id="...")
        :type fields: Dict[str, str]
        check Vision One API documentation for full list of supported fields.
        :return: Result[GetApiKeyListResp]
        """
        return self._core.send_linkable(
            ListApiKeyResp,
            Api.GET_API_KEY_LIST,
            consumer,
            params={"orderBy": "createdDateTime desc", "top": top},
            headers=utils.tmv1_filter(op, fields),
        )
