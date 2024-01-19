from pytmv1 import (
    ListExceptionsResp,
    ListSuspiciousResp,
    MultiResp,
    ObjectRequest,
    ObjectType,
    ResultCode,
    SuspiciousObjectRequest,
)
from pytmv1.model.enum import ScanAction


def test_add_exceptions(client):
    result = client.object.add_exception(
        ObjectRequest(objectType=ObjectType.IP, objectValue="1.1.1.1")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].task_id is None
    assert result.response.items[0].status == 201


def test_add_block(client):
    result = client.object.add_block(
        ObjectRequest(objectType=ObjectType.IP, objectValue="1.1.1.1")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].task_id
    assert result.response.items[0].status == 202


def test_add_suspicious(client):
    result = client.object.add_suspicious(
        SuspiciousObjectRequest(
            objectType=ObjectType.IP,
            objectValue="1.1.1.1",
            scanAction=ScanAction.BLOCK,
        )
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].task_id is None
    assert result.response.items[0].status == 201


def test_delete_block(client):
    result = client.object.delete_block(
        ObjectRequest(objectType=ObjectType.IP, objectValue="1.1.1.1")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].task_id
    assert result.response.items[0].status == 202


def test_delete_exceptions(client):
    result = client.object.delete_exception(
        ObjectRequest(objectType=ObjectType.IP, objectValue="1.1.1.1")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].task_id is None
    assert result.response.items[0].status == 204


def test_delete_suspicious(client):
    result = client.object.delete_suspicious(
        ObjectRequest(objectType=ObjectType.IP, objectValue="1.1.1.1")
    )
    assert isinstance(result.response, MultiResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].task_id is None
    assert result.response.items[0].status == 204


def test_list_exceptions(client):
    result = client.object.list_exception()
    assert isinstance(result.response, ListExceptionsResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].type == ObjectType.URL
    assert result.response.items[0].value == "https://*.example.com/path1/*"


def test_list_suspicious(client):
    result = client.object.list_suspicious()
    assert isinstance(result.response, ListSuspiciousResp)
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].type == ObjectType.FILE_SHA256
    assert (
        result.response.items[0].value
        == "asidj123123jsdsidjsid123sidsidj123sss123s224212312312312312sdaas"
    )


def test_consume_exceptions(client):
    result = client.object.consume_exception(lambda s: None)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1


def test_consume_suspicious(client):
    result = client.object.consume_suspicious(lambda s: None)
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1
