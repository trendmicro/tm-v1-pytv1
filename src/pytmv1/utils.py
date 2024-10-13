import base64
import re
from typing import Any, Dict, List, Optional, Pattern, Type

from .model.enum import QueryOp, SearchMode, TaskAction
from .model.request import ObjectRequest, SuspiciousObjectRequest
from .model.response import (
    AccountTaskResp,
    BaseTaskResp,
    BlockListTaskResp,
    CollectFileTaskResp,
    CustomScriptTaskResp,
    EmailMessageTaskResp,
    EndpointTaskResp,
    SandboxSubmitUrlTaskResp,
    TerminateProcessTaskResp,
)

MAC_ADDRESS_PATTERN: Pattern[str] = re.compile(
    "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
)
GUID_PATTERN: Pattern[str] = re.compile("^(\\w+-+){1,5}\\w+$")

TASK_ACTION_MAP: Dict[TaskAction, Type[BaseTaskResp]] = {
    TaskAction.COLLECT_FILE: CollectFileTaskResp,
    TaskAction.ISOLATE_ENDPOINT: EndpointTaskResp,
    TaskAction.RESTORE_ENDPOINT: EndpointTaskResp,
    TaskAction.TERMINATE_PROCESS: TerminateProcessTaskResp,
    TaskAction.QUARANTINE_MESSAGE: EmailMessageTaskResp,
    TaskAction.DELETE_MESSAGE: EmailMessageTaskResp,
    TaskAction.RESTORE_MESSAGE: EmailMessageTaskResp,
    TaskAction.BLOCK_SUSPICIOUS: BlockListTaskResp,
    TaskAction.REMOVE_SUSPICIOUS: BlockListTaskResp,
    TaskAction.RESET_PASSWORD: AccountTaskResp,
    TaskAction.SUBMIT_SANDBOX: SandboxSubmitUrlTaskResp,
    TaskAction.ENABLE_ACCOUNT: AccountTaskResp,
    TaskAction.DISABLE_ACCOUNT: AccountTaskResp,
    TaskAction.FORCE_SIGN_OUT: AccountTaskResp,
    TaskAction.RUN_CUSTOM_SCRIPT: CustomScriptTaskResp,
}


def _build_query(
    op: QueryOp, header: str, fields: Dict[str, str]
) -> Dict[str, str]:
    return filter_none(
        {
            header: (" " + op + " ").join(
                [f"{k} eq '{v}'" for k, v in fields.items()]
            )
        }
    )


def _build_activity_query(
    op: QueryOp, fields: Dict[str, str]
) -> Dict[str, str]:
    return filter_none(
        {
            "TMV1-Query": (" " + op + " ").join(
                [f'{k}:"{v}"' for k, v in fields.items()]
            )
        }
    )


def _b64_encode(value: Optional[str]) -> Optional[str]:
    return base64.b64encode(value.encode()).decode() if value else None


def build_activity_request(
    start_time: Optional[str],
    end_time: Optional[str],
    select: Optional[List[str]],
    top: int,
    search_mode: SearchMode,
) -> Dict[str, str]:
    return filter_none(
        {
            "startDateTime": start_time,
            "endDateTime": end_time,
            "select": ",".join(select) if select else select,
            "top": top,
            "mode": search_mode,
        }
    )


def build_object_request(*tasks: ObjectRequest) -> List[Dict[str, str]]:
    return [
        filter_none(
            {
                task.object_type.value: task.object_value,
                "description": task.description,
            }
        )
        for task in tasks
    ]


def build_sandbox_file_request(
    document_password: Optional[str],
    archive_password: Optional[str],
    arguments: Optional[str],
) -> Dict[str, str]:
    return filter_none(
        {
            "documentPassword": _b64_encode(document_password),
            "archivePassword": _b64_encode(archive_password),
            "arguments": _b64_encode(arguments),
        }
    )


def build_suspicious_request(
    *tasks: SuspiciousObjectRequest,
) -> List[Dict[str, Any]]:
    return [
        filter_none(
            {
                task.object_type.value: task.object_value,
                "description": task.description,
                "riskLevel": (
                    task.risk_level.value if task.risk_level else None
                ),
                "scanAction": (
                    task.scan_action.value if task.scan_action else None
                ),
                "daysToExpiration": task.days_to_expiration,
            }
        )
        for task in tasks
    ]


def filter_none(dictionary: Dict[str, Optional[Any]]) -> Dict[str, Any]:
    return {k: v for k, v in dictionary.items() if v}


def tmv1_filter(op: QueryOp, fields: Dict[str, str]) -> Dict[str, str]:
    return _build_query(op, "TMV1-Filter", fields)


def tmv1_query(op: QueryOp, fields: Dict[str, str]) -> Dict[str, str]:
    return _build_query(op, "TMV1-Query", fields)


def tmv1_activity_query(op: QueryOp, fields: Dict[str, str]) -> Dict[str, str]:
    return _build_activity_query(op, fields)


def filter_query(op: QueryOp, fields: Dict[str, str]) -> Dict[str, str]:
    return _build_query(op, "filter", fields)


def task_action_resp_class(
    task_action: TaskAction,
) -> Type[BaseTaskResp]:
    return TASK_ACTION_MAP.get(task_action, BaseTaskResp)
