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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.securityposture_v1.types import (
    org_policy_constraints,
    sha_constraints,
)

__protobuf__ = proto.module(
    package="google.cloud.securityposture.v1",
    manifest={
        "OperationMetadata",
        "Posture",
        "PolicySet",
        "Policy",
        "Constraint",
        "ListPosturesRequest",
        "ListPosturesResponse",
        "ListPostureRevisionsRequest",
        "ListPostureRevisionsResponse",
        "GetPostureRequest",
        "CreatePostureRequest",
        "UpdatePostureRequest",
        "DeletePostureRequest",
        "ExtractPostureRequest",
        "PostureDeployment",
        "ListPostureDeploymentsRequest",
        "ListPostureDeploymentsResponse",
        "GetPostureDeploymentRequest",
        "CreatePostureDeploymentRequest",
        "UpdatePostureDeploymentRequest",
        "DeletePostureDeploymentRequest",
        "PostureTemplate",
        "ListPostureTemplatesRequest",
        "ListPostureTemplatesResponse",
        "GetPostureTemplateRequest",
    },
)


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
            cancellation of the operation. Operations that have been
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
        error_message (str):
            Output only. This is a output only optional field which will
            be filled only in cases where PostureDeployments enter
            failure states like UPDATE_FAILED or CREATE_FAILED or
            DELETE_FAILED.
    """

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
    error_message: str = proto.Field(
        proto.STRING,
        number=8,
    )


class Posture(proto.Message):
    r"""Postures
    Definition of a Posture.

    Attributes:
        name (str):
            Required. Identifier. The name of this Posture resource, in
            the format of
            organizations/{org_id}/locations/{location_id}/postures/{posture}.
        state (google.cloud.securityposture_v1.types.Posture.State):
            Required. State of Posture resource.
        revision_id (str):
            Output only. Immutable. The revision ID of
            the posture. The format is an 8-character
            hexadecimal string. https://google.aip.dev/162
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp that the posture
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp that the posture
            was updated.
        description (str):
            Optional. User provided description of the
            posture.
        policy_sets (MutableSequence[google.cloud.securityposture_v1.types.PolicySet]):
            Required. List of Policy sets.
        etag (str):
            Optional. An opaque tag indicating the current version of
            the Posture, used for concurrency control. When the
            ``Posture`` is returned from either a ``GetPosture`` or a
            ``ListPostures`` request, this ``etag`` indicates the
            version of the current ``Posture`` to use when executing a
            read-modify-write loop.

            When the ``Posture`` is used in a ``UpdatePosture`` method,
            use the ``etag`` value that was returned from a
            ``GetPosture`` request as part of a read-modify-write loop
            for concurrency control. Not setting the ``etag`` in a
            ``UpdatePosture`` request will result in an unconditional
            write of the ``Posture``.
        annotations (MutableMapping[str, str]):
            Optional. User annotations. These attributes
            can only be set and used by the user, and not by
            Google Security Postures. .
        reconciling (bool):
            Output only. Whether or not this Posture is
            in the process of being updated.
    """

    class State(proto.Enum):
        r"""State of a Posture.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified operation state.
            DEPRECATED (1):
                The Posture is marked deprecated when it is
                not in use by the user.
            DRAFT (2):
                The Posture is created successfully but is
                not yet ready for usage.
            ACTIVE (3):
                The Posture state is active. Ready for
                use/deployments.
        """
        STATE_UNSPECIFIED = 0
        DEPRECATED = 1
        DRAFT = 2
        ACTIVE = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    revision_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=6,
    )
    policy_sets: MutableSequence["PolicySet"] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="PolicySet",
    )
    etag: str = proto.Field(
        proto.STRING,
        number=8,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=10,
    )


class PolicySet(proto.Message):
    r"""PolicySet representation.

    Attributes:
        policy_set_id (str):
            Required. ID of the Policy set.
        description (str):
            Optional. Description of the Policy set.
        policies (MutableSequence[google.cloud.securityposture_v1.types.Policy]):
            Required. List of policies.
    """

    policy_set_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    policies: MutableSequence["Policy"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="Policy",
    )


class Policy(proto.Message):
    r"""Policy representation.

    Attributes:
        policy_id (str):
            Required. ID of the Policy that is user
            generated, immutable and unique within the scope
            of a policy set.
        compliance_standards (MutableSequence[google.cloud.securityposture_v1.types.Policy.ComplianceStandard]):
            Optional. Contains list of mapping for a
            Policy to a standard and control.
        constraint (google.cloud.securityposture_v1.types.Constraint):
            Required. Constraint details.
        description (str):
            Optional. Description of the Policy.
    """

    class ComplianceStandard(proto.Message):
        r"""Mapping for a Policy to standard and control.

        Attributes:
            standard (str):
                Optional. The compliance standard that the
                Policy maps to, e.g.: CIS-2.0.
            control (str):
                Optional. Control mapping provided by user
                for this Policy. e.g.: 1.5.
        """

        standard: str = proto.Field(
            proto.STRING,
            number=1,
        )
        control: str = proto.Field(
            proto.STRING,
            number=2,
        )

    policy_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    compliance_standards: MutableSequence[ComplianceStandard] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=ComplianceStandard,
    )
    constraint: "Constraint" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Constraint",
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )


class Constraint(proto.Message):
    r"""Representation of a Constraint.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        security_health_analytics_module (google.cloud.securityposture_v1.types.SecurityHealthAnalyticsModule):
            Optional. SHA built-in detector.

            This field is a member of `oneof`_ ``implementation``.
        security_health_analytics_custom_module (google.cloud.securityposture_v1.types.SecurityHealthAnalyticsCustomModule):
            Optional. SHA custom detector.

            This field is a member of `oneof`_ ``implementation``.
        org_policy_constraint (google.cloud.securityposture_v1.types.OrgPolicyConstraint):
            Optional. Org Policy builtin constraint.

            This field is a member of `oneof`_ ``implementation``.
        org_policy_constraint_custom (google.cloud.securityposture_v1.types.OrgPolicyConstraintCustom):
            Optional. Org Policy custom constraint.

            This field is a member of `oneof`_ ``implementation``.
    """

    security_health_analytics_module: sha_constraints.SecurityHealthAnalyticsModule = (
        proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="implementation",
            message=sha_constraints.SecurityHealthAnalyticsModule,
        )
    )
    security_health_analytics_custom_module: sha_constraints.SecurityHealthAnalyticsCustomModule = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="implementation",
        message=sha_constraints.SecurityHealthAnalyticsCustomModule,
    )
    org_policy_constraint: org_policy_constraints.OrgPolicyConstraint = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="implementation",
        message=org_policy_constraints.OrgPolicyConstraint,
    )
    org_policy_constraint_custom: org_policy_constraints.OrgPolicyConstraintCustom = (
        proto.Field(
            proto.MESSAGE,
            number=6,
            oneof="implementation",
            message=org_policy_constraints.OrgPolicyConstraintCustom,
        )
    )


class ListPosturesRequest(proto.Message):
    r"""Message for requesting list of Postures.

    Attributes:
        parent (str):
            Required. Parent value for
            ListPosturesRequest.
        page_size (int):
            Requested page size. Server may return fewer
            items than requested. If unspecified, server
            will pick an appropriate default.
        page_token (str):
            A token identifying a page of results the
            server should return.
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


