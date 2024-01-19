from typing import Type

from ..core import Core
from ..model.response import BaseTaskResp, T
from ..result import Result


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
