# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrappers for protocol buffer enum types."""

import enum


class ProtectionLevel(enum.IntEnum):
    """
    ``ProtectionLevel`` specifies how cryptographic operations are
    performed.

    Attributes:
      PROTECTION_LEVEL_UNSPECIFIED (int): Not specified.
      SOFTWARE (int): Crypto operations are performed in software.
      HSM (int): Crypto operations are performed in a Hardware Security Module.
    """

    PROTECTION_LEVEL_UNSPECIFIED = 0
    SOFTWARE = 1
    HSM = 2


class CryptoKey(object):
    class CryptoKeyPurpose(enum.IntEnum):
        """
        ``CryptoKeyPurpose`` describes the cryptographic capabilities of a
        ``CryptoKey``. A given key can only be used for the operations allowed
        by its purpose.

        Attributes:
          CRYPTO_KEY_PURPOSE_UNSPECIFIED (int): Not specified.
          ENCRYPT_DECRYPT (int): ``CryptoKeys`` with this purpose may be used with ``Encrypt`` and
          ``Decrypt``.
          ASYMMETRIC_SIGN (int): ``CryptoKeys`` with this purpose may be used with ``AsymmetricSign`` and
          ``GetPublicKey``.
          ASYMMETRIC_DECRYPT (int): ``CryptoKeys`` with this purpose may be used with ``AsymmetricDecrypt``
          and ``GetPublicKey``.
        """

        CRYPTO_KEY_PURPOSE_UNSPECIFIED = 0
        ENCRYPT_DECRYPT = 1
        ASYMMETRIC_SIGN = 5
        ASYMMETRIC_DECRYPT = 6


