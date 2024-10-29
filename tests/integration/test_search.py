from pytmv1 import (
    GetEmailActivitiesCountResp,
    GetEndpointActivitiesCountResp,
    ListEmailActivityResp,
    ListEndpointActivityResp,
    ListEndpointDataResp,
    ProductCode,
    QueryOp,
    ResultCode,
)


def test_consume_email_activities(client):
    result = client.email.consume_activity(
        lambda s: None, mailMsgSubject="spam"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_list_email_activities(client):
    result = client.email.list_activity(
        mailMsgSubject="spam", mailSenderIp="192.169.1.1"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEmailActivityResp)
    assert len(result.response.items) > 0


def test_get_email_activities_count(client):
    result = client.email.get_activity_count(mailMsgSubject="spam")
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, GetEmailActivitiesCountResp)
    assert result.response.total_count > 0


def test_consume_endpoint_activities(client):
    result = client.endpoint.consume_activity(lambda s: None, dpt="443")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_list_endpoint_activities(client):
    result = client.endpoint.list_activity(dpt="443")
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEndpointActivityResp)
    assert len(result.response.items) > 0


def test_get_endpoint_activities_count(client):
    result = client.endpoint.get_activity_count(dpt="443")
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, GetEndpointActivitiesCountResp)
    assert result.response.total_count > 0


def test_consume_endpoint_data(client):
    result = client.endpoint.consume_data(
        lambda s: None, QueryOp.AND, endpointName="client1"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_list_endpoint_data(client):
    result = client.endpoint.list_data(
        endpointName="client1", productCode=ProductCode.XES
    )
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEndpointDataResp)
    assert len(result.response.items) > 0
    assert result.response.items[0].componentUpdatePolicy == "N-2"
    assert result.response.items[0].componentUpdateStatus == "pause"
    assert result.response.items[0].componentVersion == "outdatedVersion"


def test_list_endpoint_data_optional_fields(client):
    result = client.endpoint.list_data(endpointName="optional_fields")
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEndpointDataResp)
    assert len(result.response.items) > 0
    assert not result.response.items[0].product_code
    assert not result.response.items[0].os_name
    assert not result.response.items[0].os_version
    assert not result.response.items[0].os_description
