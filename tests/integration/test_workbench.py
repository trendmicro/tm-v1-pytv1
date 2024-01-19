from pytmv1 import (
    AddAlertNoteResp,
    GetAlertNoteResp,
    InvestigationStatus,
    ListAlertNoteResp,
    ListAlertsResp,
    NoContentResp,
    Provider,
    ResultCode,
    Severity,
)


def test_create_note(client):
    result = client.note.create("1", "dummy note")
    assert isinstance(result.response, AddAlertNoteResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.note_id.isdigit()


def test_update_note(client):
    result = client.note.update("1", "2", "3", "update content")
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_delete_note(client):
    result = client.note.delete("1", "2", "3")
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_get_note(client):
    result = client.note.get("1", "2")
    assert isinstance(result.response, GetAlertNoteResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.etag == "33a64df551425fcc55e4d42a148795d9f25f89d4"
    assert result.response.data.content


def test_list_notes(client):
    result = client.note.list("1", creatorName="John Doe")
    assert isinstance(result.response, ListAlertNoteResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0


def test_consume_notes(client):
    result = client.note.consume(lambda s: None, "1", creatorName="John Doe")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 2


def test_consume_alerts(client):
    result = client.alert.consume(
        lambda s: None, "2020-06-15T10:00:00Z", "2020-06-15T10:00:00Z"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 2


def test_consume_alerts_with_next_link(client):
    result = client.alert.consume(
        lambda s: None, "next_link", "2020-06-15T10:00:00Z"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 11


def test_update_alert_status(client):
    result = client.alert.update_status(
        "1",
        InvestigationStatus.IN_PROGRESS,
        "d41d8cd98f00b204e9800998ecf8427e",
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_update_alert_status_is_precondition_failed(client):
    result = client.alert.update_status(
        "1", InvestigationStatus.IN_PROGRESS, "precondition_failed"
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.error.code == "ConditionNotMet"
    assert result.error.status == 412


def test_update_alert_status_is_not_found(client):
    result = client.alert.update_status(
        "1", InvestigationStatus.IN_PROGRESS, "not_found"
    )
    assert not result.response
    assert result.result_code == ResultCode.ERROR
    assert result.error.code == "NotFound"
    assert result.error.status == 404


def test_get_alert(client):
    result = client.alert.get("12345")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.data.alert_provider == Provider.SAE
    assert result.response.etag == "33a64df551425fcc55e4d42a148795d9f25f89d4"


def test_list_alerts(client):
    result = client.alert.list(
        "2020-06-15T10:00:00Z", "2020-06-15T10:00:00Z", severity=Severity.HIGH
    )
    assert isinstance(result.response, ListAlertsResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
