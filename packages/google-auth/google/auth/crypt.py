# Copyright 2016 Google Inc.
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

Uses the ``rsa``, ``pyasn1`` and ``pyasn1_modules`` packages
to parse PEM files storing PKCS#1 or PKCS#8 keys as well as
certificates. There is no support for p12 files.

The simplest way to verify signatures is using :func:`verify_signature`::

    cert = open('certs.pem').read()
    valid = crypt.verify_signature(message, signature, cert)

If you're going to verify many messages with the same certificate, you can use
:class:`Verifier`::

    cert = open('certs.pem').read()
    verifier = crypt.Verifier.from_string(cert)
    valid = verifier.verify(message, signature)


To sign messages use :class:`Signer` with a private key::

    private_key = open('private_key.pem').read()
    signer = crypt.Signer(private_key)
    signature = signer.sign(message)

"""

from pyasn1.codec.der import decoder
from pyasn1_modules import pem
from pyasn1_modules.rfc2459 import Certificate
from pyasn1_modules.rfc5208 import PrivateKeyInfo
import rsa
import six

from google.auth import _helpers

_POW2 = (128, 64, 32, 16, 8, 4, 2, 1)
_CERTIFICATE_MARKER = b'-----BEGIN CERTIFICATE-----'
_PKCS1_MARKER = ('-----BEGIN RSA PRIVATE KEY-----',
                 '-----END RSA PRIVATE KEY-----')
_PKCS8_MARKER = ('-----BEGIN PRIVATE KEY-----',
                 '-----END PRIVATE KEY-----')
_PKCS8_SPEC = PrivateKeyInfo()


def _bit_list_to_bytes(bit_list):
    """Converts an iterable of 1s and 0s to bytes.

    Combines the list 8 at a time, treating each group of 8 bits
    as a single byte.

    Args:
        bit_list (Sequence): Sequence of 1s and 0s.

    Returns:
        bytes: The decoded bytes.
    """
    num_bits = len(bit_list)
    byte_vals = bytearray()
    for start in six.moves.xrange(0, num_bits, 8):
        curr_bits = bit_list[start:start + 8]
        char_val = sum(val * digit
                       for val, digit in six.moves.zip(_POW2, curr_bits))
        byte_vals.append(char_val)
    return bytes(byte_vals)


class Verifier(object):
    """This object is used to verify cryptographic signatures.

    Args:
        public_key (rsa.key.PublicKey): The public key used to verify
            signatures.
    """

    def __init__(self, public_key):
        self._pubkey = public_key

    def verify(self, message, signature):
        """Verifies a message against a cryptographic signature.

        Args:
            message (Union[str, bytes]): The message to verify.
            signature (Union[str, bytes]): The cryptography signature to check.

        Returns:
            bool: True if message was signed by the private key associated
            with the public key that this object was constructed with.
        """
        message = _helpers.to_bytes(message)
        try:
            return rsa.pkcs1.verify(message, signature, self._pubkey)
        except (ValueError, rsa.pkcs1.VerificationError):
            return False

    @classmethod
    def from_string(cls, public_key):
        """Construct an Verifier instance from a public key or public
        certificate string.

        Args:
            public_key (Union[str, bytes]): The public key in PEM format or the
                x509 public key certificate.

        Returns:
            Verifier: The constructed verifier.

        Raises:
            ValueError: If the public_key can't be parsed.
        """
        public_key = _helpers.to_bytes(public_key)
        is_x509_cert = _CERTIFICATE_MARKER in public_key

        # If this is a certificate, extract the public key info.
        if is_x509_cert:
            der = rsa.pem.load_pem(public_key, 'CERTIFICATE')
            asn1_cert, remaining = decoder.decode(der, asn1Spec=Certificate())
            if remaining != b'':
                raise ValueError('Unused bytes', remaining)

            cert_info = asn1_cert['tbsCertificate']['subjectPublicKeyInfo']
            key_bytes = _bit_list_to_bytes(cert_info['subjectPublicKey'])
            pubkey = rsa.PublicKey.load_pkcs1(key_bytes, 'DER')
        else:
            pubkey = rsa.PublicKey.load_pkcs1(public_key, 'PEM')
        return cls(pubkey)


def verify_signature(message, signature, certs):
    """Verify a cryptographic signature.

    Checks that the provided ``signature`` was generated from ``bytes`` using
    the private key associated with the ``cert``.

    Args:
        message (Union[str, bytes]): The plaintext message.
        signature (Union[str, bytes]): The cryptographic signature to check.
        certs (Union[Sequence, str, bytes]): The certificate or certificates
            to use to check the signature.

    Returns:
        bool: True if the signature is valid, otherwise False.
    """
    if isinstance(certs, (six.text_type, six.binary_type)):
        certs = [certs]

    for cert in certs:
        verifier = Verifier.from_string(cert)
        if verifier.verify(message, signature):
            return True
    return False


class Signer(object):
    """Signs messages with a private key.

    Args:
        private_key (rsa.key.PrivateKey): The private key to sign with.
        key_id (str): Optional key ID used to identify this private key. This
            can be useful to associate the private key with its associated
            public key or certificate.
    """

    def __init__(self, private_key, key_id=None):
        self._key = private_key
        self.key_id = key_id

    def sign(self, message):
        """Signs a message.

        Args:
            message (Union[str, bytes]): The message to be signed.

        Returns:
            bytes: The signature of the message for the given key.
        """
        message = _helpers.to_bytes(message)
        return rsa.pkcs1.sign(message, self._key, 'SHA-256')

    @classmethod
    def from_string(cls, key, key_id=None):
        """Construct an Signer instance from a private key in PEM format.

        Args:
            key (str): Private key in PEM format.
            key_id (str): An optional key id used to identify the private key.

        Returns:
            Signer: The constructed signer.

        Raises:
            ValueError: If the key cannot be parsed as PKCS#1 or PKCS#8 in
                PEM format.
        """
        key = _helpers.from_bytes(key)  # PEM expects str in Python 3
        marker_id, key_bytes = pem.readPemBlocksFromFile(
            six.StringIO(key), _PKCS1_MARKER, _PKCS8_MARKER)

        # Key is in pkcs1 format.
        if marker_id == 0:
            private_key = rsa.key.PrivateKey.load_pkcs1(
                key_bytes, format='DER')
        # Key is in pkcs8.
        elif marker_id == 1:
            key_info, remaining = decoder.decode(
                key_bytes, asn1Spec=_PKCS8_SPEC)
            if remaining != b'':
                raise ValueError('Unused bytes', remaining)
            private_key_info = key_info.getComponentByName('privateKey')
            private_key = rsa.key.PrivateKey.load_pkcs1(
                private_key_info.asOctets(), format='DER')
        else:
            raise ValueError('No key could be detected.')

        return cls(private_key, key_id=key_id)
