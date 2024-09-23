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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.kms.v1",
    manifest={
        "ProtectionLevel",
        "AccessReason",
        "KeyRing",
        "CryptoKey",
        "CryptoKeyVersionTemplate",
        "KeyOperationAttestation",
        "CryptoKeyVersion",
        "PublicKey",
        "ImportJob",
        "ExternalProtectionLevelOptions",
        "KeyAccessJustificationsPolicy",
    },
)


class ProtectionLevel(proto.Enum):
    r"""[ProtectionLevel][google.cloud.kms.v1.ProtectionLevel] specifies how
    cryptographic operations are performed. For more information, see
    [Protection levels]
    (https://cloud.google.com/kms/docs/algorithms#protection_levels).

    Values:
        PROTECTION_LEVEL_UNSPECIFIED (0):
            Not specified.
        SOFTWARE (1):
            Crypto operations are performed in software.
        HSM (2):
            Crypto operations are performed in a Hardware
            Security Module.
        EXTERNAL (3):
            Crypto operations are performed by an
            external key manager.
        EXTERNAL_VPC (4):
            Crypto operations are performed in an
            EKM-over-VPC backend.
    """
    PROTECTION_LEVEL_UNSPECIFIED = 0
    SOFTWARE = 1
    HSM = 2
    EXTERNAL = 3
    EXTERNAL_VPC = 4


class AccessReason(proto.Enum):
    r"""Describes the reason for a data access. Please refer to
    https://cloud.google.com/assured-workloads/key-access-justifications/docs/justification-codes
    for the detailed semantic meaning of justification reason codes.

    Values:
        REASON_UNSPECIFIED (0):
            Unspecified access reason.
        CUSTOMER_INITIATED_SUPPORT (1):
            Customer-initiated support.
        GOOGLE_INITIATED_SERVICE (2):
            Google-initiated access for system management
            and troubleshooting.
        THIRD_PARTY_DATA_REQUEST (3):
            Google-initiated access in response to a
            legal request or legal process.
        GOOGLE_INITIATED_REVIEW (4):
            Google-initiated access for security, fraud,
            abuse, or compliance purposes.
        CUSTOMER_INITIATED_ACCESS (5):
            Customer uses their account to perform any
            access to their own data which their IAM policy
            authorizes.
        GOOGLE_INITIATED_SYSTEM_OPERATION (6):
            Google systems access customer data to help
            optimize the structure of the data or quality
            for future uses by the customer.
        REASON_NOT_EXPECTED (7):
            No reason is expected for this key request.
        MODIFIED_CUSTOMER_INITIATED_ACCESS (8):
            Customer uses their account to perform any access to their
            own data which their IAM policy authorizes, and one of the
            following is true:

            -  A Google administrator has reset the root-access account
               associated with the user's organization within the past 7
               days.
            -  A Google-initiated emergency access operation has
               interacted with a resource in the same project or folder
               as the currently accessed resource within the past 7
               days.
        MODIFIED_GOOGLE_INITIATED_SYSTEM_OPERATION (9):
            Google systems access customer data to help optimize the
            structure of the data or quality for future uses by the
            customer, and one of the following is true:

            -  A Google administrator has reset the root-access account
               associated with the user's organization within the past 7
               days.
            -  A Google-initiated emergency access operation has
               interacted with a resource in the same project or folder
               as the currently accessed resource within the past 7
               days.
        GOOGLE_RESPONSE_TO_PRODUCTION_ALERT (10):
            Google-initiated access to maintain system
            reliability.
        CUSTOMER_AUTHORIZED_WORKFLOW_SERVICING (11):
            One of the following operations is being executed while
            simultaneously encountering an internal technical issue
            which prevented a more precise justification code from being
            generated:

            -  Your account has been used to perform any access to your
               own data which your IAM policy authorizes.
            -  An automated Google system operates on encrypted customer
               data which your IAM policy authorizes.
            -  Customer-initiated Google support access.
            -  Google-initiated support access to protect system
               reliability.
    """
    REASON_UNSPECIFIED = 0
    CUSTOMER_INITIATED_SUPPORT = 1
    GOOGLE_INITIATED_SERVICE = 2
    THIRD_PARTY_DATA_REQUEST = 3
    GOOGLE_INITIATED_REVIEW = 4
    CUSTOMER_INITIATED_ACCESS = 5
    GOOGLE_INITIATED_SYSTEM_OPERATION = 6
    REASON_NOT_EXPECTED = 7
    MODIFIED_CUSTOMER_INITIATED_ACCESS = 8
    MODIFIED_GOOGLE_INITIATED_SYSTEM_OPERATION = 9
    GOOGLE_RESPONSE_TO_PRODUCTION_ALERT = 10
    CUSTOMER_AUTHORIZED_WORKFLOW_SERVICING = 11


