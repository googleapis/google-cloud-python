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
import calendar
import datetime
import six
from six.moves.urllib.parse import urlencode  # pylint: disable=F0401

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from oauth2client import client
from oauth2client import crypt
from oauth2client import service_account
import pytz


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


def get_for_service_account_p12(client_email, private_key_path, scope=None):
    """Gets the credentials for a service account.

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


def _get_signed_query_params(credentials, expiration, signature_string):
    """Gets query parameters for creating a signed URL.

    :type credentials: :class:`client.SignedJwtAssertionCredentials`,
                       :class:`service_account._ServiceAccountCredentials`
    :param credentials: The credentials used to create an RSA key
                        for signing text.

    :type expiration: int or long
    :param expiration: When the signed URL should expire.

    :type signature_string: string
    :param signature_string: The string to be signed by the credentials.

    :rtype: dict
    :returns: Query parameters matching the signing credentials with a
              signed payload.
    """
    pem_key = _get_pem_key(credentials)
    # Sign the string with the RSA key.
    signer = PKCS1_v1_5.new(pem_key)
    signature_hash = SHA256.new(signature_string)
    signature_bytes = signer.sign(signature_hash)
    signature = base64.b64encode(signature_bytes)

    if isinstance(credentials, client.SignedJwtAssertionCredentials):
        service_account_name = credentials.service_account_name
    elif isinstance(credentials, service_account._ServiceAccountCredentials):
        service_account_name = credentials._service_account_email
    # We know one of the above must occur since `_get_pem_key` fails if not.
    return {
        'GoogleAccessId': service_account_name,
        'Expires': str(expiration),
        'Signature': signature,
    }


def _utcnow():  # pragma: NO COVER testing replaces
    """Returns current time as UTC datetime.

    NOTE: on the module namespace so tests can replace it.
    """
    return datetime.datetime.utcnow()


def _get_expiration_seconds(expiration):
    """Convert 'expiration' to a number of seconds in the future.

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds.
    """
    # If it's a timedelta, add it to `now` in UTC.
    if isinstance(expiration, datetime.timedelta):
        now = _utcnow().replace(tzinfo=pytz.utc)
        expiration = now + expiration

    # If it's a datetime, convert to a timestamp.
    if isinstance(expiration, datetime.datetime):
        # Make sure the timezone on the value is UTC
        # (either by converting or replacing the value).
        if expiration.tzinfo:
            expiration = expiration.astimezone(pytz.utc)
        else:
            expiration = expiration.replace(tzinfo=pytz.utc)

        # Turn the datetime into a timestamp (seconds, not microseconds).
        expiration = int(calendar.timegm(expiration.timetuple()))

    if not isinstance(expiration, six.integer_types):
        raise TypeError('Expected an integer timestamp, datetime, or '
                        'timedelta. Got %s' % type(expiration))
    return expiration


def generate_signed_url(credentials, resource, expiration,
                        api_access_endpoint='',
                        method='GET', content_md5=None,
                        content_type=None):
    """Generate signed URL to provide query-string auth'n to a resource.

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
    signature_string = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        str(expiration),
        resource])

    # Set the right query parameters.
    query_params = _get_signed_query_params(credentials,
                                            expiration,
                                            signature_string)

    # Return the built URL.
    return '{endpoint}{resource}?{querystring}'.format(
        endpoint=api_access_endpoint, resource=resource,
        querystring=urlencode(query_params))
