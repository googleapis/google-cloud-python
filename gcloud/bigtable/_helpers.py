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

"""Utility methods for gcloud Bigtable.

Primarily includes helpers for dealing with low-level
protobuf objects.
"""


from grpc.beta import implementations


class MetadataPlugin(object):
    """Callable class to transform metadata for gRPC requests.

    :type client: :class:`.client.Client`
    :param client: The client that owns the cluster. Provides authorization and
                   user agent.
    """

    def __init__(self, client):
        self._credentials = client.credentials
        self._user_agent = client.user_agent

    def __call__(self, unused_context, callback):
        """Adds authorization header to request metadata."""
        access_token = self._credentials.get_access_token().access_token
        headers = [
            ('Authorization', 'Bearer ' + access_token),
            ('User-agent', self._user_agent),
        ]
        callback(headers, None)


def make_stub(client, stub_factory, host, port):
    """Makes a stub for an RPC service.

    Uses / depends on the beta implementation of gRPC.

    :type client: :class:`.client.Client`
    :param client: The client that owns the cluster. Provides authorization and
                   user agent.

    :type stub_factory: callable
    :param stub_factory: A factory which will create a gRPC stub for
                         a given service.

    :type host: str
    :param host: The host for the service.

    :type port: int
    :param port: The port for the service.

    :rtype: :class:`grpc.beta._stub._AutoIntermediary`
    :returns: The stub object used to make gRPC requests to a given API.
    """
    # Leaving the first argument to ssl_channel_credentials() as None
    # loads root certificates from `grpc/_adapter/credentials/roots.pem`.
    transport_creds = implementations.ssl_channel_credentials(None, None, None)
    custom_metadata_plugin = MetadataPlugin(client)
    auth_creds = implementations.metadata_call_credentials(
        custom_metadata_plugin, name='google_creds')
    channel_creds = implementations.composite_channel_credentials(
        transport_creds, auth_creds)
    channel = implementations.secure_channel(host, port, channel_creds)
    return stub_factory(channel)
