from pytmv1 import (
    BytesResp,
    CaseAttachmentResp,
    CaseContentResp,
    CasePriority,
    CaseResp,
    CaseStatus,
    CaseType,
    GetCaseContentResp,
    GetCaseResp,
    ListCaseContentResp,
    ListCaseResp,
    NoContentResp,
    ResultCode,
)


def test_create_case(client):
    result = client.case_mgmt.create(
        "Test Case",
        CasePriority.P0,
        "JIRA Alias",
        "JIRA-12345",
        description="My test case description",
    )
    assert isinstance(result.response, CaseResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.case_id == "CL-00005-20231007-00005"


def test_get_case(client):
    result = client.case_mgmt.get("CL-00005-20231007-00005")
    assert isinstance(result.response, GetCaseResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.etag == "33a64df551425fcc55e4d42a148795d9f25f89d4"
    assert result.response.data.status == CaseStatus.OPEN
    assert result.response.data.id == "CL-00005-20231007-00005"
    assert result.response.data.name == "Possible Ransomware Attack"


def test_update_case(client):
    result = client.case_mgmt.update(
        "CL-00005-20231007-00005",
        "33a64df551425fcc55e4d42a148795d9f25f89d4",
        "Test",
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_list_case(client):
    result = client.case_mgmt.list(priority=CasePriority.P1)
    assert isinstance(result.response, ListCaseResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_count == 100
    assert result.response.count == 50
    assert result.response.items[0].id == "CL-00005-20231007-00005"
    assert result.response.items[0].status == CaseStatus.OPEN
    assert result.response.items[0].name == "Possible Ransomware Attack"
    assert result.response.items[0].type == CaseType.WORKBENCH


def test_consume_case(client):
    result = client.case_mgmt.consume(lambda s: None, start_time="next_link")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 2


def test_add_content(client):
    result = client.case_mgmt.add_content(
        "CL-00005-20231007-00005", "My Comment"
    )
    assert isinstance(result.response, CaseContentResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.content_id == "250aa526-985c-4dc9-8b20-e5118cbbd1e9"


def test_get_content(client):
    result = client.case_mgmt.get_content(
        "CL-00005-20231007-00005", "7bdc2bcf-97cd-4570-bfb9-a15989399534"
    )
    assert isinstance(result.response, GetCaseContentResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.etag == "33a64df551425fcc55e4d42a148795d9f25f89d4"
    assert result.response.data.id == "7bdc2bcf-97cd-4570-bfb9-a15989399534"
    assert result.response.data.comment == "Please see the attached file."
    assert result.response.data.attachments[0].name == "screenshot.jpg"
    assert result.response.data.creator.name == "Ted Mosby"


def test_update_content(client):
    result = client.case_mgmt.update_content(
        "CL-00005-20231007-00005",
        "dc294b2b-f671-4868-a8fd-1cd547e420af",
        "33a64df551425fcc55e4d42a148795d9f25f89d4",
        "New comment",
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_delete_content(client):
    result = client.case_mgmt.delete_content(
        "CL-00005-20231007-00005", "dc294b2b-f671-4868-a8fd-1cd547e420af"
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_list_content(client):
    result = client.case_mgmt.list_content("CL-00005-20231007-00005")
    assert isinstance(result.response, ListCaseContentResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_count == 100
    assert result.response.count == 50
    assert (
        result.response.items[0].id == "7bdc2bcf-97cd-4570-bfb9-a15989399534"
    )
    assert result.response.items[0].comment == "Please see the attached file."
    assert result.response.items[0].creator.name == "Ted Mosby"


def test_consume_content(client):
    result = client.case_mgmt.consume_content(
        "CL-00005-20231007-00005", lambda s: None, start_time="next_link"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 2


def test_add_attachment(client):
    result = client.case_mgmt.add_attachment(
        "CL-00005-20231007-00005", bytes("Test", "utf-8"), "Test file"
    )
    assert isinstance(result.response, CaseAttachmentResp)
    assert result.result_code == ResultCode.SUCCESS
    assert (
        result.response.attachment_id == "dc294b2b-f671-4868-a8fd-1cd547e420af"
    )


def test_download_attachment(client):
    result = client.case_mgmt.download_attachment(
        "CL-00005-20231007-00005", "dc294b2b-f671-4868-a8fd-1cd547e420af"
    )
    assert isinstance(result.response, BytesResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.content


def test_delete_attachment(client):
    result = client.case_mgmt.delete_attachment(
        "CL-00005-20231007-00005", "dc294b2b-f671-4868-a8fd-1cd547e420af"
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS
