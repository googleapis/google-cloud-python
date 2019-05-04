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
import binascii
import collections
import datetime
import hashlib
import re

import six

import google.auth.credentials
from google.cloud import _helpers


NOW = datetime.datetime.utcnow  # To be replaced by tests.
MULTIPLE_SPACES_RE = r"\s+"
MULTIPLE_SPACES = re.compile(MULTIPLE_SPACES_RE)


def ensure_signed_credentials(credentials):
    """Raise AttributeError if the credentials are unsigned.

    :type credentials: :class:`google.auth.credentials.Signing`
    :param credentials: The credentials used to create a private key
                        for signing text.

    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.
    """
    if not isinstance(credentials, google.auth.credentials.Signing):
        auth_uri = (
            "https://google-cloud-python.readthedocs.io/en/latest/"
            "core/auth.html?highlight=authentication#setting-up-"
            "a-service-account"
        )
        raise AttributeError(
            "you need a private key to sign credentials."
            "the credentials you are currently using %s "
            "just contains a token. see %s for more "
            "details." % (type(credentials), auth_uri)
        )


def get_signed_query_params_v2(credentials, expiration, string_to_sign):
    """Gets query parameters for creating a signed URL.

    :type credentials: :class:`google.auth.credentials.Signing`
    :param credentials: The credentials used to create a private key
                        for signing text.

    :type expiration: int or long
    :param expiration: When the signed URL should expire.

    :type string_to_sign: str
    :param string_to_sign: The string to be signed by the credentials.

    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.

    :rtype: dict
    :returns: Query parameters matching the signing credentials with a
              signed payload.
    """
    ensure_signed_credentials(credentials)
    signature_bytes = credentials.sign_bytes(string_to_sign)
    signature = base64.b64encode(signature_bytes)
    service_account_name = credentials.signer_email
    return {
        "GoogleAccessId": service_account_name,
        "Expires": str(expiration),
        "Signature": signature,
    }


def get_expiration_seconds_v2(expiration):
    """Convert 'expiration' to a number of seconds in the future.

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire.

    :raises: :exc:`TypeError` when expiration is not a valid type.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds since epoch.
    """
    # If it's a timedelta, add it to `now` in UTC.
    if isinstance(expiration, datetime.timedelta):
        now = NOW().replace(tzinfo=_helpers.UTC)
        expiration = now + expiration

    # If it's a datetime, convert to a timestamp.
    if isinstance(expiration, datetime.datetime):
        micros = _helpers._microseconds_from_datetime(expiration)
        expiration = micros // 10 ** 6

    if not isinstance(expiration, six.integer_types):
        raise TypeError(
            "Expected an integer timestamp, datetime, or "
            "timedelta. Got %s" % type(expiration)
        )
    return expiration


_EXPIRATION_TYPES = six.integer_types + (datetime.datetime, datetime.timedelta)


def get_expiration_seconds_v4(expiration):
    """Convert 'expiration' to a number of seconds offset from the current time.

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire.

    :raises: :exc:`TypeError` when expiration is not a valid type.
    :raises: :exc:`ValueError` when expiration is too large.
    :rtype: Integer
    :returns: seconds in the future when the signed URL will expire
    """
    if not isinstance(expiration, _EXPIRATION_TYPES):
        raise TypeError(
            "Expected an integer timestamp, datetime, or "
            "timedelta. Got %s" % type(expiration)
        )

    now = NOW().replace(tzinfo=_helpers.UTC)

    if isinstance(expiration, six.integer_types):
        seconds = expiration

    if isinstance(expiration, datetime.datetime):

        if expiration.tzinfo is None:
            expiration = expiration.replace(tzinfo=_helpers.UTC)

        expiration = expiration - now

    if isinstance(expiration, datetime.timedelta):
        seconds = int(expiration.total_seconds())

    if seconds > SEVEN_DAYS:
        raise ValueError(
            "Max allowed expiration interval is seven days (%d seconds)".format(
                SEVEN_DAYS
            )
        )

    return seconds


def get_canonical_headers(headers):
    """Canonicalize headers for signing.

    See:
    https://cloud.google.com/storage/docs/access-control/signed-urls#about-canonical-extension-headers

    :type headers: Union[dict|List(Tuple(str,str))]
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :rtype: str
    :returns: List of headers, normalized / sortted per the URL refernced above.
    """
    if headers is None:
        headers = []
    elif isinstance(headers, dict):
        headers = list(headers.items())

    if not headers:
        return [], []

    normalized = collections.defaultdict(list)
    for key, val in headers:
        key = key.lower().strip()
        val = MULTIPLE_SPACES.sub(" ", val.strip())
        normalized[key].append(val)

    ordered_headers = sorted((key, ",".join(val)) for key, val in normalized.items())

    canonical_headers = ["{}:{}".format(*item) for item in ordered_headers]
    return canonical_headers, ordered_headers


