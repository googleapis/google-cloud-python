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

import proto  # type: ignore

from google.cloud.eventarc_v1.types import channel as gce_channel
from google.cloud.eventarc_v1.types import channel_connection as gce_channel_connection
from google.cloud.eventarc_v1.types import discovery
from google.cloud.eventarc_v1.types import google_channel_config as gce_google_channel_config
from google.cloud.eventarc_v1.types import trigger as gce_trigger
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.eventarc.v1',
    manifest={
        'GetTriggerRequest',
        'ListTriggersRequest',
        'ListTriggersResponse',
        'CreateTriggerRequest',
        'UpdateTriggerRequest',
        'DeleteTriggerRequest',
        'GetChannelRequest',
        'ListChannelsRequest',
        'ListChannelsResponse',
        'CreateChannelRequest',
        'UpdateChannelRequest',
        'DeleteChannelRequest',
        'GetProviderRequest',
        'ListProvidersRequest',
        'ListProvidersResponse',
        'GetChannelConnectionRequest',
        'ListChannelConnectionsRequest',
        'ListChannelConnectionsResponse',
        'CreateChannelConnectionRequest',
        'DeleteChannelConnectionRequest',
        'UpdateGoogleChannelConfigRequest',
        'GetGoogleChannelConfigRequest',
        'OperationMetadata',
    },
)


