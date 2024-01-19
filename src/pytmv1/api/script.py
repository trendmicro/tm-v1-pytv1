from typing import Callable, Optional

from .. import utils
from ..core import Core
from ..model.common import Script
from ..model.enum import Api, HttpMethod, QueryOp, ScriptType
from ..model.request import CustomScriptRequest
from ..model.response import (
    AddCustomScriptResp,
    ConsumeLinkableResp,
    ListCustomScriptsResp,
    MultiResp,
    NoContentResp,
    TextResp,
)
from ..result import MultiResult, Result


class CustomScript:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def create(
        self,
        script_type: ScriptType,
        script_name: str,
        script_content: str,
        description: Optional[str] = None,
    ) -> Result[AddCustomScriptResp]:
        """
        Uploads a custom script. Supported file extensions: .ps1, .sh.
        Note: Custom scripts must use UTF-8 encoding.
        :param script_type: File type.
        :type script_type: ScriptType
        :param script_name: File name.
        :type script_name: str
        :param script_content: Plain text content of the script.
        :type script_content: str
        :param description: Description.
        :type description: Optional[str]
        :return: Result[AddACustomScriptResp]
        """
        return self._core.send(
            AddCustomScriptResp,
            Api.ADD_CUSTOM_SCRIPT,
            HttpMethod.POST,
            data=utils.filter_none(
                {"fileType": script_type.value, "description": description}
            ),
            files={
                "file": (
                    script_name,
                    bytes(script_content, "utf-8"),
                    "text/plain",
                )
            },
        )

    def update(
        self,
        script_id: str,
        script_type: ScriptType,
        script_name: str,
        script_content: str,
        description: Optional[str] = None,
    ) -> Result[NoContentResp]:
        """
        Updates a custom script. Supported file extensions: .ps1, .sh.
        Note: Custom scripts must use UTF-8 encoding.
        :param script_id: Unique string that identifies a script file.
        :type script_id: str
        :param script_type: File type.
        :type script_type: ScriptType
        :param script_name: File name.
        :type script_name: str
        :param script_content: Plain text content of the file.
        :type script_content: str
        :param description: Description.
        :type description: Optional[str]
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.UPDATE_CUSTOM_SCRIPT.value.format(script_id),
            HttpMethod.POST,
            data=utils.filter_none(
                {"fileType": script_type.value, "description": description}
            ),
            files={
                "file": (
                    script_name,
                    bytes(script_content, "utf-8"),
                    "text/plain",
                )
            },
        )

    def download(self, script_id: str) -> Result[TextResp]:
        """Downloads custom script.

        :param script_id: Unique string that identifies a script file.
        :type script_id: str
        :return: Result[BytesResp]
        """
        return self._core.send(
            TextResp, Api.DOWNLOAD_CUSTOM_SCRIPT.value.format(script_id)
        )

    def delete(self, script_id: str) -> Result[NoContentResp]:
        """Deletes custom script.

        :param script_id: Unique string that identifies a script file.
        :type script_id: str
        :return: Result[NoContentResp]
        """
        return self._core.send(
            NoContentResp,
            Api.DELETE_CUSTOM_SCRIPT.value.format(script_id),
            HttpMethod.DELETE,
        )

    def list(
        self, op: QueryOp = QueryOp.AND, **fields: str
    ) -> Result[ListCustomScriptsResp]:
        """Retrieves scripts in a paginated list filtered by provided values.

        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:fileName="1.sh"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :return: Result[GetCustomScriptsResp]
        """
        return self._core.send(
            ListCustomScriptsResp,
            Api.GET_CUSTOM_SCRIPTS,
            params=utils.filter_query(op, fields),
        )

    def run(self, *scripts: CustomScriptRequest) -> MultiResult[MultiResp]:
        """Runs multiple custom script.

        :param scripts: Custom scripts to run.
        :type scripts: Tuple[CustomScriptTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.RUN_CUSTOM_SCRIPT,
            json=[
                task.model_dump(by_alias=True, exclude_none=True)
                for task in scripts
            ],
        )

    def consume(
        self,
        consumer: Callable[[Script], None],
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume cust. scripts filtered by provided values.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[Script], None]
        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:fileName="1.sh"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :return: Result[ConsumeLinkableResp]
        """
        return self._core.send_linkable(
            ListCustomScriptsResp,
            Api.GET_CUSTOM_SCRIPTS,
            consumer,
            params=utils.filter_query(op, fields),
        )
