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
    package="google.cloud.kms.inventory.v1",
    manifest={
        "GetProtectedResourcesSummaryRequest",
        "ProtectedResourcesSummary",
        "SearchProtectedResourcesRequest",
        "SearchProtectedResourcesResponse",
        "ProtectedResource",
    },
)


class GetProtectedResourcesSummaryRequest(proto.Message):
    r"""Request message for
    [KeyTrackingService.GetProtectedResourcesSummary][google.cloud.kms.inventory.v1.KeyTrackingService.GetProtectedResourcesSummary].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKey][google.cloud.kms.v1.CryptoKey].
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ProtectedResourcesSummary(proto.Message):
    r"""Aggregate information about the resources protected by a
    Cloud KMS key in the same Cloud organization as the key.

    Attributes:
        name (str):
            The full name of the
            ProtectedResourcesSummary resource. Example:

            projects/test-project/locations/us/keyRings/test-keyring/cryptoKeys/test-key/protectedResourcesSummary
        resource_count (int):
            The total number of protected resources in
            the same Cloud organization as the key.
        project_count (int):
            The number of distinct Cloud projects in the
            same Cloud organization as the key that have
            resources protected by the key.
        resource_types (MutableMapping[str, int]):
            The number of resources protected by the key
            grouped by resource type.
        cloud_products (MutableMapping[str, int]):
            The number of resources protected by the key
            grouped by Cloud product.
        locations (MutableMapping[str, int]):
            The number of resources protected by the key
            grouped by region.
    """

    name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    resource_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    project_count: int = proto.Field(
        proto.INT32,
        number=2,
    )
    resource_types: MutableMapping[str, int] = proto.MapField(
        proto.STRING,
        proto.INT64,
        number=3,
    )
    cloud_products: MutableMapping[str, int] = proto.MapField(
        proto.STRING,
        proto.INT64,
        number=6,
    )
    locations: MutableMapping[str, int] = proto.MapField(
        proto.STRING,
        proto.INT64,
        number=4,
    )


class SearchProtectedResourcesRequest(proto.Message):
    r"""Request message for
    [KeyTrackingService.SearchProtectedResources][google.cloud.kms.inventory.v1.KeyTrackingService.SearchProtectedResources].

    Attributes:
        scope (str):
            Required. Resource name of the organization.
            Example: organizations/123
        crypto_key (str):
            Required. The resource name of the
            [CryptoKey][google.cloud.kms.v1.CryptoKey].
        page_size (int):
            The maximum number of resources to return.
            The service may return fewer than this value. If
            unspecified, at most 500 resources will be
            returned. The maximum value is 500; values above
            500 will be coerced to 500.
        page_token (str):
            A page token, received from a previous
            [KeyTrackingService.SearchProtectedResources][google.cloud.kms.inventory.v1.KeyTrackingService.SearchProtectedResources]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [KeyTrackingService.SearchProtectedResources][google.cloud.kms.inventory.v1.KeyTrackingService.SearchProtectedResources]
            must match the call that provided the page token.
        resource_types (MutableSequence[str]):
            Optional. A list of resource types that this request
            searches for. If empty, it will search all the `trackable
            resource
            types <https://cloud.google.com/kms/docs/view-key-usage#tracked-resource-types>`__.

            Regular expressions are also supported. For example:

            -  ``compute.googleapis.com.*`` snapshots resources whose
               type starts with ``compute.googleapis.com``.
            -  ``.*Image`` snapshots resources whose type ends with
               ``Image``.
            -  ``.*Image.*`` snapshots resources whose type contains
               ``Image``.

            See `RE2 <https://github.com/google/re2/wiki/Syntax>`__ for
            all supported regular expression syntax. If the regular
            expression does not match any supported resource type, an
            INVALID_ARGUMENT error will be returned.
    """

    scope: str = proto.Field(
        proto.STRING,
        number=2,
    )
    crypto_key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )
    resource_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )


class SearchProtectedResourcesResponse(proto.Message):
    r"""Response message for
    [KeyTrackingService.SearchProtectedResources][google.cloud.kms.inventory.v1.KeyTrackingService.SearchProtectedResources].

    Attributes:
        protected_resources (MutableSequence[google.cloud.kms_inventory_v1.types.ProtectedResource]):
            Protected resources for this page.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    protected_resources: MutableSequence["ProtectedResource"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ProtectedResource",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ProtectedResource(proto.Message):
    r"""Metadata about a resource protected by a Cloud KMS key.

    Attributes:
        name (str):
            The full resource name of the resource. Example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
        project (str):
            Format: ``projects/{PROJECT_NUMBER}``.
        project_id (str):
            The ID of the project that owns the resource.
        cloud_product (str):
            The Cloud product that owns the resource. Example:
            ``compute``
        resource_type (str):
            Example: ``compute.googleapis.com/Disk``
        location (str):
            Location can be ``global``, regional like ``us-east1``, or
            zonal like ``us-west1-b``.
        labels (MutableMapping[str, str]):
            A key-value pair of the resource's labels
            (v1) to their values.
        crypto_key_version (str):
            The name of the Cloud KMS
            `CryptoKeyVersion <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions?hl=en>`__
            used to protect this resource via CMEK. This field is empty
            if the Google Cloud product owning the resource does not
            provide key version data to Asset Inventory. If there are
            multiple key versions protecting the resource, then this is
            same value as the first element of crypto_key_versions.
        crypto_key_versions (MutableSequence[str]):
            The names of the Cloud KMS
            `CryptoKeyVersion <https://cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions?hl=en>`__
            used to protect this resource via CMEK. This field is empty
            if the Google Cloud product owning the resource does not
            provide key versions data to Asset Inventory. The first
            element of this field is stored in crypto_key_version.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this resource
            was created. The granularity is in seconds.
            Timestamp.nanos will always be 0.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    project: str = proto.Field(
        proto.STRING,
        number=2,
    )
    project_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    cloud_product: str = proto.Field(
        proto.STRING,
        number=8,
    )
    resource_type: str = proto.Field(
        proto.STRING,
        number=3,
    )
    location: str = proto.Field(
        proto.STRING,
        number=4,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    crypto_key_version: str = proto.Field(
        proto.STRING,
        number=6,
    )
    crypto_key_versions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
