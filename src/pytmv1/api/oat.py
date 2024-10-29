from typing import Callable, List, Optional

from .. import utils
from ..core import Core
from ..model.common import OatEvent, OatPackage
from ..model.enum import Api, HttpMethod, OatRiskLevel, QueryOp
from ..model.response import (
    ConsumeLinkableResp,
    GetOatPackageResp,
    GetPipelineResp,
    ListOatPackagesResp,
    ListOatPipelinesResp,
    ListOatsResp,
    MultiResp,
    NoContentResp,
    OatPipelineResp,
)
from ..result import MultiResult, Result


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
    ) -> Result[ConsumeLinkableResp]:
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
        :rtype: Result[ConsumeLinkableResp]
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

    def create_pipeline(
        self,
        has_detail: bool,
        risk_levels: List[OatRiskLevel],
        description: Optional[str] = None,
    ) -> Result[OatPipelineResp]:
        """Registers a customer
        to the Observed Attack Techniques data pipeline.

        :param has_detail: Retrieve detailed logs from the OAT data pipeline.
        :type has_detail: bool
        :param risk_levels: Risk levels to include in the results,
        requests must include at least one risk level.
        :type risk_levels: List[OatRiskLevel]
        :param description: Notes or comments about the pipeline.
        :type description: Optional[str]
        :return: Result[PipelineResp]
        """
        return self._core.send(
            OatPipelineResp,
            Api.CREATE_OAT_PIPELINE,
            HttpMethod.POST,
            json=utils.filter_none(
                {
                    "hasDetail": has_detail,
                    "riskLevels": risk_levels,
                    "description": description,
                }
            ),
        )

    def get_pipeline(self, pipeline_id: str) -> Result[GetPipelineResp]:
        """Displays the settings of the specified data pipeline.

        :param pipeline_id: Pipeline ID.
        :type pipeline_id: str
        :return: Result[GetPipelineResp]
        """
        return self._core.send(
            GetPipelineResp, Api.GET_OAT_PIPELINE.value.format(pipeline_id)
        )

    def update_pipeline(
        self,
        pipeline_id: str,
        etag: str,
        has_detail: Optional[bool] = None,
        risk_levels: Optional[List[OatRiskLevel]] = None,
        description: Optional[str] = None,
    ) -> Result[NoContentResp]:
        """Modifies the settings of the specified data pipeline.

        :param pipeline_id: Pipeline ID.
        :type pipeline_id: str
        :param etag: ETag of the resource you want to update.
        :type etag: str
        :param has_detail: Retrieve detailed logs from the OAT data pipeline.
        :type has_detail: Optional[bool]
        :param risk_levels: Risk levels to include in the results,
        requests must include at least one risk level.
        :type risk_levels: Optional[List[OatRiskLevel]]
        :param description: Notes or comments about the pipeline.
        :type description: Optional[str]
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.UPDATE_OAT_PIPELINE.value.format(pipeline_id),
            HttpMethod.PATCH,
            json=utils.filter_none(
                {
                    "hasDetail": has_detail,
                    "riskLevels": risk_levels,
                    "description": description,
                }
            ),
            headers={
                "If-Match": (etag[1:-1] if etag.startswith('"') else etag)
            },
        )

    def delete_pipelines(self, *pipeline_ids: str) -> MultiResult[MultiResp]:
        """Unregisters a customer
        from the Observed Attack Techniques data pipeline(s).

        :param pipeline_ids: Pipeline IDs.
        :type pipeline_ids: List[str]
        :return: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.DELETE_OAT_PIPELINE,
            json=[{"id": pipeline_id} for pipeline_id in pipeline_ids],
        )

    def list_pipelines(self) -> Result[ListOatPipelinesResp]:
        """Displays all data pipelines that have registered users.

        :return: Result[ListOatPipelineResp]
        """
        return self._core.send(ListOatPipelinesResp, Api.LIST_OAT_PIPELINE)

    def get_package(
        self, pipeline_id: str, package_id: str
    ) -> Result[GetOatPackageResp]:
        """Retrieves the specified Observed Attack Techniques package.

        :param pipeline_id: Pipeline ID.
        :type pipeline_id: str
        :param package_id: Package ID.
        :type package_id: str
        :return: Result[GetOatPackageResp]
        """
        return self._core.send(
            GetOatPackageResp,
            Api.DOWNLOAD_OAT_PACKAGE.value.format(pipeline_id, package_id),
        )

    def list_packages(
        self,
        pipeline_id: str,
        start_date_time: Optional[str] = None,
        end_date_time: Optional[str] = None,
        top: int = 500,
    ) -> Result[ListOatPackagesResp]:
        """Displays all the available packages from a data pipeline
         in a paginated list.

        :param pipeline_id: Pipeline ID.
        :type pipeline_id: str
        :param start_date_time: Date that indicates the start of
        the data retrieval time range. (yyyy-MM-ddThh:mm:ssZ).
        :type start_date_time: Optional[str]
        :param end_date_time: Date that indicates the end of
        the data retrieval time range. (yyyy-MM-ddThh:mm:ssZ).
        :type end_date_time: Optional[str]
        :param top: Number of records displayed on a page.
        :type top: int
        :return: Result[ListOatPackagesResp]
        """
        return self._core.send(
            ListOatPackagesResp,
            Api.LIST_OAT_PACKAGE.value.format(pipeline_id),
            params=utils.filter_none(
                {
                    "startDateTime": start_date_time,
                    "endDateTime": end_date_time,
                    "top": top,
                }
            ),
        )

    def consume_packages(
        self,
        pipeline_id: str,
        consumer: Callable[[OatPackage], None],
        start_date_time: Optional[str] = None,
        end_date_time: Optional[str] = None,
        top: int = 500,
    ) -> Result[ConsumeLinkableResp]:
        """Displays and consume all the available packages from a data pipeline
         in a paginated list.

        :param pipeline_id: Pipeline ID.
        :type pipeline_id: str
        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[OatPackage], None]
        :param start_date_time: Date that indicates the start of
        the data retrieval time range. (yyyy-MM-ddThh:mm:ssZ).
        :type start_date_time: Optional[str]
        :param end_date_time: Date that indicates the end of
        the data retrieval time range. (yyyy-MM-ddThh:mm:ssZ).
        :type end_date_time: Optional[str]
        :param top: Number of records displayed on a page.
        :type top: int
        :return: Result[ConsumeLinkableResp]
        """
        return self._core.send_linkable(
            ListOatPackagesResp,
            Api.LIST_OAT_PACKAGE.value.format(pipeline_id),
            consumer,
            params=utils.filter_none(
                {
                    "startDateTime": start_date_time,
                    "endDateTime": end_date_time,
                    "top": top,
                }
            ),
        )
