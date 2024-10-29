import logging
import os
import re
import time
from logging import Logger
from typing import Any, Callable, Dict, List, Optional, Type, Union
from urllib.parse import SplitResult, urlsplit

from bs4 import BeautifulSoup
from pydantic import AnyHttpUrl, TypeAdapter
from requests import PreparedRequest, Request, Response

from . import utils
from .__about__ import __version__
from .adapter import HTTPAdapter
from .exception import (
    ParseModelError,
    ServerHtmlError,
    ServerJsonError,
    ServerMultiJsonError,
    ServerTextError,
)
from .model.common import Error, MsError, MsStatus
from .model.enum import Api, HttpMethod, Status, TaskAction
from .model.request import EndpointRequest
from .model.response import (
    MR,
    BaseLinkableResp,
    BaseTaskResp,
    BytesResp,
    C,
    ConsumeLinkableResp,
    GetAlertNoteResp,
    GetAlertResp,
    GetApiKeyResp,
    GetOatPackageResp,
    GetPipelineResp,
    MultiApiKeyResp,
    MultiResp,
    MultiUrlResp,
    NoContentResp,
    R,
    S,
    SandboxSubmissionStatusResp,
    T,
    TextResp,
)
from .result import multi_result, result

USERAGENT_SUFFIX: str = "PyTMV1"
API_VERSION: str = "v3.0"

log: Logger = logging.getLogger(__name__)


class Core:
    def __init__(
        self,
        appname: str,
        token: str,
        url: str,
        pool_connections: int,
        pool_maxsize: int,
        connect_timeout: int,
        read_timeout: int,
    ):
        self._adapter = HTTPAdapter(pool_connections, pool_maxsize, 0, True)
        self._c_timeout = connect_timeout
        self._r_timeout = read_timeout
        self._appname = appname
        self._token = token
        self._url = str(TypeAdapter(AnyHttpUrl).validate_python(_format(url)))
        self._headers: Dict[str, str] = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": f"{self._appname}-{USERAGENT_SUFFIX}/{__version__}",
        }
        self._proxies: Optional[Dict[str, str]] = _proxy(
            os.getenv("HTTP_PROXY"), os.getenv("HTTPS_PROXY")
        )

    @result
    def send(
        self,
        class_: Type[R],
        api: str,
        method: HttpMethod = HttpMethod.GET,
        **kwargs: Any,
    ) -> R:
        return self._process(
            class_,
            api,
            method,
            **kwargs,
        )

    @multi_result
    def send_endpoint(
        self,
        api: Api,
        *tasks: EndpointRequest,
    ) -> MultiResp:
        return self._process(
            MultiResp,
            api,
            HttpMethod.POST,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in tasks
            ],
        )

    @result
    def send_linkable(
        self,
        class_: Type[BaseLinkableResp[C]],
        api: str,
        consumer: Callable[[C], None],
        **kwargs: Any,
    ) -> ConsumeLinkableResp:
        return ConsumeLinkableResp(
            total_consumed=self._consume_linkable(
                lambda: self._process(
                    class_,
                    api,
                    **kwargs,
                ),
                consumer,
                kwargs.get("headers", {}),
            )
        )

    @multi_result
    def send_multi(
        self,
        class_: Type[MR],
        api: str,
        **kwargs: Any,
    ) -> MR:
        return self._process(
            class_,
            api,
            HttpMethod.POST,
            **kwargs,
        )

    @result
    def send_sandbox_result(
        self,
        class_: Type[R],
        api: Api,
        submit_id: str,
        poll: bool,
        poll_time_sec: float,
    ) -> R:
        if poll:
            _poll_status(
                lambda: self._process(
                    SandboxSubmissionStatusResp,
                    Api.GET_SANDBOX_SUBMISSION_STATUS.value.format(submit_id),
                ),
                poll_time_sec,
            )
        return self._process(class_, api.value.format(submit_id))

    @result
    def send_task_result(
        self, class_: Type[T], task_id: str, poll: bool, poll_time_sec: float
    ) -> T:
        status_call: Callable[[], T] = lambda: self._process(
            class_,
            Api.GET_TASK_RESULT.value.format(task_id),
        )
        if poll:
            return _poll_status(
                status_call,
                poll_time_sec,
            )
        return status_call()

    def _consume_linkable(
        self,
        api_call: Callable[[], BaseLinkableResp[C]],
        consumer: Callable[[C], None],
        headers: Dict[str, str],
        count: int = 0,
    ) -> int:
        total_count: int = count
        response: BaseLinkableResp[C] = api_call()
        for item in response.items:
            consumer(item)
            total_count += 1
        if response.next_link:
            sr: SplitResult = urlsplit(response.next_link)
            log.debug("Found nextLink")
            return self._consume_linkable(
                lambda: self._process(
                    type(response),
                    f"{sr.path[5:]}?{sr.query}",
                    headers=headers,
                ),
                consumer,
                headers,
                total_count,
            )
        log.debug(
            "Records consumed: [Total=%s, Type=%s]",
            total_count,
            type(
                response.items[0] if len(response.items) > 0 else response
            ).__name__,
        )
        return total_count

    def _process(
        self,
        class_: Type[R],
        uri: str,
        method: HttpMethod = HttpMethod.GET,
        **kwargs: Any,
    ) -> R:
        log.debug(
            "Processing request [Method=%s, Class=%s, URI=%s, Options=%s]",
            method.value,
            class_.__name__,
            uri,
            kwargs,
        )
        raw_response: Response = self._send_internal(
            self._prepare(uri, method, **kwargs)
        )
        _validate(raw_response)
        return _parse_data(raw_response, class_)

    def _prepare(
        self, uri: str, method: HttpMethod, **kwargs: Any
    ) -> PreparedRequest:
        return Request(
            method.value,
            self._url + uri,
            headers={**self._headers, **kwargs.pop("headers", {})},
            **kwargs,
        ).prepare()

    def _send_internal(self, request: PreparedRequest) -> Response:
        log.info(
            "Sending request [Method=%s, URL=%s, Headers=%s, Body=%s]",
            request.method,
            request.url,
            re.sub("Bearer \\S+", "*****", str(request.headers)),
            _hide_binary(request),
        )
        response: Response = self._adapter.send(
            request,
            timeout=(self._c_timeout, self._r_timeout),
            proxies=self._proxies,
        )
        log.info(
            "Received response [Status=%s, Headers=%s, Body=%s]",
            response.status_code,
            response.headers,
            _hide_binary(response),
        )
        return response