class GetTriggerRequest(proto.Message):
    r"""The request message for the GetTrigger method.

    Attributes:
        name (str):
            Required. The name of the trigger to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListTriggersRequest(proto.Message):
    r"""The request message for the ListTriggers method.

    Attributes:
        parent (str):
            Required. The parent collection to list
            triggers on.
        page_size (int):
            The maximum number of triggers to return on
            each page.
            Note: The service may send fewer.
        page_token (str):
            The page token; provide the value from the
            ``next_page_token`` field in a previous ``ListTriggers``
            call to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListTriggers`` must match the call that provided the page
            token.
        order_by (str):
            The sorting order of the resources returned. Value should be
            a comma-separated list of fields. The default sorting order
            is ascending. To specify descending order for a field,
            append a ``desc`` suffix; for example:
            ``name desc, trigger_id``.
        filter (str):
            Filter field. Used to filter the Triggers to
            be listed. Possible filters are described in
            https://google.aip.dev/160. For example, using
            "?filter=destination:gke" would list only
            Triggers with a gke destination.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=4,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListTriggersResponse(proto.Message):
    r"""The response message for the ``ListTriggers`` method.

    Attributes:
        triggers (MutableSequence[google.cloud.eventarc_v1.types.Trigger]):
            The requested triggers, up to the number specified in
            ``page_size``.
        next_page_token (str):
            A page token that can be sent to ``ListTriggers`` to request
            the next page. If this is empty, then there are no more
            pages.
        unreachable (MutableSequence[str]):
            Unreachable resources, if any.
    """

    @property
    def raw_page(self):
        return self

    triggers: MutableSequence[gce_trigger.Trigger] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gce_trigger.Trigger,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateTriggerRequest(proto.Message):
    r"""The request message for the CreateTrigger method.

    Attributes:
        parent (str):
            Required. The parent collection in which to
            add this trigger.
        trigger (google.cloud.eventarc_v1.types.Trigger):
            Required. The trigger to create.
        trigger_id (str):
            Required. The user-provided ID to be assigned
            to the trigger.
        validate_only (bool):
            Required. If set, validate the request and
            preview the review, but do not post it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    trigger: gce_trigger.Trigger = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gce_trigger.Trigger,
    )
    trigger_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateTriggerRequest(proto.Message):
    r"""The request message for the UpdateTrigger method.

    Attributes:
        trigger (google.cloud.eventarc_v1.types.Trigger):
            The trigger to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields to be updated; only fields explicitly provided
            are updated. If no field mask is provided, all provided
            fields in the request are updated. To update all fields,
            provide a field mask of "*".
        allow_missing (bool):
            If set to true, and the trigger is not found, a new trigger
            will be created. In this situation, ``update_mask`` is
            ignored.
        validate_only (bool):
            Required. If set, validate the request and
            preview the review, but do not post it.
    """

    trigger: gce_trigger.Trigger = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gce_trigger.Trigger,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class DeleteTriggerRequest(proto.Message):
    r"""The request message for the DeleteTrigger method.

    Attributes:
        name (str):
            Required. The name of the trigger to be
            deleted.
        etag (str):
            If provided, the trigger will only be deleted
            if the etag matches the current etag on the
            resource.
        allow_missing (bool):
            If set to true, and the trigger is not found,
            the request will succeed but no action will be
            taken on the server.
        validate_only (bool):
            Required. If set, validate the request and
            preview the review, but do not post it.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class GetChannelRequest(proto.Message):
    r"""The request message for the GetChannel method.

    Attributes:
        name (str):
            Required. The name of the channel to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListChannelsRequest(proto.Message):
    r"""The request message for the ListChannels method.

    Attributes:
        parent (str):
            Required. The parent collection to list
            channels on.
        page_size (int):
            The maximum number of channels to return on
            each page.
            Note: The service may send fewer.
        page_token (str):
            The page token; provide the value from the
            ``next_page_token`` field in a previous ``ListChannels``
            call to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListChannels`` must match the call that provided the page
            token.
        order_by (str):
            The sorting order of the resources returned. Value should be
            a comma-separated list of fields. The default sorting order
            is ascending. To specify descending order for a field,
            append a ``desc`` suffix; for example:
            ``name desc, channel_id``.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListChannelsResponse(proto.Message):
    r"""The response message for the ``ListChannels`` method.

    Attributes:
        channels (MutableSequence[google.cloud.eventarc_v1.types.Channel]):
            The requested channels, up to the number specified in
            ``page_size``.
        next_page_token (str):
            A page token that can be sent to ``ListChannels`` to request
            the next page. If this is empty, then there are no more
            pages.
        unreachable (MutableSequence[str]):
            Unreachable resources, if any.
    """

    @property
    def raw_page(self):
        return self

    channels: MutableSequence[gce_channel.Channel] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gce_channel.Channel,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateChannelRequest(proto.Message):
    r"""The request message for the CreateChannel method.

    Attributes:
        parent (str):
            Required. The parent collection in which to
            add this channel.
        channel (google.cloud.eventarc_v1.types.Channel):
            Required. The channel to create.
        channel_id (str):
            Required. The user-provided ID to be assigned
            to the channel.
        validate_only (bool):
            Required. If set, validate the request and
            preview the review, but do not post it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    channel: gce_channel.Channel = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gce_channel.Channel,
    )
    channel_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class UpdateChannelRequest(proto.Message):
    r"""The request message for the UpdateChannel method.

    Attributes:
        channel (google.cloud.eventarc_v1.types.Channel):
            The channel to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields to be updated; only fields explicitly provided
            are updated. If no field mask is provided, all provided
            fields in the request are updated. To update all fields,
            provide a field mask of "*".
        validate_only (bool):
            Required. If set, validate the request and
            preview the review, but do not post it.
    """

    channel: gce_channel.Channel = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gce_channel.Channel,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteChannelRequest(proto.Message):
    r"""The request message for the DeleteChannel method.

    Attributes:
        name (str):
            Required. The name of the channel to be
            deleted.
        validate_only (bool):
            Required. If set, validate the request and
            preview the review, but do not post it.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class GetProviderRequest(proto.Message):
    r"""The request message for the GetProvider method.

    Attributes:
        name (str):
            Required. The name of the provider to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListProvidersRequest(proto.Message):
    r"""The request message for the ListProviders method.

    Attributes:
        parent (str):
            Required. The parent of the provider to get.
        page_size (int):
            The maximum number of providers to return on
            each page.
        page_token (str):
            The page token; provide the value from the
            ``next_page_token`` field in a previous ``ListProviders``
            call to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListProviders`` must match the call that provided the page
            token.
        order_by (str):
            The sorting order of the resources returned. Value should be
            a comma-separated list of fields. The default sorting oder
            is ascending. To specify descending order for a field,
            append a ``desc`` suffix; for example: ``name desc, _id``.
        filter (str):
            The filter field that the list request will
            filter on.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=4,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListProvidersResponse(proto.Message):
    r"""The response message for the ``ListProviders`` method.

    Attributes:
        providers (MutableSequence[google.cloud.eventarc_v1.types.Provider]):
            The requested providers, up to the number specified in
            ``page_size``.
        next_page_token (str):
            A page token that can be sent to ``ListProviders`` to
            request the next page. If this is empty, then there are no
            more pages.
        unreachable (MutableSequence[str]):
            Unreachable resources, if any.
    """

    @property
    def raw_page(self):
        return self

    providers: MutableSequence[discovery.Provider] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=discovery.Provider,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetChannelConnectionRequest(proto.Message):
    r"""The request message for the GetChannelConnection method.

    Attributes:
        name (str):
            Required. The name of the channel connection
            to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListChannelConnectionsRequest(proto.Message):
    r"""The request message for the ListChannelConnections method.

    Attributes:
        parent (str):
            Required. The parent collection from which to
            list channel connections.
        page_size (int):
            The maximum number of channel connections to
            return on each page.
            Note: The service may send fewer responses.
        page_token (str):
            The page token; provide the value from the
            ``next_page_token`` field in a previous
            ``ListChannelConnections`` call to retrieve the subsequent
            page.

            When paginating, all other parameters provided to
            ``ListChannelConnetions`` match the call that provided the
            page token.
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


