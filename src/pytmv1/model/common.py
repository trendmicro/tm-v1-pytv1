from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field
from pydantic import RootModel as PydanticRootModel
from pydantic import field_validator, model_validator
from pydantic.alias_generators import to_camel

from .enum import (
    AlertStatus,
    ApiStatus,
    DetectionType,
    EntityType,
    Iam,
    IntegrityLevel,
    InvestigationResult,
    InvestigationStatus,
    OatDataSource,
    OatEntityType,
    OatRiskLevel,
    ObjectType,
    OperatingSystem,
    ProductCode,
    Provider,
    RiskLevel,
    ScanAction,
    ScriptType,
    Severity,
    Status,
)

CFG = ConfigDict(alias_generator=to_camel, populate_by_name=True)
CFG_NAMESPACE = ConfigDict(**CFG, protected_namespaces=())


class BaseModel(PydanticBaseModel):
    model_config = CFG


class RootModel(PydanticRootModel[List[int]]):
    model_config = CFG


class BaseConsumable(BaseModel): ...


class Account(BaseModel):
    account_name: str
    iam: Iam
    last_action_date_time: str
    status: Status


class Alert(BaseConsumable):
    model_config = CFG_NAMESPACE

    id: str
    schema_version: str
    status: AlertStatus
    # Deprecated
    investigation_status: InvestigationStatus
    investigation_result: InvestigationResult
    workbench_link: str
    alert_provider: Provider
    model: str
    model_type: DetectionType
    score: int
    severity: Severity
    impact_scope: ImpactScope
    created_date_time: str
    updated_date_time: str
    first_investigated_date_time: Optional[str] = None
    incident_id: Optional[str] = None
    case_id: Optional[str] = None
    owner_ids: List[str] = Field(default=[])
    model_id: str


class AlertNote(BaseConsumable):
    id: int
    content: str
    creator_name: str
    created_date_time: str
    creator_mail_address: Optional[str]
    last_updated_by: Optional[str]
    last_updated_date_time: Optional[str]


class ApiKey(BaseConsumable):
    id: str
    name: str
    status: ApiStatus
    role: str
    expired_date_time: str
    last_used_date_time: str
    description: Optional[str]


class Digest(BaseModel):
    md5: str
    sha1: str
    sha256: str


class EmailMessage(BaseModel):
    last_action_date_time: str
    message_id: Optional[str] = None
    mail_box: Optional[str] = None
    message_subject: Optional[str] = None
    unique_id: Optional[str] = None
    organization_id: Optional[str] = None
    status: Status


class Value(BaseModel):
    updated_date_time: str
    value: str


class ValueList(BaseModel):
    updated_date_time: str
    value: List[str]


class Endpoint(BaseConsumable):
    agent_guid: str
    login_account: ValueList
    endpoint_name: Value
    mac_address: ValueList
    ip: ValueList
    os_name: Optional[OperatingSystem] = None
    os_version: Optional[str] = None
    os_description: Optional[str] = None
    product_code: Optional[ProductCode] = None
    installed_product_codes: List[ProductCode] = Field(default=[])
    componentUpdatePolicy: Optional[str] = None
    componentUpdateStatus: Optional[str] = None
    componentVersion: Optional[str] = None
    policyName: Optional[str] = None
    protectionManager: Optional[str] = None

    @field_validator("os_name", "product_code", mode="before")
    @classmethod
    def allow_empty_enum_string(cls, value: Any) -> Union[Any, None]:
        if value == "":
            return None
        return value


class EmailActivity(BaseConsumable):
    event_source_type: Optional[str] = None
    mail_msg_subject: Optional[str] = None
    mail_msg_id: Optional[str] = None
    msg_uuid: str
    mailbox: Optional[str] = None
    mail_sender_ip: Optional[str] = None
    mail_from_addresses: List[str] = Field(default=[])
    mail_whole_header: List[str] = Field(default=[])
    mail_to_addresses: List[str] = Field(default=[])
    mail_source_domain: Optional[str] = None
    search_d_l: Optional[str] = None
    scan_type: Optional[str] = None
    event_time: Optional[int] = None
    org_id: Optional[str] = None
    mail_urls_visible_link: List[str] = Field(default=[])
    mail_urls_real_link: List[str] = Field(default=[])


