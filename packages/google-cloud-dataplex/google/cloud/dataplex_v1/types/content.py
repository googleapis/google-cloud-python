# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import proto  # type: ignore

from google.cloud.dataplex_v1.types import analyze

__protobuf__ = proto.module(
    package="google.cloud.dataplex.v1",
    manifest={
        "CreateContentRequest",
        "UpdateContentRequest",
        "DeleteContentRequest",
        "ListContentRequest",
        "ListContentResponse",
        "GetContentRequest",
    },
)


class CreateContentRequest(proto.Message):
    r"""Create content request.

    Attributes:
        parent (str):
            Required. The resource name of the parent lake:
            projects/{project_id}/locations/{location_id}/lakes/{lake_id}
        content (google.cloud.dataplex_v1.types.Content):
            Required. Content resource.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    content: analyze.Content = proto.Field(
        proto.MESSAGE,
        number=2,
        message=analyze.Content,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class UpdateContentRequest(proto.Message):
    r"""Update content request.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields to update.
        content (google.cloud.dataplex_v1.types.Content):
            Required. Update description. Only fields specified in
            ``update_mask`` are updated.
        validate_only (bool):
            Optional. Only validate the request, but do
            not perform mutations. The default is false.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    content: analyze.Content = proto.Field(
        proto.MESSAGE,
        number=2,
        message=analyze.Content,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteContentRequest(proto.Message):
    r"""Delete content request.

    Attributes:
        name (str):
            Required. The resource name of the content:
            projects/{project_id}/locations/{location_id}/lakes/{lake_id}/content/{content_id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListContentRequest(proto.Message):
    r"""List content request. Returns the BASIC Content view.

    Attributes:
        parent (str):
            Required. The resource name of the parent lake:
            projects/{project_id}/locations/{location_id}/lakes/{lake_id}
        page_size (int):
            Optional. Maximum number of content to
            return. The service may return fewer than this
            value. If unspecified, at most 10 content will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. Page token received from a previous
            ``ListContent`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListContent`` must match the call that
            provided the page token.
        filter (str):
            Optional. Filter request. Filters are case-sensitive. The
            following formats are supported:

            labels.key1 = "value1" labels:key1 type = "NOTEBOOK" type =
            "SQL_SCRIPT"

            These restrictions can be coinjoined with AND, OR and NOT
            conjunctions.
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


class ListContentResponse(proto.Message):
    r"""List content response.

    Attributes:
        content (MutableSequence[google.cloud.dataplex_v1.types.Content]):
            Content under the given parent lake.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    content: MutableSequence[analyze.Content] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=analyze.Content,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetContentRequest(proto.Message):
    r"""Get content request.

    Attributes:
        name (str):
            Required. The resource name of the content:
            projects/{project_id}/locations/{location_id}/lakes/{lake_id}/content/{content_id}
        view (google.cloud.dataplex_v1.types.GetContentRequest.ContentView):
            Optional. Specify content view to make a
            partial request.
    """

    class ContentView(proto.Enum):
        r"""Specifies whether the request should return the full or the
        partial representation.

        Values:
            CONTENT_VIEW_UNSPECIFIED (0):
                Content view not specified. Defaults to
                BASIC. The API will default to the BASIC view.
            BASIC (1):
                Will not return the ``data_text`` field.
            FULL (2):
                Returns the complete proto.
        """
        CONTENT_VIEW_UNSPECIFIED = 0
        BASIC = 1
        FULL = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: ContentView = proto.Field(
        proto.ENUM,
        number=2,
        enum=ContentView,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
