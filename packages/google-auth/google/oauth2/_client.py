# Copyright 2016 Google LLC
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

"""OAuth 2.0 client.

This is a client for interacting with an OAuth 2.0 authorization server's
token endpoint.

For more information about the token endpoint, see
`Section 3.1 of rfc6749`_

.. _Section 3.1 of rfc6749: https://tools.ietf.org/html/rfc6749#section-3.2
"""

import datetime
import http.client
import json
import urllib

from google.auth import _helpers
from google.auth import exceptions
from google.auth import jwt

_URLENCODED_CONTENT_TYPE = "application/x-www-form-urlencoded"
_JSON_CONTENT_TYPE = "application/json"
_JWT_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"
_REFRESH_GRANT_TYPE = "refresh_token"


def _handle_error_response(response_data):
    """Translates an error response into an exception.

    Args:
        response_data (Mapping): The decoded response data.

    Raises:
        google.auth.exceptions.RefreshError: The errors contained in response_data.
    """
    try:
        error_details = "{}: {}".format(
            response_data["error"], response_data.get("error_description")
        )
    # If no details could be extracted, use the response data.
    except (KeyError, ValueError):
        error_details = json.dumps(response_data)

    raise exceptions.RefreshError(error_details, response_data)


def _parse_expiry(response_data):
    """Parses the expiry field from a response into a datetime.

    Args:
        response_data (Mapping): The JSON-parsed response data.

    Returns:
        Optional[datetime]: The expiration or ``None`` if no expiration was
            specified.
    """
    expires_in = response_data.get("expires_in", None)

    if expires_in is not None:
        return _helpers.utcnow() + datetime.timedelta(seconds=expires_in)
    else:
        return None


def _token_endpoint_request_no_throw(
    request, token_uri, body, access_token=None, use_json=False
):
    """Makes a request to the OAuth 2.0 authorization server's token endpoint.
    This function doesn't throw on response errors.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorizations server's token endpoint
            URI.
        body (Mapping[str, str]): The parameters to send in the request body.
        access_token (Optional(str)): The access token needed to make the request.
        use_json (Optional(bool)): Use urlencoded format or json format for the
            content type. The default value is False.

    Returns:
        Tuple(bool, Mapping[str, str]): A boolean indicating if the request is
            successful, and a mapping for the JSON-decoded response data.
    """
    if use_json:
        headers = {"Content-Type": _JSON_CONTENT_TYPE}
        body = json.dumps(body).encode("utf-8")
    else:
        headers = {"Content-Type": _URLENCODED_CONTENT_TYPE}
        body = urllib.parse.urlencode(body).encode("utf-8")

    if access_token:
        headers["Authorization"] = "Bearer {}".format(access_token)

    retry = 0
    # retry to fetch token for maximum of two times if any internal failure
    # occurs.
    while True:
        response = request(method="POST", url=token_uri, headers=headers, body=body)
        response_body = (
            response.data.decode("utf-8")
            if hasattr(response.data, "decode")
            else response.data
        )
        response_data = json.loads(response_body)

        if response.status == http.client.OK:
            break
        else:
            error_desc = response_data.get("error_description") or ""
            error_code = response_data.get("error") or ""
            if (
                any(e == "internal_failure" for e in (error_code, error_desc))
                and retry < 1
            ):
                retry += 1
                continue
            return response.status == http.client.OK, response_data

    return response.status == http.client.OK, response_data


def _token_endpoint_request(
    request, token_uri, body, access_token=None, use_json=False
):
    """Makes a request to the OAuth 2.0 authorization server's token endpoint.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorizations server's token endpoint
            URI.
        body (Mapping[str, str]): The parameters to send in the request body.
        access_token (Optional(str)): The access token needed to make the request.
        use_json (Optional(bool)): Use urlencoded format or json format for the
            content type. The default value is False.

    Returns:
        Mapping[str, str]: The JSON-decoded response data.

    Raises:
        google.auth.exceptions.RefreshError: If the token endpoint returned
            an error.
    """
    response_status_ok, response_data = _token_endpoint_request_no_throw(
        request, token_uri, body, access_token=access_token, use_json=use_json
    )
    if not response_status_ok:
        _handle_error_response(response_data)
    return response_data