_Canonical = collections.namedtuple(
    "_Canonical", ["method", "resource", "query_parameters", "headers"]
)


def canonicalize(method, resource, query_parameters, headers):
    """Canonicalize method, resource

    :type method: str
    :param method: The HTTP verb that will be used when requesting the URL.
                   Defaults to ``'GET'``. If method is ``'RESUMABLE'`` then the
                   signature will additionally contain the `x-goog-resumable`
                   header, and the method changed to POST. See the signed URL
                   docs regarding this flow:
                   https://cloud.google.com/storage/docs/access-control/signed-urls

    :type resource: str
    :param resource: A pointer to a specific resource
                     (typically, ``/bucket-name/path/to/blob.txt``).

    :type query_parameters: dict
    :param query_parameters:
        (Optional) Additional query paramtersto be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers#query

    :type headers: Union[dict|List(Tuple(str,str))]
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :rtype: :class:_Canonical
    :returns: Canonical method, resource, query_parameters, and headers.
    """
    headers, _ = get_canonical_headers(headers)

    if method == "RESUMABLE":
        method = "POST"
        headers.append("x-goog-resumable:start")

    if query_parameters is None:
        return _Canonical(method, resource, [], headers)

    normalized_qp = sorted(
        (key.lower(), value and value.strip() or "")
        for key, value in query_parameters.items()
    )
    encoded_qp = six.moves.urllib.parse.urlencode(normalized_qp)
    canonical_resource = "{}?{}".format(resource, encoded_qp)
    return _Canonical(method, canonical_resource, normalized_qp, headers)


def generate_signed_url_v2(
    credentials,
    resource,
    expiration,
    api_access_endpoint="",
    method="GET",
    content_md5=None,
    content_type=None,
    response_type=None,
    response_disposition=None,
    generation=None,
    headers=None,
    query_parameters=None,
):
    """Generate a V2 signed URL to provide query-string auth'n to a resource.

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

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire.

    :type api_access_endpoint: str
    :param api_access_endpoint: Optional URI base. Defaults to empty string.

    :type method: str
    :param method: The HTTP verb that will be used when requesting the URL.
                   Defaults to ``'GET'``. If method is ``'RESUMABLE'`` then the
                   signature will additionally contain the `x-goog-resumable`
                   header, and the method changed to POST. See the signed URL
                   docs regarding this flow:
                   https://cloud.google.com/storage/docs/access-control/signed-urls


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

    :type headers: Union[dict|List(Tuple(str,str))]
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :type query_parameters: dict
    :param query_parameters:
        (Optional) Additional query paramtersto be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers#query

    :raises: :exc:`TypeError` when expiration is not a valid type.
    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.

    :rtype: str
    :returns: A signed URL you can use to access the resource
              until expiration.
    """
    expiration_stamp = get_expiration_seconds_v2(expiration)

    canonical = canonicalize(method, resource, query_parameters, headers)

    # Generate the string to sign.
    elements_to_sign = [
        canonical.method,
        content_md5 or "",
        content_type or "",
        str(expiration_stamp),
    ]
    elements_to_sign.extend(canonical.headers)
    elements_to_sign.append(canonical.resource)
    string_to_sign = "\n".join(elements_to_sign)

    # Set the right query parameters.
    signed_query_params = get_signed_query_params_v2(
        credentials, expiration_stamp, string_to_sign
    )

    if response_type is not None:
        signed_query_params["response-content-type"] = response_type
    if response_disposition is not None:
        signed_query_params["response-content-disposition"] = response_disposition
    if generation is not None:
        signed_query_params["generation"] = generation

    signed_query_params.update(canonical.query_parameters)
    sorted_signed_query_params = sorted(signed_query_params.items())

    # Return the built URL.
    return "{endpoint}{resource}?{querystring}".format(
        endpoint=api_access_endpoint,
        resource=resource,
        querystring=six.moves.urllib.parse.urlencode(sorted_signed_query_params),
    )


SEVEN_DAYS = 7 * 24 * 60 * 60  # max age for V4 signed URLs.
DEFAULT_ENDPOINT = "https://storage.googleapis.com"


