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


__protobuf__ = proto.module(
    package="google.cloud.accessapproval.v1",
    manifest={
        "EnrollmentLevel",
        "AccessLocations",
        "AccessReason",
        "ApproveDecision",
        "DismissDecision",
        "ResourceProperties",
        "ApprovalRequest",
        "EnrolledService",
        "AccessApprovalSettings",
        "ListApprovalRequestsMessage",
        "ListApprovalRequestsResponse",
        "GetApprovalRequestMessage",
        "ApproveApprovalRequestMessage",
        "DismissApprovalRequestMessage",
        "GetAccessApprovalSettingsMessage",
        "UpdateAccessApprovalSettingsMessage",
        "DeleteAccessApprovalSettingsMessage",
    },
)


class EnrollmentLevel(proto.Enum):
    r"""Represents the type of enrollment for a given service to
    Access Approval.
    """
    ENROLLMENT_LEVEL_UNSPECIFIED = 0
    BLOCK_ALL = 1


class AccessLocations(proto.Message):
    r"""Home office and physical location of the principal.
    Attributes:
        principal_office_country (str):
            The "home office" location of the principal.
            A two-letter country code (ISO 3166-1 alpha-2),
            such as "US", "DE" or "GB" or a region code. In
            some limited situations Google systems may refer
            refer to a region code instead of a country
            code.
            Possible Region Codes:

            - ASI: Asia
            - EUR: Europe
            - OCE: Oceania
            - AFR: Africa
            - NAM: North America
            - SAM: South America
            - ANT: Antarctica
            - ANY: Any location
        principal_physical_location_country (str):
            Physical location of the principal at the
            time of the access. A two-letter country code
            (ISO 3166-1 alpha-2), such as "US", "DE" or "GB"
            or a region code. In some limited situations
            Google systems may refer refer to a region code
            instead of a country code.
            Possible Region Codes:

            - ASI: Asia
            - EUR: Europe
            - OCE: Oceania
            - AFR: Africa
            - NAM: North America
            - SAM: South America
            - ANT: Antarctica
            - ANY: Any location
    """

    principal_office_country = proto.Field(proto.STRING, number=1,)
    principal_physical_location_country = proto.Field(proto.STRING, number=2,)


class AccessReason(proto.Message):
    r"""
    Attributes:
        type_ (google.cloud.accessapproval_v1.types.AccessReason.Type):
            Type of access justification.
        detail (str):
            More detail about certain reason types. See
            comments for each type above.
    """

    class Type(proto.Enum):
        r"""Type of access justification."""
        TYPE_UNSPECIFIED = 0
        CUSTOMER_INITIATED_SUPPORT = 1
        GOOGLE_INITIATED_SERVICE = 2
        GOOGLE_INITIATED_REVIEW = 3

    type_ = proto.Field(proto.ENUM, number=1, enum=Type,)
    detail = proto.Field(proto.STRING, number=2,)


class ApproveDecision(proto.Message):
    r"""A decision that has been made to approve access to a
    resource.

    Attributes:
        approve_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which approval was granted.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the approval expires.
    """

    approve_time = proto.Field(
        proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,
    )
    expire_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)


class DismissDecision(proto.Message):
    r"""A decision that has been made to dismiss an approval request.
    Attributes:
        dismiss_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which the approval request was
            dismissed.
    """

    dismiss_time = proto.Field(
        proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,
    )


class ResourceProperties(proto.Message):
    r"""The properties associated with the resource of the request.
    Attributes:
        excludes_descendants (bool):
            Whether an approval will exclude the
            descendants of the resource being requested.
    """

    excludes_descendants = proto.Field(proto.BOOL, number=1,)


