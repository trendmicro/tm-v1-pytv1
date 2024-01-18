from pytmv1 import (
    AddAlertNoteResp,
    GetAlertListResp,
    GetAlertNoteDetailsResp,
    GetAlertNoteListResp,
    InvestigationStatus,
    NoContentResp,
    Provider,
    ResultCode,
    Severity,
)


def test_add_alert_note(client):
    result = client.add_alert_note("1", "dummy note")
    assert isinstance(result.response, AddAlertNoteResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.note_id.isdigit()


def test_update_alert_note(client):
    result = client.update_alert_note("1", "2", "3", "update content")
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_delete_alert_note(client):
    result = client.delete_alert_notes("1", "2", "3")
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_get_alert_note(client):
    result = client.get_alert_note("1", "2")
    assert isinstance(result.response, GetAlertNoteDetailsResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.etag == "33a64df551425fcc55e4d42a148795d9f25f89d4"
    assert result.response.data.content


def test_get_alert_note_list(client):
    result = client.get_alert_note_list("1", creatorName="John Doe")
    assert isinstance(result.response, GetAlertNoteListResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0


def test_consume_alert_note_list(client):
    result = client.consume_alert_note_list(
        lambda s: None, "1", creatorName="John Doe"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 2


def test_consume_alert_list(client):
    result = client.consume_alert_list(
        lambda s: None, "2020-06-15T10:00:00Z", "2020-06-15T10:00:00Z"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 2


def test_consume_alert_list_with_next_link(client):
    result = client.consume_alert_list(
        lambda s: None, "next_link", "2020-06-15T10:00:00Z"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 11


def test_edit_alert_status(client):
    result = client.edit_alert_status(
        "1",
        InvestigationStatus.IN_PROGRESS,
        "d41d8cd98f00b204e9800998ecf8427e",
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_edit_alert_status_is_precondition_failed(client):
    result = client.edit_alert_status(
        "1", InvestigationStatus.IN_PROGRESS, "precondition_failed"
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.error.code == "ConditionNotMet"
    assert result.error.status == 412


def test_edit_alert_status_is_not_found(client):
    result = client.edit_alert_status(
        "1", InvestigationStatus.IN_PROGRESS, "not_found"
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.error.code == "NotFound"
    assert result.error.status == 404


def test_get_alert_details(client):
    result = client.get_alert_details("12345")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.data.alert_provider == Provider.SAE
    assert result.response.etag == "33a64df551425fcc55e4d42a148795d9f25f89d4"


def test_get_alert_list(client):
    result = client.get_alert_list(
        "2020-06-15T10:00:00Z", "2020-06-15T10:00:00Z", severity=Severity.HIGH
    )
    assert isinstance(result.response, GetAlertListResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
