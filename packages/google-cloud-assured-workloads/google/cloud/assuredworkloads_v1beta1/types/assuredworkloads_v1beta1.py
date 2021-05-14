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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.assuredworkloads.v1beta1",
    manifest={
        "CreateWorkloadRequest",
        "UpdateWorkloadRequest",
        "DeleteWorkloadRequest",
        "GetWorkloadRequest",
        "ListWorkloadsRequest",
        "ListWorkloadsResponse",
        "Workload",
        "CreateWorkloadOperationMetadata",
    },
)


class CreateWorkloadRequest(proto.Message):
    r"""Request for creating a workload.
    Attributes:
        parent (str):
            Required. The resource name of the new Workload's parent.
            Must be of the form
            ``organizations/{org_id}/locations/{location_id}``.
        workload (google.cloud.assuredworkloads_v1beta1.types.Workload):
            Required. Assured Workload to create
        external_id (str):
            Optional. A identifier associated with the
            workload and underlying projects which allows
            for the break down of billing costs for a
            workload. The value provided for the identifier
            will add a label to the workload and contained
            projects with the identifier as the value.
    """

    parent = proto.Field(proto.STRING, number=1,)
    workload = proto.Field(proto.MESSAGE, number=2, message="Workload",)
    external_id = proto.Field(proto.STRING, number=3,)


