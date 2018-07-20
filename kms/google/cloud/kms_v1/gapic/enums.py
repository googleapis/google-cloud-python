# Copyright 2018 Google LLC
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


class CryptoKey(object):
    class CryptoKeyPurpose(enum.IntEnum):
        """
        ``CryptoKeyPurpose`` describes the capabilities of a ``CryptoKey``. Two
        keys with the same purpose may use different underlying algorithms, but
        must support the same set of operations.

        Attributes:
          CRYPTO_KEY_PURPOSE_UNSPECIFIED (int): Not specified.
          ENCRYPT_DECRYPT (int): ``CryptoKeys`` with this purpose may be used with
          ``Encrypt`` and
          ``Decrypt``.
        """
        CRYPTO_KEY_PURPOSE_UNSPECIFIED = 0
        ENCRYPT_DECRYPT = 1


class CryptoKeyVersion(object):
    class CryptoKeyVersionState(enum.IntEnum):
        """
        The state of a ``CryptoKeyVersion``, indicating if it can be used.

        Attributes:
          CRYPTO_KEY_VERSION_STATE_UNSPECIFIED (int): Not specified.
          ENABLED (int): This version may be used in ``Encrypt`` and
          ``Decrypt`` requests.
          DISABLED (int): This version may not be used, but the key material is still available,
          and the version can be placed back into the ``ENABLED`` state.
          DESTROYED (int): This version is destroyed, and the key material is no longer stored.
          A version may not leave this state once entered.
          DESTROY_SCHEDULED (int): This version is scheduled for destruction, and will be destroyed soon.
          Call
          ``RestoreCryptoKeyVersion``
          to put it back into the ``DISABLED`` state.
        """
        CRYPTO_KEY_VERSION_STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        DESTROYED = 3
        DESTROY_SCHEDULED = 4
