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

"""PQC (ML-DSA) verifier and signer that use the ``cryptography`` library."""

from typing import Any, Optional, Union

from cryptography.hazmat import backends

try:
    from cryptography.hazmat.primitives import serialization
except ImportError:  # pragma: NO COVER
    pass

try:
    from cryptography.hazmat.primitives.asymmetric import mldsa
except ImportError:  # pragma: NO COVER
    mldsa = None  # type: ignore

from google.auth import _helpers
from google.auth.crypt import base

_BACKEND = backends.default_backend()


class PqcSigner(base.Signer, base.FromServiceAccountMixin):
    """Signs messages with a Post-Quantum Cryptography (ML-DSA) private key.

    Args:
        private_key: The ML-DSA private key object from cryptography.
        key_id (str): Optional key ID used to identify this private key.
    """

    def __init__(self, private_key: Any, key_id: Optional[str] = None) -> None:
        self._key = private_key
        self._key_id = key_id

    @property
    def algorithm(self) -> str:
        """Name of the algorithm used to sign messages.

        Returns:
            str: The algorithm name (e.g. 'ML-DSA-65' or 'ML-DSA-87').
        """
        if mldsa and isinstance(
            self._key, getattr(mldsa, "MLDSA87PrivateKey", type(None))
        ):
            return "ML-DSA-87"
        return "ML-DSA-65"

    @property  # type: ignore
    @_helpers.copy_docstring(base.Signer)
    def key_id(self) -> Optional[str]:
        return self._key_id

    @_helpers.copy_docstring(base.Signer)
    def sign(self, message: Union[str, bytes]) -> bytes:
        message = _helpers.to_bytes(message)
        return self._key.sign(message)

    @classmethod
    def from_string(  # type: ignore[override]
        cls, key: Union[bytes, str], key_id: Optional[str] = None
    ) -> "PqcSigner":
        """Construct a PqcSigner from a private key in PEM format.

        Args:
            key (Union[bytes, str]): Private key in PEM format.
            key_id (str): An optional key id used to identify the private key.

        Returns:
            PqcSigner: The constructed signer.
        """
        key_bytes = _helpers.to_bytes(key)
        private_key = serialization.load_pem_private_key(
            key_bytes, password=None, backend=_BACKEND
        )
        return cls(private_key, key_id=key_id)


def is_pqc_disabled() -> bool:
    """Checks whether Post-Quantum Cryptography (PQC) TLS key exchange is disabled via environment variable.

    Returns:
        bool: True if GOOGLE_CLOUD_DISABLE_PQC is set to '1', 'true', or 'yes'.
    """
    import os
    from google.auth import environment_vars

    val = os.environ.get(environment_vars.GOOGLE_CLOUD_DISABLE_PQC, "").lower()
    return val in ("1", "true", "yes")


def configure_ssl_context_pqc(ssl_context: Any) -> Any:
    """Configures an ssl.SSLContext object based on PQC environment settings.

    If PQC is disabled via GOOGLE_CLOUD_DISABLE_PQC, this function restricts the
    ECDH / key-exchange curves to classical algorithms (e.g. prime256v1:secp384r1),
    disabling hybrid PQC key-exchange (X25519MLKEM768).

    Args:
        ssl_context: An ssl.SSLContext instance.

    Returns:
        The configured ssl.SSLContext instance.
    """
    if is_pqc_disabled():
        if hasattr(ssl_context, "set_ecdh_curve"):
            try:
                ssl_context.set_ecdh_curve("prime256v1:secp384r1")
            except Exception:  # pragma: NO COVER
                pass
    return ssl_context