class ListChannelConnectionsResponse(proto.Message):
    r"""The response message for the ``ListChannelConnections`` method.

    Attributes:
        channel_connections (MutableSequence[google.cloud.eventarc_v1.types.ChannelConnection]):
            The requested channel connections, up to the number
            specified in ``page_size``.
        next_page_token (str):
            A page token that can be sent to ``ListChannelConnections``
            to request the next page. If this is empty, then there are
            no more pages.
        unreachable (MutableSequence[str]):
            Unreachable resources, if any.
    """

    @property
    def raw_page(self):
        return self

    channel_connections: MutableSequence[gce_channel_connection.ChannelConnection] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gce_channel_connection.ChannelConnection,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class CreateChannelConnectionRequest(proto.Message):
    r"""The request message for the CreateChannelConnection method.

    Attributes:
        parent (str):
            Required. The parent collection in which to
            add this channel connection.
        channel_connection (google.cloud.eventarc_v1.types.ChannelConnection):
            Required. Channel connection to create.
        channel_connection_id (str):
            Required. The user-provided ID to be assigned
            to the channel connection.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    channel_connection: gce_channel_connection.ChannelConnection = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gce_channel_connection.ChannelConnection,
    )
    channel_connection_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteChannelConnectionRequest(proto.Message):
    r"""The request message for the DeleteChannelConnection method.

    Attributes:
        name (str):
            Required. The name of the channel connection
            to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateGoogleChannelConfigRequest(proto.Message):
    r"""The request message for the UpdateGoogleChannelConfig method.

    Attributes:
        google_channel_config (google.cloud.eventarc_v1.types.GoogleChannelConfig):
            Required. The config to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields to be updated; only fields explicitly provided
            are updated. If no field mask is provided, all provided
            fields in the request are updated. To update all fields,
            provide a field mask of "*".
    """

    google_channel_config: gce_google_channel_config.GoogleChannelConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gce_google_channel_config.GoogleChannelConfig,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetGoogleChannelConfigRequest(proto.Message):
    r"""The request message for the GetGoogleChannelConfig method.

    Attributes:
        name (str):
            Required. The name of the config to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
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
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
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
