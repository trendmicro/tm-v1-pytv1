from typing import Callable, Optional

from .. import utils
from ..core import Core
from ..model.common import AlertNote
from ..model.enum import Api, HttpMethod, QueryOp
from ..model.response import (
    AddAlertNoteResp,
    ConsumeLinkableResp,
    GetAlertNoteResp,
    ListAlertNoteResp,
    NoContentResp,
)
from ..result import Result


class Note:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def create(
        self, alert_id: str, note_content: str
    ) -> Result[AddAlertNoteResp]:
        """Adds a note to the specified Workbench alert.

        :param alert_id: Workbench alert id.
        :type alert_id: str
        :param note_content: Value of the note.
        :type note_content: str
        :rtype: Result[AddAlertNoteResp]:
        """
        return self._core.send(
            AddAlertNoteResp,
            Api.ADD_ALERT_NOTE.value.format(alert_id),
            HttpMethod.POST,
            json={"content": note_content},
        )

    def update(
        self, alert_id: str, note_id: str, etag: str, note_content: str
    ) -> Result[NoContentResp]:
        """Updates the content of the specified Workbench alert note.

        :param alert_id: Workbench alert id.
        :type alert_id: str
        :param note_id: Workbench alert note id.
        :type note_id: str
        :param etag: Workbench alert note ETag.
        :param note_content: Content of the alert note.
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.UPDATE_ALERT_NOTE.value.format(alert_id, note_id),
            HttpMethod.PATCH,
            json={"content": note_content},
            headers={
                "If-Match": etag if etag.startswith('"') else '"' + etag + '"'
            },
        )

    def delete(
        self,
        alert_id: str,
        *note_ids: str,
    ) -> Result[NoContentResp]:
        """Deletes the specified notes from a Workbench alert.

        :param alert_id: Workbench alert id.
        :type alert_id: str
        :param note_ids: Workbench alert note ids.
        :type note_ids: Tuple[str, ...]
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.DELETE_ALERT_NOTE.value.format(alert_id),
            HttpMethod.POST,
            json=[{"id": note_id} for note_id in note_ids],
        )

    def get(self, alert_id: str, note_id: str) -> Result[GetAlertNoteResp]:
        """Retrieves the specified Workbench alert note.

        :param alert_id: Workbench alert id.
        :type alert_id: str
        :param note_id: Workbench alert note id.
        :type note_id: str
        :return:
        """
        return self._core.send(
            GetAlertNoteResp,
            Api.GET_ALERT_NOTE.value.format(alert_id, note_id),
        )

    def list(
        self,
        alert_id: str,
        top: int = 50,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListAlertNoteResp]:
        """Retrieves workbench alert notes in a paginated list.

        :param alert_id: Workbench alert id.
        :type alert_id: str
        :param top: Number of records fetched per page.
        :type top: int
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        :type end_time: Optional[str]
        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:id="1"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[GetAlertNoteListResp]:
        """
        return self._core.send(
            ListAlertNoteResp,
            Api.GET_ALERT_NOTE_LIST.value.format(alert_id),
            params=utils.filter_none(
                {
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                    "top": top,
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def consume(
        self,
        consumer: Callable[[AlertNote], None],
        alert_id: str,
        top: int = 50,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves workbench alert notes in a paginated list.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[AlertNote], None]
        :param alert_id: Workbench alert id.
        :type alert_id: str
        :param top: Number of records fetched per page.
        :type top: int
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        :type end_time: Optional[str]
        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:id="1"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[ConsumeLinkableResp]:
        """
        return self._core.send_linkable(
            ListAlertNoteResp,
            Api.GET_ALERT_NOTE_LIST.value.format(alert_id),
            consumer,
            params=utils.filter_none(
                {
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                    "top": top,
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )
