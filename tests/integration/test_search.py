from pytmv1 import (
    GetEmailActivitiesCountResp,
    GetEndpointActivitiesCountResp,
    ListEmailActivityDataResp,
    ListEndpointActivitiesResp,
    ListEndpointDataResp,
    ProductCode,
    QueryOp,
    ResultCode,
)


def test_consume_email_activities(client):
    result = client.email.consume_activities(
        lambda s: None, mailMsgSubject="spam"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_list_email_activities(client):
    result = client.email.list_activities(
        mailMsgSubject="spam", mailSenderIp="192.169.1.1"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEmailActivityDataResp)
    assert len(result.response.items) > 0


def test_get_email_activities_count(client):
    result = client.email.get_activities_count(mailMsgSubject="spam")
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, GetEmailActivitiesCountResp)
    assert result.response.total_count > 0


def test_consume_endpoint_activities(client):
    result = client.endpoint.consume_activities(lambda s: None, dpt="443")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_list_endpoint_activities(client):
    result = client.endpoint.list_activities(dpt="443")
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEndpointActivitiesResp)
    assert len(result.response.items) > 0


def test_get_endpoint_activities_count(client):
    result = client.endpoint.get_activities_count(dpt="443")
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, GetEndpointActivitiesCountResp)
    assert result.response.total_count > 0


def test_consume_endpoint_data(client):
    result = client.endpoint.consume(
        lambda s: None, QueryOp.AND, endpointName="client1"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_list_endpoint_data(client):
    result = client.endpoint.list(
        endpointName="client1", productCode=ProductCode.XES
    )
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, ListEndpointDataResp)
    assert len(result.response.items) > 0
