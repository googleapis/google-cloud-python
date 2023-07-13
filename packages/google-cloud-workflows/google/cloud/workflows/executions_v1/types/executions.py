# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.workflows.executions.v1",
    manifest={
        "ExecutionView",
        "Execution",
        "ListExecutionsRequest",
        "ListExecutionsResponse",
        "CreateExecutionRequest",
        "GetExecutionRequest",
        "CancelExecutionRequest",
    },
)


class ExecutionView(proto.Enum):
    r"""Defines possible views for execution resource.

    Values:
        EXECUTION_VIEW_UNSPECIFIED (0):
            The default / unset value.
        BASIC (1):
            Includes only basic metadata about the execution. Following
            fields are returned: name, start_time, end_time, state and
            workflow_revision_id.
        FULL (2):
            Includes all data.
    """
    EXECUTION_VIEW_UNSPECIFIED = 0
    BASIC = 1
    FULL = 2


class Execution(proto.Message):
    r"""A running instance of a
    `Workflow </workflows/docs/reference/rest/v1/projects.locations.workflows>`__.

    Attributes:
        name (str):
            Output only. The resource name of the
            execution. Format:

            projects/{project}/locations/{location}/workflows/{workflow}/executions/{execution}
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Marks the beginning of
            execution.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Marks the end of execution,
            successful or not.
        state (google.cloud.workflows.executions_v1.types.Execution.State):
            Output only. Current state of the execution.
        argument (str):
            Input parameters of the execution represented as a JSON
            string. The size limit is 32KB.

            *Note*: If you are using the REST API directly to run your
            workflow, you must escape any JSON string value of
            ``argument``. Example:
            ``'{"argument":"{\"firstName\":\"FIRST\",\"lastName\":\"LAST\"}"}'``
        result (str):
            Output only. Output of the execution represented as a JSON
            string. The value can only be present if the execution's
            state is ``SUCCEEDED``.
        error (google.cloud.workflows.executions_v1.types.Execution.Error):
            Output only. The error which caused the execution to finish
            prematurely. The value is only present if the execution's
            state is ``FAILED`` or ``CANCELLED``.
        workflow_revision_id (str):
            Output only. Revision of the workflow this
            execution is using.
        call_log_level (google.cloud.workflows.executions_v1.types.Execution.CallLogLevel):
            The call logging level associated to this
            execution.
    """

    class State(proto.Enum):
        r"""Describes the current state of the execution. More states
        might be added in the future.

        Values:
            STATE_UNSPECIFIED (0):
                Invalid state.
            ACTIVE (1):
                The execution is in progress.
            SUCCEEDED (2):
                The execution finished successfully.
            FAILED (3):
                The execution failed with an error.
            CANCELLED (4):
                The execution was stopped intentionally.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLED = 4

    class CallLogLevel(proto.Enum):
        r"""Describes the level of platform logging to apply to calls and
        call responses during workflow executions.

        Values:
            CALL_LOG_LEVEL_UNSPECIFIED (0):
                No call logging specified.
            LOG_ALL_CALLS (1):
                Log all call steps within workflows, all call
                returns, and all exceptions raised.
            LOG_ERRORS_ONLY (2):
                Log only exceptions that are raised from call
                steps within workflows.
        """
        CALL_LOG_LEVEL_UNSPECIFIED = 0
        LOG_ALL_CALLS = 1
        LOG_ERRORS_ONLY = 2

    class StackTraceElement(proto.Message):
        r"""A single stack element (frame) where an error occurred.

        Attributes:
            step (str):
                The step the error occurred at.
            routine (str):
                The routine where the error occurred.
            position (google.cloud.workflows.executions_v1.types.Execution.StackTraceElement.Position):
                The source position information of the stack
                trace element.
        """

        class Position(proto.Message):
            r"""Position contains source position information about the stack
            trace element such as line number, column number and length of
            the code block in bytes.

            Attributes:
                line (int):
                    The source code line number the current
                    instruction was generated from.
                column (int):
                    The source code column position (of the line)
                    the current instruction was generated from.
                length (int):
                    The number of bytes of source code making up
                    this stack trace element.
            """

            line: int = proto.Field(
                proto.INT64,
                number=1,
            )
            column: int = proto.Field(
                proto.INT64,
                number=2,
            )
            length: int = proto.Field(
                proto.INT64,
                number=3,
            )

        step: str = proto.Field(
            proto.STRING,
            number=1,
        )
        routine: str = proto.Field(
            proto.STRING,
            number=2,
        )
        position: "Execution.StackTraceElement.Position" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Execution.StackTraceElement.Position",
        )

    class StackTrace(proto.Message):
        r"""A collection of stack elements (frames) where an error
        occurred.

        Attributes:
            elements (MutableSequence[google.cloud.workflows.executions_v1.types.Execution.StackTraceElement]):
                An array of stack elements.
        """

        elements: MutableSequence["Execution.StackTraceElement"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Execution.StackTraceElement",
        )

    class Error(proto.Message):
        r"""Error describes why the execution was abnormally terminated.

        Attributes:
            payload (str):
                Error message and data returned represented
                as a JSON string.
            context (str):
                Human-readable stack trace string.
            stack_trace (google.cloud.workflows.executions_v1.types.Execution.StackTrace):
                Stack trace with detailed information of
                where error was generated.
        """

        payload: str = proto.Field(
            proto.STRING,
            number=1,
        )
        context: str = proto.Field(
            proto.STRING,
            number=2,
        )
        stack_trace: "Execution.StackTrace" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Execution.StackTrace",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    argument: str = proto.Field(
        proto.STRING,
        number=5,
    )
    result: str = proto.Field(
        proto.STRING,
        number=6,
    )
    error: Error = proto.Field(
        proto.MESSAGE,
        number=7,
        message=Error,
    )
    workflow_revision_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    call_log_level: CallLogLevel = proto.Field(
        proto.ENUM,
        number=9,
        enum=CallLogLevel,
    )


class ListExecutionsRequest(proto.Message):
    r"""Request for the [ListExecutions][] method.

    Attributes:
        parent (str):
            Required. Name of the workflow for which the
            executions should be listed. Format:
            projects/{project}/locations/{location}/workflows/{workflow}
        page_size (int):
            Maximum number of executions to return per
            call. Max supported value depends on the
            selected Execution view: it's 10000 for BASIC
            and 100 for FULL. The default value used if the
            field is not specified is 100, regardless of the
            selected view. Values greater than the max value
            will be coerced down to it.
        page_token (str):
            A page token, received from a previous ``ListExecutions``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListExecutions`` must match the call that provided the
            page token.
        view (google.cloud.workflows.executions_v1.types.ExecutionView):
            Optional. A view defining which fields should
            be filled in the returned executions. The API
            will default to the BASIC view.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    view: "ExecutionView" = proto.Field(
        proto.ENUM,
        number=4,
        enum="ExecutionView",
    )