def generate_signed_url_v4(
    credentials,
    resource,
    expiration,
    api_access_endpoint=DEFAULT_ENDPOINT,
    method="GET",
    content_md5=None,
    content_type=None,
    response_type=None,
    response_disposition=None,
    generation=None,
    headers=None,
    query_parameters=None,
    _request_timestamp=None,  # for testing only
):
    """Generate a V4 signed URL to provide query-string auth'n to a resource.

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

    :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
    :param expiration: Point in time when the signed URL should expire.

    :type api_access_endpoint: str
    :param api_access_endpoint: Optional URI base. Defaults to
                                "https://storage.googleapis.com/"

    :type method: str
    :param method: The HTTP verb that will be used when requesting the URL.
                   Defaults to ``'GET'``. If method is ``'RESUMABLE'`` then the
                   signature will additionally contain the `x-goog-resumable`
                   header, and the method changed to POST. See the signed URL
                   docs regarding this flow:
                   https://cloud.google.com/storage/docs/access-control/signed-urls


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

    :type headers: dict
    :param headers:
        (Optional) Additional HTTP headers to be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers
        Requests using the signed URL *must* pass the specified header
        (name and value) with each request for the URL.

    :type query_parameters: dict
    :param query_parameters:
        (Optional) Additional query paramtersto be included as part of the
        signed URLs.  See:
        https://cloud.google.com/storage/docs/xml-api/reference-headers#query

    :raises: :exc:`TypeError` when expiration is not a valid type.
    :raises: :exc:`AttributeError` if credentials is not an instance
            of :class:`google.auth.credentials.Signing`.

    :rtype: str
    :returns: A signed URL you can use to access the resource
              until expiration.
    """
    ensure_signed_credentials(credentials)
    expiration_seconds = get_expiration_seconds_v4(expiration)

    if _request_timestamp is None:
        now = NOW()
        request_timestamp = now.strftime("%Y%m%dT%H%M%SZ")
        datestamp = now.date().strftime("%Y%m%d")
    else:
        request_timestamp = _request_timestamp
        datestamp = _request_timestamp[:8]

    client_email = credentials.signer_email
    credential_scope = "{}/auto/storage/goog4_request".format(datestamp)
    credential = "{}/{}".format(client_email, credential_scope)

    if headers is None:
        headers = {}

    if content_type is not None:
        headers["Content-Type"] = content_type

    if content_md5 is not None:
        headers["Content-MD5"] = content_md5

    header_names = [key.lower() for key in headers]
    if "host" not in header_names:
        headers["Host"] = "storage.googleapis.com"

    if method.upper() == "RESUMABLE":
        method = "POST"
        headers["x-goog-resumable"] = "start"

    canonical_headers, ordered_headers = get_canonical_headers(headers)
    canonical_header_string = (
        "\n".join(canonical_headers) + "\n"
    )  # Yes, Virginia, the extra newline is part of the spec.
    signed_headers = ";".join([key for key, _ in ordered_headers])

    if query_parameters is None:
        query_parameters = {}
    else:
        query_parameters = {key: value or "" for key, value in query_parameters.items()}

    query_parameters["X-Goog-Algorithm"] = "GOOG4-RSA-SHA256"
    query_parameters["X-Goog-Credential"] = credential
    query_parameters["X-Goog-Date"] = request_timestamp
    query_parameters["X-Goog-Expires"] = expiration_seconds
    query_parameters["X-Goog-SignedHeaders"] = signed_headers

    if response_type is not None:
        query_parameters["response-content-type"] = response_type

    if response_disposition is not None:
        query_parameters["response-content-disposition"] = response_disposition

    if generation is not None:
        query_parameters["generation"] = generation

    ordered_query_parameters = sorted(query_parameters.items())
    canonical_query_string = six.moves.urllib.parse.urlencode(ordered_query_parameters)

    canonical_elements = [
        method,
        resource,
        canonical_query_string,
        canonical_header_string,
        signed_headers,
        "UNSIGNED-PAYLOAD",
    ]
    canonical_request = "\n".join(canonical_elements)

    canonical_request_hash = hashlib.sha256(
        canonical_request.encode("ascii")
    ).hexdigest()

    string_elements = [
        "GOOG4-RSA-SHA256",
        request_timestamp,
        credential_scope,
        canonical_request_hash,
    ]
    string_to_sign = "\n".join(string_elements)

    signature_bytes = credentials.sign_bytes(string_to_sign.encode("ascii"))
    signature = binascii.hexlify(signature_bytes).decode("ascii")

    return "{}{}?{}&X-Goog-Signature={}".format(
        api_access_endpoint, resource, canonical_query_string, signature
    )
