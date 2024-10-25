from pytmv1 import (
    BytesResp,
    EndpointActivity,
    NoContentResp,
    OatRiskLevel,
    ResultCode,
)


def test_list_oat(client):
    result = client.oat.list(
        "2020-06-15T10:00:00Z",
        "2020-06-15T10:00:00Z",
        "2020-06-15T10:00:00Z",
        "2020-06-15T10:00:00Z",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.count == 0
    assert result.response.total_count == 0
    assert result.response.items[0].endpoint.endpoint_name == "LAB-Luwak-1048"
    assert (
        result.response.items[0].uuid == "fdd69d98-58de-4249-9871-2e1b233b72ff"
    )
    assert result.response.items[0].source == "endpointActivityData"
    assert isinstance(result.response.items[0].detail, EndpointActivity)


def test_consume_oat(client):
    result = client.oat.consume(
        lambda s: None,
        "next_link",
        "2020-06-15T10:00:00Z",
        "2020-06-15T10:00:00Z",
        "2020-06-15T10:00:00Z",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 3


def test_create_pipeline(client):
    result = client.oat.create_pipeline(
        True,
        [OatRiskLevel.INFO, OatRiskLevel.MEDIUM, OatRiskLevel.CRITICAL],
        "my pipeline",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert (
        result.response.pipeline_id == "c80d8eaa-e55f-4c64-991f-9d0bdf59ee5b"
    )


def test_get_pipeline(client):
    result = client.oat.get_pipeline("83df1ed3-84e7-4e6d-98b5-d79468cccba1")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.etag == "0x8D9AB4B0CA9D336"
    assert result.response.data.id is None
    assert result.response.data.has_detail is True
    assert result.response.data.risk_levels == [OatRiskLevel.CRITICAL]


def test_update_pipeline(client):
    result = client.oat.update_pipeline(
        "83df1ed3-84e7-4e6d-98b5-d79468cccba1",
        "b971d16b5f6330c81a7455fcb8ba8e09c11ba970",
        True,
        risk_levels=[
            OatRiskLevel.INFO,
            OatRiskLevel.MEDIUM,
            OatRiskLevel.CRITICAL,
            OatRiskLevel.HIGH,
        ],
        description="my pipeline updated",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, NoContentResp)


def test_delete_pipelines(client):
    result = client.oat.delete_pipelines(
        "853c03ea-33dd-435e-8fc6-bf551bfec024"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 204


def test_list_pipelines(client):
    result = client.oat.list_pipelines()
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.count == 1
    assert (
        result.response.items[0].id == "8746fc45-6b9d-4923-b476-931aec6e06eb"
    )
    assert result.response.items[0].has_detail is True
    assert result.response.items[0].description == "siemhost1"


def test_download_package(client):
    result = client.oat.download_package(
        "83df1ed3-84e7-4e6d-98b5-d79468cccba1",
        "2024073012-774c3fb6-f777-4ce1-8564-39885e7d41a4",
    )
    assert isinstance(result.response, BytesResp)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.content


def test_list_packages(client):
    result = client.oat.list_packages("83df1ed3-84e7-4e6d-98b5-d79468cccba1")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_count == 20
    assert result.response.count == 2
    assert (
        result.response.items[0].id
        == "2021103019-7898c20d-fc91-443b-9a4e-f8ec3ab745ab"
    )
    assert result.response.items[0].created_date_time == "2021-10-30T19:50:00Z"


def test_consume_packages(client):
    result = client.oat.consume_packages(
        "8746fc45-6b9d-4923-b476-931aec6e06eb",
        lambda s: None,
        "next_link",
        "2020-06-15T10:00:00Z",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 4
