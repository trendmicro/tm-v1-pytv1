import os
from threading import Thread

import psutil
import pytest

import pytmv1


def test_conn_opened_with_single_call_single_client_is_one(client):
    client.object.list_exceptions()
    assert len(list_tcp_conn()) == 1


@pytest.mark.parametrize("execution_number", range(10))
def test_conn_opened_with_multi_call_single_client_is_one(
    execution_number, client
):
    client.object.list_exceptions()
    assert len(list_tcp_conn()) == 1


def test_conn_opened_with_multi_processing_single_client_is_one(client):
    threads = thread_list(lambda: client.add("1", "dummy note"))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(list_tcp_conn()) == 1


def test_conn_opened_with_multi_processing_multi_client_is_one(url):
    threads = thread_list(
        lambda: pytmv1.client("appname", "dummyToken", url).list_exceptions()
    )
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(list_tcp_conn()) == 1


def list_tcp_conn():
    return list(
        filter(
            lambda sc: len(sc[4])
            and 1024 > sc[4][1] < 49151
            and sc[-1] == os.getpid()
            and sc[5] == "ESTABLISHED",
            psutil.net_connections("tcp"),
        )
    )


def thread_list(func):
    return [Thread(target=func) for _ in range(10)]
