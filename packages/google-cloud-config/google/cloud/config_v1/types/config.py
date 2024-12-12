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
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.config.v1",
    manifest={
        "QuotaValidation",
        "Deployment",
        "TerraformBlueprint",
        "TerraformVariable",
        "ApplyResults",
        "TerraformOutput",
        "ListDeploymentsRequest",
        "ListDeploymentsResponse",
        "GetDeploymentRequest",
        "ListRevisionsRequest",
        "ListRevisionsResponse",
        "GetRevisionRequest",
        "CreateDeploymentRequest",
        "UpdateDeploymentRequest",
        "DeleteDeploymentRequest",
        "OperationMetadata",
        "Revision",
        "TerraformError",
        "GitSource",
        "DeploymentOperationMetadata",
        "Resource",
        "ResourceTerraformInfo",
        "ResourceCAIInfo",
        "GetResourceRequest",
        "ListResourcesRequest",
        "ListResourcesResponse",
        "Statefile",
        "ExportDeploymentStatefileRequest",
        "ExportRevisionStatefileRequest",
        "ImportStatefileRequest",
        "DeleteStatefileRequest",
        "LockDeploymentRequest",
        "UnlockDeploymentRequest",
        "ExportLockInfoRequest",
        "LockInfo",
        "Preview",
        "PreviewOperationMetadata",
        "PreviewArtifacts",
        "CreatePreviewRequest",
        "GetPreviewRequest",
        "ListPreviewsRequest",
        "ListPreviewsResponse",
        "DeletePreviewRequest",
        "ExportPreviewResultRequest",
        "ExportPreviewResultResponse",
        "PreviewResult",
        "GetTerraformVersionRequest",
        "ListTerraformVersionsRequest",
        "ListTerraformVersionsResponse",
        "TerraformVersion",
    },
)


class QuotaValidation(proto.Enum):
    r"""Enum values to control quota checks for resources in
    terraform configuration files.

    Values:
        QUOTA_VALIDATION_UNSPECIFIED (0):
            The default value.
            QuotaValidation on terraform configuration files
            will be disabled in this case.
        ENABLED (1):
            Enable computing quotas for resources in
            terraform configuration files to get visibility
            on resources with insufficient quotas.
        ENFORCED (2):
            Enforce quota checks so deployment fails if
            there isn't sufficient quotas available to
            deploy resources in terraform configuration
            files.
    """
    QUOTA_VALIDATION_UNSPECIFIED = 0
    ENABLED = 1
    ENFORCED = 2


class Deployment(proto.Message):
    r"""A Deployment is a group of resources and configs managed and
    provisioned by Infra Manager.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        terraform_blueprint (google.cloud.config_v1.types.TerraformBlueprint):
            A blueprint described using Terraform's
            HashiCorp Configuration Language as a root
            module.

            This field is a member of `oneof`_ ``blueprint``.
        name (str):
            Resource name of the deployment. Format:
            ``projects/{project}/locations/{location}/deployments/{deployment}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the deployment was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the deployment was
            last modified.
        labels (MutableMapping[str, str]):
            User-defined metadata for the deployment.
        state (google.cloud.config_v1.types.Deployment.State):
            Output only. Current state of the deployment.
        latest_revision (str):
            Output only. Revision name that was most recently applied.
            Format:
            ``projects/{project}/locations/{location}/deployments/{deployment}/ revisions/{revision}``
        state_detail (str):
            Output only. Additional information regarding
            the current state.
        error_code (google.cloud.config_v1.types.Deployment.ErrorCode):
            Output only. Error code describing errors
            that may have occurred.
        delete_results (google.cloud.config_v1.types.ApplyResults):
            Output only. Location of artifacts from a
            DeleteDeployment operation.
        delete_build (str):
            Output only. Cloud Build instance UUID
            associated with deleting this deployment.
        delete_logs (str):
            Output only. Location of Cloud Build logs in Google Cloud
            Storage, populated when deleting this deployment. Format:
            ``gs://{bucket}/{object}``.
        tf_errors (MutableSequence[google.cloud.config_v1.types.TerraformError]):
            Output only. Errors encountered when deleting this
            deployment. Errors are truncated to 10 entries, see
            ``delete_results`` and ``error_logs`` for full details.
        error_logs (str):
            Output only. Location of Terraform error logs in Google
            Cloud Storage. Format: ``gs://{bucket}/{object}``.
        artifacts_gcs_bucket (str):
            Optional. User-defined location of Cloud Build logs and
            artifacts in Google Cloud Storage. Format:
            ``gs://{bucket}/{folder}``

            A default bucket will be bootstrapped if the field is not
            set or empty. Default bucket format:
            ``gs://<project number>-<region>-blueprint-config``
            Constraints:

            -  The bucket needs to be in the same project as the
               deployment
            -  The path cannot be within the path of ``gcs_source``
            -  The field cannot be updated, including changing its
               presence

            This field is a member of `oneof`_ ``_artifacts_gcs_bucket``.
        service_account (str):
            Required. User-specified Service Account (SA) credentials to
            be used when actuating resources. Format:
            ``projects/{projectID}/serviceAccounts/{serviceAccount}``

            This field is a member of `oneof`_ ``_service_account``.
        import_existing_resources (bool):
            By default, Infra Manager will return a
            failure when Terraform encounters a 409 code
            (resource conflict error) during actuation. If
            this flag is set to true, Infra Manager will
            instead attempt to automatically import the
            resource into the Terraform state (for supported
            resource types) and continue actuation.

            Not all resource types are supported, refer to
            documentation.

            This field is a member of `oneof`_ ``_import_existing_resources``.
        worker_pool (str):
            Optional. The user-specified Cloud Build worker pool
            resource in which the Cloud Build job will execute. Format:
            ``projects/{project}/locations/{location}/workerPools/{workerPoolId}``.
            If this field is unspecified, the default Cloud Build worker
            pool will be used.

            This field is a member of `oneof`_ ``_worker_pool``.
        lock_state (google.cloud.config_v1.types.Deployment.LockState):
            Output only. Current lock state of the
            deployment.
        tf_version_constraint (str):
            Optional. The user-specified Terraform
            version constraint. Example: "=1.3.10".

            This field is a member of `oneof`_ ``_tf_version_constraint``.
        tf_version (str):
            Output only. The current Terraform version
            set on the deployment. It is in the format of
            "Major.Minor.Patch", for example, "1.3.10".
        quota_validation (google.cloud.config_v1.types.QuotaValidation):
            Optional. Input to control quota checks for
            resources in terraform configuration files.
            There are limited resources on which quota
            validation applies.
        annotations (MutableMapping[str, str]):
            Optional. Arbitrary key-value metadata
            storage e.g. to help client tools identify
            deployments during automation. See
            https://google.aip.dev/148#annotations for
            details on format and size limitations.
    """

    class State(proto.Enum):
        r"""Possible states of a deployment.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            CREATING (1):
                The deployment is being created.
            ACTIVE (2):
                The deployment is healthy.
            UPDATING (3):
                The deployment is being updated.
            DELETING (4):
                The deployment is being deleted.
            FAILED (5):
                The deployment has encountered an unexpected
                error.
            SUSPENDED (6):
                The deployment is no longer being actively
                reconciled. This may be the result of recovering
                the project after deletion.
            DELETED (7):
                The deployment has been deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        UPDATING = 3
        DELETING = 4
        FAILED = 5
        SUSPENDED = 6
        DELETED = 7

    class ErrorCode(proto.Enum):
        r"""Possible errors that can occur with deployments.

        Values:
            ERROR_CODE_UNSPECIFIED (0):
                No error code was specified.
            REVISION_FAILED (1):
                The revision failed. See Revision for more
                details.
            CLOUD_BUILD_PERMISSION_DENIED (3):
                Cloud Build failed due to a permission issue.
            DELETE_BUILD_API_FAILED (5):
                Cloud Build job associated with a deployment
                deletion could not be started.
            DELETE_BUILD_RUN_FAILED (6):
                Cloud Build job associated with a deployment
                deletion was started but failed.
            BUCKET_CREATION_PERMISSION_DENIED (7):
                Cloud Storage bucket creation failed due to a
                permission issue.
            BUCKET_CREATION_FAILED (8):
                Cloud Storage bucket creation failed due to
                an issue unrelated to permissions.
        """
        ERROR_CODE_UNSPECIFIED = 0
        REVISION_FAILED = 1
        CLOUD_BUILD_PERMISSION_DENIED = 3
        DELETE_BUILD_API_FAILED = 5
        DELETE_BUILD_RUN_FAILED = 6
        BUCKET_CREATION_PERMISSION_DENIED = 7
        BUCKET_CREATION_FAILED = 8

    class LockState(proto.Enum):
        r"""Possible lock states of a deployment.

        Values:
            LOCK_STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                lock state is omitted.
            LOCKED (1):
                The deployment is locked.
            UNLOCKED (2):
                The deployment is unlocked.
            LOCKING (3):
                The deployment is being locked.
            UNLOCKING (4):
                The deployment is being unlocked.
            LOCK_FAILED (5):
                The deployment has failed to lock.
            UNLOCK_FAILED (6):
                The deployment has failed to unlock.
        """
        LOCK_STATE_UNSPECIFIED = 0
        LOCKED = 1
        UNLOCKED = 2
        LOCKING = 3
        UNLOCKING = 4
        LOCK_FAILED = 5
        UNLOCK_FAILED = 6

    terraform_blueprint: "TerraformBlueprint" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="blueprint",
        message="TerraformBlueprint",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    latest_revision: str = proto.Field(
        proto.STRING,
        number=7,
    )
    state_detail: str = proto.Field(
        proto.STRING,
        number=9,
    )
    error_code: ErrorCode = proto.Field(
        proto.ENUM,
        number=10,
        enum=ErrorCode,
    )
    delete_results: "ApplyResults" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="ApplyResults",
    )
    delete_build: str = proto.Field(
        proto.STRING,
        number=11,
    )
    delete_logs: str = proto.Field(
        proto.STRING,
        number=12,
    )
    tf_errors: MutableSequence["TerraformError"] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message="TerraformError",
    )
    error_logs: str = proto.Field(
        proto.STRING,
        number=14,
    )
    artifacts_gcs_bucket: str = proto.Field(
        proto.STRING,
        number=15,
        optional=True,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=16,
        optional=True,
    )
    import_existing_resources: bool = proto.Field(
        proto.BOOL,
        number=17,
        optional=True,
    )
    worker_pool: str = proto.Field(
        proto.STRING,
        number=19,
        optional=True,
    )
    lock_state: LockState = proto.Field(
        proto.ENUM,
        number=20,
        enum=LockState,
    )
    tf_version_constraint: str = proto.Field(
        proto.STRING,
        number=21,
        optional=True,
    )
    tf_version: str = proto.Field(
        proto.STRING,
        number=22,
    )
    quota_validation: "QuotaValidation" = proto.Field(
        proto.ENUM,
        number=23,
        enum="QuotaValidation",
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=24,
    )


class TerraformBlueprint(proto.Message):
    r"""TerraformBlueprint describes the source of a Terraform root
    module which describes the resources and configs to be deployed.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_source (str):
            URI of an object in Google Cloud Storage. Format:
            ``gs://{bucket}/{object}``

            URI may also specify an object version for zipped objects.
            Format: ``gs://{bucket}/{object}#{version}``

            This field is a member of `oneof`_ ``source``.
        git_source (google.cloud.config_v1.types.GitSource):
            URI of a public Git repo.

            This field is a member of `oneof`_ ``source``.
        input_values (MutableMapping[str, google.cloud.config_v1.types.TerraformVariable]):
            Input variable values for the Terraform
            blueprint.
    """

    gcs_source: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="source",
    )
    git_source: "GitSource" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message="GitSource",
    )
    input_values: MutableMapping[str, "TerraformVariable"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=4,
        message="TerraformVariable",
    )


class TerraformVariable(proto.Message):
    r"""A Terraform input variable.

    Attributes:
        input_value (google.protobuf.struct_pb2.Value):
            Input variable value.
    """

    input_value: struct_pb2.Value = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Value,
    )


class ApplyResults(proto.Message):
    r"""Outputs and artifacts from applying a deployment.

    Attributes:
        content (str):
            Location of a blueprint copy and other manifests in Google
            Cloud Storage. Format: ``gs://{bucket}/{object}``
        artifacts (str):
            Location of artifacts (e.g. logs) in Google Cloud Storage.
            Format: ``gs://{bucket}/{object}``
        outputs (MutableMapping[str, google.cloud.config_v1.types.TerraformOutput]):
            Map of output name to output info.
    """

    content: str = proto.Field(
        proto.STRING,
        number=1,
    )
    artifacts: str = proto.Field(
        proto.STRING,
        number=2,
    )
    outputs: MutableMapping[str, "TerraformOutput"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=3,
        message="TerraformOutput",
    )


class TerraformOutput(proto.Message):
    r"""Describes a Terraform output.

    Attributes:
        sensitive (bool):
            Identifies whether Terraform has set this
            output as a potential sensitive value.
        value (google.protobuf.struct_pb2.Value):
            Value of output.
    """

    sensitive: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    value: struct_pb2.Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Value,
    )


class ListDeploymentsRequest(proto.Message):
    r"""

    Attributes:
        parent (str):
            Required. The parent in whose context the Deployments are
            listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}'.
        page_size (int):
            When requesting a page of resources, 'page_size' specifies
            number of resources to return. If unspecified, at most 500
            will be returned. The maximum value is 1000.
        page_token (str):
            Token returned by previous call to
            'ListDeployments' which specifies the position
            in the list from where to continue listing the
            resources.
        filter (str):
            Lists the Deployments that match the filter expression. A
            filter expression filters the resources listed in the
            response. The expression must be of the form '{field}
            {operator} {value}' where operators: '<', '>', '<=', '>=',
            '!=', '=', ':' are supported (colon ':' represents a HAS
            operator which is roughly synonymous with equality). {field}
            can refer to a proto or JSON field, or a synthetic field.
            Field names can be camelCase or snake_case.

            Examples:

            -  Filter by name: name =
               "projects/foo/locations/us-central1/deployments/bar

            -  Filter by labels:

               -  Resources that have a key called 'foo' labels.foo:\*
               -  Resources that have a key called 'foo' whose value is
                  'bar' labels.foo = bar

            -  Filter by state:

               -  Deployments in CREATING state. state=CREATING
        order_by (str):
            Field to use to sort the list.
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


class ListDeploymentsResponse(proto.Message):
    r"""

    Attributes:
        deployments (MutableSequence[google.cloud.config_v1.types.Deployment]):
            List of [Deployment][google.cloud.config.v1.Deployment]s.
        next_page_token (str):
            Token to be supplied to the next ListDeployments request via
            ``page_token`` to obtain the next set of results.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    deployments: MutableSequence["Deployment"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Deployment",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetDeploymentRequest(proto.Message):
    r"""

    Attributes:
        name (str):
            Required. The name of the deployment. Format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListRevisionsRequest(proto.Message):
    r"""A request to list Revisions passed to a 'ListRevisions' call.

    Attributes:
        parent (str):
            Required. The parent in whose context the Revisions are
            listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
        page_size (int):
            When requesting a page of resources, ``page_size`` specifies
            number of resources to return. If unspecified, at most 500
            will be returned. The maximum value is 1000.
        page_token (str):
            Token returned by previous call to
            'ListRevisions' which specifies the position in
            the list from where to continue listing the
            resources.
        filter (str):
            Lists the Revisions that match the filter expression. A
            filter expression filters the resources listed in the
            response. The expression must be of the form '{field}
            {operator} {value}' where operators: '<', '>', '<=', '>=',
            '!=', '=', ':' are supported (colon ':' represents a HAS
            operator which is roughly synonymous with equality). {field}
            can refer to a proto or JSON field, or a synthetic field.
            Field names can be camelCase or snake_case.

            Examples:

            -  Filter by name: name =
               "projects/foo/locations/us-central1/deployments/dep/revisions/bar

            -  Filter by labels:

               -  Resources that have a key called 'foo' labels.foo:\*
               -  Resources that have a key called 'foo' whose value is
                  'bar' labels.foo = bar

            -  Filter by state:

               -  Revisions in CREATING state. state=CREATING
        order_by (str):
            Field to use to sort the list.
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


class ListRevisionsResponse(proto.Message):
    r"""A response to a 'ListRevisions' call. Contains a list of
    Revisions.

    Attributes:
        revisions (MutableSequence[google.cloud.config_v1.types.Revision]):
            List of [Revision][google.cloud.config.v1.Revision]s.
        next_page_token (str):
            A token to request the next page of resources
            from the 'ListRevisions' method. The value of an
            empty string means that there are no more
            resources to return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    revisions: MutableSequence["Revision"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Revision",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetRevisionRequest(proto.Message):
    r"""A request to get a Revision from a 'GetRevision' call.

    Attributes:
        name (str):
            Required. The name of the Revision in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}/revisions/{revision}'.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateDeploymentRequest(proto.Message):
    r"""

    Attributes:
        parent (str):
            Required. The parent in whose context the Deployment is
            created. The parent value is in the format:
            'projects/{project_id}/locations/{location}'.
        deployment_id (str):
            Required. The Deployment ID.
        deployment (google.cloud.config_v1.types.Deployment):
            Required. [Deployment][google.cloud.config.v1.Deployment]
            resource to be created.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    deployment_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    deployment: "Deployment" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Deployment",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateDeploymentRequest(proto.Message):
    r"""

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask used to specify the fields to be
            overwritten in the Deployment resource by the update.

            The fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        deployment (google.cloud.config_v1.types.Deployment):
            Required. [Deployment][google.cloud.config.v1.Deployment] to
            update.

            The deployment's ``name`` field is used to identify the
            resource to be updated. Format:
            ``projects/{project}/locations/{location}/deployments/{deployment}``
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    deployment: "Deployment" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Deployment",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteDeploymentRequest(proto.Message):
    r"""

    Attributes:
        name (str):
            Required. The name of the Deployment in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        force (bool):
            Optional. If set to true, any revisions for
            this deployment will also be deleted.
            (Otherwise, the request will only work if the
            deployment has no revisions.)
        delete_policy (google.cloud.config_v1.types.DeleteDeploymentRequest.DeletePolicy):
            Optional. Policy on how resources actuated by
            the deployment should be deleted. If
            unspecified, the default behavior is to delete
            the underlying resources.
    """

    class DeletePolicy(proto.Enum):
        r"""Policy on how resources actuated by the deployment should be
        deleted.

        Values:
            DELETE_POLICY_UNSPECIFIED (0):
                Unspecified policy, resources will be
                deleted.
            DELETE (1):
                Deletes resources actuated by the deployment.
            ABANDON (2):
                Abandons resources and only deletes the
                deployment and its metadata.
        """
        DELETE_POLICY_UNSPECIFIED = 0
        DELETE = 1
        ABANDON = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    delete_policy: DeletePolicy = proto.Field(
        proto.ENUM,
        number=4,
        enum=DeletePolicy,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        deployment_metadata (google.cloud.config_v1.types.DeploymentOperationMetadata):
            Output only. Metadata about the deployment
            operation state.

            This field is a member of `oneof`_ ``resource_metadata``.
        preview_metadata (google.cloud.config_v1.types.PreviewOperationMetadata):
            Output only. Metadata about the preview
            operation state.

            This field is a member of `oneof`_ ``resource_metadata``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the operation finished
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
            successfully been cancelled have
            [google.longrunning.Operation.error][google.longrunning.Operation.error]
            value with a
            [google.rpc.Status.code][google.rpc.Status.code] of ``1``,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    deployment_metadata: "DeploymentOperationMetadata" = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="resource_metadata",
        message="DeploymentOperationMetadata",
    )
    preview_metadata: "PreviewOperationMetadata" = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="resource_metadata",
        message="PreviewOperationMetadata",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class Revision(proto.Message):
    r"""A child resource of a Deployment generated by a
    'CreateDeployment' or 'UpdateDeployment' call. Each Revision
    contains metadata pertaining to a snapshot of a particular
    Deployment.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        terraform_blueprint (google.cloud.config_v1.types.TerraformBlueprint):
            Output only. A blueprint described using
            Terraform's HashiCorp Configuration Language as
            a root module.

            This field is a member of `oneof`_ ``blueprint``.
        name (str):
            Revision name. Format:
            ``projects/{project}/locations/{location}/deployments/{deployment}/ revisions/{revision}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the revision was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the revision was last
            modified.
        action (google.cloud.config_v1.types.Revision.Action):
            Output only. The action which created this
            revision
        state (google.cloud.config_v1.types.Revision.State):
            Output only. Current state of the revision.
        apply_results (google.cloud.config_v1.types.ApplyResults):
            Output only. Outputs and artifacts from
            applying a deployment.
        state_detail (str):
            Output only. Additional info regarding the
            current state.
        error_code (google.cloud.config_v1.types.Revision.ErrorCode):
            Output only. Code describing any errors that
            may have occurred.
        build (str):
            Output only. Cloud Build instance UUID
            associated with this revision.
        logs (str):
            Output only. Location of Revision operation logs in
            ``gs://{bucket}/{object}`` format.
        tf_errors (MutableSequence[google.cloud.config_v1.types.TerraformError]):
            Output only. Errors encountered when creating or updating
            this deployment. Errors are truncated to 10 entries, see
            ``delete_results`` and ``error_logs`` for full details.
        error_logs (str):
            Output only. Location of Terraform error logs in Google
            Cloud Storage. Format: ``gs://{bucket}/{object}``.
        service_account (str):
            Output only. User-specified Service Account (SA) to be used
            as credential to manage resources. Format:
            ``projects/{projectID}/serviceAccounts/{serviceAccount}``
        import_existing_resources (bool):
            Output only. By default, Infra Manager will
            return a failure when Terraform encounters a 409
            code (resource conflict error) during actuation.
            If this flag is set to true, Infra Manager will
            instead attempt to automatically import the
            resource into the Terraform state (for supported
            resource types) and continue actuation.

            Not all resource types are supported, refer to
            documentation.
        worker_pool (str):
            Output only. The user-specified Cloud Build worker pool
            resource in which the Cloud Build job will execute. Format:
            ``projects/{project}/locations/{location}/workerPools/{workerPoolId}``.
            If this field is unspecified, the default Cloud Build worker
            pool will be used.
        tf_version_constraint (str):
            Output only. The user-specified Terraform
            version constraint. Example: "=1.3.10".
        tf_version (str):
            Output only. The version of Terraform used to
            create the Revision. It is in the format of
            "Major.Minor.Patch", for example, "1.3.10".
        quota_validation_results (str):
            Output only. Cloud Storage path containing quota validation
            results. This field is set when a user sets
            Deployment.quota_validation field to ENABLED or ENFORCED.
            Format: ``gs://{bucket}/{object}``.
        quota_validation (google.cloud.config_v1.types.QuotaValidation):
            Optional. Input to control quota checks for
            resources in terraform configuration files.
            There are limited resources on which quota
            validation applies.
    """

    class Action(proto.Enum):
        r"""Actions that generate a revision.

        Values:
            ACTION_UNSPECIFIED (0):
                The default value. This value is used if the
                action is omitted.
            CREATE (1):
                The revision was generated by creating a
                deployment.
            UPDATE (2):
                The revision was generated by updating a
                deployment.
            DELETE (3):
                The revision was deleted.
        """
        ACTION_UNSPECIFIED = 0
        CREATE = 1
        UPDATE = 2
        DELETE = 3

    class State(proto.Enum):
        r"""Possible states of a revision.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            APPLYING (1):
                The revision is being applied.
            APPLIED (2):
                The revision was applied successfully.
            FAILED (3):
                The revision could not be applied
                successfully.
        """
        STATE_UNSPECIFIED = 0
        APPLYING = 1
        APPLIED = 2
        FAILED = 3

    class ErrorCode(proto.Enum):
        r"""Possible errors if Revision could not be created or updated
        successfully.

        Values:
            ERROR_CODE_UNSPECIFIED (0):
                No error code was specified.
            CLOUD_BUILD_PERMISSION_DENIED (1):
                Cloud Build failed due to a permission issue.
            APPLY_BUILD_API_FAILED (4):
                Cloud Build job associated with creating or
                updating a deployment could not be started.
            APPLY_BUILD_RUN_FAILED (5):
                Cloud Build job associated with creating or
                updating a deployment was started but failed.
            QUOTA_VALIDATION_FAILED (7):
                quota validation failed for one or more
                resources in terraform configuration files.
        """
        ERROR_CODE_UNSPECIFIED = 0
        CLOUD_BUILD_PERMISSION_DENIED = 1
        APPLY_BUILD_API_FAILED = 4
        APPLY_BUILD_RUN_FAILED = 5
        QUOTA_VALIDATION_FAILED = 7

    terraform_blueprint: "TerraformBlueprint" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="blueprint",
        message="TerraformBlueprint",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    action: Action = proto.Field(
        proto.ENUM,
        number=4,
        enum=Action,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )
    apply_results: "ApplyResults" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="ApplyResults",
    )
    state_detail: str = proto.Field(
        proto.STRING,
        number=8,
    )
    error_code: ErrorCode = proto.Field(
        proto.ENUM,
        number=9,
        enum=ErrorCode,
    )
    build: str = proto.Field(
        proto.STRING,
        number=10,
    )
    logs: str = proto.Field(
        proto.STRING,
        number=11,
    )
    tf_errors: MutableSequence["TerraformError"] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message="TerraformError",
    )
    error_logs: str = proto.Field(
        proto.STRING,
        number=13,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=14,
    )
    import_existing_resources: bool = proto.Field(
        proto.BOOL,
        number=15,
    )
    worker_pool: str = proto.Field(
        proto.STRING,
        number=17,
    )
    tf_version_constraint: str = proto.Field(
        proto.STRING,
        number=18,
    )
    tf_version: str = proto.Field(
        proto.STRING,
        number=19,
    )
    quota_validation_results: str = proto.Field(
        proto.STRING,
        number=29,
    )
    quota_validation: "QuotaValidation" = proto.Field(
        proto.ENUM,
        number=20,
        enum="QuotaValidation",
    )


class TerraformError(proto.Message):
    r"""Errors encountered during actuation using Terraform

    Attributes:
        resource_address (str):
            Address of the resource associated with the error, e.g.
            ``google_compute_network.vpc_network``.
        http_response_code (int):
            HTTP response code returned from Google Cloud
            Platform APIs when Terraform fails to provision
            the resource. If unset or 0, no HTTP response
            code was returned by Terraform.
        error_description (str):
            A human-readable error description.
        error (google.rpc.status_pb2.Status):
            Original error response from underlying
            Google API, if available.
    """

    resource_address: str = proto.Field(
        proto.STRING,
        number=1,
    )
    http_response_code: int = proto.Field(
        proto.INT32,
        number=2,
    )
    error_description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=4,
        message=status_pb2.Status,
    )


class GitSource(proto.Message):
    r"""A set of files in a Git repository.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        repo (str):
            Optional. Repository URL.
            Example:
            'https://github.com/kubernetes/examples.git'

            This field is a member of `oneof`_ ``_repo``.
        directory (str):
            Optional. Subdirectory inside the repository.
            Example: 'staging/my-package'

            This field is a member of `oneof`_ ``_directory``.
        ref (str):
            Optional. Git reference (e.g. branch or tag).

            This field is a member of `oneof`_ ``_ref``.
    """

    repo: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    directory: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    ref: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )


class DeploymentOperationMetadata(proto.Message):
    r"""Ephemeral metadata content describing the state of a
    deployment operation.

    Attributes:
        step (google.cloud.config_v1.types.DeploymentOperationMetadata.DeploymentStep):
            The current step the deployment operation is
            running.
        apply_results (google.cloud.config_v1.types.ApplyResults):
            Outputs and artifacts from applying a
            deployment.
        build (str):
            Output only. Cloud Build instance UUID
            associated with this operation.
        logs (str):
            Output only. Location of Deployment operations logs in
            ``gs://{bucket}/{object}`` format.
    """

    class DeploymentStep(proto.Enum):
        r"""The possible steps a deployment may be running.

        Values:
            DEPLOYMENT_STEP_UNSPECIFIED (0):
                Unspecified deployment step
            PREPARING_STORAGE_BUCKET (1):
                Infra Manager is creating a Google Cloud
                Storage bucket to store artifacts and metadata
                about the deployment and revision
            DOWNLOADING_BLUEPRINT (2):
                Downloading the blueprint onto the Google
                Cloud Storage bucket
            RUNNING_TF_INIT (3):
                Initializing Terraform using ``terraform init``
            RUNNING_TF_PLAN (4):
                Running ``terraform plan``
            RUNNING_TF_APPLY (5):
                Actuating resources using Terraform using
                ``terraform apply``
            RUNNING_TF_DESTROY (6):
                Destroying resources using Terraform using
                ``terraform destroy``
            RUNNING_TF_VALIDATE (7):
                Validating the uploaded TF state file when
                unlocking a deployment
            UNLOCKING_DEPLOYMENT (8):
                Unlocking a deployment
            SUCCEEDED (9):
                Operation was successful
            FAILED (10):
                Operation failed
            VALIDATING_REPOSITORY (11):
                Validating the provided repository.
            RUNNING_QUOTA_VALIDATION (12):
                Running quota validation
        """
        DEPLOYMENT_STEP_UNSPECIFIED = 0
        PREPARING_STORAGE_BUCKET = 1
        DOWNLOADING_BLUEPRINT = 2
        RUNNING_TF_INIT = 3
        RUNNING_TF_PLAN = 4
        RUNNING_TF_APPLY = 5
        RUNNING_TF_DESTROY = 6
        RUNNING_TF_VALIDATE = 7
        UNLOCKING_DEPLOYMENT = 8
        SUCCEEDED = 9
        FAILED = 10
        VALIDATING_REPOSITORY = 11
        RUNNING_QUOTA_VALIDATION = 12

    step: DeploymentStep = proto.Field(
        proto.ENUM,
        number=1,
        enum=DeploymentStep,
    )
    apply_results: "ApplyResults" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ApplyResults",
    )
    build: str = proto.Field(
        proto.STRING,
        number=3,
    )
    logs: str = proto.Field(
        proto.STRING,
        number=4,
    )


class Resource(proto.Message):
    r"""Resource represents a Google Cloud Platform resource actuated
    by IM. Resources are child resources of Revisions.

    Attributes:
        name (str):
            Output only. Resource name. Format:
            ``projects/{project}/locations/{location}/deployments/{deployment}/revisions/{revision}/resources/{resource}``
        terraform_info (google.cloud.config_v1.types.ResourceTerraformInfo):
            Output only. Terraform-specific info if this
            resource was created using Terraform.
        cai_assets (MutableMapping[str, google.cloud.config_v1.types.ResourceCAIInfo]):
            Output only. Map of Cloud Asset Inventory
            (CAI) type to CAI info (e.g. CAI ID). CAI type
            format follows
            https://cloud.google.com/asset-inventory/docs/supported-asset-types
        intent (google.cloud.config_v1.types.Resource.Intent):
            Output only. Intent of the resource.
        state (google.cloud.config_v1.types.Resource.State):
            Output only. Current state of the resource.
    """

    class Intent(proto.Enum):
        r"""Possible intent of the resource.

        Values:
            INTENT_UNSPECIFIED (0):
                The default value. This value is used if the
                intent is omitted.
            CREATE (1):
                Infra Manager will create this Resource.
            UPDATE (2):
                Infra Manager will update this Resource.
            DELETE (3):
                Infra Manager will delete this Resource.
            RECREATE (4):
                Infra Manager will destroy and recreate this
                Resource.
            UNCHANGED (5):
                Infra Manager will leave this Resource
                untouched.
        """
        INTENT_UNSPECIFIED = 0
        CREATE = 1
        UPDATE = 2
        DELETE = 3
        RECREATE = 4
        UNCHANGED = 5

    class State(proto.Enum):
        r"""Possible states of a resource.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            PLANNED (1):
                Resource has been planned for reconcile.
            IN_PROGRESS (2):
                Resource is actively reconciling into the
                intended state.
            RECONCILED (3):
                Resource has reconciled to intended state.
            FAILED (4):
                Resource failed to reconcile.
        """
        STATE_UNSPECIFIED = 0
        PLANNED = 1
        IN_PROGRESS = 2
        RECONCILED = 3
        FAILED = 4

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    terraform_info: "ResourceTerraformInfo" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ResourceTerraformInfo",
    )
    cai_assets: MutableMapping[str, "ResourceCAIInfo"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=3,
        message="ResourceCAIInfo",
    )
    intent: Intent = proto.Field(
        proto.ENUM,
        number=4,
        enum=Intent,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        enum=State,
    )


class ResourceTerraformInfo(proto.Message):
    r"""Terraform info of a Resource.

    Attributes:
        address (str):
            TF resource address that uniquely identifies
            this resource within this deployment.
        type_ (str):
            TF resource type
        id (str):
            ID attribute of the TF resource
    """

    address: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )
    id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ResourceCAIInfo(proto.Message):
    r"""CAI info of a Resource.

    Attributes:
        full_resource_name (str):
            CAI resource name in the format following
            https://cloud.google.com/apis/design/resource_names#full_resource_name
    """

    full_resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetResourceRequest(proto.Message):
    r"""A request to get a Resource from a 'GetResource' call.

    Attributes:
        name (str):
            Required. The name of the Resource in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}/revisions/{revision}/resource/{resource}'.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListResourcesRequest(proto.Message):
    r"""A request to list Resources passed to a 'ListResources' call.

    Attributes:
        parent (str):
            Required. The parent in whose context the Resources are
            listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}/revisions/{revision}'.
        page_size (int):
            When requesting a page of resources, 'page_size' specifies
            number of resources to return. If unspecified, at most 500
            will be returned. The maximum value is 1000.
        page_token (str):
            Token returned by previous call to
            'ListResources' which specifies the position in
            the list from where to continue listing the
            resources.
        filter (str):
            Lists the Resources that match the filter expression. A
            filter expression filters the resources listed in the
            response. The expression must be of the form '{field}
            {operator} {value}' where operators: '<', '>', '<=', '>=',
            '!=', '=', ':' are supported (colon ':' represents a HAS
            operator which is roughly synonymous with equality). {field}
            can refer to a proto or JSON field, or a synthetic field.
            Field names can be camelCase or snake_case.

            Examples:

            -  Filter by name: name =
               "projects/foo/locations/us-central1/deployments/dep/revisions/bar/resources/baz
        order_by (str):
            Field to use to sort the list.
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


class ListResourcesResponse(proto.Message):
    r"""A response to a 'ListResources' call. Contains a list of
    Resources.

    Attributes:
        resources (MutableSequence[google.cloud.config_v1.types.Resource]):
            List of [Resources][google.cloud.config.v1.Resource].
        next_page_token (str):
            A token to request the next page of resources
            from the 'ListResources' method. The value of an
            empty string means that there are no more
            resources to return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    resources: MutableSequence["Resource"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Resource",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class Statefile(proto.Message):
    r"""Contains info about a Terraform state file

    Attributes:
        signed_uri (str):
            Output only. Cloud Storage signed URI used
            for downloading or uploading the state file.
    """

    signed_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ExportDeploymentStatefileRequest(proto.Message):
    r"""A request to export a state file passed to a
    'ExportDeploymentStatefile' call.

    Attributes:
        parent (str):
            Required. The parent in whose context the statefile is
            listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
        draft (bool):
            Optional. If this flag is set to true, the
            exported deployment state file will be the draft
            state. This will enable the draft file to be
            validated before copying it over to the working
            state on unlock.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    draft: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class ExportRevisionStatefileRequest(proto.Message):
    r"""A request to export a state file passed to a
    'ExportRevisionStatefile' call.

    Attributes:
        parent (str):
            Required. The parent in whose context the statefile is
            listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}/revisions/{revision}'.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ImportStatefileRequest(proto.Message):
    r"""A request to import a state file passed to a
    'ImportStatefile' call.

    Attributes:
        parent (str):
            Required. The parent in whose context the statefile is
            listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
        lock_id (int):
            Required. Lock ID of the lock file to verify
            that the user who is importing the state file
            previously locked the Deployment.
        skip_draft (bool):
            Optional.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lock_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    skip_draft: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteStatefileRequest(proto.Message):
    r"""A request to delete a state file passed to a
    'DeleteStatefile' call.

    Attributes:
        name (str):
            Required. The name of the deployment in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
        lock_id (int):
            Required. Lock ID of the lock file to verify
            that the user who is deleting the state file
            previously locked the Deployment.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lock_id: int = proto.Field(
        proto.INT64,
        number=2,
    )


class LockDeploymentRequest(proto.Message):
    r"""A request to lock a deployment passed to a 'LockDeployment'
    call.

    Attributes:
        name (str):
            Required. The name of the deployment in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UnlockDeploymentRequest(proto.Message):
    r"""A request to unlock a state file passed to a
    'UnlockDeployment' call.

    Attributes:
        name (str):
            Required. The name of the deployment in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
        lock_id (int):
            Required. Lock ID of the lock file to be
            unlocked.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lock_id: int = proto.Field(
        proto.INT64,
        number=2,
    )


class ExportLockInfoRequest(proto.Message):
    r"""A request to get a state file lock info passed to a
    'ExportLockInfo' call.

    Attributes:
        name (str):
            Required. The name of the deployment in the format:
            'projects/{project_id}/locations/{location}/deployments/{deployment}'.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class LockInfo(proto.Message):
    r"""Details about the lock which locked the deployment.

    Attributes:
        lock_id (int):
            Unique ID for the lock to be overridden with
            generation ID in the backend.
        operation (str):
            Terraform operation, provided by the caller.
        info (str):
            Extra information to store with the lock,
            provided by the caller.
        who (str):
            user@hostname when available
        version (str):
            Terraform version
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Time that the lock was taken.
    """

    lock_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    operation: str = proto.Field(
        proto.STRING,
        number=2,
    )
    info: str = proto.Field(
        proto.STRING,
        number=3,
    )
    who: str = proto.Field(
        proto.STRING,
        number=4,
    )
    version: str = proto.Field(
        proto.STRING,
        number=5,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )


class Preview(proto.Message):
    r"""A preview represents a set of actions Infra Manager would
    perform to move the resources towards the desired state as
    specified in the configuration.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        terraform_blueprint (google.cloud.config_v1.types.TerraformBlueprint):
            The terraform blueprint to preview.

            This field is a member of `oneof`_ ``blueprint``.
        name (str):
            Identifier. Resource name of the preview. Resource name can
            be user provided or server generated ID if unspecified.
            Format:
            ``projects/{project}/locations/{location}/previews/{preview}``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time the preview was created.
        labels (MutableMapping[str, str]):
            Optional. User-defined labels for the
            preview.
        state (google.cloud.config_v1.types.Preview.State):
            Output only. Current state of the preview.
        deployment (str):
            Optional. Optional deployment reference. If
            specified, the preview will be performed using
            the provided deployment's current state and use
            any relevant fields from the deployment unless
            explicitly specified in the preview create
            request.
        preview_mode (google.cloud.config_v1.types.Preview.PreviewMode):
            Optional. Current mode of preview.
        service_account (str):
            Required. User-specified Service Account (SA) credentials to
            be used when previewing resources. Format:
            ``projects/{projectID}/serviceAccounts/{serviceAccount}``
        artifacts_gcs_bucket (str):
            Optional. User-defined location of Cloud Build logs,
            artifacts, and in Google Cloud Storage. Format:
            ``gs://{bucket}/{folder}`` A default bucket will be
            bootstrapped if the field is not set or empty Default Bucket
            Format: ``gs://<project number>-<region>-blueprint-config``
            Constraints:

            -  The bucket needs to be in the same project as the
               deployment
            -  The path cannot be within the path of ``gcs_source`` If
               omitted and deployment resource ref provided has
               artifacts_gcs_bucket defined, that artifact bucket is
               used.

            This field is a member of `oneof`_ ``_artifacts_gcs_bucket``.
        worker_pool (str):
            Optional. The user-specified Worker Pool resource in which
            the Cloud Build job will execute. Format
            projects/{project}/locations/{location}/workerPools/{workerPoolId}
            If this field is unspecified, the default Cloud Build worker
            pool will be used. If omitted and deployment resource ref
            provided has worker_pool defined, that worker pool is used.

            This field is a member of `oneof`_ ``_worker_pool``.
        error_code (google.cloud.config_v1.types.Preview.ErrorCode):
            Output only. Code describing any errors that
            may have occurred.
        error_status (google.rpc.status_pb2.Status):
            Output only. Additional information regarding
            the current state.
        build (str):
            Output only. Cloud Build instance UUID
            associated with this preview.
        tf_errors (MutableSequence[google.cloud.config_v1.types.TerraformError]):
            Output only. Summary of errors encountered
            during Terraform preview. It has a size limit of
            10, i.e. only top 10 errors will be summarized
            here.
        error_logs (str):
            Output only. Link to tf-error.ndjson file, which contains
            the full list of the errors encountered during a Terraform
            preview. Format: ``gs://{bucket}/{object}``.
        preview_artifacts (google.cloud.config_v1.types.PreviewArtifacts):
            Output only. Artifacts from preview.
        logs (str):
            Output only. Location of preview logs in
            ``gs://{bucket}/{object}`` format.
        tf_version (str):
            Output only. The current Terraform version
            set on the preview. It is in the format of
            "Major.Minor.Patch", for example, "1.3.10".
        tf_version_constraint (str):
            Optional. The user-specified Terraform
            version constraint. Example: "=1.3.10".

            This field is a member of `oneof`_ ``_tf_version_constraint``.
        annotations (MutableMapping[str, str]):
            Optional. Arbitrary key-value metadata
            storage e.g. to help client tools identifiy
            preview during automation. See
            https://google.aip.dev/148#annotations for
            details on format and size limitations.
    """

    class State(proto.Enum):
        r"""Possible states of a preview.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is unknown.
            CREATING (1):
                The preview is being created.
            SUCCEEDED (2):
                The preview has succeeded.
            APPLYING (3):
                The preview is being applied.
            STALE (4):
                The preview is stale. A preview can become
                stale if a revision has been applied after this
                preview was created.
            DELETING (5):
                The preview is being deleted.
            FAILED (6):
                The preview has encountered an unexpected
                error.
            DELETED (7):
                The preview has been deleted.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        SUCCEEDED = 2
        APPLYING = 3
        STALE = 4
        DELETING = 5
        FAILED = 6
        DELETED = 7

    class PreviewMode(proto.Enum):
        r"""Preview mode provides options for customizing preview
        operations.

        Values:
            PREVIEW_MODE_UNSPECIFIED (0):
                Unspecified policy, default mode will be
                used.
            DEFAULT (1):
                DEFAULT mode generates an execution plan for
                reconciling current resource state into expected
                resource state.
            DELETE (2):
                DELETE mode generates as execution plan for
                destroying current resources.
        """
        PREVIEW_MODE_UNSPECIFIED = 0
        DEFAULT = 1
        DELETE = 2

    class ErrorCode(proto.Enum):
        r"""Possible errors that can occur with previews.

        Values:
            ERROR_CODE_UNSPECIFIED (0):
                No error code was specified.
            CLOUD_BUILD_PERMISSION_DENIED (1):
                Cloud Build failed due to a permissions
                issue.
            BUCKET_CREATION_PERMISSION_DENIED (2):
                Cloud Storage bucket failed to create due to
                a permissions issue.
            BUCKET_CREATION_FAILED (3):
                Cloud Storage bucket failed for a
                non-permissions-related issue.
            DEPLOYMENT_LOCK_ACQUIRE_FAILED (4):
                Acquiring lock on provided deployment
                reference failed.
            PREVIEW_BUILD_API_FAILED (5):
                Preview encountered an error when trying to
                access Cloud Build API.
            PREVIEW_BUILD_RUN_FAILED (6):
                Preview created a build but build failed and
                logs were generated.
        """
        ERROR_CODE_UNSPECIFIED = 0
        CLOUD_BUILD_PERMISSION_DENIED = 1
        BUCKET_CREATION_PERMISSION_DENIED = 2
        BUCKET_CREATION_FAILED = 3
        DEPLOYMENT_LOCK_ACQUIRE_FAILED = 4
        PREVIEW_BUILD_API_FAILED = 5
        PREVIEW_BUILD_RUN_FAILED = 6

    terraform_blueprint: "TerraformBlueprint" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="blueprint",
        message="TerraformBlueprint",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    deployment: str = proto.Field(
        proto.STRING,
        number=5,
    )
    preview_mode: PreviewMode = proto.Field(
        proto.ENUM,
        number=15,
        enum=PreviewMode,
    )
    service_account: str = proto.Field(
        proto.STRING,
        number=7,
    )
    artifacts_gcs_bucket: str = proto.Field(
        proto.STRING,
        number=8,
        optional=True,
    )
    worker_pool: str = proto.Field(
        proto.STRING,
        number=9,
        optional=True,
    )
    error_code: ErrorCode = proto.Field(
        proto.ENUM,
        number=10,
        enum=ErrorCode,
    )
    error_status: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=11,
        message=status_pb2.Status,
    )
    build: str = proto.Field(
        proto.STRING,
        number=12,
    )
    tf_errors: MutableSequence["TerraformError"] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message="TerraformError",
    )
    error_logs: str = proto.Field(
        proto.STRING,
        number=14,
    )
    preview_artifacts: "PreviewArtifacts" = proto.Field(
        proto.MESSAGE,
        number=16,
        message="PreviewArtifacts",
    )
    logs: str = proto.Field(
        proto.STRING,
        number=17,
    )
    tf_version: str = proto.Field(
        proto.STRING,
        number=18,
    )
    tf_version_constraint: str = proto.Field(
        proto.STRING,
        number=19,
        optional=True,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=20,
    )


class PreviewOperationMetadata(proto.Message):
    r"""Ephemeral metadata content describing the state of a preview
    operation.

    Attributes:
        step (google.cloud.config_v1.types.PreviewOperationMetadata.PreviewStep):
            The current step the preview operation is
            running.
        preview_artifacts (google.cloud.config_v1.types.PreviewArtifacts):
            Artifacts from preview.
        logs (str):
            Output only. Location of preview logs in
            ``gs://{bucket}/{object}`` format.
        build (str):
            Output only. Cloud Build instance UUID
            associated with this preview.
    """

    class PreviewStep(proto.Enum):
        r"""The possible steps a preview may be running.

        Values:
            PREVIEW_STEP_UNSPECIFIED (0):
                Unspecified preview step.
            PREPARING_STORAGE_BUCKET (1):
                Infra Manager is creating a Google Cloud
                Storage bucket to store artifacts and metadata
                about the preview.
            DOWNLOADING_BLUEPRINT (2):
                Downloading the blueprint onto the Google
                Cloud Storage bucket.
            RUNNING_TF_INIT (3):
                Initializing Terraform using ``terraform init``.
            RUNNING_TF_PLAN (4):
                Running ``terraform plan``.
            FETCHING_DEPLOYMENT (5):
                Fetching a deployment.
            LOCKING_DEPLOYMENT (6):
                Locking a deployment.
            UNLOCKING_DEPLOYMENT (7):
                Unlocking a deployment.
            SUCCEEDED (8):
                Operation was successful.
            FAILED (9):
                Operation failed.
            VALIDATING_REPOSITORY (10):
                Validating the provided repository.
        """
        PREVIEW_STEP_UNSPECIFIED = 0
        PREPARING_STORAGE_BUCKET = 1
        DOWNLOADING_BLUEPRINT = 2
        RUNNING_TF_INIT = 3
        RUNNING_TF_PLAN = 4
        FETCHING_DEPLOYMENT = 5
        LOCKING_DEPLOYMENT = 6
        UNLOCKING_DEPLOYMENT = 7
        SUCCEEDED = 8
        FAILED = 9
        VALIDATING_REPOSITORY = 10

    step: PreviewStep = proto.Field(
        proto.ENUM,
        number=1,
        enum=PreviewStep,
    )
    preview_artifacts: "PreviewArtifacts" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PreviewArtifacts",
    )
    logs: str = proto.Field(
        proto.STRING,
        number=3,
    )
    build: str = proto.Field(
        proto.STRING,
        number=4,
    )


class PreviewArtifacts(proto.Message):
    r"""Artifacts created by preview.

    Attributes:
        content (str):
            Output only. Location of a blueprint copy and other content
            in Google Cloud Storage. Format: ``gs://{bucket}/{object}``
        artifacts (str):
            Output only. Location of artifacts in Google Cloud Storage.
            Format: ``gs://{bucket}/{object}``
    """

    content: str = proto.Field(
        proto.STRING,
        number=1,
    )
    artifacts: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreatePreviewRequest(proto.Message):
    r"""A request to create a preview.

    Attributes:
        parent (str):
            Required. The parent in whose context the Preview is
            created. The parent value is in the format:
            'projects/{project_id}/locations/{location}'.
        preview_id (str):
            Optional. The preview ID.
        preview (google.cloud.config_v1.types.Preview):
            Required. [Preview][google.cloud.config.v1.Preview] resource
            to be created.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    preview_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    preview: "Preview" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Preview",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class GetPreviewRequest(proto.Message):
    r"""A request to get details about a preview.

    Attributes:
        name (str):
            Required. The name of the preview. Format:
            'projects/{project_id}/locations/{location}/previews/{preview}'.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPreviewsRequest(proto.Message):
    r"""A request to list all previews for a given project and
    location.

    Attributes:
        parent (str):
            Required. The parent in whose context the Previews are
            listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}'.
        page_size (int):
            Optional. When requesting a page of resources, 'page_size'
            specifies number of resources to return. If unspecified, at
            most 500 will be returned. The maximum value is 1000.
        page_token (str):
            Optional. Token returned by previous call to
            'ListDeployments' which specifies the position
            in the list from where to continue listing the
            resources.
        filter (str):
            Optional. Lists the Deployments that match the filter
            expression. A filter expression filters the resources listed
            in the response. The expression must be of the form '{field}
            {operator} {value}' where operators: '<', '>', '<=', '>=',
            '!=', '=', ':' are supported (colon ':' represents a HAS
            operator which is roughly synonymous with equality). {field}
            can refer to a proto or JSON field, or a synthetic field.
            Field names can be camelCase or snake_case.

            Examples:

            -  Filter by name: name =
               "projects/foo/locations/us-central1/deployments/bar

            -  Filter by labels:

               -  Resources that have a key called 'foo' labels.foo:\*
               -  Resources that have a key called 'foo' whose value is
                  'bar' labels.foo = bar

            -  Filter by state:

               -  Deployments in CREATING state. state=CREATING
        order_by (str):
            Optional. Field to use to sort the list.
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


class ListPreviewsResponse(proto.Message):
    r"""A response to a ``ListPreviews`` call. Contains a list of Previews.

    Attributes:
        previews (MutableSequence[google.cloud.config_v1.types.Preview]):
            List of [Previews][google.cloud.config.v1.Preview].
        next_page_token (str):
            Token to be supplied to the next ListPreviews request via
            ``page_token`` to obtain the next set of results.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    previews: MutableSequence["Preview"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Preview",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class DeletePreviewRequest(proto.Message):
    r"""A request to delete a preview.

    Attributes:
        name (str):
            Required. The name of the Preview in the format:
            'projects/{project_id}/locations/{location}/previews/{preview}'.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ExportPreviewResultRequest(proto.Message):
    r"""A request to export preview results.

    Attributes:
        parent (str):
            Required. The preview whose results should be exported. The
            preview value is in the format:
            'projects/{project_id}/locations/{location}/previews/{preview}'.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ExportPreviewResultResponse(proto.Message):
    r"""A response to ``ExportPreviewResult`` call. Contains preview
    results.

    Attributes:
        result (google.cloud.config_v1.types.PreviewResult):
            Output only. Signed URLs for accessing the
            plan files.
    """

    result: "PreviewResult" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PreviewResult",
    )


class PreviewResult(proto.Message):
    r"""Contains a signed Cloud Storage URLs.

    Attributes:
        binary_signed_uri (str):
            Output only. Plan binary signed URL
        json_signed_uri (str):
            Output only. Plan JSON signed URL
    """

    binary_signed_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    json_signed_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetTerraformVersionRequest(proto.Message):
    r"""The request message for the GetTerraformVersion method.

    Attributes:
        name (str):
            Required. The name of the TerraformVersion. Format:
            'projects/{project_id}/locations/{location}/terraformVersions/{terraform_version}'
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListTerraformVersionsRequest(proto.Message):
    r"""The request message for the ListTerraformVersions method.

    Attributes:
        parent (str):
            Required. The parent in whose context the TerraformVersions
            are listed. The parent value is in the format:
            'projects/{project_id}/locations/{location}'.
        page_size (int):
            Optional. When requesting a page of resources, 'page_size'
            specifies number of resources to return. If unspecified, at
            most 500 will be returned. The maximum value is 1000.
        page_token (str):
            Optional. Token returned by previous call to
            'ListTerraformVersions' which specifies the
            position in the list from where to continue
            listing the resources.
        filter (str):
            Optional. Lists the TerraformVersions that match the filter
            expression. A filter expression filters the resources listed
            in the response. The expression must be of the form '{field}
            {operator} {value}' where operators: '<', '>', '<=', '>=',
            '!=', '=', ':' are supported (colon ':' represents a HAS
            operator which is roughly synonymous with equality). {field}
            can refer to a proto or JSON field, or a synthetic field.
            Field names can be camelCase or snake_case.
        order_by (str):
            Optional. Field to use to sort the list.
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


class ListTerraformVersionsResponse(proto.Message):
    r"""The response message for the ``ListTerraformVersions`` method.

    Attributes:
        terraform_versions (MutableSequence[google.cloud.config_v1.types.TerraformVersion]):
            List of
            [TerraformVersion][google.cloud.config.v1.TerraformVersion]s.
        next_page_token (str):
            Token to be supplied to the next ListTerraformVersions
            request via ``page_token`` to obtain the next set of
            results.
        unreachable (MutableSequence[str]):
            Unreachable resources, if any.
    """

    @property
    def raw_page(self):
        return self

    terraform_versions: MutableSequence["TerraformVersion"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TerraformVersion",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class TerraformVersion(proto.Message):
    r"""A TerraformVersion represents the support state the
    corresponding Terraform version.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. The version name is in the format:
            'projects/{project_id}/locations/{location}/terraformVersions/{terraform_version}'.
        state (google.cloud.config_v1.types.TerraformVersion.State):
            Output only. The state of the version,
            ACTIVE, DEPRECATED or OBSOLETE.
        support_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the version is supported.
        deprecate_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the version is deprecated.

            This field is a member of `oneof`_ ``_deprecate_time``.
        obsolete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. When the version is obsolete.

            This field is a member of `oneof`_ ``_obsolete_time``.
    """

    class State(proto.Enum):
        r"""Possible states of a TerraformVersion.

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            ACTIVE (1):
                The version is actively supported.
            DEPRECATED (2):
                The version is deprecated.
            OBSOLETE (3):
                The version is obsolete.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        DEPRECATED = 2
        OBSOLETE = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    support_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    deprecate_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        optional=True,
        message=timestamp_pb2.Timestamp,
    )
    obsolete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        optional=True,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