class EndpointActivity(BaseConsumable):
    dpt: Optional[int] = None
    dst: Optional[str] = None
    endpoint_guid: str
    endpoint_host_name: Optional[str] = None
    endpoint_ip: List[str] = Field(default=[])
    event_id: Optional[str] = None
    event_source_type: Optional[str] = None
    event_sub_id: Optional[str] = None
    object_integrity_level: Optional[IntegrityLevel] = None
    object_true_type: Optional[int] = None
    object_sub_true_type: Optional[int] = None
    win_event_id: Optional[int] = None
    event_time: Optional[int] = None
    event_time_d_t: Optional[str] = None
    host_name: Optional[str] = None
    logon_user: List[str] = Field(default=[])
    object_cmd: Optional[str] = None
    object_file_hash_sha1: Optional[str] = None
    object_file_path: Optional[str] = None
    object_host_name: Optional[str] = None
    object_ip: Optional[str] = None
    object_ips: List[str] = Field(default=[])
    object_port: Optional[int] = None
    object_registry_data: Optional[str] = None
    object_registry_key_handle: Optional[str] = None
    object_registry_value: Optional[str] = None
    object_signer: List[str] = Field(default=[])
    object_signer_valid: List[bool] = Field(default=[])
    object_user: Optional[str] = None
    os: Optional[str] = None
    parent_cmd: Optional[str] = None
    parent_file_hash_sha1: Optional[str] = None
    parent_file_path: Optional[str] = None
    process_cmd: Optional[str] = None
    process_file_hash_sha1: Optional[str] = None
    process_file_path: Optional[str] = None
    request: Optional[str] = None
    search_d_l: Optional[str] = None
    spt: Optional[int] = None
    src: Optional[str] = None
    src_file_hash_sha1: Optional[str] = None
    src_file_path: Optional[str] = None
    tags: List[str] = Field(default=[])
    uuid: Optional[str] = None

    @field_validator("event_sub_id", mode="before")
    @classmethod
    def map_event_sub_id(
        cls, value: Optional[Union[int, str]]
    ) -> Optional[str]:
        if value is not None and isinstance(value, int):
            return str(value)
        return value

    @field_validator("object_integrity_level", mode="before")
    @classmethod
    def map_object_integrity_level(
        cls, value: Optional[int]
    ) -> Optional[IntegrityLevel]:
        if value:
            if IntegrityLevel.UNTRUSTED <= value < IntegrityLevel.LOW:
                return IntegrityLevel.UNTRUSTED
            if IntegrityLevel.LOW <= value < IntegrityLevel.MEDIUM:
                return IntegrityLevel.LOW
            if IntegrityLevel.MEDIUM <= value < IntegrityLevel.HIGH:
                return IntegrityLevel.MEDIUM
            if IntegrityLevel.HIGH <= value < IntegrityLevel.SYSTEM:
                return IntegrityLevel.HIGH
            return IntegrityLevel.SYSTEM
        return None


class HostInfo(BaseModel):
    name: str
    ips: List[str]
    guid: str


class Entity(BaseModel):
    entity_id: str
    entity_type: EntityType
    entity_value: Union[str, HostInfo]
    related_entities: Union[List[str], List[List[str]]]
    related_indicator_ids: List[int]
    provenance: List[str]
    management_scope_group_id: Optional[str] = None
    management_scope_instance_id: Optional[str] = None
    management_scope_partition_key: Optional[str] = None


class Error(BaseModel):
    status: int
    code: Optional[str] = None
    message: Optional[str] = None
    number: Optional[int] = None


class ExceptionObject(BaseConsumable):
    value: str
    type: ObjectType
    last_modified_date_time: str
    description: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _map_data(cls, data: Dict[str, str]) -> Dict[str, str]:
        value = data.get(data.get("type", ""))
        if value:
            data["value"] = value
        return data


class ImpactScope(BaseModel):
    desktop_count: int
    server_count: int
    account_count: int
    email_address_count: int
    container_count: int
    cloud_identity_count: int
    entities: List[Entity]


class Indicator(BaseModel):
    id: int
    type: str
    value: Union[str, HostInfo]
    related_entities: Union[List[str], List[List[str]]]
    provenance: List[str]


class MatchedEvent(BaseModel):
    uuid: str
    matched_date_time: str
    type: str


class MatchedFilter(BaseModel):
    id: str
    name: str
    matched_date_time: str
    mitre_technique_ids: List[str]
    matched_events: List[MatchedEvent]


class MatchedIndicatorPattern(BaseModel):
    id: str
    pattern: str
    tags: List[str]
    matched_logs: List[str] = Field(default=[])


