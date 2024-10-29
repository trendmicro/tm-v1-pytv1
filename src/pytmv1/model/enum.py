from enum import Enum


class AlertStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"


class Api(str, Enum):
    CONNECTIVITY = "/healthcheck/connectivity"
    CREATE_API_KEYS = "/iam/apiKeys"
    GET_API_KEY_LIST = "/iam/apiKeys"
    GET_API_KEY = "/iam/apiKeys/{0}"
    UPDATE_API_KEY = "/iam/apiKeys/{0}"
    DELETE_API_KEYS = "/iam/apiKeys/delete"
    GET_ENDPOINT_DATA = "/eiqs/endpoints"
    GET_CUSTOM_SCRIPTS = "/response/customScripts"
    ADD_CUSTOM_SCRIPT = "/response/customScripts"
    DELETE_CUSTOM_SCRIPT = "/response/customScripts/{0}"
    DOWNLOAD_CUSTOM_SCRIPT = "/response/customScripts/{0}"
    UPDATE_CUSTOM_SCRIPT = "/response/customScripts/{0}/update"
    DELETE_EMAIL_MESSAGE = "/response/emails/delete"
    QUARANTINE_EMAIL_MESSAGE = "/response/emails/quarantine"
    RESTORE_EMAIL_MESSAGE = "/response/emails/restore"
    DISABLE_ACCOUNT = "/response/domainAccounts/disable"
    ENABLE_ACCOUNT = "/response/domainAccounts/enable"
    RESET_PASSWORD = "/response/domainAccounts/resetPassword"
    SIGN_OUT_ACCOUNT = "/response/domainAccounts/signOut"
    COLLECT_ENDPOINT_FILE = "/response/endpoints/collectFile"
    ISOLATE_ENDPOINT = "/response/endpoints/isolate"
    RESTORE_ENDPOINT = "/response/endpoints/restore"
    RUN_CUSTOM_SCRIPT = "/response/endpoints/runScript"
    TERMINATE_ENDPOINT_PROCESS = "/response/endpoints/terminateProcess"
    ADD_TO_BLOCK_LIST = "/response/suspiciousObjects"
    REMOVE_FROM_BLOCK_LIST = "/response/suspiciousObjects/delete"
    GET_TASK_RESULT = "/response/tasks/{0}"
    GET_SANDBOX_ANALYSIS_RESULT = "/sandbox/analysisResults/{0}"
    DOWNLOAD_SANDBOX_INVESTIGATION_PACKAGE = (
        "/sandbox/analysisResults/{0}/investigationPackage"
    )
    DOWNLOAD_SANDBOX_ANALYSIS_RESULT = "/sandbox/analysisResults/{0}/report"
    GET_SANDBOX_SUSPICIOUS_LIST = (
        "/sandbox/analysisResults/{0}/suspiciousObjects"
    )
    SUBMIT_FILE_TO_SANDBOX = "/sandbox/files/analyze"
    GET_SANDBOX_SUBMISSION_STATUS = "/sandbox/tasks/{0}"
    SUBMIT_URLS_TO_SANDBOX = "/sandbox/urls/analyze"
    GET_EMAIL_ACTIVITY_DATA = "/search/emailActivities"
    GET_ENDPOINT_ACTIVITY_DATA = "/search/endpointActivities"
    GET_SUSPICIOUS_OBJECTS = "/threatintel/suspiciousObjects"
    ADD_TO_SUSPICIOUS_LIST = "/threatintel/suspiciousObjects"
    REMOVE_FROM_SUSPICIOUS_LIST = "/threatintel/suspiciousObjects/delete"
    ADD_TO_EXCEPTION_LIST = "/threatintel/suspiciousObjectExceptions"
    GET_EXCEPTION_OBJECTS = "/threatintel/suspiciousObjectExceptions"
    REMOVE_FROM_EXCEPTION_LIST = (
        "/threatintel/suspiciousObjectExceptions/delete"
    )
    GET_ALERT_LIST = "/workbench/alerts"
    UPDATE_ALERT_STATUS = "/workbench/alerts/{0}"
    GET_ALERT = "/workbench/alerts/{0}"
    ADD_ALERT_NOTE = "/workbench/alerts/{0}/notes"
    GET_ALERT_NOTE_LIST = "/workbench/alerts/{0}/notes"
    GET_ALERT_NOTE = "/workbench/alerts/{0}/notes/{1}"
    UPDATE_ALERT_NOTE = "/workbench/alerts/{0}/notes/{1}"
    DELETE_ALERT_NOTE = "/workbench/alerts/{0}/notes/delete"
    GET_OAT_LIST = "/oat/detections"
    CREATE_OAT_PIPELINE = "/oat/dataPipelines"
    GET_OAT_PIPELINE = "/oat/dataPipelines/{0}"
    UPDATE_OAT_PIPELINE = "/oat/dataPipelines/{0}"
    DELETE_OAT_PIPELINE = "/oat/dataPipelines/delete"
    LIST_OAT_PIPELINE = "/oat/dataPipelines"
    DOWNLOAD_OAT_PACKAGE = "/oat/dataPipelines/{0}/packages/{1}"
    LIST_OAT_PACKAGE = "/oat/dataPipelines/{0}/packages"


class ApiExpInMonths(int, Enum):
    ONE = 1
    THREE = 3
    SIX = 6
    TWELVE = 12
    ZERO = 0


class ApiStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class Iam(str, Enum):
    # Azure AD
    AAD = "AAD"
    # On-premise AD
    OPAD = "OPAD"


