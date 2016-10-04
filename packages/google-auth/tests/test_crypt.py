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

import os

import mock
from pyasn1_modules import pem
import pytest
import rsa
import six

from google.auth import _helpers
from google.auth import crypt


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# To generate privatekey.pem, privatekey.pub, and public_cert.pem:
#   $ openssl req -new -newkey rsa:1024 -x509 -nodes -out public_cert.pem \
#   >    -keyout privatekey.pem
#   $ openssl rsa -in privatekey.pem -pubout -out privatekey.pub

with open(os.path.join(DATA_DIR, 'privatekey.pem'), 'rb') as fh:
    PRIVATE_KEY_BYTES = fh.read()
    PKCS1_KEY_BYTES = PRIVATE_KEY_BYTES

with open(os.path.join(DATA_DIR, 'privatekey.pub'), 'rb') as fh:
    PUBLIC_KEY_BYTES = fh.read()

with open(os.path.join(DATA_DIR, 'public_cert.pem'), 'rb') as fh:
    PUBLIC_CERT_BYTES = fh.read()

# To generate other_cert.pem:
#   $ openssl req -new -newkey rsa:1024 -x509 -nodes -out other_cert.pem

with open(os.path.join(DATA_DIR, 'other_cert.pem'), 'rb') as fh:
    OTHER_CERT_BYTES = fh.read()

# To generate pem_from_pkcs12.pem and privatekey.p12:
#   $ openssl pkcs12 -export -out privatekey.p12 -inkey privatekey.pem \
#   >    -in public_cert.pem
#   $ openssl pkcs12 -in privatekey.p12 -nocerts -nodes \
#   >   -out pem_from_pkcs12.pem

with open(os.path.join(DATA_DIR, 'pem_from_pkcs12.pem'), 'rb') as fh:
    PKCS8_KEY_BYTES = fh.read()

with open(os.path.join(DATA_DIR, 'privatekey.p12'), 'rb') as fh:
    PKCS12_KEY_BYTES = fh.read()


def test_verify_signature():
    to_sign = b'foo'
    signer = crypt.Signer.from_string(PRIVATE_KEY_BYTES)
    signature = signer.sign(to_sign)

    assert crypt.verify_signature(
        to_sign, signature, PUBLIC_CERT_BYTES)

    # List of certs
    assert crypt.verify_signature(
        to_sign, signature, [OTHER_CERT_BYTES, PUBLIC_CERT_BYTES])


def test_verify_signature_failure():
    to_sign = b'foo'
    signer = crypt.Signer.from_string(PRIVATE_KEY_BYTES)
    signature = signer.sign(to_sign)

    assert not crypt.verify_signature(
        to_sign, signature, OTHER_CERT_BYTES)


class TestVerifier(object):
    def test_verify_success(self):
        to_sign = b'foo'
        signer = crypt.Signer.from_string(PRIVATE_KEY_BYTES)
        actual_signature = signer.sign(to_sign)

        verifier = crypt.Verifier.from_string(PUBLIC_KEY_BYTES)
        assert verifier.verify(to_sign, actual_signature)

    def test_verify_unicode_success(self):
        to_sign = u'foo'
        signer = crypt.Signer.from_string(PRIVATE_KEY_BYTES)
        actual_signature = signer.sign(to_sign)

        verifier = crypt.Verifier.from_string(PUBLIC_KEY_BYTES)
        assert verifier.verify(to_sign, actual_signature)

    def test_verify_failure(self):
        verifier = crypt.Verifier.from_string(PUBLIC_KEY_BYTES)
        bad_signature1 = b''
        assert not verifier.verify(b'foo', bad_signature1)
        bad_signature2 = b'a'
        assert not verifier.verify(b'foo', bad_signature2)

    def test_from_string_pub_key(self):
        verifier = crypt.Verifier.from_string(PUBLIC_KEY_BYTES)
        assert isinstance(verifier, crypt.Verifier)
        assert isinstance(verifier._pubkey, rsa.key.PublicKey)

    def test_from_string_pub_key_unicode(self):
        public_key = _helpers.from_bytes(PUBLIC_KEY_BYTES)
        verifier = crypt.Verifier.from_string(public_key)
        assert isinstance(verifier, crypt.Verifier)
        assert isinstance(verifier._pubkey, rsa.key.PublicKey)

    def test_from_string_pub_cert(self):
        verifier = crypt.Verifier.from_string(PUBLIC_CERT_BYTES)
        assert isinstance(verifier, crypt.Verifier)
        assert isinstance(verifier._pubkey, rsa.key.PublicKey)

    def test_from_string_pub_cert_unicode(self):
        public_cert = _helpers.from_bytes(PUBLIC_CERT_BYTES)
        verifier = crypt.Verifier.from_string(public_cert)
        assert isinstance(verifier, crypt.Verifier)
        assert isinstance(verifier._pubkey, rsa.key.PublicKey)

    def test_from_string_pub_cert_failure(self):
        cert_bytes = PUBLIC_CERT_BYTES
        true_der = rsa.pem.load_pem(cert_bytes, 'CERTIFICATE')
        with mock.patch('rsa.pem.load_pem',
                        return_value=true_der + b'extra') as load_pem:
            with pytest.raises(ValueError):
                crypt.Verifier.from_string(cert_bytes)
            load_pem.assert_called_once_with(cert_bytes, 'CERTIFICATE')


class TestSigner(object):
    def test_from_string_pkcs1(self):
        signer = crypt.Signer.from_string(PKCS1_KEY_BYTES)
        assert isinstance(signer, crypt.Signer)
        assert isinstance(signer._key, rsa.key.PrivateKey)

    def test_from_string_pkcs1_unicode(self):
        key_bytes = _helpers.from_bytes(PKCS1_KEY_BYTES)
        signer = crypt.Signer.from_string(key_bytes)
        assert isinstance(signer, crypt.Signer)
        assert isinstance(signer._key, rsa.key.PrivateKey)

    def test_from_string_pkcs8(self):
        signer = crypt.Signer.from_string(PKCS8_KEY_BYTES)
        assert isinstance(signer, crypt.Signer)
        assert isinstance(signer._key, rsa.key.PrivateKey)

    def test_from_string_pkcs8_extra_bytes(self):
        key_bytes = PKCS8_KEY_BYTES
        _, pem_bytes = pem.readPemBlocksFromFile(
            six.StringIO(_helpers.from_bytes(key_bytes)),
            crypt._PKCS8_MARKER)

        with mock.patch('pyasn1.codec.der.decoder.decode') as mock_decode:
            key_info, remaining = None, 'extra'
            mock_decode.return_value = (key_info, remaining)
            with pytest.raises(ValueError):
                crypt.Signer.from_string(key_bytes)
            # Verify mock was called.
            mock_decode.assert_called_once_with(
                pem_bytes, asn1Spec=crypt._PKCS8_SPEC)

    def test_from_string_pkcs8_unicode(self):
        key_bytes = _helpers.from_bytes(PKCS8_KEY_BYTES)
        signer = crypt.Signer.from_string(key_bytes)
        assert isinstance(signer, crypt.Signer)
        assert isinstance(signer._key, rsa.key.PrivateKey)

    def test_from_string_pkcs12(self):
        with pytest.raises(ValueError):
            crypt.Signer.from_string(PKCS12_KEY_BYTES)

    def test_from_string_bogus_key(self):
        key_bytes = 'bogus-key'
        with pytest.raises(ValueError):
            crypt.Signer.from_string(key_bytes)
