from typing import Type, Callable, List, Optional

from ..core import Core
from ..model.response import (
    BaseTaskResp,
    T,
    GetTaskListResp,
    ConsumeLinkableResp,
)
from ..result import Result
from .. import utils
from ..model.enum import Api, QueryOp


class Task:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def get_result(
        self,
        task_id: str,
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[BaseTaskResp]:
        """Retrieves the result of a response task.

        :param task_id: Task id.
        :type task_id: str
        :param poll: If we should wait until the task is finished before
         to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result
        to be available.
        :type poll_time_sec: float
        :rtype: Result[T]:
        """
        return self.get_result_class(
            task_id, BaseTaskResp, poll, poll_time_sec
        )

    def list_result(
        self,
        start_date_time: Optional[str] = None,
        end_date_time: Optional[str] = None,
        date_time_target: Optional[str] = None,
        top: int = 50,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[GetTaskListResp]:
        """
        Retrieves  response task list
        """
        return self._core.send(
            GetTaskListResp,
            Api.TASK_RESULT,
            params=utils.filter_none(
                {
                    "startDateTime": start_date_time,
                    "endDateTime": end_date_time,
                    "dateTimeTarget": date_time_target,
                    "top": top,
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def consume(
        self,
        consumer: Callable[[BaseTaskResp], None],
        start_date_time: Optional[str] = None,
        end_date_time: Optional[str] = None,
        date_time_target: Optional[str] = None,
        top: int = 50,
        op: QueryOp = QueryOp.AND,
        **fields: str,
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume task result.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[GetTaskListResp], None]
        :param start_date_time: Date that indicates the start of
        the event detection data retrieval time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to 24 hours before the request is made.
        :type detected_start_date_time: Optional[str]
        :param detected_end_date_time: Date that indicates the end of
        the event detection data retrieval time range (yyyy-MM-ddThh:mm:ssZ).
        Defaults to the time the request is made.
        :type detected_end_date_time: Optional[str]
        :param ingested_start_date_time: Date that indicates the start of
        the data ingestion time range (yyyy-MM-ddThh:mm:ssZ).
        :type ingested_start_date_time: Optional[str]
        :param ingested_end_date_time: Date that indicates the end of
        the data ingestion time range (yyyy-MM-ddThh:mm:ssZ).
        :type ingested_end_date_time: Optional[str]
        :param top: Number of records displayed on a page.
        :type top: int
        :param op: Operator to apply between fields (ie: ... OR ...).
        :type op: QueryOp
        :param fields: Field/value used to filter result (i.e:uuid="123"),
        check Vision One API documentation for full list of supported fields.
        :type fields: Dict[str, str]
        :rtype: Result[ConsumeLinkableResp]
        """
        return self._core.send_linkable(
            GetTaskListResp,
            Api.TASK_RESULT,
            consumer,
            params=utils.filter_none(
                {
                    "startDateTime": start_date_time,
                    "endDateTime": end_date_time,
                    "dateTimeTarget": date_time_target,
                    "top": top,
                }
            ),
            headers=utils.tmv1_filter(op, fields),
        )

    def get_result_class(
        self,
        task_id: str,
        class_: Type[T],
        poll: bool = True,
        poll_time_sec: float = 1800,
    ) -> Result[T]:
        """Retrieves the result of a response task.

        :param task_id: Task id.
        :type task_id: str
        :param class_: Expected task result class.
        :type class_: Type[T]
        :param poll: If we should wait until the task is finished before
         to return the result.
        :type poll: bool
        :param poll_time_sec: Maximum time to wait for the result
        to be available.
        :type poll_time_sec: float
        :rtype: Result[T]:
        """
        return self._core.send_task_result(
            class_, task_id, poll, poll_time_sec
        )
