# Copyright 2015 Google Inc. All rights reserved.
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

"""Create / interact with gcloud pubsub connections."""

import json

from six.moves.urllib.parse import urlencode  # pylint: disable=F0401

from gcloud import connection as base_connection
from gcloud.exceptions import make_exception


class Connection(base_connection.Connection):
    """A connection to Google Cloud Pubsub via the JSON REST API.

    This defines :meth:`Connection.api_request` for making a generic JSON
    API request and API requests are created elsewhere (e.g. in
    :mod:`gcloud.pubsub.api`).
    """

    API_BASE_URL = base_connection.API_BASE_URL
    """The base of the API call URL."""

    API_VERSION = 'v1beta2'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/pubsub/{api_version}{path}'
    """A template for the URL of a particular API call."""

    @classmethod
    def build_api_url(cls, path, query_params=None, api_base_url=None,
                      api_version=None):
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
                      headers=None):
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

        return self._do_request(method, url, headers, data)

    def _do_request(self, method, url, headers, data):
        """Low-level helper:  perform the actual API request over HTTP.

        Allows :class:`gcloud.pubsub.batch.Batch` to override, deferring
        the request.

        :type method: string
        :param method: The HTTP method to use in the request.

        :type url: string
        :param url: The URL to send the request to.

        :type headers: dict
        :param headers: A dictionary of HTTP headers to send with the request.

        :type data: string
        :param data: The data to send as the body of the request.

        :rtype: tuple of ``response`` (a dictionary of sorts)
                and ``content`` (a string).
        :returns: The HTTP response object and the content of the response.
        """
        return self.http.request(uri=url, method=method, headers=headers,
                                 body=data)

    def api_request(self, method, path, query_params=None,
                    data=None, content_type=None,
                    api_base_url=None, api_version=None,
                    expect_json=True):
        """Make a request over the HTTP transport to the Cloud Storage API.

        You shouldn't need to use this method, but if you plan to
        interact with the API using these primitives, this is the
        correct one to use...

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
            method=method, url=url, data=data, content_type=content_type)

        if not 200 <= response.status < 300:
            raise make_exception(response, content)

        if content and expect_json:
            content_type = response.get('content-type', '')
            if not content_type.startswith('application/json'):
                raise TypeError('Expected JSON, got %s' % content_type)
            return json.loads(content)

        return content
