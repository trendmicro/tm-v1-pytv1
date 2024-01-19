from typing import Callable

from .. import utils
from ..core import Core
from ..model.common import ExceptionObject, SuspiciousObject
from ..model.enum import Api
from ..model.request import ObjectRequest, SuspiciousObjectRequest
from ..model.response import (
    ConsumeLinkableResp,
    ListExceptionsResp,
    ListSuspiciousResp,
    MultiResp,
)
from ..result import MultiResult, Result


class Object:
    _core: Core

    def __init__(self, core: Core):
        self._core = core

    def add_block(self, *objects: ObjectRequest) -> MultiResult[MultiResp]:
        """Adds object(s) to the Suspicious Object List,
        which blocks the objects on subsequent detections.

        :param objects: Object(s) to add.
        :type objects: Tuple[ObjectTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.ADD_TO_BLOCK_LIST,
            json=utils.build_object_request(*objects),
        )

    def delete_block(self, *objects: ObjectRequest) -> MultiResult[MultiResp]:
        """Removes object(s) that was added to the Suspicious Object List
          using the "Add to block list" action

        :param objects: Object(s) to remove.
        :type objects: Tuple[ObjectTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.REMOVE_FROM_BLOCK_LIST,
            json=utils.build_object_request(*objects),
        )

    def add_exception(self, *objects: ObjectRequest) -> MultiResult[MultiResp]:
        """Adds object(s) to the Exception List.

        :param objects: Object(s) to add.
        :type objects: Tuple[ObjectTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.ADD_TO_EXCEPTION_LIST,
            json=utils.build_object_request(*objects),
        )

    def delete_exception(
        self, *objects: ObjectRequest
    ) -> MultiResult[MultiResp]:
        """Removes object(s) from the Exception List.

        :param objects: Object(s) to remove.
        :type objects: Tuple[ObjectTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.REMOVE_FROM_EXCEPTION_LIST,
            json=utils.build_object_request(*objects),
        )

    def add_suspicious(
        self, *objects: SuspiciousObjectRequest
    ) -> MultiResult[MultiResp]:
        """Adds object(s) to the Suspicious Object List.

        :param objects: Object(s) to add.
        :type objects: Tuple[SuspiciousObjectTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.ADD_TO_SUSPICIOUS_LIST,
            json=utils.build_suspicious_request(*objects),
        )

    def delete_suspicious(
        self, *objects: ObjectRequest
    ) -> MultiResult[MultiResp]:
        """Removes object(s) from the Suspicious List.

        :param objects: Object(s) to remove.
        :type objects: Tuple[ObjectTask, ...]
        :rtype: MultiResult[MultiResp]
        """
        return self._core.send_multi(
            MultiResp,
            Api.REMOVE_FROM_SUSPICIOUS_LIST,
            json=utils.build_object_request(*objects),
        )

    def list_exception(self) -> Result[ListExceptionsResp]:
        """Retrieves exception objects in a paginated list.

        :rtype: Result[GetExceptionListResp]:
        """
        return self._core.send(ListExceptionsResp, Api.GET_EXCEPTION_OBJECTS)

    def list_suspicious(
        self,
    ) -> Result[ListSuspiciousResp]:
        """Retrieves suspicious objects in a paginated list.

        :rtype: Result[GetSuspiciousListResp]:
        """
        return self._core.send(ListSuspiciousResp, Api.GET_SUSPICIOUS_OBJECTS)

    def consume_exception(
        self, consumer: Callable[[ExceptionObject], None]
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume exception objects.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[ExceptionObject], None]
        :rtype: Result[ConsumeLinkableResp]:
        """
        return self._core.send_linkable(
            ListExceptionsResp, Api.GET_EXCEPTION_OBJECTS, consumer
        )

    def consume_suspicious(
        self, consumer: Callable[[SuspiciousObject], None]
    ) -> Result[ConsumeLinkableResp]:
        """Retrieves and consume suspicious objects.

        :param consumer: Function which will consume every record in result.
        :type consumer: Callable[[SuspiciousObject], None]
        :rtype: Result[ConsumeLinkableResp]:
        """
        return self._core.send_linkable(
            ListSuspiciousResp, Api.GET_SUSPICIOUS_OBJECTS, consumer
        )
