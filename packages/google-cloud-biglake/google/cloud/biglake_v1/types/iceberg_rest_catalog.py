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

import google.protobuf.field_mask_pb2 as field_mask_pb2  # type: ignore
import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.biglake.v1",
    manifest={
        "IcebergCatalog",
        "CreateIcebergCatalogRequest",
        "UpdateIcebergCatalogRequest",
        "GetIcebergCatalogRequest",
        "ListIcebergCatalogsRequest",
        "ListIcebergCatalogsResponse",
        "FailoverIcebergCatalogRequest",
        "FailoverIcebergCatalogResponse",
    },
)


class IcebergCatalog(proto.Message):
    r"""The Iceberg REST Catalog information.

    Attributes:
        name (str):
            Identifier. The catalog name,
            ``projects/my-project/catalogs/my-catalog``. This field is
            immutable. This field is ignored for CreateIcebergCatalog.
        credential_mode (google.cloud.biglake_v1.types.IcebergCatalog.CredentialMode):
            Optional. The credential mode for the
            catalog.
        biglake_service_account (str):
            Output only. The service account used for
            credential vending, output only. Might be empty
            if Credential vending was never enabled for the
            catalog.
        catalog_type (google.cloud.biglake_v1.types.IcebergCatalog.CatalogType):
            Required. The catalog type. Required for
            CreateIcebergCatalog.
        default_location (str):
            Optional. The default location for the
            catalog. For the Google Cloud Storage Bucket
            catalog this is output only.
        catalog_regions (MutableSequence[str]):
            Output only. The GCP region(s) where the
            catalog metadata is stored. This will contain
            one value for all locations, except for the
            catalogs that are configured to use custom dual
            region buckets.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the catalog was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the catalog was last
            updated.
    """

    class CatalogType(proto.Enum):
        r"""Determines the catalog type.

        Values:
            CATALOG_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            CATALOG_TYPE_GCS_BUCKET (1):
                Catalog type for Google Cloud Storage
                Buckets.
        """

        CATALOG_TYPE_UNSPECIFIED = 0
        CATALOG_TYPE_GCS_BUCKET = 1

    class CredentialMode(proto.Enum):
        r"""The credential mode used for the catalog.

        Values:
            CREDENTIAL_MODE_UNSPECIFIED (0):
                Default value. This value is unused.
            CREDENTIAL_MODE_END_USER (1):
                End user credentials, default. The
                authenticating user must have access to the
                catalog resources and the corresponding Google
                Cloud Storage files.
            CREDENTIAL_MODE_VENDED_CREDENTIALS (2):
                Use credential vending. The authenticating user must have
                access to the catalog resources and the system will provide
                the caller with downscoped credentials to access the Google
                Cloud Storage files. All table operations in this mode would
                require ``X-Iceberg-Access-Delegation`` header with
                ``vended-credentials`` value included. System will generate
                a service account and the catalog administrator must grant
                the service account appropriate permissions.

                See:
                https://github.com/apache/iceberg/blob/931865ecaf40a827f9081dddb675bf1c95c05461/open-api/rest-catalog-open-api.yaml#L1854
                for more details.
        """

        CREDENTIAL_MODE_UNSPECIFIED = 0
        CREDENTIAL_MODE_END_USER = 1
        CREDENTIAL_MODE_VENDED_CREDENTIALS = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    credential_mode: CredentialMode = proto.Field(
        proto.ENUM,
        number=2,
        enum=CredentialMode,
    )
    biglake_service_account: str = proto.Field(
        proto.STRING,
        number=3,
    )
    catalog_type: CatalogType = proto.Field(
        proto.ENUM,
        number=4,
        enum=CatalogType,
    )
    default_location: str = proto.Field(
        proto.STRING,
        number=5,
    )
    catalog_regions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )


class CreateIcebergCatalogRequest(proto.Message):
    r"""The request message for the ``CreateIcebergCatalog`` API.

    Attributes:
        parent (str):
            Required. The parent resource where this catalog will be
            created. Format: projects/{project_id}
        iceberg_catalog_id (str):
            Required. The name of the catalog.
        iceberg_catalog (google.cloud.biglake_v1.types.IcebergCatalog):
            Required. The catalog to create. The required fields for
            creation are:

            - catalog_type. Optionally: credential_mode can be provided,
              if Credential Vending is desired.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    iceberg_catalog_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    iceberg_catalog: "IcebergCatalog" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="IcebergCatalog",
    )


class UpdateIcebergCatalogRequest(proto.Message):
    r"""The request message for the ``UpdateIcebergCatalog`` API.

    Attributes:
        iceberg_catalog (google.cloud.biglake_v1.types.IcebergCatalog):
            Required. The catalog to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The list of fields to update.
    """

    iceberg_catalog: "IcebergCatalog" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="IcebergCatalog",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetIcebergCatalogRequest(proto.Message):
    r"""The request message for the ``GetIcebergCatalog`` API.

    Attributes:
        name (str):
            Required. The catalog to get.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListIcebergCatalogsRequest(proto.Message):
    r"""The request message for the ``ListIcebergCatalogs`` API.

    Attributes:
        parent (str):
            Required. The parent resource where this catalog will be
            created. Format: projects/{project_id}
        view (google.cloud.biglake_v1.types.ListIcebergCatalogsRequest.CatalogView):
            Optional. The view of the catalog to return.
        page_size (int):
            Optional. The maximum number of catalogs to
            return. The service may return fewer than this
            value.
        page_token (str):
            Optional. The page token, received from a previous
            ``ListIcebergCatalogs`` call. Provide this to retrieve the
            subsequent page.
    """

    class CatalogView(proto.Enum):
        r"""The enumeration of the views that can be returned.

        Values:
            CATALOG_VIEW_UNSPECIFIED (0):
                Default/unset value. Same as BASIC.
            CATALOG_VIEW_BASIC (1):
                Include only the name and catalog type.
            CATALOG_VIEW_FULL (2):
                Include all fields of the catalog.
        """

        CATALOG_VIEW_UNSPECIFIED = 0
        CATALOG_VIEW_BASIC = 1
        CATALOG_VIEW_FULL = 2

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: CatalogView = proto.Field(
        proto.ENUM,
        number=2,
        enum=CatalogView,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListIcebergCatalogsResponse(proto.Message):
    r"""The response message for the ``ListIcebergCatalogs`` API.

    Attributes:
        iceberg_catalogs (MutableSequence[google.cloud.biglake_v1.types.IcebergCatalog]):
            Output only. The list of iceberg catalogs.
        next_page_token (str):
            Output only. The next page token for
            pagination.
        unreachable (MutableSequence[str]):
            Output only. The list of unreachable cloud
            regions for router fanout.
    """

    @property
    def raw_page(self):
        return self

    iceberg_catalogs: MutableSequence["IcebergCatalog"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="IcebergCatalog",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class FailoverIcebergCatalogRequest(proto.Message):
    r"""Request message for FailoverIcebergCatalog.

    Attributes:
        name (str):
            Required. The name of the catalog in the form
            "projects/{project_id}/catalogs/{catalog_id}".
        primary_replica (str):
            Required. The region being assigned as the
            new primary replica region. For example
            "us-east1". This must be one of the replica
            regions in the catalog's list of replicas marked
            as a "secondary".
        validate_only (bool):
            Optional. If set, only validate the request, but do not
            perform the update. This can be used to inspect the
            replication_time at any time, including before performing a
            fail-over.
        conditional_failover_replication_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. If unset, wait for all data from
            the source region to replicate to the new
            primary region before completing the failover,
            with no data loss (also called "soft failover").
            If set, failover immediately, accepting the loss
            of any data committed in the source region after
            this timestamp, that has not yet replicated. If
            any data committed before this time has not
            replicated, the failover will not be performed
            and an error will be returned (also called "hard
            failover").
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    primary_replica: str = proto.Field(
        proto.STRING,
        number=2,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    conditional_failover_replication_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class FailoverIcebergCatalogResponse(proto.Message):
    r"""Response message for FailoverIcebergCatalog.

    Attributes:
        replication_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The min timestamp for which all namespaces and
            table metadata have been replicated in the region specified
            as the new primary_replica. Some resources may have been
            replicated more recently than this timestamp. If empty, the
            replica has just been created and has not yet been fully
            initialized. NOTE: When the Cloud Storage replication
            watermark is available, this will represent both catalog
            metadata and Cloud Storage data.
    """

    replication_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
