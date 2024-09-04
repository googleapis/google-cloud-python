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

import proto  # type: ignore

from google.cloud.discoveryengine_v1beta.types import sample_query_set as gcd_sample_query_set
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.discoveryengine.v1beta',
    manifest={
        'GetSampleQuerySetRequest',
        'ListSampleQuerySetsRequest',
        'ListSampleQuerySetsResponse',
        'CreateSampleQuerySetRequest',
        'UpdateSampleQuerySetRequest',
        'DeleteSampleQuerySetRequest',
    },
)


class GetSampleQuerySetRequest(proto.Message):
    r"""Request message for
    [SampleQuerySetService.GetSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.GetSampleQuerySet]
    method.

    Attributes:
        name (str):
            Required. Full resource name of
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet],
            such as
            ``projects/{project}/locations/{location}/sampleQuerySets/{sample_query_set}``.

            If the caller does not have permission to access the
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet],
            regardless of whether or not it exists, a PERMISSION_DENIED
            error is returned.

            If the requested
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]
            does not exist, a NOT_FOUND error is returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListSampleQuerySetsRequest(proto.Message):
    r"""Request message for
    [SampleQuerySetService.ListSampleQuerySets][google.cloud.discoveryengine.v1beta.SampleQuerySetService.ListSampleQuerySets]
    method.

    Attributes:
        parent (str):
            Required. The parent location resource name, such as
            ``projects/{project}/locations/{location}``.

            If the caller does not have permission to list
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]s
            under this location, regardless of whether or not this
            location exists, a ``PERMISSION_DENIED`` error is returned.
        page_size (int):
            Maximum number of
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]s
            to return. If unspecified, defaults to 100. The maximum
            allowed value is 1000. Values above 1000 will be coerced to
            1000.

            If this field is negative, an ``INVALID_ARGUMENT`` error is
            returned.
        page_token (str):
            A page token
            [ListSampleQuerySetsResponse.next_page_token][google.cloud.discoveryengine.v1beta.ListSampleQuerySetsResponse.next_page_token],
            received from a previous
            [SampleQuerySetService.ListSampleQuerySets][google.cloud.discoveryengine.v1beta.SampleQuerySetService.ListSampleQuerySets]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [SampleQuerySetService.ListSampleQuerySets][google.cloud.discoveryengine.v1beta.SampleQuerySetService.ListSampleQuerySets]
            must match the call that provided the page token. Otherwise,
            an ``INVALID_ARGUMENT`` error is returned.
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


class ListSampleQuerySetsResponse(proto.Message):
    r"""Response message for
    [SampleQuerySetService.ListSampleQuerySets][google.cloud.discoveryengine.v1beta.SampleQuerySetService.ListSampleQuerySets]
    method.

    Attributes:
        sample_query_sets (MutableSequence[google.cloud.discoveryengine_v1beta.types.SampleQuerySet]):
            The
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]s.
        next_page_token (str):
            A token that can be sent as
            [ListSampleQuerySetsRequest.page_token][google.cloud.discoveryengine.v1beta.ListSampleQuerySetsRequest.page_token]
            to retrieve the next page. If this field is omitted, there
            are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    sample_query_sets: MutableSequence[gcd_sample_query_set.SampleQuerySet] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcd_sample_query_set.SampleQuerySet,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateSampleQuerySetRequest(proto.Message):
    r"""Request message for
    [SampleQuerySetService.CreateSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.CreateSampleQuerySet]
    method.

    Attributes:
        parent (str):
            Required. The parent resource name, such as
            ``projects/{project}/locations/{location}``.
        sample_query_set (google.cloud.discoveryengine_v1beta.types.SampleQuerySet):
            Required. The
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]
            to create.
        sample_query_set_id (str):
            Required. The ID to use for the
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet],
            which will become the final component of the
            [SampleQuerySet.name][google.cloud.discoveryengine.v1beta.SampleQuerySet.name].

            If the caller does not have permission to create the
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet],
            regardless of whether or not it exists, a
            ``PERMISSION_DENIED`` error is returned.

            This field must be unique among all
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]s
            with the same
            [parent][google.cloud.discoveryengine.v1beta.CreateSampleQuerySetRequest.parent].
            Otherwise, an ``ALREADY_EXISTS`` error is returned.

            This field must conform to
            `RFC-1034 <https://tools.ietf.org/html/rfc1034>`__ standard
            with a length limit of 63 characters. Otherwise, an
            ``INVALID_ARGUMENT`` error is returned.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    sample_query_set: gcd_sample_query_set.SampleQuerySet = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcd_sample_query_set.SampleQuerySet,
    )
    sample_query_set_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateSampleQuerySetRequest(proto.Message):
    r"""Request message for
    [SampleQuerySetService.UpdateSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.UpdateSampleQuerySet]
    method.

    Attributes:
        sample_query_set (google.cloud.discoveryengine_v1beta.types.SampleQuerySet):
            Required. The sample query set to update.

            If the caller does not have permission to update the
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet],
            regardless of whether or not it exists, a
            ``PERMISSION_DENIED`` error is returned.

            If the
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]
            to update does not exist a ``NOT_FOUND`` error is returned.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            imported 'sample query set' to update. If not
            set, will by default update all fields.
    """

    sample_query_set: gcd_sample_query_set.SampleQuerySet = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_sample_query_set.SampleQuerySet,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteSampleQuerySetRequest(proto.Message):
    r"""Request message for
    [SampleQuerySetService.DeleteSampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySetService.DeleteSampleQuerySet]
    method.

    Attributes:
        name (str):
            Required. Full resource name of
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet],
            such as
            ``projects/{project}/locations/{location}/sampleQuerySets/{sample_query_set}``.

            If the caller does not have permission to delete the
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet],
            regardless of whether or not it exists, a
            ``PERMISSION_DENIED`` error is returned.

            If the
            [SampleQuerySet][google.cloud.discoveryengine.v1beta.SampleQuerySet]
            to delete does not exist, a ``NOT_FOUND`` error is returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
