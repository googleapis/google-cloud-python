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
    package="google.cloud.kms.v1",
    manifest={
        "ProtectionLevel",
        "KeyRing",
        "CryptoKey",
        "CryptoKeyVersionTemplate",
        "KeyOperationAttestation",
        "CryptoKeyVersion",
        "PublicKey",
        "ImportJob",
        "ExternalProtectionLevelOptions",
    },
)


class ProtectionLevel(proto.Enum):
    r"""[ProtectionLevel][google.cloud.kms.v1.ProtectionLevel] specifies how
    cryptographic operations are performed. For more information, see
    [Protection levels]
    (https://cloud.google.com/kms/docs/algorithms#protection_levels).
    """
    PROTECTION_LEVEL_UNSPECIFIED = 0
    SOFTWARE = 1
    HSM = 2
    EXTERNAL = 3


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

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)


class CryptoKey(proto.Message):
    r"""A [CryptoKey][google.cloud.kms.v1.CryptoKey] represents a logical
    key that can be used for cryptographic operations.

    A [CryptoKey][google.cloud.kms.v1.CryptoKey] is made up of zero or
    more [versions][google.cloud.kms.v1.CryptoKeyVersion], which
    represent the actual key material used in cryptographic operations.

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
        version_template (google.cloud.kms_v1.types.CryptoKeyVersionTemplate):
            A template describing settings for new
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            instances. The properties of new
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            instances created by either
            [CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion]
            or auto-rotation are controlled by this template.
        labels (Sequence[google.cloud.kms_v1.types.CryptoKey.LabelsEntry]):
            Labels with user-defined metadata. For more information, see
            `Labeling
            Keys <https://cloud.google.com/kms/docs/labeling-keys>`__.
    """

    class CryptoKeyPurpose(proto.Enum):
        r"""[CryptoKeyPurpose][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose]
        describes the cryptographic capabilities of a
        [CryptoKey][google.cloud.kms.v1.CryptoKey]. A given key can only be
        used for the operations allowed by its purpose. For more
        information, see `Key
        purposes <https://cloud.google.com/kms/docs/algorithms#key_purposes>`__.
        """
        CRYPTO_KEY_PURPOSE_UNSPECIFIED = 0
        ENCRYPT_DECRYPT = 1
        ASYMMETRIC_SIGN = 5
        ASYMMETRIC_DECRYPT = 6

    name = proto.Field(proto.STRING, number=1,)
    primary = proto.Field(proto.MESSAGE, number=2, message="CryptoKeyVersion",)
    purpose = proto.Field(proto.ENUM, number=3, enum=CryptoKeyPurpose,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    next_rotation_time = proto.Field(
        proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,
    )
    rotation_period = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="rotation_schedule",
        message=duration_pb2.Duration,
    )
    version_template = proto.Field(
        proto.MESSAGE, number=11, message="CryptoKeyVersionTemplate",
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=10,)


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

    protection_level = proto.Field(proto.ENUM, number=1, enum="ProtectionLevel",)
    algorithm = proto.Field(
        proto.ENUM, number=3, enum="CryptoKeyVersion.CryptoKeyVersionAlgorithm",
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
    """

    class AttestationFormat(proto.Enum):
        r"""Attestation formats provided by the HSM."""
        ATTESTATION_FORMAT_UNSPECIFIED = 0
        CAVIUM_V1_COMPRESSED = 3
        CAVIUM_V2_COMPRESSED = 4

    format = proto.Field(proto.ENUM, number=4, enum=AttestationFormat,)
    content = proto.Field(proto.BYTES, number=5,)


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
            [ImportJob][google.cloud.kms.v1.ImportJob] used to import
            this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion].
            Only present if the underlying key material was imported.
        import_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]'s
            key material was imported.
        import_failure_reason (str):
            Output only. The root cause of an import failure. Only
            present if
            [state][google.cloud.kms.v1.CryptoKeyVersion.state] is
            [IMPORT_FAILED][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionState.IMPORT_FAILED].
        external_protection_level_options (google.cloud.kms_v1.types.ExternalProtectionLevelOptions):
            ExternalProtectionLevelOptions stores a group of additional
            fields for configuring a
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            that are specific to the
            [EXTERNAL][google.cloud.kms.v1.ProtectionLevel.EXTERNAL]
            protection level.
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

        Algorithms beginning with "RSA_SIGN\_" are usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [ASYMMETRIC_SIGN][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN].

        The fields in the name after "RSA_SIGN\_" correspond to the following
        parameters: padding algorithm, modulus bit length, and digest
        algorithm.

        For PSS, the salt length used is equal to the length of digest
        algorithm. For example,
        [RSA_SIGN_PSS_2048_SHA256][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm.RSA_SIGN_PSS_2048_SHA256]
        will use PSS with a salt length of 256 bits or 32 bytes.

        Algorithms beginning with "RSA_DECRYPT\_" are usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [ASYMMETRIC_DECRYPT][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_DECRYPT].

        The fields in the name after "RSA_DECRYPT\_" correspond to the
        following parameters: padding algorithm, modulus bit length, and
        digest algorithm.

        Algorithms beginning with "EC_SIGN\_" are usable with
        [CryptoKey.purpose][google.cloud.kms.v1.CryptoKey.purpose]
        [ASYMMETRIC_SIGN][google.cloud.kms.v1.CryptoKey.CryptoKeyPurpose.ASYMMETRIC_SIGN].

        The fields in the name after "EC_SIGN\_" correspond to the following
        parameters: elliptic curve, digest algorithm.

        For more information, see [Key purposes and algorithms]
        (https://cloud.google.com/kms/docs/algorithms).
        """
        CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED = 0
        GOOGLE_SYMMETRIC_ENCRYPTION = 1
        RSA_SIGN_PSS_2048_SHA256 = 2
        RSA_SIGN_PSS_3072_SHA256 = 3
        RSA_SIGN_PSS_4096_SHA256 = 4
        RSA_SIGN_PSS_4096_SHA512 = 15
        RSA_SIGN_PKCS1_2048_SHA256 = 5
        RSA_SIGN_PKCS1_3072_SHA256 = 6
        RSA_SIGN_PKCS1_4096_SHA256 = 7
        RSA_SIGN_PKCS1_4096_SHA512 = 16
        RSA_DECRYPT_OAEP_2048_SHA256 = 8
        RSA_DECRYPT_OAEP_3072_SHA256 = 9
        RSA_DECRYPT_OAEP_4096_SHA256 = 10
        RSA_DECRYPT_OAEP_4096_SHA512 = 17
        EC_SIGN_P256_SHA256 = 12
        EC_SIGN_P384_SHA384 = 13
        EC_SIGN_SECP256K1_SHA256 = 31
        EXTERNAL_SYMMETRIC_ENCRYPTION = 18

    class CryptoKeyVersionState(proto.Enum):
        r"""The state of a
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion], indicating
        if it can be used.
        """
        CRYPTO_KEY_VERSION_STATE_UNSPECIFIED = 0
        PENDING_GENERATION = 5
        ENABLED = 1
        DISABLED = 2
        DESTROYED = 3
        DESTROY_SCHEDULED = 4
        PENDING_IMPORT = 6
        IMPORT_FAILED = 7

    class CryptoKeyVersionView(proto.Enum):
        r"""A view for
        [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]s. Controls
        the level of detail returned for
        [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion] in
        [KeyManagementService.ListCryptoKeyVersions][google.cloud.kms.v1.KeyManagementService.ListCryptoKeyVersions]
        and
        [KeyManagementService.ListCryptoKeys][google.cloud.kms.v1.KeyManagementService.ListCryptoKeys].
        """
        CRYPTO_KEY_VERSION_VIEW_UNSPECIFIED = 0
        FULL = 1

    name = proto.Field(proto.STRING, number=1,)
    state = proto.Field(proto.ENUM, number=3, enum=CryptoKeyVersionState,)
    protection_level = proto.Field(proto.ENUM, number=7, enum="ProtectionLevel",)
    algorithm = proto.Field(proto.ENUM, number=10, enum=CryptoKeyVersionAlgorithm,)
    attestation = proto.Field(
        proto.MESSAGE, number=8, message="KeyOperationAttestation",
    )
    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    generate_time = proto.Field(
        proto.MESSAGE, number=11, message=timestamp_pb2.Timestamp,
    )
    destroy_time = proto.Field(
        proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
    )
    destroy_event_time = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )
    import_job = proto.Field(proto.STRING, number=14,)
    import_time = proto.Field(
        proto.MESSAGE, number=15, message=timestamp_pb2.Timestamp,
    )
    import_failure_reason = proto.Field(proto.STRING, number=16,)
    external_protection_level_options = proto.Field(
        proto.MESSAGE, number=17, message="ExternalProtectionLevelOptions",
    )


