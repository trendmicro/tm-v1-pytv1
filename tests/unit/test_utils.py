from pytmv1 import ObjectTask, QueryOp, SuspiciousObjectTask, utils
from pytmv1.model.enums import ObjectType, ScanAction, SearchMode


def test_build_activity_request():
    start_time = "2021-04-05T08:22:37Z"
    end_time = "2021-04-06T08:22:37Z"
    select = ["dpt", "dst", "endpointHostName"]
    top = 50
    mode = SearchMode.DEFAULT
    result = utils.build_activity_request(
        start_time,
        end_time,
        select,
        top,
        mode,
    )
    assert result == {
        "startDateTime": start_time,
        "endDateTime": end_time,
        "select": ",".join(select) if select else select,
        "top": top,
        "mode": mode,
    }


def test_build_object_request():
    result = utils.build_object_request(
        ObjectTask(objectType=ObjectType.IP, objectValue="1.1.1.1")
    )
    assert result == [{"ip": "1.1.1.1"}]


def test_build_object_request_by_field_name():
    result = utils.build_object_request(
        ObjectTask(object_type=ObjectType.IP, object_value="1.1.1.1")
    )
    assert result == [{"ip": "1.1.1.1"}]


def test_build_sandbox_file_request():
    result = utils.build_sandbox_file_request("pwd", "pwd2", None)
    assert result == {
        "documentPassword": "cHdk",
        "archivePassword": "cHdkMg==",
    }


def test_build_suspicious_request():
    result = utils.build_suspicious_request(
        SuspiciousObjectTask(
            objectType=ObjectType.DOMAIN,
            objectValue="bad.com",
            scanAction=ScanAction.BLOCK,
        )
    )
    assert result == [{"domain": "bad.com", "scanAction": "block"}]


def test_b64_encode():
    assert utils._b64_encode("testString") == "dGVzdFN0cmluZw=="


def test_b64_encode_with_none():
    assert utils._b64_encode(None) is None


def test_build_query():
    result = utils._build_query(
        QueryOp.AND, "TMV1-Query", {"dpt": "443", "src": "1.1.1.1"}
    )
    assert result == {"TMV1-Query": "dpt eq '443' and src eq '1.1.1.1'"}


def test_filter_query():
    assert utils.filter_query(
        QueryOp.AND, {"fileName": "test.sh", "fileType": "bash"}
    ) == {"filter": "fileName eq 'test.sh' and fileType eq 'bash'"}


def test_filter_none():
    dictionary = utils.filter_none({"123": None})
    assert len(dictionary) == 0
    dictionary = utils.filter_none({"123": "Value"})
    assert len(dictionary) == 1
