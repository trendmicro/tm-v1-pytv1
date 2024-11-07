from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import Field, field_validator, model_validator

from .common import (
    Account,
    AlertNote,
    ApiKey,
    BaseConsumable,
    BaseModel,
    Digest,
    EmailActivity,
    EmailMessage,
    Endpoint,
    EndpointActivity,
    ExceptionObject,
    MsData,
    MsDataApiKey,
    MsDataUrl,
    OatEvent,
    OatPackage,
    OatPipeline,
    SaeAlert,
    SandboxSuspiciousObject,
    Script,
    SuspiciousObject,
    TaskError,
    TiAlert,
    get_object,
)
from .enum import (
    ObjectType,
    RiskLevel,
    SandboxAction,
    SandboxObjectType,
    Status,
)

C = TypeVar("C", bound=BaseConsumable)
M = TypeVar("M", bound=MsData)


class BaseResponse(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)


class BaseLinkableResp(BaseResponse, Generic[C]):
    next_link: Optional[str] = None
    items: List[C]

    @model_validator(mode="before")
    @classmethod
    def map_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data["items"]:
            data["items"] = []
        return data


class BaseMultiResponse(BaseResponse, Generic[M]):
    items: List[M]


class BaseStatusResponse(BaseResponse):
    id: str
    status: Status
    created_date_time: str
    last_action_date_time: str


class BaseTaskResp(BaseStatusResponse):
    action: str
    description: Optional[str] = None
    account: Optional[str] = None
    error: Optional[TaskError] = None


MR = TypeVar("MR", bound=BaseMultiResponse[Any])
R = TypeVar("R", bound=BaseResponse)
S = TypeVar("S", bound=BaseStatusResponse)
T = TypeVar("T", bound=BaseTaskResp)


class AccountTaskResp(BaseTaskResp):
    tasks: List[Account]


class AddAlertNoteResp(BaseResponse):
    note_id: str = Field(validation_alias="Location")

    @field_validator("note_id", mode="before")
    @classmethod
    def get_id(cls, value: str) -> str:
        return _get_id(value)


class AddCustomScriptResp(BaseResponse):
    script_id: str = Field(validation_alias="Location")

    @field_validator("script_id", mode="before")
    @classmethod
    def get_id(cls, value: str) -> str:
        return _get_id(value)


class BlockListTaskResp(BaseTaskResp):
    type: ObjectType
    value: str

    @model_validator(mode="before")
    @classmethod
    def map_data(cls, data: Dict[str, str]) -> Dict[str, str]:
        obj = get_object(data)
        if obj:
            data["type"] = obj[0]
            data["value"] = obj[1]
        return data


class BytesResp(BaseResponse):
    content: bytes


class CollectFileTaskResp(BaseTaskResp):
    agent_guid: str
    endpoint_name: str
    file_path: Optional[str] = None
    file_sha1: Optional[str] = None
    file_sha256: Optional[str] = None
    file_size: Optional[int] = None
    resource_location: Optional[str] = None
    expired_date_time: Optional[str] = None
    password: Optional[str] = None


class ConnectivityResp(BaseResponse):
    status: str


class ConsumeLinkableResp(BaseResponse, alias_generator=None):
    total_consumed: int


class EndpointTaskResp(BaseTaskResp):
    agent_guid: str
    endpoint_name: str


class GetAlertResp(BaseResponse):
    data: Union[SaeAlert, TiAlert]
    etag: str


class GetAlertNoteResp(BaseResponse):
    data: AlertNote
    etag: str


class GetApiKeyResp(BaseResponse):
    data: ApiKey
    etag: str


class GetOatPackageResp(BaseResponse):
    package: OatEvent


class GetPipelineResp(BaseResponse):
    data: OatPipeline
    etag: str


class ListAlertsResp(BaseLinkableResp[Union[SaeAlert, TiAlert]]):
    total_count: int
    count: int


class ListAlertNoteResp(BaseLinkableResp[AlertNote]): ...


class ListApiKeyResp(BaseLinkableResp[ApiKey]):
    total_count: int
    count: int


class ListCustomScriptsResp(BaseLinkableResp[Script]): ...


class ListEndpointActivityResp(BaseLinkableResp[EndpointActivity]):
    progress_rate: int


class GetEndpointActivitiesCountResp(BaseResponse):
    total_count: int


class ListEmailActivityResp(BaseLinkableResp[EmailActivity]):
    progress_rate: int


class GetEmailActivitiesCountResp(BaseResponse):
    total_count: int


class ListEndpointDataResp(BaseLinkableResp[Endpoint]): ...


class ListExceptionsResp(BaseLinkableResp[ExceptionObject]): ...


class ListOatsResp(BaseLinkableResp[OatEvent]):
    total_count: int
    count: int


class ListOatPipelinesResp(BaseResponse):
    items: List[OatPipeline]
    count: int


class ListOatPackagesResp(BaseLinkableResp[OatPackage]):
    total_count: int
    count: int
    requested_date_time: str
    latest_package_created_date_time: Optional[str] = None


class ListSuspiciousResp(BaseLinkableResp[SuspiciousObject]): ...


class MultiResp(BaseMultiResponse[MsData]): ...


class MultiUrlResp(BaseMultiResponse[MsDataUrl]): ...


class MultiApiKeyResp(BaseMultiResponse[MsDataApiKey]): ...


class NoContentResp(BaseResponse): ...


class EmailMessageTaskResp(BaseTaskResp):
    tasks: List[EmailMessage]


class CustomScriptTaskResp(BaseTaskResp):
    file_name: str
    agent_guid: str
    endpoint_name: str
    parameter: Optional[str] = None
    resource_location: Optional[str] = None
    expired_date_time: Optional[str] = None
    password: Optional[str] = None


class OatPipelineResp(BaseResponse):
    pipeline_id: str = Field(validation_alias="Location")

    @field_validator("pipeline_id", mode="before")
    @classmethod
    def get_id(cls, value: str) -> str:
        return _get_id(value)


class SubmitFileToSandboxResp(BaseResponse):
    id: str
    digest: Digest
    arguments: Optional[str] = None


class SandboxAnalysisResultResp(BaseResponse):
    id: str
    type: SandboxObjectType
    analysis_completion_date_time: str
    risk_level: RiskLevel
    true_file_type: Optional[str] = None
    digest: Optional[Digest] = None
    arguments: Optional[str] = None
    detection_names: List[str] = Field(default=[])
    threat_types: List[str] = Field(default=[])


class SandboxSubmissionStatusResp(BaseStatusResponse):
    action: SandboxAction
    resource_location: Optional[str] = None
    is_cached: Optional[bool] = None
    digest: Optional[Digest] = None
    arguments: Optional[str] = None


class ListSandboxSuspiciousResp(BaseResponse):
    items: List[SandboxSuspiciousObject]


class SandboxSubmitUrlTaskResp(BaseTaskResp):
    url: str
    sandbox_task_id: str


class TerminateProcessTaskResp(BaseTaskResp):
    agent_guid: str
    endpoint_name: str
    file_sha1: str
    file_name: Optional[str] = None


class TextResp(BaseResponse):
    text: str


def _get_id(location: str) -> str:
    return location.split("/")[-1]
