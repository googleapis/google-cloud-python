# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

import google.protobuf.field_mask_pb2 as field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import child_publisher_messages

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "GetChildPublisherRequest",
        "ListChildPublishersRequest",
        "ListChildPublishersResponse",
        "CreateChildPublisherRequest",
        "BatchCreateChildPublishersRequest",
        "BatchCreateChildPublishersResponse",
        "UpdateChildPublisherRequest",
        "BatchUpdateChildPublishersRequest",
        "BatchUpdateChildPublishersResponse",
    },
)


class GetChildPublisherRequest(proto.Message):
    r"""Request object for [GetChildPublisher][] method.

    Attributes:
        name (str):
            Required. The resource name of the
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher].
            Format:
            ``networks/{network_code}/childPublishers/{child_publisher_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListChildPublishersRequest(proto.Message):
    r"""Request object for [ListChildPublishers][] method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]s.
            Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]s to
            return. The service may return fewer than this value. If
            unspecified, at most 50
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]s
            will be returned. The maximum value is 1000; values greater
            than 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            [ListChildPublishers][] call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            [ListChildPublishers][] must match the call that provided
            the page token.
        filter (str):
            Optional. Expression to filter the response. See syntax
            details at
            https://developers.google.com/ad-manager/api/beta/filters

            **Filterable fields:**

            - ``accountStatus``
            - ``addressVerificationStatus``
            - ``approvalStatus``
            - ``approvedManageAccountRevenueShareMillipercent``
            - ``childNetwork``
            - ``delegationType``
            - ``displayName``
            - ``email``
            - ``identityVerificationStatus``
            - ``invitationStatus``
            - ``name``
            - ``parentRevenueShareMillipercent``
            - ``pendingOnboardingTasks``
            - ``readinessStatus``
            - ``sellerId``
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters#order
        skip (int):
            Optional. Number of individual resources to
            skip while paginating.
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
    skip: int = proto.Field(
        proto.INT32,
        number=6,
    )


class ListChildPublishersResponse(proto.Message):
    r"""Response object for [ListChildPublishers][] containing matching
    [ChildPublisher][google.ads.admanager.v1.ChildPublisher] objects.

    Attributes:
        child_publishers (MutableSequence[google.ads.admanager_v1.types.ChildPublisher]):
            The [ChildPublisher][google.ads.admanager.v1.ChildPublisher]
            objects from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]
            objects. If a filter was included in the request, this
            reflects the total number after the filtering is applied.

            ``total_size`` won't be calculated in the response unless it
            has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see
            https://developers.google.com/ad-manager/api/beta/field-masks
    """

    @property
    def raw_page(self):
        return self

    child_publishers: MutableSequence[child_publisher_messages.ChildPublisher] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=child_publisher_messages.ChildPublisher,
        )
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class CreateChildPublisherRequest(proto.Message):
    r"""Request object for [CreateChildPublisher][] method.

    Attributes:
        parent (str):
            Required. The parent resource where this
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]
            will be created. Format: ``networks/{network_code}``
        child_publisher (google.ads.admanager_v1.types.ChildPublisher):
            Required. The
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher] to
            create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    child_publisher: child_publisher_messages.ChildPublisher = proto.Field(
        proto.MESSAGE,
        number=2,
        message=child_publisher_messages.ChildPublisher,
    )


class BatchCreateChildPublishersRequest(proto.Message):
    r"""Request object for [BatchCreateChildPublishers][] method.

    Attributes:
        parent (str):
            Required. The parent resource where
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]s
            will be created. Format: ``networks/{network_code}`` The
            parent field in the CreateChildPublisherRequest must match
            this field.
        requests (MutableSequence[google.ads.admanager_v1.types.CreateChildPublisherRequest]):
            Required. The
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]
            objects to create. A maximum of 100 objects can be created
            in a batch.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    requests: MutableSequence["CreateChildPublisherRequest"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="CreateChildPublisherRequest",
    )


class BatchCreateChildPublishersResponse(proto.Message):
    r"""Response object for [BatchCreateChildPublishers][] method.

    Attributes:
        child_publishers (MutableSequence[google.ads.admanager_v1.types.ChildPublisher]):
            The [ChildPublisher][google.ads.admanager.v1.ChildPublisher]
            objects created.
    """

    child_publishers: MutableSequence[child_publisher_messages.ChildPublisher] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=child_publisher_messages.ChildPublisher,
        )
    )


class UpdateChildPublisherRequest(proto.Message):
    r"""Request object for [UpdateChildPublisher][] method.

    Attributes:
        child_publisher (google.ads.admanager_v1.types.ChildPublisher):
            Required. The
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher] to
            update.

            The
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]'s
            ``name`` is used to identify the
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher] to
            update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The list of fields to update.
    """

    child_publisher: child_publisher_messages.ChildPublisher = proto.Field(
        proto.MESSAGE,
        number=1,
        message=child_publisher_messages.ChildPublisher,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class BatchUpdateChildPublishersRequest(proto.Message):
    r"""Request object for [BatchUpdateChildPublishers][] method.

    Attributes:
        parent (str):
            Required. The parent resource where
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]s
            will be updated. Format: ``networks/{network_code}`` The
            parent field in the UpdateChildPublisherRequest must match
            this field.
        requests (MutableSequence[google.ads.admanager_v1.types.UpdateChildPublisherRequest]):
            Required. The
            [ChildPublisher][google.ads.admanager.v1.ChildPublisher]
            objects to update. A maximum of 100 objects can be updated
            in a batch.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    requests: MutableSequence["UpdateChildPublisherRequest"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="UpdateChildPublisherRequest",
    )


class BatchUpdateChildPublishersResponse(proto.Message):
    r"""Response object for [BatchUpdateChildPublishers][] method.

    Attributes:
        child_publishers (MutableSequence[google.ads.admanager_v1.types.ChildPublisher]):
            The [ChildPublisher][google.ads.admanager.v1.ChildPublisher]
            objects updated.
    """

    child_publishers: MutableSequence[child_publisher_messages.ChildPublisher] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=child_publisher_messages.ChildPublisher,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
