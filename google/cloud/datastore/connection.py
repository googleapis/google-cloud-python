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

"""Connections to Google Cloud Datastore API servers."""

import os

from google.cloud import connection as connection_module
from google.cloud.environment_vars import GCD_HOST
from google.cloud.datastore._generated import datastore_pb2 as _datastore_pb2
from google.cloud.datastore._api import _add_keys_to_request
from google.cloud.datastore._api import _DatastoreAPIOverGRPC
from google.cloud.datastore._api import _DatastoreAPIOverHttp
from google.cloud.datastore._api import USE_GRPC as _USE_GRPC


DATASTORE_API_HOST = 'datastore.googleapis.com'
"""Datastore API request host."""


class Connection(connection_module.Connection):
    """A connection to the Google Cloud Datastore via the Protobuf API.

    This class should understand only the basic types (and protobufs)
    in method arguments, however it should be capable of returning advanced
    types.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: The OAuth2 Credentials to use for this connection.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests.
    """

    API_BASE_URL = 'https://' + DATASTORE_API_HOST
    """The base of the API call URL."""

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = ('{api_base}/{api_version}/projects'
                        '/{project}:{method}')
    """A template for the URL of a particular API call."""

    SCOPE = ('https://www.googleapis.com/auth/datastore',)
    """The scopes required for authenticating as a Cloud Datastore consumer."""

    def __init__(self, credentials=None, http=None):
        super(Connection, self).__init__(credentials=credentials, http=http)
        try:
            self.host = os.environ[GCD_HOST]
            self.api_base_url = 'http://' + self.host
            secure = False
        except KeyError:
            self.host = DATASTORE_API_HOST
            self.api_base_url = self.__class__.API_BASE_URL
            secure = True
        if _USE_GRPC:
            self._datastore_api = _DatastoreAPIOverGRPC(self, secure=secure)
        else:
            self._datastore_api = _DatastoreAPIOverHttp(self)

    def lookup(self, project, key_pbs,
               eventual=False, transaction_id=None):
        """Lookup keys from a project in the Cloud Datastore.

        Maps the ``DatastoreService.Lookup`` protobuf RPC.

        This uses mostly protobufs
        (:class:`google.cloud.datastore._generated.entity_pb2.Key` as input
        and :class:`google.cloud.datastore._generated.entity_pb2.Entity`
        as output). It is used under the hood in
        :meth:`Client.get() <.datastore.client.Client.get>`:

        >>> from google.cloud import datastore
        >>> client = datastore.Client(project='project')
        >>> key = client.key('MyKind', 1234)
        >>> client.get(key)
        [<Entity object>]

        Using a :class:`Connection` directly:

        >>> connection.lookup('project', [key.to_protobuf()])
        [<Entity protobuf>]

        :type project: string
        :param project: The project to look up the keys in.

        :type key_pbs: list of
                       :class:`google.cloud.datastore._generated.entity_pb2.Key`
        :param key_pbs: The keys to retrieve from the datastore.

        :type eventual: bool
        :param eventual: If False (the default), request ``STRONG`` read
                         consistency.  If True, request ``EVENTUAL`` read
                         consistency.

        :type transaction_id: string
        :param transaction_id: If passed, make the request in the scope of
                               the given transaction.  Incompatible with
                               ``eventual==True``.

        :rtype: tuple
        :returns: A triple of (``results``, ``missing``, ``deferred``) where
                  both ``results`` and ``missing`` are lists of
                  :class:`google.cloud.datastore._generated.entity_pb2.Entity`
                  and ``deferred`` is a list of
                  :class:`google.cloud.datastore._generated.entity_pb2.Key`.
        """
        return self._datastore_api.lookup(project, key_pbs, eventual=eventual,
                                          transaction_id=transaction_id)

    def run_query(self, project, query_pb, namespace=None,
                  eventual=False, transaction_id=None):
        """Run a query on the Cloud Datastore.

        Maps the ``DatastoreService.RunQuery`` protobuf RPC.

        Given a Query protobuf, sends a ``runQuery`` request to the
        Cloud Datastore API and returns a list of entity protobufs
        matching the query.

        You typically wouldn't use this method directly, in favor of the
        :meth:`google.cloud.datastore.query.Query.fetch` method.

        Under the hood, the :class:`google.cloud.datastore.query.Query` class
        uses this method to fetch data.

        :type project: string
        :param project: The project over which to run the query.

        :type query_pb: :class:`.datastore._generated.query_pb2.Query`
        :param query_pb: The Protobuf representing the query to run.

        :type namespace: string
        :param namespace: The namespace over which to run the query.

        :type eventual: bool
        :param eventual: If False (the default), request ``STRONG`` read
                         consistency.  If True, request ``EVENTUAL`` read
                         consistency.

        :type transaction_id: string
        :param transaction_id: If passed, make the request in the scope of
                               the given transaction.  Incompatible with
                               ``eventual==True``.

        :rtype: tuple
        :returns: Four-tuple containing the entities returned,
                  the end cursor of the query, a ``more_results``
                  enum and a count of the number of skipped results.
        """
        return self._datastore_api.run_query(
            project, query_pb, namespace=namespace,
            eventual=eventual, transaction_id=transaction_id)

    def begin_transaction(self, project):
        """Begin a transaction.

        Maps the ``DatastoreService.BeginTransaction`` protobuf RPC.

        :type project: string
        :param project: The project to which the transaction applies.

        :rtype: bytes
        :returns: The serialized transaction that was begun.
        """
        return self._datastore_api.begin_transaction(project)

    def commit(self, project, request, transaction_id):
        """Commit mutations in context of current transaction (if any).

        Maps the ``DatastoreService.Commit`` protobuf RPC.

        :type project: string
        :param project: The project to which the transaction applies.

        :type request: :class:`._generated.datastore_pb2.CommitRequest`
        :param request: The protobuf with the mutations being committed.

        :type transaction_id: string or None
        :param transaction_id: The transaction ID returned from
                               :meth:`begin_transaction`.  Non-transactional
                               batches must pass ``None``.

        .. note::

            This method will mutate ``request`` before using it.

        :rtype: tuple
        :returns: The pair of the number of index updates and a list of
                  :class:`._generated.entity_pb2.Key` for each incomplete key
                  that was completed in the commit.
        """
        if transaction_id:
            request.mode = _datastore_pb2.CommitRequest.TRANSACTIONAL
            request.transaction = transaction_id
        else:
            request.mode = _datastore_pb2.CommitRequest.NON_TRANSACTIONAL

        response = self._datastore_api.commit(project, request)
        return _parse_commit_response(response)

    def rollback(self, project, transaction_id):
        """Rollback the connection's existing transaction.

        Maps the ``DatastoreService.Rollback`` protobuf RPC.

        :type project: string
        :param project: The project to which the transaction belongs.

        :type transaction_id: string
        :param transaction_id: The transaction ID returned from
                               :meth:`begin_transaction`.
        """
        request = _datastore_pb2.RollbackRequest()
        request.transaction = transaction_id
        # Nothing to do with this response, so just execute the method.
        self._datastore_api.rollback(project, request)

    def allocate_ids(self, project, key_pbs):
        """Obtain backend-generated IDs for a set of keys.

        Maps the ``DatastoreService.AllocateIds`` protobuf RPC.

        :type project: string
        :param project: The project to which the transaction belongs.

        :type key_pbs: list of
                       :class:`google.cloud.datastore._generated.entity_pb2.Key`
        :param key_pbs: The keys for which the backend should allocate IDs.

        :rtype: list of :class:`.datastore._generated.entity_pb2.Key`
        :returns: An equal number of keys,  with IDs filled in by the backend.
        """
        request = _datastore_pb2.AllocateIdsRequest()
        _add_keys_to_request(request.keys, key_pbs)
        # Nothing to do with this response, so just execute the method.
        response = self._datastore_api.allocate_ids(project, request)
        return list(response.keys)


def _parse_commit_response(commit_response_pb):
    """Extract response data from a commit response.

    :type commit_response_pb: :class:`._generated.datastore_pb2.CommitResponse`
    :param commit_response_pb: The protobuf response from a commit request.

    :rtype: tuple
    :returns: The pair of the number of index updates and a list of
              :class:`._generated.entity_pb2.Key` for each incomplete key
              that was completed in the commit.
    """
    mut_results = commit_response_pb.mutation_results
    index_updates = commit_response_pb.index_updates
    completed_keys = [mut_result.key for mut_result in mut_results
                      if mut_result.HasField('key')]  # Message field (Key)
    return index_updates, completed_keys