def jwt_grant(request, token_uri, assertion):
    """Implements the JWT Profile for OAuth 2.0 Authorization Grants.

    For more details, see `rfc7523 section 4`_.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorizations server's token endpoint
            URI.
        assertion (str): The OAuth 2.0 assertion.

    Returns:
        Tuple[str, Optional[datetime], Mapping[str, str]]: The access token,
            expiration, and additional data returned by the token endpoint.

    Raises:
        google.auth.exceptions.RefreshError: If the token endpoint returned
            an error.

    .. _rfc7523 section 4: https://tools.ietf.org/html/rfc7523#section-4
    """
    body = {"assertion": assertion, "grant_type": _JWT_GRANT_TYPE}

    response_data = _token_endpoint_request(request, token_uri, body)

    try:
        access_token = response_data["access_token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError("No access token in response.", response_data)
        raise new_exc from caught_exc

    expiry = _parse_expiry(response_data)

    return access_token, expiry, response_data


def id_token_jwt_grant(request, token_uri, assertion):
    """Implements the JWT Profile for OAuth 2.0 Authorization Grants, but
    requests an OpenID Connect ID Token instead of an access token.

    This is a variant on the standard JWT Profile that is currently unique
    to Google. This was added for the benefit of authenticating to services
    that require ID Tokens instead of access tokens or JWT bearer tokens.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorization server's token endpoint
            URI.
        assertion (str): JWT token signed by a service account. The token's
            payload must include a ``target_audience`` claim.

    Returns:
        Tuple[str, Optional[datetime], Mapping[str, str]]:
            The (encoded) Open ID Connect ID Token, expiration, and additional
            data returned by the endpoint.

    Raises:
        google.auth.exceptions.RefreshError: If the token endpoint returned
            an error.
    """
    body = {"assertion": assertion, "grant_type": _JWT_GRANT_TYPE}

    response_data = _token_endpoint_request(request, token_uri, body)

    try:
        id_token = response_data["id_token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError("No ID token in response.", response_data)
        raise new_exc from caught_exc

    payload = jwt.decode(id_token, verify=False)
    expiry = datetime.datetime.utcfromtimestamp(payload["exp"])

    return id_token, expiry, response_data


def _handle_refresh_grant_response(response_data, refresh_token):
    """Extract tokens from refresh grant response.

    Args:
        response_data (Mapping[str, str]): Refresh grant response data.
        refresh_token (str): Current refresh token.

    Returns:
        Tuple[str, str, Optional[datetime], Mapping[str, str]]: The access token,
            refresh token, expiration, and additional data returned by the token
            endpoint. If response_data doesn't have refresh token, then the current
            refresh token will be returned.

    Raises:
        google.auth.exceptions.RefreshError: If the token endpoint returned
            an error.
    """
    try:
        access_token = response_data["access_token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError("No access token in response.", response_data)
        raise new_exc from caught_exc

    refresh_token = response_data.get("refresh_token", refresh_token)
    expiry = _parse_expiry(response_data)

    return access_token, refresh_token, expiry, response_data


def refresh_grant(
    request,
    token_uri,
    refresh_token,
    client_id,
    client_secret,
    scopes=None,
    rapt_token=None,
):
    """Implements the OAuth 2.0 refresh token grant.

    For more details, see `rfc678 section 6`_.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorizations server's token endpoint
            URI.
        refresh_token (str): The refresh token to use to get a new access
            token.
        client_id (str): The OAuth 2.0 application's client ID.
        client_secret (str): The Oauth 2.0 appliaction's client secret.
        scopes (Optional(Sequence[str])): Scopes to request. If present, all
            scopes must be authorized for the refresh token. Useful if refresh
            token has a wild card scope (e.g.
            'https://www.googleapis.com/auth/any-api').
        rapt_token (Optional(str)): The reauth Proof Token.

    Returns:
        Tuple[str, str, Optional[datetime], Mapping[str, str]]: The access
            token, new or current refresh token, expiration, and additional data
            returned by the token endpoint.

    Raises:
        google.auth.exceptions.RefreshError: If the token endpoint returned
            an error.

    .. _rfc6748 section 6: https://tools.ietf.org/html/rfc6749#section-6
    """
    body = {
        "grant_type": _REFRESH_GRANT_TYPE,
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    if scopes:
        body["scope"] = " ".join(scopes)
    if rapt_token:
        body["rapt"] = rapt_token

    response_data = _token_endpoint_request(request, token_uri, body)
    return _handle_refresh_grant_response(response_data, refresh_token)
