from pytmv1 import (
    CollectFileTaskResp,
    EmailMessageIdRequest,
    ResultCode,
    Status,
)


def test_check_connectivity(client):
    assert client.system.check_connectivity()


def test_get_task_result(client):
    result = client.task.get_result("collect_file")
    assert isinstance(result.response, CollectFileTaskResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.status == Status.SUCCEEDED
    assert result.response.action == "collectFile"
    assert result.response.file_sha256
    assert result.response.id == "00000003"


def test_collect_file_task_result(client):
    result = client.task.get_result_class(
        "collect_file", CollectFileTaskResp, False
    )
    assert isinstance(result.response, CollectFileTaskResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.status == Status.SUCCEEDED
    assert result.response.action == "collectFile"
    assert result.response.file_sha256
    assert result.response.id == "00000003"


def test_collect_file_task_result_is_failed(client):
    result = client.task.get_result_class(
        "internal_error", CollectFileTaskResp, False
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.error.code == "InternalServerError"
    assert result.error.status == 500


def test_collect_file_task_result_is_bad_request(client):
    result = client.task.get_result_class(
        "bad_request", CollectFileTaskResp, False
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.error.code == "BadRequest"
    assert result.error.status == 400


def test_multi_status_is_failed(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="internal_server_error")
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].code == "InternalServerError"
    assert result.errors[0].status == 500


def test_multi_status_is_bad_request(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="fields_not_found")
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].code == "BadRequest"
    assert result.errors[0].status == 400


def test_multi_status_is_denied(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="insufficient_permissions")
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].code == "AccessDenied"
    assert result.errors[0].status == 403


def test_multi_status_is_not_supported(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="action_not_supported")
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].code == "NotSupported"
    assert result.errors[0].status == 400


def test_multi_status_is_task_error(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="task_duplication")
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].code == "TaskError"
    assert result.errors[0].status == 400
