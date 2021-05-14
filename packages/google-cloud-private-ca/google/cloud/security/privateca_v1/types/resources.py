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
from google.type import expr_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.security.privateca.v1",
    manifest={
        "RevocationReason",
        "SubjectRequestMode",
        "CertificateAuthority",
        "CaPool",
        "CertificateRevocationList",
        "Certificate",
        "CertificateTemplate",
        "X509Parameters",
        "SubordinateConfig",
        "PublicKey",
        "CertificateConfig",
        "CertificateDescription",
        "ObjectId",
        "X509Extension",
        "KeyUsage",
        "Subject",
        "SubjectAltNames",
        "CertificateIdentityConstraints",
        "CertificateExtensionConstraints",
    },
)


class RevocationReason(proto.Enum):
    r"""A
    [RevocationReason][google.cloud.security.privateca.v1.RevocationReason]
    indicates whether a
    [Certificate][google.cloud.security.privateca.v1.Certificate] has
    been revoked, and the reason for revocation. These correspond to
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


class SubjectRequestMode(proto.Enum):
    r"""Describes the way in which a
    [Certificate][google.cloud.security.privateca.v1.Certificate]'s
    [Subject][google.cloud.security.privateca.v1.Subject] and/or
    [SubjectAltNames][google.cloud.security.privateca.v1.SubjectAltNames]
    will be resolved.
    """
    SUBJECT_REQUEST_MODE_UNSPECIFIED = 0
    DEFAULT = 1
    REFLECTED_SPIFFE = 2


class CertificateAuthority(proto.Message):
    r"""A
    [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
    represents an individual Certificate Authority. A
    [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
    can be used to create
    [Certificates][google.cloud.security.privateca.v1.Certificate].

    Attributes:
        name (str):
            Output only. The resource name for this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            in the format
            ``projects/*/locations/*/caPools/*/certificateAuthorities/*``.
        type_ (google.cloud.security.privateca_v1.types.CertificateAuthority.Type):
            Required. Immutable. The
            [Type][google.cloud.security.privateca.v1.CertificateAuthority.Type]
            of this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].
        config (google.cloud.security.privateca_v1.types.CertificateConfig):
            Required. Immutable. The config used to
            create a self-signed X.509 certificate or CSR.
        lifetime (google.protobuf.duration_pb2.Duration):
            Required. The desired lifetime of the CA certificate. Used
            to create the "not_before_time" and "not_after_time" fields
            inside an X.509 certificate.
        key_spec (google.cloud.security.privateca_v1.types.CertificateAuthority.KeyVersionSpec):
            Required. Immutable. Used when issuing certificates for this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].
            If this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            is a self-signed CertificateAuthority, this key is also used
            to sign the self-signed CA certificate. Otherwise, it is
            used to sign a CSR.
        subordinate_config (google.cloud.security.privateca_v1.types.SubordinateConfig):
            Optional. If this is a subordinate
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority],
            this field will be set with the subordinate configuration,
            which describes its issuers. This may be updated, but this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            must continue to validate.
        tier (google.cloud.security.privateca_v1.types.CaPool.Tier):
            Output only. The
            [CaPool.Tier][google.cloud.security.privateca.v1.CaPool.Tier]
            of the [CaPool][google.cloud.security.privateca.v1.CaPool]
            that includes this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].
        state (google.cloud.security.privateca_v1.types.CertificateAuthority.State):
            Output only. The
            [State][google.cloud.security.privateca.v1.CertificateAuthority.State]
            for this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].
        pem_ca_certificates (Sequence[str]):
            Output only. This
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
            certificate chain, including the current
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
            certificate. Ordered such that the root issuer is the final
            element (consistent with RFC 5246). For a self-signed CA,
            this will only list the current
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
            certificate.
        ca_certificate_descriptions (Sequence[google.cloud.security.privateca_v1.types.CertificateDescription]):
            Output only. A structured description of this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
            CA certificate and its issuers. Ordered as self-to-root.
        gcs_bucket (str):
            Immutable. The name of a Cloud Storage bucket where this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            will publish content, such as the CA certificate and CRLs.
            This must be a bucket name, without any prefixes (such as
            ``gs://``) or suffixes (such as ``.googleapis.com``). For
            example, to use a bucket named ``my-bucket``, you would
            simply specify ``my-bucket``. If not specified, a managed
            bucket will be created.
        access_urls (google.cloud.security.privateca_v1.types.CertificateAuthority.AccessUrls):
            Output only. URLs for accessing content
            published by this CA, such as the CA certificate
            and CRLs.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            was last updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            was soft deleted, if it is in the
            [DELETED][google.cloud.security.privateca.v1.CertificateAuthority.State.DELETED]
            state.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            will be permanently purged, if it is in the
            [DELETED][google.cloud.security.privateca.v1.CertificateAuthority.State.DELETED]
            state.
        labels (Sequence[google.cloud.security.privateca_v1.types.CertificateAuthority.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    class Type(proto.Enum):
        r"""The type of a
        [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority],
        indicating its issuing chain.
        """
        TYPE_UNSPECIFIED = 0
        SELF_SIGNED = 1
        SUBORDINATE = 2

    class State(proto.Enum):
        r"""The state of a
        [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority],
        indicating if it can be used.
        """
        STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        STAGED = 3
        AWAITING_USER_ACTIVATION = 4
        DELETED = 5

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

    class AccessUrls(proto.Message):
        r"""URLs where a
        [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
        will publish content.

        Attributes:
            ca_certificate_access_url (str):
                The URL where this
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
                CA certificate is published. This will only be set for CAs
                that have been activated.
            crl_access_urls (Sequence[str]):
                The URLs where this
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
                CRLs are published. This will only be set for CAs that have
                been activated.
        """

        ca_certificate_access_url = proto.Field(proto.STRING, number=1,)
        crl_access_urls = proto.RepeatedField(proto.STRING, number=2,)

    class KeyVersionSpec(proto.Message):
        r"""A Cloud KMS key configuration that a
        [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
        will use.

        Attributes:
            cloud_kms_key_version (str):
                The resource name for an existing Cloud KMS CryptoKeyVersion
                in the format
                ``projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*``.
                This option enables full flexibility in the key's
                capabilities and properties.
            algorithm (google.cloud.security.privateca_v1.types.CertificateAuthority.SignHashAlgorithm):
                The algorithm to use for creating a managed Cloud KMS key
                for a for a simplified experience. All managed keys will be
                have their
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
    config = proto.Field(proto.MESSAGE, number=3, message="CertificateConfig",)
    lifetime = proto.Field(proto.MESSAGE, number=4, message=duration_pb2.Duration,)
    key_spec = proto.Field(proto.MESSAGE, number=5, message=KeyVersionSpec,)
    subordinate_config = proto.Field(
        proto.MESSAGE, number=6, message="SubordinateConfig",
    )
    tier = proto.Field(proto.ENUM, number=7, enum="CaPool.Tier",)
    state = proto.Field(proto.ENUM, number=8, enum=State,)
    pem_ca_certificates = proto.RepeatedField(proto.STRING, number=9,)
    ca_certificate_descriptions = proto.RepeatedField(
        proto.MESSAGE, number=10, message="CertificateDescription",
    )
    gcs_bucket = proto.Field(proto.STRING, number=11,)
    access_urls = proto.Field(proto.MESSAGE, number=12, message=AccessUrls,)
    create_time = proto.Field(
        proto.MESSAGE, number=13, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=14, message=timestamp_pb2.Timestamp,
    )
    delete_time = proto.Field(
        proto.MESSAGE, number=15, message=timestamp_pb2.Timestamp,
    )
    expire_time = proto.Field(
        proto.MESSAGE, number=16, message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=17,)


class CaPool(proto.Message):
    r"""A [CaPool][google.cloud.security.privateca.v1.CaPool] represents a
    group of
    [CertificateAuthorities][google.cloud.security.privateca.v1.CertificateAuthority]
    that form a trust anchor. A
    [CaPool][google.cloud.security.privateca.v1.CaPool] can be used to
    manage issuance policies for one or more
    [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
    resources and to rotate CA certificates in and out of the trust
    anchor.

    Attributes:
        name (str):
            Output only. The resource name for this
            [CaPool][google.cloud.security.privateca.v1.CaPool] in the
            format ``projects/*/locations/*/caPools/*``.
        tier (google.cloud.security.privateca_v1.types.CaPool.Tier):
            Required. Immutable. The
            [Tier][google.cloud.security.privateca.v1.CaPool.Tier] of
            this [CaPool][google.cloud.security.privateca.v1.CaPool].
        issuance_policy (google.cloud.security.privateca_v1.types.CaPool.IssuancePolicy):
            Optional. The
            [IssuancePolicy][google.cloud.security.privateca.v1.CaPool.IssuancePolicy]
            to control how
            [Certificates][google.cloud.security.privateca.v1.Certificate]
            will be issued from this
            [CaPool][google.cloud.security.privateca.v1.CaPool].
        publishing_options (google.cloud.security.privateca_v1.types.CaPool.PublishingOptions):
            Optional. The
            [PublishingOptions][google.cloud.security.privateca.v1.CaPool.PublishingOptions]
            to follow when issuing
            [Certificates][google.cloud.security.privateca.v1.Certificate]
            from any
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            in this [CaPool][google.cloud.security.privateca.v1.CaPool].
        labels (Sequence[google.cloud.security.privateca_v1.types.CaPool.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    class Tier(proto.Enum):
        r"""The tier of a [CaPool][google.cloud.security.privateca.v1.CaPool],
        indicating its supported functionality and/or billing SKU.
        """
        TIER_UNSPECIFIED = 0
        ENTERPRISE = 1
        DEVOPS = 2

    class PublishingOptions(proto.Message):
        r"""Options relating to the publication of each
        [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
        CA certificate and CRLs and their inclusion as extensions in issued
        [Certificates][google.cloud.security.privateca.v1.Certificate]. The
        options set here apply to certificates issued by any
        [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
        in the [CaPool][google.cloud.security.privateca.v1.CaPool].

        Attributes:
            publish_ca_cert (bool):
                Required. When true, publishes each
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
                CA certificate and includes its URL in the "Authority
                Information Access" X.509 extension in all issued
                [Certificates][google.cloud.security.privateca.v1.Certificate].
                If this is false, the CA certificate will not be published
                and the corresponding X.509 extension will not be written in
                issued certificates.
            publish_crl (bool):
                Required. When true, publishes each
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]'s
                CRL and includes its URL in the "CRL Distribution Points"
                X.509 extension in all issued
                [Certificates][google.cloud.security.privateca.v1.Certificate].
                If this is false, CRLs will not be published and the
                corresponding X.509 extension will not be written in issued
                certificates. CRLs will expire 7 days from their creation.
                However, we will rebuild daily. CRLs are also rebuilt
                shortly after a certificate is revoked.
        """

        publish_ca_cert = proto.Field(proto.BOOL, number=1,)
        publish_crl = proto.Field(proto.BOOL, number=2,)

    class IssuancePolicy(proto.Message):
        r"""Defines controls over all certificate issuance within a
        [CaPool][google.cloud.security.privateca.v1.CaPool].

        Attributes:
            allowed_key_types (Sequence[google.cloud.security.privateca_v1.types.CaPool.IssuancePolicy.AllowedKeyType]):
                Optional. If any
                [AllowedKeyType][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.AllowedKeyType]
                is specified, then the certificate request's public key must
                match one of the key types listed here. Otherwise, any key
                may be used.
            maximum_lifetime (google.protobuf.duration_pb2.Duration):
                Optional. The maximum lifetime allowed for issued
                [Certificates][google.cloud.security.privateca.v1.Certificate].
                Note that if the issuing
                [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
                expires before a
                [Certificate][google.cloud.security.privateca.v1.Certificate]'s
                requested maximum_lifetime, the effective lifetime will be
                explicitly truncated to match it.
            allowed_issuance_modes (google.cloud.security.privateca_v1.types.CaPool.IssuancePolicy.IssuanceModes):
                Optional. If specified, then only methods allowed in the
                [IssuanceModes][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.IssuanceModes]
                may be used to issue
                [Certificates][google.cloud.security.privateca.v1.Certificate].
            baseline_values (google.cloud.security.privateca_v1.types.X509Parameters):
                Optional. A set of X.509 values that will be applied to all
                certificates issued through this
                [CaPool][google.cloud.security.privateca.v1.CaPool]. If a
                certificate request includes conflicting values for the same
                properties, they will be overwritten by the values defined
                here. If a certificate request uses a
                [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
                that defines conflicting
                [predefined_values][google.cloud.security.privateca.v1.CertificateTemplate.predefined_values]
                for the same properties, the certificate issuance request
                will fail.
            identity_constraints (google.cloud.security.privateca_v1.types.CertificateIdentityConstraints):
                Optional. Describes constraints on identities that may
                appear in
                [Certificates][google.cloud.security.privateca.v1.Certificate]
                issued through this
                [CaPool][google.cloud.security.privateca.v1.CaPool]. If this
                is omitted, then this
                [CaPool][google.cloud.security.privateca.v1.CaPool] will not
                add restrictions on a certificate's identity.
            passthrough_extensions (google.cloud.security.privateca_v1.types.CertificateExtensionConstraints):
                Optional. Describes the set of X.509 extensions that may
                appear in a
                [Certificate][google.cloud.security.privateca.v1.Certificate]
                issued through this
                [CaPool][google.cloud.security.privateca.v1.CaPool]. If a
                certificate request sets extensions that don't appear in the
                [passthrough_extensions][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.passthrough_extensions],
                those extensions will be dropped. If a certificate request
                uses a
                [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
                with
                [predefined_values][google.cloud.security.privateca.v1.CertificateTemplate.predefined_values]
                that don't appear here, the certificate issuance request
                will fail. If this is omitted, then this
                [CaPool][google.cloud.security.privateca.v1.CaPool] will not
                add restrictions on a certificate's X.509 extensions. These
                constraints do not apply to X.509 extensions set in this
                [CaPool][google.cloud.security.privateca.v1.CaPool]'s
                [baseline_values][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.baseline_values].
        """

        class AllowedKeyType(proto.Message):
            r"""Describes a "type" of key that may be used in a
            [Certificate][google.cloud.security.privateca.v1.Certificate] issued
            from a [CaPool][google.cloud.security.privateca.v1.CaPool]. Note
            that a single
            [AllowedKeyType][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.AllowedKeyType]
            may refer to either a fully-qualified key algorithm, such as RSA
            4096, or a family of key algorithms, such as any RSA key.

            Attributes:
                rsa (google.cloud.security.privateca_v1.types.CaPool.IssuancePolicy.AllowedKeyType.RsaKeyType):
                    Represents an allowed RSA key type.
                elliptic_curve (google.cloud.security.privateca_v1.types.CaPool.IssuancePolicy.AllowedKeyType.EcKeyType):
                    Represents an allowed Elliptic Curve key
                    type.
            """

            class RsaKeyType(proto.Message):
                r"""Describes an RSA key that may be used in a
                [Certificate][google.cloud.security.privateca.v1.Certificate] issued
                from a [CaPool][google.cloud.security.privateca.v1.CaPool].

                Attributes:
                    min_modulus_size (int):
                        Optional. The minimum allowed RSA modulus
                        size, in bits. If this is not set, or if set to
                        zero, the service-level min RSA modulus size
                        will continue to apply.
                    max_modulus_size (int):
                        Optional. The maximum allowed RSA modulus
                        size, in bits. If this is not set, or if set to
                        zero, the service will not enforce an explicit
                        upper bound on RSA modulus sizes.
                """

                min_modulus_size = proto.Field(proto.INT64, number=1,)
                max_modulus_size = proto.Field(proto.INT64, number=2,)

            class EcKeyType(proto.Message):
                r"""Describes an Elliptic Curve key that may be used in a
                [Certificate][google.cloud.security.privateca.v1.Certificate] issued
                from a [CaPool][google.cloud.security.privateca.v1.CaPool].

                Attributes:
                    signature_algorithm (google.cloud.security.privateca_v1.types.CaPool.IssuancePolicy.AllowedKeyType.EcKeyType.EcSignatureAlgorithm):
                        Optional. A signature algorithm that must be
                        used. If this is omitted, any EC-based signature
                        algorithm will be allowed.
                """

                class EcSignatureAlgorithm(proto.Enum):
                    r"""Describes an elliptic curve-based signature algorithm that may be
                    used in a
                    [Certificate][google.cloud.security.privateca.v1.Certificate] issued
                    from a [CaPool][google.cloud.security.privateca.v1.CaPool].
                    """
                    EC_SIGNATURE_ALGORITHM_UNSPECIFIED = 0
                    ECDSA_P256 = 1
                    ECDSA_P384 = 2
                    EDDSA_25519 = 3

                signature_algorithm = proto.Field(
                    proto.ENUM,
                    number=1,
                    enum="CaPool.IssuancePolicy.AllowedKeyType.EcKeyType.EcSignatureAlgorithm",
                )

            rsa = proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="key_type",
                message="CaPool.IssuancePolicy.AllowedKeyType.RsaKeyType",
            )
            elliptic_curve = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="key_type",
                message="CaPool.IssuancePolicy.AllowedKeyType.EcKeyType",
            )

        class IssuanceModes(proto.Message):
            r"""[IssuanceModes][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.IssuanceModes]
            specifies the allowed ways in which
            [Certificates][google.cloud.security.privateca.v1.Certificate] may
            be requested from this
            [CaPool][google.cloud.security.privateca.v1.CaPool].

            Attributes:
                allow_csr_based_issuance (bool):
                    Required. When true, allows callers to create
                    [Certificates][google.cloud.security.privateca.v1.Certificate]
                    by specifying a CSR.
                allow_config_based_issuance (bool):
                    Required. When true, allows callers to create
                    [Certificates][google.cloud.security.privateca.v1.Certificate]
                    by specifying a
                    [CertificateConfig][google.cloud.security.privateca.v1.CertificateConfig].
            """

            allow_csr_based_issuance = proto.Field(proto.BOOL, number=1,)
            allow_config_based_issuance = proto.Field(proto.BOOL, number=2,)

        allowed_key_types = proto.RepeatedField(
            proto.MESSAGE, number=1, message="CaPool.IssuancePolicy.AllowedKeyType",
        )
        maximum_lifetime = proto.Field(
            proto.MESSAGE, number=2, message=duration_pb2.Duration,
        )
        allowed_issuance_modes = proto.Field(
            proto.MESSAGE, number=3, message="CaPool.IssuancePolicy.IssuanceModes",
        )
        baseline_values = proto.Field(
            proto.MESSAGE, number=4, message="X509Parameters",
        )
        identity_constraints = proto.Field(
            proto.MESSAGE, number=5, message="CertificateIdentityConstraints",
        )
        passthrough_extensions = proto.Field(
            proto.MESSAGE, number=6, message="CertificateExtensionConstraints",
        )

    name = proto.Field(proto.STRING, number=1,)
    tier = proto.Field(proto.ENUM, number=2, enum=Tier,)
    issuance_policy = proto.Field(proto.MESSAGE, number=3, message=IssuancePolicy,)
    publishing_options = proto.Field(
        proto.MESSAGE, number=4, message=PublishingOptions,
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=5,)


class CertificateRevocationList(proto.Message):
    r"""A
    [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList]
    corresponds to a signed X.509 certificate Revocation List (CRL). A
    CRL contains the serial numbers of certificates that should no
    longer be trusted.

    Attributes:
        name (str):
            Output only. The resource name for this
            [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList]
            in the format
            ``projects/*/locations/*/caPools/*certificateAuthorities/*/ certificateRevocationLists/*``.
        sequence_number (int):
            Output only. The CRL sequence number that appears in
            pem_crl.
        revoked_certificates (Sequence[google.cloud.security.privateca_v1.types.CertificateRevocationList.RevokedCertificate]):
            Output only. The revoked serial numbers that appear in
            pem_crl.
        pem_crl (str):
            Output only. The PEM-encoded X.509 CRL.
        access_url (str):
            Output only. The location where 'pem_crl' can be accessed.
        state (google.cloud.security.privateca_v1.types.CertificateRevocationList.State):
            Output only. The
            [State][google.cloud.security.privateca.v1.CertificateRevocationList.State]
            for this
            [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList].
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList]
            was updated.
        revision_id (str):
            Output only. The revision ID of this
            [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList].
            A new revision is committed whenever a new CRL is published.
            The format is an 8-character hexadecimal string.
        labels (Sequence[google.cloud.security.privateca_v1.types.CertificateRevocationList.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    class State(proto.Enum):
        r"""The state of a
        [CertificateRevocationList][google.cloud.security.privateca.v1.CertificateRevocationList],
        indicating if it is current.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        SUPERSEDED = 2

    class RevokedCertificate(proto.Message):
        r"""Describes a revoked
        [Certificate][google.cloud.security.privateca.v1.Certificate].

        Attributes:
            certificate (str):
                The resource name for the
                [Certificate][google.cloud.security.privateca.v1.Certificate]
                in the format
                ``projects/*/locations/*/caPools/*/certificates/*``.
            hex_serial_number (str):
                The serial number of the
                [Certificate][google.cloud.security.privateca.v1.Certificate].
            revocation_reason (google.cloud.security.privateca_v1.types.RevocationReason):
                The reason the
                [Certificate][google.cloud.security.privateca.v1.Certificate]
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
    revision_id = proto.Field(proto.STRING, number=9,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=10,)


class Certificate(proto.Message):
    r"""A [Certificate][google.cloud.security.privateca.v1.Certificate]
    corresponds to a signed X.509 certificate issued by a
    [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].

    Attributes:
        name (str):
            Output only. The resource name for this
            [Certificate][google.cloud.security.privateca.v1.Certificate]
            in the format
            ``projects/*/locations/*/caPools/*/certificates/*``.
        pem_csr (str):
            Immutable. A pem-encoded X.509 certificate
            signing request (CSR).
        config (google.cloud.security.privateca_v1.types.CertificateConfig):
            Immutable. A description of the certificate
            and key that does not require X.509 or ASN.1.
        issuer_certificate_authority (str):
            Output only. The resource name of the issuing
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            in the format
            ``projects/*/locations/*/caPools/*/certificateAuthorities/*``.
        lifetime (google.protobuf.duration_pb2.Duration):
            Required. Immutable. The desired lifetime of a certificate.
            Used to create the "not_before_time" and "not_after_time"
            fields inside an X.509 certificate. Note that the lifetime
            may be truncated if it would extend past the life of any
            certificate authority in the issuing chain.
        certificate_template (str):
            Immutable. The resource name for a
            [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
            used to issue this certificate, in the format
            ``projects/*/locations/*/certificateTemplates/*``. If this
            is specified, the caller must have the necessary permission
            to use this template. If this is omitted, no template will
            be used. This template must be in the same location as the
            [Certificate][google.cloud.security.privateca.v1.Certificate].
        subject_mode (google.cloud.security.privateca_v1.types.SubjectRequestMode):
            Immutable. Specifies how the
            [Certificate][google.cloud.security.privateca.v1.Certificate]'s
            identity fields are to be decided. If this is omitted, the
            ``DEFAULT`` subject mode will be used.
        revocation_details (google.cloud.security.privateca_v1.types.Certificate.RevocationDetails):
            Output only. Details regarding the revocation of this
            [Certificate][google.cloud.security.privateca.v1.Certificate].
            This
            [Certificate][google.cloud.security.privateca.v1.Certificate]
            is considered revoked if and only if this field is present.
        pem_certificate (str):
            Output only. The pem-encoded, signed X.509
            certificate.
        certificate_description (google.cloud.security.privateca_v1.types.CertificateDescription):
            Output only. A structured description of the
            issued X.509 certificate.
        pem_certificate_chain (Sequence[str]):
            Output only. The chain that may be used to
            verify the X.509 certificate. Expected to be in
            issuer-to-root order according to RFC 5246.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [Certificate][google.cloud.security.privateca.v1.Certificate]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [Certificate][google.cloud.security.privateca.v1.Certificate]
            was updated.
        labels (Sequence[google.cloud.security.privateca_v1.types.Certificate.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    class RevocationDetails(proto.Message):
        r"""Describes fields that are relavent to the revocation of a
        [Certificate][google.cloud.security.privateca.v1.Certificate].

        Attributes:
            revocation_state (google.cloud.security.privateca_v1.types.RevocationReason):
                Indicates why a
                [Certificate][google.cloud.security.privateca.v1.Certificate]
                was revoked.
            revocation_time (google.protobuf.timestamp_pb2.Timestamp):
                The time at which this
                [Certificate][google.cloud.security.privateca.v1.Certificate]
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
    issuer_certificate_authority = proto.Field(proto.STRING, number=4,)
    lifetime = proto.Field(proto.MESSAGE, number=5, message=duration_pb2.Duration,)
    certificate_template = proto.Field(proto.STRING, number=6,)
    subject_mode = proto.Field(proto.ENUM, number=7, enum="SubjectRequestMode",)
    revocation_details = proto.Field(
        proto.MESSAGE, number=8, message=RevocationDetails,
    )
    pem_certificate = proto.Field(proto.STRING, number=9,)
    certificate_description = proto.Field(
        proto.MESSAGE, number=10, message="CertificateDescription",
    )
    pem_certificate_chain = proto.RepeatedField(proto.STRING, number=11,)
    create_time = proto.Field(
        proto.MESSAGE, number=12, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=13, message=timestamp_pb2.Timestamp,
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=14,)


class CertificateTemplate(proto.Message):
    r"""A
    [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
    refers to a managed template for certificate issuance.

    Attributes:
        name (str):
            Output only. The resource name for this
            [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
            in the format
            ``projects/*/locations/*/certificateTemplates/*``.
        predefined_values (google.cloud.security.privateca_v1.types.X509Parameters):
            Optional. A set of X.509 values that will be applied to all
            issued certificates that use this template. If the
            certificate request includes conflicting values for the same
            properties, they will be overwritten by the values defined
            here. If the issuing
            [CaPool][google.cloud.security.privateca.v1.CaPool]'s
            [IssuancePolicy][google.cloud.security.privateca.v1.CaPool.IssuancePolicy]
            defines conflicting
            [baseline_values][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.baseline_values]
            for the same properties, the certificate issuance request
            will fail.
        identity_constraints (google.cloud.security.privateca_v1.types.CertificateIdentityConstraints):
            Optional. Describes constraints on identities that may be
            appear in
            [Certificates][google.cloud.security.privateca.v1.Certificate]
            issued using this template. If this is omitted, then this
            template will not add restrictions on a certificate's
            identity.
        passthrough_extensions (google.cloud.security.privateca_v1.types.CertificateExtensionConstraints):
            Optional. Describes the set of X.509 extensions that may
            appear in a
            [Certificate][google.cloud.security.privateca.v1.Certificate]
            issued using this
            [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate].
            If a certificate request sets extensions that don't appear
            in the
            [passthrough_extensions][google.cloud.security.privateca.v1.CertificateTemplate.passthrough_extensions],
            those extensions will be dropped. If the issuing
            [CaPool][google.cloud.security.privateca.v1.CaPool]'s
            [IssuancePolicy][google.cloud.security.privateca.v1.CaPool.IssuancePolicy]
            defines
            [baseline_values][google.cloud.security.privateca.v1.CaPool.IssuancePolicy.baseline_values]
            that don't appear here, the certificate issuance request
            will fail. If this is omitted, then this template will not
            add restrictions on a certificate's X.509 extensions. These
            constraints do not apply to X.509 extensions set in this
            [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]'s
            [predefined_values][google.cloud.security.privateca.v1.CertificateTemplate.predefined_values].
        description (str):
            Optional. A human-readable description of
            scenarios this template is intended for.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
            was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CertificateTemplate][google.cloud.security.privateca.v1.CertificateTemplate]
            was updated.
        labels (Sequence[google.cloud.security.privateca_v1.types.CertificateTemplate.LabelsEntry]):
            Optional. Labels with user-defined metadata.
    """

    name = proto.Field(proto.STRING, number=1,)
    predefined_values = proto.Field(proto.MESSAGE, number=2, message="X509Parameters",)
    identity_constraints = proto.Field(
        proto.MESSAGE, number=3, message="CertificateIdentityConstraints",
    )
    passthrough_extensions = proto.Field(
        proto.MESSAGE, number=4, message="CertificateExtensionConstraints",
    )
    description = proto.Field(proto.STRING, number=5,)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=8,)


class X509Parameters(proto.Message):
    r"""An
    [X509Parameters][google.cloud.security.privateca.v1.X509Parameters]
    is used to describe certain fields of an X.509 certificate, such as
    the key usage fields, fields specific to CA certificates,
    certificate policy extensions and custom extensions.

    Attributes:
        key_usage (google.cloud.security.privateca_v1.types.KeyUsage):
            Optional. Indicates the intended use for keys
            that correspond to a certificate.
        ca_options (google.cloud.security.privateca_v1.types.X509Parameters.CaOptions):
            Optional. Describes options in this
            [X509Parameters][google.cloud.security.privateca.v1.X509Parameters]
            that are relevant in a CA certificate.
        policy_ids (Sequence[google.cloud.security.privateca_v1.types.ObjectId]):
            Optional. Describes the X.509 certificate
            policy object identifiers, per
            https://tools.ietf.org/html/rfc5280#section-4.2.1.4.
        aia_ocsp_servers (Sequence[str]):
            Optional. Describes Online Certificate Status
            Protocol (OCSP) endpoint addresses that appear
            in the "Authority Information Access" extension
            in the certificate.
        additional_extensions (Sequence[google.cloud.security.privateca_v1.types.X509Extension]):
            Optional. Describes custom X.509 extensions.
    """

    class CaOptions(proto.Message):
        r"""Describes values that are relevant in a CA certificate.
        Attributes:
            is_ca (bool):
                Optional. Refers to the "CA" X.509 extension,
                which is a boolean value. When this value is
                missing, the extension will be omitted from the
                CA certificate.
            max_issuer_path_length (int):
                Optional. Refers to the path length
                restriction X.509 extension. For a CA
                certificate, this value describes the depth of
                subordinate CA certificates that are allowed.
                If this value is less than 0, the request will
                fail. If this value is missing, the max path
                length will be omitted from the CA certificate.
        """

        is_ca = proto.Field(proto.BOOL, number=1, optional=True,)
        max_issuer_path_length = proto.Field(proto.INT32, number=2, optional=True,)

    key_usage = proto.Field(proto.MESSAGE, number=1, message="KeyUsage",)
    ca_options = proto.Field(proto.MESSAGE, number=2, message=CaOptions,)
    policy_ids = proto.RepeatedField(proto.MESSAGE, number=3, message="ObjectId",)
    aia_ocsp_servers = proto.RepeatedField(proto.STRING, number=4,)
    additional_extensions = proto.RepeatedField(
        proto.MESSAGE, number=5, message="X509Extension",
    )


class SubordinateConfig(proto.Message):
    r"""Describes a subordinate CA's issuers. This is either a resource name
    to a known issuing
    [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority],
    or a PEM issuer certificate chain.

    Attributes:
        certificate_authority (str):
            Required. This can refer to a
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            in the same project that was used to create a subordinate
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority].
            This field is used for information and usability purposes
            only. The resource name is in the format
            ``projects/*/locations/*/caPools/*/certificateAuthorities/*``.
        pem_issuer_chain (google.cloud.security.privateca_v1.types.SubordinateConfig.SubordinateConfigChain):
            Required. Contains the PEM certificate chain for the issuers
            of this
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority],
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
    r"""A [PublicKey][google.cloud.security.privateca.v1.PublicKey]
    describes a public key.

    Attributes:
        key (bytes):
            Required. A public key. The padding and encoding must match
            with the ``KeyFormat`` value specified for the ``format``
            field.
        format_ (google.cloud.security.privateca_v1.types.PublicKey.KeyFormat):
            Required. The format of the public key.
    """

    class KeyFormat(proto.Enum):
        r"""Types of public keys formats that are supported. Currently, only
        ``PEM`` format is supported.
        """
        KEY_FORMAT_UNSPECIFIED = 0
        PEM = 1

    key = proto.Field(proto.BYTES, number=1,)
    format_ = proto.Field(proto.ENUM, number=2, enum=KeyFormat,)


class CertificateConfig(proto.Message):
    r"""A
    [CertificateConfig][google.cloud.security.privateca.v1.CertificateConfig]
    describes an X.509 certificate or CSR that is to be created, as an
    alternative to using ASN.1.

    Attributes:
        subject_config (google.cloud.security.privateca_v1.types.CertificateConfig.SubjectConfig):
            Required. Specifies some of the values in a
            certificate that are related to the subject.
        x509_config (google.cloud.security.privateca_v1.types.X509Parameters):
            Required. Describes how some of the technical
            X.509 fields in a certificate should be
            populated.
        public_key (google.cloud.security.privateca_v1.types.PublicKey):
            Optional. The public key that corresponds to this config.
            This is, for example, used when issuing
            [Certificates][google.cloud.security.privateca.v1.Certificate],
            but not when creating a self-signed
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            or
            [CertificateAuthority][google.cloud.security.privateca.v1.CertificateAuthority]
            CSR.
    """

    class SubjectConfig(proto.Message):
        r"""These values are used to create the distinguished name and
        subject alternative name fields in an X.509 certificate.

        Attributes:
            subject (google.cloud.security.privateca_v1.types.Subject):
                Required. Contains distinguished name fields
                such as the common name, location and
                organization.
            subject_alt_name (google.cloud.security.privateca_v1.types.SubjectAltNames):
                Optional. The subject alternative name
                fields.
        """

        subject = proto.Field(proto.MESSAGE, number=1, message="Subject",)
        subject_alt_name = proto.Field(
            proto.MESSAGE, number=2, message="SubjectAltNames",
        )

    subject_config = proto.Field(proto.MESSAGE, number=1, message=SubjectConfig,)
    x509_config = proto.Field(proto.MESSAGE, number=2, message="X509Parameters",)
    public_key = proto.Field(proto.MESSAGE, number=3, message="PublicKey",)


class CertificateDescription(proto.Message):
    r"""A
    [CertificateDescription][google.cloud.security.privateca.v1.CertificateDescription]
    describes an X.509 certificate or CSR that has been issued, as an
    alternative to using ASN.1 / X.509.

    Attributes:
        subject_description (google.cloud.security.privateca_v1.types.CertificateDescription.SubjectDescription):
            Describes some of the values in a certificate
            that are related to the subject and lifetime.
        x509_description (google.cloud.security.privateca_v1.types.X509Parameters):
            Describes some of the technical X.509 fields
            in a certificate.
        public_key (google.cloud.security.privateca_v1.types.PublicKey):
            The public key that corresponds to an issued
            certificate.
        subject_key_id (google.cloud.security.privateca_v1.types.CertificateDescription.KeyId):
            Provides a means of identifiying certificates
            that contain a particular public key, per
            https://tools.ietf.org/html/rfc5280#section-4.2.1.2.
        authority_key_id (google.cloud.security.privateca_v1.types.CertificateDescription.KeyId):
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
        cert_fingerprint (google.cloud.security.privateca_v1.types.CertificateDescription.CertificateFingerprint):
            The hash of the x.509 certificate.
    """

    class SubjectDescription(proto.Message):
        r"""These values describe fields in an issued X.509 certificate
        such as the distinguished name, subject alternative names,
        serial number, and lifetime.

        Attributes:
            subject (google.cloud.security.privateca_v1.types.Subject):
                Contains distinguished name fields such as
                the common name, location and / organization.
            subject_alt_name (google.cloud.security.privateca_v1.types.SubjectAltNames):
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
        subject_alt_name = proto.Field(
            proto.MESSAGE, number=2, message="SubjectAltNames",
        )
        hex_serial_number = proto.Field(proto.STRING, number=3,)
        lifetime = proto.Field(proto.MESSAGE, number=4, message=duration_pb2.Duration,)
        not_before_time = proto.Field(
            proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
        )
        not_after_time = proto.Field(
            proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
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
    x509_description = proto.Field(proto.MESSAGE, number=2, message="X509Parameters",)
    public_key = proto.Field(proto.MESSAGE, number=3, message="PublicKey",)
    subject_key_id = proto.Field(proto.MESSAGE, number=4, message=KeyId,)
    authority_key_id = proto.Field(proto.MESSAGE, number=5, message=KeyId,)
    crl_distribution_points = proto.RepeatedField(proto.STRING, number=6,)
    aia_issuing_certificate_urls = proto.RepeatedField(proto.STRING, number=7,)
    cert_fingerprint = proto.Field(
        proto.MESSAGE, number=8, message=CertificateFingerprint,
    )


class ObjectId(proto.Message):
    r"""An [ObjectId][google.cloud.security.privateca.v1.ObjectId] specifies
    an object identifier (OID). These provide context and describe types
    in ASN.1 messages.

    Attributes:
        object_id_path (Sequence[int]):
            Required. The parts of an OID path. The most
            significant parts of the path come first.
    """

    object_id_path = proto.RepeatedField(proto.INT32, number=1,)


class X509Extension(proto.Message):
    r"""An [X509Extension][google.cloud.security.privateca.v1.X509Extension]
    specifies an X.509 extension, which may be used in different parts
    of X.509 objects like certificates, CSRs, and CRLs.

    Attributes:
        object_id (google.cloud.security.privateca_v1.types.ObjectId):
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
    r"""A [KeyUsage][google.cloud.security.privateca.v1.KeyUsage] describes
    key usage values that may appear in an X.509 certificate.

    Attributes:
        base_key_usage (google.cloud.security.privateca_v1.types.KeyUsage.KeyUsageOptions):
            Describes high-level ways in which a key may
            be used.
        extended_key_usage (google.cloud.security.privateca_v1.types.KeyUsage.ExtendedKeyUsageOptions):
            Detailed scenarios in which a key may be
            used.
        unknown_extended_key_usages (Sequence[google.cloud.security.privateca_v1.types.ObjectId]):
            Used to describe extended key usages that are not listed in
            the
            [KeyUsage.ExtendedKeyUsageOptions][google.cloud.security.privateca.v1.KeyUsage.ExtendedKeyUsageOptions]
            message.
    """

    class KeyUsageOptions(proto.Message):
        r"""[KeyUsage.KeyUsageOptions][google.cloud.security.privateca.v1.KeyUsage.KeyUsageOptions]
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
        r"""[KeyUsage.ExtendedKeyUsageOptions][google.cloud.security.privateca.v1.KeyUsage.ExtendedKeyUsageOptions]
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
    r"""[Subject][google.cloud.security.privateca.v1.Subject] describes
    parts of a distinguished name that, in turn, describes the subject
    of the certificate.

    Attributes:
        common_name (str):
            The "common name" of the subject.
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

    common_name = proto.Field(proto.STRING, number=1,)
    country_code = proto.Field(proto.STRING, number=2,)
    organization = proto.Field(proto.STRING, number=3,)
    organizational_unit = proto.Field(proto.STRING, number=4,)
    locality = proto.Field(proto.STRING, number=5,)
    province = proto.Field(proto.STRING, number=6,)
    street_address = proto.Field(proto.STRING, number=7,)
    postal_code = proto.Field(proto.STRING, number=8,)


class SubjectAltNames(proto.Message):
    r"""[SubjectAltNames][google.cloud.security.privateca.v1.SubjectAltNames]
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
        custom_sans (Sequence[google.cloud.security.privateca_v1.types.X509Extension]):
            Contains additional subject alternative name
            values.
    """

    dns_names = proto.RepeatedField(proto.STRING, number=1,)
    uris = proto.RepeatedField(proto.STRING, number=2,)
    email_addresses = proto.RepeatedField(proto.STRING, number=3,)
    ip_addresses = proto.RepeatedField(proto.STRING, number=4,)
    custom_sans = proto.RepeatedField(proto.MESSAGE, number=5, message="X509Extension",)


class CertificateIdentityConstraints(proto.Message):
    r"""Describes constraints on a
    [Certificate][google.cloud.security.privateca.v1.Certificate]'s
    [Subject][google.cloud.security.privateca.v1.Subject] and
    [SubjectAltNames][google.cloud.security.privateca.v1.SubjectAltNames].

    Attributes:
        cel_expression (google.type.expr_pb2.Expr):
            Optional. A CEL expression that may be used
            to validate the resolved X.509 Subject and/or
            Subject Alternative Name before a certificate is
            signed. To see the full allowed syntax and some
            examples, see
            https://cloud.google.com/certificate-authority-
            service/docs/cel-guide
        allow_subject_passthrough (bool):
            Required. If this is true, the
            [Subject][google.cloud.security.privateca.v1.Subject] field
            may be copied from a certificate request into the signed
            certificate. Otherwise, the requested
            [Subject][google.cloud.security.privateca.v1.Subject] will
            be discarded. The bool is optional to indicate an unset
            field, which suggests a forgotten value that needs to be set
            by the caller.
        allow_subject_alt_names_passthrough (bool):
            Required. If this is true, the
            [SubjectAltNames][google.cloud.security.privateca.v1.SubjectAltNames]
            extension may be copied from a certificate request into the
            signed certificate. Otherwise, the requested
            [SubjectAltNames][google.cloud.security.privateca.v1.SubjectAltNames]
            will be discarded. The bool is optional to indicate an unset
            field, which suggests a forgotten value that needs to be set
            by the caller.
    """

    cel_expression = proto.Field(proto.MESSAGE, number=1, message=expr_pb2.Expr,)
    allow_subject_passthrough = proto.Field(proto.BOOL, number=2, optional=True,)
    allow_subject_alt_names_passthrough = proto.Field(
        proto.BOOL, number=3, optional=True,
    )


class CertificateExtensionConstraints(proto.Message):
    r"""Describes a set of X.509 extensions that may be part of some
    certificate issuance controls.

    Attributes:
        known_extensions (Sequence[google.cloud.security.privateca_v1.types.CertificateExtensionConstraints.KnownCertificateExtension]):
            Optional. A set of named X.509 extensions. Will be combined
            with
            [additional_extensions][google.cloud.security.privateca.v1.CertificateExtensionConstraints.additional_extensions]
            to determine the full set of X.509 extensions.
        additional_extensions (Sequence[google.cloud.security.privateca_v1.types.ObjectId]):
            Optional. A set of
            [ObjectIds][google.cloud.security.privateca.v1.ObjectId]
            identifying custom X.509 extensions. Will be combined with
            [known_extensions][google.cloud.security.privateca.v1.CertificateExtensionConstraints.known_extensions]
            to determine the full set of X.509 extensions.
    """

    class KnownCertificateExtension(proto.Enum):
        r"""Describes well-known X.509 extensions that can appear in a
        [Certificate][google.cloud.security.privateca.v1.Certificate], not
        including the
        [SubjectAltNames][google.cloud.security.privateca.v1.SubjectAltNames]
        extension.
        """
        KNOWN_CERTIFICATE_EXTENSION_UNSPECIFIED = 0
        BASE_KEY_USAGE = 1
        EXTENDED_KEY_USAGE = 2
        CA_OPTIONS = 3
        POLICY_IDS = 4
        AIA_OCSP_SERVERS = 5

    known_extensions = proto.RepeatedField(
        proto.ENUM, number=1, enum=KnownCertificateExtension,
    )
    additional_extensions = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ObjectId",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