class ListPosturesResponse(proto.Message):
    r"""Message for response to listing Postures.

    Attributes:
        postures (MutableSequence[google.cloud.securityposture_v1.types.Posture]):
            The list of Posture.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Unreachable resources.
    """

    @property
    def raw_page(self):
        return self

    postures: MutableSequence["Posture"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Posture",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class ListPostureRevisionsRequest(proto.Message):
    r"""Message for requesting list of Posture revisions.

    Attributes:
        name (str):
            Required. Name value for
            ListPostureRevisionsRequest.
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick 100 as default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
    """

    name: str = proto.Field(
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


class ListPostureRevisionsResponse(proto.Message):
    r"""Message for response to listing PostureRevisions.

    Attributes:
        revisions (MutableSequence[google.cloud.securityposture_v1.types.Posture]):
            The list of Posture revisions.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    revisions: MutableSequence["Posture"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Posture",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetPostureRequest(proto.Message):
    r"""Message for getting a Posture.

    Attributes:
        name (str):
            Required. Name of the resource.
        revision_id (str):
            Optional. Posture revision which needs to be
            retrieved.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    revision_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class CreatePostureRequest(proto.Message):
    r"""Message for creating a Posture.

    Attributes:
        parent (str):
            Required. Value for parent.
        posture_id (str):
            Required. User provided identifier. It should
            be unique in scope of an Organization and
            location.
        posture (google.cloud.securityposture_v1.types.Posture):
            Required. The resource being created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    posture_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    posture: "Posture" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Posture",
    )


class UpdatePostureRequest(proto.Message):
    r"""Message for updating a Posture.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the Posture resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        posture (google.cloud.securityposture_v1.types.Posture):
            Required. The resource being updated.
        revision_id (str):
            Required. Posture revision which needs to be
            updated.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    posture: "Posture" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Posture",
    )
    revision_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeletePostureRequest(proto.Message):
    r"""Message for deleting a Posture.

    Attributes:
        name (str):
            Required. Name of the resource.
        etag (str):
            Optional. Etag value of the Posture to be
            deleted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ExtractPostureRequest(proto.Message):
    r"""Message for extracting existing policies on a workload as a
    Posture.

    Attributes:
        parent (str):
            Required. The parent resource name. The format of this value
            is as follows:
            ``organizations/{organization}/locations/{location}``
        posture_id (str):
            Required. User provided identifier. It should
            be unique in scope of an Organization and
            location.
        workload (str):
            Required. Workload from which the policies are to be
            extracted, it should belong to the same organization defined
            in parent. The format of this value varies depending on the
            scope of the request:

            -  ``folder/folderNumber``
            -  ``project/projectNumber``
            -  ``organization/organizationNumber``
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    posture_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    workload: str = proto.Field(
        proto.STRING,
        number=3,
    )


class PostureDeployment(proto.Message):
    r"""========================== PostureDeployments
    ========================== Message describing PostureDeployment
    resource.

    Attributes:
        name (str):
            Required. The name of this PostureDeployment resource, in
            the format of
            organizations/{organization}/locations/{location_id}/postureDeployments/{postureDeployment}.
        target_resource (str):
            Required. Target resource where the Posture
            will be deployed. Currently supported resources
            are of types: projects/projectNumber,
            folders/folderNumber,
            organizations/organizationNumber.
        state (google.cloud.securityposture_v1.types.PostureDeployment.State):
            Output only. State of PostureDeployment
            resource.
        posture_id (str):
            Required. Posture that needs to be deployed. Format:
            organizations/{org_id}/locations/{location_id}/postures/
            Example:
            organizations/99/locations/global/postures/les-miserables.
        posture_revision_id (str):
            Required. Revision_id of the Posture that is to be deployed.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp that the
            PostureDeployment was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp that the
            PostureDeployment was updated.
        description (str):
            Optional. User provided description of the
            PostureDeployment.
        etag (str):
            Optional. An opaque tag indicating the current version of
            the PostureDeployment, used for concurrency control. When
            the ``PostureDeployment`` is returned from either a
            ``GetPostureDeployment`` or a ``ListPostureDeployments``
            request, this ``etag`` indicates the version of the current
            ``PostureDeployment`` to use when executing a
            read-modify-write loop.

            When the ``PostureDeployment`` is used in a
            ``UpdatePostureDeployment`` method, use the ``etag`` value
            that was returned from a ``GetPostureDeployment`` request as
            part of a read-modify-write loop for concurrency control.
            Not setting the ``etag`` in a ``UpdatePostureDeployment``
            request will result in an unconditional write of the
            ``PostureDeployment``.
        annotations (MutableMapping[str, str]):
            Optional. User annotations. These attributes
            can only be set and used by the user, and not by
            Google Security Postures. .
        reconciling (bool):
            Output only. Whether or not this Posture is
            in the process of being updated.
        desired_posture_id (str):
            Output only. This is a output only optional field which will
            be filled in case where PostureDeployment state is
            UPDATE_FAILED or CREATE_FAILED or DELETE_FAILED. It denotes
            the desired Posture.
        desired_posture_revision_id (str):
            Output only. Output only optional field which provides
            revision_id of the desired_posture_id.
        failure_message (str):
            Output only. This is a output only optional field which will
            be filled in case where PostureDeployment enters a failure
            state like UPDATE_FAILED or CREATE_FAILED or DELETE_FAILED.
    """

    class State(proto.Enum):
        r"""State of a PostureDeployment.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified operation state.
            CREATING (1):
                The PostureDeployment is being created.
            DELETING (2):
                The PostureDeployment is being deleted.
            UPDATING (3):
                The PostureDeployment state is being updated.
            ACTIVE (4):
                The PostureDeployment state is active and in
                use.
            CREATE_FAILED (5):
                The PostureDeployment creation failed.
            UPDATE_FAILED (6):
                The PostureDeployment update failed.
            DELETE_FAILED (7):
                The PostureDeployment deletion failed.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        DELETING = 2
        UPDATING = 3
        ACTIVE = 4
        CREATE_FAILED = 5
        UPDATE_FAILED = 6
        DELETE_FAILED = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    target_resource: str = proto.Field(
        proto.STRING,
        number=13,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    posture_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    posture_revision_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    description: str = proto.Field(
        proto.STRING,
        number=7,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=8,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=10,
    )
    desired_posture_id: str = proto.Field(
        proto.STRING,
        number=11,
    )
    desired_posture_revision_id: str = proto.Field(
        proto.STRING,
        number=12,
    )
    failure_message: str = proto.Field(
        proto.STRING,
        number=14,
    )


class ListPostureDeploymentsRequest(proto.Message):
    r"""Message for requesting list of PostureDeployments.

    Attributes:
        parent (str):
            Required. Parent value for
            ListPostureDeploymentsRequest.
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


class ListPostureDeploymentsResponse(proto.Message):
    r"""Message for response to listing PostureDeployments.

    Attributes:
        posture_deployments (MutableSequence[google.cloud.securityposture_v1.types.PostureDeployment]):
            The list of PostureDeployment.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    posture_deployments: MutableSequence["PostureDeployment"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PostureDeployment",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetPostureDeploymentRequest(proto.Message):
    r"""Message for getting a PostureDeployment.

    Attributes:
        name (str):
            Required. Name of the resource.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreatePostureDeploymentRequest(proto.Message):
    r"""Message for creating a PostureDeployment.

    Attributes:
        parent (str):
            Required. Value for parent. Format:
            organizations/{org_id}/locations/{location}
        posture_deployment_id (str):
            Required. User provided identifier. It should
            be unique in scope of an Organization and
            location.
        posture_deployment (google.cloud.securityposture_v1.types.PostureDeployment):
            Required. The resource being created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    posture_deployment_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    posture_deployment: "PostureDeployment" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="PostureDeployment",
    )


class UpdatePostureDeploymentRequest(proto.Message):
    r"""Message for updating a PostureDeployment.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the PostureDeployment resource by the update.
            The fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        posture_deployment (google.cloud.securityposture_v1.types.PostureDeployment):
            Required. The resource being updated.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    posture_deployment: "PostureDeployment" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PostureDeployment",
    )