def _proxy(
    http: Optional[str], https: Optional[str]
) -> Optional[Dict[str, str]]:
    proxies = {}
    if http:
        proxies["http"] = http
    if https:
        proxies["https"] = https
    log.debug("Proxy settings: %s", proxies)
    return proxies if len(proxies.items()) > 0 else None


def _format(url: str) -> str:
    return (url if url.endswith("/") else url + "/") + API_VERSION


def _hide_binary(http_object: Union[PreparedRequest, Response]) -> str:
    content_type = http_object.headers.get("Content-Type", "")
    if "json" not in content_type and "application" in content_type:
        return "***binary content***"
    if "multipart/form-data" in content_type:
        return "***file content***"
    if isinstance(http_object, Response):
        return http_object.text
    return str(http_object.body)


def _is_http_success(status_codes: List[int]) -> bool:
    return len(list(filter(lambda s: not 200 <= s < 399, status_codes))) == 0


def _parse_data(raw_response: Response, class_: Type[R]) -> R:
    content_type = raw_response.headers.get("Content-Type", "")
    if raw_response.status_code == 201:
        return class_(**raw_response.headers)
    if raw_response.status_code == 204 and class_ == NoContentResp:
        return class_()
    if "text" in content_type and class_ == TextResp:
        return class_.model_construct(text=raw_response.text)
    if "json" in content_type or "text" in content_type:
        log.debug("Parsing json response [Class=%s]", class_.__name__)
        if class_ in [MultiResp, MultiUrlResp, MultiApiKeyResp]:
            return class_(items=raw_response.json())
        if class_ == GetOatPackageResp:
            return class_(package=raw_response.json())
        if class_ in [
            GetAlertResp,
            GetApiKeyResp,
            GetAlertNoteResp,
            GetPipelineResp,
        ]:
            return class_(
                data=raw_response.json(),
                etag=raw_response.headers.get("ETag", ""),
            )
        if class_ == BaseTaskResp:
            resp_class: Type[BaseTaskResp] = utils.task_action_resp_class(
                TaskAction(raw_response.json()["action"])
            )
            class_ = resp_class if issubclass(resp_class, class_) else class_
        return class_(**raw_response.json())
    if (
        "application" in content_type
        or "gzip" == raw_response.headers.get("Content-Encoding")
    ) and class_ == BytesResp:
        log.debug("Parsing binary response")
        return class_.model_construct(content=raw_response.content)
    raise ParseModelError(class_.__name__, raw_response)


def _parse_html(html: str) -> str:
    log.info("Parsing html response [Html=%s]", html)
    soup = BeautifulSoup(html, "html.parser")
    return "\n".join(
        line.strip() for line in soup.text.split("\n") if line.strip()
    )


def _poll_status(
    status_call: Callable[[], S],
    poll_time_sec: float,
) -> S:
    start_time: float = time.time()
    elapsed_time: float = 0
    response: S = status_call()
    while elapsed_time < poll_time_sec:
        if response.status in [Status.QUEUED, Status.RUNNING]:
            time.sleep(2)
            response = status_call()
            elapsed_time = time.time() - start_time
        else:
            break
    return response


def _validate(raw_response: Response) -> None:
    log.debug("Validating response [%s]", raw_response)
    content_type: str = raw_response.headers.get("Content-Type", "")
    if not _is_http_success([raw_response.status_code]):
        if "application/json" in content_type:
            error: Dict[str, Any] = raw_response.json().get("error")
            error["status"] = raw_response.status_code
            raise ServerJsonError(
                Error(**error),
            )
        if "text/html" in content_type:
            raise ServerHtmlError(
                raw_response.status_code, _parse_html(raw_response.text)
            )
        raise ServerTextError(raw_response.status_code, raw_response.text)
    if raw_response.status_code == 207:
        if not _is_http_success(
            MsStatus(
                root=[int(d.get("status", 500)) for d in raw_response.json()]
            ).values()
        ):
            raise ServerMultiJsonError(
                [
                    MsError.model_validate(error)
                    for error in raw_response.json()
                ]
            )
