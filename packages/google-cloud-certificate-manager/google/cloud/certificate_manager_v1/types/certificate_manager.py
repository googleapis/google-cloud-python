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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.certificatemanager.v1",
    manifest={
        "ServingState",
        "ListCertificatesRequest",
        "ListCertificatesResponse",
        "GetCertificateRequest",
        "CreateCertificateRequest",
        "UpdateCertificateRequest",
        "DeleteCertificateRequest",
        "ListCertificateMapsRequest",
        "ListCertificateMapsResponse",
        "GetCertificateMapRequest",
        "CreateCertificateMapRequest",
        "UpdateCertificateMapRequest",
        "DeleteCertificateMapRequest",
        "ListCertificateMapEntriesRequest",
        "ListCertificateMapEntriesResponse",
        "GetCertificateMapEntryRequest",
        "CreateCertificateMapEntryRequest",
        "UpdateCertificateMapEntryRequest",
        "DeleteCertificateMapEntryRequest",
        "ListDnsAuthorizationsRequest",
        "ListDnsAuthorizationsResponse",
        "GetDnsAuthorizationRequest",
        "CreateDnsAuthorizationRequest",
        "UpdateDnsAuthorizationRequest",
        "DeleteDnsAuthorizationRequest",
        "OperationMetadata",
        "Certificate",
        "CertificateMap",
        "CertificateMapEntry",
        "DnsAuthorization",
    },
)


class ServingState(proto.Enum):
    r"""Defines set of serving states associated with a resource."""
    SERVING_STATE_UNSPECIFIED = 0
    ACTIVE = 1
    PENDING = 2


