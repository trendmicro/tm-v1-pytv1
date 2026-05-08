from pytmv1.model.common import EmailActivity, EndpointActivity, OatEvent


def _base_event(detail):
    return {
        "filters": [],
        "entityType": "endpoint",
        "entityName": "host-1",
        "detail": detail,
    }


def test_oat_event_detail_endpoint_parsed_as_endpoint_activity():
    event = OatEvent.model_validate(
        _base_event(
            {"endpointGuid": "guid-1", "endpointHostName": "host-1"}
        )
    )
    assert isinstance(event.detail, EndpointActivity)
    assert event.detail.endpoint_guid == "guid-1"


def test_oat_event_detail_email_parsed_as_email_activity():
    event = OatEvent.model_validate(
        _base_event({"msgUuid": "msg-1", "mailMsgSubject": "subj"})
    )
    assert isinstance(event.detail, EmailActivity)
    assert event.detail.msg_uuid == "msg-1"


def test_oat_event_detail_unmodeled_falls_back_to_dict():
    raw_detail = {"act": ["log"], "src": "1.2.3.4", "evt": "cloudtrail"}
    event = OatEvent.model_validate(_base_event(raw_detail))
    assert isinstance(event.detail, dict)
    assert event.detail == raw_detail
