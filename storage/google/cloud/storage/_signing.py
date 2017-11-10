# Copyright 2017 Google LLC
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


import base64
import datetime

import six

import google.auth.credentials
from google.cloud import _helpers


NOW = datetime.datetime.utcnow  # To be replaced by tests.


def ensure_signed_credentials(credentials):
    """Raise AttributeError if the credentials are unsigned.

    :type credentials: :class:`google.auth.credentials.Signer`
    :param credentials: The credentials used to create a private key
                        for signing text.
    """
    if not isinstance(credentials, google.auth.credentials.Signing):
        auth_uri = ('https://google-cloud-python.readthedocs.io/en/latest/'
                    'core/auth.html?highlight=authentication#setting-up-'
                    'a-service-account')
        raise AttributeError('you need a private key to sign credentials.'
                             'the credentials you are currently using %s '
                             'just contains a token. see %s for more '
                             'details.' % (type(credentials), auth_uri))


def get_signed_query_params(credentials, expiration, string_to_sign):
    """Gets query parameters for creating a signed URL.

    :type credentials: :class:`google.auth.credentials.Signer`
    :param credentials: The credentials used to create a private key
                        for signing text.

    :type expiration: int or long
    :param expiration: When the signed URL should expire.

    :type string_to_sign: str
    :param string_to_sign: The string to be signed by the credentials.

    :raises AttributeError: If :meth: sign_blob is unavailable.

    :rtype: dict
    :returns: Query parameters matching the signing credentials with a
              signed payload.
    """
    ensure_signed_credentials(credentials)
    signature_bytes = credentials.sign_bytes(string_to_sign)
    signature = base64.b64encode(signature_bytes)
    service_account_name = credentials.signer_email
    return {
        'GoogleAccessId': service_account_name,
        'Expires': str(expiration),
        'Signature': signature,
    }


def get_expiration_seconds(expiration):
    """Convert 'expiration' to a number of seconds in the future.

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :raises TypeError: When expiration is not an integer.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds.
    """
    # If it's a timedelta, add it to `now` in UTC.
    if isinstance(expiration, datetime.timedelta):
        now = NOW().replace(tzinfo=_helpers.UTC)
        expiration = now + expiration

    # If it's a datetime, convert to a timestamp.
    if isinstance(expiration, datetime.datetime):
        micros = _helpers._microseconds_from_datetime(expiration)
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

        Assumes ``credentials`` implements the
        :class:`google.auth.credentials.Signing` interface. Also assumes
        ``credentials`` has a ``service_account_email`` property which
        identifies the credentials.

    .. note::

        If you are on Google Compute Engine, you can't generate a signed URL.
        Follow `Issue 922`_ for updates on this. If you'd like to be able to
        generate a signed URL from GCE, you can use a standard service account
        from a JSON file rather than a GCE service account.

    See headers `reference`_ for more details on optional arguments.

    .. _Issue 922: https://github.com/GoogleCloudPlatform/\
                   google-cloud-python/issues/922
    .. _reference: https://cloud.google.com/storage/docs/reference-headers

    :type credentials: :class:`google.auth.credentials.Signing`
    :param credentials: Credentials object with an associated private key to
                        sign text.

    :type resource: str
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

    :rtype: str
    :returns: A signed URL you can use to access the resource
              until expiration.
    """
    expiration = get_expiration_seconds(expiration)

    # Generate the string to sign.
    string_to_sign = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        str(expiration),
        resource,
    ])

    # Set the right query parameters.
    query_params = get_signed_query_params(
        credentials, expiration, string_to_sign)

    if response_type is not None:
        query_params['response-content-type'] = response_type
    if response_disposition is not None:
        query_params['response-content-disposition'] = response_disposition
    if generation is not None:
        query_params['generation'] = generation

    # Return the built URL.
    return '{endpoint}{resource}?{querystring}'.format(
        endpoint=api_access_endpoint, resource=resource,
        querystring=six.moves.urllib.parse.urlencode(query_params))
