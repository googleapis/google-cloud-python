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
from google.type import money_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.domains.v1beta1",
    manifest={
        "ContactPrivacy",
        "DomainNotice",
        "ContactNotice",
        "TransferLockState",
        "Registration",
        "ManagementSettings",
        "DnsSettings",
        "ContactSettings",
        "SearchDomainsRequest",
        "SearchDomainsResponse",
        "RetrieveRegisterParametersRequest",
        "RetrieveRegisterParametersResponse",
        "RegisterDomainRequest",
        "ListRegistrationsRequest",
        "ListRegistrationsResponse",
        "GetRegistrationRequest",
        "UpdateRegistrationRequest",
        "ConfigureManagementSettingsRequest",
        "ConfigureDnsSettingsRequest",
        "ConfigureContactSettingsRequest",
        "ExportRegistrationRequest",
        "DeleteRegistrationRequest",
        "RetrieveAuthorizationCodeRequest",
        "ResetAuthorizationCodeRequest",
        "RegisterParameters",
        "AuthorizationCode",
        "OperationMetadata",
    },
)


class ContactPrivacy(proto.Enum):
    r"""Defines a set of possible contact privacy settings for a
    ``Registration``.

    `ICANN <https://icann.org/>`__ maintains the WHOIS database, a
    publicly accessible mapping from domain name to contact information,
    and requires that each domain name have an entry. Choose from these
    options to control how much information in your ``ContactSettings``
    is published.
    """
    CONTACT_PRIVACY_UNSPECIFIED = 0
    PUBLIC_CONTACT_DATA = 1
    PRIVATE_CONTACT_DATA = 2
    REDACTED_CONTACT_DATA = 3


class DomainNotice(proto.Enum):
    r"""Notices about special properties of certain domains."""
    DOMAIN_NOTICE_UNSPECIFIED = 0
    HSTS_PRELOADED = 1


class ContactNotice(proto.Enum):
    r"""Notices related to contact information."""
    CONTACT_NOTICE_UNSPECIFIED = 0
    PUBLIC_CONTACT_DATA_ACKNOWLEDGEMENT = 1


class TransferLockState(proto.Enum):
    r"""Possible states of a ``Registration``'s transfer lock."""
    TRANSFER_LOCK_STATE_UNSPECIFIED = 0
    UNLOCKED = 1
    LOCKED = 2


class Registration(proto.Message):
    r"""The ``Registration`` resource facilitates managing and configuring
    domain name registrations.

    To create a new ``Registration`` resource, find a suitable domain
    name by calling the ``SearchDomains`` method with a query to see
    available domain name options. After choosing a name, call
    ``RetrieveRegisterParameters`` to ensure availability and obtain
    information like pricing, which is needed to build a call to
    ``RegisterDomain``.

    Attributes:
        name (str):
            Output only. Name of the ``Registration`` resource, in the
            format
            ``projects/*/locations/*/registrations/<domain_name>``.
        domain_name (str):
            Required. Immutable. The domain name. Unicode
            domain names must be expressed in Punycode
            format.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation timestamp of the ``Registration``
            resource.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The expiration timestamp of the
            ``Registration``.
        state (google.cloud.domains_v1beta1.types.Registration.State):
            Output only. The state of the ``Registration``
        issues (Sequence[google.cloud.domains_v1beta1.types.Registration.Issue]):
            Output only. The set of issues with the ``Registration``
            that require attention.
        labels (Sequence[google.cloud.domains_v1beta1.types.Registration.LabelsEntry]):
            Set of labels associated with the ``Registration``.
        management_settings (google.cloud.domains_v1beta1.types.ManagementSettings):
            Settings for management of the ``Registration``, including
            renewal, billing, and transfer. You cannot update these with
            the ``UpdateRegistration`` method. To update these settings,
            use the ``ConfigureManagementSettings`` method.
        dns_settings (google.cloud.domains_v1beta1.types.DnsSettings):
            Settings controlling the DNS configuration of the
            ``Registration``. You cannot update these with the
            ``UpdateRegistration`` method. To update these settings, use
            the ``ConfigureDnsSettings`` method.
        contact_settings (google.cloud.domains_v1beta1.types.ContactSettings):
            Required. Settings for contact information linked to the
            ``Registration``. You cannot update these with the
            ``UpdateRegistration`` method. To update these settings, use
            the ``ConfigureContactSettings`` method.
        pending_contact_settings (google.cloud.domains_v1beta1.types.ContactSettings):
            Output only. Pending contact settings for the
            ``Registration``. Updates to the ``contact_settings`` field
            that change its ``registrant_contact`` or ``privacy`` fields
            require email confirmation by the ``registrant_contact``
            before taking effect. This field is set only if there are
            pending updates to the ``contact_settings`` that have not
            yet been confirmed. To confirm the changes, the
            ``registrant_contact`` must follow the instructions in the
            email they receive.
        supported_privacy (Sequence[google.cloud.domains_v1beta1.types.ContactPrivacy]):
            Output only. Set of options for the
            ``contact_settings.privacy`` field that this
            ``Registration`` supports.
    """

    class State(proto.Enum):
        r"""Possible states of a ``Registration``."""
        STATE_UNSPECIFIED = 0
        REGISTRATION_PENDING = 1
        REGISTRATION_FAILED = 2
        ACTIVE = 6
        SUSPENDED = 7
        EXPORTED = 8

    class Issue(proto.Enum):
        r"""Possible issues with a ``Registration`` that require attention."""
        ISSUE_UNSPECIFIED = 0
        CONTACT_SUPPORT = 1
        UNVERIFIED_EMAIL = 2

    name = proto.Field(proto.STRING, number=1,)
    domain_name = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    expire_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    state = proto.Field(proto.ENUM, number=7, enum=State,)
    issues = proto.RepeatedField(proto.ENUM, number=8, enum=Issue,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=9,)
    management_settings = proto.Field(
        proto.MESSAGE, number=10, message="ManagementSettings",
    )
    dns_settings = proto.Field(proto.MESSAGE, number=11, message="DnsSettings",)
    contact_settings = proto.Field(proto.MESSAGE, number=12, message="ContactSettings",)
    pending_contact_settings = proto.Field(
        proto.MESSAGE, number=13, message="ContactSettings",
    )
    supported_privacy = proto.RepeatedField(
        proto.ENUM, number=14, enum="ContactPrivacy",
    )


class ManagementSettings(proto.Message):
    r"""Defines renewal, billing, and transfer settings for a
    ``Registration``.

    Attributes:
        renewal_method (google.cloud.domains_v1beta1.types.ManagementSettings.RenewalMethod):
            Output only. The renewal method for this ``Registration``.
        transfer_lock_state (google.cloud.domains_v1beta1.types.TransferLockState):
            Controls whether the domain can be
            transferred to another registrar.
    """

    class RenewalMethod(proto.Enum):
        r"""Defines how the ``Registration`` is renewed."""
        RENEWAL_METHOD_UNSPECIFIED = 0
        AUTOMATIC_RENEWAL = 1
        MANUAL_RENEWAL = 2

    renewal_method = proto.Field(proto.ENUM, number=3, enum=RenewalMethod,)
    transfer_lock_state = proto.Field(proto.ENUM, number=4, enum="TransferLockState",)