class DeletePostureDeploymentRequest(proto.Message):
    r"""Message for deleting a PostureDeployment.

    Attributes:
        name (str):
            Required. Name of the resource.
        etag (str):
            Optional. Etag value of the PostureDeployment
            to be deleted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class PostureTemplate(proto.Message):
    r"""PostureTemplates
    Message describing PostureTemplate object.

    Attributes:
        name (str):
            Output only. Identifier. The name of the
            Posture template will be of the format
            organizations/{organization}/locations/{location}/postureTemplates/{postureTemplate}
        revision_id (str):
            Output only. The revision_id of a PostureTemplate.
        description (str):
            Output only. Description of the Posture
            template.
        state (google.cloud.securityposture_v1.types.PostureTemplate.State):
            Output only. State of PostureTemplate
            resource.
        policy_sets (MutableSequence[google.cloud.securityposture_v1.types.PolicySet]):
            Output only. Policy_sets to be used by the user.
    """

    class State(proto.Enum):
        r"""State of a PostureTemplate

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state
            ACTIVE (1):
                If the Posture template is adhering to the
                latest controls and standards.
            DEPRECATED (2):
                If the Posture template controls and
                standards are outdated and not recommended for
                use.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        DEPRECATED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    revision_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    policy_sets: MutableSequence["PolicySet"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="PolicySet",
    )


class ListPostureTemplatesRequest(proto.Message):
    r"""Message for requesting list of Posture Templates.

    Attributes:
        parent (str):
            Required. Parent value for
            ListPostureTemplatesRequest.
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


class ListPostureTemplatesResponse(proto.Message):
    r"""Message for response to listing PostureTemplates.

    Attributes:
        posture_templates (MutableSequence[google.cloud.securityposture_v1.types.PostureTemplate]):
            The list of PostureTemplate.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    posture_templates: MutableSequence["PostureTemplate"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PostureTemplate",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetPostureTemplateRequest(proto.Message):
    r"""Message for getting a Posture Template.

    Attributes:
        name (str):
            Required. Name of the resource.
        revision_id (str):
            Optional. Specific revision_id of a Posture Template.
            PostureTemplate revision_id which needs to be retrieved.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    revision_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
