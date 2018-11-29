# Copyright 2014 Google LLC
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

"""Shared implementation of connections to API servers."""

import json
import platform

from pkg_resources import get_distribution
from six.moves.urllib.parse import urlencode

from google.cloud import exceptions


API_BASE_URL = "https://www.googleapis.com"
"""The base of the API call URL."""

DEFAULT_USER_AGENT = "gcloud-python/{0}".format(
    get_distribution("google-cloud-core").version
)
"""The user agent for google-cloud-python requests."""

CLIENT_INFO_HEADER = "X-Goog-API-Client"
CLIENT_INFO_TEMPLATE = "gl-python/" + platform.python_version() + " gccl/{}"


class Connection(object):
    """A generic connection to Google Cloud Platform.

    :type client: :class:`~google.cloud.client.Client`
    :param client: The client that owns the current connection.
    """

    USER_AGENT = DEFAULT_USER_AGENT
    _EXTRA_HEADERS = {}
    """Headers to be sent with every request.

    Intended to be over-ridden by subclasses.
    """

    def __init__(self, client):
        self._client = client

    @property
    def credentials(self):
        """Getter for current credentials.

        :rtype: :class:`google.auth.credentials.Credentials` or
                :class:`NoneType`
        :returns: The credentials object associated with this connection.
        """
        return self._client._credentials

    @property
    def http(self):
        """A getter for the HTTP transport used in talking to the API.

        Returns:
            google.auth.transport.requests.AuthorizedSession:
                A :class:`requests.Session` instance.
        """
        return self._client._http


class JSONConnection(Connection):
    """A connection to a Google JSON-based API.

    These APIs are discovery based. For reference:

        https://developers.google.com/discovery/

    This defines :meth:`api_request` for making a generic JSON
    API request and API requests are created elsewhere.

    The class constants

    * :attr:`API_BASE_URL`
    * :attr:`API_VERSION`
    * :attr:`API_URL_TEMPLATE`

    must be updated by subclasses.
    """

    API_BASE_URL = None
    """The base of the API call URL."""

    API_VERSION = None
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = None
    """A template for the URL of a particular API call."""

    @classmethod
    def build_api_url(
        cls, path, query_params=None, api_base_url=None, api_version=None
    ):
        """Construct an API url given a few components, some optional.

        Typically, you shouldn't need to use this method.

        :type path: str
        :param path: The path to the resource (ie, ``'/b/bucket-name'``).

        :type query_params: dict or list
        :param query_params: A dictionary of keys and values (or list of
                             key-value pairs) to insert into the query
                             string of the URL.

        :type api_base_url: str
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.

        :type api_version: str
        :param api_version: The version of the API to call.
                            Typically you shouldn't provide this and instead
                            use the default for the library.

        :rtype: str
        :returns: The URL assembled from the pieces provided.
        """
        url = cls.API_URL_TEMPLATE.format(
            api_base_url=(api_base_url or cls.API_BASE_URL),
            api_version=(api_version or cls.API_VERSION),
            path=path,
        )

        query_params = query_params or {}
        if query_params:
            url += "?" + urlencode(query_params, doseq=True)

        return url

    def _make_request(
        self,
        method,
        url,
        data=None,
        content_type=None,
        headers=None,
        target_object=None,
    ):
        """A low level method to send a request to the API.

        Typically, you shouldn't need to use this method.

        :type method: str
        :param method: The HTTP method to use in the request.

        :type url: str
        :param url: The URL to send the request to.

        :type data: str
        :param data: The data to send as the body of the request.

        :type content_type: str
        :param content_type: The proper MIME type of the data provided.

        :type headers: dict
        :param headers: (Optional) A dictionary of HTTP headers to send with
                        the request. If passed, will be modified directly
                        here with added headers.

        :type target_object: object
        :param target_object:
            (Optional) Argument to be used by library callers.  This can allow
            custom behavior, for example, to defer an HTTP request and complete
            initialization of the object at a later time.

        :rtype: :class:`requests.Response`
        :returns: The HTTP response.
        """
        headers = headers or {}
        headers.update(self._EXTRA_HEADERS)
        headers["Accept-Encoding"] = "gzip"

        if content_type:
            headers["Content-Type"] = content_type

        headers["User-Agent"] = self.USER_AGENT

        return self._do_request(method, url, headers, data, target_object)

    def _do_request(
        self, method, url, headers, data, target_object
    ):  # pylint: disable=unused-argument
        """Low-level helper:  perform the actual API request over HTTP.

        Allows batch context managers to override and defer a request.

        :type method: str
        :param method: The HTTP method to use in the request.

        :type url: str
        :param url: The URL to send the request to.

        :type headers: dict
        :param headers: A dictionary of HTTP headers to send with the request.

        :type data: str
        :param data: The data to send as the body of the request.

        :type target_object: object
        :param target_object:
            (Optional) Unused ``target_object`` here but may be used by a
            superclass.

        :rtype: :class:`requests.Response`
        :returns: The HTTP response.
        """
        return self.http.request(url=url, method=method, headers=headers, data=data)

    def api_request(
        self,
        method,
        path,
        query_params=None,
        data=None,
        content_type=None,
        headers=None,
        api_base_url=None,
        api_version=None,
        expect_json=True,
        _target_object=None,
    ):
        """Make a request over the HTTP transport to the API.

        You shouldn't need to use this method, but if you plan to
        interact with the API using these primitives, this is the
        correct one to use.

        :type method: str
        :param method: The HTTP method name (ie, ``GET``, ``POST``, etc).
                       Required.

        :type path: str
        :param path: The path to the resource (ie, ``'/b/bucket-name'``).
                     Required.

        :type query_params: dict or list
        :param query_params: A dictionary of keys and values (or list of
                             key-value pairs) to insert into the query
                             string of the URL.

        :type data: str
        :param data: The data to send as the body of the request. Default is
                     the empty string.

        :type content_type: str
        :param content_type: The proper MIME type of the data provided. Default
                             is None.

        :type headers: dict
        :param headers: extra HTTP headers to be sent with the request.

        :type api_base_url: str
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.
                             Default is the standard API base URL.

        :type api_version: str
        :param api_version: The version of the API to call.  Typically
                            you shouldn't provide this and instead use
                            the default for the library.  Default is the
                            latest API version supported by
                            google-cloud-python.

        :type expect_json: bool
        :param expect_json: If True, this method will try to parse the
                            response as JSON and raise an exception if
                            that cannot be done.  Default is True.

        :type _target_object: :class:`object`
        :param _target_object:
            (Optional) Protected argument to be used by library callers. This
            can allow custom behavior, for example, to defer an HTTP request
            and complete initialization of the object at a later time.

        :raises ~google.cloud.exceptions.GoogleCloudError: if the response code
            is not 200 OK.
        :raises ValueError: if the response content type is not JSON.
        :rtype: dict or str
        :returns: The API response payload, either as a raw string or
                  a dictionary if the response is valid JSON.
        """
        url = self.build_api_url(
            path=path,
            query_params=query_params,
            api_base_url=api_base_url,
            api_version=api_version,
        )

        # Making the executive decision that any dictionary
        # data will be sent properly as JSON.
        if data and isinstance(data, dict):
            data = json.dumps(data)
            content_type = "application/json"

        response = self._make_request(
            method=method,
            url=url,
            data=data,
            content_type=content_type,
            headers=headers,
            target_object=_target_object,
        )

        if not 200 <= response.status_code < 300:
            raise exceptions.from_http_response(response)

        if expect_json and response.content:
            return response.json()
        else:
            return response.content
