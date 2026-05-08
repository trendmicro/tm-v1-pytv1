from unittest.mock import MagicMock

from pytmv1.api.alert import Alert


def _list_params(core_mock):
    return core_mock.send.call_args.kwargs["params"]


def _consume_params(core_mock):
    return core_mock.send_linkable.call_args.kwargs["params"]


def test_list_default_order_by_is_created_desc():
    core = MagicMock()
    Alert(core).list()
    assert _list_params(core)["orderBy"] == "createdDateTime desc"


def test_list_respects_order_by_kwarg():
    core = MagicMock()
    Alert(core).list(order_by="createdDateTime asc")
    assert _list_params(core)["orderBy"] == "createdDateTime asc"


def test_consume_default_order_by_is_created_desc():
    core = MagicMock()
    Alert(core).consume(lambda _: None)
    assert _consume_params(core)["orderBy"] == "createdDateTime desc"


def test_consume_respects_order_by_kwarg():
    core = MagicMock()
    Alert(core).consume(lambda _: None, order_by="createdDateTime asc")
    assert _consume_params(core)["orderBy"] == "createdDateTime asc"
