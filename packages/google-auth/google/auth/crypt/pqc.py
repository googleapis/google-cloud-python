# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Post-quantum ML-DSA verifier and signer that use the ``cryptography`` library.
"""

from typing import Any, Dict, Optional, Union

import cryptography.exceptions
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import serialization
import cryptography.x509

from google.auth import _helpers
from google.auth.crypt import base

# ==============================================================================
# Module-level imports & NIST FIPS 204 OID definitions
# ==============================================================================

try:
    from cryptography.hazmat.primitives.asymmetric import mldsa
except ImportError:
    mldsa = None  # type: ignore

_CERTIFICATE_MARKER = b"-----BEGIN CERTIFICATE-----"
_BACKEND = backends.default_backend()

_UPGRADE_ERROR = (
    "Post-Quantum ML-DSA Service Account keys require cryptography>=47.0.0. "
    "Please upgrade your cryptography library (pip install 'cryptography>=47.0.0')."
)


def _get_mldsa_types(*attr_names: str) -> tuple:
    if mldsa is None:
        return ()
    types = []
    for name in attr_names:
        t = getattr(mldsa, name, None)
        if isinstance(t, type):
            types.append(t)
    return tuple(types)


# ==============================================================================
# Key detection helpers
# ==============================================================================


def is_mldsa_key(key: Union[str, bytes]) -> bool:
    """Determines whether a key is an ML-DSA private or public key."""
    if mldsa is None:
        return False

    expected_types = _get_mldsa_types(
        "MLDSA44PrivateKey",
        "MLDSA65PrivateKey",
        "MLDSA87PrivateKey",
        "MLDSA44PublicKey",
        "MLDSA65PublicKey",
        "MLDSA87PublicKey",
    )
    if not expected_types:
        return False

    try:
        key_bytes = _helpers.to_bytes(key)
    except (TypeError, ValueError, AttributeError):
        return False

    try:
        priv_key = serialization.load_pem_private_key(
            key_bytes, password=None, backend=_BACKEND
        )
        return isinstance(priv_key, expected_types)
    except Exception:
        pass

    try:
        pub_key = serialization.load_pem_public_key(key_bytes, _BACKEND)
        return isinstance(pub_key, expected_types)
    except Exception:
        pass

    return False


def _get_mldsa_algorithm_name(key: Any) -> str:
    """Determines the ML-DSA algorithm string ("ML-DSA-44", "ML-DSA-65", or "ML-DSA-87") for a key."""
    cls_name = key.__class__.__name__
    t44 = _get_mldsa_types("MLDSA44PrivateKey", "MLDSA44PublicKey")
    t65 = _get_mldsa_types("MLDSA65PrivateKey", "MLDSA65PublicKey")
    t87 = _get_mldsa_types("MLDSA87PrivateKey", "MLDSA87PublicKey")

    if "87" in cls_name or (t87 and isinstance(key, t87)):
        return "ML-DSA-87"
    if "65" in cls_name or (t65 and isinstance(key, t65)):
        return "ML-DSA-65"
    if "44" in cls_name or (t44 and isinstance(key, t44)):
        return "ML-DSA-44"

    raise TypeError(
        "Expected key of type ML-DSA (e.g. MLDSA44PrivateKey, MLDSA65PrivateKey, or MLDSA87PrivateKey), got: {}".format(
            cls_name
        )
    )


# ==============================================================================
# PQC Verifier
# ==============================================================================


class PqcVerifier(base.Verifier):
    """Verifies ML-DSA cryptographic signatures using public keys.

    ML-DSA-65 (3,309-byte signature) is set as the recommended default PQC key
    type over ML-DSA-87 (4,627 bytes) to minimize HTTP request header overhead.

    Args:
        public_key: The public key used to verify signatures.
    """

    def __init__(self, public_key: Any) -> None:
        self._pubkey = public_key

    @_helpers.copy_docstring(base.Verifier)
    def verify(self, message: bytes, signature: bytes) -> bool:
        message = _helpers.to_bytes(message)
        sig_bytes = _helpers.to_bytes(signature)
        try:
            self._pubkey.verify(sig_bytes, message)
            return True
        except (ValueError, TypeError, cryptography.exceptions.InvalidSignature):
            return False

    @classmethod
    def from_string(cls, public_key: Union[str, bytes]) -> "PqcVerifier":
        """Construct a Verifier instance from a public key or certificate string.

        Args:
            public_key (Union[bytes, str]): Public key or certificate in PEM format.

        Returns:
            google.auth.crypt.pqc.PqcVerifier: The constructed verifier.

        Raises:
            RuntimeError: If ``cryptography`` is less than version 47.0.0.
            TypeError: If ``public_key`` is not an ML-DSA public key.
        """
        if mldsa is None:
            raise RuntimeError(_UPGRADE_ERROR)

        public_key_data = _helpers.to_bytes(public_key)

        if _CERTIFICATE_MARKER in public_key_data:
            cert = cryptography.x509.load_pem_x509_certificate(
                public_key_data, _BACKEND
            )
            pubkey: Any = cert.public_key()
        else:
            pubkey = serialization.load_pem_public_key(public_key_data, _BACKEND)

        expected_types = _get_mldsa_types(
            "MLDSA44PublicKey", "MLDSA65PublicKey", "MLDSA87PublicKey"
        )
        if not expected_types or not isinstance(pubkey, expected_types):
            raise TypeError(
                "Expected public key of type ML-DSA (e.g. MLDSA44PublicKey, MLDSA65PublicKey, or MLDSA87PublicKey)"
            )

        return cls(pubkey)


# ==============================================================================
# PQC Signer
# ==============================================================================


class PqcSigner(base.Signer, base.FromServiceAccountMixin):
    """Signs messages with a post-quantum ML-DSA (Module-Lattice-Based Digital
    Signature Algorithm) private key.

    ML-DSA-65 (3,309-byte signature) is set as the recommended default PQC key
    type over ML-DSA-87 (4,627 bytes) to minimize HTTP request header overhead.

    Args:
        private_key: The ML-DSA private key to sign with.
        key_id (Optional[str]): Optional key ID used to identify this private key.
    """

    RECOMMENDED_DEFAULT_ALGORITHM = "ML-DSA-65"

    def __init__(self, private_key: Any, key_id: Optional[str] = None) -> None:
        self._key = private_key
        self._key_id = key_id
        self._algorithm = _get_mldsa_algorithm_name(private_key)

    @property
    def algorithm(self) -> str:
        """Name of the algorithm used to sign messages.

        Returns:
            str: The algorithm name (e.g., "ML-DSA-65" or "ML-DSA-87").
        """
        return self._algorithm

    @property  # type: ignore
    @_helpers.copy_docstring(base.Signer)
    def key_id(self) -> Optional[str]:
        return self._key_id

    @_helpers.copy_docstring(base.Signer)
    def sign(self, message: bytes) -> bytes:
        message = _helpers.to_bytes(message)
        return self._key.sign(message)

    @classmethod
    def from_string(
        cls, key: Union[bytes, str], key_id: Optional[str] = None
    ) -> "PqcSigner":
        """Construct a PqcSigner from a private key in PEM format.

        Args:
            key (Union[bytes, str]): Private key in PEM format.
            key_id (Optional[str]): An optional key id used to identify the private key.

        Returns:
            google.auth.crypt.pqc.PqcSigner: The constructed signer.

        Raises:
            RuntimeError: If ``cryptography`` is less than version 47.0.0.
            ValueError: If ``cryptography`` "Could not deserialize key data."
            TypeError: If ``key`` is not an ML-DSA private key.
        """
        if mldsa is None:
            raise RuntimeError(_UPGRADE_ERROR)

        key_bytes = _helpers.to_bytes(key)
        private_key = serialization.load_pem_private_key(
            key_bytes, password=None, backend=_BACKEND
        )

        expected_types = _get_mldsa_types(
            "MLDSA44PrivateKey", "MLDSA65PrivateKey", "MLDSA87PrivateKey"
        )
        if not expected_types or not isinstance(private_key, expected_types):
            raise TypeError(
                "Expected private key of type ML-DSA (e.g. MLDSA44PrivateKey, MLDSA65PrivateKey, or MLDSA87PrivateKey)"
            )

        return cls(private_key, key_id=key_id)

    def __getstate__(self) -> Dict[str, Any]:
        """Pickle helper that serializes the _key attribute."""
        state = self.__dict__.copy()
        state["_key"] = self._key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """Pickle helper that deserializes the _key attribute."""
        if mldsa is None:
            raise RuntimeError(_UPGRADE_ERROR)
        state = state.copy()
        state["_key"] = serialization.load_pem_private_key(
            state["_key"], password=None, backend=_BACKEND
        )
        self.__dict__.update(state)
