# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
        'OperationMetadata',
    },
)


class GetTriggerRequest(proto.Message):
    r"""The request message for the GetTrigger method.

    Attributes:
        name (str):
            Required. The name of the trigger to get.
    """

    name = proto.Field(
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
            each page. Note: The service may send fewer.
        page_token (str):
            The page token; provide the value from the
            ``next_page_token`` field in a previous ``ListTriggers``
            call to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListTriggers`` must match the call that provided the page
            token.
        order_by (str):
            The sorting order of the resources returned. Value should be
            a comma separated list of fields. The default sorting oder
            is ascending. To specify descending order for a field,
            append a ``desc`` suffix; for example:
            ``name desc, trigger_id``.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    order_by = proto.Field(
        proto.STRING,
        number=4,
    )


class ListTriggersResponse(proto.Message):
    r"""The response message for the ListTriggers method.

    Attributes:
        triggers (Sequence[google.cloud.eventarc_v1.types.Trigger]):
            The requested triggers, up to the number specified in
            ``page_size``.
        next_page_token (str):
            A page token that can be sent to ListTriggers
            to request the next page. If this is empty, then
            there are no more pages.
        unreachable (Sequence[str]):
            Unreachable resources, if any.
    """

    @property
    def raw_page(self):
        return self

    triggers = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gce_trigger.Trigger,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
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
            preview the review, but do not actually post it.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    trigger = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gce_trigger.Trigger,
    )
    trigger_id = proto.Field(
        proto.STRING,
        number=3,
    )
    validate_only = proto.Field(
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
            will be updated. If no field mask is provided, all provided
            fields in the request will be updated. To update all fields,
            provide a field mask of "*".
        allow_missing (bool):
            If set to true, and the trigger is not found, a new trigger
            will be created. In this situation, ``update_mask`` is
            ignored.
        validate_only (bool):
            Required. If set, validate the request and
            preview the review, but do not actually post it.
    """

    trigger = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gce_trigger.Trigger,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only = proto.Field(
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
            preview the review, but do not actually post it.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    etag = proto.Field(
        proto.STRING,
        number=2,
    )
    allow_missing = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=4,
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

    create_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target = proto.Field(
        proto.STRING,
        number=3,
    )
    verb = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
