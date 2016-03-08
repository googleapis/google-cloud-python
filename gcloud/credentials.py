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
from six.moves.urllib.parse import urlencode

from oauth2client import client

from gcloud._helpers import UTC
from gcloud._helpers import _NOW
from gcloud._helpers import _microseconds_from_datetime


def get_credentials():
    """Gets credentials implicitly from the current environment.

    .. note::

        You should not need to use this function directly. Instead, use a
        helper method which uses this method under the hood.

    Checks environment in order of precedence:

    * Google App Engine (production and testing)
    * Environment variable :envvar:`GOOGLE_APPLICATION_CREDENTIALS` pointing to
      a file with stored credentials information.
    * Stored "well known" file associated with ``gcloud`` command line tool.
    * Google Compute Engine production environment.

    The file referred to in :envvar:`GOOGLE_APPLICATION_CREDENTIALS` is
    expected to contain information about credentials that are ready to use.
    This means either service account information or user account information
    with a ready-to-use refresh token:

    .. code:: json

      {
          'type': 'authorized_user',
          'client_id': '...',
          'client_secret': '...',
          'refresh_token': '...'
      }

    or

    .. code:: json

      {
          'type': 'service_account',
          'client_id': '...',
          'client_email': '...',
          'private_key_id': '...',
          'private_key': '...'
      }

    The second of these is simply a JSON key downloaded from the Google APIs
    console. The first is a close cousin of the "client secrets" JSON file
    used by :mod:`oauth2client.clientsecrets` but differs in formatting.

    :rtype: :class:`oauth2client.client.GoogleCredentials`,
            :class:`oauth2client.contrib.appengine.AppAssertionCredentials`,
            :class:`oauth2client.contrib.gce.AppAssertionCredentials`,
            :class:`oauth2client.service_account.ServiceAccountCredentials`
    :returns: A new credentials instance corresponding to the implicit
              environment.
    """
    return client.GoogleCredentials.get_application_default()


def _get_signed_query_params(credentials, expiration, string_to_sign):
    """Gets query parameters for creating a signed URL.

    :type credentials: :class:`oauth2client.client.AssertionCredentials`
    :param credentials: The credentials used to create a private key
                        for signing text.

    :type expiration: int or long
    :param expiration: When the signed URL should expire.

    :type string_to_sign: string
    :param string_to_sign: The string to be signed by the credentials.

    :rtype: dict
    :returns: Query parameters matching the signing credentials with a
              signed payload.
    """
    _, signature_bytes = credentials.sign_blob(string_to_sign)
    signature = base64.b64encode(signature_bytes)
    service_account_name = credentials.service_account_email
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
                        content_type=None, response_type=None,
                        response_disposition=None, generation=None):
    """Generate signed URL to provide query-string auth'n to a resource.

    .. note::

        Assumes ``credentials`` implements a ``sign_blob()`` method that takes
        bytes to sign and returns a pair of the key ID (unused here) and the
        signed bytes (this is abstract in the base class
        :class:`oauth2client.client.AssertionCredentials`). Also assumes
        ``credentials`` has a ``service_account_email`` property which
        identifies the credentials.

    .. note::

        If you are on Google Compute Engine, you can't generate a signed URL.
        Follow `Issue 922`_ for updates on this. If you'd like to be able to
        generate a signed URL from GCE, you can use a standard service account
        from a JSON file rather than a GCE service account.

    See headers `reference`_ for more details on optional arguments.

    .. _Issue 922: https://github.com/GoogleCloudPlatform/\
                   gcloud-python/issues/922
    .. _reference: https://cloud.google.com/storage/docs/reference-headers

    :type credentials: :class:`oauth2client.appengine.AppAssertionCredentials`
    :param credentials: Credentials object with an associated private key to
                        sign text.

    :type resource: string
    :param resource: A pointer to a specific resource
                     (typically, ``/bucket-name/path/to/blob.txt``).

    :type expiration: :class:`int`, :class:`long`, :class:`datetime.datetime`,
                      :class:`datetime.timedelta`
    :param expiration: When the signed URL should expire.

    :type api_access_endpoint: str
    :param api_access_endpoint: Optional URI base. Defaults to empty string.

    :type method: str
    :param method: The HTTP verb that will be used when requesting the URL.
                   Defaults to ``'GET'``.

    :type content_md5: str
    :param content_md5: (Optional) The MD5 hash of the object referenced by
                        ``resource``.

    :type content_type: str
    :param content_type: (Optional) The content type of the object referenced
                         by ``resource``.

    :type response_type: str
    :param response_type: (Optional) Content type of responses to requests for
                          the signed URL. Used to over-ride the content type of
                          the underlying resource.

    :type response_disposition: str
    :param response_disposition: (Optional) Content disposition of responses to
                                 requests for the signed URL.

    :type generation: str
    :param generation: (Optional) A value that indicates which generation of
                       the resource to fetch.

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
    if response_type is not None:
        query_params['response-content-type'] = response_type
    if response_disposition is not None:
        query_params['response-content-disposition'] = response_disposition
    if generation is not None:
        query_params['generation'] = generation

    # Return the built URL.
    return '{endpoint}{resource}?{querystring}'.format(
        endpoint=api_access_endpoint, resource=resource,
        querystring=urlencode(query_params))
