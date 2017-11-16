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

"""Connections to Google Cloud Datastore API servers."""

from google.rpc import status_pb2

from google.cloud import _http as connection_module
from google.cloud import exceptions
from google.cloud.datastore_v1.proto import datastore_pb2 as _datastore_pb2

from google.cloud.datastore import __version__


DATASTORE_API_HOST = 'datastore.googleapis.com'
"""Datastore API request host."""
API_BASE_URL = 'https://' + DATASTORE_API_HOST
"""The base of the API call URL."""
API_VERSION = 'v1'
"""The version of the API, used in building the API call's URL."""
API_URL_TEMPLATE = ('{api_base}/{api_version}/projects'
                    '/{project}:{method}')
"""A template for the URL of a particular API call."""

_CLIENT_INFO = connection_module.CLIENT_INFO_TEMPLATE.format(__version__)


def _request(http, project, method, data, base_url):
    """Make a request over the Http transport to the Cloud Datastore API.

    :type http: :class:`requests.Session`
    :param http: HTTP object to make requests.

    :type project: str
    :param project: The project to make the request for.

    :type method: str
    :param method: The API call method name (ie, ``runQuery``,
                   ``lookup``, etc)

    :type data: str
    :param data: The data to send with the API call.
                 Typically this is a serialized Protobuf string.

    :type base_url: str
    :param base_url: The base URL where the API lives.

    :rtype: str
    :returns: The string response content from the API call.
    :raises: :class:`google.cloud.exceptions.GoogleCloudError` if the
             response code is not 200 OK.
    """
    headers = {
        'Content-Type': 'application/x-protobuf',
        'User-Agent': connection_module.DEFAULT_USER_AGENT,
        connection_module.CLIENT_INFO_HEADER: _CLIENT_INFO,
    }
    api_url = build_api_url(project, method, base_url)

    response = http.request(
        url=api_url, method='POST', headers=headers, data=data)

    if response.status_code != 200:
        error_status = status_pb2.Status.FromString(response.content)
        raise exceptions.from_http_status(
            response.status_code, error_status.message, errors=[error_status])

    return response.content


def _rpc(http, project, method, base_url, request_pb, response_pb_cls):
    """Make a protobuf RPC request.

    :type http: :class:`requests.Session`
    :param http: HTTP object to make requests.

    :type project: str
    :param project: The project to connect to. This is
                    usually your project name in the cloud console.

    :type method: str
    :param method: The name of the method to invoke.

    :type base_url: str
    :param base_url: The base URL where the API lives.

    :type request_pb: :class:`google.protobuf.message.Message` instance
    :param request_pb: the protobuf instance representing the request.

    :type response_pb_cls: A :class:`google.protobuf.message.Message`
                           subclass.
    :param response_pb_cls: The class used to unmarshall the response
                            protobuf.

    :rtype: :class:`google.protobuf.message.Message`
    :returns: The RPC message parsed from the response.
    """
    req_data = request_pb.SerializeToString()
    response = _request(
        http, project, method, req_data, base_url)
    return response_pb_cls.FromString(response)


def build_api_url(project, method, base_url):
    """Construct the URL for a particular API call.

    This method is used internally to come up with the URL to use when
    making RPCs to the Cloud Datastore API.

    :type project: str
    :param project: The project to connect to. This is
                    usually your project name in the cloud console.

    :type method: str
    :param method: The API method to call (e.g. 'runQuery', 'lookup').

    :type base_url: str
    :param base_url: The base URL where the API lives.

    :rtype: str
    :returns: The API URL created.
    """
    return API_URL_TEMPLATE.format(
        api_base=base_url, api_version=API_VERSION,
        project=project, method=method)


