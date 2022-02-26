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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import error_details_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.vmmigration.v1",
    manifest={
        "UtilizationReportView",
        "ComputeEngineDiskType",
        "ComputeEngineLicenseType",
        "ComputeEngineBootOption",
        "ReplicationCycle",
        "ReplicationSync",
        "MigratingVm",
        "CloneJob",
        "CutoverJob",
        "CreateCloneJobRequest",
        "CancelCloneJobRequest",
        "CancelCloneJobResponse",
        "ListCloneJobsRequest",
        "ListCloneJobsResponse",
        "GetCloneJobRequest",
        "Source",
        "VmwareSourceDetails",
        "DatacenterConnector",
        "ListSourcesRequest",
        "ListSourcesResponse",
        "GetSourceRequest",
        "CreateSourceRequest",
        "UpdateSourceRequest",
        "DeleteSourceRequest",
        "FetchInventoryRequest",
        "VmwareVmDetails",
        "VmwareVmsDetails",
        "FetchInventoryResponse",
        "UtilizationReport",
        "VmUtilizationInfo",
        "VmUtilizationMetrics",
        "ListUtilizationReportsRequest",
        "ListUtilizationReportsResponse",
        "GetUtilizationReportRequest",
        "CreateUtilizationReportRequest",
        "DeleteUtilizationReportRequest",
        "ListDatacenterConnectorsResponse",
        "GetDatacenterConnectorRequest",
        "CreateDatacenterConnectorRequest",
        "DeleteDatacenterConnectorRequest",
        "ListDatacenterConnectorsRequest",
        "ComputeEngineTargetDefaults",
        "ComputeEngineTargetDetails",
        "NetworkInterface",
        "AppliedLicense",
        "SchedulingNodeAffinity",
        "ComputeScheduling",
        "SchedulePolicy",
        "CreateMigratingVmRequest",
        "ListMigratingVmsRequest",
        "ListMigratingVmsResponse",
        "GetMigratingVmRequest",
        "UpdateMigratingVmRequest",
        "DeleteMigratingVmRequest",
        "StartMigrationRequest",
        "StartMigrationResponse",
        "PauseMigrationRequest",
        "PauseMigrationResponse",
        "ResumeMigrationRequest",
        "ResumeMigrationResponse",
        "FinalizeMigrationRequest",
        "FinalizeMigrationResponse",
        "TargetProject",
        "GetTargetProjectRequest",
        "ListTargetProjectsRequest",
        "ListTargetProjectsResponse",
        "CreateTargetProjectRequest",
        "UpdateTargetProjectRequest",
        "DeleteTargetProjectRequest",
        "Group",
        "ListGroupsRequest",
        "ListGroupsResponse",
        "GetGroupRequest",
        "CreateGroupRequest",
        "UpdateGroupRequest",
        "DeleteGroupRequest",
        "AddGroupMigrationRequest",
        "AddGroupMigrationResponse",
        "RemoveGroupMigrationRequest",
        "RemoveGroupMigrationResponse",
        "CreateCutoverJobRequest",
        "CancelCutoverJobRequest",
        "CancelCutoverJobResponse",
        "ListCutoverJobsRequest",
        "ListCutoverJobsResponse",
        "GetCutoverJobRequest",
        "OperationMetadata",
        "MigrationError",
    },
)


class UtilizationReportView(proto.Enum):
    r"""Controls the level of details of a Utilization Report."""
    UTILIZATION_REPORT_VIEW_UNSPECIFIED = 0
    BASIC = 1
    FULL = 2


class ComputeEngineDiskType(proto.Enum):
    r"""Types of disks supported for Compute Engine VM."""
    COMPUTE_ENGINE_DISK_TYPE_UNSPECIFIED = 0
    COMPUTE_ENGINE_DISK_TYPE_STANDARD = 1
    COMPUTE_ENGINE_DISK_TYPE_SSD = 2
    COMPUTE_ENGINE_DISK_TYPE_BALANCED = 3


class ComputeEngineLicenseType(proto.Enum):
    r"""Types of licenses used in OS adaptation."""
    COMPUTE_ENGINE_LICENSE_TYPE_DEFAULT = 0
    COMPUTE_ENGINE_LICENSE_TYPE_PAYG = 1
    COMPUTE_ENGINE_LICENSE_TYPE_BYOL = 2


class ComputeEngineBootOption(proto.Enum):
    r"""Possible values for vm boot option."""
    COMPUTE_ENGINE_BOOT_OPTION_UNSPECIFIED = 0
    COMPUTE_ENGINE_BOOT_OPTION_EFI = 1
    COMPUTE_ENGINE_BOOT_OPTION_BIOS = 2


class ReplicationCycle(proto.Message):
    r"""ReplicationCycle contains information about the current
    replication cycle status.

    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the replication cycle has started.
        progress_percent (int):
            The current progress in percentage of this
            cycle.
    """

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    progress_percent = proto.Field(proto.INT32, number=5,)


class ReplicationSync(proto.Message):
    r"""ReplicationSync contain information about the last replica
    sync to the cloud.

    Attributes:
        last_sync_time (google.protobuf.timestamp_pb2.Timestamp):
            The most updated snapshot created time in the
            source that finished replication.
    """

    last_sync_time = proto.Field(
        proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,
    )


class MigratingVm(proto.Message):
    r"""MigratingVm describes the VM that will be migrated from a
    Source environment and its replication state.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        compute_engine_target_defaults (google.cloud.vmmigration_v1.types.ComputeEngineTargetDefaults):
            Details of the target VM in Compute Engine.

            This field is a member of `oneof`_ ``target_vm_defaults``.
        name (str):
            Output only. The identifier of the
            MigratingVm.
        source_vm_id (str):
            The unique ID of the VM in the source.
            The VM's name in vSphere can be changed, so this
            is not the VM's name but rather its moRef id.
            This id is of the form vm-<num>.
        display_name (str):
            The display name attached to the MigratingVm
            by the user.
        description (str):
            The description attached to the migrating VM
            by the user.
        policy (google.cloud.vmmigration_v1.types.SchedulePolicy):
            The replication schedule policy.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the migrating VM was
            created (this refers to this resource and not to
            the time it was installed in the source).
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last time the migrating VM
            resource was updated.
        last_sync (google.cloud.vmmigration_v1.types.ReplicationSync):
            Output only. The most updated snapshot
            created time in the source that finished
            replication.
        state (google.cloud.vmmigration_v1.types.MigratingVm.State):
            Output only. State of the MigratingVm.
        state_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last time the migrating VM
            state was updated.
        current_sync_info (google.cloud.vmmigration_v1.types.ReplicationCycle):
            Output only. The percentage progress of the
            current running replication cycle.
        group (str):
            Output only. The group this migrating vm is included in, if
            any. The group is represented by the full path of the
            appropriate [Group][google.cloud.vmmigration.v1.Group]
            resource.
        labels (Sequence[google.cloud.vmmigration_v1.types.MigratingVm.LabelsEntry]):
            The labels of the migrating VM.
        error (google.rpc.status_pb2.Status):
            Output only. Provides details on the state of
            the Migrating VM in case of an error in
            replication.
    """

    class State(proto.Enum):
        r"""The possible values of the state/health of source VM."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        READY = 2
        FIRST_SYNC = 3
        ACTIVE = 4
        CUTTING_OVER = 7
        CUTOVER = 8
        FINAL_SYNC = 9
        PAUSED = 10
        FINALIZING = 11
        FINALIZED = 12
        ERROR = 13

    compute_engine_target_defaults = proto.Field(
        proto.MESSAGE,
        number=26,
        oneof="target_vm_defaults",
        message="ComputeEngineTargetDefaults",
    )
    name = proto.Field(proto.STRING, number=1,)
    source_vm_id = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=18,)
    description = proto.Field(proto.STRING, number=3,)
    policy = proto.Field(proto.MESSAGE, number=8, message="SchedulePolicy",)
    create_time = proto.Field(proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )
    last_sync = proto.Field(proto.MESSAGE, number=11, message="ReplicationSync",)
    state = proto.Field(proto.ENUM, number=23, enum=State,)
    state_time = proto.Field(proto.MESSAGE, number=22, message=timestamp_pb2.Timestamp,)
    current_sync_info = proto.Field(
        proto.MESSAGE, number=13, message="ReplicationCycle",
    )
    group = proto.Field(proto.STRING, number=15,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=16,)
    error = proto.Field(proto.MESSAGE, number=19, message=status_pb2.Status,)


class CloneJob(proto.Message):
    r"""CloneJob describes the process of creating a clone of a
    [MigratingVM][google.cloud.vmmigration.v1.MigratingVm] to the
    requested target based on the latest successful uploaded snapshots.
    While the migration cycles of a MigratingVm take place, it is
    possible to verify the uploaded VM can be started in the cloud, by
    creating a clone. The clone can be created without any downtime, and
    it is created using the latest snapshots which are already in the
    cloud. The cloneJob is only responsible for its work, not its
    products, which means once it is finished, it will never touch the
    instance it created. It will only delete it in case of the CloneJob
    being cancelled or upon failure to clone.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        compute_engine_target_details (google.cloud.vmmigration_v1.types.ComputeEngineTargetDetails):
            Output only. Details of the target VM in
            Compute Engine.

            This field is a member of `oneof`_ ``target_vm_details``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the clone job was
            created (as an API call, not when it was
            actually created in the target).
        name (str):
            The name of the clone.
        state (google.cloud.vmmigration_v1.types.CloneJob.State):
            Output only. State of the clone job.
        state_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the state was last
            updated.
        error (google.rpc.status_pb2.Status):
            Output only. Provides details for the errors
            that led to the Clone Job's state.
    """

    class State(proto.Enum):
        r"""Possible states of the clone job."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        ACTIVE = 2
        FAILED = 3
        SUCCEEDED = 4
        CANCELLED = 5
        CANCELLING = 6
        ADAPTING_OS = 7

    compute_engine_target_details = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="target_vm_details",
        message="ComputeEngineTargetDetails",
    )
    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    name = proto.Field(proto.STRING, number=3,)
    state = proto.Field(proto.ENUM, number=12, enum=State,)
    state_time = proto.Field(proto.MESSAGE, number=14, message=timestamp_pb2.Timestamp,)
    error = proto.Field(proto.MESSAGE, number=17, message=status_pb2.Status,)


class CutoverJob(proto.Message):
    r"""CutoverJob message describes a cutover of a migrating VM. The
    CutoverJob is the operation of shutting down the VM, creating a
    snapshot and clonning the VM using the replicated snapshot.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        compute_engine_target_details (google.cloud.vmmigration_v1.types.ComputeEngineTargetDetails):
            Output only. Details of the target VM in
            Compute Engine.

            This field is a member of `oneof`_ ``target_vm_details``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the cutover job was
            created (as an API call, not when it was
            actually created in the target).
        name (str):
            Output only. The name of the cutover job.
        state (google.cloud.vmmigration_v1.types.CutoverJob.State):
            Output only. State of the cutover job.
        state_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the state was last
            updated.
        progress_percent (int):
            Output only. The current progress in
            percentage of the cutover job.
        error (google.rpc.status_pb2.Status):
            Output only. Provides details for the errors
            that led to the Cutover Job's state.
        state_message (str):
            Output only. A message providing possible
            extra details about the current state.
    """

    class State(proto.Enum):
        r"""Possible states of the cutover job."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        FAILED = 2
        SUCCEEDED = 3
        CANCELLED = 4
        CANCELLING = 5
        ACTIVE = 6
        ADAPTING_OS = 7

    compute_engine_target_details = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="target_vm_details",
        message="ComputeEngineTargetDetails",
    )
    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    name = proto.Field(proto.STRING, number=3,)
    state = proto.Field(proto.ENUM, number=5, enum=State,)
    state_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    progress_percent = proto.Field(proto.INT32, number=13,)
    error = proto.Field(proto.MESSAGE, number=9, message=status_pb2.Status,)
    state_message = proto.Field(proto.STRING, number=10,)


class CreateCloneJobRequest(proto.Message):
    r"""Request message for 'CreateCloneJob' request.

    Attributes:
        parent (str):
            Required. The Clone's parent.
        clone_job_id (str):
            Required. The clone job identifier.
        clone_job (google.cloud.vmmigration_v1.types.CloneJob):
            Required. The clone request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    clone_job_id = proto.Field(proto.STRING, number=2,)
    clone_job = proto.Field(proto.MESSAGE, number=3, message="CloneJob",)
    request_id = proto.Field(proto.STRING, number=4,)


class CancelCloneJobRequest(proto.Message):
    r"""Request message for 'CancelCloneJob' request.

    Attributes:
        name (str):
            Required. The clone job id
    """

    name = proto.Field(proto.STRING, number=1,)


class CancelCloneJobResponse(proto.Message):
    r"""Response message for 'CancelCloneJob' request.
    """


class ListCloneJobsRequest(proto.Message):
    r"""Request message for 'ListCloneJobsRequest' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of source VMs.
        page_size (int):
            Optional. The maximum number of clone jobs to
            return. The service may return fewer than this
            value. If unspecified, at most 500 clone jobs
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListCloneJobs`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListCloneJobs`` must match the call that provided the page
            token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListCloneJobsResponse(proto.Message):
    r"""Response message for 'ListCloneJobs' request.

    Attributes:
        clone_jobs (Sequence[google.cloud.vmmigration_v1.types.CloneJob]):
            Output only. The list of clone jobs response.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    clone_jobs = proto.RepeatedField(proto.MESSAGE, number=1, message="CloneJob",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetCloneJobRequest(proto.Message):
    r"""Request message for 'GetCloneJob' request.

    Attributes:
        name (str):
            Required. The name of the CloneJob.
    """

    name = proto.Field(proto.STRING, number=1,)


class Source(proto.Message):
    r"""Source message describes a specific vm migration Source
    resource. It contains the source environment information.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        vmware (google.cloud.vmmigration_v1.types.VmwareSourceDetails):
            Vmware type source details.

            This field is a member of `oneof`_ ``source_details``.
        name (str):
            Output only. The Source name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The create time timestamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time timestamp.
        labels (Sequence[google.cloud.vmmigration_v1.types.Source.LabelsEntry]):
            The labels of the source.
        description (str):
            User-provided description of the source.
    """

    vmware = proto.Field(
        proto.MESSAGE, number=10, oneof="source_details", message="VmwareSourceDetails",
    )
    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=4,)
    description = proto.Field(proto.STRING, number=6,)


class VmwareSourceDetails(proto.Message):
    r"""VmwareSourceDetails message describes a specific source
    details for the vmware source type.

    Attributes:
        username (str):
            The credentials username.
        password (str):
            Input only. The credentials password. This is
            write only and can not be read in a GET
            operation.
        vcenter_ip (str):
            The ip address of the vcenter this Source
            represents.
        thumbprint (str):
            The thumbprint representing the certificate
            for the vcenter.
    """

    username = proto.Field(proto.STRING, number=1,)
    password = proto.Field(proto.STRING, number=2,)
    vcenter_ip = proto.Field(proto.STRING, number=3,)
    thumbprint = proto.Field(proto.STRING, number=4,)


class DatacenterConnector(proto.Message):
    r"""DatacenterConnector message describes a connector between the
    Source and GCP, which is installed on a vmware datacenter (an
    OVA vm installed by the user) to connect the Datacenter to GCP
    and support vm migration data transfer.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the connector was
            created (as an API call, not when it was
            actually installed).
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last time the connector was
            updated with an API call.
        name (str):
            Output only. The connector's name.
        registration_id (str):
            Immutable. A unique key for this connector.
            This key is internal to the OVA connector and is
            supplied with its creation during the
            registration process and can not be modified.
        service_account (str):
            The service account to use in the connector
            when communicating with the cloud.
        version (str):
            The version running in the
            DatacenterConnector. This is supplied by the OVA
            connector during the registration process and
            can not be modified.
        bucket (str):
            Output only. The communication channel
            between the datacenter connector and GCP.
        state (google.cloud.vmmigration_v1.types.DatacenterConnector.State):
            Output only. State of the
            DatacenterConnector, as determined by the health
            checks.
        state_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the state was last set.
        error (google.rpc.status_pb2.Status):
            Output only. Provides details on the state of
            the Datacenter Connector in case of an error.
    """

    class State(proto.Enum):
        r"""The possible values of the state."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        OFFLINE = 2
        FAILED = 3
        ACTIVE = 4

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    name = proto.Field(proto.STRING, number=3,)
    registration_id = proto.Field(proto.STRING, number=12,)
    service_account = proto.Field(proto.STRING, number=5,)
    version = proto.Field(proto.STRING, number=6,)
    bucket = proto.Field(proto.STRING, number=10,)
    state = proto.Field(proto.ENUM, number=7, enum=State,)
    state_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)
    error = proto.Field(proto.MESSAGE, number=11, message=status_pb2.Status,)


class ListSourcesRequest(proto.Message):
    r"""Request message for 'ListSources' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of sources.
        page_size (int):
            Optional. The maximum number of sources to
            return. The service may return fewer than this
            value. If unspecified, at most 500 sources will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListSources`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListSources`` must match the call that provided the page
            token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListSourcesResponse(proto.Message):
    r"""Response message for 'ListSources' request.

    Attributes:
        sources (Sequence[google.cloud.vmmigration_v1.types.Source]):
            Output only. The list of sources response.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    sources = proto.RepeatedField(proto.MESSAGE, number=1, message="Source",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetSourceRequest(proto.Message):
    r"""Request message for 'GetSource' request.

    Attributes:
        name (str):
            Required. The Source name.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateSourceRequest(proto.Message):
    r"""Request message for 'CreateSource' request.

    Attributes:
        parent (str):
            Required. The Source's parent.
        source_id (str):
            Required. The source identifier.
        source (google.cloud.vmmigration_v1.types.Source):
            Required. The create request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    source_id = proto.Field(proto.STRING, number=2,)
    source = proto.Field(proto.MESSAGE, number=3, message="Source",)
    request_id = proto.Field(proto.STRING, number=4,)


class UpdateSourceRequest(proto.Message):
    r"""Update message for 'UpdateSources' request.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the Source resource by the update. The fields specified
            in the update_mask are relative to the resource, not the
            full request. A field will be overwritten if it is in the
            mask. If the user does not provide a mask then all fields
            will be overwritten.
        source (google.cloud.vmmigration_v1.types.Source):
            Required. The update request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    source = proto.Field(proto.MESSAGE, number=2, message="Source",)
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteSourceRequest(proto.Message):
    r"""Request message for 'DeleteSource' request.

    Attributes:
        name (str):
            Required. The Source name.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class FetchInventoryRequest(proto.Message):
    r"""Request message for
    [fetchInventory][google.cloud.vmmigration.v1.VmMigration.FetchInventory].

    Attributes:
        source (str):
            Required. The name of the Source.
        force_refresh (bool):
            If this flag is set to true, the source will
            be queried instead of using cached results.
            Using this flag will make the call slower.
    """

    source = proto.Field(proto.STRING, number=1,)
    force_refresh = proto.Field(proto.BOOL, number=2,)


class VmwareVmDetails(proto.Message):
    r"""VmwareVmDetails describes a VM in vCenter.

    Attributes:
        vm_id (str):
            The VM's id in the source (note that this is
            not the MigratingVm's id). This is the moref id
            of the VM.
        datacenter_id (str):
            The id of the vCenter's datacenter this VM is
            contained in.
        datacenter_description (str):
            The descriptive name of the vCenter's
            datacenter this VM is contained in.
        uuid (str):
            The unique identifier of the VM in vCenter.
        display_name (str):
            The display name of the VM. Note that this is
            not necessarily unique.
        power_state (google.cloud.vmmigration_v1.types.VmwareVmDetails.PowerState):
            The power state of the VM at the moment list
            was taken.
        cpu_count (int):
            The number of cpus in the VM.
        memory_mb (int):
            The size of the memory of the VM in MB.
        disk_count (int):
            The number of disks the VM has.
        committed_storage_mb (int):
            The total size of the storage allocated to
            the VM in MB.
        guest_description (str):
            The VM's OS. See for example
            https://pubs.vmware.com/vi-sdk/visdk250/ReferenceGuide/vim.vm.GuestOsDescriptor.GuestOsIdentifier.html
            for types of strings this might hold.
        boot_option (google.cloud.vmmigration_v1.types.VmwareVmDetails.BootOption):
            Output only. The VM Boot Option.
    """

    class PowerState(proto.Enum):
        r"""Possible values for the power state of the VM."""
        POWER_STATE_UNSPECIFIED = 0
        ON = 1
        OFF = 2
        SUSPENDED = 3

    class BootOption(proto.Enum):
        r"""Possible values for vm boot option."""
        BOOT_OPTION_UNSPECIFIED = 0
        EFI = 1
        BIOS = 2

    vm_id = proto.Field(proto.STRING, number=1,)
    datacenter_id = proto.Field(proto.STRING, number=2,)
    datacenter_description = proto.Field(proto.STRING, number=3,)
    uuid = proto.Field(proto.STRING, number=4,)
    display_name = proto.Field(proto.STRING, number=5,)
    power_state = proto.Field(proto.ENUM, number=6, enum=PowerState,)
    cpu_count = proto.Field(proto.INT32, number=7,)
    memory_mb = proto.Field(proto.INT32, number=8,)
    disk_count = proto.Field(proto.INT32, number=9,)
    committed_storage_mb = proto.Field(proto.INT64, number=12,)
    guest_description = proto.Field(proto.STRING, number=11,)
    boot_option = proto.Field(proto.ENUM, number=13, enum=BootOption,)


class VmwareVmsDetails(proto.Message):
    r"""VmwareVmsDetails describes VMs in vCenter.

    Attributes:
        details (Sequence[google.cloud.vmmigration_v1.types.VmwareVmDetails]):
            The details of the vmware VMs.
    """

    details = proto.RepeatedField(proto.MESSAGE, number=1, message="VmwareVmDetails",)


class FetchInventoryResponse(proto.Message):
    r"""Response message for
    [fetchInventory][google.cloud.vmmigration.v1.VmMigration.FetchInventory].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        vmware_vms (google.cloud.vmmigration_v1.types.VmwareVmsDetails):
            Output only. The description of the VMs in a
            Source of type Vmware.

            This field is a member of `oneof`_ ``SourceVms``.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the source
            was last queried (if the result is from the
            cache).
    """

    vmware_vms = proto.Field(
        proto.MESSAGE, number=1, oneof="SourceVms", message="VmwareVmsDetails",
    )
    update_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)


class UtilizationReport(proto.Message):
    r"""Utilization report details the utilization (CPU, memory,
    etc.) of selected source VMs.

    Attributes:
        name (str):
            Output only. The report unique name.
        display_name (str):
            The report display name, as assigned by the
            user.
        state (google.cloud.vmmigration_v1.types.UtilizationReport.State):
            Output only. Current state of the report.
        state_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the state was last set.
        error (google.rpc.status_pb2.Status):
            Output only. Provides details on the state of
            the report in case of an error.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the report was created
            (this refers to the time of the request, not the
            time the report creation completed).
        time_frame (google.cloud.vmmigration_v1.types.UtilizationReport.TimeFrame):
            Time frame of the report.
        frame_end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The point in time when the time frame ends.
            Notice that the time frame is counted backwards. For
            instance if the "frame_end_time" value is 2021/01/20 and the
            time frame is WEEK then the report covers the week between
            2021/01/20 and 2021/01/14.
        vm_count (int):
            Output only. Total number of VMs included in
            the report.
        vms (Sequence[google.cloud.vmmigration_v1.types.VmUtilizationInfo]):
            List of utilization information per VM. When sent as part of
            the request, the "vm_id" field is used in order to specify
            which VMs to include in the report. In that case all other
            fields are ignored.
    """

    class State(proto.Enum):
        r"""Utilization report state."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        SUCCEEDED = 2
        FAILED = 3

    class TimeFrame(proto.Enum):
        r"""Report time frame options."""
        TIME_FRAME_UNSPECIFIED = 0
        WEEK = 1
        MONTH = 2
        YEAR = 3

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    state = proto.Field(proto.ENUM, number=3, enum=State,)
    state_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    error = proto.Field(proto.MESSAGE, number=5, message=status_pb2.Status,)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    time_frame = proto.Field(proto.ENUM, number=7, enum=TimeFrame,)
    frame_end_time = proto.Field(
        proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,
    )
    vm_count = proto.Field(proto.INT32, number=9,)
    vms = proto.RepeatedField(proto.MESSAGE, number=10, message="VmUtilizationInfo",)


class VmUtilizationInfo(proto.Message):
    r"""Utilization information of a single VM.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        vmware_vm_details (google.cloud.vmmigration_v1.types.VmwareVmDetails):
            The description of the VM in a Source of type
            Vmware.

            This field is a member of `oneof`_ ``VmDetails``.
        vm_id (str):
            The VM's ID in the source.
        utilization (google.cloud.vmmigration_v1.types.VmUtilizationMetrics):
            Utilization metrics for this VM.
    """

    vmware_vm_details = proto.Field(
        proto.MESSAGE, number=1, oneof="VmDetails", message="VmwareVmDetails",
    )
    vm_id = proto.Field(proto.STRING, number=3,)
    utilization = proto.Field(proto.MESSAGE, number=2, message="VmUtilizationMetrics",)


class VmUtilizationMetrics(proto.Message):
    r"""Utilization metrics values for a single VM.

    Attributes:
        cpu_max_percent (int):
            Max CPU usage, percent.
        cpu_average_percent (int):
            Average CPU usage, percent.
        memory_max_percent (int):
            Max memory usage, percent.
        memory_average_percent (int):
            Average memory usage, percent.
        disk_io_rate_max_kbps (int):
            Max disk IO rate, in kilobytes per second.
        disk_io_rate_average_kbps (int):
            Average disk IO rate, in kilobytes per
            second.
        network_throughput_max_kbps (int):
            Max network throughput (combined
            transmit-rates and receive-rates), in kilobytes
            per second.
        network_throughput_average_kbps (int):
            Average network throughput (combined
            transmit-rates and receive-rates), in kilobytes
            per second.
    """

    cpu_max_percent = proto.Field(proto.INT32, number=9,)
    cpu_average_percent = proto.Field(proto.INT32, number=10,)
    memory_max_percent = proto.Field(proto.INT32, number=11,)
    memory_average_percent = proto.Field(proto.INT32, number=12,)
    disk_io_rate_max_kbps = proto.Field(proto.INT64, number=13,)
    disk_io_rate_average_kbps = proto.Field(proto.INT64, number=14,)
    network_throughput_max_kbps = proto.Field(proto.INT64, number=15,)
    network_throughput_average_kbps = proto.Field(proto.INT64, number=16,)


class ListUtilizationReportsRequest(proto.Message):
    r"""Request message for 'ListUtilizationReports' request.

    Attributes:
        parent (str):
            Required. The Utilization Reports parent.
        view (google.cloud.vmmigration_v1.types.UtilizationReportView):
            Optional. The level of details of each
            report. Defaults to BASIC.
        page_size (int):
            Optional. The maximum number of reports to
            return. The service may return fewer than this
            value. If unspecified, at most 500 reports will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListUtilizationReports`` call. Provide this to retrieve
            the subsequent page.

            When paginating, all other parameters provided to
            ``ListUtilizationReports`` must match the call that provided
            the page token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    view = proto.Field(proto.ENUM, number=2, enum="UtilizationReportView",)
    page_size = proto.Field(proto.INT32, number=3,)
    page_token = proto.Field(proto.STRING, number=4,)
    filter = proto.Field(proto.STRING, number=5,)
    order_by = proto.Field(proto.STRING, number=6,)


class ListUtilizationReportsResponse(proto.Message):
    r"""Response message for 'ListUtilizationReports' request.

    Attributes:
        utilization_reports (Sequence[google.cloud.vmmigration_v1.types.UtilizationReport]):
            Output only. The list of reports.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    utilization_reports = proto.RepeatedField(
        proto.MESSAGE, number=1, message="UtilizationReport",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetUtilizationReportRequest(proto.Message):
    r"""Request message for 'GetUtilizationReport' request.

    Attributes:
        name (str):
            Required. The Utilization Report name.
        view (google.cloud.vmmigration_v1.types.UtilizationReportView):
            Optional. The level of details of the report.
            Defaults to FULL
    """

    name = proto.Field(proto.STRING, number=1,)
    view = proto.Field(proto.ENUM, number=2, enum="UtilizationReportView",)


class CreateUtilizationReportRequest(proto.Message):
    r"""Request message for 'CreateUtilizationReport' request.

    Attributes:
        parent (str):
            Required. The Utilization Report's parent.
        utilization_report (google.cloud.vmmigration_v1.types.UtilizationReport):
            Required. The report to create.
        utilization_report_id (str):
            Required. The ID to use for the report, which will become
            the final component of the reports's resource name.

            This value maximum length is 63 characters, and valid
            characters are /[a-z][0-9]-/. It must start with an english
            letter and must not end with a hyphen.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    utilization_report = proto.Field(
        proto.MESSAGE, number=2, message="UtilizationReport",
    )
    utilization_report_id = proto.Field(proto.STRING, number=3,)
    request_id = proto.Field(proto.STRING, number=4,)


class DeleteUtilizationReportRequest(proto.Message):
    r"""Request message for 'DeleteUtilizationReport' request.

    Attributes:
        name (str):
            Required. The Utilization Report name.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class ListDatacenterConnectorsResponse(proto.Message):
    r"""Response message for 'ListDatacenterConnectors' request.

    Attributes:
        datacenter_connectors (Sequence[google.cloud.vmmigration_v1.types.DatacenterConnector]):
            Output only. The list of sources response.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    datacenter_connectors = proto.RepeatedField(
        proto.MESSAGE, number=1, message="DatacenterConnector",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetDatacenterConnectorRequest(proto.Message):
    r"""Request message for 'GetDatacenterConnector' request.

    Attributes:
        name (str):
            Required. The name of the
            DatacenterConnector.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateDatacenterConnectorRequest(proto.Message):
    r"""Request message for 'CreateDatacenterConnector' request.

    Attributes:
        parent (str):
            Required. The DatacenterConnector's parent. Required. The
            Source in where the new DatacenterConnector will be created.
            For example:
            ``projects/my-project/locations/us-central1/sources/my-source``
        datacenter_connector_id (str):
            Required. The datacenterConnector identifier.
        datacenter_connector (google.cloud.vmmigration_v1.types.DatacenterConnector):
            Required. The create request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    datacenter_connector_id = proto.Field(proto.STRING, number=2,)
    datacenter_connector = proto.Field(
        proto.MESSAGE, number=3, message="DatacenterConnector",
    )
    request_id = proto.Field(proto.STRING, number=4,)


class DeleteDatacenterConnectorRequest(proto.Message):
    r"""Request message for 'DeleteDatacenterConnector' request.

    Attributes:
        name (str):
            Required. The DatacenterConnector name.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes after the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class ListDatacenterConnectorsRequest(proto.Message):
    r"""Request message for 'ListDatacenterConnectors' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of connectors.
        page_size (int):
            Optional. The maximum number of connectors to
            return. The service may return fewer than this
            value. If unspecified, at most 500 sources will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListDatacenterConnectors`` call. Provide this to retrieve
            the subsequent page.

            When paginating, all other parameters provided to
            ``ListDatacenterConnectors`` must match the call that
            provided the page token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ComputeEngineTargetDefaults(proto.Message):
    r"""ComputeEngineTargetDefaults is a collection of details for
    creating a VM in a target Compute Engine project.

    Attributes:
        vm_name (str):
            The name of the VM to create.
        target_project (str):
            The full path of the resource of type
            TargetProject which represents the Compute
            Engine project in which to create this VM.
        zone (str):
            The zone in which to create the VM.
        machine_type_series (str):
            The machine type series to create the VM
            with.
        machine_type (str):
            The machine type to create the VM with.
        network_tags (Sequence[str]):
            A map of network tags to associate with the
            VM.
        network_interfaces (Sequence[google.cloud.vmmigration_v1.types.NetworkInterface]):
            List of NICs connected to this VM.
        service_account (str):
            The service account to associate the VM with.
        disk_type (google.cloud.vmmigration_v1.types.ComputeEngineDiskType):
            The disk type to use in the VM.
        labels (Sequence[google.cloud.vmmigration_v1.types.ComputeEngineTargetDefaults.LabelsEntry]):
            A map of labels to associate with the VM.
        license_type (google.cloud.vmmigration_v1.types.ComputeEngineLicenseType):
            The license type to use in OS adaptation.
        applied_license (google.cloud.vmmigration_v1.types.AppliedLicense):
            Output only. The OS license returned from the
            adaptation module report.
        compute_scheduling (google.cloud.vmmigration_v1.types.ComputeScheduling):
            Compute instance scheduling information (if
            empty default is used).
        secure_boot (bool):
            Defines whether the instance has Secure Boot
            enabled. This can be set to true only if the vm
            boot option is EFI.
        boot_option (google.cloud.vmmigration_v1.types.ComputeEngineBootOption):
            Output only. The VM Boot Option, as set in
            the source vm.
        metadata (Sequence[google.cloud.vmmigration_v1.types.ComputeEngineTargetDefaults.MetadataEntry]):
            The metadata key/value pairs to assign to the
            VM.
    """

    vm_name = proto.Field(proto.STRING, number=1,)
    target_project = proto.Field(proto.STRING, number=2,)
    zone = proto.Field(proto.STRING, number=3,)
    machine_type_series = proto.Field(proto.STRING, number=4,)
    machine_type = proto.Field(proto.STRING, number=5,)
    network_tags = proto.RepeatedField(proto.STRING, number=6,)
    network_interfaces = proto.RepeatedField(
        proto.MESSAGE, number=7, message="NetworkInterface",
    )
    service_account = proto.Field(proto.STRING, number=8,)
    disk_type = proto.Field(proto.ENUM, number=9, enum="ComputeEngineDiskType",)
    labels = proto.MapField(proto.STRING, proto.STRING, number=10,)
    license_type = proto.Field(proto.ENUM, number=11, enum="ComputeEngineLicenseType",)
    applied_license = proto.Field(proto.MESSAGE, number=12, message="AppliedLicense",)
    compute_scheduling = proto.Field(
        proto.MESSAGE, number=13, message="ComputeScheduling",
    )
    secure_boot = proto.Field(proto.BOOL, number=14,)
    boot_option = proto.Field(proto.ENUM, number=15, enum="ComputeEngineBootOption",)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=16,)


class ComputeEngineTargetDetails(proto.Message):
    r"""ComputeEngineTargetDetails is a collection of details for
    creating a VM in a target Compute Engine project.

    Attributes:
        vm_name (str):
            The name of the VM to create.
        project (str):
            The GCP target project ID or project name.
        zone (str):
            The zone in which to create the VM.
        machine_type_series (str):
            The machine type series to create the VM
            with.
        machine_type (str):
            The machine type to create the VM with.
        network_tags (Sequence[str]):
            A map of network tags to associate with the
            VM.
        network_interfaces (Sequence[google.cloud.vmmigration_v1.types.NetworkInterface]):
            List of NICs connected to this VM.
        service_account (str):
            The service account to associate the VM with.
        disk_type (google.cloud.vmmigration_v1.types.ComputeEngineDiskType):
            The disk type to use in the VM.
        labels (Sequence[google.cloud.vmmigration_v1.types.ComputeEngineTargetDetails.LabelsEntry]):
            A map of labels to associate with the VM.
        license_type (google.cloud.vmmigration_v1.types.ComputeEngineLicenseType):
            The license type to use in OS adaptation.
        applied_license (google.cloud.vmmigration_v1.types.AppliedLicense):
            The OS license returned from the adaptation
            module report.
        compute_scheduling (google.cloud.vmmigration_v1.types.ComputeScheduling):
            Compute instance scheduling information (if
            empty default is used).
        secure_boot (bool):
            Defines whether the instance has Secure Boot
            enabled. This can be set to true only if the vm
            boot option is EFI.
        boot_option (google.cloud.vmmigration_v1.types.ComputeEngineBootOption):
            The VM Boot Option, as set in the source vm.
        metadata (Sequence[google.cloud.vmmigration_v1.types.ComputeEngineTargetDetails.MetadataEntry]):
            The metadata key/value pairs to assign to the
            VM.
    """

    vm_name = proto.Field(proto.STRING, number=1,)
    project = proto.Field(proto.STRING, number=2,)
    zone = proto.Field(proto.STRING, number=3,)
    machine_type_series = proto.Field(proto.STRING, number=4,)
    machine_type = proto.Field(proto.STRING, number=5,)
    network_tags = proto.RepeatedField(proto.STRING, number=6,)
    network_interfaces = proto.RepeatedField(
        proto.MESSAGE, number=7, message="NetworkInterface",
    )
    service_account = proto.Field(proto.STRING, number=8,)
    disk_type = proto.Field(proto.ENUM, number=9, enum="ComputeEngineDiskType",)
    labels = proto.MapField(proto.STRING, proto.STRING, number=10,)
    license_type = proto.Field(proto.ENUM, number=11, enum="ComputeEngineLicenseType",)
    applied_license = proto.Field(proto.MESSAGE, number=12, message="AppliedLicense",)
    compute_scheduling = proto.Field(
        proto.MESSAGE, number=13, message="ComputeScheduling",
    )
    secure_boot = proto.Field(proto.BOOL, number=14,)
    boot_option = proto.Field(proto.ENUM, number=15, enum="ComputeEngineBootOption",)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=16,)


class NetworkInterface(proto.Message):
    r"""NetworkInterface represents a NIC of a VM.

    Attributes:
        network (str):
            The network to connect the NIC to.
        subnetwork (str):
            The subnetwork to connect the NIC to.
        internal_ip (str):
            The internal IP to define in the NIC. The formats accepted
            are: ``ephemeral`` \\ ipv4 address \\ a named address
            resource full path.
        external_ip (str):
            The external IP to define in the NIC.
    """

    network = proto.Field(proto.STRING, number=1,)
    subnetwork = proto.Field(proto.STRING, number=2,)
    internal_ip = proto.Field(proto.STRING, number=3,)
    external_ip = proto.Field(proto.STRING, number=4,)


class AppliedLicense(proto.Message):
    r"""AppliedLicense holds the license data returned by adaptation
    module report.

    Attributes:
        type_ (google.cloud.vmmigration_v1.types.AppliedLicense.Type):
            The license type that was used in OS
            adaptation.
        os_license (str):
            The OS license returned from the adaptation
            module's report.
    """

    class Type(proto.Enum):
        r"""License types used in OS adaptation."""
        TYPE_UNSPECIFIED = 0
        NONE = 1
        PAYG = 2
        BYOL = 3

    type_ = proto.Field(proto.ENUM, number=1, enum=Type,)
    os_license = proto.Field(proto.STRING, number=2,)


class SchedulingNodeAffinity(proto.Message):
    r"""Node Affinity: the configuration of desired nodes onto which
    this Instance could be scheduled. Based on
    https://cloud.google.com/compute/docs/reference/rest/v1/instances/setScheduling

    Attributes:
        key (str):
            The label key of Node resource to reference.
        operator (google.cloud.vmmigration_v1.types.SchedulingNodeAffinity.Operator):
            The operator to use for the node resources specified in the
            ``values`` parameter.
        values (Sequence[str]):
            Corresponds to the label values of Node
            resource.
    """

    class Operator(proto.Enum):
        r"""Possible types of node selection operators. Valid operators are IN
        for affinity and NOT_IN for anti-affinity.
        """
        OPERATOR_UNSPECIFIED = 0
        IN = 1
        NOT_IN = 2

    key = proto.Field(proto.STRING, number=1,)
    operator = proto.Field(proto.ENUM, number=2, enum=Operator,)
    values = proto.RepeatedField(proto.STRING, number=3,)


class ComputeScheduling(proto.Message):
    r"""Scheduling information for VM on maintenance/restart
    behaviour and node allocation in sole tenant nodes.

    Attributes:
        on_host_maintenance (google.cloud.vmmigration_v1.types.ComputeScheduling.OnHostMaintenance):
            How the instance should behave when the host
            machine undergoes maintenance that may
            temporarily impact instance performance.
        restart_type (google.cloud.vmmigration_v1.types.ComputeScheduling.RestartType):
            Whether the Instance should be automatically restarted
            whenever it is terminated by Compute Engine (not terminated
            by user). This configuration is identical to
            ``automaticRestart`` field in Compute Engine create instance
            under scheduling. It was changed to an enum (instead of a
            boolean) to match the default value in Compute Engine which
            is automatic restart.
        node_affinities (Sequence[google.cloud.vmmigration_v1.types.SchedulingNodeAffinity]):
            A set of node affinity and anti-affinity
            configurations for sole tenant nodes.
        min_node_cpus (int):
            The minimum number of virtual CPUs this instance will
            consume when running on a sole-tenant node. Ignored if no
            node_affinites are configured.
    """

    class OnHostMaintenance(proto.Enum):
        r""""""
        ON_HOST_MAINTENANCE_UNSPECIFIED = 0
        TERMINATE = 1
        MIGRATE = 2

    class RestartType(proto.Enum):
        r"""Defines whether the Instance should be automatically
        restarted whenever it is terminated by Compute Engine (not
        terminated by user).
        """
        RESTART_TYPE_UNSPECIFIED = 0
        AUTOMATIC_RESTART = 1
        NO_AUTOMATIC_RESTART = 2

    on_host_maintenance = proto.Field(proto.ENUM, number=1, enum=OnHostMaintenance,)
    restart_type = proto.Field(proto.ENUM, number=5, enum=RestartType,)
    node_affinities = proto.RepeatedField(
        proto.MESSAGE, number=3, message="SchedulingNodeAffinity",
    )
    min_node_cpus = proto.Field(proto.INT32, number=4,)


class SchedulePolicy(proto.Message):
    r"""A policy for scheduling replications.

    Attributes:
        idle_duration (google.protobuf.duration_pb2.Duration):
            The idle duration between replication stages.
        skip_os_adaptation (bool):
            A flag to indicate whether to skip OS
            adaptation during the replication sync. OS
            adaptation is a process where the VM's operating
            system undergoes changes and adaptations to
            fully function on Compute Engine.
    """

    idle_duration = proto.Field(proto.MESSAGE, number=1, message=duration_pb2.Duration,)
    skip_os_adaptation = proto.Field(proto.BOOL, number=2,)


class CreateMigratingVmRequest(proto.Message):
    r"""Request message for 'CreateMigratingVm' request.

    Attributes:
        parent (str):
            Required. The MigratingVm's parent.
        migrating_vm_id (str):
            Required. The migratingVm identifier.
        migrating_vm (google.cloud.vmmigration_v1.types.MigratingVm):
            Required. The create request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    migrating_vm_id = proto.Field(proto.STRING, number=2,)
    migrating_vm = proto.Field(proto.MESSAGE, number=3, message="MigratingVm",)
    request_id = proto.Field(proto.STRING, number=4,)


class ListMigratingVmsRequest(proto.Message):
    r"""Request message for 'LisMigratingVmsRequest' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of MigratingVms.
        page_size (int):
            Optional. The maximum number of migrating VMs
            to return. The service may return fewer than
            this value. If unspecified, at most 500
            migrating VMs will be returned. The maximum
            value is 1000; values above 1000 will be coerced
            to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListMigratingVms`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListMigratingVms`` must match the call that provided the
            page token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListMigratingVmsResponse(proto.Message):
    r"""Response message for 'ListMigratingVms' request.

    Attributes:
        migrating_vms (Sequence[google.cloud.vmmigration_v1.types.MigratingVm]):
            Output only. The list of Migrating VMs
            response.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    migrating_vms = proto.RepeatedField(proto.MESSAGE, number=1, message="MigratingVm",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetMigratingVmRequest(proto.Message):
    r"""Request message for 'GetMigratingVm' request.

    Attributes:
        name (str):
            Required. The name of the MigratingVm.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateMigratingVmRequest(proto.Message):
    r"""Request message for 'UpdateMigratingVm' request.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the MigratingVm resource by the update. The fields
            specified in the update_mask are relative to the resource,
            not the full request. A field will be overwritten if it is
            in the mask. If the user does not provide a mask then all
            fields will be overwritten.
        migrating_vm (google.cloud.vmmigration_v1.types.MigratingVm):
            Required. The update request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    migrating_vm = proto.Field(proto.MESSAGE, number=2, message="MigratingVm",)
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteMigratingVmRequest(proto.Message):
    r"""Request message for 'DeleteMigratingVm' request.

    Attributes:
        name (str):
            Required. The name of the MigratingVm.
    """

    name = proto.Field(proto.STRING, number=1,)


class StartMigrationRequest(proto.Message):
    r"""Request message for 'StartMigrationRequest' request.

    Attributes:
        migrating_vm (str):
            Required. The name of the MigratingVm.
    """

    migrating_vm = proto.Field(proto.STRING, number=1,)


class StartMigrationResponse(proto.Message):
    r"""Response message for 'StartMigration' request.
    """


class PauseMigrationRequest(proto.Message):
    r"""Request message for 'PauseMigration' request.

    Attributes:
        migrating_vm (str):
            Required. The name of the MigratingVm.
    """

    migrating_vm = proto.Field(proto.STRING, number=1,)


class PauseMigrationResponse(proto.Message):
    r"""Response message for 'PauseMigration' request.
    """


class ResumeMigrationRequest(proto.Message):
    r"""Request message for 'ResumeMigration' request.

    Attributes:
        migrating_vm (str):
            Required. The name of the MigratingVm.
    """

    migrating_vm = proto.Field(proto.STRING, number=1,)


class ResumeMigrationResponse(proto.Message):
    r"""Response message for 'ResumeMigration' request.
    """


class FinalizeMigrationRequest(proto.Message):
    r"""Request message for 'FinalizeMigration' request.

    Attributes:
        migrating_vm (str):
            Required. The name of the MigratingVm.
    """

    migrating_vm = proto.Field(proto.STRING, number=1,)


class FinalizeMigrationResponse(proto.Message):
    r"""Response message for 'FinalizeMigration' request.
    """


class TargetProject(proto.Message):
    r"""TargetProject message represents a target Compute Engine
    project for a migration or a clone.

    Attributes:
        name (str):
            The name of the target project.
        project (str):
            The target project ID (number) or project
            name.
        description (str):
            The target project's description.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this target project
            resource was created (not related to when the
            Compute Engine project it points to was
            created).
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last time the target project
            resource was updated.
    """

    name = proto.Field(proto.STRING, number=1,)
    project = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)


class GetTargetProjectRequest(proto.Message):
    r"""Request message for 'GetTargetProject' call.

    Attributes:
        name (str):
            Required. The TargetProject name.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListTargetProjectsRequest(proto.Message):
    r"""Request message for 'ListTargetProjects' call.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of targets.
        page_size (int):
            Optional. The maximum number of targets to
            return. The service may return fewer than this
            value. If unspecified, at most 500 targets will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListTargets`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListTargets`` must match the call that provided the page
            token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListTargetProjectsResponse(proto.Message):
    r"""Response message for 'ListTargetProjects' call.

    Attributes:
        target_projects (Sequence[google.cloud.vmmigration_v1.types.TargetProject]):
            Output only. The list of target response.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    target_projects = proto.RepeatedField(
        proto.MESSAGE, number=1, message="TargetProject",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class CreateTargetProjectRequest(proto.Message):
    r"""Request message for 'CreateTargetProject' request.

    Attributes:
        parent (str):
            Required. The TargetProject's parent.
        target_project_id (str):
            Required. The target_project identifier.
        target_project (google.cloud.vmmigration_v1.types.TargetProject):
            Required. The create request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    target_project_id = proto.Field(proto.STRING, number=2,)
    target_project = proto.Field(proto.MESSAGE, number=3, message="TargetProject",)
    request_id = proto.Field(proto.STRING, number=4,)


class UpdateTargetProjectRequest(proto.Message):
    r"""Update message for 'UpdateTargetProject' request.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the TargetProject resource by the update. The fields
            specified in the update_mask are relative to the resource,
            not the full request. A field will be overwritten if it is
            in the mask. If the user does not provide a mask then all
            fields will be overwritten.
        target_project (google.cloud.vmmigration_v1.types.TargetProject):
            Required. The update request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    target_project = proto.Field(proto.MESSAGE, number=2, message="TargetProject",)
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteTargetProjectRequest(proto.Message):
    r"""Request message for 'DeleteTargetProject' request.

    Attributes:
        name (str):
            Required. The TargetProject name.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class Group(proto.Message):
    r"""Describes message for 'Group' resource. The Group is a
    collections of several MigratingVms.

    Attributes:
        name (str):
            The Group name.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The create time timestamp.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update time timestamp.
        description (str):
            User-provided description of the group.
        display_name (str):
            Display name is a user defined name for this
            group which can be updated.
    """

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    description = proto.Field(proto.STRING, number=4,)
    display_name = proto.Field(proto.STRING, number=5,)


class ListGroupsRequest(proto.Message):
    r"""Request message for 'ListGroups' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of groups.
        page_size (int):
            Optional. The maximum number of groups to
            return. The service may return fewer than this
            value. If unspecified, at most 500 groups will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListGroups`` call. Provide this to retrieve the subsequent
            page.

            When paginating, all other parameters provided to
            ``ListGroups`` must match the call that provided the page
            token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListGroupsResponse(proto.Message):
    r"""Response message for 'ListGroups' request.

    Attributes:
        groups (Sequence[google.cloud.vmmigration_v1.types.Group]):
            Output only. The list of groups response.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    groups = proto.RepeatedField(proto.MESSAGE, number=1, message="Group",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetGroupRequest(proto.Message):
    r"""Request message for 'GetGroup' request.

    Attributes:
        name (str):
            Required. The group name.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateGroupRequest(proto.Message):
    r"""Request message for 'CreateGroup' request.

    Attributes:
        parent (str):
            Required. The Group's parent.
        group_id (str):
            Required. The group identifier.
        group (google.cloud.vmmigration_v1.types.Group):
            Required. The create request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    group_id = proto.Field(proto.STRING, number=2,)
    group = proto.Field(proto.MESSAGE, number=3, message="Group",)
    request_id = proto.Field(proto.STRING, number=4,)


class UpdateGroupRequest(proto.Message):
    r"""Update message for 'UpdateGroups' request.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Field mask is used to specify the fields to be overwritten
            in the Group resource by the update. The fields specified in
            the update_mask are relative to the resource, not the full
            request. A field will be overwritten if it is in the mask.
            If the user does not provide a mask then all fields will be
            overwritten.
        group (google.cloud.vmmigration_v1.types.Group):
            Required. The update request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=1, message=field_mask_pb2.FieldMask,
    )
    group = proto.Field(proto.MESSAGE, number=2, message="Group",)
    request_id = proto.Field(proto.STRING, number=3,)