class PublicKey(proto.Message):
    r"""The public key for a given
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
    """

    pem = proto.Field(proto.STRING, number=1,)
    algorithm = proto.Field(
        proto.ENUM, number=2, enum="CryptoKeyVersion.CryptoKeyVersionAlgorithm",
    )
    pem_crc32c = proto.Field(proto.MESSAGE, number=3, message=wrappers_pb2.Int64Value,)
    name = proto.Field(proto.STRING, number=4,)


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
        """
        IMPORT_METHOD_UNSPECIFIED = 0
        RSA_OAEP_3072_SHA1_AES_256 = 1
        RSA_OAEP_4096_SHA1_AES_256 = 2

    class ImportJobState(proto.Enum):
        r"""The state of the [ImportJob][google.cloud.kms.v1.ImportJob],
        indicating if it can be used.
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

        pem = proto.Field(proto.STRING, number=1,)

    name = proto.Field(proto.STRING, number=1,)
    import_method = proto.Field(proto.ENUM, number=2, enum=ImportMethod,)
    protection_level = proto.Field(proto.ENUM, number=9, enum="ProtectionLevel",)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    generate_time = proto.Field(
        proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,
    )
    expire_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    expire_event_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )
    state = proto.Field(proto.ENUM, number=6, enum=ImportJobState,)
    public_key = proto.Field(proto.MESSAGE, number=7, message=WrappingPublicKey,)
    attestation = proto.Field(
        proto.MESSAGE, number=8, message="KeyOperationAttestation",
    )


class ExternalProtectionLevelOptions(proto.Message):
    r"""ExternalProtectionLevelOptions stores a group of additional fields
    for configuring a
    [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] that are
    specific to the
    [EXTERNAL][google.cloud.kms.v1.ProtectionLevel.EXTERNAL] protection
    level.

    Attributes:
        external_key_uri (str):
            The URI for an external resource that this
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            represents.
    """

    external_key_uri = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
