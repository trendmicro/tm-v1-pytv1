from typing import Callable, Optional

from .. import utils
from ..core import Core
from ..model.common import OatEvent
from ..model.enum import Api, QueryOp
from ..model.response import ListOatsResp
from ..result import Result


class Oat:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def list(
        self,
        detected_start_date_time: Optional[str] = None,
        detected_end_date_time: Optional[str] = None,
        ingested_start_date_time: Optional[str] = None,
        ingested_end_date_time: Optional[str] = None,
        top: int = 50,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListOatsResp]:
        """Retrieves Observed Attack Techniques events in a paginated list.

        :param detected_start_date_time: Date that indicates the start of
        the event detection data retrieval time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type detected_start_date_time: Optional[str]
        :param detected_end_date_time: Date that indicates the end of
        the event detection data retrieval time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type detected_end_date_time: Optional[str]
        :param ingested_start_date_time: Date that indicates the start of
        the data ingestion time range (yyyy-MM-ddThh:mm:ssZ).
        :type ingested_start_date_time: Optional[str]
        :param ingested_end_date_time: Date that indicates the end of
        the data ingestion time range (yyyy-MM-ddThh:mm:ssZ).
        :type ingested_end_date_time: Optional[str]
        :param top: Number of records displayed on a page.
        :type top: int
        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:uuid="123"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[ListOatsResp]
        """
        return self._core.send(
            ListOatsResp,
            Api.GET_OAT_LIST,
            params=utils.filter_none(
                {
                    "detectedStartDateTime": detected_start_date_time,
                    "detectedEndDateTime": detected_end_date_time,
                    "ingestedStartDateTime": ingested_start_date_time,
                    "ingestedEndDateTime": ingested_end_date_time,
                    "top": top,
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def consume(
        self,
        consumer: Callable[[OatEvent], None],
        detected_start_date_time: Optional[str] = None,
        detected_end_date_time: Optional[str] = None,
        ingested_start_date_time: Optional[str] = None,
        ingested_end_date_time: Optional[str] = None,
        top: int = 50,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListOatsResp]:
        """Retrieves and consume OAT events.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[Oat], None]
        :param detected_start_date_time: Date that indicates the start of
        the event detection data retrieval time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type detected_start_date_time: Optional[str]
        :param detected_end_date_time: Date that indicates the end of
        the event detection data retrieval time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type detected_end_date_time: Optional[str]
        :param ingested_start_date_time: Date that indicates the start of
        the data ingestion time range (yyyy-MM-ddThh:mm:ssZ).
        :type ingested_start_date_time: Optional[str]
        :param ingested_end_date_time: Date that indicates the end of
        the data ingestion time range (yyyy-MM-ddThh:mm:ssZ).
        :type ingested_end_date_time: Optional[str]
        :param top: Number of records displayed on a page.
        :type top: int
        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:uuid="123"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[ListOatsResp]
        """
        return self._core.send_linkable(
            ListOatsResp,
            Api.GET_OAT_LIST,
            consumer,
            params=utils.filter_none(
                {
                    "detectedStartDateTime": detected_start_date_time,
                    "detectedEndDateTime": detected_end_date_time,
                    "ingestedStartDateTime": ingested_start_date_time,
                    "ingestedEndDateTime": ingested_end_date_time,
                    "top": top,
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )
