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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.cloudsecuritycompliance_v1.types import common

__protobuf__ = proto.module(
    package="google.cloud.cloudsecuritycompliance.v1",
    manifest={
        "DeploymentState",
        "FrameworkDeployment",
        "CloudControlDeployment",
        "TargetResourceConfig",
        "TargetResourceCreationConfig",
        "FolderCreationConfig",
        "ProjectCreationConfig",
        "CloudControlMetadata",
        "CreateFrameworkDeploymentRequest",
        "DeleteFrameworkDeploymentRequest",
        "GetFrameworkDeploymentRequest",
        "ListFrameworkDeploymentsRequest",
        "ListFrameworkDeploymentsResponse",
        "GetCloudControlDeploymentRequest",
        "ListCloudControlDeploymentsRequest",
        "ListCloudControlDeploymentsResponse",
        "CloudControlDeploymentReference",
        "FrameworkDeploymentReference",
    },
)


class DeploymentState(proto.Enum):
    r"""DeploymentState represents the state of the Deployment
    resource.

    Values:
        DEPLOYMENT_STATE_UNSPECIFIED (0):
            Unspecified. Invalid state.
        DEPLOYMENT_STATE_VALIDATING (1):
            Validating the deployment.
        DEPLOYMENT_STATE_CREATING (2):
            Deployment is in CREATING state.
        DEPLOYMENT_STATE_DELETING (3):
            Deployment is in DELETING state.
        DEPLOYMENT_STATE_FAILED (4):
            Deployment has failed. All the changes made
            by the deployment have been successfully rolled
            back. A deployment in the FAILED state can be
            retried or deleted.
        DEPLOYMENT_STATE_READY (5):
            Deployment is successful and ready to use.
        DEPLOYMENT_STATE_PARTIALLY_DEPLOYED (6):
            Deployment is partially deployed. All the
            Cloud Controls were not deployed successfully.
            Retrying the operation will resume from the
            first failed step.
        DEPLOYMENT_STATE_PARTIALLY_DELETED (7):
            Deployment is partially deleted. All the
            Cloud Control Deployments were not deleted
            successfully. Retrying the operation will resume
            from the first failed step.
    """
    DEPLOYMENT_STATE_UNSPECIFIED = 0
    DEPLOYMENT_STATE_VALIDATING = 1
    DEPLOYMENT_STATE_CREATING = 2
    DEPLOYMENT_STATE_DELETING = 3
    DEPLOYMENT_STATE_FAILED = 4
    DEPLOYMENT_STATE_READY = 5
    DEPLOYMENT_STATE_PARTIALLY_DEPLOYED = 6
    DEPLOYMENT_STATE_PARTIALLY_DELETED = 7


class FrameworkDeployment(proto.Message):
    r"""FrameworkDeployment represents deployment of a Framework on a
    target resource. Supported target resources are
    organizations/{organization}, folders/{folder}, and
    projects/{project}.

    Attributes:
        name (str):
            Identifier. FrameworkDeployment name in the following
            format:
            organizations/{organization}/locations/{location}/frameworkDeployments/{framework_deployment_id}
        target_resource_config (google.cloud.cloudsecuritycompliance_v1.types.TargetResourceConfig):
            Required. The details of the target resource
            on which the Framework is to be deployed. It can
            either be an existing target resource or a new
            target resource to be created.
        computed_target_resource (str):
            Output only. The resource on which the
            Framework is deployed based on the provided
            TargetResourceConfig in the following format:

            organizations/{organization}, folders/{folder}
            or projects/{project}
        framework (google.cloud.cloudsecuritycompliance_v1.types.FrameworkReference):
            Required. Reference to the framework to be
            deployed.
        description (str):
            Optional. User provided description of the
            Framework deployment
        cloud_control_metadata (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.CloudControlMetadata]):
            Required. Deployment mode and parameters for
            each of the Cloud Controls in the framework.
            Every Cloud Control in the framework must have a
            CloudControlMetadata.
        deployment_state (google.cloud.cloudsecuritycompliance_v1.types.DeploymentState):
            Output only. State of the Framework
            Deployment
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the resource
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the resource
            last updated.
        etag (str):
            Optional. To prevent concurrent updates from overwriting
            each other, always provide the ``etag`` when you update a
            FrameworkDeployment. You can also provide the ``etag`` when
            you delete a FrameworkDeployment, to help ensure that you're
            deleting the intended version of the FrameworkDeployment.
        target_resource_display_name (str):
            Output only. The display name of the target
            resource.
        cloud_control_deployment_references (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.CloudControlDeploymentReference]):
            Output only. The references to the cloud control
            deployments. It has all the CloudControlDeployments which
            are either directly added in the framework or through a
            CloudControlGroup. Example: If a framework deployment
            deploys two cloud controls, cc-deployment-1 and
            cc-deployment-2, then the
            cloud_control_deployment_references will be: {
            cloud_control_deployment_reference: {
            cloud_control_deployment:
            "organizations/{organization}/locations/{location}/cloudControlDeployments/cc-deployment-1"
            }, cloud_control_deployment_reference: {
            cloud_control_deployment:
            "organizations/{organization}/locations/{location}/cloudControlDeployments/cc-deployment-2"
            }
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    target_resource_config: "TargetResourceConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="TargetResourceConfig",
    )
    computed_target_resource: str = proto.Field(
        proto.STRING,
        number=3,
    )
    framework: common.FrameworkReference = proto.Field(
        proto.MESSAGE,
        number=4,
        message=common.FrameworkReference,
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    cloud_control_metadata: MutableSequence[
        "CloudControlMetadata"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="CloudControlMetadata",
    )
    deployment_state: "DeploymentState" = proto.Field(
        proto.ENUM,
        number=7,
        enum="DeploymentState",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=11,
    )
    target_resource_display_name: str = proto.Field(
        proto.STRING,
        number=13,
    )
    cloud_control_deployment_references: MutableSequence[
        "CloudControlDeploymentReference"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message="CloudControlDeploymentReference",
    )


class CloudControlDeployment(proto.Message):
    r"""CloudControlDeployment represents deployment of a
    CloudControl on a target resource. Supported target resources
    are organizations/{organization}, folders/{folder}, and
    projects/{project}.

    Attributes:
        name (str):
            Identifier. CloudControlDeployment name in the following
            format:
            organizations/{organization}/locations/{location}/cloudControlDeployments/{cloud_control_deployment_id}
        target_resource_config (google.cloud.cloudsecuritycompliance_v1.types.TargetResourceConfig):
            Required. The details of the target resource
            on which the CloudControl is to be deployed. It
            can either be an existing target resource or a
            new target resource to be created.
        target_resource (str):
            Output only. The resource on which the
            CloudControl is deployed based on the provided
            TargetResourceConfig in the following format:

            organizations/{organization}, folders/{folder}
            or projects/{project}.
        cloud_control_metadata (google.cloud.cloudsecuritycompliance_v1.types.CloudControlMetadata):
            Required. Deployment mode and parameters for
            the Cloud Control.
        description (str):
            Optional. User provided description of the
            CloudControl deployment
        deployment_state (google.cloud.cloudsecuritycompliance_v1.types.DeploymentState):
            Output only. State of the CloudControl
            deployment
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the resource
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the resource
            last updated.
        etag (str):
            Optional. To prevent concurrent updates from overwriting
            each other, always provide the ``etag`` when you update a
            CloudControlDeployment. You can also provide the ``etag``
            when you delete a CloudControlDeployment, to help ensure
            that you're deleting the intended version of the
            CloudControlDeployment.
        parameter_substituted_cloud_control (google.cloud.cloudsecuritycompliance_v1.types.CloudControl):
            Output only. The CloudControl after
            substitution of given parameters.
        framework_deployment_references (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.FrameworkDeploymentReference]):
            Output only. The references to the Framework
            deployments that this Cloud Control deployment
            is part of. A Cloud Control deployment can be
            part of multiple Framework deployments.
        target_resource_display_name (str):
            Output only. The display name of the target
            resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    target_resource_config: "TargetResourceConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="TargetResourceConfig",
    )
    target_resource: str = proto.Field(
        proto.STRING,
        number=3,
    )
    cloud_control_metadata: "CloudControlMetadata" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="CloudControlMetadata",
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )
    deployment_state: "DeploymentState" = proto.Field(
        proto.ENUM,
        number=6,
        enum="DeploymentState",
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
    etag: str = proto.Field(
        proto.STRING,
        number=9,
    )
    parameter_substituted_cloud_control: common.CloudControl = proto.Field(
        proto.MESSAGE,
        number=10,
        message=common.CloudControl,
    )
    framework_deployment_references: MutableSequence[
        "FrameworkDeploymentReference"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message="FrameworkDeploymentReference",
    )
    target_resource_display_name: str = proto.Field(
        proto.STRING,
        number=12,
    )


class TargetResourceConfig(proto.Message):
    r"""TargetResourceConfig contains either the name of the target_resource
    or contains the config to create a new target_resource.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        existing_target_resource (str):
            Optional. CRM node in format
            organizations/{organization}, folders/{folder},
            or projects/{project}

            This field is a member of `oneof`_ ``resource_config``.
        target_resource_creation_config (google.cloud.cloudsecuritycompliance_v1.types.TargetResourceCreationConfig):
            Optional. Config to create a new resource and use that as
            the target_resource for deployment.

            This field is a member of `oneof`_ ``resource_config``.
    """

    existing_target_resource: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="resource_config",
    )
    target_resource_creation_config: "TargetResourceCreationConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="resource_config",
        message="TargetResourceCreationConfig",
    )


class TargetResourceCreationConfig(proto.Message):
    r"""TargetResourceCreationConfig contains the config to create a new
    resource to be used as the target_resource of a deployment.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        folder_creation_config (google.cloud.cloudsecuritycompliance_v1.types.FolderCreationConfig):
            Optional. Config to create a new folder to be used as the
            target_resource of a deployment.

            This field is a member of `oneof`_ ``resource_creation_config``.
        project_creation_config (google.cloud.cloudsecuritycompliance_v1.types.ProjectCreationConfig):
            Optional. Config to create a new project to be used as the
            target_resource of a deployment.

            This field is a member of `oneof`_ ``resource_creation_config``.
    """

    folder_creation_config: "FolderCreationConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="resource_creation_config",
        message="FolderCreationConfig",
    )
    project_creation_config: "ProjectCreationConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="resource_creation_config",
        message="ProjectCreationConfig",
    )


class FolderCreationConfig(proto.Message):
    r"""FolderCreationConfig contains the config to create a new folder to
    be used as the target_resource of a deployment.

    Attributes:
        parent (str):
            Required. The parent of the folder to be
            created. It can be an organizations/{org} or
            folders/{folder}
        folder_display_name (str):
            Required. Display name of the folder to be
            created
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    folder_display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ProjectCreationConfig(proto.Message):
    r"""ProjectCreationConfig contains the config to create a new project to
    be used as the target_resource of a deployment.

    Attributes:
        parent (str):
            Required. organizations/{org} or
            folders/{folder}
        project_display_name (str):
            Required. Display name of the project to be
            created.
        billing_account_id (str):
            Required. Billing account id to be used for
            the project.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    project_display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    billing_account_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class CloudControlMetadata(proto.Message):
    r"""CloudControlMetadata contains the enforcement mode and
    parameters of a Cloud Control Deployment.

    Attributes:
        cloud_control_details (google.cloud.cloudsecuritycompliance_v1.types.CloudControlDetails):
            Required. Cloud control name and parameters.
        enforcement_mode (google.cloud.cloudsecuritycompliance_v1.types.EnforcementMode):
            Required. Enforcement mode of the cloud
            control
    """

    cloud_control_details: common.CloudControlDetails = proto.Field(
        proto.MESSAGE,
        number=1,
        message=common.CloudControlDetails,
    )
    enforcement_mode: common.EnforcementMode = proto.Field(
        proto.ENUM,
        number=2,
        enum=common.EnforcementMode,
    )


class CreateFrameworkDeploymentRequest(proto.Message):
    r"""Request message for CreateFrameworkDeployment API.

    Attributes:
        parent (str):
            Required. The parent resource of the
            FrameworkDeployment in the format:
            organizations/{organization}/locations/{location}
            Only global location is supported.
        framework_deployment_id (str):
            Optional. User provided identifier. It should
            be unique in scope of a parent. This is optional
            and if not provided, a random UUID will be
            generated.
        framework_deployment (google.cloud.cloudsecuritycompliance_v1.types.FrameworkDeployment):
            Required. The FrameworkDeployment to be
            created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    framework_deployment_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    framework_deployment: "FrameworkDeployment" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="FrameworkDeployment",
    )


class DeleteFrameworkDeploymentRequest(proto.Message):
    r"""Request message for DeleteFrameworkDeployment.

    Attributes:
        name (str):
            Required. name of the FrameworkDeployment to be deleted in
            the following format:
            organizations/{organization}/locations/{location}/frameworkDeployments/{framework_deployment_id}
        etag (str):
            Optional. An opaque identifier for the current version of
            the resource.

            If you provide this value, then it must match the existing
            value. If the values don't match, then the request fails
            with an [ABORTED][google.rpc.Code.ABORTED] error.

            If you omit this value, then the resource is deleted
            regardless of its current ``etag`` value.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetFrameworkDeploymentRequest(proto.Message):
    r"""Request message for GetFrameworkDeployment.

    Attributes:
        name (str):
            Required. FrameworkDeployment name in the following format:
            organizations/{organization}/locations/{location}/frameworkDeployments/{framework_deployment_id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListFrameworkDeploymentsRequest(proto.Message):
    r"""Request message for ListFrameworkDeployments.

    Attributes:
        parent (str):
            Required. parent resource of the
            FrameworkDeployment in the format:
            organizations/{organization}/locations/{location}
            Only global location is supported.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filter to be applied on the
            resource, defined by EBNF grammar
            https://google.aip.dev/assets/misc/ebnf-filtering.txt.
        order_by (str):
            Optional. Sort results. Supported are "name",
            "name desc" or "" (unsorted).
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


class ListFrameworkDeploymentsResponse(proto.Message):
    r"""Response message for ListFrameworkDeployments.

    Attributes:
        framework_deployments (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.FrameworkDeployment]):
            The list of FrameworkDeployments.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    framework_deployments: MutableSequence["FrameworkDeployment"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="FrameworkDeployment",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetCloudControlDeploymentRequest(proto.Message):
    r"""Request message for GetCloudControlDeployment.

    Attributes:
        name (str):
            Required. CloudControlDeployment name in the following
            format:
            organizations/{organization}/locations/{location}/cloudControlDeployments/{cloud_control_deployment_id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCloudControlDeploymentsRequest(proto.Message):
    r"""Request message for ListCloudControlDeployments.

    Attributes:
        parent (str):
            Required. parent resource of the
            CloudControlDeployment in the format:
            organizations/{organization}/locations/{location}
            Only global location is supported.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filter to be applied on the
            resource, defined by EBNF grammar
            https://google.aip.dev/assets/misc/ebnf-filtering.txt.
        order_by (str):
            Optional. Sort results. Supported are "name",
            "name desc" or "" (unsorted).
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


class ListCloudControlDeploymentsResponse(proto.Message):
    r"""Response message for ListCloudControlDeployments.

    Attributes:
        cloud_control_deployments (MutableSequence[google.cloud.cloudsecuritycompliance_v1.types.CloudControlDeployment]):
            The list of CloudControlDeployments.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    cloud_control_deployments: MutableSequence[
        "CloudControlDeployment"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CloudControlDeployment",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CloudControlDeploymentReference(proto.Message):
    r"""The reference to a CloudControlDeployment.

    Attributes:
        cloud_control_deployment (str):
            Output only. The name of the CloudControlDeployment. The
            format is:
            organizations/{org}/locations/{location}/cloudControlDeployments/{cloud_control_deployment_id}
    """

    cloud_control_deployment: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FrameworkDeploymentReference(proto.Message):
    r"""The reference to a FrameworkDeployment.

    Attributes:
        framework_deployment (str):
            Output only. The name of the FrameworkDeployment. The format
            is:
            organizations/{org}/locations/{location}/frameworkDeployments/{framework_deployment_id}
        framework_reference (google.cloud.cloudsecuritycompliance_v1.types.FrameworkReference):
            Optional. The reference to the Framework that this
            deployment is for. Example: { framework:
            "organizations/{org}/locations/{location}/frameworks/{framework}",
            major_revision_id: 1 }
        framework_display_name (str):
            Optional. The display name of the Framework
            that this FrameworkDeployment is for.
    """

    framework_deployment: str = proto.Field(
        proto.STRING,
        number=1,
    )
    framework_reference: common.FrameworkReference = proto.Field(
        proto.MESSAGE,
        number=2,
        message=common.FrameworkReference,
    )
    framework_display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