class UpdateWorkloadRequest(proto.Message):
    r"""Request for Updating a workload.
    Attributes:
        workload (google.cloud.assuredworkloads_v1beta1.types.Workload):
            Required. The workload to update. The workload’s ``name``
            field is used to identify the workload to be updated.
            Format:
            organizations/{org_id}/locations/{location_id}/workloads/{workload_id}
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated.
    """

    workload = proto.Field(proto.MESSAGE, number=1, message="Workload",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteWorkloadRequest(proto.Message):
    r"""Request for deleting a Workload.
    Attributes:
        name (str):
            Required. The ``name`` field is used to identify the
            workload. Format:
            organizations/{org_id}/locations/{location_id}/workloads/{workload_id}
        etag (str):
            Optional. The etag of the workload.
            If this is provided, it must match the server's
            etag.
    """

    name = proto.Field(proto.STRING, number=1,)
    etag = proto.Field(proto.STRING, number=2,)


class GetWorkloadRequest(proto.Message):
    r"""Request for fetching a workload.
    Attributes:
        name (str):
            Required. The resource name of the Workload to fetch. This
            is the workloads's relative path in the API, formatted as
            "organizations/{organization_id}/locations/{location_id}/workloads/{workload_id}".
            For example,
            "organizations/123/locations/us-east1/workloads/assured-workload-1".
    """

    name = proto.Field(proto.STRING, number=1,)


class ListWorkloadsRequest(proto.Message):
    r"""Request for fetching workloads in an organization.
    Attributes:
        parent (str):
            Required. Parent Resource to list workloads from. Must be of
            the form ``organizations/{org_id}/locations/{location}``.
        page_size (int):
            Page size.
        page_token (str):
            Page token returned from previous request.
            Page token contains context from previous
            request. Page token needs to be passed in the
            second and following requests.
        filter (str):
            A custom filter for filtering by properties
            of a workload. At this time, only filtering by
            labels is supported.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)


class ListWorkloadsResponse(proto.Message):
    r"""Response of ListWorkloads endpoint.
    Attributes:
        workloads (Sequence[google.cloud.assuredworkloads_v1beta1.types.Workload]):
            List of Workloads under a given parent.
        next_page_token (str):
            The next page token. Return empty if reached
            the last page.
    """

    @property
    def raw_page(self):
        return self

    workloads = proto.RepeatedField(proto.MESSAGE, number=1, message="Workload",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class Workload(proto.Message):
    r"""An Workload object for managing highly regulated workloads of
    cloud customers.

    Attributes:
        name (str):
            Optional. The resource name of the workload.
            Format:
            organizations/{organization}/locations/{location}/workloads/{workload}
            Read-only.
        display_name (str):
            Required. The user-assigned display name of
            the Workload. When present it must be between 4
            to 30 characters. Allowed characters are:
            lowercase and uppercase letters, numbers,
            hyphen, and spaces.

            Example: My Workload
        resources (Sequence[google.cloud.assuredworkloads_v1beta1.types.Workload.ResourceInfo]):
            Output only. The resources associated with
            this workload. These resources will be created
            when creating the workload. If any of the
            projects already exist, the workload creation
            will fail. Always read only.
        compliance_regime (google.cloud.assuredworkloads_v1beta1.types.Workload.ComplianceRegime):
            Required. Immutable. Compliance Regime
            associated with this workload.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Immutable. The Workload creation
            timestamp.
        billing_account (str):
            Required. Input only. The billing account used for the
            resources which are direct children of workload. This
            billing account is initially associated with the resources
            created as part of Workload creation. After the initial
            creation of these resources, the customer can change the
            assigned billing account. The resource name has the form
            ``billingAccounts/{billing_account_id}``. For example,
            ``billingAccounts/012345-567890-ABCDEF``.
        il4_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.IL4Settings):
            Required. Input only. Immutable. Settings
            specific to resources needed for IL4.
        cjis_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.CJISSettings):
            Required. Input only. Immutable. Settings
            specific to resources needed for CJIS.
        fedramp_high_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.FedrampHighSettings):
            Required. Input only. Immutable. Settings
            specific to resources needed for FedRAMP High.
        fedramp_moderate_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.FedrampModerateSettings):
            Required. Input only. Immutable. Settings
            specific to resources needed for FedRAMP
            Moderate.
        etag (str):
            Optional. ETag of the workload, it is
            calculated on the basis of the Workload
            contents. It will be used in Update & Delete
            operations.
        labels (Sequence[google.cloud.assuredworkloads_v1beta1.types.Workload.LabelsEntry]):
            Optional. Labels applied to the workload.
        provisioned_resources_parent (str):
            Input only. The parent resource for the resources managed by
            this Assured Workload. May be either an organization or a
            folder. Must be the same or a child of the Workload parent.
            If not specified all resources are created under the
            Workload parent. Formats: folders/{folder_id}
            organizations/{organization_id}
        kms_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.KMSSettings):
            Input only. Settings used to create a CMEK
            crypto key. When set a project with a KMS CMEK
            key is provisioned. This field is mandatory for
            a subset of Compliance Regimes.
        resource_settings (Sequence[google.cloud.assuredworkloads_v1beta1.types.Workload.ResourceSettings]):
            Input only. Resource properties that are used
            to customize workload resources. These
            properties (such as custom project id) will be
            used to create workload resources if possible.
            This field is optional.
    """

    class ComplianceRegime(proto.Enum):
        r"""Supported Compliance Regimes."""
        COMPLIANCE_REGIME_UNSPECIFIED = 0
        IL4 = 1
        CJIS = 2
        FEDRAMP_HIGH = 3
        FEDRAMP_MODERATE = 4
        US_REGIONAL_ACCESS = 5
        HIPAA = 6
        HITRUST = 7

    class ResourceInfo(proto.Message):
        r"""Represent the resources that are children of this Workload.
        Attributes:
            resource_id (int):
                Resource identifier. For a project this represents
                project_number.
            resource_type (google.cloud.assuredworkloads_v1beta1.types.Workload.ResourceInfo.ResourceType):
                Indicates the type of resource.
        """

        class ResourceType(proto.Enum):
            r"""The type of resource."""
            RESOURCE_TYPE_UNSPECIFIED = 0
            CONSUMER_PROJECT = 1
            ENCRYPTION_KEYS_PROJECT = 2

        resource_id = proto.Field(proto.INT64, number=1,)
        resource_type = proto.Field(
            proto.ENUM, number=2, enum="Workload.ResourceInfo.ResourceType",
        )

    class KMSSettings(proto.Message):
        r"""Settings specific to the Key Management Service.
        Attributes:
            next_rotation_time (google.protobuf.timestamp_pb2.Timestamp):
                Required. Input only. Immutable. The time at
                which the Key Management Service will
                automatically create a new version of the crypto
                key and mark it as the primary.
            rotation_period (google.protobuf.duration_pb2.Duration):
                Required. Input only. Immutable. [next_rotation_time] will
                be advanced by this period when the Key Management Service
                automatically rotates a key. Must be at least 24 hours and
                at most 876,000 hours.
        """

        next_rotation_time = proto.Field(
            proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,
        )
        rotation_period = proto.Field(
            proto.MESSAGE, number=2, message=duration_pb2.Duration,
        )

    class IL4Settings(proto.Message):
        r"""Settings specific to resources needed for IL4.
        Attributes:
            kms_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.KMSSettings):
                Required. Input only. Immutable. Settings
                used to create a CMEK crypto key.
        """

        kms_settings = proto.Field(
            proto.MESSAGE, number=1, message="Workload.KMSSettings",
        )

    class CJISSettings(proto.Message):
        r"""Settings specific to resources needed for CJIS.
        Attributes:
            kms_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.KMSSettings):
                Required. Input only. Immutable. Settings
                used to create a CMEK crypto key.
        """

        kms_settings = proto.Field(
            proto.MESSAGE, number=1, message="Workload.KMSSettings",
        )

    class FedrampHighSettings(proto.Message):
        r"""Settings specific to resources needed for FedRAMP High.
        Attributes:
            kms_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.KMSSettings):
                Required. Input only. Immutable. Settings
                used to create a CMEK crypto key.
        """

        kms_settings = proto.Field(
            proto.MESSAGE, number=1, message="Workload.KMSSettings",
        )

    class FedrampModerateSettings(proto.Message):
        r"""Settings specific to resources needed for FedRAMP Moderate.
        Attributes:
            kms_settings (google.cloud.assuredworkloads_v1beta1.types.Workload.KMSSettings):
                Required. Input only. Immutable. Settings
                used to create a CMEK crypto key.
        """

        kms_settings = proto.Field(
            proto.MESSAGE, number=1, message="Workload.KMSSettings",
        )

    class ResourceSettings(proto.Message):
        r"""Represent the custom settings for the resources to be
        created.

        Attributes:
            resource_id (str):
                Resource identifier. For a project this represents
                project_id. If the project is already taken, the workload
                creation will fail.
            resource_type (google.cloud.assuredworkloads_v1beta1.types.Workload.ResourceInfo.ResourceType):
                Indicates the type of resource. This field should be
                specified to correspond the id to the right project type
                (CONSUMER_PROJECT or ENCRYPTION_KEYS_PROJECT)
        """

        resource_id = proto.Field(proto.STRING, number=1,)
        resource_type = proto.Field(
            proto.ENUM, number=2, enum="Workload.ResourceInfo.ResourceType",
        )

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    resources = proto.RepeatedField(proto.MESSAGE, number=3, message=ResourceInfo,)
    compliance_regime = proto.Field(proto.ENUM, number=4, enum=ComplianceRegime,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    billing_account = proto.Field(proto.STRING, number=6,)
    il4_settings = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="compliance_regime_settings",
        message=IL4Settings,
    )
    cjis_settings = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="compliance_regime_settings",
        message=CJISSettings,
    )
    fedramp_high_settings = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="compliance_regime_settings",
        message=FedrampHighSettings,
    )
    fedramp_moderate_settings = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="compliance_regime_settings",
        message=FedrampModerateSettings,
    )
    etag = proto.Field(proto.STRING, number=9,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=10,)
    provisioned_resources_parent = proto.Field(proto.STRING, number=13,)
    kms_settings = proto.Field(proto.MESSAGE, number=14, message=KMSSettings,)
    resource_settings = proto.RepeatedField(
        proto.MESSAGE, number=15, message=ResourceSettings,
    )


class CreateWorkloadOperationMetadata(proto.Message):
    r"""Operation metadata to give request details of CreateWorkload.
    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Time when the operation was
            created.
        display_name (str):
            Optional. The display name of the workload.
        parent (str):
            Optional. The parent of the workload.
        compliance_regime (google.cloud.assuredworkloads_v1beta1.types.Workload.ComplianceRegime):
            Optional. Compliance controls that should be
            applied to the resources managed by the
            workload.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    display_name = proto.Field(proto.STRING, number=2,)
    parent = proto.Field(proto.STRING, number=3,)
    compliance_regime = proto.Field(
        proto.ENUM, number=4, enum="Workload.ComplianceRegime",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