class CryptoKeyVersion(object):
    class CryptoKeyVersionAlgorithm(enum.IntEnum):
        """
        The algorithm of the ``CryptoKeyVersion``, indicating what parameters
        must be used for each cryptographic operation.

        The ``GOOGLE_SYMMETRIC_ENCRYPTION`` algorithm is usable with
        ``CryptoKey.purpose`` ``ENCRYPT_DECRYPT``.

        Algorithms beginning with "RSA\_SIGN\_" are usable with
        ``CryptoKey.purpose`` ``ASYMMETRIC_SIGN``.

        The fields in the name after "RSA\_SIGN\_" correspond to the following
        parameters: padding algorithm, modulus bit length, and digest algorithm.

        For PSS, the salt length used is equal to the length of digest
        algorithm. For example, ``RSA_SIGN_PSS_2048_SHA256`` will use PSS with a
        salt length of 256 bits or 32 bytes.

        Algorithms beginning with "RSA\_DECRYPT\_" are usable with
        ``CryptoKey.purpose`` ``ASYMMETRIC_DECRYPT``.

        The fields in the name after "RSA\_DECRYPT\_" correspond to the
        following parameters: padding algorithm, modulus bit length, and digest
        algorithm.

        Algorithms beginning with "EC\_SIGN\_" are usable with
        ``CryptoKey.purpose`` ``ASYMMETRIC_SIGN``.

        The fields in the name after "EC\_SIGN\_" correspond to the following
        parameters: elliptic curve, digest algorithm.

        Attributes:
          CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED (int): Not specified.
          GOOGLE_SYMMETRIC_ENCRYPTION (int): Creates symmetric encryption keys.
          RSA_SIGN_PSS_2048_SHA256 (int): RSASSA-PSS 2048 bit key with a SHA256 digest.
          RSA_SIGN_PSS_3072_SHA256 (int): RSASSA-PSS 3072 bit key with a SHA256 digest.
          RSA_SIGN_PSS_4096_SHA256 (int): RSASSA-PSS 4096 bit key with a SHA256 digest.
          RSA_SIGN_PKCS1_2048_SHA256 (int): RSASSA-PKCS1-v1\_5 with a 2048 bit key and a SHA256 digest.
          RSA_SIGN_PKCS1_3072_SHA256 (int): RSASSA-PKCS1-v1\_5 with a 3072 bit key and a SHA256 digest.
          RSA_SIGN_PKCS1_4096_SHA256 (int): RSASSA-PKCS1-v1\_5 with a 4096 bit key and a SHA256 digest.
          RSA_DECRYPT_OAEP_2048_SHA256 (int): RSAES-OAEP 2048 bit key with a SHA256 digest.
          RSA_DECRYPT_OAEP_3072_SHA256 (int): RSAES-OAEP 3072 bit key with a SHA256 digest.
          RSA_DECRYPT_OAEP_4096_SHA256 (int): RSAES-OAEP 4096 bit key with a SHA256 digest.
          EC_SIGN_P256_SHA256 (int): ECDSA on the NIST P-256 curve with a SHA256 digest.
          EC_SIGN_P384_SHA384 (int): ECDSA on the NIST P-384 curve with a SHA384 digest.
        """

        CRYPTO_KEY_VERSION_ALGORITHM_UNSPECIFIED = 0
        GOOGLE_SYMMETRIC_ENCRYPTION = 1
        RSA_SIGN_PSS_2048_SHA256 = 2
        RSA_SIGN_PSS_3072_SHA256 = 3
        RSA_SIGN_PSS_4096_SHA256 = 4
        RSA_SIGN_PKCS1_2048_SHA256 = 5
        RSA_SIGN_PKCS1_3072_SHA256 = 6
        RSA_SIGN_PKCS1_4096_SHA256 = 7
        RSA_DECRYPT_OAEP_2048_SHA256 = 8
        RSA_DECRYPT_OAEP_3072_SHA256 = 9
        RSA_DECRYPT_OAEP_4096_SHA256 = 10
        EC_SIGN_P256_SHA256 = 12
        EC_SIGN_P384_SHA384 = 13

    class CryptoKeyVersionState(enum.IntEnum):
        """
        The state of a ``CryptoKeyVersion``, indicating if it can be used.

        Attributes:
          CRYPTO_KEY_VERSION_STATE_UNSPECIFIED (int): Not specified.
          PENDING_GENERATION (int): This version is still being generated. It may not be used, enabled,
          disabled, or destroyed yet. Cloud KMS will automatically mark this
          version ``ENABLED`` as soon as the version is ready.
          ENABLED (int): This version may be used for cryptographic operations.
          DISABLED (int): This version may not be used, but the key material is still available,
          and the version can be placed back into the ``ENABLED`` state.
          DESTROYED (int): This version is destroyed, and the key material is no longer stored.
          A version may not leave this state once entered.
          DESTROY_SCHEDULED (int): This version is scheduled for destruction, and will be destroyed soon.
          Call ``RestoreCryptoKeyVersion`` to put it back into the ``DISABLED``
          state.
        """

        CRYPTO_KEY_VERSION_STATE_UNSPECIFIED = 0
        PENDING_GENERATION = 5
        ENABLED = 1
        DISABLED = 2
        DESTROYED = 3
        DESTROY_SCHEDULED = 4

    class CryptoKeyVersionView(enum.IntEnum):
        """
        A view for ``CryptoKeyVersion``\ s. Controls the level of detail
        returned for ``CryptoKeyVersions`` in
        ``KeyManagementService.ListCryptoKeyVersions`` and
        ``KeyManagementService.ListCryptoKeys``.

        Attributes:
          CRYPTO_KEY_VERSION_VIEW_UNSPECIFIED (int): Default view for each ``CryptoKeyVersion``. Does not include the
          ``attestation`` field.
          FULL (int): Provides all fields in each ``CryptoKeyVersion``, including the
          ``attestation``.
        """

        CRYPTO_KEY_VERSION_VIEW_UNSPECIFIED = 0
        FULL = 1


class KeyOperationAttestation(object):
    class AttestationFormat(enum.IntEnum):
        """
        Attestion formats provided by the HSM.

        Attributes:
          ATTESTATION_FORMAT_UNSPECIFIED (int)
          CAVIUM_V1_COMPRESSED (int): Cavium HSM attestation compressed with gzip. Note that this format is
          defined by Cavium and subject to change at any time.
        """

        ATTESTATION_FORMAT_UNSPECIFIED = 0
        CAVIUM_V1_COMPRESSED = 3