class DnsSettings(proto.Message):
    r"""Defines the DNS configuration of a ``Registration``, including name
    servers, DNSSEC, and glue records.

    Attributes:
        custom_dns (google.cloud.domains_v1beta1.types.DnsSettings.CustomDns):
            An arbitrary DNS provider identified by its
            name servers.
        google_domains_dns (google.cloud.domains_v1beta1.types.DnsSettings.GoogleDomainsDns):
            The free DNS zone provided by `Google
            Domains <https://domains.google/>`__.
        glue_records (Sequence[google.cloud.domains_v1beta1.types.DnsSettings.GlueRecord]):
            The list of glue records for this ``Registration``. Commonly
            empty.
    """

    class DsState(proto.Enum):
        r"""The publication state of DS records for a ``Registration``."""
        DS_STATE_UNSPECIFIED = 0
        DS_RECORDS_UNPUBLISHED = 1
        DS_RECORDS_PUBLISHED = 2

    class CustomDns(proto.Message):
        r"""Configuration for an arbitrary DNS provider.
        Attributes:
            name_servers (Sequence[str]):
                Required. A list of name servers that store
                the DNS zone for this domain. Each name server
                is a domain name, with Unicode domain names
                expressed in Punycode format.
            ds_records (Sequence[google.cloud.domains_v1beta1.types.DnsSettings.DsRecord]):
                The list of DS records for this domain, which
                are used to enable DNSSEC. The domain's DNS
                provider can provide the values to set here. If
                this field is empty, DNSSEC is disabled.
        """

        name_servers = proto.RepeatedField(proto.STRING, number=1,)
        ds_records = proto.RepeatedField(
            proto.MESSAGE, number=2, message="DnsSettings.DsRecord",
        )

    class GoogleDomainsDns(proto.Message):
        r"""Configuration for using the free DNS zone provided by Google Domains
        as a ``Registration``'s ``dns_provider``. You cannot configure the
        DNS zone itself using the API. To configure the DNS zone, go to
        `Google Domains <https://domains.google/>`__.

        Attributes:
            name_servers (Sequence[str]):
                Output only. A list of name servers that
                store the DNS zone for this domain. Each name
                server is a domain name, with Unicode domain
                names expressed in Punycode format. This field
                is automatically populated with the name servers
                assigned to the Google Domains DNS zone.
            ds_state (google.cloud.domains_v1beta1.types.DnsSettings.DsState):
                Required. The state of DS records for this
                domain. Used to enable or disable automatic
                DNSSEC.
            ds_records (Sequence[google.cloud.domains_v1beta1.types.DnsSettings.DsRecord]):
                Output only. The list of DS records published for this
                domain. The list is automatically populated when
                ``ds_state`` is ``DS_RECORDS_PUBLISHED``, otherwise it
                remains empty.
        """

        name_servers = proto.RepeatedField(proto.STRING, number=1,)
        ds_state = proto.Field(proto.ENUM, number=2, enum="DnsSettings.DsState",)
        ds_records = proto.RepeatedField(
            proto.MESSAGE, number=3, message="DnsSettings.DsRecord",
        )

    class DsRecord(proto.Message):
        r"""Defines a Delegation Signer (DS) record, which is needed to
        enable DNSSEC for a domain. It contains a digest (hash) of a
        DNSKEY record that must be present in the domain's DNS zone.

        Attributes:
            key_tag (int):
                The key tag of the record. Must be set in
                range 0 -- 65535.
            algorithm (google.cloud.domains_v1beta1.types.DnsSettings.DsRecord.Algorithm):
                The algorithm used to generate the referenced
                DNSKEY.
            digest_type (google.cloud.domains_v1beta1.types.DnsSettings.DsRecord.DigestType):
                The hash function used to generate the digest
                of the referenced DNSKEY.
            digest (str):
                The digest generated from the referenced
                DNSKEY.
        """

        class Algorithm(proto.Enum):
            r"""List of algorithms used to create a DNSKEY. Certain
            algorithms are not supported for particular domains.
            """
            ALGORITHM_UNSPECIFIED = 0
            DSA = 3
            ECC = 4
            RSASHA1 = 5
            DSANSEC3SHA1 = 6
            RSASHA1NSEC3SHA1 = 7
            RSASHA256 = 8
            RSASHA512 = 10
            ECCGOST = 12
            ECDSAP256SHA256 = 13
            ECDSAP384SHA384 = 14
            ED25519 = 15
            ED448 = 16

        class DigestType(proto.Enum):
            r"""List of hash functions that may have been used to generate a
            digest of a DNSKEY.
            """
            DIGEST_TYPE_UNSPECIFIED = 0
            SHA1 = 1
            SHA256 = 2
            GOST3411 = 3
            SHA384 = 4

        key_tag = proto.Field(proto.INT32, number=1,)
        algorithm = proto.Field(
            proto.ENUM, number=2, enum="DnsSettings.DsRecord.Algorithm",
        )
        digest_type = proto.Field(
            proto.ENUM, number=3, enum="DnsSettings.DsRecord.DigestType",
        )
        digest = proto.Field(proto.STRING, number=4,)

    class GlueRecord(proto.Message):
        r"""Defines a host on your domain that is a DNS name server for your
        domain and/or other domains. Glue records are a way of making the IP
        address of a name server known, even when it serves DNS queries for
        its parent domain. For example, when ``ns.example.com`` is a name
        server for ``example.com``, the host ``ns.example.com`` must have a
        glue record to break the circular DNS reference.

        Attributes:
            host_name (str):
                Required. Domain name of the host in Punycode
                format.
            ipv4_addresses (Sequence[str]):
                List of IPv4 addresses corresponding to this host in the
                standard decimal format (e.g. ``198.51.100.1``). At least
                one of ``ipv4_address`` and ``ipv6_address`` must be set.
            ipv6_addresses (Sequence[str]):
                List of IPv6 addresses corresponding to this host in the
                standard hexadecimal format (e.g. ``2001:db8::``). At least
                one of ``ipv4_address`` and ``ipv6_address`` must be set.
        """

        host_name = proto.Field(proto.STRING, number=1,)
        ipv4_addresses = proto.RepeatedField(proto.STRING, number=2,)
        ipv6_addresses = proto.RepeatedField(proto.STRING, number=3,)

    custom_dns = proto.Field(
        proto.MESSAGE, number=1, oneof="dns_provider", message=CustomDns,
    )
    google_domains_dns = proto.Field(
        proto.MESSAGE, number=2, oneof="dns_provider", message=GoogleDomainsDns,
    )
    glue_records = proto.RepeatedField(proto.MESSAGE, number=4, message=GlueRecord,)


