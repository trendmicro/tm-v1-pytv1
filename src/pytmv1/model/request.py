from typing import Optional

from .common import BaseModel
from .enum import ApiExpInMonths, ApiStatus, ObjectType, RiskLevel, ScanAction


class AccountRequest(BaseModel):
    account_name: str
    """User account name."""
    description: Optional[str] = None
    """Description of a response task."""


class EndpointRequest(BaseModel):
    endpoint_name: Optional[str] = None
    """Endpoint name."""
    agent_guid: Optional[str] = None
    """Agent guid"""
    description: Optional[str] = None
    """Description of a response task."""


class CustomScriptRequest(EndpointRequest):
    file_name: str
    parameter: Optional[str] = None
    """Options passed to the script during execution"""


class EmailMessageIdRequest(BaseModel):
    message_id: str
    """Email message id."""
    mail_box: Optional[str] = None
    """Email address."""
    description: Optional[str] = None
    """Description of a response task."""


class EmailMessageUIdRequest(BaseModel):
    unique_id: str
    """Email unique message id."""
    description: Optional[str] = None
    """Description of a response task."""


class ObjectRequest(BaseModel):
    object_type: ObjectType
    """Type of object."""
    object_value: str
    """Value of an object."""
    description: Optional[str] = None
    """Description of an object."""


class SuspiciousObjectRequest(ObjectRequest):
    scan_action: Optional[ScanAction] = None
    """Action applied after detecting a suspicious object."""
    risk_level: Optional[RiskLevel] = None
    """Risk level of a suspicious object."""
    days_to_expiration: Optional[int] = None
    """Number of days before the object expires."""


class CollectFileRequest(EndpointRequest):
    file_path: str
    """File path of the file to be collected from the target."""


class TerminateProcessRequest(EndpointRequest):
    file_sha1: str
    """SHA1 hash of the terminated process's executable file."""
    file_name: Optional[str] = None
    """File name of the target."""


class ApiKeyRequest(BaseModel):
    name: str
    role: str
    months_to_expiration: Optional[ApiExpInMonths] = ApiExpInMonths.ZERO
    description: Optional[str] = None
    status: Optional[ApiStatus] = ApiStatus.ENABLED
