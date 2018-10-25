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

"""Helpers for making API requests via gapic / gRPC."""

from google.api_core.gapic_v1 import client_info
from google.cloud.datastore_v1.gapic import datastore_client
from grpc import insecure_channel
import six

from google.cloud._helpers import make_secure_channel
from google.cloud._http import DEFAULT_USER_AGENT

from google.cloud.datastore import __version__


def make_datastore_api(client):
    """Create an instance of the GAPIC Datastore API.

    :type client: :class:`~google.cloud.datastore.client.Client`
    :param client: The client that holds configuration details.

    :rtype: :class:`.datastore.v1.datastore_client.DatastoreClient`
    :returns: A datastore API instance with the proper credentials.
    """
    parse_result = six.moves.urllib_parse.urlparse(
        client._base_url)
    host = parse_result.netloc
    if parse_result.scheme == 'https':
        channel = make_secure_channel(
            client._credentials, DEFAULT_USER_AGENT, host)
    else:
        channel = insecure_channel(host)

    return datastore_client.DatastoreClient(
        channel=channel,
        client_info=client_info.ClientInfo(
            client_library_version=__version__,
            gapic_version=__version__,
        ),
    )