class ContactSettings(proto.Message):
    r"""Defines the contact information associated with a ``Registration``.

    `ICANN <https://icann.org/>`__ requires all domain names to have
    associated contact information. The ``registrant_contact`` is
    considered the domain's legal owner, and often the other contacts
    are identical.

    Attributes:
        privacy (google.cloud.domains_v1beta1.types.ContactPrivacy):
            Required. Privacy setting for the contacts associated with
            the ``Registration``.
        registrant_contact (google.cloud.domains_v1beta1.types.ContactSettings.Contact):
            Required. The registrant contact for the ``Registration``.

            *Caution: Anyone with access to this email address, phone
            number, and/or postal address can take control of the
            domain.*

            *Warning: For new ``Registration``\ s, the registrant will
            receive an email confirmation that they must complete within
            14 days to avoid domain suspension.*
        admin_contact (google.cloud.domains_v1beta1.types.ContactSettings.Contact):
            Required. The administrative contact for the
            ``Registration``.
        technical_contact (google.cloud.domains_v1beta1.types.ContactSettings.Contact):
            Required. The technical contact for the ``Registration``.
    """

    class Contact(proto.Message):
        r"""Details required for a contact associated with a ``Registration``.
        Attributes:
            postal_address (google.type.postal_address_pb2.PostalAddress):
                Required. Postal address of the contact.
            email (str):
                Required. Email address of the contact.
            phone_number (str):
                Required. Phone number of the contact in international
                format. For example, ``"+1-800-555-0123"``.
            fax_number (str):
                Fax number of the contact in international format. For
                example, ``"+1-800-555-0123"``.
        """

        postal_address = proto.Field(
            proto.MESSAGE, number=1, message=postal_address_pb2.PostalAddress,
        )
        email = proto.Field(proto.STRING, number=2,)
        phone_number = proto.Field(proto.STRING, number=3,)
        fax_number = proto.Field(proto.STRING, number=4,)

    privacy = proto.Field(proto.ENUM, number=1, enum="ContactPrivacy",)
    registrant_contact = proto.Field(proto.MESSAGE, number=2, message=Contact,)
    admin_contact = proto.Field(proto.MESSAGE, number=3, message=Contact,)
    technical_contact = proto.Field(proto.MESSAGE, number=4, message=Contact,)