class HTTPDatastoreAPI(object):
    """An API object that sends proto-over-HTTP requests.

    Intended to provide the same methods as the GAPIC ``DatastoreClient``.

    :type client: :class:`~google.cloud.datastore.client.Client`
    :param client: The client that provides configuration.
    """

    def __init__(self, client):
        self.client = client

    def lookup(self, project_id, keys, read_options=None):
        """Perform a ``lookup`` request.

        :type project_id: str
        :param project_id: The project to connect to. This is
                           usually your project name in the cloud console.

        :type keys: List[.entity_pb2.Key]
        :param keys: The keys to retrieve from the datastore.

        :type read_options: :class:`.datastore_pb2.ReadOptions`
        :param read_options: (Optional) The options for this lookup. Contains
                             either the transaction for the read or
                             ``STRONG`` or ``EVENTUAL`` read consistency.

        :rtype: :class:`.datastore_pb2.LookupResponse`
        :returns: The returned protobuf response object.
        """
        request_pb = _datastore_pb2.LookupRequest(
            project_id=project_id,
            read_options=read_options,
            keys=keys,
        )
        return _rpc(self.client._http, project_id, 'lookup',
                    self.client._base_url,
                    request_pb, _datastore_pb2.LookupResponse)

    def run_query(self, project_id, partition_id, read_options=None,
                  query=None, gql_query=None):
        """Perform a ``runQuery`` request.

        :type project_id: str
        :param project_id: The project to connect to. This is
                           usually your project name in the cloud console.

        :type partition_id: :class:`.entity_pb2.PartitionId`
        :param partition_id: Partition ID corresponding to an optional
                             namespace and project ID.

        :type read_options: :class:`.datastore_pb2.ReadOptions`
        :param read_options: (Optional) The options for this query. Contains
                             either the transaction for the read or
                             ``STRONG`` or ``EVENTUAL`` read consistency.

        :type query: :class:`.query_pb2.Query`
        :param query: (Optional) The query protobuf to run. At most one of
                      ``query`` and ``gql_query`` can be specified.

        :type gql_query: :class:`.query_pb2.GqlQuery`
        :param gql_query: (Optional) The GQL query to run. At most one of
                          ``query`` and ``gql_query`` can be specified.

        :rtype: :class:`.datastore_pb2.RunQueryResponse`
        :returns: The returned protobuf response object.
        """
        request_pb = _datastore_pb2.RunQueryRequest(
            project_id=project_id,
            partition_id=partition_id,
            read_options=read_options,
            query=query,
            gql_query=gql_query,
        )
        return _rpc(self.client._http, project_id, 'runQuery',
                    self.client._base_url,
                    request_pb, _datastore_pb2.RunQueryResponse)

    def begin_transaction(self, project_id, transaction_options=None):
        """Perform a ``beginTransaction`` request.

        :type project_id: str
        :param project_id: The project to connect to. This is
                           usually your project name in the cloud console.

        :type transaction_options: ~.datastore_v1.types.TransactionOptions
        :param transaction_options: (Optional) Options for a new transaction.

        :rtype: :class:`.datastore_pb2.BeginTransactionResponse`
        :returns: The returned protobuf response object.
        """
        request_pb = _datastore_pb2.BeginTransactionRequest()
        return _rpc(self.client._http, project_id, 'beginTransaction',
                    self.client._base_url,
                    request_pb, _datastore_pb2.BeginTransactionResponse)

    def commit(self, project_id, mode, mutations, transaction=None):
        """Perform a ``commit`` request.

        :type project_id: str
        :param project_id: The project to connect to. This is
                           usually your project name in the cloud console.

        :type mode: :class:`.gapic.datastore.v1.enums.CommitRequest.Mode`
        :param mode: The type of commit to perform. Expected to be one of
                     ``TRANSACTIONAL`` or ``NON_TRANSACTIONAL``.

        :type mutations: list
        :param mutations: List of :class:`.datastore_pb2.Mutation`, the
                          mutations to perform.

        :type transaction: bytes
        :param transaction: (Optional) The transaction ID returned from
                            :meth:`begin_transaction`.  Non-transactional
                            commits must pass :data:`None`.

        :rtype: :class:`.datastore_pb2.CommitResponse`
        :returns: The returned protobuf response object.
        """
        request_pb = _datastore_pb2.CommitRequest(
            project_id=project_id,
            mode=mode,
            transaction=transaction,
            mutations=mutations,
        )
        return _rpc(self.client._http, project_id, 'commit',
                    self.client._base_url,
                    request_pb, _datastore_pb2.CommitResponse)

    def rollback(self, project_id, transaction):
        """Perform a ``rollback`` request.

        :type project_id: str
        :param project_id: The project to connect to. This is
                           usually your project name in the cloud console.

        :type transaction: bytes
        :param transaction: The transaction ID to rollback.

        :rtype: :class:`.datastore_pb2.RollbackResponse`
        :returns: The returned protobuf response object.
        """
        request_pb = _datastore_pb2.RollbackRequest(
            project_id=project_id,
            transaction=transaction,
        )
        # Response is empty (i.e. no fields) but we return it anyway.
        return _rpc(self.client._http, project_id, 'rollback',
                    self.client._base_url,
                    request_pb, _datastore_pb2.RollbackResponse)

    def allocate_ids(self, project_id, keys):
        """Perform an ``allocateIds`` request.

        :type project_id: str
        :param project_id: The project to connect to. This is
                           usually your project name in the cloud console.

        :type keys: List[.entity_pb2.Key]
        :param keys: The keys for which the backend should allocate IDs.

        :rtype: :class:`.datastore_pb2.AllocateIdsResponse`
        :returns: The returned protobuf response object.
        """
        request_pb = _datastore_pb2.AllocateIdsRequest(keys=keys)
        return _rpc(self.client._http, project_id, 'allocateIds',
                    self.client._base_url,
                    request_pb, _datastore_pb2.AllocateIdsResponse)