class ListCertificatesRequest(proto.Message):
    r"""Request for the ``ListCertificates`` method.

    Attributes:
        parent (str):
            Required. The project and location from which the
            certificate should be listed, specified in the format
            ``projects/*/locations/*``.
        page_size (int):
            Maximum number of certificates to return per
            call.
        page_token (str):
            The value returned by the last ``ListCertificatesResponse``.
            Indicates that this is a continuation of a prior
            ``ListCertificates`` call, and that the system should return
            the next page of data.
        filter (str):
            Filter expression to restrict the
            Certificates returned.
        order_by (str):
            A list of Certificate field names used to
            specify the order of the returned results. The
            default sorting order is ascending. To specify
            descending order for a field, add a suffix "
            desc".
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListCertificatesResponse(proto.Message):
    r"""Response for the ``ListCertificates`` method.

    Attributes:
        certificates (Sequence[google.cloud.certificate_manager_v1.types.Certificate]):
            A list of certificates for the parent
            resource.
        next_page_token (str):
            If there might be more results than those appearing in this
            response, then ``next_page_token`` is included. To get the
            next set of results, call this method again using the value
            of ``next_page_token`` as ``page_token``.
        unreachable (Sequence[str]):
            A list of locations that could not be
            reached.
    """

    @property
    def raw_page(self):
        return self

    certificates = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Certificate",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetCertificateRequest(proto.Message):
    r"""Request for the ``GetCertificate`` method.

    Attributes:
        name (str):
            Required. A name of the certificate to describe. Must be in
            the format ``projects/*/locations/*/certificates/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateCertificateRequest(proto.Message):
    r"""Request for the ``CreateCertificate`` method.

    Attributes:
        parent (str):
            Required. The parent resource of the certificate. Must be in
            the format ``projects/*/locations/*``.
        certificate_id (str):
            Required. A user-provided name of the
            certificate.
        certificate (google.cloud.certificate_manager_v1.types.Certificate):
            Required. A definition of the certificate to
            create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    certificate_id = proto.Field(
        proto.STRING,
        number=2,
    )
    certificate = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Certificate",
    )


class UpdateCertificateRequest(proto.Message):
    r"""Request for the ``UpdateCertificate`` method.

    Attributes:
        certificate (google.cloud.certificate_manager_v1.types.Certificate):
            Required. A definition of the certificate to
            update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The update mask applies to the resource. For the
            ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.
    """

    certificate = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Certificate",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteCertificateRequest(proto.Message):
    r"""Request for the ``DeleteCertificate`` method.

    Attributes:
        name (str):
            Required. A name of the certificate to delete. Must be in
            the format ``projects/*/locations/*/certificates/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCertificateMapsRequest(proto.Message):
    r"""Request for the ``ListCertificateMaps`` method.

    Attributes:
        parent (str):
            Required. The project and location from which the
            certificate maps should be listed, specified in the format
            ``projects/*/locations/*``.
        page_size (int):
            Maximum number of certificate maps to return
            per call.
        page_token (str):
            The value returned by the last
            ``ListCertificateMapsResponse``. Indicates that this is a
            continuation of a prior ``ListCertificateMaps`` call, and
            that the system should return the next page of data.
        filter (str):
            Filter expression to restrict the
            Certificates Maps returned.
        order_by (str):
            A list of Certificate Map field names used to
            specify the order of the returned results. The
            default sorting order is ascending. To specify
            descending order for a field, add a suffix "
            desc".
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListCertificateMapsResponse(proto.Message):
    r"""Response for the ``ListCertificateMaps`` method.

    Attributes:
        certificate_maps (Sequence[google.cloud.certificate_manager_v1.types.CertificateMap]):
            A list of certificate maps for the parent
            resource.
        next_page_token (str):
            If there might be more results than those appearing in this
            response, then ``next_page_token`` is included. To get the
            next set of results, call this method again using the value
            of ``next_page_token`` as ``page_token``.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    certificate_maps = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CertificateMap",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetCertificateMapRequest(proto.Message):
    r"""Request for the ``GetCertificateMap`` method.

    Attributes:
        name (str):
            Required. A name of the certificate map to describe. Must be
            in the format ``projects/*/locations/*/certificateMaps/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateCertificateMapRequest(proto.Message):
    r"""Request for the ``CreateCertificateMap`` method.

    Attributes:
        parent (str):
            Required. The parent resource of the certificate map. Must
            be in the format ``projects/*/locations/*``.
        certificate_map_id (str):
            Required. A user-provided name of the
            certificate map.
        certificate_map (google.cloud.certificate_manager_v1.types.CertificateMap):
            Required. A definition of the certificate map
            to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    certificate_map_id = proto.Field(
        proto.STRING,
        number=2,
    )
    certificate_map = proto.Field(
        proto.MESSAGE,
        number=3,
        message="CertificateMap",
    )


class UpdateCertificateMapRequest(proto.Message):
    r"""Request for the ``UpdateCertificateMap`` method.

    Attributes:
        certificate_map (google.cloud.certificate_manager_v1.types.CertificateMap):
            Required. A definition of the certificate map
            to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The update mask applies to the resource. For the
            ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.
    """

    certificate_map = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CertificateMap",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteCertificateMapRequest(proto.Message):
    r"""Request for the ``DeleteCertificateMap`` method.

    Attributes:
        name (str):
            Required. A name of the certificate map to delete. Must be
            in the format ``projects/*/locations/*/certificateMaps/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCertificateMapEntriesRequest(proto.Message):
    r"""Request for the ``ListCertificateMapEntries`` method.

    Attributes:
        parent (str):
            Required. The project, location and certificate map from
            which the certificate map entries should be listed,
            specified in the format
            ``projects/*/locations/*/certificateMaps/*``.
        page_size (int):
            Maximum number of certificate map entries to
            return. The service may return fewer than this
            value. If unspecified, at most 50 certificate
            map entries will be returned. The maximum value
            is 1000; values above 1000 will be coerced to
            1000.
        page_token (str):
            The value returned by the last
            ``ListCertificateMapEntriesResponse``. Indicates that this
            is a continuation of a prior ``ListCertificateMapEntries``
            call, and that the system should return the next page of
            data.
        filter (str):
            Filter expression to restrict the returned
            Certificate Map Entries.
        order_by (str):
            A list of Certificate Map Entry field names
            used to specify the order of the returned
            results. The default sorting order is ascending.
            To specify descending order for a field, add a
            suffix " desc".
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListCertificateMapEntriesResponse(proto.Message):
    r"""Response for the ``ListCertificateMapEntries`` method.

    Attributes:
        certificate_map_entries (Sequence[google.cloud.certificate_manager_v1.types.CertificateMapEntry]):
            A list of certificate map entries for the
            parent resource.
        next_page_token (str):
            If there might be more results than those appearing in this
            response, then ``next_page_token`` is included. To get the
            next set of results, call this method again using the value
            of ``next_page_token`` as ``page_token``.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    certificate_map_entries = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CertificateMapEntry",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetCertificateMapEntryRequest(proto.Message):
    r"""Request for the ``GetCertificateMapEntry`` method.

    Attributes:
        name (str):
            Required. A name of the certificate map entry to describe.
            Must be in the format
            ``projects/*/locations/*/certificateMaps/*/certificateMapEntries/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateCertificateMapEntryRequest(proto.Message):
    r"""Request for the ``CreateCertificateMapEntry`` method.

    Attributes:
        parent (str):
            Required. The parent resource of the certificate map entry.
            Must be in the format
            ``projects/*/locations/*/certificateMaps/*``.
        certificate_map_entry_id (str):
            Required. A user-provided name of the
            certificate map entry.
        certificate_map_entry (google.cloud.certificate_manager_v1.types.CertificateMapEntry):
            Required. A definition of the certificate map
            entry to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    certificate_map_entry_id = proto.Field(
        proto.STRING,
        number=2,
    )
    certificate_map_entry = proto.Field(
        proto.MESSAGE,
        number=3,
        message="CertificateMapEntry",
    )


class UpdateCertificateMapEntryRequest(proto.Message):
    r"""Request for the ``UpdateCertificateMapEntry`` method.

    Attributes:
        certificate_map_entry (google.cloud.certificate_manager_v1.types.CertificateMapEntry):
            Required. A definition of the certificate map
            entry to create map entry.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The update mask applies to the resource. For the
            ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.
    """

    certificate_map_entry = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CertificateMapEntry",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteCertificateMapEntryRequest(proto.Message):
    r"""Request for the ``DeleteCertificateMapEntry`` method.

    Attributes:
        name (str):
            Required. A name of the certificate map entry to delete.
            Must be in the format
            ``projects/*/locations/*/certificateMaps/*/certificateMapEntries/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListDnsAuthorizationsRequest(proto.Message):
    r"""Request for the ``ListDnsAuthorizations`` method.

    Attributes:
        parent (str):
            Required. The project and location from which the dns
            authorizations should be listed, specified in the format
            ``projects/*/locations/*``.
        page_size (int):
            Maximum number of dns authorizations to
            return per call.
        page_token (str):
            The value returned by the last
            ``ListDnsAuthorizationsResponse``. Indicates that this is a
            continuation of a prior ``ListDnsAuthorizations`` call, and
            that the system should return the next page of data.
        filter (str):
            Filter expression to restrict the Dns
            Authorizations returned.
        order_by (str):
            A list of Dns Authorization field names used
            to specify the order of the returned results.
            The default sorting order is ascending. To
            specify descending order for a field, add a
            suffix " desc".
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    filter = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by = proto.Field(
        proto.STRING,
        number=5,
    )


class ListDnsAuthorizationsResponse(proto.Message):
    r"""Response for the ``ListDnsAuthorizations`` method.

    Attributes:
        dns_authorizations (Sequence[google.cloud.certificate_manager_v1.types.DnsAuthorization]):
            A list of dns authorizations for the parent
            resource.
        next_page_token (str):
            If there might be more results than those appearing in this
            response, then ``next_page_token`` is included. To get the
            next set of results, call this method again using the value
            of ``next_page_token`` as ``page_token``.
        unreachable (Sequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    dns_authorizations = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DnsAuthorization",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetDnsAuthorizationRequest(proto.Message):
    r"""Request for the ``GetDnsAuthorization`` method.

    Attributes:
        name (str):
            Required. A name of the dns authorization to describe. Must
            be in the format
            ``projects/*/locations/*/dnsAuthorizations/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateDnsAuthorizationRequest(proto.Message):
    r"""Request for the ``CreateDnsAuthorization`` method.

    Attributes:
        parent (str):
            Required. The parent resource of the dns authorization. Must
            be in the format ``projects/*/locations/*``.
        dns_authorization_id (str):
            Required. A user-provided name of the dns
            authorization.
        dns_authorization (google.cloud.certificate_manager_v1.types.DnsAuthorization):
            Required. A definition of the dns
            authorization to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    dns_authorization_id = proto.Field(
        proto.STRING,
        number=2,
    )
    dns_authorization = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DnsAuthorization",
    )


class UpdateDnsAuthorizationRequest(proto.Message):
    r"""Request for the ``UpdateDnsAuthorization`` method.

    Attributes:
        dns_authorization (google.cloud.certificate_manager_v1.types.DnsAuthorization):
            Required. A definition of the dns
            authorization to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The update mask applies to the resource. For the
            ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.
    """

    dns_authorization = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DnsAuthorization",
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteDnsAuthorizationRequest(proto.Message):
    r"""Request for the ``DeleteDnsAuthorization`` method.

    Attributes:
        name (str):
            Required. A name of the dns authorization to delete. Must be
            in the format
            ``projects/*/locations/*/dnsAuthorizations/*``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation. Output
    only.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished running.
        target (str):
            Server-defined resource path for the target
            of the operation.
        verb (str):
            Name of the verb executed by the operation.
        status_message (str):
            Human-readable status of the operation, if
            any.
        requested_cancellation (bool):
            Identifies whether the user has requested cancellation of
            the operation. Operations that have successfully been
            cancelled have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            API version used to start the operation.
    """

    create_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target = proto.Field(
        proto.STRING,
        number=3,
    )
    verb = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version = proto.Field(
        proto.STRING,
        number=7,
    )


class Certificate(proto.Message):
    r"""Defines TLS certificate.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            A user-defined name of the certificate. Certificate names
            must be unique globally and match pattern
            ``projects/*/locations/*/certificates/*``.
        description (str):
            One or more paragraphs of text description of
            a certificate.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of a
            Certificate.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update timestamp of a
            Certificate.
        labels (Sequence[google.cloud.certificate_manager_v1.types.Certificate.LabelsEntry]):
            Set of labels associated with a Certificate.
        self_managed (google.cloud.certificate_manager_v1.types.Certificate.SelfManagedCertificate):
            If set, defines data of a self-managed
            certificate.

            This field is a member of `oneof`_ ``type``.
        managed (google.cloud.certificate_manager_v1.types.Certificate.ManagedCertificate):
            If set, contains configuration and state of a
            managed certificate.

            This field is a member of `oneof`_ ``type``.
        san_dnsnames (Sequence[str]):
            Output only. The list of Subject Alternative
            Names of dnsName type defined in the certificate
            (see RFC 5280 4.2.1.6). Managed certificates
            that haven't been provisioned yet have this
            field populated with a value of the
            managed.domains field.
        pem_certificate (str):
            Output only. The PEM-encoded certificate
            chain.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The expiry timestamp of a
            Certificate.
        scope (google.cloud.certificate_manager_v1.types.Certificate.Scope):
            Immutable. The scope of the certificate.
    """

    class Scope(proto.Enum):
        r"""Certificate scope."""
        DEFAULT = 0
        EDGE_CACHE = 1

    class SelfManagedCertificate(proto.Message):
        r"""Certificate data for a SelfManaged Certificate.
        SelfManaged Certificates are uploaded by the user. Updating such
        certificates before they expire remains the user's
        responsibility.

        Attributes:
            pem_certificate (str):
                Input only. The PEM-encoded certificate
                chain. Leaf certificate comes first, followed by
                intermediate ones if any.
            pem_private_key (str):
                Input only. The PEM-encoded private key of
                the leaf certificate.
        """

        pem_certificate = proto.Field(
            proto.STRING,
            number=1,
        )
        pem_private_key = proto.Field(
            proto.STRING,
            number=2,
        )

    class ManagedCertificate(proto.Message):
        r"""Configuration and state of a Managed Certificate.
        Certificate Manager provisions and renews Managed Certificates
        automatically, for as long as it's authorized to do so.

        Attributes:
            domains (Sequence[str]):
                Immutable. The domains for which a managed
                SSL certificate will be generated. Wildcard
                domains are only supported with DNS challenge
                resolution.
            dns_authorizations (Sequence[str]):
                Immutable. Authorizations that will be used
                for performing domain authorization.
            state (google.cloud.certificate_manager_v1.types.Certificate.ManagedCertificate.State):
                Output only. State of the managed certificate
                resource.
            provisioning_issue (google.cloud.certificate_manager_v1.types.Certificate.ManagedCertificate.ProvisioningIssue):
                Information about issues with provisioning a
                Managed Certificate.
            authorization_attempt_info (Sequence[google.cloud.certificate_manager_v1.types.Certificate.ManagedCertificate.AuthorizationAttemptInfo]):
                Output only. Detailed state of the latest
                authorization attempt for each domain specified
                for managed certificate resource.
        """

        class State(proto.Enum):
            r""""""
            STATE_UNSPECIFIED = 0
            PROVISIONING = 1
            FAILED = 2
            ACTIVE = 3

        class ProvisioningIssue(proto.Message):
            r"""Information about issues with provisioning a Managed
            Certificate.

            Attributes:
                reason (google.cloud.certificate_manager_v1.types.Certificate.ManagedCertificate.ProvisioningIssue.Reason):
                    Reason for provisioning failures.
                details (str):
                    Human readable explanation about the issue.
                    Provided to help address the configuration
                    issues. Not guaranteed to be stable. For
                    programmatic access use Reason enum.
            """

            class Reason(proto.Enum):
                r""""""
                REASON_UNSPECIFIED = 0
                AUTHORIZATION_ISSUE = 1
                RATE_LIMITED = 2

            reason = proto.Field(
                proto.ENUM,
                number=1,
                enum="Certificate.ManagedCertificate.ProvisioningIssue.Reason",
            )
            details = proto.Field(
                proto.STRING,
                number=2,
            )

        class AuthorizationAttemptInfo(proto.Message):
            r"""State of the latest attempt to authorize a domain for
            certificate issuance.

            Attributes:
                domain (str):
                    Domain name of the authorization attempt.
                state (google.cloud.certificate_manager_v1.types.Certificate.ManagedCertificate.AuthorizationAttemptInfo.State):
                    State of the domain for managed certificate
                    issuance.
                failure_reason (google.cloud.certificate_manager_v1.types.Certificate.ManagedCertificate.AuthorizationAttemptInfo.FailureReason):
                    Output only. Reason for failure of the
                    authorization attempt for the domain.
                details (str):
                    Human readable explanation for reaching the
                    state. Provided to help address the
                    configuration issues. Not guaranteed to be
                    stable. For programmatic access use Reason enum.
            """

            class State(proto.Enum):
                r""""""
                STATE_UNSPECIFIED = 0
                AUTHORIZING = 1
                AUTHORIZED = 6
                FAILED = 7

            class FailureReason(proto.Enum):
                r""""""
                FAILURE_REASON_UNSPECIFIED = 0
                CONFIG = 1
                CAA = 2
                RATE_LIMITED = 3

            domain = proto.Field(
                proto.STRING,
                number=1,
            )
            state = proto.Field(
                proto.ENUM,
                number=2,
                enum="Certificate.ManagedCertificate.AuthorizationAttemptInfo.State",
            )
            failure_reason = proto.Field(
                proto.ENUM,
                number=3,
                enum="Certificate.ManagedCertificate.AuthorizationAttemptInfo.FailureReason",
            )
            details = proto.Field(
                proto.STRING,
                number=4,
            )

        domains = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        dns_authorizations = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        state = proto.Field(
            proto.ENUM,
            number=4,
            enum="Certificate.ManagedCertificate.State",
        )
        provisioning_issue = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Certificate.ManagedCertificate.ProvisioningIssue",
        )
        authorization_attempt_info = proto.RepeatedField(
            proto.MESSAGE,
            number=5,
            message="Certificate.ManagedCertificate.AuthorizationAttemptInfo",
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=8,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    self_managed = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="type",
        message=SelfManagedCertificate,
    )
    managed = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="type",
        message=ManagedCertificate,
    )
    san_dnsnames = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    pem_certificate = proto.Field(
        proto.STRING,
        number=9,
    )
    expire_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    scope = proto.Field(
        proto.ENUM,
        number=12,
        enum=Scope,
    )


class CertificateMap(proto.Message):
    r"""Defines a collection of certificate configurations.

    Attributes:
        name (str):
            A user-defined name of the Certificate Map. Certificate Map
            names must be unique globally and match pattern
            ``projects/*/locations/*/certificateMaps/*``.
        description (str):
            One or more paragraphs of text description of
            a certificate map.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of a
            Certificate Map.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update timestamp of a
            Certificate Map.
        labels (Sequence[google.cloud.certificate_manager_v1.types.CertificateMap.LabelsEntry]):
            Set of labels associated with a Certificate
            Map.
        gclb_targets (Sequence[google.cloud.certificate_manager_v1.types.CertificateMap.GclbTarget]):
            Output only. A list of GCLB targets which use
            this Certificate Map.
    """

    class GclbTarget(proto.Message):
        r"""Describes a Target Proxy which uses this Certificate Map.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            target_https_proxy (str):
                A name must be in the format
                ``projects/*/locations/*/targetHttpsProxies/*``.

                This field is a member of `oneof`_ ``target_proxy``.
            target_ssl_proxy (str):
                A name must be in the format
                ``projects/*/locations/*/targetSslProxies/*``.

                This field is a member of `oneof`_ ``target_proxy``.
            ip_configs (Sequence[google.cloud.certificate_manager_v1.types.CertificateMap.GclbTarget.IpConfig]):
                IP configurations for this Target Proxy where
                the Certificate Map is serving.
        """

        class IpConfig(proto.Message):
            r"""Defines IP configuration where this Certificate Map is
            serving.

            Attributes:
                ip_address (str):
                    An external IP address.
                ports (Sequence[int]):
                    Ports.
            """

            ip_address = proto.Field(
                proto.STRING,
                number=1,
            )
            ports = proto.RepeatedField(
                proto.UINT32,
                number=3,
            )

        target_https_proxy = proto.Field(
            proto.STRING,
            number=1,
            oneof="target_proxy",
        )
        target_ssl_proxy = proto.Field(
            proto.STRING,
            number=3,
            oneof="target_proxy",
        )
        ip_configs = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="CertificateMap.GclbTarget.IpConfig",
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=5,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )
    gclb_targets = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=GclbTarget,
    )


class CertificateMapEntry(proto.Message):
    r"""Defines a certificate map entry.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            A user-defined name of the Certificate Map Entry.
            Certificate Map Entry names must be unique globally and
            match pattern
            ``projects/*/locations/*/certificateMaps/*/certificateMapEntries/*``.
        description (str):
            One or more paragraphs of text description of
            a certificate map entry.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of a
            Certificate Map Entry.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The update timestamp of a
            Certificate Map Entry.
        labels (Sequence[google.cloud.certificate_manager_v1.types.CertificateMapEntry.LabelsEntry]):
            Set of labels associated with a Certificate
            Map Entry.
        hostname (str):
            A Hostname (FQDN, e.g. ``example.com``) or a wildcard
            hostname expression (``*.example.com``) for a set of
            hostnames with common suffix. Used as Server Name Indication
            (SNI) for selecting a proper certificate.

            This field is a member of `oneof`_ ``match``.
        matcher (google.cloud.certificate_manager_v1.types.CertificateMapEntry.Matcher):
            A predefined matcher for particular cases,
            other than SNI selection.

            This field is a member of `oneof`_ ``match``.
        certificates (Sequence[str]):
            A set of Certificates defines for the given ``hostname``.
            There can be defined up to fifteen certificates in each
            Certificate Map Entry. Each certificate must match pattern
            ``projects/*/locations/*/certificates/*``.
        state (google.cloud.certificate_manager_v1.types.ServingState):
            Output only. A serving state of this
            Certificate Map Entry.
    """

    class Matcher(proto.Enum):
        r"""Defines predefined cases other than SNI-hostname match when
        this configuration should be applied.
        """
        MATCHER_UNSPECIFIED = 0
        PRIMARY = 1

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    description = proto.Field(
        proto.STRING,
        number=9,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    hostname = proto.Field(
        proto.STRING,
        number=5,
        oneof="match",
    )
    matcher = proto.Field(
        proto.ENUM,
        number=10,
        oneof="match",
        enum=Matcher,
    )
    certificates = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    state = proto.Field(
        proto.ENUM,
        number=8,
        enum="ServingState",
    )


class DnsAuthorization(proto.Message):
    r"""A DnsAuthorization resource describes a way to perform domain
    authorization for certificate issuance.

    Attributes:
        name (str):
            A user-defined name of the dns authorization.
            DnsAuthorization names must be unique globally and match
            pattern ``projects/*/locations/*/dnsAuthorizations/*``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of a
            DnsAuthorization.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update timestamp of a
            DnsAuthorization.
        labels (Sequence[google.cloud.certificate_manager_v1.types.DnsAuthorization.LabelsEntry]):
            Set of labels associated with a
            DnsAuthorization.
        description (str):
            One or more paragraphs of text description of
            a DnsAuthorization.
        domain (str):
            Required. Immutable. A domain which is being authorized. A
            DnsAuthorization resource covers a single domain and its
            wildcard, e.g. authorization for ``example.com`` can be used
            to issue certificates for ``example.com`` and
            ``*.example.com``.
        dns_resource_record (google.cloud.certificate_manager_v1.types.DnsAuthorization.DnsResourceRecord):
            Output only. DNS Resource Record that needs
            to be added to DNS configuration.
    """

    class DnsResourceRecord(proto.Message):
        r"""The structure describing the DNS Resource Record that needs
        to be added to DNS configuration for the authorization to be
        usable by certificate.

        Attributes:
            name (str):
                Output only. Fully qualified name of the DNS Resource
                Record. e.g. ``_acme-challenge.example.com``
            type_ (str):
                Output only. Type of the DNS Resource Record.
                Currently always set to "CNAME".
            data (str):
                Output only. Data of the DNS Resource Record.
        """

        name = proto.Field(
            proto.STRING,
            number=1,
        )
        type_ = proto.Field(
            proto.STRING,
            number=2,
        )
        data = proto.Field(
            proto.STRING,
            number=3,
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    description = proto.Field(
        proto.STRING,
        number=5,
    )
    domain = proto.Field(
        proto.STRING,
        number=6,
    )
    dns_resource_record = proto.Field(
        proto.MESSAGE,
        number=10,
        message=DnsResourceRecord,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