class DeleteGroupRequest(proto.Message):
    r"""Request message for 'DeleteGroup' request.

    Attributes:
        name (str):
            Required. The Group name.
        request_id (str):
            Optional. A request ID to identify requests.
            Specify a unique request ID so that if you must
            retry your request, the server will know to
            ignore the request if it has already been
            completed. The server will guarantee that for at
            least 60 minutes after the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name = proto.Field(proto.STRING, number=1,)
    request_id = proto.Field(proto.STRING, number=2,)


class AddGroupMigrationRequest(proto.Message):
    r"""Request message for 'AddGroupMigration' request.

    Attributes:
        group (str):
            Required. The full path name of the Group to
            add to.
        migrating_vm (str):
            The full path name of the MigratingVm to add.
    """

    group = proto.Field(proto.STRING, number=1,)
    migrating_vm = proto.Field(proto.STRING, number=2,)


class AddGroupMigrationResponse(proto.Message):
    r"""Response message for 'AddGroupMigration' request.
    """


class RemoveGroupMigrationRequest(proto.Message):
    r"""Request message for 'RemoveMigration' request.

    Attributes:
        group (str):
            Required. The name of the Group.
        migrating_vm (str):
            The MigratingVm to remove.
    """

    group = proto.Field(proto.STRING, number=1,)
    migrating_vm = proto.Field(proto.STRING, number=2,)


class RemoveGroupMigrationResponse(proto.Message):
    r"""Response message for 'RemoveMigration' request.
    """


class CreateCutoverJobRequest(proto.Message):
    r"""Request message for 'CreateCutoverJob' request.

    Attributes:
        parent (str):
            Required. The Cutover's parent.
        cutover_job_id (str):
            Required. The cutover job identifier.
        cutover_job (google.cloud.vmmigration_v1.types.CutoverJob):
            Required. The cutover request body.
        request_id (str):
            A request ID to identify requests. Specify a
            unique request ID so that if you must retry your
            request, the server will know to ignore the
            request if it has already been completed. The
            server will guarantee that for at least 60
            minutes since the first request.
            For example, consider a situation where you make
            an initial request and t he request times out.
            If you make the request again with the same
            request ID, the server can check if original
            operation with the same request ID was received,
            and if so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.
            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent = proto.Field(proto.STRING, number=1,)
    cutover_job_id = proto.Field(proto.STRING, number=2,)
    cutover_job = proto.Field(proto.MESSAGE, number=3, message="CutoverJob",)
    request_id = proto.Field(proto.STRING, number=4,)


