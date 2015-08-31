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

"""Shared implementation of connections to API servers."""

import json
from pkg_resources import get_distribution
import six
from six.moves.urllib.parse import urlencode  # pylint: disable=F0401

import httplib2

from gcloud.exceptions import make_exception


API_BASE_URL = 'https://www.googleapis.com'
"""The base of the API call URL."""


class Connection(object):
    """A generic connection to Google Cloud Platform.

    Subclasses should understand only the basic types in method arguments,
    however they should be capable of returning advanced types.

    If no value is passed in for ``http``, a :class:`httplib2.Http` object
    will be created and authorized with the ``credentials``. If not, the
    ``credentials`` and ``http`` need not be related.

    Subclasses may seek to use the private key from ``credentials`` to sign
    data.

    A custom (non-``httplib2``) HTTP object must have a ``request`` method
    which accepts the following arguments:

    * ``uri``
    * ``method``
    * ``body``
    * ``headers``

    In addition, ``redirections`` and ``connection_type`` may be used.

    Without the use of ``credentials.authorize(http)``, a custom ``http``
    object will also need to be able to add a bearer token to API
    requests and handle token refresh on 401 errors.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for this connection.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests.
    """

    USER_AGENT = "gcloud-python/{0}".format(get_distribution('gcloud').version)
    """The user agent for gcloud-python requests."""

    SCOPE = None
    """The scopes required for authenticating with a service.

    Needs to be set by subclasses.
    """

    def __init__(self, credentials=None, http=None):
        self._http = http
        self._credentials = self._create_scoped_credentials(
            credentials, self.SCOPE)

    @property
    def credentials(self):
        """Getter for current credentials.

        :rtype: :class:`oauth2client.client.OAuth2Credentials` or
                :class:`NoneType`
        :returns: The credentials object associated with this connection.
        """
        return self._credentials

    @property
    def http(self):
        """A getter for the HTTP transport used in talking to the API.

        :rtype: :class:`httplib2.Http`
        :returns: A Http object used to transport data.
        """
        if self._http is None:
            self._http = httplib2.Http()
            if self._credentials:
                self._http = self._credentials.authorize(self._http)
        return self._http

    @staticmethod
    def _create_scoped_credentials(credentials, scope):
        """Create a scoped set of credentials if it is required.

        :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                           :class:`NoneType`
        :param credentials: The OAuth2 Credentials to add a scope to.

        :type scope: list of URLs
        :param scope: the effective service auth scopes for the connection.

        :rtype: :class:`oauth2client.client.OAuth2Credentials` or
                :class:`NoneType`
        :returns: A new credentials object that has a scope added (if needed).
        """
        if credentials and credentials.create_scoped_required():
            credentials = credentials.create_scoped(scope)
        return credentials


