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
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.resourcemanager.v3",
    manifest={
        "TagValue",
        "ListTagValuesRequest",
        "ListTagValuesResponse",
        "GetTagValueRequest",
        "CreateTagValueRequest",
        "CreateTagValueMetadata",
        "UpdateTagValueRequest",
        "UpdateTagValueMetadata",
        "DeleteTagValueRequest",
        "DeleteTagValueMetadata",
    },
)


class TagValue(proto.Message):
    r"""A TagValue is a child of a particular TagKey. This is used to
    group cloud resources for the purpose of controlling them using
    policies.

    Attributes:
        name (str):
            Immutable. Resource name for TagValue in the format
            ``tagValues/456``.
        parent (str):
            Immutable. The resource name of the new TagValue's parent
            TagKey. Must be of the form ``tagKeys/{tag_key_id}``.
        short_name (str):
            Required. Immutable. User-assigned short name for TagValue.
            The short name should be unique for TagValues within the
            same parent TagKey.

            The short name must be 63 characters or less, beginning and
            ending with an alphanumeric character ([a-z0-9A-Z]) with
            dashes (-), underscores (_), dots (.), and alphanumerics
            between.
        namespaced_name (str):
            Output only. Namespaced name of the TagValue. Must be in the
            format
            ``{organization_id}/{tag_key_short_name}/{short_name}``.
        description (str):
            Optional. User-assigned description of the
            TagValue. Must not exceed 256 characters.

            Read-write.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Update time.
        etag (str):
            Optional. Entity tag which users can pass to
            prevent race conditions. This field is always
            set in server responses. See
            UpdateTagValueRequest for details.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    parent = proto.Field(
        proto.STRING,
        number=2,
    )
    short_name = proto.Field(
        proto.STRING,
        number=3,
    )
    namespaced_name = proto.Field(
        proto.STRING,
        number=4,
    )
    description = proto.Field(
        proto.STRING,
        number=5,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    etag = proto.Field(
        proto.STRING,
        number=8,
    )


class ListTagValuesRequest(proto.Message):
    r"""The request message for listing TagValues for the specified
    TagKey.

    Attributes:
        parent (str):
            Required. Resource name for TagKey, parent of the TagValues
            to be listed, in the format ``tagKeys/123``.
        page_size (int):
            Optional. The maximum number of TagValues to
            return in the response. The server allows a
            maximum of 300 TagValues to return. If
            unspecified, the server will use 100 as the
            default.
        page_token (str):
            Optional. A pagination token returned from a previous call
            to ``ListTagValues`` that indicates where this listing
            should continue from.
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


class ListTagValuesResponse(proto.Message):
    r"""The ListTagValues response.

    Attributes:
        tag_values (Sequence[google.cloud.resourcemanager_v3.types.TagValue]):
            A possibly paginated list of TagValues that
            are direct descendants of the specified parent
            TagKey.
        next_page_token (str):
            A pagination token returned from a previous call to
            ``ListTagValues`` that indicates from where listing should
            continue. This is currently not used, but the server may at
            any point start supplying a valid token.
    """

    @property
    def raw_page(self):
        return self

    tag_values = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TagValue",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetTagValueRequest(proto.Message):
    r"""The request message for getting a TagValue.

    Attributes:
        name (str):
            Required. Resource name for TagValue to be fetched in the
            format ``tagValues/456``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateTagValueRequest(proto.Message):
    r"""The request message for creating a TagValue.

    Attributes:
        tag_value (google.cloud.resourcemanager_v3.types.TagValue):
            Required. The TagValue to be created. Only fields
            ``short_name``, ``description``, and ``parent`` are
            considered during the creation request.
        validate_only (bool):
            Optional. Set as true to perform the
            validations necessary for creating the resource,
            but not actually perform the action.
    """

    tag_value = proto.Field(
        proto.MESSAGE,
        number=1,
        message="TagValue",
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=2,
    )


class CreateTagValueMetadata(proto.Message):
    r"""Runtime operation information for creating a TagValue."""


class UpdateTagValueRequest(proto.Message):
    r"""The request message for updating a TagValue.

    Attributes:
        tag_value (google.cloud.resourcemanager_v3.types.TagValue):
            Required. The new definition of the TagValue. Only fields
            ``description`` and ``etag`` fields can be updated by this
            request. If the ``etag`` field is nonempty, it must match
            the ``etag`` field of the existing ControlGroup. Otherwise,
            ``FAILED_PRECONDITION`` will be returned.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Fields to be updated.
        validate_only (bool):
            Optional. True to perform validations
            necessary for updating the resource, but not
            actually perform the action.
    """

    tag_value = proto.Field(
        proto.MESSAGE,
        number=1,
        message="TagValue",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=3,
    )


class UpdateTagValueMetadata(proto.Message):
    r"""Runtime operation information for updating a TagValue."""


class DeleteTagValueRequest(proto.Message):
    r"""The request message for deleting a TagValue.

    Attributes:
        name (str):
            Required. Resource name for TagValue to be
            deleted in the format tagValues/456.
        validate_only (bool):
            Optional. Set as true to perform the
            validations necessary for deletion, but not
            actually perform the action.
        etag (str):
            Optional. The etag known to the client for
            the expected state of the TagValue. This is to
            be used for optimistic concurrency.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=2,
    )
    etag = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteTagValueMetadata(proto.Message):
    r"""Runtime operation information for deleting a TagValue."""


__all__ = tuple(sorted(__protobuf__.manifest))
