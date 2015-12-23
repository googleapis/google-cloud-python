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


import platform

from grpc.beta import implementations


# See https://gist.github.com/dhermes/bbc5b7be1932bfffae77
# for appropriate values on other systems.
_PLAT_SYS = platform.system()
SSL_CERT_FILE = None
if _PLAT_SYS == 'Linux':
    SSL_CERT_FILE = '/etc/ssl/certs/ca-certificates.crt'
elif _PLAT_SYS == 'Darwin':  # pragma: NO COVER
    SSL_CERT_FILE = '/usr/local/etc/openssl/cert.pem'


class MetadataTransformer(object):
    """Callable class to transform metadata for gRPC requests.

    :type client: :class:`.client.Client`
    :param client: The client that owns the cluster. Provides authorization and
                   user agent.
    """

    def __init__(self, client):
        self._credentials = client.credentials
        self._user_agent = client.user_agent

    def __call__(self, ignored_val):
        """Adds authorization header to request metadata."""
        access_token = self._credentials.get_access_token().access_token
        return [
            ('Authorization', 'Bearer ' + access_token),
            ('User-agent', self._user_agent),
        ]


def get_certs():
    """Gets the root certificates.

    .. note::

        This is only called by :func:`make_stub`. For most applications,
        a few gRPC stubs (four total, one for each service) will be created
        when a :class:`.Client` is created. This function will not likely
        be used again while that application is running.

        However, it may be worthwhile to cache the output of this function.

    :rtype: str
    :returns: The root certificates for the current machine.
    """
    with open(SSL_CERT_FILE, mode='rb') as file_obj:
        return file_obj.read()


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
    root_certificates = get_certs()
    client_credentials = implementations.ssl_client_credentials(
        root_certificates, private_key=None, certificate_chain=None)
    channel = implementations.secure_channel(
        host, port, client_credentials)
    custom_metadata_transformer = MetadataTransformer(client)
    return stub_factory(channel,
                        metadata_transformer=custom_metadata_transformer)
