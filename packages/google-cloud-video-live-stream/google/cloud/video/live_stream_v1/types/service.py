# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.cloud.video.live_stream_v1.types import resources
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.video.livestream.v1",
    manifest={
        "CreateChannelRequest",
        "ListChannelsRequest",
        "ListChannelsResponse",
        "GetChannelRequest",
        "DeleteChannelRequest",
        "UpdateChannelRequest",
        "StartChannelRequest",
        "StopChannelRequest",
        "CreateInputRequest",
        "ListInputsRequest",
        "ListInputsResponse",
        "GetInputRequest",
        "DeleteInputRequest",
        "UpdateInputRequest",
        "CreateEventRequest",
        "ListEventsRequest",
        "ListEventsResponse",
        "GetEventRequest",
        "DeleteEventRequest",
        "ChannelOperationResponse",
        "OperationMetadata",
    },
)


class CreateChannelRequest(proto.Message):
    r"""Request message for "LivestreamService.CreateChannel".

    Attributes:
        parent (str):
            Required. The parent location for the resource, in the form
            of: ``projects/{project}/locations/{location}``.
        channel (google.cloud.video.live_stream_v1.types.Channel):
            Required. The channel resource to be created.
        channel_id (str):
            Required. The ID of the channel resource to be created. This
            value must be 1-63 characters, begin and end with
            ``[a-z0-9]``, could contain dashes (-) in between.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    channel = proto.Field(proto.MESSAGE, number=2, message=resources.Channel,)
    channel_id = proto.Field(proto.STRING, number=3,)
    request_id = proto.Field(proto.STRING, number=4,)


class ListChannelsRequest(proto.Message):
    r"""Request message for "LivestreamService.ListChannels".

    Attributes:
        parent (str):
            Required. The parent location for the resource, in the form
            of: ``projects/{project}/locations/{location}``.
        page_size (int):
            The maximum number of items to return. If unspecified,
            server will pick an appropriate default. Server may return
            fewer items than requested. A caller should only rely on
            response's
            [next_page_token][google.cloud.video.livestream.v1.ListChannelsResponse.next_page_token]
            to determine if there are more items left to be queried.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
        filter (str):
            The filter to apply to list results.
        order_by (str):
            Specifies the ordering of results following syntax at
            https://cloud.google.com/apis/design/design_patterns#sorting_order.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListChannelsResponse(proto.Message):
    r"""Response message for "LivestreamService.ListChannels".

    Attributes:
        channels (Sequence[google.cloud.video.live_stream_v1.types.Channel]):
            A list of channels.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    channels = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.Channel,)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetChannelRequest(proto.Message):
    r"""Request message for "LivestreamService.GetChannel".

    Attributes:
        name (str):
            Required. The name of the channel resource, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteChannelRequest(proto.Message):
    r"""Request message for "LivestreamService.DeleteChannel".

    Attributes:
        name (str):
            Required. The name of the channel resource, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}``.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes after
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
        force (bool):
            If the ``force`` field is set to the default value of
            ``false``, you must delete all of a channel's events before
            you can delete the channel itself. If the field is set to
            ``true``, requests to delete a channel also delete
            associated channel events.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)
    force = proto.Field(proto.BOOL, number=3,)


class UpdateChannelRequest(proto.Message):
    r"""Request message for "LivestreamService.UpdateChannel".

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the Channel resource by the update. You can only update
            the following fields:

            -  ```inputAttachments`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#inputattachment>`__
            -  ```output`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#output>`__
            -  ```elementaryStreams`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#ElementaryStream>`__
            -  ```muxStreams`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#muxstream>`__
            -  ```manifests`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#Manifest>`__
            -  ```spritesheets`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.channels#spritesheet>`__

            The fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask.
        channel (google.cloud.video.live_stream_v1.types.Channel):
            Required. The channel resource to be updated.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    channel = proto.Field(proto.MESSAGE, number=2, message=resources.Channel,)
    request_id = proto.Field(proto.STRING, number=3,)


