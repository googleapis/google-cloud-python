# Copyright 2014 Google Inc.
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

import base64
import datetime
import os

import pytest

from google.auth import _helpers
from google.auth import crypt
from google.auth import jwt


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

with open(os.path.join(DATA_DIR, 'privatekey.pem'), 'rb') as fh:
    PRIVATE_KEY_BYTES = fh.read()

with open(os.path.join(DATA_DIR, 'public_cert.pem'), 'rb') as fh:
    PUBLIC_CERT_BYTES = fh.read()

with open(os.path.join(DATA_DIR, 'other_cert.pem'), 'rb') as fh:
    OTHER_CERT_BYTES = fh.read()


@pytest.fixture
def signer():
    return crypt.Signer.from_string(PRIVATE_KEY_BYTES, '1')


def test_encode_basic(signer):
    test_payload = {'test': 'value'}
    encoded = jwt.encode(signer, test_payload)
    header, payload, _, _ = jwt._unverified_decode(encoded)
    assert payload == test_payload
    assert header == {'typ': 'JWT', 'alg': 'RS256', 'kid': signer.key_id}


def test_encode_extra_headers(signer):
    encoded = jwt.encode(signer, {}, header={'extra': 'value'})
    header = jwt.decode_header(encoded)
    assert header == {
        'typ': 'JWT', 'alg': 'RS256', 'kid': signer.key_id, 'extra': 'value'}


@pytest.fixture
def token_factory(signer):
    def factory(claims=None, key_id=None):
        now = _helpers.datetime_to_secs(_helpers.utcnow())
        payload = {
            'aud': 'audience@example.com',
            'iat': now,
            'exp': now + 300,
            'user': 'billy bob',
            'metadata': {'meta': 'data'}
        }
        payload.update(claims or {})

        # False is specified to remove the signer's key id for testing
        # headers without key ids.
        if key_id is False:
            signer.key_id = None
            key_id = None

        return jwt.encode(signer, payload, key_id=key_id)
    return factory


def test_decode_valid(token_factory):
    payload = jwt.decode(token_factory(), certs=PUBLIC_CERT_BYTES)
    assert payload['aud'] == 'audience@example.com'
    assert payload['user'] == 'billy bob'
    assert payload['metadata']['meta'] == 'data'


def test_decode_valid_with_audience(token_factory):
    payload = jwt.decode(
        token_factory(), certs=PUBLIC_CERT_BYTES,
        audience='audience@example.com')
    assert payload['aud'] == 'audience@example.com'
    assert payload['user'] == 'billy bob'
    assert payload['metadata']['meta'] == 'data'


def test_decode_valid_unverified(token_factory):
    payload = jwt.decode(token_factory(), certs=OTHER_CERT_BYTES, verify=False)
    assert payload['aud'] == 'audience@example.com'
    assert payload['user'] == 'billy bob'
    assert payload['metadata']['meta'] == 'data'


def test_decode_bad_token_wrong_number_of_segments():
    with pytest.raises(ValueError) as excinfo:
        jwt.decode('1.2', PUBLIC_CERT_BYTES)
    assert excinfo.match(r'Wrong number of segments')


def test_decode_bad_token_not_base64():
    with pytest.raises((ValueError, TypeError)) as excinfo:
        jwt.decode('1.2.3', PUBLIC_CERT_BYTES)
    assert excinfo.match(r'Incorrect padding')


def test_decode_bad_token_not_json():
    token = b'.'.join([base64.urlsafe_b64encode(b'123!')] * 3)
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token, PUBLIC_CERT_BYTES)
    assert excinfo.match(r'Can\'t parse segment')


def test_decode_bad_token_no_iat_or_exp(signer):
    token = jwt.encode(signer, {'test': 'value'})
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token, PUBLIC_CERT_BYTES)
    assert excinfo.match(r'Token does not contain required claim')


def test_decode_bad_token_too_early(token_factory):
    token = token_factory(claims={
        'iat': _helpers.datetime_to_secs(
            _helpers.utcnow() + datetime.timedelta(hours=1))
    })
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token, PUBLIC_CERT_BYTES)
    assert excinfo.match(r'Token used too early')


def test_decode_bad_token_expired(token_factory):
    token = token_factory(claims={
        'exp': _helpers.datetime_to_secs(
            _helpers.utcnow() - datetime.timedelta(hours=1))
    })
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token, PUBLIC_CERT_BYTES)
    assert excinfo.match(r'Token expired')


def test_decode_bad_token_wrong_audience(token_factory):
    token = token_factory()
    audience = 'audience2@example.com'
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token, PUBLIC_CERT_BYTES, audience=audience)
    assert excinfo.match(r'Token has wrong audience')


def test_decode_wrong_cert(token_factory):
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token_factory(), OTHER_CERT_BYTES)
    assert excinfo.match(r'Could not verify token signature')


def test_decode_multicert_bad_cert(token_factory):
    certs = {'1': OTHER_CERT_BYTES, '2': PUBLIC_CERT_BYTES}
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token_factory(), certs)
    assert excinfo.match(r'Could not verify token signature')


def test_decode_no_cert(token_factory):
    certs = {'2': PUBLIC_CERT_BYTES}
    with pytest.raises(ValueError) as excinfo:
        jwt.decode(token_factory(), certs)
    assert excinfo.match(r'Certificate for key id 1 not found')


def test_decode_no_key_id(token_factory):
    token = token_factory(key_id=False)
    certs = {'2': PUBLIC_CERT_BYTES}
    payload = jwt.decode(token, certs)
    assert payload['user'] == 'billy bob'


def test_roundtrip_explicit_key_id(token_factory):
    token = token_factory(key_id='3')
    certs = {'2': OTHER_CERT_BYTES, '3': PUBLIC_CERT_BYTES}
    payload = jwt.decode(token, certs)
    assert payload['user'] == 'billy bob'
