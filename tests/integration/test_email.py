from pytmv1 import EmailMessageIdRequest, ResultCode


def test_delete_email_messages(client):
    result = client.email.delete(EmailMessageIdRequest(messageId="1"))
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202


def test_delete_email_messages_is_failed(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="server_error")
    )
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].status == 500
    assert result.errors[0].code == "InternalServerError"


def test_delete_email_messages_is_bad_request(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="invalid_format")
    )
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].code == "BadRequest"
    assert result.errors[0].status == 400


def test_delete_email_messages_is_denied(client):
    result = client.email.delete(
        EmailMessageIdRequest(messageId="access_denied")
    )
    assert result.result_code == ResultCode.ERROR
    assert result.errors[0].code == "AccessDenied"
    assert result.errors[0].status == 403


def test_quarantine_email_messages(client):
    result = client.email.quarantine(EmailMessageIdRequest(messageId="1"))
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202


def test_restore_email_messages(client):
    result = client.email.restore(EmailMessageIdRequest(messageId="1"))
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202
