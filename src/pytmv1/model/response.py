from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import Field, model_validator

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
    SaeAlert,
    SandboxSuspiciousObject,
    Script,
    SuspiciousObject,
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


MR = TypeVar("MR", bound=BaseMultiResponse[Any])
R = TypeVar("R", bound=BaseResponse)
S = TypeVar("S", bound=BaseStatusResponse)
T = TypeVar("T", bound=BaseTaskResp)


class AccountTaskResp(BaseTaskResp):
    tasks: List[Account]


class AddAlertNoteResp(BaseResponse):
    note_id: str

    @model_validator(mode="before")
    @classmethod
    def map_data(cls, data: Dict[str, str]) -> Dict[str, str]:
        location = data.get("Location")
        if location:
            data["note_id"] = location.split("/")[-1]
        return data


class AddCustomScriptResp(BaseResponse):
    script_id: str

    @model_validator(mode="before")
    @classmethod
    def map_data(cls, data: Dict[str, str]) -> Dict[str, str]:
        location = data.get("Location")
        if location:
            data["script_id"] = location.split("/")[-1]
        return data


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


class ListAlertsResp(BaseLinkableResp[Union[SaeAlert, TiAlert]]):
    total_count: int
    count: int


class ListAlertNoteResp(BaseLinkableResp[AlertNote]):
    ...


class ListApiKeyResp(BaseLinkableResp[ApiKey]):
    total_count: int
    count: int


class ListCustomScriptsResp(BaseLinkableResp[Script]):
    ...


class ListEndpointActivityResp(BaseLinkableResp[EndpointActivity]):
    progress_rate: int


class GetEndpointActivitiesCountResp(BaseResponse):
    total_count: int


class ListEmailActivityResp(BaseLinkableResp[EmailActivity]):
    progress_rate: int


class GetEmailActivitiesCountResp(BaseResponse):
    total_count: int


class ListEndpointDataResp(BaseLinkableResp[Endpoint]):
    ...


class ListExceptionsResp(BaseLinkableResp[ExceptionObject]):
    ...


class ListOatsResp(BaseLinkableResp[OatEvent]):
    total_count: int
    count: int


class ListSuspiciousResp(BaseLinkableResp[SuspiciousObject]):
    ...


class MultiResp(BaseMultiResponse[MsData]):
    ...


class MultiUrlResp(BaseMultiResponse[MsDataUrl]):
    ...


class MultiApiKeyResp(BaseMultiResponse[MsDataApiKey]):
    ...


class NoContentResp(BaseResponse):
    ...


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


class TaskAction(Enum):
    COLLECT_FILE = ("collectFile", CollectFileTaskResp)
    COLLECT_EVIDENCE = ("collectEvidence", None)
    COLLECT_NETWORK_ANALYSIS_PACKAGE = ("collectNetworkAnalysisPackage", None)
    ISOLATE_ENDPOINT = ("isolate", EndpointTaskResp)
    ISOLATE_ENDPOINT_MULTIPLE = ("isolateForMultiple", None)
    RESTORE_ENDPOINT = ("restoreIsolate", EndpointTaskResp)
    RESTORE_ENDPOINT_MULTIPLE = ("restoreIsolateForMultiple", None)
    TERMINATE_PROCESS = ("terminateProcess", TerminateProcessTaskResp)
    DUMP_PROCESS_MEMORY = ("dumpProcessMemory", None)
    QUARANTINE_MESSAGE = ("quarantineMessage", EmailMessageTaskResp)
    DELETE_MESSAGE = ("deleteMessage", EmailMessageTaskResp)
    RESTORE_MESSAGE = ("restoreMessage", EmailMessageTaskResp)
    BLOCK_SUSPICIOUS = ("block", BlockListTaskResp)
    REMOVE_SUSPICIOUS = ("restoreBlock", BlockListTaskResp)
    RESET_PASSWORD = ("resetPassword", AccountTaskResp)
    SUBMIT_SANDBOX = ("submitSandbox", SandboxSubmitUrlTaskResp)
    ENABLE_ACCOUNT = ("enableAccount", AccountTaskResp)
    DISABLE_ACCOUNT = ("disableAccount", AccountTaskResp)
    FORCE_SIGN_OUT = ("forceSignOut", AccountTaskResp)
    REMOTE_SHELL = ("remoteShell", None)
    RUN_INVESTIGATION_KIT = ("runInvestigationKit", None)
    RUN_CUSTOM_SCRIPT = ("runCustomScript", CustomScriptTaskResp)
    RUN_CUSTOM_SCRIPT_MULTIPLE = ("runCustomScriptForMultiple", None)
    RUN_OS_QUERY = ("runOsquery", None)
    RUN_YARA_RULES = ("runYaraRules", None)

    def __init__(self, action: str, class_: Optional[Type[T]]):
        self.action = action
        self.class_ = class_
