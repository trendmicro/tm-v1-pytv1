from pytmv1 import (
    CollectFileRequest,
    EndpointRequest,
    MultiResp,
    ResultCode,
    TerminateProcessRequest,
)


def test_collect_endpoints_file(client):
    result = client.endpoint.collect_file(
        CollectFileRequest(endpointName="client1", filePath="/tmp/dummy.txt")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202


def test_isolate_endpoints(client):
    result = client.endpoint.isolate(EndpointRequest(endpointName="client1"))
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202


def test_restore_endpoints(client):
    result = client.endpoint.restore(EndpointRequest(endpointName="client1"))
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202


def test_terminate_endpoints_process(client):
    result = client.endpoint.terminate_process(
        TerminateProcessRequest(
            endpointName="client1", fileSha1="sha12345", fileName="dummy.exe"
        )
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202
