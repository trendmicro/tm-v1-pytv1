from pytmv1 import (
    AddCustomScriptResp,
    ConsumeLinkableResp,
    CustomScriptTask,
    FileType,
    GetCustomScriptListResp,
    MultiResp,
    NoContentResp,
    ResultCode,
    TextResp,
)


def test_add_custom_script(client):
    result = client.add_custom_script(
        file_type=FileType.BASH,
        file_name="add_script.sh",
        file=bytes("#!/bin/sh\necho 'Add script'", "utf-8"),
    )
    assert isinstance(result.response, AddCustomScriptResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.script_id()


def test_delete_custom_script(client):
    result = client.delete_custom_script("delete_script")
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_download_custom_script(client):
    result = client.download_custom_script("download_script")
    assert isinstance(result.response, TextResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.text == "#!/bin/sh Download Script"


def test_run_custom_script(client):
    result = client.run_custom_script(
        CustomScriptTask(fileName="test", endpointName="client1")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202


def test_update_custom_script(client):
    result = client.update_custom_script(
        script_id="123",
        file_type=FileType.BASH,
        file_name="update_script.sh",
        file=bytes("#!/bin/sh Update script", "utf-8"),
    )
    assert isinstance(result.response, NoContentResp)
    assert result.result_code == ResultCode.SUCCESS


def test_consume_custom_script_list(client):
    result = client.consume_custom_script_list(
        lambda s: None, fileName="random_script.ps1", fileType="powershell"
    )
    assert isinstance(result.response, ConsumeLinkableResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_get_custom_script_list(client):
    result = client.get_custom_script_list(
        fileName="random_script.ps1", fileType="powershell"
    )
    assert isinstance(result.response, GetCustomScriptListResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