class JSONConnection(Connection):
    """A connection to a Google JSON-based API.

    These APIs are discovery based. For reference:
        https://developers.google.com/discovery/

    This defines :meth:`Connection.api_request` for making a generic JSON
    API request and API requests are created elsewhere.

    The class constants
    * ``API_BASE_URL``
    * ``API_VERSION``
    * ``API_URL_TEMPLATE``
    must be updated by subclasses.
    """

    API_BASE_URL = None
    """The base of the API call URL."""

    API_VERSION = None
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = None
    """A template for the URL of a particular API call."""

    @classmethod
    def build_api_url(cls, path, query_params=None,
                      api_base_url=None, api_version=None):
        """Construct an API url given a few components, some optional.

        Typically, you shouldn't need to use this method.

        :type path: string
        :param path: The path to the resource (ie, ``'/b/bucket-name'``).

        :type query_params: dict
        :param query_params: A dictionary of keys and values to insert into
                             the query string of the URL.

        :type api_base_url: string
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.

        :type api_version: string
        :param api_version: The version of the API to call.
                            Typically you shouldn't provide this and instead
                            use the default for the library.

        :rtype: string
        :returns: The URL assembled from the pieces provided.
        """
        api_base_url = api_base_url or cls.API_BASE_URL

        url = cls.API_URL_TEMPLATE.format(
            api_base_url=(api_base_url or cls.API_BASE_URL),
            api_version=(api_version or cls.API_VERSION),
            path=path)

        query_params = query_params or {}
        if query_params:
            url += '?' + urlencode(query_params)

        return url

    def _make_request(self, method, url, data=None, content_type=None,
                      headers=None, target_object=None):
        """A low level method to send a request to the API.

        Typically, you shouldn't need to use this method.

        :type method: string
        :param method: The HTTP method to use in the request.

        :type url: string
        :param url: The URL to send the request to.

        :type data: string
        :param data: The data to send as the body of the request.

        :type content_type: string
        :param content_type: The proper MIME type of the data provided.

        :type headers: dict
        :param headers: A dictionary of HTTP headers to send with the request.

        :type target_object: object or :class:`NoneType`
        :param target_object: Argument to be used by library callers.
                              This can allow custom behavior, for example, to
                              defer an HTTP request and complete initialization
                              of the object at a later time.

        :rtype: tuple of ``response`` (a dictionary of sorts)
                and ``content`` (a string).
        :returns: The HTTP response object and the content of the response,
                  returned by :meth:`_do_request`.
        """
        headers = headers or {}
        headers['Accept-Encoding'] = 'gzip'

        if data:
            content_length = len(str(data))
        else:
            content_length = 0

        headers['Content-Length'] = content_length

        if content_type:
            headers['Content-Type'] = content_type

        headers['User-Agent'] = self.USER_AGENT

        return self._do_request(method, url, headers, data, target_object)

    def _do_request(self, method, url, headers, data,
                    target_object):  # pylint: disable=unused-argument
        """Low-level helper:  perform the actual API request over HTTP.

        Allows batch context managers to override and defer a request.

        :type method: string
        :param method: The HTTP method to use in the request.

        :type url: string
        :param url: The URL to send the request to.

        :type headers: dict
        :param headers: A dictionary of HTTP headers to send with the request.

        :type data: string
        :param data: The data to send as the body of the request.

        :type target_object: object or :class:`NoneType`
        :param target_object: Unused ``target_object`` here but may be used
                              by a superclass.

        :rtype: tuple of ``response`` (a dictionary of sorts)
                and ``content`` (a string).
        :returns: The HTTP response object and the content of the response.
        """
        return self.http.request(uri=url, method=method, headers=headers,
                                 body=data)

    def api_request(self, method, path, query_params=None,
                    data=None, content_type=None,
                    api_base_url=None, api_version=None,
                    expect_json=True, _target_object=None):
        """Make a request over the HTTP transport to the API.

        You shouldn't need to use this method, but if you plan to
        interact with the API using these primitives, this is the
        correct one to use.

        :type method: string
        :param method: The HTTP method name (ie, ``GET``, ``POST``, etc).
                       Required.

        :type path: string
        :param path: The path to the resource (ie, ``'/b/bucket-name'``).
                     Required.

        :type query_params: dict
        :param query_params: A dictionary of keys and values to insert into
                             the query string of the URL.  Default is
                             empty dict.

        :type data: string
        :param data: The data to send as the body of the request. Default is
                     the empty string.

        :type content_type: string
        :param content_type: The proper MIME type of the data provided. Default
                             is None.

        :type api_base_url: string
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.
                             Default is the standard API base URL.

        :type api_version: string
        :param api_version: The version of the API to call.  Typically
                            you shouldn't provide this and instead use
                            the default for the library.  Default is the
                            latest API version supported by
                            gcloud-python.

        :type expect_json: boolean
        :param expect_json: If True, this method will try to parse the
                            response as JSON and raise an exception if
                            that cannot be done.  Default is True.

        :type _target_object: object or :class:`NoneType`
        :param _target_object: Protected argument to be used by library
                               callers. This can allow custom behavior, for
                               example, to defer an HTTP request and complete
                               initialization of the object at a later time.

        :raises: Exception if the response code is not 200 OK.
        """
        url = self.build_api_url(path=path, query_params=query_params,
                                 api_base_url=api_base_url,
                                 api_version=api_version)

        # Making the executive decision that any dictionary
        # data will be sent properly as JSON.
        if data and isinstance(data, dict):
            data = json.dumps(data)
            content_type = 'application/json'

        response, content = self._make_request(
            method=method, url=url, data=data, content_type=content_type,
            target_object=_target_object)

        if not 200 <= response.status < 300:
            raise make_exception(response, content,
                                 error_info=method + ' ' + url)

        string_or_bytes = (six.binary_type, six.text_type)
        if content and expect_json and isinstance(content, string_or_bytes):
            content_type = response.get('content-type', '')
            if not content_type.startswith('application/json'):
                raise TypeError('Expected JSON, got %s' % content_type)
            if isinstance(content, six.binary_type):
                content = content.decode('utf-8')
            return json.loads(content)

        return content
