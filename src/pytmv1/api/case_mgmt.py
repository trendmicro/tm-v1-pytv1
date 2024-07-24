from typing import Callable, List, Optional

from .. import utils
from ..core import Core
from ..model.common import Case, CaseContent
from ..model.enum import (
    Api,
    CaseFindings,
    CaseHolder,
    CasePriority,
    CaseStatus,
    HttpMethod,
    QueryOp,
)
from ..model.response import (
    BytesResp,
    CaseAttachmentResp,
    CaseContentResp,
    CaseResp,
    ConsumeLinkableResp,
    GetCaseContentResp,
    GetCaseResp,
    ListCaseContentResp,
    ListCaseResp,
    NoContentResp,
)
from ..result import Result


class CaseMgmt:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def create(
        self,
        name: str,
        priority: CasePriority,
        ext_tck_alias: str,
        ext_tck_id: str,
        status: CaseStatus = CaseStatus.OPEN,
        description: Optional[str] = None,
        ext_tck_created_date_time: Optional[str] = None,
        holder: Optional[CaseHolder] = None,
        findings: Optional[CaseFindings] = None,
        associated_item_ids: Optional[List[str]] = None,
        related_case_ids: Optional[List[str]] = None,
    ) -> Result[CaseResp]:
        """Allows third-party ticketing systems
         to create new Case Management cases.

        :param name: User-defined name of the case.
        :type name: str
        :param priority: Priority level of the case.
        :type priority: CasePriority
        :param ext_tck_alias: Case ID in external ticketing system.
        :type ext_tck_alias: str
        :param ext_tck_id: Unique ID in external ticketing system.
        :type ext_tck_id: str
        :param status: Status of the case.
        :type status: CaseStatus
        :param description: User-defined description of the case.
        :type description: Optional[str]
        :param ext_tck_created_date_time: External ticket
        creation date (yyyy-MM-ddThh:mm:ssZ).
        :type ext_tck_created_date_time: Optional[str]
        :param holder: Current role of the owner of the case.
        :type holder: Optional[CaseHolder]
        :param findings: Investigation findings of the case.
        :type findings: Optional[CaseFindings]
        :param associated_item_ids: Alert/Incident IDs related to the case.
        :type associated_item_ids: Optional[List[str]]
        :param related_case_ids:  Case IDs related to the case.
        :type related_case_ids: Optional[List[str]]
        :return: Result[CaseResp]
        """
        return self._core.send(
            CaseResp,
            Api.CREATE_CASE,
            HttpMethod.POST,
            json=utils.filter_none(
                {
                    "name": name,
                    "priority": priority,
                    "externalTicketAlias": ext_tck_alias,
                    "externalTicketId": ext_tck_id,
                    "status": status,
                    "description": description,
                    "externalTicketCreatedDateTime": ext_tck_created_date_time,
                    "holder": holder,
                    "findings": findings,
                    "associatedItemIds": associated_item_ids,
                    "relatedCaseIds": related_case_ids,
                }
            ),
        )

    def get(self, case_id: str) -> Result[GetCaseResp]:
        """Allows third-party ticketing systems
        to get the details of the specified Case Management case.

        :param case_id:
        :type case_id: str
        :return: Result[GetCaseResp]
        """
        return self._core.send(GetCaseResp, Api.GET_CASE.value.format(case_id))

    def update(
        self,
        case_id: str,
        etag: str,
        name: Optional[str] = None,
        priority: Optional[CasePriority] = None,
        status: Optional[CaseStatus] = None,
        description: Optional[str] = None,
        ext_tck_created_date_time: Optional[str] = None,
        holder: Optional[CaseHolder] = None,
        findings: Optional[CaseFindings] = None,
        associated_item_ids: Optional[List[str]] = None,
        related_case_ids: Optional[List[str]] = None,
    ) -> Result[NoContentResp]:
        """Allows third-party ticketing systems
         to update the specified case.

        :param case_id: Case ID.
        :type case_id: str
        :param etag: ETag of the resource to be updated.
        :type etag: str
        :param name: User-defined name of the case.
        :type name: Optional[str]
        :param priority: Priority level of the case.
        :type priority: Optional[CasePriority]
        :param status: Status of the case.
        :type status: Optional[CaseStatus]
        :param description: User-defined description of the case.
        :type description: Optional[str]
        :param ext_tck_created_date_time: External ticket
        creation date (yyyy-MM-ddThh:mm:ssZ).
        :type ext_tck_created_date_time: Optional[str]
        :param holder: Current role of the owner of the case.
        :type holder: Optional[CaseHolder]
        :param findings: Investigation findings of the case.
        :type findings: Optional[CaseFindings]
        :param associated_item_ids: Alert/Incident IDs related to the case.
        :type associated_item_ids: Optional[List[str]]
        :param related_case_ids:  Case IDs related to the case.
        :type related_case_ids: Optional[List[str]]
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.UPDATE_CASE.value.format(case_id),
            HttpMethod.PATCH,
            headers={
                "If-Match": etag if not etag.startswith('"') else etag[1:-1]
            },
            json=utils.filter_none(
                {
                    "name": name,
                    "priority": priority,
                    "status": status,
                    "description": description,
                    "externalTicketCreatedDateTime": ext_tck_created_date_time,
                    "holder": holder,
                    "findings": findings,
                    "associatedItemIds": associated_item_ids,
                    "relatedCaseIds": related_case_ids,
                }
            ),
        )

    def list(
        self,
        top: Optional[int] = 50,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListCaseResp]:
        """Allows third-party ticketing systems
        to get a list of your Case Management cases.

        :param top: Number of records displayed on a page.
        :type top: int
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: id="...")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :return: Result[ListCaseResp]
        """
        return self._core.send(
            ListCaseResp,
            Api.GET_CASE_LIST,
            params=utils.filter_none(
                {
                    "top": top,
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def consume(
        self,
        consumer: Callable[[Case], None],
        top: Optional[int] = 50,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Allows third-party ticketing systems
        to retrieves and consume Case Management cases.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[Case], None]
        :param top: Number of records displayed on a page.
        :type top: int
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: id="...")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :return: Result[ConsumeLinkableResp]
        """
        return self._core.send_linkable(
            ListCaseResp,
            Api.GET_CASE_LIST,
            consumer,
            params=utils.filter_none(
                {
                    "top": top,
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def add_content(
        self,
        case_id: str,
        comment: str,
        attachment_ids: Optional[List[str]] = None,
    ) -> Result[CaseContentResp]:
        """Allows third-party ticketing systems
        to add content to a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param comment: Comment added to the note.
        :type comment: str
        :param attachment_ids: Attachment IDs from case notes,
        supports up to 5 attachments per note.
        :type attachment_ids: Optional[List[str]]
        :return: Result[CaseContentResp]
        """
        return self._core.send(
            CaseContentResp,
            Api.ADD_CASE_CONTENT.value.format(case_id),
            HttpMethod.POST,
            json=utils.filter_none(
                {"comment": comment, "attachmentIds": attachment_ids}
            ),
        )

    def get_content(
        self, case_id: str, content_id: str
    ) -> Result[GetCaseContentResp]:
        """Allows third-party ticketing systems
        to get the specified element of a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param content_id: Content ID.
        :type content_id: str
        :return: Result[GetCaseContentResp]
        """
        return self._core.send(
            GetCaseContentResp,
            Api.GET_CASE_CONTENT.value.format(case_id, content_id),
        )

    def update_content(
        self,
        case_id: str,
        content_id: str,
        etag: str,
        comment: Optional[str] = None,
        attachment_ids: Optional[List[str]] = None,
    ) -> Result[NoContentResp]:
        """Allows third-party ticketing systems
        to update the specified element of a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param content_id: Content ID.
        :type content_id: str
        :param etag: ETag of the resource to be updated.
        :type etag: str
        :param comment: Comment added to the note.
        :type comment: Optional[str]
        :param attachment_ids: Attachment IDs from case notes,
        supports up to 5 attachments per note.
        :type attachment_ids: Optional[List[str]]
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.UPDATE_CASE_CONTENT.value.format(case_id, content_id),
            HttpMethod.PATCH,
            headers={
                "If-Match": etag if not etag.startswith('"') else etag[1:-1]
            },
            json=utils.filter_none(
                {"comment": comment, "attachmentIds": attachment_ids}
            ),
        )

    def delete_content(
        self, case_id: str, content_id: str
    ) -> Result[NoContentResp]:
        """Allows third-party ticketing systems
        to delete the specified element from a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param content_id: Content ID.
        :type content_id: str
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.DELETE_CASE_CONTENT.value.format(case_id, content_id),
            HttpMethod.DELETE,
        )

    def list_content(
        self,
        case_id: str,
        top: Optional[int] = 50,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ListCaseContentResp]:
        """Allows third-party ticketing systems
        to get the contents of a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param top: Number of records displayed on a page.
        :type top: int
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: id="...")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :return: Result[ListCaseContentResp]
        """
        return self._core.send(
            ListCaseContentResp,
            Api.GET_CASE_CONTENT_LIST.value.format(case_id),
            params=utils.filter_none(
                {
                    "top": top,
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def consume_content(
        self,
        case_id: str,
        consumer: Callable[[CaseContent], None],
        top: Optional[int] = 50,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Allows third-party ticketing systems
        to retrieves and consume contents of Case Management cases.

        :param case_id: Case ID.
        :type case_id: str
        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[CaseContent], None]
        :param top: Number of records displayed on a page.
        :type top: int
        :param start_time: Date that indicates the start of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type start_time: Optional[str]
        :param end_time: Date that indicates the end of the data retrieval
        time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type end_time: Optional[str]
        :param op: Query operator to apply.
        :type op: QueryOp
        :param fields: Field/value used to filter result (ie: id="...")
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :return: Result[ConsumeLinkableResp]
        """
        return self._core.send_linkable(
            ListCaseContentResp,
            Api.GET_CASE_CONTENT_LIST.value.format(case_id),
            consumer,
            params=utils.filter_none(
                {
                    "top": top,
                    "startDateTime": start_time,
                    "endDateTime": end_time,
                    "orderBy": "createdDateTime desc",
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def add_attachment(
        self,
        case_id: str,
        file: bytes,
        file_name: str,
        ext_attachment_id: Optional[str] = None,
    ) -> Result[CaseAttachmentResp]:
        """Allows third-party ticketing systems
        to add attachments to a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param file: Raw content in bytes.
        :type file: bytes
        :param file_name: Name of the file.
        :type file_name: str
        :param ext_attachment_id: Attachment ID in external ticketing system.
        :type ext_attachment_id: Optional[str]
        :return: Result[CaseAttachmentResp]
        """
        return self._core.send(
            CaseAttachmentResp,
            Api.ADD_CASE_ATTACHMENT.value.format(case_id),
            HttpMethod.POST,
            data=utils.filter_none(
                {"externalAttachmentId": ext_attachment_id}
            ),
            files={"file": (file_name, file, "application/octet-stream")},
        )

    def download_attachment(
        self, case_id: str, attachment_id: str
    ) -> Result[BytesResp]:
        """Allows third-party ticketing systems
        to get the specified attachment from a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param attachment_id: Attachment ID.
        :type attachment_id: str
        :return: Result[BytesResp]
        """
        return self._core.send(
            BytesResp,
            Api.DOWNLOAD_CASE_ATTACHMENT.value.format(case_id, attachment_id),
        )

    def delete_attachment(
        self, case_id: str, attachment_id: str
    ) -> Result[NoContentResp]:
        """Allows third-party ticketing systems
        to delete the specified attachment from a Case Management case.

        :param case_id: Case ID.
        :type case_id: str
        :param attachment_id: Attachment ID.
        :type attachment_id: str
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.DELETE_CASE_ATTACHMENT.value.format(case_id, attachment_id),
            HttpMethod.DELETE,
        )