class KeyRing(proto.Message):
    r"""A [KeyRing][google.cloud.kms.v1.KeyRing] is a toplevel logical
    grouping of [CryptoKeys][google.cloud.kms.v1.CryptoKey].

    Attributes:
        name (str):
            Output only. The resource name for the
            [KeyRing][google.cloud.kms.v1.KeyRing] in the format
            ``projects/*/locations/*/keyRings/*``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [KeyRing][google.cloud.kms.v1.KeyRing] was created.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class CryptoKey(proto.Message):
    r"""A [CryptoKey][google.cloud.kms.v1.CryptoKey] represents a logical
    key that can be used for cryptographic operations.

    A [CryptoKey][google.cloud.kms.v1.CryptoKey] is made up of zero or
    more [versions][google.cloud.kms.v1.CryptoKeyVersion], which
    represent the actual key material used in cryptographic operations.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The resource name for this
            [CryptoKey][google.cloud.kms.v1.CryptoKey] in the format
            ``projects/*/locations/*/keyRings/*/cryptoKeys/*``.
        primary (google.cloud.kms_v1.types.CryptoKeyVersion):
            Output only. A copy of the "primary"
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            that will be used by
            [Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt]
            when this [CryptoKey][google.cloud.kms.v1.CryptoKey] is
            given in
            [EncryptRequest.name][google.cloud.kms.v1.EncryptRequest.name].

            The [CryptoKey][google.cloud.kms.v1.CryptoKey]'s primary
            version can be updated via
            [UpdateCryptoKeyPrimaryVersion][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKeyPrimaryVersion].

            Keys with [purpose][google.cloud.kms.v1.CryptoKey.purpose]
            [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT]
            may have a primary. For other keys, this field will be
            omitted.
        purpose (google.cloud.kms_v1.types.CryptoKey.CryptoKeyPurpose):
            Immutable. The immutable purpose of this
            [CryptoKey][google.cloud.kms.v1.CryptoKey].
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CryptoKey][google.cloud.kms.v1.CryptoKey] was created.
        next_rotation_time (google.protobuf.timestamp_pb2.Timestamp):
            At
            [next_rotation_time][google.cloud.kms.v1.CryptoKey.next_rotation_time],
            the Key Management Service will automatically:

            1. Create a new version of this
               [CryptoKey][google.cloud.kms.v1.CryptoKey].
            2. Mark the new version as primary.

            Key rotations performed manually via
            [CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion]
            and
            [UpdateCryptoKeyPrimaryVersion][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKeyPrimaryVersion]
            do not affect
            [next_rotation_time][google.cloud.kms.v1.CryptoKey.next_rotation_time].

            Keys with [purpose][google.cloud.kms.v1.CryptoKey.purpose]
            [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT]
            support automatic rotation. For other keys, this field must
            be omitted.
        rotation_period (google.protobuf.duration_pb2.Duration):
            [next_rotation_time][google.cloud.kms.v1.CryptoKey.next_rotation_time]
            will be advanced by this period when the service
            automatically rotates a key. Must be at least 24 hours and
            at most 876,000 hours.

            If
            [rotation_period][google.cloud.kms.v1.CryptoKey.rotation_period]
            is set,
            [next_rotation_time][google.cloud.kms.v1.CryptoKey.next_rotation_time]
            must also be set.

            Keys with [purpose][google.cloud.kms.v1.CryptoKey.purpose]
            [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT]
            support automatic rotation. For other keys, this field must
            be omitted.

            This field is a member of `oneof`_ ``rotation_schedule``.
        version_template (google.cloud.kms_v1.types.CryptoKeyVersionTemplate):
            A template describing settings for new
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            instances. The properties of new
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            instances created by either
            [CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion]
            or auto-rotation are controlled by this template.
        labels (MutableMapping[str, str]):
            Labels with user-defined metadata. For more information, see
            `Labeling
            Keys <https://cloud.google.com/kms/docs/labeling-keys>`__.
        import_only (bool):
            Immutable. Whether this key may contain
            imported versions only.
        destroy_scheduled_duration (google.protobuf.duration_pb2.Duration):
            Immutable. The period of time that versions of this key
            spend in the
            [DESTROY_SCHEDULED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DESTROY_SCHEDULED]
            state before transitioning to
            [DESTROYED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DESTROYED].
            If not specified at creation time, the default duration is
            30 days.
        crypto_key_backend (str):
            Immutable. The resource name of the backend environment
            where the key material for all
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
            associated with this
            [CryptoKey][google.cloud.kms.v1.CryptoKey] reside and where
            all related cryptographic operations are performed. Only
            applicable if
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
            have a
            [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel] of
            [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC],
            with the resource name in the format
            ``projects/*/locations/*/ekmConnections/*``. Note, this list
            is non-exhaustive and may apply to additional
            [ProtectionLevels][google.cloud.kms.v1.ProtectionLevel] in
            the future.
        key_access_justifications_policy (google.cloud.kms_v1.types.KeyAccessJustificationsPolicy):
            Optional. The policy used for Key Access
            Justifications Policy Enforcement. If this field
            is present and this key is enrolled in Key
            Access Justifications Policy Enforcement, the
            policy will be evaluated in encrypt, decrypt,
            and sign operations, and the operation will fail
            if rejected by the policy. The policy is defined
            by specifying zero or more allowed justification
            codes.
            https://cloud.google.com/assured-workloads/key-access-justifications/docs/justification-codes
            By default, this field is absent, and all
            justification codes are allowed.
    """

    class CryptoKeyPurpose(proto.Enum):
        r"""[CryptoKeyPurpose][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose]
        describes the cryptographic capabilities of a
        [CryptoKey][google.cloud.kms.v1.CryptoKey]. A given key can only be
        used for the operations allowed by its purpose. For more
        information, see `Key
        purposes <https://cloud.google.com/kms/docs/algorithms#key_purposes>`__.

        Values:
            CRYPTO_KEY_PURPOSE_UNSPECIFIED (0):
                Not specified.
            ENCRYPT_DECRYPT (1):
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] with this
                purpose may be used with
                [Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt]
                and
                [Decrypt][google.cloud.kms.v1.KeyManagementService.Decrypt].
            ASYMMETRIC_SIGN (5):
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] with this
                purpose may be used with
                [AsymmetricSign][google.cloud.kms.v1.KeyManagementService.AsymmetricSign]
                and
                [GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey].
            ASYMMETRIC_DECRYPT (6):
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] with this
                purpose may be used with
                [AsymmetricDecrypt][google.cloud.kms.v1.KeyManagementService.AsymmetricDecrypt]
                and
                [GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey].
            RAW_ENCRYPT_DECRYPT (7):
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] with this
                purpose may be used with
                [RawEncrypt][google.cloud.kms.v1.KeyManagementService.RawEncrypt]
                and
                [RawDecrypt][google.cloud.kms.v1.KeyManagementService.RawDecrypt].
                This purpose is meant to be used for interoperable symmetric
                encryption and does not support automatic CryptoKey
                rotation.
            MAC (9):
                [CryptoKeys][google.cloud.kms.v1.CryptoKey] with this
                purpose may be used with
                [MacSign][google.cloud.kms.v1.KeyManagementService.MacSign].
        """
        CRYPTO_KEY_PURPOSE_UNSPECIFIED = 0
        ENCRYPT_DECRYPT = 1
        ASYMMETRIC_SIGN = 5
        ASYMMETRIC_DECRYPT = 6
        RAW_ENCRYPT_DECRYPT = 7
        MAC = 9

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    primary: "CryptoKeyVersion" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="CryptoKeyVersion",
    )
    purpose: CryptoKeyPurpose = proto.Field(
        proto.ENUM,
        number=3,
        enum=CryptoKeyPurpose,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    next_rotation_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    rotation_period: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="rotation_schedule",
        message=duration_pb2.Duration,
    )
    version_template: "CryptoKeyVersionTemplate" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="CryptoKeyVersionTemplate",
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=10,
    )
    import_only: bool = proto.Field(
        proto.BOOL,
        number=13,
    )
    destroy_scheduled_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=14,
        message=duration_pb2.Duration,
    )
    crypto_key_backend: str = proto.Field(
        proto.STRING,
        number=15,
    )
    key_access_justifications_policy: "KeyAccessJustificationsPolicy" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="KeyAccessJustificationsPolicy",
    )


class CryptoKeyVersionTemplate(proto.Message):
    r"""A
    [CryptoKeyVersionTemplate][google.cloud.kms.v1.CryptoKeyVersionTemplate]
    specifies the properties to use when creating a new
    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion], either
    manually with
    [CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion]
    or automatically as a result of auto-rotation.

    Attributes:
        protection_level (google.cloud.kms_v1.types.ProtectionLevel):
            [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel] to
            use when creating a
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            based on this template. Immutable. Defaults to
            [SOFTWARE][google.cloud.kms.v1.ProtectionLevel.SOFTWARE].
        algorithm (google.cloud.kms_v1.types.CryptoKeyVersion.CryptoKeyVersionAlgorithm):
            Required.
            [Algorithm][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm]
            to use when creating a
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            based on this template.

            For backwards compatibility, GOOGLE_SYMMETRIC_ENCRYPTION is
            implied if both this field is omitted and
            [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
            is
            [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT].
    """

    protection_level: "ProtectionLevel" = proto.Field(
        proto.ENUM,
        number=1,
        enum="ProtectionLevel",
    )
    algorithm: "CryptoKeyVersion.CryptoKeyVersionAlgorithm" = proto.Field(
        proto.ENUM,
        number=3,
        enum="CryptoKeyVersion.CryptoKeyVersionAlgorithm",
    )


class KeyOperationAttestation(proto.Message):
    r"""Contains an HSM-generated attestation about a key operation. For
    more information, see [Verifying attestations]
    (https://cloud.google.com/kms/docs/attest-key).

    Attributes:
        format (google.cloud.kms_v1.types.KeyOperationAttestation.AttestationFormat):
            Output only. The format of the attestation
            data.
        content (bytes):
            Output only. The attestation data provided by
            the HSM when the key operation was performed.
        cert_chains (google.cloud.kms_v1.types.KeyOperationAttestation.CertificateChains):
            Output only. The certificate chains needed to
            validate the attestation
    """

    class AttestationFormat(proto.Enum):
        r"""Attestation formats provided by the HSM.

        Values:
            ATTESTATION_FORMAT_UNSPECIFIED (0):
                Not specified.
            CAVIUM_V1_COMPRESSED (3):
                Cavium HSM attestation compressed with gzip.
                Note that this format is defined by Cavium and
                subject to change at any time.

                See
                https://www.marvell.com/products/security-solutions/nitrox-hs-adapters/software-key-attestation.html.
            CAVIUM_V2_COMPRESSED (4):
                Cavium HSM attestation V2 compressed with
                gzip. This is a new format introduced in
                Cavium's version 3.2-08.
        """
        ATTESTATION_FORMAT_UNSPECIFIED = 0
        CAVIUM_V1_COMPRESSED = 3
        CAVIUM_V2_COMPRESSED = 4

    class CertificateChains(proto.Message):
        r"""Certificate chains needed to verify the attestation.
        Certificates in chains are PEM-encoded and are ordered based on
        https://tools.ietf.org/html/rfc5246#section-7.4.2.

        Attributes:
            cavium_certs (MutableSequence[str]):
                Cavium certificate chain corresponding to the
                attestation.
            google_card_certs (MutableSequence[str]):
                Google card certificate chain corresponding
                to the attestation.
            google_partition_certs (MutableSequence[str]):
                Google partition certificate chain
                corresponding to the attestation.
        """

        cavium_certs: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        google_card_certs: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        google_partition_certs: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )

    format: AttestationFormat = proto.Field(
        proto.ENUM,
        number=4,
        enum=AttestationFormat,
    )
    content: bytes = proto.Field(
        proto.BYTES,
        number=5,
    )
    cert_chains: CertificateChains = proto.Field(
        proto.MESSAGE,
        number=6,
        message=CertificateChains,
    )


class CryptoKeyVersion(proto.Message):
    r"""A [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
    represents an individual cryptographic key, and the associated key
    material.

    An
    [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
    version can be used for cryptographic operations.

    For security reasons, the raw cryptographic key material represented
    by a [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] can
    never be viewed or exported. It can only be used to encrypt,
    decrypt, or sign data when an authorized user or application invokes
    Cloud KMS.

    Attributes:
        name (str):
            Output only. The resource name for this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] in
            the format
            ``projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*``.
        state (google.cloud.kms_v1.types.CryptoKeyVersion.CryptoKeyVersionState):
            The current state of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].
        protection_level (google.cloud.kms_v1.types.ProtectionLevel):
            Output only. The
            [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
            describing how crypto operations are performed with this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].
        algorithm (google.cloud.kms_v1.types.CryptoKeyVersion.CryptoKeyVersionAlgorithm):
            Output only. The
            [CryptoKeyVersionAlgorithm][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm]
            that this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            supports.
        attestation (google.cloud.kms_v1.types.KeyOperationAttestation):
            Output only. Statement that was generated and signed by the
            HSM at key creation time. Use this statement to verify
            attributes of the key as stored on the HSM, independently of
            Google. Only provided for key versions with
            [protection_level][google.cloud.kms.v1.CryptoKeyVersion.protection_level]
            [HSM][google.cloud.kms.v1.ProtectionLevel.HSM].
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] was
            created.
        generate_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]'s
            key material was generated.
        destroy_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]'s
            key material is scheduled for destruction. Only present if
            [state][google.cloud.kms.v1.CryptoKeyVersion.state] is
            [DESTROY_SCHEDULED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DESTROY_SCHEDULED].
        destroy_event_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this CryptoKeyVersion's key material
            was destroyed. Only present if
            [state][google.cloud.kms.v1.CryptoKeyVersion.state] is
            [DESTROYED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DESTROYED].
        import_job (str):
            Output only. The name of the
            [ImportJob][google.cloud.kms.v1.ImportJob] used in the most
            recent import of this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].
            Only present if the underlying key material was imported.
        import_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]'s
            key material was most recently imported.
        import_failure_reason (str):
            Output only. The root cause of the most recent import
            failure. Only present if
            [state][google.cloud.kms.v1.CryptoKeyVersion.state] is
            [IMPORT_FAILED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.IMPORT_FAILED].
        generation_failure_reason (str):
            Output only. The root cause of the most recent generation
            failure. Only present if
            [state][google.cloud.kms.v1.CryptoKeyVersion.state] is
            [GENERATION_FAILED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.GENERATION_FAILED].
        external_destruction_failure_reason (str):
            Output only. The root cause of the most recent external
            destruction failure. Only present if
            [state][google.cloud.kms.v1.CryptoKeyVersion.state] is
            [EXTERNAL_DESTRUCTION_FAILED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.EXTERNAL_DESTRUCTION_FAILED].
        external_protection_level_options (google.cloud.kms_v1.types.ExternalProtectionLevelOptions):
            ExternalProtectionLevelOptions stores a group of additional
            fields for configuring a
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            that are specific to the
            [EXTERNAL][google.cloud.kms.v1.ProtectionLevel.EXTERNAL]
            protection level and
            [EXTERNAL_VPC][google.cloud.kms.v1.ProtectionLevel.EXTERNAL_VPC]
            protection levels.
        reimport_eligible (bool):
            Output only. Whether or not this key version is eligible for
            reimport, by being specified as a target in
            [ImportCryptoKeyVersionRequest.crypto_key_version][google.cloud.kms.v1.ImportCryptoKeyVersionRequest.crypto_key_version].
    """

    class CryptoKeyVersionAlgorithm(proto.Enum):
        r"""The algorithm of the
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion], indicating
        what parameters must be used for each cryptographic operation.

        The
        [GOOGLE_SYMMETRIC_ENCRYPTION][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION]
        algorithm is usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [ENCRYPT_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT].

        Algorithms beginning with ``RSA_SIGN_`` are usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [ASYMMETRIC_SIGN][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN].

        The fields in the name after ``RSA_SIGN_`` correspond to the
        following parameters: padding algorithm, modulus bit length, and
        digest algorithm.

        For PSS, the salt length used is equal to the length of digest
        algorithm. For example,
        [RSA_SIGN_PSS_2048_SHA256][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PSS_2048_SHA256]
        will use PSS with a salt length of 256 bits or 32 bytes.

        Algorithms beginning with ``RSA_DECRYPT_`` are usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [ASYMMETRIC_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT].

        The fields in the name after ``RSA_DECRYPT_`` correspond to the
        following parameters: padding algorithm, modulus bit length, and
        digest algorithm.

        Algorithms beginning with ``EC_SIGN_`` are usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [ASYMMETRIC_SIGN][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN].

        The fields in the name after ``EC_SIGN_`` correspond to the
        following parameters: elliptic curve, digest algorithm.

        Algorithms beginning with ``HMAC_`` are usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [MAC][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.MAC].

        The suffix following ``HMAC_`` corresponds to the hash algorithm
        being used (eg. SHA256).

        For more information, see [Key purposes and algorithms]
        (https://cloud.google.com/kms/docs/algorithms).

        Values:
            CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED (0):
                Not specified.
            GOOGLE_SYMMETRIC_ENCRYPTION (1):
                Creates symmetric encryption keys.
            AES_128_GCM (41):
                AES-GCM (Galois Counter Mode) using 128-bit
                keys.
            AES_256_GCM (19):
                AES-GCM (Galois Counter Mode) using 256-bit
                keys.
            AES_128_CBC (42):
                AES-CBC (Cipher Block Chaining Mode) using
                128-bit keys.
            AES_256_CBC (43):
                AES-CBC (Cipher Block Chaining Mode) using
                256-bit keys.
            AES_128_CTR (44):
                AES-CTR (Counter Mode) using 128-bit keys.
            AES_256_CTR (45):
                AES-CTR (Counter Mode) using 256-bit keys.
            RSA_SIGN_PSS_2048_SHA256 (2):
                RSASSA-PSS 2048 bit key with a SHA256 digest.
            RSA_SIGN_PSS_3072_SHA256 (3):
                RSASSA-PSS 3072 bit key with a SHA256 digest.
            RSA_SIGN_PSS_4096_SHA256 (4):
                RSASSA-PSS 4096 bit key with a SHA256 digest.
            RSA_SIGN_PSS_4096_SHA512 (15):
                RSASSA-PSS 4096 bit key with a SHA512 digest.
            RSA_SIGN_PKCS1_2048_SHA256 (5):
                RSASSA-PKCS1-v1_5 with a 2048 bit key and a SHA256 digest.
            RSA_SIGN_PKCS1_3072_SHA256 (6):
                RSASSA-PKCS1-v1_5 with a 3072 bit key and a SHA256 digest.
            RSA_SIGN_PKCS1_4096_SHA256 (7):
                RSASSA-PKCS1-v1_5 with a 4096 bit key and a SHA256 digest.
            RSA_SIGN_PKCS1_4096_SHA512 (16):
                RSASSA-PKCS1-v1_5 with a 4096 bit key and a SHA512 digest.
            RSA_SIGN_RAW_PKCS1_2048 (28):
                RSASSA-PKCS1-v1_5 signing without encoding, with a 2048 bit
                key.
            RSA_SIGN_RAW_PKCS1_3072 (29):
                RSASSA-PKCS1-v1_5 signing without encoding, with a 3072 bit
                key.
            RSA_SIGN_RAW_PKCS1_4096 (30):
                RSASSA-PKCS1-v1_5 signing without encoding, with a 4096 bit
                key.
            RSA_DECRYPT_OAEP_2048_SHA256 (8):
                RSAES-OAEP 2048 bit key with a SHA256 digest.
            RSA_DECRYPT_OAEP_3072_SHA256 (9):
                RSAES-OAEP 3072 bit key with a SHA256 digest.
            RSA_DECRYPT_OAEP_4096_SHA256 (10):
                RSAES-OAEP 4096 bit key with a SHA256 digest.
            RSA_DECRYPT_OAEP_4096_SHA512 (17):
                RSAES-OAEP 4096 bit key with a SHA512 digest.
            RSA_DECRYPT_OAEP_2048_SHA1 (37):
                RSAES-OAEP 2048 bit key with a SHA1 digest.
            RSA_DECRYPT_OAEP_3072_SHA1 (38):
                RSAES-OAEP 3072 bit key with a SHA1 digest.
            RSA_DECRYPT_OAEP_4096_SHA1 (39):
                RSAES-OAEP 4096 bit key with a SHA1 digest.
            EC_SIGN_P256_SHA256 (12):
                ECDSA on the NIST P-256 curve with a SHA256 digest. Other
                hash functions can also be used:
                https://cloud.google.com/kms/docs/create-validate-signatures#ecdsa_support_for_other_hash_algorithms
            EC_SIGN_P384_SHA384 (13):
                ECDSA on the NIST P-384 curve with a SHA384 digest. Other
                hash functions can also be used:
                https://cloud.google.com/kms/docs/create-validate-signatures#ecdsa_support_for_other_hash_algorithms
            EC_SIGN_SECP256K1_SHA256 (31):
                ECDSA on the non-NIST secp256k1 curve. This curve is only
                supported for HSM protection level. Other hash functions can
                also be used:
                https://cloud.google.com/kms/docs/create-validate-signatures#ecdsa_support_for_other_hash_algorithms
            EC_SIGN_ED25519 (40):
                EdDSA on the Curve25519 in pure mode (taking
                data as input).
            HMAC_SHA256 (32):
                HMAC-SHA256 signing with a 256 bit key.
            HMAC_SHA1 (33):
                HMAC-SHA1 signing with a 160 bit key.
            HMAC_SHA384 (34):
                HMAC-SHA384 signing with a 384 bit key.
            HMAC_SHA512 (35):
                HMAC-SHA512 signing with a 512 bit key.
            HMAC_SHA224 (36):
                HMAC-SHA224 signing with a 224 bit key.
            EXTERNAL_SYMMETRIC_ENCRYPTION (18):
                Algorithm representing symmetric encryption
                by an external key manager.
        """
        CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED = 0
        GOOGLE_SYMMETRIC_ENCRYPTION = 1
        AES_128_GCM = 41
        AES_256_GCM = 19
        AES_128_CBC = 42
        AES_256_CBC = 43
        AES_128_CTR = 44
        AES_256_CTR = 45
        RSA_SIGN_PSS_2048_SHA256 = 2
        RSA_SIGN_PSS_3072_SHA256 = 3
        RSA_SIGN_PSS_4096_SHA256 = 4
        RSA_SIGN_PSS_4096_SHA512 = 15
        RSA_SIGN_PKCS1_2048_SHA256 = 5
        RSA_SIGN_PKCS1_3072_SHA256 = 6
        RSA_SIGN_PKCS1_4096_SHA256 = 7
        RSA_SIGN_PKCS1_4096_SHA512 = 16
        RSA_SIGN_RAW_PKCS1_2048 = 28
        RSA_SIGN_RAW_PKCS1_3072 = 29
        RSA_SIGN_RAW_PKCS1_4096 = 30
        RSA_DECRYPT_OAEP_2048_SHA256 = 8
        RSA_DECRYPT_OAEP_3072_SHA256 = 9
        RSA_DECRYPT_OAEP_4096_SHA256 = 10
        RSA_DECRYPT_OAEP_4096_SHA512 = 17
        RSA_DECRYPT_OAEP_2048_SHA1 = 37
        RSA_DECRYPT_OAEP_3072_SHA1 = 38
        RSA_DECRYPT_OAEP_4096_SHA1 = 39
        EC_SIGN_P256_SHA256 = 12
        EC_SIGN_P384_SHA384 = 13
        EC_SIGN_SECP256K1_SHA256 = 31
        EC_SIGN_ED25519 = 40
        HMAC_SHA256 = 32
        HMAC_SHA1 = 33
        HMAC_SHA384 = 34
        HMAC_SHA512 = 35
        HMAC_SHA224 = 36
        EXTERNAL_SYMMETRIC_ENCRYPTION = 18

    class CryptoKeyVersionState(proto.Enum):
        r"""The state of a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion], indicating
        if it can be used.

        Values:
            CRYPTO_KEY_VERSION_STATE_UNSPECIFIED (0):
                Not specified.
            PENDING_GENERATION (5):
                This version is still being generated. It may not be used,
                enabled, disabled, or destroyed yet. Cloud KMS will
                automatically mark this version
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                as soon as the version is ready.
            ENABLED (1):
                This version may be used for cryptographic
                operations.
            DISABLED (2):
                This version may not be used, but the key material is still
                available, and the version can be placed back into the
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                state.
            DESTROYED (3):
                This version is destroyed, and the key material is no longer
                stored. This version may only become
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                again if this version is
                [reimport_eligible][google.cloud.kms.v1.CryptoKeyVersion.reimport_eligible]
                and the original key material is reimported with a call to
                [KeyManagementService.ImportCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion].
            DESTROY_SCHEDULED (4):
                This version is scheduled for destruction, and will be
                destroyed soon. Call
                [RestoreCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.RestoreCryptoKeyVersion]
                to put it back into the
                [DISABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.DISABLED]
                state.
            PENDING_IMPORT (6):
                This version is still being imported. It may not be used,
                enabled, disabled, or destroyed yet. Cloud KMS will
                automatically mark this version
                [ENABLED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.ENABLED]
                as soon as the version is ready.
            IMPORT_FAILED (7):
                This version was not imported successfully. It may not be
                used, enabled, disabled, or destroyed. The submitted key
                material has been discarded. Additional details can be found
                in
                [CryptoKeyVersion.import_failure_reason][google.cloud.kms.v1.CryptoKeyVersion.import_failure_reason].
            GENERATION_FAILED (8):
                This version was not generated successfully. It may not be
                used, enabled, disabled, or destroyed. Additional details
                can be found in
                [CryptoKeyVersion.generation_failure_reason][google.cloud.kms.v1.CryptoKeyVersion.generation_failure_reason].
            PENDING_EXTERNAL_DESTRUCTION (9):
                This version was destroyed, and it may not be
                used or enabled again. Cloud KMS is waiting for
                the corresponding key material residing in an
                external key manager to be destroyed.
            EXTERNAL_DESTRUCTION_FAILED (10):
                This version was destroyed, and it may not be used or
                enabled again. However, Cloud KMS could not confirm that the
                corresponding key material residing in an external key
                manager was destroyed. Additional details can be found in
                [CryptoKeyVersion.external_destruction_failure_reason][google.cloud.kms.v1.CryptoKeyVersion.external_destruction_failure_reason].
        """
        CRYPTO_KEY_VERSION_STATE_UNSPECIFIED = 0
        PENDING_GENERATION = 5
        ENABLED = 1
        DISABLED = 2
        DESTROYED = 3
        DESTROY_SCHEDULED = 4
        PENDING_IMPORT = 6
        IMPORT_FAILED = 7
        GENERATION_FAILED = 8
        PENDING_EXTERNAL_DESTRUCTION = 9
        EXTERNAL_DESTRUCTION_FAILED = 10

    class CryptoKeyVersionView(proto.Enum):
        r"""A view for
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]s. Controls
        the level of detail returned for
        [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion] in
        [KeyManagementService.ListCryptoKeyVersions][google.cloud.kms.v1.KeyManagementService.ListCryptoKeyVersions]
        and
        [KeyManagementService.ListCryptoKeys][google.cloud.kms.v1.KeyManagementService.ListCryptoKeys].

        Values:
            CRYPTO_KEY_VERSION_VIEW_UNSPECIFIED (0):
                Default view for each
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].
                Does not include the
                [attestation][google.cloud.kms.v1.CryptoKeyVersion.attestation]
                field.
            FULL (1):
                Provides all fields in each
                [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion],
                including the
                [attestation][google.cloud.kms.v1.CryptoKeyVersion.attestation].
        """
        CRYPTO_KEY_VERSION_VIEW_UNSPECIFIED = 0
        FULL = 1

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: CryptoKeyVersionState = proto.Field(
        proto.ENUM,
        number=3,
        enum=CryptoKeyVersionState,
    )
    protection_level: "ProtectionLevel" = proto.Field(
        proto.ENUM,
        number=7,
        enum="ProtectionLevel",
    )
    algorithm: CryptoKeyVersionAlgorithm = proto.Field(
        proto.ENUM,
        number=10,
        enum=CryptoKeyVersionAlgorithm,
    )
    attestation: "KeyOperationAttestation" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="KeyOperationAttestation",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    generate_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    destroy_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    destroy_event_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    import_job: str = proto.Field(
        proto.STRING,
        number=14,
    )
    import_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=15,
        message=timestamp_pb2.Timestamp,
    )
    import_failure_reason: str = proto.Field(
        proto.STRING,
        number=16,
    )
    generation_failure_reason: str = proto.Field(
        proto.STRING,
        number=19,
    )
    external_destruction_failure_reason: str = proto.Field(
        proto.STRING,
        number=20,
    )
    external_protection_level_options: "ExternalProtectionLevelOptions" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="ExternalProtectionLevelOptions",
    )
    reimport_eligible: bool = proto.Field(
        proto.BOOL,
        number=18,
    )


class PublicKey(proto.Message):
    r"""The public keys for a given
    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]. Obtained
    via
    [GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey].

    Attributes:
        pem (str):
            The public key, encoded in PEM format. For more information,
            see the `RFC 7468 <https://tools.ietf.org/html/rfc7468>`__
            sections for `General
            Considerations <https://tools.ietf.org/html/rfc7468#section-2>`__
            and [Textual Encoding of Subject Public Key Info]
            (https://tools.ietf.org/html/rfc7468#section-13).
        algorithm (google.cloud.kms_v1.types.CryptoKeyVersion.CryptoKeyVersionAlgorithm):
            The
            [Algorithm][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm]
            associated with this key.
        pem_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Integrity verification field. A CRC32C checksum of the
            returned [PublicKey.pem][google.cloud.kms.v1.PublicKey.pem].
            An integrity check of
            [PublicKey.pem][google.cloud.kms.v1.PublicKey.pem] can be
            performed by computing the CRC32C checksum of
            [PublicKey.pem][google.cloud.kms.v1.PublicKey.pem] and
            comparing your results to this field. Discard the response
            in case of non-matching checksum values, and perform a
            limited number of retries. A persistent mismatch may
            indicate an issue in your computation of the CRC32C
            checksum. Note: This field is defined as int64 for reasons
            of compatibility across different languages. However, it is
            a non-negative integer, which will never exceed 2^32-1, and
            can be safely downconverted to uint32 in languages that
            support this type.

            NOTE: This field is in Beta.
        name (str):
            The [name][google.cloud.kms.v1.CryptoKeyVersion.name] of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            public key. Provided here for verification.

            NOTE: This field is in Beta.
        protection_level (google.cloud.kms_v1.types.ProtectionLevel):
            The [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
            of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            public key.
    """

    pem: str = proto.Field(
        proto.STRING,
        number=1,
    )
    algorithm: "CryptoKeyVersion.CryptoKeyVersionAlgorithm" = proto.Field(
        proto.ENUM,
        number=2,
        enum="CryptoKeyVersion.CryptoKeyVersionAlgorithm",
    )
    pem_crc32c: wrappers_pb2.Int64Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int64Value,
    )
    name: str = proto.Field(
        proto.STRING,
        number=4,
    )
    protection_level: "ProtectionLevel" = proto.Field(
        proto.ENUM,
        number=5,
        enum="ProtectionLevel",
    )


class ImportJob(proto.Message):
    r"""An [ImportJob][google.cloud.kms.v1.ImportJob] can be used to create
    [CryptoKeys][google.cloud.kms.v1.CryptoKey] and
    [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion] using
    pre-existing key material, generated outside of Cloud KMS.

    When an [ImportJob][google.cloud.kms.v1.ImportJob] is created, Cloud
    KMS will generate a "wrapping key", which is a public/private key
    pair. You use the wrapping key to encrypt (also known as wrap) the
    pre-existing key material to protect it during the import process.
    The nature of the wrapping key depends on the choice of
    [import_method][google.cloud.kms.v1.ImportJob.import_method]. When
    the wrapping key generation is complete, the
    [state][google.cloud.kms.v1.ImportJob.state] will be set to
    [ACTIVE][google.cloud.kms.v1.ImportJob.ImportJobState.ACTIVE] and
    the [public_key][google.cloud.kms.v1.ImportJob.public_key] can be
    fetched. The fetched public key can then be used to wrap your
    pre-existing key material.

    Once the key material is wrapped, it can be imported into a new
    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] in an
    existing [CryptoKey][google.cloud.kms.v1.CryptoKey] by calling
    [ImportCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion].
    Multiple [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
    can be imported with a single
    [ImportJob][google.cloud.kms.v1.ImportJob]. Cloud KMS uses the
    private key portion of the wrapping key to unwrap the key material.
    Only Cloud KMS has access to the private key.

    An [ImportJob][google.cloud.kms.v1.ImportJob] expires 3 days after
    it is created. Once expired, Cloud KMS will no longer be able to
    import or unwrap any key material that was wrapped with the
    [ImportJob][google.cloud.kms.v1.ImportJob]'s public key.

    For more information, see `Importing a
    key <https://cloud.google.com/kms/docs/importing-a-key>`__.

    Attributes:
        name (str):
            Output only. The resource name for this
            [ImportJob][google.cloud.kms.v1.ImportJob] in the format
            ``projects/*/locations/*/keyRings/*/importJobs/*``.
        import_method (google.cloud.kms_v1.types.ImportJob.ImportMethod):
            Required. Immutable. The wrapping method to
            be used for incoming key material.
        protection_level (google.cloud.kms_v1.types.ProtectionLevel):
            Required. Immutable. The protection level of the
            [ImportJob][google.cloud.kms.v1.ImportJob]. This must match
            the
            [protection_level][google.cloud.kms.v1.CryptoKeyVersionTemplate.protection_level]
            of the
            [version_template][google.cloud.kms.v1.CryptoKey.version_template]
            on the [CryptoKey][google.cloud.kms.v1.CryptoKey] you
            attempt to import into.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [ImportJob][google.cloud.kms.v1.ImportJob] was created.
        generate_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this
            [ImportJob][google.cloud.kms.v1.ImportJob]'s key material
            was generated.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [ImportJob][google.cloud.kms.v1.ImportJob] is scheduled for
            expiration and can no longer be used to import key material.
        expire_event_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this
            [ImportJob][google.cloud.kms.v1.ImportJob] expired. Only
            present if [state][google.cloud.kms.v1.ImportJob.state] is
            [EXPIRED][google.cloud.kms.v1.ImportJob.ImportJobState.EXPIRED].
        state (google.cloud.kms_v1.types.ImportJob.ImportJobState):
            Output only. The current state of the
            [ImportJob][google.cloud.kms.v1.ImportJob], indicating if it
            can be used.
        public_key (google.cloud.kms_v1.types.ImportJob.WrappingPublicKey):
            Output only. The public key with which to wrap key material
            prior to import. Only returned if
            [state][google.cloud.kms.v1.ImportJob.state] is
            [ACTIVE][google.cloud.kms.v1.ImportJob.ImportJobState.ACTIVE].
        attestation (google.cloud.kms_v1.types.KeyOperationAttestation):
            Output only. Statement that was generated and signed by the
            key creator (for example, an HSM) at key creation time. Use
            this statement to verify attributes of the key as stored on
            the HSM, independently of Google. Only present if the chosen
            [ImportMethod][google.cloud.kms.v1.ImportJob.ImportMethod]
            is one with a protection level of
            [HSM][google.cloud.kms.v1.ProtectionLevel.HSM].
    """

    class ImportMethod(proto.Enum):
        r"""[ImportMethod][google.cloud.kms.v1.ImportJob.ImportMethod] describes
        the key wrapping method chosen for this
        [ImportJob][google.cloud.kms.v1.ImportJob].

        Values:
            IMPORT_METHOD_UNSPECIFIED (0):
                Not specified.
            RSA_OAEP_3072_SHA1_AES_256 (1):
                This ImportMethod represents the CKM_RSA_AES_KEY_WRAP key
                wrapping scheme defined in the PKCS #11 standard. In
                summary, this involves wrapping the raw key with an
                ephemeral AES key, and wrapping the ephemeral AES key with a
                3072 bit RSA key. For more details, see `RSA AES key wrap
                mechanism <http://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/cos01/pkcs11-curr-v2.40-cos01.html#_Toc408226908>`__.
            RSA_OAEP_4096_SHA1_AES_256 (2):
                This ImportMethod represents the CKM_RSA_AES_KEY_WRAP key
                wrapping scheme defined in the PKCS #11 standard. In
                summary, this involves wrapping the raw key with an
                ephemeral AES key, and wrapping the ephemeral AES key with a
                4096 bit RSA key. For more details, see `RSA AES key wrap
                mechanism <http://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/cos01/pkcs11-curr-v2.40-cos01.html#_Toc408226908>`__.
            RSA_OAEP_3072_SHA256_AES_256 (3):
                This ImportMethod represents the CKM_RSA_AES_KEY_WRAP key
                wrapping scheme defined in the PKCS #11 standard. In
                summary, this involves wrapping the raw key with an
                ephemeral AES key, and wrapping the ephemeral AES key with a
                3072 bit RSA key. For more details, see `RSA AES key wrap
                mechanism <http://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/cos01/pkcs11-curr-v2.40-cos01.html#_Toc408226908>`__.
            RSA_OAEP_4096_SHA256_AES_256 (4):
                This ImportMethod represents the CKM_RSA_AES_KEY_WRAP key
                wrapping scheme defined in the PKCS #11 standard. In
                summary, this involves wrapping the raw key with an
                ephemeral AES key, and wrapping the ephemeral AES key with a
                4096 bit RSA key. For more details, see `RSA AES key wrap
                mechanism <http://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/cos01/pkcs11-curr-v2.40-cos01.html#_Toc408226908>`__.
            RSA_OAEP_3072_SHA256 (5):
                This ImportMethod represents RSAES-OAEP with
                a 3072 bit RSA key. The key material to be
                imported is wrapped directly with the RSA key.
                Due to technical limitations of RSA wrapping,
                this method cannot be used to wrap RSA keys for
                import.
            RSA_OAEP_4096_SHA256 (6):
                This ImportMethod represents RSAES-OAEP with
                a 4096 bit RSA key. The key material to be
                imported is wrapped directly with the RSA key.
                Due to technical limitations of RSA wrapping,
                this method cannot be used to wrap RSA keys for
                import.
        """
        IMPORT_METHOD_UNSPECIFIED = 0
        RSA_OAEP_3072_SHA1_AES_256 = 1
        RSA_OAEP_4096_SHA1_AES_256 = 2
        RSA_OAEP_3072_SHA256_AES_256 = 3
        RSA_OAEP_4096_SHA256_AES_256 = 4
        RSA_OAEP_3072_SHA256 = 5
        RSA_OAEP_4096_SHA256 = 6

    class ImportJobState(proto.Enum):
        r"""The state of the [ImportJob][google.cloud.kms.v1.ImportJob],
        indicating if it can be used.

        Values:
            IMPORT_JOB_STATE_UNSPECIFIED (0):
                Not specified.
            PENDING_GENERATION (1):
                The wrapping key for this job is still being generated. It
                may not be used. Cloud KMS will automatically mark this job
                as
                [ACTIVE][google.cloud.kms.v1.ImportJob.ImportJobState.ACTIVE]
                as soon as the wrapping key is generated.
            ACTIVE (2):
                This job may be used in
                [CreateCryptoKey][google.cloud.kms.v1.KeyManagementService.CreateCryptoKey]
                and
                [CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion]
                requests.
            EXPIRED (3):
                This job can no longer be used and may not
                leave this state once entered.
        """
        IMPORT_JOB_STATE_UNSPECIFIED = 0
        PENDING_GENERATION = 1
        ACTIVE = 2
        EXPIRED = 3

    class WrappingPublicKey(proto.Message):
        r"""The public key component of the wrapping key. For details of the
        type of key this public key corresponds to, see the
        [ImportMethod][google.cloud.kms.v1.ImportJob.ImportMethod].

        Attributes:
            pem (str):
                The public key, encoded in PEM format. For more information,
                see the `RFC 7468 <https://tools.ietf.org/html/rfc7468>`__
                sections for `General
                Considerations <https://tools.ietf.org/html/rfc7468#section-2>`__
                and [Textual Encoding of Subject Public Key Info]
                (https://tools.ietf.org/html/rfc7468#section-13).
        """

        pem: str = proto.Field(
            proto.STRING,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    import_method: ImportMethod = proto.Field(
        proto.ENUM,
        number=2,
        enum=ImportMethod,
    )
    protection_level: "ProtectionLevel" = proto.Field(
        proto.ENUM,
        number=9,
        enum="ProtectionLevel",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    generate_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    expire_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    expire_event_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )
    state: ImportJobState = proto.Field(
        proto.ENUM,
        number=6,
        enum=ImportJobState,
    )
    public_key: WrappingPublicKey = proto.Field(
        proto.MESSAGE,
        number=7,
        message=WrappingPublicKey,
    )
    attestation: "KeyOperationAttestation" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="KeyOperationAttestation",
    )


class ExternalProtectionLevelOptions(proto.Message):
    r"""ExternalProtectionLevelOptions stores a group of additional fields
    for configuring a
    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] that are
    specific to the
    [EXTERNAL][google.cloud.kms.v1.ProtectionLevel.EXTERNAL] protection
    level and
    [EXTERNAL_VPC][google.cloud.kms.v1.ProtectionLevel.EXTERNAL_VPC]
    protection levels.

    Attributes:
        external_key_uri (str):
            The URI for an external resource that this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            represents.
        ekm_connection_key_path (str):
            The path to the external key material on the EKM when using
            [EkmConnection][google.cloud.kms.v1.EkmConnection] e.g.,
            "v0/my/key". Set this field instead of external_key_uri when
            using an [EkmConnection][google.cloud.kms.v1.EkmConnection].
    """

    external_key_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ekm_connection_key_path: str = proto.Field(
        proto.STRING,
        number=2,
    )


class KeyAccessJustificationsPolicy(proto.Message):
    r"""A
    [KeyAccessJustificationsPolicy][google.cloud.kms.v1.KeyAccessJustificationsPolicy]
    specifies zero or more allowed
    [AccessReason][google.cloud.kms.v1.AccessReason] values for encrypt,
    decrypt, and sign operations on a
    [CryptoKey][google.cloud.kms.v1.CryptoKey].

    Attributes:
        allowed_access_reasons (MutableSequence[google.cloud.kms_v1.types.AccessReason]):
            The list of allowed reasons for access to a
            [CryptoKey][google.cloud.kms.v1.CryptoKey]. Zero allowed
            access reasons means all encrypt, decrypt, and sign
            operations for the
            [CryptoKey][google.cloud.kms.v1.CryptoKey] associated with
            this policy will fail.
    """

    allowed_access_reasons: MutableSequence["AccessReason"] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum="AccessReason",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