class ApprovalRequest(proto.Message):
    r"""A request for the customer to approve access to a resource.
    Attributes:
        name (str):
            The resource name of the request. Format is
            "{projects|folders|organizations}/{id}/approvalRequests/{approval_request_id}".
        requested_resource_name (str):
            The resource for which approval is being requested. The
            format of the resource name is defined at
            https://cloud.google.com/apis/design/resource_names. The
            resource name here may either be a "full" resource name
            (e.g. "//library.googleapis.com/shelves/shelf1/books/book2")
            or a "relative" resource name (e.g.
            "shelves/shelf1/books/book2") as described in the resource
            name specification.
        requested_resource_properties (google.cloud.accessapproval_v1.types.ResourceProperties):
            Properties related to the resource represented by
            requested_resource_name.
        requested_reason (google.cloud.accessapproval_v1.types.AccessReason):
            The justification for which approval is being
            requested.
        requested_locations (google.cloud.accessapproval_v1.types.AccessLocations):
            The locations for which approval is being
            requested.
        request_time (google.protobuf.timestamp_pb2.Timestamp):
            The time at which approval was requested.
        requested_expiration (google.protobuf.timestamp_pb2.Timestamp):
            The requested expiration for the approval. If
            the request is approved, access will be granted
            from the time of approval until the expiration
            time.
        approve (google.cloud.accessapproval_v1.types.ApproveDecision):
            Access was approved.
        dismiss (google.cloud.accessapproval_v1.types.DismissDecision):
            The request was dismissed.
    """

    name = proto.Field(proto.STRING, number=1,)
    requested_resource_name = proto.Field(proto.STRING, number=2,)
    requested_resource_properties = proto.Field(
        proto.MESSAGE, number=9, message="ResourceProperties",
    )
    requested_reason = proto.Field(proto.MESSAGE, number=3, message="AccessReason",)
    requested_locations = proto.Field(
        proto.MESSAGE, number=4, message="AccessLocations",
    )
    request_time = proto.Field(
        proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
    )
    requested_expiration = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )
    approve = proto.Field(
        proto.MESSAGE, number=7, oneof="decision", message="ApproveDecision",
    )
    dismiss = proto.Field(
        proto.MESSAGE, number=8, oneof="decision", message="DismissDecision",
    )


class EnrolledService(proto.Message):
    r"""Represents the enrollment of a cloud resource into a specific
    service.

    Attributes:
        cloud_product (str):
            The product for which Access Approval will be
            enrolled. Allowed values are listed below (case-
            sensitive):
            - all
            - appengine.googleapis.com
            - bigquery.googleapis.com
            - bigtable.googleapis.com
            - cloudkms.googleapis.com
            - compute.googleapis.com
            - dataflow.googleapis.com
            - iam.googleapis.com
            - pubsub.googleapis.com
            - storage.googleapis.com
        enrollment_level (google.cloud.accessapproval_v1.types.EnrollmentLevel):
            The enrollment level of the service.
    """

    cloud_product = proto.Field(proto.STRING, number=1,)
    enrollment_level = proto.Field(proto.ENUM, number=2, enum="EnrollmentLevel",)


class AccessApprovalSettings(proto.Message):
    r"""Settings on a Project/Folder/Organization related to Access
    Approval.

    Attributes:
        name (str):
            The resource name of the settings. Format is one of:

            -  "projects/{project_id}/accessApprovalSettings"
            -  "folders/{folder_id}/accessApprovalSettings"
            -  "organizations/{organization_id}/accessApprovalSettings".
        notification_emails (Sequence[str]):
            A list of email addresses to which
            notifications relating to approval requests
            should be sent. Notifications relating to a
            resource will be sent to all emails in the
            settings of ancestor resources of that resource.
            A maximum of 50 email addresses are allowed.
        enrolled_services (Sequence[google.cloud.accessapproval_v1.types.EnrolledService]):
            A list of Google Cloud Services for which the given resource
            has Access Approval enrolled. Access requests for the
            resource given by name against any of these services
            contained here will be required to have explicit approval.
            If name refers to an organization, enrollment can be done
            for individual services. If name refers to a folder or
            project, enrollment can only be done on an all or nothing
            basis.

            If a cloud_product is repeated in this list, the first entry
            will be honored and all following entries will be discarded.
            A maximum of 10 enrolled services will be enforced, to be
            expanded as the set of supported services is expanded.
        enrolled_ancestor (bool):
            Output only. This field is read only (not
            settable via UpdateAccessAccessApprovalSettings
            method). If the field is true, that indicates
            that at least one service is enrolled for Access
            Approval in one or more ancestors of the Project
            or Folder (this field will always be unset for
            the organization since organizations do not have
            ancestors).
    """

    name = proto.Field(proto.STRING, number=1,)
    notification_emails = proto.RepeatedField(proto.STRING, number=2,)
    enrolled_services = proto.RepeatedField(
        proto.MESSAGE, number=3, message="EnrolledService",
    )
    enrolled_ancestor = proto.Field(proto.BOOL, number=4,)


