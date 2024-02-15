from typing import Callable, List, Optional

from .. import utils
from ..core import Core
from ..model.common import Endpoint as Ept
from ..model.common import EndpointActivity
from ..model.enum import Api, QueryOp, SearchMode
from ..model.request import (
    CollectFileRequest,
    EndpointRequest,
    TerminateProcessRequest,
)
from ..model.response import (
    ConsumeLinkableResp,
    GetEndpointActivitiesCountResp,
    ListEndpointActivityResp,
    ListEndpointDataResp,
    MultiResp,
)
from ..result import MultiResult, Result


class Endpoint:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def isolate(self, *endpoints: EndpointRequest) -> MultiResult[MultiResp]:
        """Disconnects one or more endpoints from the network
        but allows communication with the managing Trend Micro server product.

        :param endpoints: Endpoint(s) to isolate.
        :type endpoints: Tuple[EndpointTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_endpoint(Api.ISOLATE_ENDPOINT, *endpoints)

    def restore(self, *endpoints: EndpointRequest) -> MultiResult[MultiResp]:
        """Restores network connectivity to one or more endpoints that applied
        the "Isolate endpoint" action.

        :param endpoints: Endpoint(s) to restore.
        :type endpoints: Tuple[EndpointTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_endpoint(Api.RESTORE_ENDPOINT, *endpoints)

    def collect_file(
        self, *files: CollectFileRequest
    ) -> MultiResult[MultiResp]:
        """Collects a file from one or more endpoints and then sends the files
        to Vision One in a password-protected archive.

        :param files: File(s) to collect.
        :type files: Tuple[FileTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_endpoint(Api.COLLECT_ENDPOINT_FILE, *files)

    def terminate_process(
        self, *processes: TerminateProcessRequest
    ) -> MultiResult[MultiResp]:
        """Terminates a process that is running on one or more endpoints.

        :param processes: Process(es) to terminate.
        :type processes: Tuple[ProcessTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_endpoint(
            Api.TERMINATE_ENDPOINT_PROCESS, *processes
        )

    def get_activity_count(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        select: Optional[List[str]] = None,
        top: int = 500,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[GetEndpointActivitiesCountResp]:
        """Retrieves the count of endpoint activity data in a paginated list
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
        :param op: Operator to apply between fields (ie: dpt=... OR src=...)
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: dpt="443")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[GetEndpointActivityDataCountResp]:
        """
        return self._core.send(
            GetEndpointActivitiesCountResp,
            Api.GET_ENDPOINT_ACTIVITY_DATA,
            params=utils.build_activity_request(
                start_time,
                end_time,
                select,
                top,
                SearchMode.COUNT_ONLY,
            ),
            headers=utils.tmv1_activity_query(op, fields),
        )

    def list_data(
        self, op: QueryOp = QueryOp.AND, **fields: str
    ) -> Result[ListEndpointDataResp]:
        """Retrieves endpoints in a paginated list filtered by provided values.

        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:ip="1.1.1.1")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[GetEndpointDataResp]:
        """
        return self._core.send(
            ListEndpointDataResp,
            Api.GET_ENDPOINT_DATA,
            headers=utils.tmv1_query(op, fields),
        )

    def list_activity(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        select: Optional[List[str]] = None,
        top: int = 500,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListEndpointActivityResp]:
        """Retrieves endpoint activity data in a paginated list
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
        :param op: Operator to apply between fields (ie: dpt=... OR src=...)
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: dpt="443")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[GetEndpointActivityDataResp]:
        """
        return self._core.send(
            ListEndpointActivityResp,
            Api.GET_ENDPOINT_ACTIVITY_DATA,
            params=utils.build_activity_request(
                start_time,
                end_time,
                select,
                top,
                SearchMode.DEFAULT,
            ),
            headers=utils.tmv1_activity_query(op, fields),
        )

    def consume_data(
        self,
        consumer: Callable[[Ept], None],
        op: QueryOp,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume endpoints.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[Endpoint], None]
        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:ip="1.1.1.1")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[ConsumeLinkableResp]:
        """
        return self._core.send_linkable(
            ListEndpointDataResp,
            Api.GET_ENDPOINT_DATA,
            consumer,
            headers=utils.tmv1_query(op, fields),
        )

    def consume_activity(
        self,
        consumer: Callable[[EndpointActivity], None],
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        select: Optional[List[str]] = None,
        top: int = 500,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume endpoint activity data in a paginated list
         filtered by provided values.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[EndpointActivity], None]
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
        :param op: Operator to apply between fields (ie: dpt=... OR src=...)
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: dpt="443")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[ConsumeLinkableResp]:
        """
        return self._core.send_linkable(
            ListEndpointActivityResp,
            Api.GET_ENDPOINT_ACTIVITY_DATA,
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
