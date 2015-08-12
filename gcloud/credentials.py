# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A simple wrapper around the OAuth2 credentials library."""

import base64
import datetime
import six
from six.moves.urllib.parse import urlencode  # pylint: disable=F0401

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from oauth2client import client
from oauth2client.client import _get_application_default_credential_from_file
from oauth2client import crypt
from oauth2client import service_account

try:
    from google.appengine.api import app_identity
except ImportError:
    app_identity = None

try:
    from oauth2client.appengine import AppAssertionCredentials as _GAECreds
except ImportError:
    class _GAECreds(object):
        """Dummy class if not in App Engine environment."""

from gcloud._helpers import UTC
from gcloud._helpers import _NOW
from gcloud._helpers import _microseconds_from_datetime


def get_credentials():
    """Gets credentials implicitly from the current environment.

    .. note::
      You should not need to use this function directly. Instead, use the
      helper method :func:`gcloud.datastore.__init__.get_connection`
      which uses this method under the hood.

    Checks environment in order of precedence:

    * Google App Engine (production and testing)
    * Environment variable GOOGLE_APPLICATION_CREDENTIALS pointing to
      a file with stored credentials information.
    * Stored "well known" file associated with ``gcloud`` command line tool.
    * Google Compute Engine production environment.

    The file referred to in GOOGLE_APPLICATION_CREDENTIALS is expected to
    contain information about credentials that are ready to use. This means
    either service account information or user account information with
    a ready-to-use refresh token::

      {                                       {
          'type': 'authorized_user',              'type': 'service_account',
          'client_id': '...',                     'client_id': '...',
          'client_secret': '...',       OR        'client_email': '...',
          'refresh_token': '...,                  'private_key_id': '...',
      }                                           'private_key': '...',
                                              }

    The second of these is simply a JSON key downloaded from the Google APIs
    console. The first is a close cousin of the "client secrets" JSON file
    used by ``oauth2client.clientsecrets`` but differs in formatting.

    :rtype: :class:`oauth2client.client.GoogleCredentials`,
            :class:`oauth2client.appengine.AppAssertionCredentials`,
            :class:`oauth2client.gce.AppAssertionCredentials`,
            :class:`oauth2client.service_account._ServiceAccountCredentials`
    :returns: A new credentials instance corresponding to the implicit
              environment.
    """
    return client.GoogleCredentials.get_application_default()


def get_for_service_account_json(json_credentials_path, scope=None):
    """Gets the credentials for a service account with JSON key.

    :type json_credentials_path: string
    :param json_credentials_path: The path to a private key file (this file was
                                  given to you when you created the service
                                  account). This file must contain a JSON
                                  object with a private key and other
                                  credentials information (downloaded from the
                                  Google APIs console).

    :type scope: string or tuple of string
    :param scope: The scope against which to authenticate. (Different services
                  require different scopes, check the documentation for which
                  scope is required for the different levels of access to any
                  particular API.)

    :rtype: :class:`oauth2client.client.GoogleCredentials`,
            :class:`oauth2client.service_account._ServiceAccountCredentials`
    :returns: New service account or Google (for a user JSON key file)
              credentials object.
    """
    credentials = _get_application_default_credential_from_file(
        json_credentials_path)
    if scope is not None:
        credentials = credentials.create_scoped(scope)
    return credentials


def get_for_service_account_p12(client_email, private_key_path, scope=None):
    """Gets the credentials for a service account with PKCS12 / p12 key.

    .. note::
      This method is not used by default, instead :func:`get_credentials`
      is used. This method is intended to be used when the environments is
      known explicitly and detecting the environment implicitly would be
      superfluous.

    :type client_email: string
    :param client_email: The e-mail attached to the service account.

    :type private_key_path: string
    :param private_key_path: The path to a private key file (this file was
                             given to you when you created the service
                             account). This file must be in P12 format.

    :type scope: string or tuple of string
    :param scope: The scope against which to authenticate. (Different services
                  require different scopes, check the documentation for which
                  scope is required for the different levels of access to any
                  particular API.)

    :rtype: :class:`oauth2client.client.SignedJwtAssertionCredentials`
    :returns: A new ``SignedJwtAssertionCredentials`` instance with the
              needed service account settings.
    """
    return client.SignedJwtAssertionCredentials(
        service_account_name=client_email,
        private_key=open(private_key_path, 'rb').read(),
        scope=scope)


def _get_pem_key(credentials):
    """Gets RSA key for a PEM payload from a credentials object.

    :type credentials: :class:`client.SignedJwtAssertionCredentials`,
                       :class:`service_account._ServiceAccountCredentials`
    :param credentials: The credentials used to create an RSA key
                        for signing text.

    :rtype: :class:`Crypto.PublicKey.RSA._RSAobj`
    :returns: An RSA object used to sign text.
    :raises: `TypeError` if `credentials` is the wrong type.
    """
    if isinstance(credentials, client.SignedJwtAssertionCredentials):
        # Take our PKCS12 (.p12) key and make it into a RSA key we can use.
        pem_text = crypt.pkcs12_key_as_pem(credentials.private_key,
                                           credentials.private_key_password)
    elif isinstance(credentials, service_account._ServiceAccountCredentials):
        pem_text = credentials._private_key_pkcs8_text
    else:
        raise TypeError((credentials,
                         'not a valid service account credentials type'))

    return RSA.importKey(pem_text)


