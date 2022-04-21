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

__protobuf__ = proto.module(
    package="google.cloud.resourcemanager.v3",
    manifest={
        "TagBinding",
        "CreateTagBindingMetadata",
        "CreateTagBindingRequest",
        "DeleteTagBindingMetadata",
        "DeleteTagBindingRequest",
        "ListTagBindingsRequest",
        "ListTagBindingsResponse",
    },
)


class TagBinding(proto.Message):
    r"""A TagBinding represents a connection between a TagValue and a
    cloud resource (currently project, folder, or organization).
    Once a TagBinding is created, the TagValue is applied to all the
    descendants of the cloud resource.

    Attributes:
        name (str):
            Output only. The name of the TagBinding. This is a String of
            the form:
            ``tagBindings/{full-resource-name}/{tag-value-name}`` (e.g.
            ``tagBindings/%2F%2Fcloudresourcemanager.googleapis.com%2Fprojects%2F123/tagValues/456``).
        parent (str):
            The full resource name of the resource the TagValue is bound
            to. E.g.
            ``//cloudresourcemanager.googleapis.com/projects/123``
        tag_value (str):
            The TagValue of the TagBinding. Must be of the form
            ``tagValues/456``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    parent = proto.Field(
        proto.STRING,
        number=2,
    )
    tag_value = proto.Field(
        proto.STRING,
        number=3,
    )


class CreateTagBindingMetadata(proto.Message):
    r"""Runtime operation information for creating a TagValue."""


class CreateTagBindingRequest(proto.Message):
    r"""The request message to create a TagBinding.

    Attributes:
        tag_binding (google.cloud.resourcemanager_v3.types.TagBinding):
            Required. The TagBinding to be created.
        validate_only (bool):
            Optional. Set to true to perform the
            validations necessary for creating the resource,
            but not actually perform the action.
    """

    tag_binding = proto.Field(
        proto.MESSAGE,
        number=1,
        message="TagBinding",
    )
    validate_only = proto.Field(
        proto.BOOL,
        number=2,
    )


class DeleteTagBindingMetadata(proto.Message):
    r"""Runtime operation information for deleting a TagBinding."""


class DeleteTagBindingRequest(proto.Message):
    r"""The request message to delete a TagBinding.

    Attributes:
        name (str):
            Required. The name of the TagBinding. This is a String of
            the form: ``tagBindings/{id}`` (e.g.
            ``tagBindings/%2F%2Fcloudresourcemanager.googleapis.com%2Fprojects%2F123/tagValues/456``).
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListTagBindingsRequest(proto.Message):
    r"""The request message to list all TagBindings for a parent.

    Attributes:
        parent (str):
            Required. The full resource name of a
            resource for which you want to list existing
            TagBindings. E.g.
            "//cloudresourcemanager.googleapis.com/projects/123".
        page_size (int):
            Optional. The maximum number of TagBindings
            to return in the response. The server allows a
            maximum of 300 TagBindings to return. If
            unspecified, the server will use 100 as the
            default.
        page_token (str):
            Optional. A pagination token returned from a previous call
            to ``ListTagBindings`` that indicates where this listing
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


class ListTagBindingsResponse(proto.Message):
    r"""The ListTagBindings response.

    Attributes:
        tag_bindings (Sequence[google.cloud.resourcemanager_v3.types.TagBinding]):
            A possibly paginated list of TagBindings for
            the specified TagValue or resource.
        next_page_token (str):
            Pagination token.

            If the result set is too large to fit in a single response,
            this token is returned. It encodes the position of the
            current result cursor. Feeding this value into a new list
            request with the ``page_token`` parameter gives the next
            page of the results.

            When ``next_page_token`` is not filled in, there is no next
            page and the list returned is the last page in the result
            set.

            Pagination tokens have a limited lifetime.
    """

    @property
    def raw_page(self):
        return self

    tag_bindings = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TagBinding",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