class IntegrityLevel(int, Enum):
    UNTRUSTED = 0
    LOW = 4096
    MEDIUM = 8192
    HIGH = 12288
    SYSTEM = 16384


class InvestigationResult(str, Enum):
    NO_FINDINGS = "No Findings"
    NOTEWORTHY = "Noteworthy"
    TRUE_POSITIVE = "True Positive"
    FALSE_POSITIVE = "False Positive"
    BENIGN_TRUE_POSITIVE = "Benign True Positive"


class InvestigationStatus(str, Enum):
    BENIGN_TRUE_POSITIVE = "Benign True Positive"
    CLOSED = "Closed"
    FALSE_POSITIVE = "False Positive"
    IN_PROGRESS = "In Progress"
    NEW = "New"
    TRUE_POSITIVE = "True Positive"


class EntityType(str, Enum):
    HOST = "host"
    ACCOUNT = "account"
    EMAIL_ADDRESS = "emailAddress"
    CONTAINER = "container"
    CLOUD_IDENTITY = "cloudIdentity"
    AWS_LAMBDA = "awsLambda"


class ScriptType(str, Enum):
    POWERSHELL = "powershell"
    BASH = "bash"


class HttpMethod(str, Enum):
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class OatDataSource(str, Enum):
    DETECTIONS = "detections"
    IDENTITY_ACTIVITY_DATA = "identityActivityData"
    ENDPOINT_ACTIVITY_DATA = "endpointActivityData"
    CLOUD_ACTIVITY_DATA = "cloudActivityData"
    EMAIL_ACTIVITY_DATA = "emailActivityData"
    MOBILE_ACTIVITY_DATA = "mobileActivityData"
    NETWORK_ACTIVITY_DATA = "networkActivityData"
    CONTAINER_ACTIVITY_DATA = "containerActivityData"


class OatEntityType(str, Enum):
    ENDPOINT = "endpoint"
    MAILBOX = "mailbox"
    CLOUDTRAIL = "cloudtrail"
    MESSAGING = "messaging"
    NETWORK = "network"
    ICS = "ics"
    CONTAINER = "container"


class OatRiskLevel(str, Enum):
    UNDEFINED = "undefined"
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DetectionType(str, Enum):
    CUSTOM = "custom"
    PRESET = "preset"


class ObjectType(str, Enum):
    IP = "ip"
    URL = "url"
    DOMAIN = "domain"
    FILE_SHA1 = "fileSha1"
    FILE_SHA256 = "fileSha256"
    SENDER_MAIL_ADDRESS = "senderMailAddress"


class OperatingSystem(str, Enum):
    LINUX = "Linux"
    WINDOWS = "Windows"
    MACOS = "macOS"
    MACOSX = "macOSX"


class ProductCode(str, Enum):
    SAO = "sao"
    SDS = "sds"
    XES = "xes"


class Provenance(str, Enum):
    ALERT = "Alert"
    SWEEPING = "Sweeping"
    NETWORK_ANALYTICS = "Network Analytics"


class Provider(str, Enum):
    SAE = "SAE"
    TI = "TI"


class QueryOp(str, Enum):
    AND = "and"
    OR = "or"


class RiskLevel(str, Enum):
    NO_RISK = "noRisk"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SandboxAction(str, Enum):
    ANALYZE_FILE = "analyzeFile"
    ANALYZE_URL = "analyzeUrl"


class SandboxObjectType(str, Enum):
    URL = "url"
    FILE = "file"


class ScanAction(str, Enum):
    BLOCK = "block"
    LOG = "log"


class SearchMode(str, Enum):
    DEFAULT = "default"
    COUNT_ONLY = "countOnly"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Status(str, Enum):
    FAILED = "failed"
    QUEUED = "queued"
    REJECTED = "rejected"
    CANCELED = "canceled"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    PENDING_APPROVAL = "pendingApproval"


class TaskAction(str, Enum):
    COLLECT_FILE = "collectFile"
    COLLECT_EVIDENCE = "collectEvidence"
    COLLECT_NETWORK_ANALYSIS_PACKAGE = "collectNetworkAnalysisPackage"
    ISOLATE_ENDPOINT = "isolate"
    ISOLATE_ENDPOINT_MULTIPLE = "isolateForMultiple"
    RESTORE_ENDPOINT = "restoreIsolate"
    RESTORE_ENDPOINT_MULTIPLE = "restoreIsolateForMultiple"
    TERMINATE_PROCESS = "terminateProcess"
    DUMP_PROCESS_MEMORY = "dumpProcessMemory"
    QUARANTINE_MESSAGE = "quarantineMessage"
    DELETE_MESSAGE = "deleteMessage"
    RESTORE_MESSAGE = "restoreMessage"
    BLOCK_SUSPICIOUS = "block"
    REMOVE_SUSPICIOUS = "restoreBlock"
    RESET_PASSWORD = "resetPassword"
    SUBMIT_SANDBOX = "submitSandbox"
    ENABLE_ACCOUNT = "enableAccount"
    DISABLE_ACCOUNT = "disableAccount"
    FORCE_SIGN_OUT = "forceSignOut"
    REMOTE_SHELL = "remoteShell"
    RUN_INVESTIGATION_KIT = "runInvestigationKit"
    RUN_CUSTOM_SCRIPT = "runCustomScript"
    RUN_CUSTOM_SCRIPT_MULTIPLE = "runCustomScriptForMultiple"
    RUN_OS_QUERY = "runOsquery"
    RUN_YARA_RULES = "runYaraRules"
