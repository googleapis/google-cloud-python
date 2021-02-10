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

"""Create / interact with Google Cloud Storage connections."""

import functools
import os
import pkg_resources

from google.cloud import _http

from google.cloud.storage import __version__


if os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE") == "true":  # pragma: NO COVER
    release = pkg_resources.get_distribution("google-cloud-core").parsed_version
    if release < pkg_resources.parse_version("1.6.0"):
        raise ImportError("google-cloud-core >= 1.6.0 is required to use mTLS feature")


class Connection(_http.JSONConnection):
    """A connection to Google Cloud Storage via the JSON REST API. Mutual TLS feature will be
    enabled if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is set to "true".

    :type client: :class:`~google.cloud.storage.client.Client`
    :param client: The client that owns the current connection.

    :type client_info: :class:`~google.api_core.client_info.ClientInfo`
    :param client_info: (Optional) instance used to generate user agent.

    :type api_endpoint: str
    :param api_endpoint: (Optional) api endpoint to use.
    """

    DEFAULT_API_ENDPOINT = "https://storage.googleapis.com"
    DEFAULT_API_MTLS_ENDPOINT = "https://storage.mtls.googleapis.com"

    def __init__(self, client, client_info=None, api_endpoint=None):
        super(Connection, self).__init__(client, client_info)
        self.API_BASE_URL = api_endpoint or self.DEFAULT_API_ENDPOINT
        self.API_BASE_MTLS_URL = self.DEFAULT_API_MTLS_ENDPOINT
        self.ALLOW_AUTO_SWITCH_TO_MTLS_URL = api_endpoint is None
        self._client_info.client_library_version = __version__

        # TODO: When metrics all use gccl, this should be removed #9552
        if self._client_info.user_agent is None:  # pragma: no branch
            self._client_info.user_agent = ""
        self._client_info.user_agent += " gcloud-python/{} ".format(__version__)

    API_VERSION = "v1"
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = "{api_base_url}/storage/{api_version}{path}"
    """A template for the URL of a particular API call."""

    def api_request(self, *args, **kwargs):
        retry = kwargs.pop("retry", None)
        call = functools.partial(super(Connection, self).api_request, *args, **kwargs)
        if retry:
            # If this is a ConditionalRetryPolicy, check conditions.
            try:
                retry = retry.get_retry_policy_if_conditions_met(**kwargs)
            except AttributeError:  # This is not a ConditionalRetryPolicy.
                pass
            if retry:
                call = retry(call)
        return call()
