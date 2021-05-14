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
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.security.privateca.v1beta1",
    manifest={
        "RevocationReason",
        "CertificateAuthority",
        "CertificateRevocationList",
        "Certificate",
        "ReusableConfig",
        "ReusableConfigValues",
        "ReusableConfigWrapper",
        "SubordinateConfig",
        "PublicKey",
        "CertificateConfig",
        "CertificateDescription",
        "ObjectId",
        "X509Extension",
        "KeyUsage",
        "Subject",
        "SubjectAltNames",
    },
)


class RevocationReason(proto.Enum):
    r"""A
    [RevocationReason][google.cloud.security.privateca.v1beta1.RevocationReason]
    indicates whether a
    [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
    has been revoked, and the reason for revocation. These correspond to
    standard revocation reasons from RFC 5280. Note that the enum labels
    and values in this definition are not the same ASN.1 values defined
    in RFC 5280. These values will be translated to the correct ASN.1
    values when a CRL is created.
    """
    REVOCATION_REASON_UNSPECIFIED = 0
    KEY_COMPROMISE = 1
    CERTIFICATE_AUTHORITY_COMPROMISE = 2
    AFFILIATION_CHANGED = 3
    SUPERSEDED = 4
    CESSATION_OF_OPERATION = 5
    CERTIFICATE_HOLD = 6
    PRIVILEGE_WITHDRAWN = 7
    ATTRIBUTE_AUTHORITY_COMPROMISE = 8


class CertificateAuthority(proto.Message):
    r"""A
    [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
    represents an individual Certificate Authority. A
    [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
    can be used to create
    [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

    Attributes:
        name (str):
            Output only. The resource name for this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            in the format
            ``projects/*/locations/*/certificateAuthorities/*``.
        type_ (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.Type):
            Required. Immutable. The
            [Type][google.cloud.security.privateca.v1beta1.CertificateAuthority.Type]
            of this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
        tier (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.Tier):
            Required. Immutable. The
            [Tier][google.cloud.security.privateca.v1beta1.CertificateAuthority.Tier]
            of this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
        config (google.cloud.security.privateca_v1beta1.types.CertificateConfig):
            Required. Immutable. The config used to
            create a self-signed X.509 certificate or CSR.
        lifetime (google.protobuf.duration_pb2.Duration):
            Required. The desired lifetime of the CA certificate. Used
            to create the "not_before_time" and "not_after_time" fields
            inside an X.509 certificate.
        key_spec (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.KeyVersionSpec):
            Required. Immutable. Used when issuing certificates for this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
            If this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            is a self-signed CertificateAuthority, this key is also used
            to sign the self-signed CA certificate. Otherwise, it is
            used to sign a CSR.
        certificate_policy (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.CertificateAuthorityPolicy):
            Optional. The
            [CertificateAuthorityPolicy][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy]
            to enforce when issuing
            [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
            from this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
        issuing_options (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.IssuingOptions):
            Optional. The
            [IssuingOptions][google.cloud.security.privateca.v1beta1.CertificateAuthority.IssuingOptions]
            to follow when issuing
            [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
            from this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
        subordinate_config (google.cloud.security.privateca_v1beta1.types.SubordinateConfig):
            Optional. If this is a subordinate
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority],
            this field will be set with the subordinate configuration,
            which describes its issuers. This may be updated, but this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            must continue to validate.
        state (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.State):
            Output only. The
            [State][google.cloud.security.privateca.v1beta1.CertificateAuthority.State]
            for this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
        pem_ca_certificates (Sequence[str]):
            Output only. This
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]'s
            certificate chain, including the current
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]'s
            certificate. Ordered such that the root issuer is the final
            element (consistent with RFC 5246). For a self-signed CA,
            this will only list the current
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]'s
            certificate.
        ca_certificate_descriptions (Sequence[google.cloud.security.privateca_v1beta1.types.CertificateDescription]):
            Output only. A structured description of this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]'s
            CA certificate and its issuers. Ordered as self-to-root.
        gcs_bucket (str):
            Immutable. The name of a Cloud Storage bucket where this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            will publish content, such as the CA certificate and CRLs.
            This must be a bucket name, without any prefixes (such as
            ``gs://``) or suffixes (such as ``.googleapis.com``). For
            example, to use a bucket named ``my-bucket``, you would
            simply specify ``my-bucket``. If not specified, a managed
            bucket will be created.
        access_urls (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.AccessUrls):
            Output only. URLs for accessing content
            published by this CA, such as the CA certificate
            and CRLs.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            was updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            will be deleted, if scheduled for deletion.
        labels (Sequence[google.cloud.security.privateca_v1beta1.types.CertificateAuthority.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    class Type(proto.Enum):
        r"""The type of a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority],
        indicating its issuing chain.
        """
        TYPE_UNSPECIFIED = 0
        SELF_SIGNED = 1
        SUBORDINATE = 2

    class Tier(proto.Enum):
        r"""The tier of a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority],
        indicating its supported functionality and/or billing SKU.
        """
        TIER_UNSPECIFIED = 0
        ENTERPRISE = 1
        DEVOPS = 2

    class State(proto.Enum):
        r"""The state of a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority],
        indicating if it can be used.
        """
        STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        PENDING_ACTIVATION = 3
        PENDING_DELETION = 4

    class SignHashAlgorithm(proto.Enum):
        r"""The algorithm of a Cloud KMS CryptoKeyVersion of a
        [CryptoKey][google.cloud.kms.v1.CryptoKey] with the
        [CryptoKeyPurpose][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose]
        value ``ASYMMETRIC_SIGN``. These values correspond to the
        [CryptoKeyVersionAlgorithm][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm]
        values. For RSA signing algorithms, the PSS algorithms should be
        preferred, use PKCS1 algorithms if required for compatibility. For
        further recommandations, see
        https://cloud.google.com/kms/docs/algorithms#algorithm_recommendations.
        """
        SIGN_HASH_ALGORITHM_UNSPECIFIED = 0
        RSA_PSS_2048_SHA256 = 1
        RSA_PSS_3072_SHA256 = 2
        RSA_PSS_4096_SHA256 = 3
        RSA_PKCS1_2048_SHA256 = 6
        RSA_PKCS1_3072_SHA256 = 7
        RSA_PKCS1_4096_SHA256 = 8
        EC_P256_SHA256 = 4
        EC_P384_SHA384 = 5

    class IssuingOptions(proto.Message):
        r"""Options that affect all certificates issued by a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

        Attributes:
            include_ca_cert_url (bool):
                Required. When true, includes a URL to the
                issuing CA certificate in the "authority
                information access" X.509 extension.
            include_crl_access_url (bool):
                Required. When true, includes a URL to the CRL corresponding
                to certificates issued from a
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
                CRLs will expire 7 days from their creation. However, we
                will rebuild daily. CRLs are also rebuilt shortly after a
                certificate is revoked.
        """

        include_ca_cert_url = proto.Field(proto.BOOL, number=1,)
        include_crl_access_url = proto.Field(proto.BOOL, number=2,)

    class CertificateAuthorityPolicy(proto.Message):
        r"""The issuing policy for a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
        [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
        will not be successfully issued from this
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        if they violate the policy.

        Attributes:
            allowed_config_list (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.CertificateAuthorityPolicy.AllowedConfigList):
                Optional. All
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                issued by the
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                must match at least one listed
                [ReusableConfigWrapper][google.cloud.security.privateca.v1beta1.ReusableConfigWrapper]
                in the list.
            overwrite_config_values (google.cloud.security.privateca_v1beta1.types.ReusableConfigWrapper):
                Optional. All
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                issued by the
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                will use the provided configuration values, overwriting any
                requested configuration values.
            allowed_locations_and_organizations (Sequence[google.cloud.security.privateca_v1beta1.types.Subject]):
                Optional. If any
                [Subject][google.cloud.security.privateca.v1beta1.Subject]
                is specified here, then all
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                issued by the
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                must match at least one listed
                [Subject][google.cloud.security.privateca.v1beta1.Subject].
                If a
                [Subject][google.cloud.security.privateca.v1beta1.Subject]
                has an empty field, any value will be allowed for that
                field.
            allowed_common_names (Sequence[str]):
                Optional. If any value is specified here, then all
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                issued by the
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                must match at least one listed value. If no value is
                specified, all values will be allowed for this fied. Glob
                patterns are also supported.
            allowed_sans (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.CertificateAuthorityPolicy.AllowedSubjectAltNames):
                Optional. If a
                [AllowedSubjectAltNames][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy.AllowedSubjectAltNames]
                is specified here, then all
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                issued by the
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                must match
                [AllowedSubjectAltNames][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy.AllowedSubjectAltNames].
                If no value or an empty value is specified, any value will
                be allowed for the
                [SubjectAltNames][google.cloud.security.privateca.v1beta1.SubjectAltNames]
                field.
            maximum_lifetime (google.protobuf.duration_pb2.Duration):
                Optional. The maximum lifetime allowed by the
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
                Note that if the any part if the issuing chain expires
                before a
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]'s
                requested maximum_lifetime, the effective lifetime will be
                explicitly truncated.
            allowed_issuance_modes (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.CertificateAuthorityPolicy.IssuanceModes):
                Optional. If specified, then only methods allowed in the
                [IssuanceModes][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy.IssuanceModes]
                may be used to issue
                [Certificates][google.cloud.security.privateca.v1beta1.Certificate].
        """

        class AllowedConfigList(proto.Message):
            r"""
            Attributes:
                allowed_config_values (Sequence[google.cloud.security.privateca_v1beta1.types.ReusableConfigWrapper]):
                    Required. All
                    [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                    issued by the
                    [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
                    must match at least one listed
                    [ReusableConfigWrapper][google.cloud.security.privateca.v1beta1.ReusableConfigWrapper].
                    If a
                    [ReusableConfigWrapper][google.cloud.security.privateca.v1beta1.ReusableConfigWrapper]
                    has an empty field, any value will be allowed for that
                    field.
            """

            allowed_config_values = proto.RepeatedField(
                proto.MESSAGE, number=1, message="ReusableConfigWrapper",
            )

        class AllowedSubjectAltNames(proto.Message):
            r"""[AllowedSubjectAltNames][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy.AllowedSubjectAltNames]
            specifies the allowed values for
            [SubjectAltNames][google.cloud.security.privateca.v1beta1.SubjectAltNames]
            by the
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            when issuing
            [Certificates][google.cloud.security.privateca.v1beta1.Certificate].

            Attributes:
                allowed_dns_names (Sequence[str]):
                    Optional. Contains valid, fully-qualified host names. Glob
                    patterns are also supported. To allow an explicit wildcard
                    certificate, escape with backlash (i.e. "*"). E.g. for
                    globbed entries: '*bar.com' will allow foo.bar.com, but not
                    *.bar.com, unless the
                    [allow_globbing_dns_wildcards][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy.AllowedSubjectAltNames.allow_globbing_dns_wildcards]
                    field is set. E.g. for wildcard entries: '*.bar.com' will
                    allow '*.bar.com', but not 'foo.bar.com'.
                allowed_uris (Sequence[str]):
                    Optional. Contains valid RFC 3986 URIs. Glob patterns are
                    also supported. To match across path seperators (i.e. '/')
                    use the double star glob pattern (i.e. '**').
                allowed_email_addresses (Sequence[str]):
                    Optional. Contains valid RFC 2822 E-mail
                    addresses. Glob patterns are also supported.
                allowed_ips (Sequence[str]):
                    Optional. Contains valid 32-bit IPv4
                    addresses and subnet ranges or RFC 4291 IPv6
                    addresses and subnet ranges. Subnet ranges are
                    specified using the '/' notation (e.g.
                    10.0.0.0/8, 2001:700:300:1800::/64). Glob
                    patterns are supported only for ip address
                    entries (i.e. not for subnet ranges).
                allow_globbing_dns_wildcards (bool):
                    Optional. Specifies if glob patterns used for
                    [allowed_dns_names][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy.AllowedSubjectAltNames.allowed_dns_names]
                    allows wildcard certificates.
                allow_custom_sans (bool):
                    Optional. Specifies if to allow custom
                    X509Extension values.
            """

            allowed_dns_names = proto.RepeatedField(proto.STRING, number=1,)
            allowed_uris = proto.RepeatedField(proto.STRING, number=2,)
            allowed_email_addresses = proto.RepeatedField(proto.STRING, number=3,)
            allowed_ips = proto.RepeatedField(proto.STRING, number=4,)
            allow_globbing_dns_wildcards = proto.Field(proto.BOOL, number=5,)
            allow_custom_sans = proto.Field(proto.BOOL, number=6,)

        class IssuanceModes(proto.Message):
            r"""[IssuanceModes][google.cloud.security.privateca.v1beta1.CertificateAuthority.CertificateAuthorityPolicy.IssuanceModes]
            specifies the allowed ways in which
            [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
            may be requested from this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

            Attributes:
                allow_csr_based_issuance (bool):
                    Required. When true, allows callers to create
                    [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                    by specifying a CSR.
                allow_config_based_issuance (bool):
                    Required. When true, allows callers to create
                    [Certificates][google.cloud.security.privateca.v1beta1.Certificate]
                    by specifying a
                    [CertificateConfig][google.cloud.security.privateca.v1beta1.CertificateConfig].
            """

            allow_csr_based_issuance = proto.Field(proto.BOOL, number=1,)
            allow_config_based_issuance = proto.Field(proto.BOOL, number=2,)

        allowed_config_list = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="config_policy",
            message="CertificateAuthority.CertificateAuthorityPolicy.AllowedConfigList",
        )
        overwrite_config_values = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="config_policy",
            message="ReusableConfigWrapper",
        )
        allowed_locations_and_organizations = proto.RepeatedField(
            proto.MESSAGE, number=3, message="Subject",
        )
        allowed_common_names = proto.RepeatedField(proto.STRING, number=4,)
        allowed_sans = proto.Field(
            proto.MESSAGE,
            number=5,
            message="CertificateAuthority.CertificateAuthorityPolicy.AllowedSubjectAltNames",
        )
        maximum_lifetime = proto.Field(
            proto.MESSAGE, number=6, message=duration_pb2.Duration,
        )
        allowed_issuance_modes = proto.Field(
            proto.MESSAGE,
            number=8,
            message="CertificateAuthority.CertificateAuthorityPolicy.IssuanceModes",
        )

    class AccessUrls(proto.Message):
        r"""URLs where a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        will publish content.

        Attributes:
            ca_certificate_access_url (str):
                The URL where this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]'s
                CA certificate is published. This will only be set for CAs
                that have been activated.
            crl_access_url (str):
                The URL where this
                [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]'s
                CRLs are published. This will only be set for CAs that have
                been activated.
        """

        ca_certificate_access_url = proto.Field(proto.STRING, number=1,)
        crl_access_url = proto.Field(proto.STRING, number=2,)

    class KeyVersionSpec(proto.Message):
        r"""A Cloud KMS key configuration that a
        [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
        will use.

        Attributes:
            cloud_kms_key_version (str):
                Required. The resource name for an existing Cloud KMS
                CryptoKeyVersion in the format
                ``projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*``.
                This option enables full flexibility in the key's
                capabilities and properties.
            algorithm (google.cloud.security.privateca_v1beta1.types.CertificateAuthority.SignHashAlgorithm):
                Required. The algorithm to use for creating a managed Cloud
                KMS key for a for a simplified experience. All managed keys
                will be have their
                [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel] as
                ``HSM``.
        """

        cloud_kms_key_version = proto.Field(proto.STRING, number=1, oneof="KeyVersion",)
        algorithm = proto.Field(
            proto.ENUM,
            number=2,
            oneof="KeyVersion",
            enum="CertificateAuthority.SignHashAlgorithm",
        )

    name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum=Type,)
    tier = proto.Field(proto.ENUM, number=3, enum=Tier,)
    config = proto.Field(proto.MESSAGE, number=4, message="CertificateConfig",)
    lifetime = proto.Field(proto.MESSAGE, number=5, message=duration_pb2.Duration,)
    key_spec = proto.Field(proto.MESSAGE, number=6, message=KeyVersionSpec,)
    certificate_policy = proto.Field(
        proto.MESSAGE, number=7, message=CertificateAuthorityPolicy,
    )
    issuing_options = proto.Field(proto.MESSAGE, number=8, message=IssuingOptions,)
    subordinate_config = proto.Field(
        proto.MESSAGE, number=19, message="SubordinateConfig",
    )
    state = proto.Field(proto.ENUM, number=10, enum=State,)
    pem_ca_certificates = proto.RepeatedField(proto.STRING, number=9,)
    ca_certificate_descriptions = proto.RepeatedField(
        proto.MESSAGE, number=12, message="CertificateDescription",
    )
    gcs_bucket = proto.Field(proto.STRING, number=13,)
    access_urls = proto.Field(proto.MESSAGE, number=14, message=AccessUrls,)
    create_time = proto.Field(
        proto.MESSAGE, number=15, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=16, message=timestamp_pb2.Timestamp,
    )
    delete_time = proto.Field(
        proto.MESSAGE, number=17, message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=18,)


class CertificateRevocationList(proto.Message):
    r"""A
    [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
    corresponds to a signed X.509 certificate Revocation List (CRL). A
    CRL contains the serial numbers of certificates that should no
    longer be trusted.

    Attributes:
        name (str):
            Output only. The resource path for this
            [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
            in the format
            ``projects/*/locations/*/certificateAuthorities/*/ certificateRevocationLists/*``.
        sequence_number (int):
            Output only. The CRL sequence number that appears in
            pem_crl.
        revoked_certificates (Sequence[google.cloud.security.privateca_v1beta1.types.CertificateRevocationList.RevokedCertificate]):
            Output only. The revoked serial numbers that appear in
            pem_crl.
        pem_crl (str):
            Output only. The PEM-encoded X.509 CRL.
        access_url (str):
            Output only. The location where 'pem_crl' can be accessed.
        state (google.cloud.security.privateca_v1beta1.types.CertificateRevocationList.State):
            Output only. The
            [State][google.cloud.security.privateca.v1beta1.CertificateRevocationList.State]
            for this
            [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList].
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList]
            was updated.
        labels (Sequence[google.cloud.security.privateca_v1beta1.types.CertificateRevocationList.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    class State(proto.Enum):
        r"""The state of a
        [CertificateRevocationList][google.cloud.security.privateca.v1beta1.CertificateRevocationList],
        indicating if it is current.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        SUPERSEDED = 2

    class RevokedCertificate(proto.Message):
        r"""Describes a revoked
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Attributes:
            certificate (str):
                The resource path for the
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                in the format
                ``projects/*/locations/*/certificateAuthorities/*/certificates/*``.
            hex_serial_number (str):
                The serial number of the
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate].
            revocation_reason (google.cloud.security.privateca_v1beta1.types.RevocationReason):
                The reason the
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                was revoked.
        """

        certificate = proto.Field(proto.STRING, number=1,)
        hex_serial_number = proto.Field(proto.STRING, number=2,)
        revocation_reason = proto.Field(proto.ENUM, number=3, enum="RevocationReason",)

    name = proto.Field(proto.STRING, number=1,)
    sequence_number = proto.Field(proto.INT64, number=2,)
    revoked_certificates = proto.RepeatedField(
        proto.MESSAGE, number=3, message=RevokedCertificate,
    )
    pem_crl = proto.Field(proto.STRING, number=4,)
    access_url = proto.Field(proto.STRING, number=5,)
    state = proto.Field(proto.ENUM, number=6, enum=State,)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=9,)


class Certificate(proto.Message):
    r"""A [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
    corresponds to a signed X.509 certificate issued by a
    [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].

    Attributes:
        name (str):
            Output only. The resource path for this
            [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
            in the format
            ``projects/*/locations/*/certificateAuthorities/*/certificates/*``.
        pem_csr (str):
            Immutable. A pem-encoded X.509 certificate
            signing request (CSR).
        config (google.cloud.security.privateca_v1beta1.types.CertificateConfig):
            Immutable. A description of the certificate
            and key that does not require X.509 or ASN.1.
        lifetime (google.protobuf.duration_pb2.Duration):
            Required. Immutable. The desired lifetime of a certificate.
            Used to create the "not_before_time" and "not_after_time"
            fields inside an X.509 certificate. Note that the lifetime
            may be truncated if it would extend past the life of any
            certificate authority in the issuing chain.
        revocation_details (google.cloud.security.privateca_v1beta1.types.Certificate.RevocationDetails):
            Output only. Details regarding the revocation of this
            [Certificate][google.cloud.security.privateca.v1beta1.Certificate].
            This
            [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
            is considered revoked if and only if this field is present.
        pem_certificate (str):
            Output only. The pem-encoded, signed X.509
            certificate.
        certificate_description (google.cloud.security.privateca_v1beta1.types.CertificateDescription):
            Output only. A structured description of the
            issued X.509 certificate.
        pem_certificate_chain (Sequence[str]):
            Output only. The chain that may be used to
            verify the X.509 certificate. Expected to be in
            issuer-to-root order according to RFC 5246.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
            was updated.
        labels (Sequence[google.cloud.security.privateca_v1beta1.types.Certificate.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    class RevocationDetails(proto.Message):
        r"""Describes fields that are relavent to the revocation of a
        [Certificate][google.cloud.security.privateca.v1beta1.Certificate].

        Attributes:
            revocation_state (google.cloud.security.privateca_v1beta1.types.RevocationReason):
                Indicates why a
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                was revoked.
            revocation_time (google.protobuf.timestamp_pb2.Timestamp):
                The time at which this
                [Certificate][google.cloud.security.privateca.v1beta1.Certificate]
                was revoked.
        """

        revocation_state = proto.Field(proto.ENUM, number=1, enum="RevocationReason",)
        revocation_time = proto.Field(
            proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,
        )

    name = proto.Field(proto.STRING, number=1,)
    pem_csr = proto.Field(proto.STRING, number=2, oneof="certificate_config",)
    config = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="certificate_config",
        message="CertificateConfig",
    )
    lifetime = proto.Field(proto.MESSAGE, number=4, message=duration_pb2.Duration,)
    revocation_details = proto.Field(
        proto.MESSAGE, number=5, message=RevocationDetails,
    )
    pem_certificate = proto.Field(proto.STRING, number=6,)
    certificate_description = proto.Field(
        proto.MESSAGE, number=7, message="CertificateDescription",
    )
    pem_certificate_chain = proto.RepeatedField(proto.STRING, number=8,)
    create_time = proto.Field(proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=11,)


class ReusableConfig(proto.Message):
    r"""A
    [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
    refers to a managed
    [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues].
    Those, in turn, are used to describe certain fields of an X.509
    certificate, such as the key usage fields, fields specific to CA
    certificates, certificate policy extensions and custom extensions.

    Attributes:
        name (str):
            Output only. The resource path for this
            [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
            in the format ``projects/*/locations/*/reusableConfigs/*``.
        values (google.cloud.security.privateca_v1beta1.types.ReusableConfigValues):
            Required. The config values.
        description (str):
            Optional. A human-readable description of
            scenarios these ReusableConfigValues may be
            compatible with.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
            was updated.
        labels (Sequence[google.cloud.security.privateca_v1beta1.types.ReusableConfig.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    name = proto.Field(proto.STRING, number=1,)
    values = proto.Field(proto.MESSAGE, number=2, message="ReusableConfigValues",)
    description = proto.Field(proto.STRING, number=3,)
    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=6,)


class ReusableConfigValues(proto.Message):
    r"""A
    [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues]
    is used to describe certain fields of an X.509 certificate, such as
    the key usage fields, fields specific to CA certificates,
    certificate policy extensions and custom extensions.

    Attributes:
        key_usage (google.cloud.security.privateca_v1beta1.types.KeyUsage):
            Optional. Indicates the intended use for keys
            that correspond to a certificate.
        ca_options (google.cloud.security.privateca_v1beta1.types.ReusableConfigValues.CaOptions):
            Optional. Describes options in this
            [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues]
            that are relevant in a CA certificate.
        policy_ids (Sequence[google.cloud.security.privateca_v1beta1.types.ObjectId]):
            Optional. Describes the X.509 certificate
            policy object identifiers, per
            https://tools.ietf.org/html/rfc5280#section-4.2.1.4.
        aia_ocsp_servers (Sequence[str]):
            Optional. Describes Online Certificate Status
            Protocol (OCSP) endpoint addresses that appear
            in the "Authority Information Access" extension
            in the certificate.
        additional_extensions (Sequence[google.cloud.security.privateca_v1beta1.types.X509Extension]):
            Optional. Describes custom X.509 extensions.
    """

    class CaOptions(proto.Message):
        r"""Describes values that are relevant in a CA certificate.
        Attributes:
            is_ca (google.protobuf.wrappers_pb2.BoolValue):
                Optional. Refers to the "CA" X.509 extension,
                which is a boolean value. When this value is
                missing, the extension will be omitted from the
                CA certificate.
            max_issuer_path_length (google.protobuf.wrappers_pb2.Int32Value):
                Optional. Refers to the path length
                restriction X.509 extension. For a CA
                certificate, this value describes the depth of
                subordinate CA certificates that are allowed.
                If this value is less than 0, the request will
                fail. If this value is missing, the max path
                length will be omitted from the CA certificate.
        """

        is_ca = proto.Field(proto.MESSAGE, number=1, message=wrappers_pb2.BoolValue,)
        max_issuer_path_length = proto.Field(
            proto.MESSAGE, number=2, message=wrappers_pb2.Int32Value,
        )

    key_usage = proto.Field(proto.MESSAGE, number=1, message="KeyUsage",)
    ca_options = proto.Field(proto.MESSAGE, number=2, message=CaOptions,)
    policy_ids = proto.RepeatedField(proto.MESSAGE, number=3, message="ObjectId",)
    aia_ocsp_servers = proto.RepeatedField(proto.STRING, number=4,)
    additional_extensions = proto.RepeatedField(
        proto.MESSAGE, number=5, message="X509Extension",
    )


class ReusableConfigWrapper(proto.Message):
    r"""A
    [ReusableConfigWrapper][google.cloud.security.privateca.v1beta1.ReusableConfigWrapper]
    describes values that may assist in creating an X.509 certificate,
    or a reference to a pre-defined set of values.

    Attributes:
        reusable_config (str):
            Required. A resource path to a
            [ReusableConfig][google.cloud.security.privateca.v1beta1.ReusableConfig]
            in the format ``projects/*/locations/*/reusableConfigs/*``.
        reusable_config_values (google.cloud.security.privateca_v1beta1.types.ReusableConfigValues):
            Required. A user-specified inline
            [ReusableConfigValues][google.cloud.security.privateca.v1beta1.ReusableConfigValues].
    """

    reusable_config = proto.Field(proto.STRING, number=1, oneof="config_values",)
    reusable_config_values = proto.Field(
        proto.MESSAGE, number=2, oneof="config_values", message="ReusableConfigValues",
    )


class SubordinateConfig(proto.Message):
    r"""Describes a subordinate CA's issuers. This is either a resource path
    to a known issuing
    [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority],
    or a PEM issuer certificate chain.

    Attributes:
        certificate_authority (str):
            Required. This can refer to a
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            in the same project that was used to create a subordinate
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority].
            This field is used for information and usability purposes
            only. The resource name is in the format
            ``projects/*/locations/*/certificateAuthorities/*``.
        pem_issuer_chain (google.cloud.security.privateca_v1beta1.types.SubordinateConfig.SubordinateConfigChain):
            Required. Contains the PEM certificate chain for the issuers
            of this
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority],
            but not pem certificate for this CA itself.
    """

    class SubordinateConfigChain(proto.Message):
        r"""This message describes a subordinate CA's issuer certificate
        chain. This wrapper exists for compatibility reasons.

        Attributes:
            pem_certificates (Sequence[str]):
                Required. Expected to be in leaf-to-root
                order according to RFC 5246.
        """

        pem_certificates = proto.RepeatedField(proto.STRING, number=1,)

    certificate_authority = proto.Field(
        proto.STRING, number=1, oneof="subordinate_config",
    )
    pem_issuer_chain = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="subordinate_config",
        message=SubordinateConfigChain,
    )


class PublicKey(proto.Message):
    r"""A [PublicKey][google.cloud.security.privateca.v1beta1.PublicKey]
    describes a public key.

    Attributes:
        type_ (google.cloud.security.privateca_v1beta1.types.PublicKey.KeyType):
            Required. The type of public key.
        key (bytes):
            Required. A public key. Padding and encoding
            varies by 'KeyType' and is described along with
            the KeyType values.
    """

    class KeyType(proto.Enum):
        r"""Types of public keys that are supported. At a minimum, we support
        RSA and ECDSA, for the key sizes or curves listed:
        https://cloud.google.com/kms/docs/algorithms#asymmetric_signing_algorithms
        """
        KEY_TYPE_UNSPECIFIED = 0
        PEM_RSA_KEY = 1
        PEM_EC_KEY = 2

    type_ = proto.Field(proto.ENUM, number=1, enum=KeyType,)
    key = proto.Field(proto.BYTES, number=2,)


class CertificateConfig(proto.Message):
    r"""A
    [CertificateConfig][google.cloud.security.privateca.v1beta1.CertificateConfig]
    describes an X.509 certificate or CSR that is to be created, as an
    alternative to using ASN.1.

    Attributes:
        subject_config (google.cloud.security.privateca_v1beta1.types.CertificateConfig.SubjectConfig):
            Required. Specifies some of the values in a
            certificate that are related to the subject.
        reusable_config (google.cloud.security.privateca_v1beta1.types.ReusableConfigWrapper):
            Required. Describes how some of the technical
            fields in a certificate should be populated.
        public_key (google.cloud.security.privateca_v1beta1.types.PublicKey):
            Optional. The public key that corresponds to this config.
            This is, for example, used when issuing
            [Certificates][google.cloud.security.privateca.v1beta1.Certificate],
            but not when creating a self-signed
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            or
            [CertificateAuthority][google.cloud.security.privateca.v1beta1.CertificateAuthority]
            CSR.
    """

    class SubjectConfig(proto.Message):
        r"""These values are used to create the distinguished name and
        subject alternative name fields in an X.509 certificate.

        Attributes:
            subject (google.cloud.security.privateca_v1beta1.types.Subject):
                Required. Contains distinguished name fields
                such as the location and organization.
            common_name (str):
                Optional. The "common name" of the
                distinguished name.
            subject_alt_name (google.cloud.security.privateca_v1beta1.types.SubjectAltNames):
                Optional. The subject alternative name
                fields.
        """

        subject = proto.Field(proto.MESSAGE, number=1, message="Subject",)
        common_name = proto.Field(proto.STRING, number=2,)
        subject_alt_name = proto.Field(
            proto.MESSAGE, number=3, message="SubjectAltNames",
        )

    subject_config = proto.Field(proto.MESSAGE, number=1, message=SubjectConfig,)
    reusable_config = proto.Field(
        proto.MESSAGE, number=2, message="ReusableConfigWrapper",
    )
    public_key = proto.Field(proto.MESSAGE, number=3, message="PublicKey",)


class CertificateDescription(proto.Message):
    r"""A
    [CertificateDescription][google.cloud.security.privateca.v1beta1.CertificateDescription]
    describes an X.509 certificate or CSR that has been issued, as an
    alternative to using ASN.1 / X.509.

    Attributes:
        subject_description (google.cloud.security.privateca_v1beta1.types.CertificateDescription.SubjectDescription):
            Describes some of the values in a certificate
            that are related to the subject and lifetime.
        config_values (google.cloud.security.privateca_v1beta1.types.ReusableConfigValues):
            Describes some of the technical fields in a
            certificate.
        public_key (google.cloud.security.privateca_v1beta1.types.PublicKey):
            The public key that corresponds to an issued
            certificate.
        subject_key_id (google.cloud.security.privateca_v1beta1.types.CertificateDescription.KeyId):
            Provides a means of identifiying certificates
            that contain a particular public key, per
            https://tools.ietf.org/html/rfc5280#section-4.2.1.2.
        authority_key_id (google.cloud.security.privateca_v1beta1.types.CertificateDescription.KeyId):
            Identifies the subject_key_id of the parent certificate, per
            https://tools.ietf.org/html/rfc5280#section-4.2.1.1
        crl_distribution_points (Sequence[str]):
            Describes a list of locations to obtain CRL
            information, i.e. the DistributionPoint.fullName
            described by
            https://tools.ietf.org/html/rfc5280#section-4.2.1.13
        aia_issuing_certificate_urls (Sequence[str]):
            Describes lists of issuer CA certificate URLs
            that appear in the "Authority Information
            Access" extension in the certificate.
        cert_fingerprint (google.cloud.security.privateca_v1beta1.types.CertificateDescription.CertificateFingerprint):
            The hash of the x.509 certificate.
    """

    class SubjectDescription(proto.Message):
        r"""These values describe fields in an issued X.509 certificate
        such as the distinguished name, subject alternative names,
        serial number, and lifetime.

        Attributes:
            subject (google.cloud.security.privateca_v1beta1.types.Subject):
                Contains distinguished name fields such as
                the location and organization.
            common_name (str):
                The "common name" of the distinguished name.
            subject_alt_name (google.cloud.security.privateca_v1beta1.types.SubjectAltNames):
                The subject alternative name fields.
            hex_serial_number (str):
                The serial number encoded in lowercase
                hexadecimal.
            lifetime (google.protobuf.duration_pb2.Duration):
                For convenience, the actual lifetime of an issued
                certificate. Corresponds to 'not_after_time' -
                'not_before_time'.
            not_before_time (google.protobuf.timestamp_pb2.Timestamp):
                The time at which the certificate becomes
                valid.
            not_after_time (google.protobuf.timestamp_pb2.Timestamp):
                The time at which the certificate expires.
        """

        subject = proto.Field(proto.MESSAGE, number=1, message="Subject",)
        common_name = proto.Field(proto.STRING, number=2,)
        subject_alt_name = proto.Field(
            proto.MESSAGE, number=3, message="SubjectAltNames",
        )
        hex_serial_number = proto.Field(proto.STRING, number=4,)
        lifetime = proto.Field(proto.MESSAGE, number=5, message=duration_pb2.Duration,)
        not_before_time = proto.Field(
            proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
        )
        not_after_time = proto.Field(
            proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
        )

    class KeyId(proto.Message):
        r"""A KeyId identifies a specific public key, usually by hashing
        the public key.

        Attributes:
            key_id (str):
                Optional. The value of this KeyId encoded in
                lowercase hexadecimal. This is most likely the
                160 bit SHA-1 hash of the public key.
        """

        key_id = proto.Field(proto.STRING, number=1,)

    class CertificateFingerprint(proto.Message):
        r"""A group of fingerprints for the x509 certificate.
        Attributes:
            sha256_hash (str):
                The SHA 256 hash, encoded in hexadecimal, of
                the DER x509 certificate.
        """

        sha256_hash = proto.Field(proto.STRING, number=1,)

    subject_description = proto.Field(
        proto.MESSAGE, number=1, message=SubjectDescription,
    )
    config_values = proto.Field(
        proto.MESSAGE, number=2, message="ReusableConfigValues",
    )
    public_key = proto.Field(proto.MESSAGE, number=3, message="PublicKey",)
    subject_key_id = proto.Field(proto.MESSAGE, number=4, message=KeyId,)
    authority_key_id = proto.Field(proto.MESSAGE, number=5, message=KeyId,)
    crl_distribution_points = proto.RepeatedField(proto.STRING, number=6,)
    aia_issuing_certificate_urls = proto.RepeatedField(proto.STRING, number=7,)
    cert_fingerprint = proto.Field(
        proto.MESSAGE, number=8, message=CertificateFingerprint,
    )


class ObjectId(proto.Message):
    r"""An [ObjectId][google.cloud.security.privateca.v1beta1.ObjectId]
    specifies an object identifier (OID). These provide context and
    describe types in ASN.1 messages.

    Attributes:
        object_id_path (Sequence[int]):
            Required. The parts of an OID path. The most
            significant parts of the path come first.
    """

    object_id_path = proto.RepeatedField(proto.INT32, number=1,)


class X509Extension(proto.Message):
    r"""An
    [X509Extension][google.cloud.security.privateca.v1beta1.X509Extension]
    specifies an X.509 extension, which may be used in different parts
    of X.509 objects like certificates, CSRs, and CRLs.

    Attributes:
        object_id (google.cloud.security.privateca_v1beta1.types.ObjectId):
            Required. The OID for this X.509 extension.
        critical (bool):
            Required. Indicates whether or not this
            extension is critical (i.e., if the client does
            not know how to handle this extension, the
            client should consider this to be an error).
        value (bytes):
            Required. The value of this X.509 extension.
    """

    object_id = proto.Field(proto.MESSAGE, number=1, message="ObjectId",)
    critical = proto.Field(proto.BOOL, number=2,)
    value = proto.Field(proto.BYTES, number=3,)


class KeyUsage(proto.Message):
    r"""A [KeyUsage][google.cloud.security.privateca.v1beta1.KeyUsage]
    describes key usage values that may appear in an X.509 certificate.

    Attributes:
        base_key_usage (google.cloud.security.privateca_v1beta1.types.KeyUsage.KeyUsageOptions):
            Describes high-level ways in which a key may
            be used.
        extended_key_usage (google.cloud.security.privateca_v1beta1.types.KeyUsage.ExtendedKeyUsageOptions):
            Detailed scenarios in which a key may be
            used.
        unknown_extended_key_usages (Sequence[google.cloud.security.privateca_v1beta1.types.ObjectId]):
            Used to describe extended key usages that are not listed in
            the
            [KeyUsage.ExtendedKeyUsageOptions][google.cloud.security.privateca.v1beta1.KeyUsage.ExtendedKeyUsageOptions]
            message.
    """

    class KeyUsageOptions(proto.Message):
        r"""[KeyUsage.KeyUsageOptions][google.cloud.security.privateca.v1beta1.KeyUsage.KeyUsageOptions]
        corresponds to the key usage values described in
        https://tools.ietf.org/html/rfc5280#section-4.2.1.3.

        Attributes:
            digital_signature (bool):
                The key may be used for digital signatures.
            content_commitment (bool):
                The key may be used for cryptographic
                commitments. Note that this may also be referred
                to as "non-repudiation".
            key_encipherment (bool):
                The key may be used to encipher other keys.
            data_encipherment (bool):
                The key may be used to encipher data.
            key_agreement (bool):
                The key may be used in a key agreement
                protocol.
            cert_sign (bool):
                The key may be used to sign certificates.
            crl_sign (bool):
                The key may be used sign certificate
                revocation lists.
            encipher_only (bool):
                The key may be used to encipher only.
            decipher_only (bool):
                The key may be used to decipher only.
        """

        digital_signature = proto.Field(proto.BOOL, number=1,)
        content_commitment = proto.Field(proto.BOOL, number=2,)
        key_encipherment = proto.Field(proto.BOOL, number=3,)
        data_encipherment = proto.Field(proto.BOOL, number=4,)
        key_agreement = proto.Field(proto.BOOL, number=5,)
        cert_sign = proto.Field(proto.BOOL, number=6,)
        crl_sign = proto.Field(proto.BOOL, number=7,)
        encipher_only = proto.Field(proto.BOOL, number=8,)
        decipher_only = proto.Field(proto.BOOL, number=9,)

    class ExtendedKeyUsageOptions(proto.Message):
        r"""[KeyUsage.ExtendedKeyUsageOptions][google.cloud.security.privateca.v1beta1.KeyUsage.ExtendedKeyUsageOptions]
        has fields that correspond to certain common OIDs that could be
        specified as an extended key usage value.

        Attributes:
            server_auth (bool):
                Corresponds to OID 1.3.6.1.5.5.7.3.1.
                Officially described as "TLS WWW server
                authentication", though regularly used for non-
                WWW TLS.
            client_auth (bool):
                Corresponds to OID 1.3.6.1.5.5.7.3.2.
                Officially described as "TLS WWW client
                authentication", though regularly used for non-
                WWW TLS.
            code_signing (bool):
                Corresponds to OID 1.3.6.1.5.5.7.3.3.
                Officially described as "Signing of downloadable
                executable code client authentication".
            email_protection (bool):
                Corresponds to OID 1.3.6.1.5.5.7.3.4.
                Officially described as "Email protection".
            time_stamping (bool):
                Corresponds to OID 1.3.6.1.5.5.7.3.8.
                Officially described as "Binding the hash of an
                object to a time".
            ocsp_signing (bool):
                Corresponds to OID 1.3.6.1.5.5.7.3.9.
                Officially described as "Signing OCSP
                responses".
        """

        server_auth = proto.Field(proto.BOOL, number=1,)
        client_auth = proto.Field(proto.BOOL, number=2,)
        code_signing = proto.Field(proto.BOOL, number=3,)
        email_protection = proto.Field(proto.BOOL, number=4,)
        time_stamping = proto.Field(proto.BOOL, number=5,)
        ocsp_signing = proto.Field(proto.BOOL, number=6,)

    base_key_usage = proto.Field(proto.MESSAGE, number=1, message=KeyUsageOptions,)
    extended_key_usage = proto.Field(
        proto.MESSAGE, number=2, message=ExtendedKeyUsageOptions,
    )
    unknown_extended_key_usages = proto.RepeatedField(
        proto.MESSAGE, number=3, message="ObjectId",
    )


class Subject(proto.Message):
    r"""[Subject][google.cloud.security.privateca.v1beta1.Subject] describes
    parts of a distinguished name that, in turn, describes the subject
    of the certificate.

    Attributes:
        country_code (str):
            The country code of the subject.
        organization (str):
            The organization of the subject.
        organizational_unit (str):
            The organizational_unit of the subject.
        locality (str):
            The locality or city of the subject.
        province (str):
            The province, territory, or regional state of
            the subject.
        street_address (str):
            The street address of the subject.
        postal_code (str):
            The postal code of the subject.
    """

    country_code = proto.Field(proto.STRING, number=1,)
    organization = proto.Field(proto.STRING, number=2,)
    organizational_unit = proto.Field(proto.STRING, number=3,)
    locality = proto.Field(proto.STRING, number=4,)
    province = proto.Field(proto.STRING, number=5,)
    street_address = proto.Field(proto.STRING, number=6,)
    postal_code = proto.Field(proto.STRING, number=7,)


class SubjectAltNames(proto.Message):
    r"""[SubjectAltNames][google.cloud.security.privateca.v1beta1.SubjectAltNames]
    corresponds to a more modern way of listing what the asserted
    identity is in a certificate (i.e., compared to the "common name" in
    the distinguished name).

    Attributes:
        dns_names (Sequence[str]):
            Contains only valid, fully-qualified host
            names.
        uris (Sequence[str]):
            Contains only valid RFC 3986 URIs.
        email_addresses (Sequence[str]):
            Contains only valid RFC 2822 E-mail
            addresses.
        ip_addresses (Sequence[str]):
            Contains only valid 32-bit IPv4 addresses or
            RFC 4291 IPv6 addresses.
        custom_sans (Sequence[google.cloud.security.privateca_v1beta1.types.X509Extension]):
            Contains additional subject alternative name
            values.
    """

    dns_names = proto.RepeatedField(proto.STRING, number=1,)
    uris = proto.RepeatedField(proto.STRING, number=2,)
    email_addresses = proto.RepeatedField(proto.STRING, number=3,)
    ip_addresses = proto.RepeatedField(proto.STRING, number=4,)
    custom_sans = proto.RepeatedField(proto.MESSAGE, number=5, message="X509Extension",)


__all__ = tuple(sorted(__protobuf__.manifest))