class SearchDomainsRequest(proto.Message):
    r"""Request for the ``SearchDomains`` method.
    Attributes:
        query (str):
            Required. String used to search for available
            domain names.
        location (str):
            Required. The location. Must be in the format
            ``projects/*/locations/*``.
    """

    query = proto.Field(proto.STRING, number=1,)
    location = proto.Field(proto.STRING, number=2,)


class SearchDomainsResponse(proto.Message):
    r"""Response for the ``SearchDomains`` method.
    Attributes:
        register_parameters (Sequence[google.cloud.domains_v1beta1.types.RegisterParameters]):
            Results of the domain name search.
    """

    register_parameters = proto.RepeatedField(
        proto.MESSAGE, number=1, message="RegisterParameters",
    )


class RetrieveRegisterParametersRequest(proto.Message):
    r"""Request for the ``RetrieveRegisterParameters`` method.
    Attributes:
        domain_name (str):
            Required. The domain name. Unicode domain
            names must be expressed in Punycode format.
        location (str):
            Required. The location. Must be in the format
            ``projects/*/locations/*``.
    """

    domain_name = proto.Field(proto.STRING, number=1,)
    location = proto.Field(proto.STRING, number=2,)


class RetrieveRegisterParametersResponse(proto.Message):
    r"""Response for the ``RetrieveRegisterParameters`` method.
    Attributes:
        register_parameters (google.cloud.domains_v1beta1.types.RegisterParameters):
            Parameters to use when calling the ``RegisterDomain``
            method.
    """

    register_parameters = proto.Field(
        proto.MESSAGE, number=1, message="RegisterParameters",
    )


class RegisterDomainRequest(proto.Message):
    r"""Request for the ``RegisterDomain`` method.
    Attributes:
        parent (str):
            Required. The parent resource of the ``Registration``. Must
            be in the format ``projects/*/locations/*``.
        registration (google.cloud.domains_v1beta1.types.Registration):
            Required. The complete ``Registration`` resource to be
            created.
        domain_notices (Sequence[google.cloud.domains_v1beta1.types.DomainNotice]):
            The list of domain notices that you acknowledge. Call
            ``RetrieveRegisterParameters`` to see the notices that need
            acknowledgement.
        contact_notices (Sequence[google.cloud.domains_v1beta1.types.ContactNotice]):
            The list of contact notices that the caller acknowledges.
            The notices required here depend on the values specified in
            ``registration.contact_settings``.
        yearly_price (google.type.money_pb2.Money):
            Required. Yearly price to register or renew
            the domain. The value that should be put here
            can be obtained from RetrieveRegisterParameters
            or SearchDomains calls.
        validate_only (bool):
            When true, only validation will be performed, without
            actually registering the domain. Follows:
            https://cloud.google.com/apis/design/design_patterns#request_validation
    """

    parent = proto.Field(proto.STRING, number=1,)
    registration = proto.Field(proto.MESSAGE, number=2, message="Registration",)
    domain_notices = proto.RepeatedField(proto.ENUM, number=3, enum="DomainNotice",)
    contact_notices = proto.RepeatedField(proto.ENUM, number=4, enum="ContactNotice",)
    yearly_price = proto.Field(proto.MESSAGE, number=5, message=money_pb2.Money,)
    validate_only = proto.Field(proto.BOOL, number=6,)


class ListRegistrationsRequest(proto.Message):
    r"""Request for the ``ListRegistrations`` method.
    Attributes:
        parent (str):
            Required. The project and location from which to list
            ``Registration``\ s, specified in the format
            ``projects/*/locations/*``.
        page_size (int):
            Maximum number of results to return.
        page_token (str):
            When set to the ``next_page_token`` from a prior response,
            provides the next page of results.
        filter (str):
            Filter expression to restrict the ``Registration``\ s
            returned.

            The expression must specify the field name, a comparison
            operator, and the value that you want to use for filtering.
            The value must be a string, a number, a boolean, or an enum
            value. The comparison operator should be one of =, !=, >, <,
            >=, <=, or : for prefix or wildcard matches.

            For example, to filter to a specific domain name, use an
            expression like ``domainName="example.com"``. You can also
            check for the existence of a field; for example, to find
            domains using custom DNS settings, use an expression like
            ``dnsSettings.customDns:*``.

            You can also create compound filters by combining
            expressions with the ``AND`` and ``OR`` operators. For
            example, to find domains that are suspended or have specific
            issues flagged, use an expression like
            ``(state=SUSPENDED) OR (issue:*)``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)


class ListRegistrationsResponse(proto.Message):
    r"""Response for the ``ListRegistrations`` method.
    Attributes:
        registrations (Sequence[google.cloud.domains_v1beta1.types.Registration]):
            A list of ``Registration``\ s.
        next_page_token (str):
            When present, there are more results to retrieve. Set
            ``page_token`` to this value on a subsequent call to get the
            next page of results.
    """

    @property
    def raw_page(self):
        return self

    registrations = proto.RepeatedField(
        proto.MESSAGE, number=1, message="Registration",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetRegistrationRequest(proto.Message):
    r"""Request for the ``GetRegistration`` method.
    Attributes:
        name (str):
            Required. The name of the ``Registration`` to get, in the
            format ``projects/*/locations/*/registrations/*``.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateRegistrationRequest(proto.Message):
    r"""Request for the ``UpdateRegistration`` method.
    Attributes:
        registration (google.cloud.domains_v1beta1.types.Registration):
            Fields of the ``Registration`` to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The field mask describing which fields to update
            as a comma-separated list. For example, if only the labels
            are being updated, the ``update_mask`` would be
            ``"labels"``.
    """

    registration = proto.Field(proto.MESSAGE, number=1, message="Registration",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class ConfigureManagementSettingsRequest(proto.Message):
    r"""Request for the ``ConfigureManagementSettings`` method.
    Attributes:
        registration (str):
            Required. The name of the ``Registration`` whose management
            settings are being updated, in the format
            ``projects/*/locations/*/registrations/*``.
        management_settings (google.cloud.domains_v1beta1.types.ManagementSettings):
            Fields of the ``ManagementSettings`` to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The field mask describing which fields to update
            as a comma-separated list. For example, if only the transfer
            lock is being updated, the ``update_mask`` would be
            ``"transfer_lock_state"``.
    """

    registration = proto.Field(proto.STRING, number=1,)
    management_settings = proto.Field(
        proto.MESSAGE, number=2, message="ManagementSettings",
    )
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )


class ConfigureDnsSettingsRequest(proto.Message):
    r"""Request for the ``ConfigureDnsSettings`` method.
    Attributes:
        registration (str):
            Required. The name of the ``Registration`` whose DNS
            settings are being updated, in the format
            ``projects/*/locations/*/registrations/*``.
        dns_settings (google.cloud.domains_v1beta1.types.DnsSettings):
            Fields of the ``DnsSettings`` to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The field mask describing which fields to update
            as a comma-separated list. For example, if only the name
            servers are being updated for an existing Custom DNS
            configuration, the ``update_mask`` would be
            ``"custom_dns.name_servers"``.

            When changing the DNS provider from one type to another,
            pass the new provider's field name as part of the field
            mask. For example, when changing from a Google Domains DNS
            configuration to a Custom DNS configuration, the
            ``update_mask`` would be ``"custom_dns"``. //
        validate_only (bool):
            Validate the request without actually
            updating the DNS settings.
    """

    registration = proto.Field(proto.STRING, number=1,)
    dns_settings = proto.Field(proto.MESSAGE, number=2, message="DnsSettings",)
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )
    validate_only = proto.Field(proto.BOOL, number=4,)


class ConfigureContactSettingsRequest(proto.Message):
    r"""Request for the ``ConfigureContactSettings`` method.
    Attributes:
        registration (str):
            Required. The name of the ``Registration`` whose contact
            settings are being updated, in the format
            ``projects/*/locations/*/registrations/*``.
        contact_settings (google.cloud.domains_v1beta1.types.ContactSettings):
            Fields of the ``ContactSettings`` to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The field mask describing which fields to update
            as a comma-separated list. For example, if only the
            registrant contact is being updated, the ``update_mask``
            would be ``"registrant_contact"``.
        contact_notices (Sequence[google.cloud.domains_v1beta1.types.ContactNotice]):
            The list of contact notices that the caller acknowledges.
            The notices required here depend on the values specified in
            ``contact_settings``.
        validate_only (bool):
            Validate the request without actually
            updating the contact settings.
    """

    registration = proto.Field(proto.STRING, number=1,)
    contact_settings = proto.Field(proto.MESSAGE, number=2, message="ContactSettings",)
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )
    contact_notices = proto.RepeatedField(proto.ENUM, number=4, enum="ContactNotice",)
    validate_only = proto.Field(proto.BOOL, number=5,)


class ExportRegistrationRequest(proto.Message):
    r"""Request for the ``ExportRegistration`` method.
    Attributes:
        name (str):
            Required. The name of the ``Registration`` to export, in the
            format ``projects/*/locations/*/registrations/*``.
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteRegistrationRequest(proto.Message):
    r"""Request for the ``DeleteRegistration`` method.
    Attributes:
        name (str):
            Required. The name of the ``Registration`` to delete, in the
            format ``projects/*/locations/*/registrations/*``.
    """

    name = proto.Field(proto.STRING, number=1,)


class RetrieveAuthorizationCodeRequest(proto.Message):
    r"""Request for the ``RetrieveAuthorizationCode`` method.
    Attributes:
        registration (str):
            Required. The name of the ``Registration`` whose
            authorization code is being retrieved, in the format
            ``projects/*/locations/*/registrations/*``.
    """

    registration = proto.Field(proto.STRING, number=1,)


class ResetAuthorizationCodeRequest(proto.Message):
    r"""Request for the ``ResetAuthorizationCode`` method.
    Attributes:
        registration (str):
            Required. The name of the ``Registration`` whose
            authorization code is being reset, in the format
            ``projects/*/locations/*/registrations/*``.
    """

    registration = proto.Field(proto.STRING, number=1,)


class RegisterParameters(proto.Message):
    r"""Parameters required to register a new domain.
    Attributes:
        domain_name (str):
            The domain name. Unicode domain names are
            expressed in Punycode format.
        availability (google.cloud.domains_v1beta1.types.RegisterParameters.Availability):
            Indicates whether the domain is available for registration.
            This value is accurate when obtained by calling
            ``RetrieveRegisterParameters``, but is approximate when
            obtained by calling ``SearchDomains``.
        supported_privacy (Sequence[google.cloud.domains_v1beta1.types.ContactPrivacy]):
            Contact privacy options that the domain
            supports.
        domain_notices (Sequence[google.cloud.domains_v1beta1.types.DomainNotice]):
            Notices about special properties of the
            domain.
        yearly_price (google.type.money_pb2.Money):
            Price to register or renew the domain for one
            year.
    """

    class Availability(proto.Enum):
        r"""Possible availability states of a domain name."""
        AVAILABILITY_UNSPECIFIED = 0
        AVAILABLE = 1
        UNAVAILABLE = 2
        UNSUPPORTED = 3
        UNKNOWN = 4

    domain_name = proto.Field(proto.STRING, number=1,)
    availability = proto.Field(proto.ENUM, number=2, enum=Availability,)
    supported_privacy = proto.RepeatedField(
        proto.ENUM, number=3, enum="ContactPrivacy",
    )
    domain_notices = proto.RepeatedField(proto.ENUM, number=4, enum="DomainNotice",)
    yearly_price = proto.Field(proto.MESSAGE, number=5, message=money_pb2.Money,)


class AuthorizationCode(proto.Message):
    r"""Defines an authorization code.
    Attributes:
        code (str):
            The Authorization Code in ASCII. It can be
            used to transfer the domain to or from another
            registrar.
    """

    code = proto.Field(proto.STRING, number=1,)


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
        status_detail (str):
            Human-readable status of the operation, if
            any.
        api_version (str):
            API version used to start the operation.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    target = proto.Field(proto.STRING, number=3,)
    verb = proto.Field(proto.STRING, number=4,)
    status_detail = proto.Field(proto.STRING, number=5,)
    api_version = proto.Field(proto.STRING, number=6,)


__all__ = tuple(sorted(__protobuf__.manifest))
