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

from google.cloud.clouddms_v1.types import clouddms_resources
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.clouddms.v1",
    manifest={
        "ListMigrationJobsRequest",
        "ListMigrationJobsResponse",
        "GetMigrationJobRequest",
        "CreateMigrationJobRequest",
        "UpdateMigrationJobRequest",
        "DeleteMigrationJobRequest",
        "StartMigrationJobRequest",
        "StopMigrationJobRequest",
        "ResumeMigrationJobRequest",
        "PromoteMigrationJobRequest",
        "VerifyMigrationJobRequest",
        "RestartMigrationJobRequest",
        "GenerateSshScriptRequest",
        "VmCreationConfig",
        "VmSelectionConfig",
        "SshScript",
        "ListConnectionProfilesRequest",
        "ListConnectionProfilesResponse",
        "GetConnectionProfileRequest",
        "CreateConnectionProfileRequest",
        "UpdateConnectionProfileRequest",
        "DeleteConnectionProfileRequest",
        "OperationMetadata",
    },
)


class ListMigrationJobsRequest(proto.Message):
    r"""Retrieve a list of all migration jobs in a given project and
    location.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of migrationJobs.
        page_size (int):
            The maximum number of migration jobs to
            return. The service may return fewer than this
            value. If unspecified, at most 50 migration jobs
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            The nextPageToken value received in the
            previous call to migrationJobs.list, used in the
            subsequent request to retrieve the next page of
            results. On first call this should be left
            blank. When paginating, all other parameters
            provided to migrationJobs.list must match the
            call that provided the page token.
        filter (str):
            A filter expression that filters migration jobs listed in
            the response. The expression must specify the field name, a
            comparison operator, and the value that you want to use for
            filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be either =, !=, >, or
            <. For example, list migration jobs created this year by
            specifying **createTime %gt;
            2020-01-01T00:00:00.000000000Z.** You can also filter nested
            fields. For example, you could specify
            **reverseSshConnectivity.vmIp = "1.2.3.4"** to select all
            migration jobs connecting through the specific SSH tunnel
            bastion.
        order_by (str):
            Sort the results based on the migration job
            name. Valid values are: "name", "name asc", and
            "name desc".
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListMigrationJobsResponse(proto.Message):
    r"""Response message for 'ListMigrationJobs' request.

    Attributes:
        migration_jobs (Sequence[google.cloud.clouddms_v1.types.MigrationJob]):
            The list of migration jobs objects.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    migration_jobs = proto.RepeatedField(
        proto.MESSAGE, number=1, message=clouddms_resources.MigrationJob,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetMigrationJobRequest(proto.Message):
    r"""Request message for 'GetMigrationJob' request.

    Attributes:
        name (str):
            Required. Name of the migration job resource
            to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateMigrationJobRequest(proto.Message):
    r"""Request message to create a new Database Migration Service
    migration job in the specified project and region.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of migration jobs.
        migration_job_id (str):
            Required. The ID of the instance to create.
        migration_job (google.cloud.clouddms_v1.types.MigrationJob):
            Required. Represents a `migration
            job <https://cloud.google.com/database-migration/docs/reference/rest/v1/projects.locations.migrationJobs>`__
            object.
        request_id (str):
            A unique id used to identify the request. If the server
            receives two requests with the same id, then the second
            request will be ignored.

            It is recommended to always set this value to a UUID.

            The id must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and hyphens (-). The maximum length is 40
            characters.
    """

    parent = proto.Field(proto.STRING, number=1,)
    migration_job_id = proto.Field(proto.STRING, number=2,)
    migration_job = proto.Field(
        proto.MESSAGE, number=3, message=clouddms_resources.MigrationJob,
    )
    request_id = proto.Field(proto.STRING, number=4,)


class UpdateMigrationJobRequest(proto.Message):
    r"""Request message for 'UpdateMigrationJob' request.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the
            fields to be overwritten in the migration job
            resource by the update.
        migration_job (google.cloud.clouddms_v1.types.MigrationJob):
            Required. The migration job parameters to
            update.
        request_id (str):
            A unique id used to identify the request. If the server
            receives two requests with the same id, then the second
            request will be ignored.

            It is recommended to always set this value to a UUID.

            The id must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and hyphens (-). The maximum length is 40
            characters.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    migration_job = proto.Field(
        proto.MESSAGE, number=2, message=clouddms_resources.MigrationJob,
    )
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteMigrationJobRequest(proto.Message):
    r"""Request message for 'DeleteMigrationJob' request.

    Attributes:
        name (str):
            Required. Name of the migration job resource
            to delete.
        request_id (str):
            A unique id used to identify the request. If the server
            receives two requests with the same id, then the second
            request will be ignored.

            It is recommended to always set this value to a UUID.

            The id must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and hyphens (-). The maximum length is 40
            characters.
        force (bool):
            The destination CloudSQL connection profile
            is always deleted with the migration job. In
            case of force delete, the destination CloudSQL
            replica database is also deleted.
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)
    force = proto.Field(proto.BOOL, number=3,)


class StartMigrationJobRequest(proto.Message):
    r"""Request message for 'StartMigrationJob' request.

    Attributes:
        name (str):
            Name of the migration job resource to start.
    """

    name = proto.Field(proto.STRING, number=1,)


class StopMigrationJobRequest(proto.Message):
    r"""Request message for 'StopMigrationJob' request.

    Attributes:
        name (str):
            Name of the migration job resource to stop.
    """

    name = proto.Field(proto.STRING, number=1,)


class ResumeMigrationJobRequest(proto.Message):
    r"""Request message for 'ResumeMigrationJob' request.

    Attributes:
        name (str):
            Name of the migration job resource to resume.
    """

    name = proto.Field(proto.STRING, number=1,)


class PromoteMigrationJobRequest(proto.Message):
    r"""Request message for 'PromoteMigrationJob' request.

    Attributes:
        name (str):
            Name of the migration job resource to
            promote.
    """

    name = proto.Field(proto.STRING, number=1,)


class VerifyMigrationJobRequest(proto.Message):
    r"""Request message for 'VerifyMigrationJob' request.

    Attributes:
        name (str):
            Name of the migration job resource to verify.
    """

    name = proto.Field(proto.STRING, number=1,)


class RestartMigrationJobRequest(proto.Message):
    r"""Request message for 'RestartMigrationJob' request.

    Attributes:
        name (str):
            Name of the migration job resource to
            restart.
    """

    name = proto.Field(proto.STRING, number=1,)


class GenerateSshScriptRequest(proto.Message):
    r"""Request message for 'GenerateSshScript' request.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        migration_job (str):
            Name of the migration job resource to
            generate the SSH script.
        vm (str):
            Required. Bastion VM Instance name to use or
            to create.
        vm_creation_config (google.cloud.clouddms_v1.types.VmCreationConfig):
            The VM creation configuration

            This field is a member of `oneof`_ ``vm_config``.
        vm_selection_config (google.cloud.clouddms_v1.types.VmSelectionConfig):
            The VM selection configuration

            This field is a member of `oneof`_ ``vm_config``.
        vm_port (int):
            The port that will be open on the bastion
            host
    """

    migration_job = proto.Field(proto.STRING, number=1,)
    vm = proto.Field(proto.STRING, number=2,)
    vm_creation_config = proto.Field(
        proto.MESSAGE, number=100, oneof="vm_config", message="VmCreationConfig",
    )
    vm_selection_config = proto.Field(
        proto.MESSAGE, number=101, oneof="vm_config", message="VmSelectionConfig",
    )
    vm_port = proto.Field(proto.INT32, number=3,)


class VmCreationConfig(proto.Message):
    r"""VM creation configuration message

    Attributes:
        vm_machine_type (str):
            Required. VM instance machine type to create.
        vm_zone (str):
            The Google Cloud Platform zone to create the
            VM in.
        subnet (str):
            The subnet name the vm needs to be created
            in.
    """

    vm_machine_type = proto.Field(proto.STRING, number=1,)
    vm_zone = proto.Field(proto.STRING, number=2,)
    subnet = proto.Field(proto.STRING, number=3,)


class VmSelectionConfig(proto.Message):
    r"""VM selection configuration message

    Attributes:
        vm_zone (str):
            Required. The Google Cloud Platform zone the
            VM is located.
    """

    vm_zone = proto.Field(proto.STRING, number=1,)


class SshScript(proto.Message):
    r"""Response message for 'GenerateSshScript' request.

    Attributes:
        script (str):
            The ssh configuration script.
    """

    script = proto.Field(proto.STRING, number=1,)


class ListConnectionProfilesRequest(proto.Message):
    r"""Request message for 'ListConnectionProfiles' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of connection profiles.
        page_size (int):
            The maximum number of connection profiles to
            return. The service may return fewer than this
            value. If unspecified, at most 50 connection
            profiles will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            A page token, received from a previous
            ``ListConnectionProfiles`` call. Provide this to retrieve
            the subsequent page.

            When paginating, all other parameters provided to
            ``ListConnectionProfiles`` must match the call that provided
            the page token.
        filter (str):
            A filter expression that filters connection profiles listed
            in the response. The expression must specify the field name,
            a comparison operator, and the value that you want to use
            for filtering. The value must be a string, a number, or a
            boolean. The comparison operator must be either =, !=, >, or
            <. For example, list connection profiles created this year
            by specifying **createTime %gt;
            2020-01-01T00:00:00.000000000Z**. You can also filter nested
            fields. For example, you could specify **mySql.username =
            %lt;my_username%gt;** to list all connection profiles
            configured to connect with a specific username.
        order_by (str):
            the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListConnectionProfilesResponse(proto.Message):
    r"""Response message for 'ListConnectionProfiles' request.

    Attributes:
        connection_profiles (Sequence[google.cloud.clouddms_v1.types.ConnectionProfile]):
            The response list of connection profiles.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    connection_profiles = proto.RepeatedField(
        proto.MESSAGE, number=1, message=clouddms_resources.ConnectionProfile,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetConnectionProfileRequest(proto.Message):
    r"""Request message for 'GetConnectionProfile' request.

    Attributes:
        name (str):
            Required. Name of the connection profile
            resource to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateConnectionProfileRequest(proto.Message):
    r"""Request message for 'CreateConnectionProfile' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of connection profiles.
        connection_profile_id (str):
            Required. The connection profile identifier.
        connection_profile (google.cloud.clouddms_v1.types.ConnectionProfile):
            Required. The create request body including
            the connection profile data
        request_id (str):
            A unique id used to identify the request. If the server
            receives two requests with the same id, then the second
            request will be ignored.

            It is recommended to always set this value to a UUID.

            The id must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and hyphens (-). The maximum length is 40
            characters.
    """

    parent = proto.Field(proto.STRING, number=1,)
    connection_profile_id = proto.Field(proto.STRING, number=2,)
    connection_profile = proto.Field(
        proto.MESSAGE, number=3, message=clouddms_resources.ConnectionProfile,
    )
    request_id = proto.Field(proto.STRING, number=4,)


class UpdateConnectionProfileRequest(proto.Message):
    r"""Request message for 'UpdateConnectionProfile' request.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the
            fields to be overwritten in the connection
            profile resource by the update.
        connection_profile (google.cloud.clouddms_v1.types.ConnectionProfile):
            Required. The connection profile parameters
            to update.
        request_id (str):
            A unique id used to identify the request. If the server
            receives two requests with the same id, then the second
            request will be ignored.

            It is recommended to always set this value to a UUID.

            The id must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and hyphens (-). The maximum length is 40
            characters.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    connection_profile = proto.Field(
        proto.MESSAGE, number=2, message=clouddms_resources.ConnectionProfile,
    )
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteConnectionProfileRequest(proto.Message):
    r"""Request message for 'DeleteConnectionProfile' request.

    Attributes:
        name (str):
            Required. Name of the connection profile
            resource to delete.
        request_id (str):
            A unique id used to identify the request. If the server
            receives two requests with the same id, then the second
            request will be ignored.

            It is recommended to always set this value to a UUID.

            The id must contain only letters (a-z, A-Z), numbers (0-9),
            underscores (_), and hyphens (-). The maximum length is 40
            characters.
        force (bool):
            In case of force delete, the CloudSQL replica
            database is also deleted (only for CloudSQL
            connection profile).
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)
    force = proto.Field(proto.BOOL, number=3,)


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

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    target = proto.Field(proto.STRING, number=3,)
    verb = proto.Field(proto.STRING, number=4,)
    status_message = proto.Field(proto.STRING, number=5,)
    requested_cancellation = proto.Field(proto.BOOL, number=6,)
    api_version = proto.Field(proto.STRING, number=7,)


__all__ = tuple(sorted(__protobuf__.manifest))
