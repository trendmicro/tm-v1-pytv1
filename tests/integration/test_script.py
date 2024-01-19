from pytmv1 import (
    AddCustomScriptResp,
    ConsumeLinkableResp,
    FileType,
    ListCustomScriptsResp,
    MultiResp,
    NoContentResp,
    ResultCode,
    RunCustomScriptRequest,
    TextResp,
)


def test_add_custom_script(client):
    result = client.script.add(
        file_type=FileType.BASH,
        file_name="add_script.sh",
        file_content="#!/bin/sh\necho 'Add script'",
    )
    assert isinstance(result.response, AddCustomScriptResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.script_id


def test_delete_custom_script(client):
    result = client.script.delete("delete_script")
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_download_custom_script(client):
    result = client.script.download("download_script")
    assert isinstance(result.response, TextResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.text == "#!/bin/sh Download Script"


def test_run_custom_scripts(client):
    result = client.script.run(
        RunCustomScriptRequest(fileName="test", endpointName="client1")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202


def test_update_custom_script(client):
    result = client.script.update(
        script_id="123",
        file_type=FileType.BASH,
        file_name="update_script.sh",
        file_content="#!/bin/sh Update script",
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_consume_custom_scripts(client):
    result = client.script.consume(
        lambda s: None, fileName="random_script.ps1", fileType="powershell"
    )
    assert isinstance(result.response, ConsumeLinkableResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_list_custom_scripts(client):
    result = client.script.list(
        fileName="random_script.ps1", fileType="powershell"
    )
    assert isinstance(result.response, ListCustomScriptsResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
