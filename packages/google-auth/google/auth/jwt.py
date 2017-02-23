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

To encode a JWT use :func:`encode`::

    from google.auth import crypto
    from google.auth import jwt

    signer = crypt.Signer(private_key)
    payload = {'some': 'payload'}
    encoded = jwt.encode(signer, payload)

To decode a JWT and verify claims use :func:`decode`::

    claims = jwt.decode(encoded, certs=public_certs)

You can also skip verification::

    claims = jwt.decode(encoded, verify=False)

.. _rfc7519: https://tools.ietf.org/html/rfc7519

"""

import base64
import collections
import datetime
import json

from google.auth import _helpers
from google.auth import _service_account_info
from google.auth import credentials
from google.auth import crypt


_DEFAULT_TOKEN_LIFETIME_SECS = 3600  # 1 hour in sections
_CLOCK_SKEW_SECS = 300  # 5 minutes in seconds


def encode(signer, payload, header=None, key_id=None):
    """Make a signed JWT.

    Args:
        signer (google.auth.crypt.Signer): The signer used to sign the JWT.
        payload (Mapping[str, str]): The JWT payload.
        header (Mapping[str, str]): Additional JWT header payload.
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
    section_bytes = _helpers.padded_urlsafe_b64decode(encoded_section)
    try:
        return json.loads(section_bytes.decode('utf-8'))
    except ValueError:
        raise ValueError('Can\'t parse segment: {0}'.format(section_bytes))


def _unverified_decode(token):
    """Decodes a token and does no verification.

    Args:
        token (Union[str, bytes]): The encoded JWT.

    Returns:
        Tuple[str, str, str, str]: header, payload, signed_section, and
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
    signature = _helpers.padded_urlsafe_b64decode(signature)

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
    """Verifies the ``iat`` (Issued At) and ``exp`` (Expires) claims in a token
    payload.

    Args:
        payload (Mapping[str, str]): The JWT payload.

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
        token (str): The encoded JWT.
        certs (Union[str, bytes, Mapping[str, Union[str, bytes]]]): The
            certificate used to validate the JWT signatyre. If bytes or string,
            it must the the public key certificate in PEM format. If a mapping,
            it must be a mapping of key IDs to public key certificates in PEM
            format. The mapping must contain the same key ID that's specified
            in the token's header.
        verify (bool): Whether to perform signature and claim validation.
            Verification is done by default.
        audience (str): The audience claim, 'aud', that this JWT should
            contain. If None then the JWT's 'aud' parameter is not verified.

    Returns:
        Mapping[str, str]: The deserialized JSON payload in the JWT.

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


