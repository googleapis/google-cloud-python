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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import dayofweek_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.metastore.v1",
    manifest={
        "Service",
        "MaintenanceWindow",
        "HiveMetastoreConfig",
        "KerberosConfig",
        "Secret",
        "MetadataManagementActivity",
        "MetadataImport",
        "MetadataExport",
        "ListServicesRequest",
        "ListServicesResponse",
        "GetServiceRequest",
        "CreateServiceRequest",
        "UpdateServiceRequest",
        "DeleteServiceRequest",
        "ListMetadataImportsRequest",
        "ListMetadataImportsResponse",
        "GetMetadataImportRequest",
        "CreateMetadataImportRequest",
        "UpdateMetadataImportRequest",
        "ExportMetadataRequest",
        "OperationMetadata",
        "LocationMetadata",
        "DatabaseDumpSpec",
    },
)


class Service(proto.Message):
    r"""A managed metastore service that serves metadata queries.
    Attributes:
        hive_metastore_config (google.cloud.metastore_v1.types.HiveMetastoreConfig):
            Configuration information specific to running
            Hive metastore software as the metastore
            service.
        name (str):
            Immutable. The relative resource name of the metastore
            service, of the form:

            ``projects/{project_number}/locations/{location_id}/services/{service_id}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the metastore
            service was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the metastore
            service was last updated.
        labels (Sequence[google.cloud.metastore_v1.types.Service.LabelsEntry]):
            User-defined labels for the metastore
            service.
        network (str):
            Immutable. The relative resource name of the VPC network on
            which the instance can be accessed. It is specified in the
            following form:

            ``projects/{project_number}/global/networks/{network_id}``.
        endpoint_uri (str):
            Output only. The URI of the endpoint used to
            access the metastore service.
        port (int):
            The TCP port at which the metastore service
            is reached. Default: 9083.
        state (google.cloud.metastore_v1.types.Service.State):
            Output only. The current state of the
            metastore service.
        state_message (str):
            Output only. Additional information about the
            current state of the metastore service, if
            available.
        artifact_gcs_uri (str):
            Output only. A Cloud Storage URI (starting with ``gs://``)
            that specifies where artifacts related to the metastore
            service are stored.
        tier (google.cloud.metastore_v1.types.Service.Tier):
            The tier of the service.
        maintenance_window (google.cloud.metastore_v1.types.MaintenanceWindow):
            The one hour maintenance window of the
            metastore service. This specifies when the
            service can be restarted for maintenance
            purposes in UTC time.
        uid (str):
            Output only. The globally unique resource
            identifier of the metastore service.
        metadata_management_activity (google.cloud.metastore_v1.types.MetadataManagementActivity):
            Output only. The metadata management
            activities of the metastore service.
        release_channel (google.cloud.metastore_v1.types.Service.ReleaseChannel):
            Immutable. The release channel of the service. If
            unspecified, defaults to ``STABLE``.
    """

    class State(proto.Enum):
        r"""The current state of the metastore service."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        SUSPENDING = 3
        SUSPENDED = 4
        UPDATING = 5
        DELETING = 6
        ERROR = 7

    class Tier(proto.Enum):
        r"""Available service tiers."""
        TIER_UNSPECIFIED = 0
        DEVELOPER = 1
        ENTERPRISE = 3

    class ReleaseChannel(proto.Enum):
        r"""Release channels bundle features of varying levels of
        stability. Newer features may be introduced initially into less
        stable release channels and can be automatically promoted into
        more stable release channels.
        """
        RELEASE_CHANNEL_UNSPECIFIED = 0
        CANARY = 1
        STABLE = 2

    hive_metastore_config = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="metastore_config",
        message="HiveMetastoreConfig",
    )
    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=4,)
    network = proto.Field(proto.STRING, number=7,)
    endpoint_uri = proto.Field(proto.STRING, number=8,)
    port = proto.Field(proto.INT32, number=9,)
    state = proto.Field(proto.ENUM, number=10, enum=State,)
    state_message = proto.Field(proto.STRING, number=11,)
    artifact_gcs_uri = proto.Field(proto.STRING, number=12,)
    tier = proto.Field(proto.ENUM, number=13, enum=Tier,)
    maintenance_window = proto.Field(
        proto.MESSAGE, number=15, message="MaintenanceWindow",
    )
    uid = proto.Field(proto.STRING, number=16,)
    metadata_management_activity = proto.Field(
        proto.MESSAGE, number=17, message="MetadataManagementActivity",
    )
    release_channel = proto.Field(proto.ENUM, number=19, enum=ReleaseChannel,)


class MaintenanceWindow(proto.Message):
    r"""Maintenance window. This specifies when Dataproc Metastore
    may perform system maintenance operation to the service.

    Attributes:
        hour_of_day (google.protobuf.wrappers_pb2.Int32Value):
            The hour of day (0-23) when the window
            starts.
        day_of_week (google.type.dayofweek_pb2.DayOfWeek):
            The day of week, when the window starts.
    """

    hour_of_day = proto.Field(proto.MESSAGE, number=1, message=wrappers_pb2.Int32Value,)
    day_of_week = proto.Field(proto.ENUM, number=2, enum=dayofweek_pb2.DayOfWeek,)


class HiveMetastoreConfig(proto.Message):
    r"""Specifies configuration information specific to running Hive
    metastore software as the metastore service.

    Attributes:
        version (str):
            Immutable. The Hive metastore schema version.
        config_overrides (Sequence[google.cloud.metastore_v1.types.HiveMetastoreConfig.ConfigOverridesEntry]):
            A mapping of Hive metastore configuration key-value pairs to
            apply to the Hive metastore (configured in
            ``hive-site.xml``). The mappings override system defaults
            (some keys cannot be overridden).
        kerberos_config (google.cloud.metastore_v1.types.KerberosConfig):
            Information used to configure the Hive metastore service as
            a service principal in a Kerberos realm. To disable
            Kerberos, use the ``UpdateService`` method and specify this
            field's path (``hive_metastore_config.kerberos_config``) in
            the request's ``update_mask`` while omitting this field from
            the request's ``service``.
    """

    version = proto.Field(proto.STRING, number=1,)
    config_overrides = proto.MapField(proto.STRING, proto.STRING, number=2,)
    kerberos_config = proto.Field(proto.MESSAGE, number=3, message="KerberosConfig",)


class KerberosConfig(proto.Message):
    r"""Configuration information for a Kerberos principal.
    Attributes:
        keytab (google.cloud.metastore_v1.types.Secret):
            A Kerberos keytab file that can be used to
            authenticate a service principal with a Kerberos
            Key Distribution Center (KDC).
        principal (str):
            A Kerberos principal that exists in the both the keytab the
            KDC to authenticate as. A typical principal is of the form
            ``primary/instance@REALM``, but there is no exact format.
        krb5_config_gcs_uri (str):
            A Cloud Storage URI that specifies the path to a krb5.conf
            file. It is of the form
            ``gs://{bucket_name}/path/to/krb5.conf``, although the file
            does not need to be named krb5.conf explicitly.
    """

    keytab = proto.Field(proto.MESSAGE, number=1, message="Secret",)
    principal = proto.Field(proto.STRING, number=2,)
    krb5_config_gcs_uri = proto.Field(proto.STRING, number=3,)


class Secret(proto.Message):
    r"""A securely stored value.
    Attributes:
        cloud_secret (str):
            The relative resource name of a Secret Manager secret
            version, in the following form:

            ``projects/{project_number}/secrets/{secret_id}/versions/{version_id}``.
    """

    cloud_secret = proto.Field(proto.STRING, number=2, oneof="value",)


class MetadataManagementActivity(proto.Message):
    r"""The metadata management activities of the metastore service.
    Attributes:
        metadata_exports (Sequence[google.cloud.metastore_v1.types.MetadataExport]):
            Output only. The latest metadata exports of
            the metastore service.
    """

    metadata_exports = proto.RepeatedField(
        proto.MESSAGE, number=1, message="MetadataExport",
    )


class MetadataImport(proto.Message):
    r"""A metastore resource that imports metadata.
    Attributes:
        database_dump (google.cloud.metastore_v1.types.MetadataImport.DatabaseDump):
            Immutable. A database dump from a pre-
            xisting metastore's database.
        name (str):
            Immutable. The relative resource name of the metadata
            import, of the form:

            ``projects/{project_number}/locations/{location_id}/services/{service_id}/metadataImports/{metadata_import_id}``.
        description (str):
            The description of the metadata import.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the metadata
            import was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the metadata
            import was last updated.
        state (google.cloud.metastore_v1.types.MetadataImport.State):
            Output only. The current state of the
            metadata import.
    """

    class State(proto.Enum):
        r"""The current state of the metadata import."""
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        UPDATING = 3
        FAILED = 4

    class DatabaseDump(proto.Message):
        r"""A specification of the location of and metadata about a
        database dump from a relational database management system.

        Attributes:
            database_type (google.cloud.metastore_v1.types.MetadataImport.DatabaseDump.DatabaseType):
                The type of the database.
            gcs_uri (str):
                A Cloud Storage object or folder URI that specifies the
                source from which to import metadata. It must begin with
                ``gs://``.
            type_ (google.cloud.metastore_v1.types.DatabaseDumpSpec.Type):
                Optional. The type of the database dump. If unspecified,
                defaults to ``MYSQL``.
        """

        class DatabaseType(proto.Enum):
            r"""The type of the database."""
            DATABASE_TYPE_UNSPECIFIED = 0
            MYSQL = 1

        database_type = proto.Field(
            proto.ENUM, number=1, enum="MetadataImport.DatabaseDump.DatabaseType",
        )
        gcs_uri = proto.Field(proto.STRING, number=2,)
        type_ = proto.Field(proto.ENUM, number=4, enum="DatabaseDumpSpec.Type",)

    database_dump = proto.Field(
        proto.MESSAGE, number=6, oneof="metadata", message=DatabaseDump,
    )
    name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    state = proto.Field(proto.ENUM, number=5, enum=State,)


class MetadataExport(proto.Message):
    r"""The details of a metadata export operation.
    Attributes:
        destination_gcs_uri (str):
            Output only. A Cloud Storage URI of a folder that metadata
            are exported to, in the form of
            ``gs://<bucket_name>/<path_inside_bucket>/<export_folder>``,
            where ``<export_folder>`` is automatically generated.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the export
            started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the export ended.
        state (google.cloud.metastore_v1.types.MetadataExport.State):
            Output only. The current state of the export.
        database_dump_type (google.cloud.metastore_v1.types.DatabaseDumpSpec.Type):
            Output only. The type of the database dump.
    """

    class State(proto.Enum):
        r"""The current state of the metadata export."""
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLED = 4

    destination_gcs_uri = proto.Field(proto.STRING, number=4, oneof="destination",)
    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    state = proto.Field(proto.ENUM, number=3, enum=State,)
    database_dump_type = proto.Field(
        proto.ENUM, number=5, enum="DatabaseDumpSpec.Type",
    )


class ListServicesRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices].

    Attributes:
        parent (str):
            Required. The relative resource name of the location of
            metastore services to list, in the following form:

            ``projects/{project_number}/locations/{location_id}``.
        page_size (int):
            Optional. The maximum number of services to
            return. The response may contain less than the
            maximum number. If unspecified, no more than 500
            services are returned. The maximum value is
            1000; values above 1000 are changed to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices]
            call. Provide this token to retrieve the subsequent page.

            To retrieve the first page, supply an empty page token.

            When paginating, other parameters provided to
            [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices]
            must match the call that provided the page token.
        filter (str):
            Optional. The filter to apply to list
            results.
        order_by (str):
            Optional. Specify the ordering of results as described in
            `Sorting
            Order <https://cloud.google.com/apis/design/design_patterns#sorting_order>`__.
            If not specified, the results will be sorted in the default
            order.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListServicesResponse(proto.Message):
    r"""Response message for
    [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices].

    Attributes:
        services (Sequence[google.cloud.metastore_v1.types.Service]):
            The services in the specified location.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    services = proto.RepeatedField(proto.MESSAGE, number=1, message="Service",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetServiceRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.GetService][google.cloud.metastore.v1.DataprocMetastore.GetService].

    Attributes:
        name (str):
            Required. The relative resource name of the metastore
            service to retrieve, in the following form:

            ``projects/{project_number}/locations/{location_id}/services/{service_id}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateServiceRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.CreateService][google.cloud.metastore.v1.DataprocMetastore.CreateService].

    Attributes:
        parent (str):
            Required. The relative resource name of the location in
            which to create a metastore service, in the following form:

            ``projects/{project_number}/locations/{location_id}``.
        service_id (str):
            Required. The ID of the metastore service,
            which is used as the final component of the
            metastore service's name.
            This value must be between 2 and 63 characters
            long inclusive, begin with a letter, end with a
            letter or number, and consist of alpha-numeric
            ASCII characters or hyphens.
        service (google.cloud.metastore_v1.types.Service):
            Required. The Metastore service to create. The ``name``
            field is ignored. The ID of the created metastore service
            must be provided in the request's ``service_id`` field.
        request_id (str):
            Optional. A request ID. Specify a unique request ID to allow
            the server to ignore the request if it has completed. The
            server will ignore subsequent requests that provide a
            duplicate request ID for at least 60 minutes after the first
            request.

            For example, if an initial request times out, followed by
            another request with the same request ID, the server ignores
            the second request to prevent the creation of duplicate
            commitments.

            The request ID must be a valid
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier#Format>`__
            A zero UUID (00000000-0000-0000-0000-000000000000) is not
            supported.
    """

    parent = proto.Field(proto.STRING, number=1,)
    service_id = proto.Field(proto.STRING, number=2,)
    service = proto.Field(proto.MESSAGE, number=3, message="Service",)
    request_id = proto.Field(proto.STRING, number=4,)


class UpdateServiceRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.UpdateService][google.cloud.metastore.v1.DataprocMetastore.UpdateService].

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. A field mask used to specify the fields to be
            overwritten in the metastore service resource by the update.
            Fields specified in the ``update_mask`` are relative to the
            resource (not to the full request). A field is overwritten
            if it is in the mask.
        service (google.cloud.metastore_v1.types.Service):
            Required. The metastore service to update. The server only
            merges fields in the service if they are specified in
            ``update_mask``.

            The metastore service's ``name`` field is used to identify
            the metastore service to be updated.
        request_id (str):
            Optional. A request ID. Specify a unique request ID to allow
            the server to ignore the request if it has completed. The
            server will ignore subsequent requests that provide a
            duplicate request ID for at least 60 minutes after the first
            request.

            For example, if an initial request times out, followed by
            another request with the same request ID, the server ignores
            the second request to prevent the creation of duplicate
            commitments.

            The request ID must be a valid
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier#Format>`__
            A zero UUID (00000000-0000-0000-0000-000000000000) is not
            supported.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    service = proto.Field(proto.MESSAGE, number=2, message="Service",)
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteServiceRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.DeleteService][google.cloud.metastore.v1.DataprocMetastore.DeleteService].

    Attributes:
        name (str):
            Required. The relative resource name of the metastore
            service to delete, in the following form:

            ``projects/{project_number}/locations/{location_id}/services/{service_id}``.
        request_id (str):
            Optional. A request ID. Specify a unique request ID to allow
            the server to ignore the request if it has completed. The
            server will ignore subsequent requests that provide a
            duplicate request ID for at least 60 minutes after the first
            request.

            For example, if an initial request times out, followed by
            another request with the same request ID, the server ignores
            the second request to prevent the creation of duplicate
            commitments.

            The request ID must be a valid
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier#Format>`__
            A zero UUID (00000000-0000-0000-0000-000000000000) is not
            supported.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class ListMetadataImportsRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1.DataprocMetastore.ListMetadataImports].

    Attributes:
        parent (str):
            Required. The relative resource name of the service whose
            metadata imports to list, in the following form:

            ``projects/{project_number}/locations/{location_id}/services/{service_id}/metadataImports``.
        page_size (int):
            Optional. The maximum number of imports to
            return. The response may contain less than the
            maximum number. If unspecified, no more than 500
            imports are returned. The maximum value is 1000;
            values above 1000 are changed to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices]
            call. Provide this token to retrieve the subsequent page.

            To retrieve the first page, supply an empty page token.

            When paginating, other parameters provided to
            [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices]
            must match the call that provided the page token.
        filter (str):
            Optional. The filter to apply to list
            results.
        order_by (str):
            Optional. Specify the ordering of results as described in
            `Sorting
            Order <https://cloud.google.com/apis/design/design_patterns#sorting_order>`__.
            If not specified, the results will be sorted in the default
            order.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListMetadataImportsResponse(proto.Message):
    r"""Response message for
    [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1.DataprocMetastore.ListMetadataImports].

    Attributes:
        metadata_imports (Sequence[google.cloud.metastore_v1.types.MetadataImport]):
            The imports in the specified service.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    metadata_imports = proto.RepeatedField(
        proto.MESSAGE, number=1, message="MetadataImport",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetMetadataImportRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.GetMetadataImport][google.cloud.metastore.v1.DataprocMetastore.GetMetadataImport].

    Attributes:
        name (str):
            Required. The relative resource name of the metadata import
            to retrieve, in the following form:

            ``projects/{project_number}/locations/{location_id}/services/{service_id}/metadataImports/{import_id}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateMetadataImportRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.CreateMetadataImport][google.cloud.metastore.v1.DataprocMetastore.CreateMetadataImport].

    Attributes:
        parent (str):
            Required. The relative resource name of the service in which
            to create a metastore import, in the following form:

            ``projects/{project_number}/locations/{location_id}/services/{service_id}``.
        metadata_import_id (str):
            Required. The ID of the metadata import,
            which is used as the final component of the
            metadata import's name.
            This value must be between 1 and 64 characters
            long, begin with a letter, end with a letter or
            number, and consist of alpha-numeric ASCII
            characters or hyphens.
        metadata_import (google.cloud.metastore_v1.types.MetadataImport):
            Required. The metadata import to create. The ``name`` field
            is ignored. The ID of the created metadata import must be
            provided in the request's ``metadata_import_id`` field.
        request_id (str):
            Optional. A request ID. Specify a unique request ID to allow
            the server to ignore the request if it has completed. The
            server will ignore subsequent requests that provide a
            duplicate request ID for at least 60 minutes after the first
            request.

            For example, if an initial request times out, followed by
            another request with the same request ID, the server ignores
            the second request to prevent the creation of duplicate
            commitments.

            The request ID must be a valid
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier#Format>`__
            A zero UUID (00000000-0000-0000-0000-000000000000) is not
            supported.
    """

    parent = proto.Field(proto.STRING, number=1,)
    metadata_import_id = proto.Field(proto.STRING, number=2,)
    metadata_import = proto.Field(proto.MESSAGE, number=3, message="MetadataImport",)
    request_id = proto.Field(proto.STRING, number=4,)


class UpdateMetadataImportRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.UpdateMetadataImport][google.cloud.metastore.v1.DataprocMetastore.UpdateMetadataImport].

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. A field mask used to specify the fields to be
            overwritten in the metadata import resource by the update.
            Fields specified in the ``update_mask`` are relative to the
            resource (not to the full request). A field is overwritten
            if it is in the mask.
        metadata_import (google.cloud.metastore_v1.types.MetadataImport):
            Required. The metadata import to update. The server only
            merges fields in the import if they are specified in
            ``update_mask``.

            The metadata import's ``name`` field is used to identify the
            metastore import to be updated.
        request_id (str):
            Optional. A request ID. Specify a unique request ID to allow
            the server to ignore the request if it has completed. The
            server will ignore subsequent requests that provide a
            duplicate request ID for at least 60 minutes after the first
            request.

            For example, if an initial request times out, followed by
            another request with the same request ID, the server ignores
            the second request to prevent the creation of duplicate
            commitments.

            The request ID must be a valid
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier#Format>`__
            A zero UUID (00000000-0000-0000-0000-000000000000) is not
            supported.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    metadata_import = proto.Field(proto.MESSAGE, number=2, message="MetadataImport",)
    request_id = proto.Field(proto.STRING, number=3,)


class ExportMetadataRequest(proto.Message):
    r"""Request message for
    [DataprocMetastore.ExportMetadata][google.cloud.metastore.v1.DataprocMetastore.ExportMetadata].

    Attributes:
        destination_gcs_folder (str):
            A Cloud Storage URI of a folder, in the format
            ``gs://<bucket_name>/<path_inside_bucket>``. A sub-folder
            ``<export_folder>`` containing exported files will be
            created below it.
        service (str):
            Required. The relative resource name of the metastore
            service to run export, in the following form:

            ``projects/{project_id}/locations/{location_id}/services/{service_id}``.
        request_id (str):
            Optional. A request ID. Specify a unique request ID to allow
            the server to ignore the request if it has completed. The
            server will ignore subsequent requests that provide a
            duplicate request ID for at least 60 minutes after the first
            request.

            For example, if an initial request times out, followed by
            another request with the same request ID, the server ignores
            the second request to prevent the creation of duplicate
            commitments.

            The request ID must be a valid
            `UUID <https://en.wikipedia.org/wiki/Universally_unique_identifier#Format>`__.
            A zero UUID (00000000-0000-0000-0000-000000000000) is not
            supported.
        database_dump_type (google.cloud.metastore_v1.types.DatabaseDumpSpec.Type):
            Optional. The type of the database dump. If unspecified,
            defaults to ``MYSQL``.
    """

    destination_gcs_folder = proto.Field(proto.STRING, number=2, oneof="destination",)
    service = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=3,)
    database_dump_type = proto.Field(
        proto.ENUM, number=4, enum="DatabaseDumpSpec.Type",
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of a long-running operation.
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
            Output only. Identifies whether the caller has requested
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
    status_message = proto.Field(proto.STRING, number=5,)
    requested_cancellation = proto.Field(proto.BOOL, number=6,)
    api_version = proto.Field(proto.STRING, number=7,)


class LocationMetadata(proto.Message):
    r"""Metadata about the service in a location.
    Attributes:
        supported_hive_metastore_versions (Sequence[google.cloud.metastore_v1.types.LocationMetadata.HiveMetastoreVersion]):
            The versions of Hive Metastore that can be used when
            creating a new metastore service in this location. The
            server guarantees that exactly one ``HiveMetastoreVersion``
            in the list will set ``is_default``.
    """

    class HiveMetastoreVersion(proto.Message):
        r"""A specification of a supported version of the Hive Metastore
        software.

        Attributes:
            version (str):
                The semantic version of the Hive Metastore
                software.
            is_default (bool):
                Whether ``version`` will be chosen by the server if a
                metastore service is created with a ``HiveMetastoreConfig``
                that omits the ``version``.
        """

        version = proto.Field(proto.STRING, number=1,)
        is_default = proto.Field(proto.BOOL, number=2,)

    supported_hive_metastore_versions = proto.RepeatedField(
        proto.MESSAGE, number=1, message=HiveMetastoreVersion,
    )


class DatabaseDumpSpec(proto.Message):
    r"""The specification of database dump to import from or export
    to.
        """

    class Type(proto.Enum):
        r"""The type of the database dump."""
        TYPE_UNSPECIFIED = 0
        MYSQL = 1


__all__ = tuple(sorted(__protobuf__.manifest))