class ListApprovalRequestsMessage(proto.Message):
    r"""Request to list approval requests.
    Attributes:
        parent (str):
            The parent resource. This may be "projects/{project_id}",
            "folders/{folder_id}", or "organizations/{organization_id}".
        filter (str):
            A filter on the type of approval requests to retrieve. Must
            be one of the following values:

            -  [not set]: Requests that are pending or have active
               approvals.
            -  ALL: All requests.
            -  PENDING: Only pending requests.
            -  ACTIVE: Only active (i.e. currently approved) requests.
            -  DISMISSED: Only dismissed (including expired) requests.
        page_size (int):
            Requested page size.
        page_token (str):
            A token identifying the page of results to
            return.
    """

    parent = proto.Field(proto.STRING, number=1,)
    filter = proto.Field(proto.STRING, number=2,)
    page_size = proto.Field(proto.INT32, number=3,)
    page_token = proto.Field(proto.STRING, number=4,)


class ListApprovalRequestsResponse(proto.Message):
    r"""Response to listing of ApprovalRequest objects.
    Attributes:
        approval_requests (Sequence[google.cloud.accessapproval_v1.types.ApprovalRequest]):
            Approval request details.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more.
    """

    @property
    def raw_page(self):
        return self

    approval_requests = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ApprovalRequest",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetApprovalRequestMessage(proto.Message):
    r"""Request to get an approval request.
    Attributes:
        name (str):
            Name of the approval request to retrieve.
    """

    name = proto.Field(proto.STRING, number=1,)


class ApproveApprovalRequestMessage(proto.Message):
    r"""Request to approve an ApprovalRequest.
    Attributes:
        name (str):
            Name of the approval request to approve.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            The expiration time of this approval.
    """

    name = proto.Field(proto.STRING, number=1,)
    expire_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)


class DismissApprovalRequestMessage(proto.Message):
    r"""Request to dismiss an approval request.
    Attributes:
        name (str):
            Name of the ApprovalRequest to dismiss.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetAccessApprovalSettingsMessage(proto.Message):
    r"""Request to get access approval settings.
    Attributes:
        name (str):
            Name of the AccessApprovalSettings to
            retrieve.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateAccessApprovalSettingsMessage(proto.Message):
    r"""Request to update access approval settings.
    Attributes:
        settings (google.cloud.accessapproval_v1.types.AccessApprovalSettings):
            The new AccessApprovalSettings.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The update mask applies to the settings. Only the top level
            fields of AccessApprovalSettings (notification_emails &
            enrolled_services) are supported. For each field, if it is
            included, the currently stored value will be entirely
            overwritten with the value of the field passed in this
            request.

            For the ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
            If this field is left unset, only the notification_emails
            field will be updated.
    """

    settings = proto.Field(proto.MESSAGE, number=1, message="AccessApprovalSettings",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteAccessApprovalSettingsMessage(proto.Message):
    r"""Request to delete access approval settings.
    Attributes:
        name (str):
            Name of the AccessApprovalSettings to delete.
    """

    name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
