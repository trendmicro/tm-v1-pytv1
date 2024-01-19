from pytmv1 import ApiKeyRequest, ApiStatus, NoContentResp, ResultCode


def test_create_api_key(client):
    result = client.api_key.create(
        ApiKeyRequest(name="test", role="Master Administrator")
    )
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 201
    assert (
        result.response.items[0].id == "d367abdd-7739-4129-a36a-862c4ec018b4"
    )
    assert result.response.items[0].value == "string"


def test_update_api_key(client):
    result = client.api_key.update(
        key_id="d367abdd-7739-4129-a36a-862c4ec018b4",
        etag="d41d8cd98f00b204e9800998ecf8427e",
        name="thomas_legros3",
    )
    assert result.result_code == ResultCode.SUCCESS
    assert isinstance(result.response, NoContentResp)


def test_delete_api_key(client):
    result = client.api_key.delete("d367abdd-7739-4129-a36a-862c4ec018b4")
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 204


def test_get_api_key(client):
    result = client.api_key.get("d367abdd-7739-4129-a36a-862c4ec018b4")
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.etag == "d41d8cd98f00b204e9800998ecf8427e"
    assert result.response.data.id == "d367abdd-7739-4129-a36a-862c4ec018b4"
    assert result.response.data.status == ApiStatus.ENABLED
    assert result.response.data.name == "test"
    assert result.response.data.role == "Master Administrator"


def test_list_api_keys(client):
    result = client.api_key.list(name="test", role="Master Administrator")
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert (
        result.response.items[0].id == "d367abdd-7739-4129-a36a-862c4ec018b4"
    )


def test_consume_api_keys(client):
    result = client.api_key.consume(
        lambda s: None, name="test", role="Master Administrator"
    )
    assert result.result_code == ResultCode.SUCCESS
    assert result.response.total_consumed == 1