class CancelCutoverJobRequest(proto.Message):
    r"""Request message for 'CancelCutoverJob' request.

    Attributes:
        name (str):
            Required. The cutover job id
    """

    name = proto.Field(proto.STRING, number=1,)


class CancelCutoverJobResponse(proto.Message):
    r"""Response message for 'CancelCutoverJob' request.
    """


class ListCutoverJobsRequest(proto.Message):
    r"""Request message for 'ListCutoverJobsRequest' request.

    Attributes:
        parent (str):
            Required. The parent, which owns this
            collection of migrating VMs.
        page_size (int):
            Optional. The maximum number of cutover jobs
            to return. The service may return fewer than
            this value. If unspecified, at most 500 cutover
            jobs will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            Required. A page token, received from a previous
            ``ListCutoverJobs`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListCutoverJobs`` must match the call that provided the
            page token.
        filter (str):
            Optional. The filter request.
        order_by (str):
            Optional. the order by fields for the result.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListCutoverJobsResponse(proto.Message):
    r"""Response message for 'ListCutoverJobs' request.

    Attributes:
        cutover_jobs (Sequence[google.cloud.vmmigration_v1.types.CutoverJob]):
            Output only. The list of cutover jobs
            response.
        next_page_token (str):
            Output only. A token, which can be sent as ``page_token`` to
            retrieve the next page. If this field is omitted, there are
            no subsequent pages.
        unreachable (Sequence[str]):
            Output only. Locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    cutover_jobs = proto.RepeatedField(proto.MESSAGE, number=1, message="CutoverJob",)
    next_page_token = proto.Field(proto.STRING, number=2,)
    unreachable = proto.RepeatedField(proto.STRING, number=3,)