class Credentials(credentials.Signing,
                  credentials.Credentials):
    """Credentials that use a JWT as the bearer token.

    These credentials require an "audience" claim. This claim identifies the
    intended recipient of the bearer token.

    The constructor arguments determine the claims for the JWT that is
    sent with requests. Usually, you'll construct these credentials with
    one of the helper constructors as shown in the next section.

    To create JWT credentials using a Google service account private key
    JSON file::

        credentials = jwt.Credentials.from_service_account_file(
            'service-account.json',
            audience='https://speech.googleapis.com')

    If you already have the service account file loaded and parsed::

        service_account_info = json.load(open('service_account.json'))
        credentials = jwt.Credentials.from_service_account_info(
            service_account_info,
            audience='https://speech.googleapis.com')

    Both helper methods pass on arguments to the constructor, so you can
    specify the JWT claims::

        credentials = jwt.Credentials.from_service_account_file(
            'service-account.json',
            audience='https://speech.googleapis.com',
            additional_claims={'meta': 'data'})

    You can also construct the credentials directly if you have a
    :class:`~google.auth.crypt.Signer` instance::

        credentials = jwt.Credentials(
            signer,
            issuer='your-issuer',
            subject='your-subject',
            audience=''https://speech.googleapis.com'')

    The claims are considered immutable. If you want to modify the claims,
    you can easily create another instance using :meth:`with_claims`::

        new_credentials = credentials.with_claims(
            audience='https://vision.googleapis.com')
    """

    def __init__(self, signer, issuer, subject, audience,
                 additional_claims=None,
                 token_lifetime=_DEFAULT_TOKEN_LIFETIME_SECS):
        """
        Args:
            signer (google.auth.crypt.Signer): The signer used to sign JWTs.
            issuer (str): The `iss` claim.
            subject (str): The `sub` claim.
            audience (str): the `aud` claim. The intended audience for the
                credentials.
            additional_claims (Mapping[str, str]): Any additional claims for
                the JWT payload.
            token_lifetime (int): The amount of time in seconds for
                which the token is valid. Defaults to 1 hour.
        """
        super(Credentials, self).__init__()
        self._signer = signer
        self._issuer = issuer
        self._subject = subject
        self._audience = audience
        self._token_lifetime = token_lifetime

        if additional_claims is not None:
            self._additional_claims = additional_claims
        else:
            self._additional_claims = {}

    @classmethod
    def _from_signer_and_info(cls, signer, info, **kwargs):
        """Creates a Credentials instance from a signer and service account
        info.

        Args:
            signer (google.auth.crypt.Signer): The signer used to sign JWTs.
            info (Mapping[str, str]): The service account info.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.jwt.Credentials: The constructed credentials.

        Raises:
            ValueError: If the info is not in the expected format.
        """
        kwargs.setdefault('subject', info['client_email'])
        kwargs.setdefault('issuer', info['client_email'])
        return cls(signer, **kwargs)

    @classmethod
    def from_service_account_info(cls, info, **kwargs):
        """Creates a Credentials instance from a dictionary containing service
        account info in Google format.

        Args:
            info (Mapping[str, str]): The service account info in Google
                format.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.jwt.Credentials: The constructed credentials.

        Raises:
            ValueError: If the info is not in the expected format.
        """
        signer = _service_account_info.from_dict(
            info, require=['client_email'])
        return cls._from_signer_and_info(signer, info, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename, **kwargs):
        """Creates a Credentials instance from a service account .json file
        in Google format.

        Args:
            filename (str): The path to the service account .json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.jwt.Credentials: The constructed credentials.
        """
        info, signer = _service_account_info.from_filename(
            filename, require=['client_email'])
        return cls._from_signer_and_info(signer, info, **kwargs)

    def with_claims(self, issuer=None, subject=None, audience=None,
                    additional_claims=None):
        """Returns a copy of these credentials with modified claims.

        Args:
            issuer (str): The `iss` claim. If unspecified the current issuer
                claim will be used.
            subject (str): The `sub` claim. If unspecified the current subject
                claim will be used.
            audience (str): the `aud` claim. If unspecified the current
                audience claim will be used.
            additional_claims (Mapping[str, str]): Any additional claims for
                the JWT payload. This will be merged with the current
                additional claims.

        Returns:
            google.auth.jwt.Credentials: A new credentials instance.
        """
        return Credentials(
            self._signer,
            issuer=issuer if issuer is not None else self._issuer,
            subject=subject if subject is not None else self._subject,
            audience=audience if audience is not None else self._audience,
            additional_claims=self._additional_claims.copy().update(
                additional_claims or {}))

    def _make_jwt(self):
        """Make a signed JWT.

        Returns:
            Tuple[bytes, datetime]: The encoded JWT and the expiration.
        """
        now = _helpers.utcnow()
        lifetime = datetime.timedelta(seconds=self._token_lifetime)
        expiry = now + lifetime

        payload = {
            'iss': self._issuer,
            'sub': self._subject,
            'iat': _helpers.datetime_to_secs(now),
            'exp': _helpers.datetime_to_secs(expiry),
            'aud': self._audience,
        }

        payload.update(self._additional_claims)

        jwt = encode(self._signer, payload)

        return jwt, expiry

    def refresh(self, request):
        """Refreshes the access token.

        Args:
            request (Any): Unused.
        """
        # pylint: disable=unused-argument
        # (pylint doesn't correctly recognize overridden methods.)
        self.token, self.expiry = self._make_jwt()

    @_helpers.copy_docstring(credentials.Signing)
    def sign_bytes(self, message):
        return self._signer.sign(message)

    @property
    @_helpers.copy_docstring(credentials.Signing)
    def signer_email(self):
        return self._issuer

    @property
    @_helpers.copy_docstring(credentials.Signing)
    def signer(self):
        return self._signer
