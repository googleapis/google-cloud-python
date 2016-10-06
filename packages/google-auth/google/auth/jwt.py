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

"""JSON Web Tokens

Provides support for creating (encoding) and verifying (decoding) JWTs,
especially JWTs generated and consumed by Google infrastructure.

See `rfc7519`_ for more details on JWTs.

To encode a JWT::

    from google.auth import crypto
    from google.auth import jwt

    signer = crypt.Signer(private_key)
    payload = {'some': 'payload'}
    encoded = jwt.encode(signer, payload)

To decode a JWT and verify claims::

    claims = jwt.decode(encoded, certs=public_certs)

You can also skip verification::

    claims = jwt.decode(encoded, verify=False)

.. _rfc7519: https://tools.ietf.org/html/rfc7519

"""

import base64
import collections
import json

from google.auth import crypt
from google.auth import _helpers


_DEFAULT_TOKEN_LIFETIME_SECS = 3600  # 1 hour in sections
_CLOCK_SKEW_SECS = 300  # 5 minutes in seconds


def encode(signer, payload, header=None, key_id=None):
    """Make a signed JWT.

    Args:
        signer (google.auth.crypt.Signer): The signer used to sign the JWT.
        payload (Mapping): The JWT payload.
        header (Mapping): Additional JWT header payload.
        key_id (str): The key id to add to the JWT header. If the
            signer has a key id it will be used as the default. If this is
            specified it will override the signer's key id.

    Returns:
        bytes: The encoded JWT.
    """
    if header is None:
        header = {}

    if key_id is None:
        key_id = signer.key_id

    header.update({'typ': 'JWT', 'alg': 'RS256'})

    if key_id is not None:
        header['kid'] = key_id

    segments = [
        base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')),
        base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')),
    ]

    signing_input = b'.'.join(segments)
    signature = signer.sign(signing_input)
    segments.append(base64.urlsafe_b64encode(signature))

    return b'.'.join(segments)


def _decode_jwt_segment(encoded_section):
    """Decodes a single JWT segment."""
    section_bytes = base64.urlsafe_b64decode(encoded_section)
    try:
        return json.loads(section_bytes.decode('utf-8'))
    except ValueError:
        raise ValueError('Can\'t parse segment: {0}'.format(section_bytes))


def _unverified_decode(token):
    """Decodes a token and does no verification.

    Args:
        token (Union[str, bytes]): The encoded JWT.

    Returns:
        Tuple(str, str, str, str): header, payload, signed_section, and
            signature.

    Raises:
        ValueError: if there are an incorrect amount of segments in the token.
    """
    token = _helpers.to_bytes(token)

    if token.count(b'.') != 2:
        raise ValueError(
            'Wrong number of segments in token: {0}'.format(token))

    encoded_header, encoded_payload, signature = token.split(b'.')
    signed_section = encoded_header + b'.' + encoded_payload
    signature = base64.urlsafe_b64decode(signature)

    # Parse segments
    header = _decode_jwt_segment(encoded_header)
    payload = _decode_jwt_segment(encoded_payload)

    return header, payload, signed_section, signature


def decode_header(token):
    """Return the decoded header of a token.

    No verification is done. This is useful to extract the key id from
    the header in order to acquire the appropriate certificate to verify
    the token.

    Args:
        token (Union[str, bytes]): the encoded JWT.

    Returns:
        Mapping: The decoded JWT header.
    """
    header, _, _, _ = _unverified_decode(token)
    return header


def _verify_iat_and_exp(payload):
    """Verifies the iat (Issued At) and exp (Expires) claims in a token
    payload.

    Args:
        payload (mapping): The JWT payload.

    Raises:
        ValueError: if any checks failed.
    """
    now = _helpers.datetime_to_secs(_helpers.utcnow())

    # Make sure the iat and exp claims are present
    for key in ('iat', 'exp'):
        if key not in payload:
            raise ValueError(
                'Token does not contain required claim {}'.format(key))

    # Make sure the token wasn't issued in the future
    iat = payload['iat']
    earliest = iat - _CLOCK_SKEW_SECS
    if now < earliest:
        raise ValueError('Token used too early, {} < {}'.format(now, iat))

    # Make sure the token wasn't issue in the past
    exp = payload['exp']
    latest = exp + _CLOCK_SKEW_SECS
    if latest < now:
        raise ValueError('Token expired, {} < {}'.format(latest, now))


def decode(token, certs=None, verify=True, audience=None):
    """Decode and verify a JWT.

    Args:
        token (string): The encoded JWT.
        certs (Union[str, bytes, Mapping]): The certificate used to
            validate. If bytes or string, it must the the public key
            certificate in PEM format. If a mapping, it must be a mapping of
            key IDs to public key certificates in PEM format. The mapping must
            contain the same key ID that's specified in the token's header.
        verify (bool): Whether to perform signature and claim validation.
            Verification is done by default.
        audience (str): The audience claim, 'aud', that this JWT should
            contain. If None then the JWT's 'aud' parameter is not verified.

    Returns:
        Mapping: The deserialized JSON payload in the JWT.

    Raises:
        ValueError: if any verification checks failed.
    """
    header, payload, signed_section, signature = _unverified_decode(token)

    if not verify:
        return payload

    # If certs is specified as a dictionary of key IDs to certificates, then
    # use the certificate identified by the key ID in the token header.
    if isinstance(certs, collections.Mapping):
        key_id = header.get('kid')
        if key_id:
            if key_id not in certs:
                raise ValueError(
                    'Certificate for key id {} not found.'.format(key_id))
            certs_to_check = [certs[key_id]]
        # If there's no key id in the header, check against all of the certs.
        else:
            certs_to_check = certs.values()
    else:
        certs_to_check = certs

    # Verify that the signature matches the message.
    if not crypt.verify_signature(signed_section, signature, certs_to_check):
        raise ValueError('Could not verify token signature.')

    # Verify the issued at and created times in the payload.
    _verify_iat_and_exp(payload)

    # Check audience.
    if audience is not None:
        claim_audience = payload.get('aud')
        if audience != claim_audience:
            raise ValueError(
                'Token has wrong audience {}, expected {}'.format(
                    claim_audience, audience))

    return payload
