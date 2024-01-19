from typing import Optional

from .. import utils
from ..core import Core
from ..model.enum import Api, HttpMethod
from ..model.response import (
    BytesResp,
    ListSandboxSuspiciousResp,
    MultiUrlResp,
    SandboxAnalysisResultResp,
    SandboxSubmissionStatusResp,
    SubmitFileToSandboxResp,
)
from ..result import MultiResult, Result


class Sandbox:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def submit_file(
        self,
        file: bytes,
        file_name: str,
        document_password: Optional[str] = None,
        archive_password: Optional[str] = None,
        arguments: Optional[str] = None,
    ) -> Result[SubmitFileToSandboxResp]:
        """Submits a file to the sandbox for analysis.

        :param file: Raw content in bytes.
        :type file: bytes
        :param file_name: Name of the file.
        :type file_name: str
        :param document_password: Password used to
         decrypt the submitted file sample.
        :type document_password: Optional[str]
        :param archive_password: Password encoded in Base64 used to decrypt
         the submitted archive.
        :type archive_password: Optional[str]
        :param arguments: Command line arguments to run the submitted file.
         Only available for Portable Executable (PE) files and script files.
        :type arguments: Optional[str]
        :rtype: Result[SubmitFileToSandboxResp]:
        """
        return self._core.send(
            SubmitFileToSandboxResp,
            Api.SUBMIT_FILE_TO_SANDBOX,
            HttpMethod.POST,
            data=utils.build_sandbox_file_request(
                document_password, archive_password, arguments
            ),
            files={"file": (file_name, file, "application/octet-stream")},
        )

    def submit_url(self, *urls: str) -> MultiResult[MultiUrlResp]:
        """Submits URLs to the sandbox for analysis.

        :param urls: URL(s) to be submitted.
        :type urls: Tuple[str, ...]
        :rtype: MultiResult[MultiUrlResp]
        """
        return self._core.send_multi(
            MultiUrlResp,
            Api.SUBMIT_URLS_TO_SANDBOX,
            json=[{"url": url} for url in urls],
        )

    def download_analysis_result(
        self,
        submit_id: str,
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[BytesResp]:
        """Downloads the analysis results of the specified object as PDF.

        :param submit_id: Sandbox submission id.
        :type submit_id: str
        :param poll: If we should wait until the task is finished before
        to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result to
         be available.
        :type poll_time_sec: float
        :rtype: Result[BytesResp]:
        """
        return self._core.send_sandbox_result(
            BytesResp,
            Api.DOWNLOAD_SANDBOX_ANALYSIS_RESULT,
            submit_id,
            poll,
            poll_time_sec,
        )

    def download_investigation_package(
        self,
        submit_id: str,
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[BytesResp]:
        """Downloads the Investigation Package of the specified object.

        :param submit_id: Sandbox submission id.
        :type submit_id: str
        :param poll: If we should wait until the task is finished before
        to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result to
         be available.
        :type poll_time_sec: float
        :rtype: Result[BytesResp]:
        """
        return self._core.send_sandbox_result(
            BytesResp,
            Api.DOWNLOAD_SANDBOX_INVESTIGATION_PACKAGE,
            submit_id,
            poll,
            poll_time_sec,
        )

    def get_analysis_result(
        self,
        submit_id: str,
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[SandboxAnalysisResultResp]:
        """Retrieves the analysis results of the specified object.

        :param submit_id: Sandbox submission id.
        :type submit_id: str
        :param poll: If we should wait until the task is finished before
         to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result
         to be available.
        :type poll_time_sec: float
        :rtype: Result[SandboxAnalysisResultResp]:
        """
        return self._core.send_sandbox_result(
            SandboxAnalysisResultResp,
            Api.GET_SANDBOX_ANALYSIS_RESULT,
            submit_id,
            poll,
            poll_time_sec,
        )

    def get_submission_status(
        self, submit_id: str
    ) -> Result[SandboxSubmissionStatusResp]:
        """Retrieves the submission status of the specified object.

        :param submit_id: Sandbox submission id.
        :type submit_id: str
        :rtype: Result[SandboxSubmissionStatusResp]:
        """
        return self._core.send(
            SandboxSubmissionStatusResp,
            Api.GET_SANDBOX_SUBMISSION_STATUS.value.format(submit_id),
        )

    def list_suspicious(
        self,
        submit_id: str,
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[ListSandboxSuspiciousResp]:
        """Retrieves the suspicious object list associated to the
        specified object.

        :param submit_id: Sandbox submission id.
        :type submit_id: str
        :param poll: If we should wait until the task is finished before
         to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result
         to be available.
        :type poll_time_sec: float
        :rtype: Result[SandboxSuspiciousListResp]:
        """
        return self._core.send_sandbox_result(
            ListSandboxSuspiciousResp,
            Api.GET_SANDBOX_SUSPICIOUS_LIST,
            submit_id,
            poll,
            poll_time_sec,
        )