class GetCutoverJobRequest(proto.Message):
    r"""Request message for 'GetCutoverJob' request.

    Attributes:
        name (str):
            Required. The name of the CutoverJob.
    """

    name = proto.Field(proto.STRING, number=1,)


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


class MigrationError(proto.Message):
    r"""Represents migration resource error information that can be
    used with google.rpc.Status message. MigrationError is used to
    present the user with error information in migration operations.

    Attributes:
        code (google.cloud.vmmigration_v1.types.MigrationError.ErrorCode):
            Output only. The error code.
        error_message (google.rpc.error_details_pb2.LocalizedMessage):
            Output only. The localized error message.
        action_item (google.rpc.error_details_pb2.LocalizedMessage):
            Output only. Suggested action for solving the
            error.
        help_links (Sequence[google.rpc.error_details_pb2.Link]):
            Output only. URL(s) pointing to additional
            information on handling the current error.
        error_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the error occurred.
    """

    class ErrorCode(proto.Enum):
        r"""Represents resource error codes."""
        ERROR_CODE_UNSPECIFIED = 0
        UNKNOWN_ERROR = 1
        SOURCE_VALIDATION_ERROR = 2
        SOURCE_REPLICATION_ERROR = 3
        TARGET_REPLICATION_ERROR = 4
        OS_ADAPTATION_ERROR = 5
        CLONE_ERROR = 6
        CUTOVER_ERROR = 7
        UTILIZATION_REPORT_ERROR = 8

    code = proto.Field(proto.ENUM, number=1, enum=ErrorCode,)
    error_message = proto.Field(
        proto.MESSAGE, number=2, message=error_details_pb2.LocalizedMessage,
    )
    action_item = proto.Field(
        proto.MESSAGE, number=3, message=error_details_pb2.LocalizedMessage,
    )
    help_links = proto.RepeatedField(
        proto.MESSAGE, number=4, message=error_details_pb2.Help.Link,
    )
    error_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
