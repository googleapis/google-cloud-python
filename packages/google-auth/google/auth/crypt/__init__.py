# Copyright 2016 Google LLC
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

"""Cryptography helpers for verifying and signing messages.

The simplest way to verify signatures is using :func:`verify_signature`::

    cert = open('certs.pem').read()
    valid = crypt.verify_signature(message, signature, cert)

If you're going to verify many messages with the same certificate, you can use
:class:`RSAVerifier`::

    cert = open('certs.pem').read()
    verifier = crypt.RSAVerifier.from_string(cert)
    valid = verifier.verify(message, signature)

To sign messages use :class:`RSASigner` with a private key::

    private_key = open('private_key.pem').read()
    signer = crypt.RSASigner.from_string(private_key)
    signature = signer.sign(message)

The code above also works for :class:`ES256Signer` and :class:`ES256Verifier`.
Note that these two classes are only available if your `cryptography` dependency
version is at least 1.4.0.
"""

from google.auth.crypt import base
from google.auth.crypt import es
from google.auth.crypt import es256
from google.auth.crypt import rsa

EsSigner = es.EsSigner
EsVerifier = es.EsVerifier
ES256Signer = es256.ES256Signer
ES256Verifier = es256.ES256Verifier


# Aliases to maintain the v1.0.0 interface, as the crypt module was split
# into submodules.
Signer = base.Signer
Verifier = base.Verifier
RSASigner = rsa.RSASigner
RSAVerifier = rsa.RSAVerifier


def from_service_account_info(info):
    """Create a Signer instance from a service account info dictionary.

    Automatically detects whether the private key is RSA or ECDSA (or other non-RSA)
    and returns the appropriate Signer instance.

    Args:
        info (Mapping[str, str]): Service account info dictionary.

    Returns:
        google.auth.crypt.Signer: The constructed signer.
    """
    private_key = info.get("private_key")
    key_id = info.get("private_key_id")
    if not private_key:
        raise ValueError("The private_key field is missing from service account info.")

    try:
        return RSASigner.from_service_account_info(info)
    except (ValueError, TypeError):
        pass

    return EsSigner.from_string(private_key, key_id=key_id)


def verify_signature(message, signature, certs, verifier_cls=rsa.RSAVerifier):
    """Verify an RSA or ECDSA cryptographic signature.

    Checks that the provided ``signature`` was generated from ``bytes`` using
    the private key associated with the ``cert``.

    Args:
        message (Union[str, bytes]): The plaintext message.
        signature (Union[str, bytes]): The cryptographic signature to check.
        certs (Union[Sequence, str, bytes]): The certificate or certificates
            to use to check the signature.
        verifier_cls (Optional[~google.auth.crypt.base.Signer]): Which verifier
            class to use for verification. This can be used to select different
            algorithms, such as RSA or ECDSA. Default value is :class:`RSAVerifier`.

    Returns:
        bool: True if the signature is valid, otherwise False.
    """
    if isinstance(certs, (str, bytes)):
        certs = [certs]

    for cert in certs:
        verifier = verifier_cls.from_string(cert)
        if verifier.verify(message, signature):
            return True
    return False


__all__ = [
    "EsSigner",
    "EsVerifier",
    "ES256Signer",
    "ES256Verifier",
    "RSASigner",
    "RSAVerifier",
    "Signer",
    "Verifier",
    "from_service_account_info",
]
