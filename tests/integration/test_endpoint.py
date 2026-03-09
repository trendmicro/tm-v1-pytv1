from pytmv1 import (
    CollectFileRequest,
    EndpointRequest,
    GetEndpointDetailsResp,
    ListEndpointSecurityResp,
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


def test_list_endpoint_security(client):
    result = client.endpoint.list_endpoints(
        select=["endpointName", "agentGuid", "isolationStatus"],
        top=50,
        osPlatform="windows",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEndpointSecurityResp)
    assert len(result.response.items) > 0


def test_consume_endpoint_security(client):
    result = client.endpoint.consume_endpoints(
        lambda s: None,
        osPlatform="windows",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed >= 0


def test_get_endpoint_security(client):
    list_result = client.endpoint.list_endpoints(top=10)
    assert list_result.result_code == ResultCode.SUCCESS
    assert len(list_result.response.items) > 0
    endpoint_id = list_result.response.items[0].agent_guid
    result = client.endpoint.get_endpoint(endpoint_id)
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, GetEndpointDetailsResp)
    assert result.response.data.agent_guid == endpoint_id