class ListExecutionsResponse(proto.Message):
    r"""Response for the
    [ListExecutions][google.cloud.workflows.executions.v1.Executions.ListExecutions]
    method.

    Attributes:
        executions (MutableSequence[google.cloud.workflows.executions_v1.types.Execution]):
            The executions which match the request.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    executions: MutableSequence["Execution"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Execution",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateExecutionRequest(proto.Message):
    r"""Request for the
    [CreateExecution][google.cloud.workflows.executions.v1.Executions.CreateExecution]
    method.

    Attributes:
        parent (str):
            Required. Name of the workflow for which an
            execution should be created. Format:
            projects/{project}/locations/{location}/workflows/{workflow}
            The latest revision of the workflow will be
            used.
        execution (google.cloud.workflows.executions_v1.types.Execution):
            Required. Execution to be created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    execution: "Execution" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Execution",
    )


class GetExecutionRequest(proto.Message):
    r"""Request for the
    [GetExecution][google.cloud.workflows.executions.v1.Executions.GetExecution]
    method.

    Attributes:
        name (str):
            Required. Name of the execution to be
            retrieved. Format:

            projects/{project}/locations/{location}/workflows/{workflow}/executions/{execution}
        view (google.cloud.workflows.executions_v1.types.ExecutionView):
            Optional. A view defining which fields should
            be filled in the returned execution. The API
            will default to the FULL view.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: "ExecutionView" = proto.Field(
        proto.ENUM,
        number=2,
        enum="ExecutionView",
    )


class CancelExecutionRequest(proto.Message):
    r"""Request for the
    [CancelExecution][google.cloud.workflows.executions.v1.Executions.CancelExecution]
    method.

    Attributes:
        name (str):
            Required. Name of the execution to be
            cancelled. Format:

            projects/{project}/locations/{location}/workflows/{workflow}/executions/{execution}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