def _get_signature_bytes(credentials, string_to_sign):
    """Uses crypto attributes of credentials to sign a string/bytes.

    :type credentials: :class:`client.SignedJwtAssertionCredentials`,
                       :class:`service_account._ServiceAccountCredentials`,
                       :class:`_GAECreds`
    :param credentials: The credentials used for signing text (typically
                        involves the creation of an RSA key).

    :type string_to_sign: string
    :param string_to_sign: The string to be signed by the credentials.

    :rtype: bytes
    :returns: Signed bytes produced by the credentials.
    """
    if isinstance(credentials, _GAECreds):
        _, signed_bytes = app_identity.sign_blob(string_to_sign)
        return signed_bytes
    else:
        pem_key = _get_pem_key(credentials)
        # Sign the string with the RSA key.
        signer = PKCS1_v1_5.new(pem_key)
        if not isinstance(string_to_sign, six.binary_type):
            string_to_sign = string_to_sign.encode('utf-8')
        signature_hash = SHA256.new(string_to_sign)
        return signer.sign(signature_hash)


def _get_service_account_name(credentials):
    """Determines service account name from a credentials object.

    :type credentials: :class:`client.SignedJwtAssertionCredentials`,
                       :class:`service_account._ServiceAccountCredentials`,
                       :class:`_GAECreds`
    :param credentials: The credentials used to determine the service
                        account name.

    :rtype: string
    :returns: Service account name associated with the credentials.
    :raises: :class:`ValueError` if the credentials are not a valid service
             account type.
    """
    service_account_name = None
    if isinstance(credentials, client.SignedJwtAssertionCredentials):
        service_account_name = credentials.service_account_name
    elif isinstance(credentials, service_account._ServiceAccountCredentials):
        service_account_name = credentials._service_account_email
    elif isinstance(credentials, _GAECreds):
        service_account_name = app_identity.get_service_account_name()

    if service_account_name is None:
        raise ValueError('Service account name could not be determined '
                         'from credentials')
    return service_account_name


def _get_signed_query_params(credentials, expiration, string_to_sign):
    """Gets query parameters for creating a signed URL.

    :type credentials: :class:`client.SignedJwtAssertionCredentials`,
                       :class:`service_account._ServiceAccountCredentials`
    :param credentials: The credentials used to create an RSA key
                        for signing text.

    :type expiration: int or long
    :param expiration: When the signed URL should expire.

    :type string_to_sign: string
    :param string_to_sign: The string to be signed by the credentials.

    :rtype: dict
    :returns: Query parameters matching the signing credentials with a
              signed payload.
    """
    signature_bytes = _get_signature_bytes(credentials, string_to_sign)
    signature = base64.b64encode(signature_bytes)
    service_account_name = _get_service_account_name(credentials)
    return {
        'GoogleAccessId': service_account_name,
        'Expires': str(expiration),
        'Signature': signature,
    }


def _get_expiration_seconds(expiration):
    """Convert 'expiration' to a number of seconds in the future.

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds.
    """
    # If it's a timedelta, add it to `now` in UTC.
    if isinstance(expiration, datetime.timedelta):
        now = _NOW().replace(tzinfo=UTC)
        expiration = now + expiration

    # If it's a datetime, convert to a timestamp.
    if isinstance(expiration, datetime.datetime):
        micros = _microseconds_from_datetime(expiration)
        expiration = micros // 10**6

    if not isinstance(expiration, six.integer_types):
        raise TypeError('Expected an integer timestamp, datetime, or '
                        'timedelta. Got %s' % type(expiration))
    return expiration


def generate_signed_url(credentials, resource, expiration,
                        api_access_endpoint='',
                        method='GET', content_md5=None,
                        content_type=None):
    """Generate signed URL to provide query-string auth'n to a resource.

    .. note::
      If you are on Google Compute Engine, you can't generate a signed URL.
      Follow https://github.com/GoogleCloudPlatform/gcloud-python/issues/922
      for updates on this. If you'd like to be able to generate a signed URL
      from GCE, you can use a standard service account from a JSON file
      rather than a GCE service account.

    :type credentials: :class:`oauth2client.appengine.AppAssertionCredentials`
    :param credentials: Credentials object with an associated private key to
                        sign text.

    :type resource: string
    :param resource: A pointer to a specific resource
                     (typically, ``/bucket-name/path/to/blob.txt``).

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :type api_access_endpoint: string
    :param api_access_endpoint: Optional URI base. Defaults to empty string.

    :type method: string
    :param method: The HTTP verb that will be used when requesting the URL.

    :type content_md5: string
    :param content_md5: The MD5 hash of the object referenced by
                        ``resource``.

    :type content_type: string
    :param content_type: The content type of the object referenced by
                         ``resource``.

    :rtype: string
    :returns: A signed URL you can use to access the resource
              until expiration.
    """
    expiration = _get_expiration_seconds(expiration)

    # Generate the string to sign.
    string_to_sign = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        str(expiration),
        resource])

    # Set the right query parameters.
    query_params = _get_signed_query_params(credentials,
                                            expiration,
                                            string_to_sign)

    # Return the built URL.
    return '{endpoint}{resource}?{querystring}'.format(
        endpoint=api_access_endpoint, resource=resource,
        querystring=urlencode(query_params))