class StartChannelRequest(proto.Message):
    r"""Request message for "LivestreamService.StartChannel".

    Attributes:
        name (str):
            Required. The name of the channel resource, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}``.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class StopChannelRequest(proto.Message):
    r"""Request message for "LivestreamService.StopChannel".

    Attributes:
        name (str):
            Required. The name of the channel resource, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}``.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class CreateInputRequest(proto.Message):
    r"""Request message for "LivestreamService.CreateInput".

    Attributes:
        parent (str):
            Required. The parent location for the resource, in the form
            of: ``projects/{project}/locations/{location}``.
        input (google.cloud.video.live_stream_v1.types.Input):
            Required. The input resource to be created.
        input_id (str):
            Required. The ID of the input resource to be created. This
            value must be 1-63 characters, begin and end with
            ``[a-z0-9]``, could contain dashes (-) in between.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    input = proto.Field(proto.MESSAGE, number=2, message=resources.Input,)
    input_id = proto.Field(proto.STRING, number=3,)
    request_id = proto.Field(proto.STRING, number=4,)


class ListInputsRequest(proto.Message):
    r"""Request message for "LivestreamService.ListInputs".

    Attributes:
        parent (str):
            Required. The parent location for the resource, in the form
            of: ``projects/{project}/locations/{location}``.
        page_size (int):
            The maximum number of items to return. If unspecified,
            server will pick an appropriate default. Server may return
            fewer items than requested. A caller should only rely on
            response's
            [next_page_token][google.cloud.video.livestream.v1.ListInputsResponse.next_page_token]
            to determine if there are more items left to be queried.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
        filter (str):
            The filter to apply to list results.
        order_by (str):
            Specifies the ordering of results following syntax at
            `Sorting
            Order <https://cloud.google.com/apis/design/design_patterns#sorting_order>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListInputsResponse(proto.Message):
    r"""Response message for "LivestreamService.ListInputs".

    Attributes:
        inputs (Sequence[google.cloud.video.live_stream_v1.types.Input]):
            A list of inputs.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    inputs = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.Input,)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetInputRequest(proto.Message):
    r"""Request message for "LivestreamService.GetInput".

    Attributes:
        name (str):
            Required. The name of the input resource, in the form of:
            ``projects/{project}/locations/{location}/inputs/{inputId}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteInputRequest(proto.Message):
    r"""Request message for "LivestreamService.DeleteInput".

    Attributes:
        name (str):
            Required. The name of the input resource, in the form of:
            ``projects/{project}/locations/{location}/inputs/{inputId}``.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class UpdateInputRequest(proto.Message):
    r"""Request message for "LivestreamService.UpdateInput".

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the Input resource by the update. You can only update the
            following fields:

            -  ```preprocessingConfig`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.inputs#PreprocessingConfig>`__
            -  ```securityRules`` <https://cloud.google.com/livestream/docs/reference/rest/v1/projects.locations.inputs#SecurityRule>`__

            The fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask.
        input (google.cloud.video.live_stream_v1.types.Input):
            Required. The input resource to be updated.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    input = proto.Field(proto.MESSAGE, number=2, message=resources.Input,)
    request_id = proto.Field(proto.STRING, number=3,)


class CreateEventRequest(proto.Message):
    r"""Request message for "LivestreamService.CreateEvent".

    Attributes:
        parent (str):
            Required. The parent channel for the resource, in the form
            of:
            ``projects/{project}/locations/{location}/channels/{channelId}``.
        event (google.cloud.video.live_stream_v1.types.Event):
            Required. The event resource to be created.
        event_id (str):
            Required. The ID of the event resource to be created. This
            value must be 1-63 characters, begin and end with
            ``[a-z0-9]``, could contain dashes (-) in between.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    event = proto.Field(proto.MESSAGE, number=2, message=resources.Event,)
    event_id = proto.Field(proto.STRING, number=3,)
    request_id = proto.Field(proto.STRING, number=4,)


class ListEventsRequest(proto.Message):
    r"""Request message for "LivestreamService.ListEvents".

    Attributes:
        parent (str):
            Required. The parent channel for the resource, in the form
            of:
            ``projects/{project}/locations/{location}/channels/{channelId}``.
        page_size (int):
            The maximum number of items to return. If unspecified,
            server will pick an appropriate default. Server may return
            fewer items than requested. A caller should only rely on
            response's
            [next_page_token][google.cloud.video.livestream.v1.ListEventsResponse.next_page_token]
            to determine if there are more items left to be queried.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
        filter (str):
            The filter to apply to list results.
        order_by (str):
            Specifies the ordering of results following syntax at
            https://cloud.google.com/apis/design/design_patterns#sorting_order.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListEventsResponse(proto.Message):
    r"""Response message for "LivestreamService.ListEvents".

    Attributes:
        events (Sequence[google.cloud.video.live_stream_v1.types.Event]):
            A list of events.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    events = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.Event,)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetEventRequest(proto.Message):
    r"""Request message for "LivestreamService.GetEvent".

    Attributes:
        name (str):
            Required. The name of the event resource, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}/events/{eventId}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteEventRequest(proto.Message):
    r"""Request message for "LivestreamService.DeleteEvent".

    Attributes:
        name (str):
            Required. The name of the event resource, in the form of:
            ``projects/{project}/locations/{location}/channels/{channelId}/events/{eventId}``.
        request_id (str):
            A request ID to identify requests. Specify a unique request
            ID so that if you must retry your request, the server will
            know to ignore the request if it has already been completed.
            The server will guarantee that for at least 60 minutes since
            the first request.

            For example, consider a situation where you make an initial
            request and the request times out. If you make the request
            again with the same request ID, the server can check if
            original operation with the same request ID was received,
            and if so, will ignore the second request. This prevents
            clients from accidentally creating duplicate commitments.

            The request ID must be a valid UUID with the exception that
            zero UUID is not supported
            ``(00000000-0000-0000-0000-000000000000)``.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class ChannelOperationResponse(proto.Message):
    r"""Response message for Start/Stop Channel long-running
    operations.

    """


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
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    target = proto.Field(proto.STRING, number=3,)
    verb = proto.Field(proto.STRING, number=4,)
    requested_cancellation = proto.Field(proto.BOOL, number=5,)
    api_version = proto.Field(proto.STRING, number=6,)


__all__ = tuple(sorted(__protobuf__.manifest))