class MatchedRule(BaseModel):
    id: str
    name: str
    matched_filters: List[MatchedFilter]


class MsData(BaseModel):
    status: int
    task_id: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def map_task_id(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["task_id"] = _get_task_id(data)
        return data


class MsDataApiKey(MsData):
    id: str
    value: str
    expired_date_time: str

    @model_validator(mode="before")
    @classmethod
    def map_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data.update(data.pop("body", {}))
        return data


class MsDataUrl(MsData):
    url: str
    id: Optional[str] = None
    digest: Optional[Digest] = None

    @model_validator(mode="before")
    @classmethod
    def map_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data.update(data.pop("body", {}))
        return data


class MsError(Error):
    extra: Dict[str, str] = {}
    task_id: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def map_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data.update(data.pop("body", {}))
        data.update(data.pop("error", {}))
        data["task_id"] = _get_task_id(data)
        url = data.pop("url", None)
        if url:
            data["extra"] = {"url": url}
        return data


class MsStatus(RootModel):
    root: List[int]

    def values(self) -> List[int]:
        return self.root


class OatEndpoint(BaseModel):
    endpoint_name: Optional[str] = None
    name: Optional[str] = None
    agent_guid: Optional[str] = None
    guid: Optional[str] = None
    ips: List[str]


class OatObject(BaseModel):
    field: str
    type: str
    value: Union[int, str, List[str]]
    master: Optional[bool] = None
    risk_level: Optional[OatRiskLevel] = None


class OatFilter(BaseModel):
    id: str
    unique_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    mitre_tactic_ids: Optional[List[str]] = None
    tactics: Optional[List[str]] = None
    mitre_technique_ids: Optional[List[str]] = None
    techniques: Optional[List[str]] = None
    highlighted_objects: List[OatObject]
    risk_level: Optional[OatRiskLevel] = None
    level: Optional[OatRiskLevel] = None
    type: DetectionType


class OatEvent(BaseConsumable):
    source: Optional[OatDataSource] = None
    uuid: Optional[str] = None
    filters: List[OatFilter]
    endpoint: Optional[OatEndpoint] = None
    entity_type: OatEntityType
    entity_name: str
    detected_date_time: Optional[str] = None
    detection_time: Optional[str] = None
    ingested_date_time: Optional[str] = None
    detail: Union[EndpointActivity, EmailActivity]


class OatPackage(BaseConsumable):
    id: str
    created_date_time: str


class OatPipeline(BaseModel):
    has_detail: bool
    registered_date_time: str
    risk_levels: List[OatRiskLevel]
    id: Optional[str] = None
    description: Optional[str] = None


class SaeIndicator(Indicator):
    field: str
    filter_ids: List[str]


class SaeAlert(Alert):
    description: str
    matched_rules: List[MatchedRule]
    indicators: List[SaeIndicator]


class SandboxSuspiciousObject(BaseModel):
    risk_level: RiskLevel
    analysis_completion_date_time: str
    expired_date_time: str
    root_sha1: str
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


class Script(BaseConsumable):
    id: str
    file_name: str
    file_type: ScriptType
    description: Optional[str] = None


class SuspiciousObject(ExceptionObject):
    scan_action: ScanAction
    risk_level: RiskLevel
    in_exception_list: bool
    expired_date_time: str


class TaskError(BaseModel):
    code: str
    message: str
    number: int


class TiIndicator(Indicator):
    fields: List[List[str]]
    matched_indicator_pattern_ids: List[str]
    first_seen_date_times: List[str]
    last_seen_date_times: List[str]


class TiAlert(Alert):
    campaign: Optional[str] = None
    industry: Optional[str] = None
    region_and_country: Optional[str] = None
    created_by: str
    total_indicator_count: int
    matched_indicator_count: int
    report_link: str
    matched_indicator_patterns: List[MatchedIndicatorPattern]
    indicators: List[TiIndicator]


def _get_task_id(data: Dict[str, Any]) -> Optional[str]:
    return next(
        map(
            lambda header: header.get("value", "").split("/")[-1],
            filter(
                lambda header: "Operation-Location" == header.get("name", ""),
                data.pop("headers", []),
            ),
        ),
        None,
    )


def get_object(data: Dict[str, str]) -> Optional[Tuple[str, str]]:
    obj = next(
        filter(
            lambda item: item[0] in map(lambda ot: ot.value, ObjectType),
            data.items(),
        ),
        None,
    )
    return obj
