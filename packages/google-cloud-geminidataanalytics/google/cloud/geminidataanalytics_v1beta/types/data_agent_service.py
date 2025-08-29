# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.geminidataanalytics_v1beta.types import data_agent as gcg_data_agent

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1beta",
    manifest={
        "ListDataAgentsRequest",
        "ListDataAgentsResponse",
        "ListAccessibleDataAgentsRequest",
        "ListAccessibleDataAgentsResponse",
        "GetDataAgentRequest",
        "CreateDataAgentRequest",
        "UpdateDataAgentRequest",
        "DeleteDataAgentRequest",
        "OperationMetadata",
    },
)


class ListDataAgentsRequest(proto.Message):
    r"""Message for requesting list of DataAgents.

    Attributes:
        parent (str):
            Required. Parent value for
            ListDataAgentsRequest.
        page_size (int):
            Optional. Server may return fewer items than
            requested. If unspecified, server will pick an
            appropriate default.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListDataAgents`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListDataAgents`` must match the call that provided the
            page token. The service may return fewer than this value.
        filter (str):
            Optional. Filtering results. See
            `AIP-160 <https://google.aip.dev/160>`__ for syntax.
        order_by (str):
            Optional. User specification for how to order
            the results.
        show_deleted (bool):
            Optional. If true, the list results will
            include soft-deleted DataAgents. Defaults to
            false.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    show_deleted: bool = proto.Field(
        proto.BOOL,
        number=6,
    )


class ListDataAgentsResponse(proto.Message):
    r"""Message for response to listing DataAgents.

    Attributes:
        data_agents (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.DataAgent]):
            The list of DataAgent.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (MutableSequence[str]):
            Unordered list. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    data_agents: MutableSequence[gcg_data_agent.DataAgent] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcg_data_agent.DataAgent,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ListAccessibleDataAgentsRequest(proto.Message):
    r"""Message for requesting list of accessible DataAgents.

    Attributes:
        parent (str):
            Required. Parent value for
            ListAccessibleDataAgentsRequest.
        page_size (int):
            Optional. Server may return fewer items than
            requested. If unspecified, server will pick an
            appropriate default.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListAccessibleDataAgents`` call. Provide this to retrieve
            the subsequent page.

            When paginating, all other parameters provided to
            ``ListAccessibleDataAgents`` must match the call that
            provided the page token. The service may return fewer than
            this value.
        filter (str):
            Optional. Filtering results. See
            `AIP-160 <https://google.aip.dev/160>`__ for syntax.
        order_by (str):
            Optional. User specification for how to order
            the results.
        show_deleted (bool):
            Optional. If true, the list results will
            include soft-deleted DataAgents. Defaults to
            false.
        creator_filter (google.cloud.geminidataanalytics_v1beta.types.ListAccessibleDataAgentsRequest.CreatorFilter):
            Optional. Filter for the creator of the
            agent.
    """

    class CreatorFilter(proto.Enum):
        r"""Filter for the creator of the agent.

        Values:
            CREATOR_FILTER_UNSPECIFIED (0):
                Default value.
            NONE (1):
                No creator-specific filter will be applied.
                All agents will be returned.
            CREATOR_ONLY (2):
                Only agents created by the user calling the
                API will be returned.
            NOT_CREATOR_ONLY (3):
                Only agents not created by the user calling
                the API will be returned.
        """
        CREATOR_FILTER_UNSPECIFIED = 0
        NONE = 1
        CREATOR_ONLY = 2
        NOT_CREATOR_ONLY = 3

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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    show_deleted: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    creator_filter: CreatorFilter = proto.Field(
        proto.ENUM,
        number=7,
        enum=CreatorFilter,
    )


class ListAccessibleDataAgentsResponse(proto.Message):
    r"""Message for response to listing accessible DataAgents.

    Attributes:
        data_agents (MutableSequence[google.cloud.geminidataanalytics_v1beta.types.DataAgent]):
            The list of accessible DataAgent.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (MutableSequence[str]):
            Unordered list. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    data_agents: MutableSequence[gcg_data_agent.DataAgent] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcg_data_agent.DataAgent,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetDataAgentRequest(proto.Message):
    r"""Message for getting a DataAgent.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateDataAgentRequest(proto.Message):
    r"""Message for creating a DataAgent.

    Attributes:
        parent (str):
            Required. Value for parent.
        data_agent_id (str):
            Optional. Id of the requesting object. Must be unique within
            the parent. The allowed format is:
            ``^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$``. If not provided, the
            server will auto-generate a value for the id.
        data_agent (google.cloud.geminidataanalytics_v1beta.types.DataAgent):
            Required. The resource being created.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_agent_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    data_agent: gcg_data_agent.DataAgent = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gcg_data_agent.DataAgent,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateDataAgentRequest(proto.Message):
    r"""Message for updating a DataAgent.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask is used to specify the fields to be
            overwritten in the DataAgent resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields with non-default values present in the
            request will be overwritten. If a wildcard mask is provided,
            all fields will be overwritten.
        data_agent (google.cloud.geminidataanalytics_v1beta.types.DataAgent):
            Required. The resource being updated.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    data_agent: gcg_data_agent.DataAgent = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcg_data_agent.DataAgent,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteDataAgentRequest(proto.Message):
    r"""Message for deleting a DataAgent.

    Attributes:
        name (str):
            Required. Name of the resource.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
