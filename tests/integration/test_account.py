from pytmv1 import AccountRequest, ResultCode


def test_disable_accounts(client):
    result = client.account.disable(AccountRequest(accountName="test"))
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202
    assert result.response.items[0].task_id == "00000009"


def test_enable_accounts(client):
    result = client.account.enable(AccountRequest(accountName="test"))
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202
    assert result.response.items[0].task_id == "00000010"


def test_reset_accounts(client):
    result = client.account.reset(AccountRequest(accountName="test"))
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202
    assert result.response.items[0].task_id == "00000011"


def test_sign_out_accounts(client):
    result = client.account.sign_out(AccountRequest(accountName="test"))
    assert result.result_code == ResultCode.SUCCESS
    assert len(result.response.items) > 0
    assert result.response.items[0].status == 202
    assert result.response.items[0].task_id == "00000012"
