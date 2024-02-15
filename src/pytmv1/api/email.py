from typing import Callable, List, Optional, Union

from .. import utils
from ..core import Core
from ..model.common import EmailActivity
from ..model.enum import Api, QueryOp, SearchMode
from ..model.request import EmailMessageIdRequest, EmailMessageUIdRequest
from ..model.response import (
    ConsumeLinkableResp,
    GetEmailActivitiesCountResp,
    ListEmailActivityResp,
    MultiResp,
)
from ..result import MultiResult, Result


class Email:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def quarantine(
        self, *messages: Union[EmailMessageUIdRequest, EmailMessageIdRequest]
    ) -> MultiResult[MultiResp]:
        """Quarantine a message from one or more mailboxes.

        :param messages: Message(s) to quarantine.
        :type messages: Tuple[EmailUIdTask, EmailMsgIdTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.QUARANTINE_EMAIL_MESSAGE,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in messages
            ],
        )

    def restore(
        self, *messages: Union[EmailMessageUIdRequest, EmailMessageIdRequest]
    ) -> MultiResult[MultiResp]:
        """Restore quarantined email message(s).

        :param messages: Message(s) to restore.
        :type messages: Tuple[EmailUIdTask, EmailMsgIdTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.RESTORE_EMAIL_MESSAGE,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in messages
            ],
        )

    def delete(
        self, *messages: Union[EmailMessageUIdRequest, EmailMessageIdRequest]
    ) -> MultiResult[MultiResp]:
        """Deletes a message from one or more mailboxes.

        :param messages: Message(s) to delete.
        :type messages: Tuple[EmailUIdTask, EmailMsgIdTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.DELETE_EMAIL_MESSAGE,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in messages
            ],
        )

    def get_activity_count(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        select: Optional[List[str]] = None,
        top: int = 500,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[GetEmailActivitiesCountResp]:
        """Retrieves the count of email activity data in a paginated list
         filtered by provided values.

        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param select: List of fields to include in the search results,
        if no fields are specified, the query returns all supported fields.
        :type select: Optional[List[str]]
        :param top: Number of records fetched per page.
        :type top: int
        :param op: Operator to apply between fields (ie: uuid=... OR tags=...)
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: uuid="123456")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[GetEmailActivityDataCountResp]:
        """
        return self._core.send(
            GetEmailActivitiesCountResp,
            Api.GET_EMAIL_ACTIVITY_DATA,
            params=utils.build_activity_request(
                start_time,
                end_time,
                select,
                top,
                SearchMode.COUNT_ONLY,
            ),
            headers=utils.tmv1_activity_query(op, fields),
        )

    def list_activity(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        select: Optional[List[str]] = None,
        top: int = 500,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListEmailActivityResp]:
        """Retrieves email activity data in a paginated list
         filtered by provided values.

        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param select: List of fields to include in the search results,
        if no fields are specified, the query returns all supported fields.
        :type select: Optional[List[str]]
        :param top: Number of records fetched per page.
        :type top: int
        :param op: Operator to apply between fields (ie: uuid=... OR tags=...)
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: uuid="123456")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[GetEmailActivityDataResp]:
        """
        return self._core.send(
            ListEmailActivityResp,
            Api.GET_EMAIL_ACTIVITY_DATA,
            params=utils.build_activity_request(
                start_time,
                end_time,
                select,
                top,
                SearchMode.DEFAULT,
            ),
            headers=utils.tmv1_activity_query(op, fields),
        )

    def consume_activity(
        self,
        consumer: Callable[[EmailActivity], None],
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        select: Optional[List[str]] = None,
        top: int = 500,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume email activity data in a paginated list
         filtered by provided values.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[EmailActivity], None]
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param select: List of fields to include in the search results,
        if no fields are specified, the query returns all supported fields.
        :type select: Optional[List[str]]
        :param top: Number of records fetched per page.
        :type top: int
        :param op: Operator to apply between fields (ie: uuid=... OR tags=...)
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: uuid="123456")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[ConsumeLinkableResp]:
        """
        return self._core.send_linkable(
            ListEmailActivityResp,
            Api.GET_EMAIL_ACTIVITY_DATA,
            consumer,
            params=utils.build_activity_request(
                start_time,
                end_time,
                select,
                top,
                SearchMode.DEFAULT,
            ),
            headers=utils.tmv1_activity_query(op, fields),
        )
