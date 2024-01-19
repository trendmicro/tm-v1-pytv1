from typing import Callable, Optional, Union

from .. import utils
from ..core import Core
from ..model.common import SaeAlert, TiAlert
from ..model.enum import Api, HttpMethod, InvestigationStatus, QueryOp
from ..model.response import (
    ConsumeLinkableResp,
    GetAlertResp,
    ListAlertsResp,
    NoContentResp,
)
from ..result import Result


class Alert:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def update_status(
        self,
        alert_id: str,
        status: InvestigationStatus,
        if_match: str,
    ) -> Result[NoContentResp]:
        """Edit the status of an alert or investigation triggered in Workbench.

        :param alert_id: Workbench alert id.
        :type alert_id: str
        :param status: Status to be updated.
        :type status: InvestigationStatus
        :param if_match: Target resource will be updated only if
         it matches ETag of the target one.
        :type if_match: str
        :rtype: Result[NoContentResp]:
        """
        return self._core.send(
            NoContentResp,
            Api.UPDATE_ALERT_STATUS.value.format(alert_id),
            HttpMethod.PATCH,
            json={"investigationStatus": status},
            headers={
                "If-Match": (
                    if_match
                    if if_match.startswith('"')
                    else '"' + if_match + '"'
                )
            },
        )

    def get(self, alert_id: str) -> Result[GetAlertResp]:
        """Displays information about the specified alert.

        :param alert_id: Workbench alert id.
        :type alert_id: str
        :rtype: Result[GetAlertDetailsResp]:
        """
        return self._core.send(
            GetAlertResp,
            Api.GET_ALERT.value.format(alert_id),
        )

    def list(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListAlertsResp]:
        """Retrieves workbench alerts in a paginated list.

        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:fileName="1.sh"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[GetAlertListResp]:
        """
        return self._core.send(
            ListAlertsResp,
            Api.GET_ALERT_LIST,
            params=utils.filter_none(
                {
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def consume(
        self,
        consumer: Callable[[Union[SaeAlert, TiAlert]], None],
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume workbench alerts.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[Union[SaeAlert, TiAlert]], None]
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :rtype: Result[ConsumeLinkableResp]:
        """
        return self._core.send_linkable(
            ListAlertsResp,
            Api.GET_ALERT_LIST,
            consumer,
            params=utils.filter_none(
                {
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                }
            ),
        )
