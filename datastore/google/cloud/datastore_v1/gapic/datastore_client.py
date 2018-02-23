# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Accesses the google.datastore.v1 Datastore API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.protobuf_helpers

from google.cloud.datastore_v1.gapic import datastore_client_config
from google.cloud.datastore_v1.gapic import enums
from google.cloud.datastore_v1.proto import datastore_pb2
from google.cloud.datastore_v1.proto import entity_pb2
from google.cloud.datastore_v1.proto import query_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-datastore', ).version


class DatastoreClient(object):
    """
    Each RPC normalizes the partition IDs of the keys in its input entities,
    and always returns entities with keys with normalized partition IDs.
    This applies to all keys and entities, including those in values, except keys
    with both an empty path and an empty or unset partition ID. Normalization of
    input keys sets the project ID (if not already set) to the project ID from
    the request.
    """

    SERVICE_ADDRESS = 'datastore.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/datastore',
    )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.datastore.v1.Datastore'

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=datastore_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict): A dictionary of call options for each
                method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__), )

        # Create the channel.
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.datastore_stub = (datastore_pb2.DatastoreStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._lookup = google.api_core.gapic_v1.method.wrap_method(
            self.datastore_stub.Lookup,
            default_retry=method_configs['Lookup'].retry,
            default_timeout=method_configs['Lookup'].timeout,
            client_info=client_info,
        )
        self._run_query = google.api_core.gapic_v1.method.wrap_method(
            self.datastore_stub.RunQuery,
            default_retry=method_configs['RunQuery'].retry,
            default_timeout=method_configs['RunQuery'].timeout,
            client_info=client_info,
        )
        self._begin_transaction = google.api_core.gapic_v1.method.wrap_method(
            self.datastore_stub.BeginTransaction,
            default_retry=method_configs['BeginTransaction'].retry,
            default_timeout=method_configs['BeginTransaction'].timeout,
            client_info=client_info,
        )
        self._commit = google.api_core.gapic_v1.method.wrap_method(
            self.datastore_stub.Commit,
            default_retry=method_configs['Commit'].retry,
            default_timeout=method_configs['Commit'].timeout,
            client_info=client_info,
        )
        self._rollback = google.api_core.gapic_v1.method.wrap_method(
            self.datastore_stub.Rollback,
            default_retry=method_configs['Rollback'].retry,
            default_timeout=method_configs['Rollback'].timeout,
            client_info=client_info,
        )
        self._allocate_ids = google.api_core.gapic_v1.method.wrap_method(
            self.datastore_stub.AllocateIds,
            default_retry=method_configs['AllocateIds'].retry,
            default_timeout=method_configs['AllocateIds'].timeout,
            client_info=client_info,
        )
        self._reserve_ids = google.api_core.gapic_v1.method.wrap_method(
            self.datastore_stub.ReserveIds,
            default_retry=method_configs['ReserveIds'].retry,
            default_timeout=method_configs['ReserveIds'].timeout,
            client_info=client_info,
        )

    # Service calls
    def lookup(self,
               project_id,
               keys,
               read_options=None,
               retry=google.api_core.gapic_v1.method.DEFAULT,
               timeout=google.api_core.gapic_v1.method.DEFAULT,
               metadata=None):
        """
        Looks up entities by key.

        Example:
            >>> from google.cloud import datastore_v1
            >>>
            >>> client = datastore_v1.DatastoreClient()
            >>>
            >>> project_id = ''
            >>> keys = []
            >>>
            >>> response = client.lookup(project_id, keys)

        Args:
            project_id (str): The ID of the project against which to make the request.
            keys (list[Union[dict, ~google.cloud.datastore_v1.types.Key]]): Keys of entities to look up.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.Key`
            read_options (Union[dict, ~google.cloud.datastore_v1.types.ReadOptions]): The options for this lookup request.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.ReadOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_v1.types.LookupResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = datastore_pb2.LookupRequest(
            project_id=project_id,
            keys=keys,
            read_options=read_options,
        )
        return self._lookup(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def run_query(self,
                  project_id,
                  partition_id,
                  read_options=None,
                  query=None,
                  gql_query=None,
                  retry=google.api_core.gapic_v1.method.DEFAULT,
                  timeout=google.api_core.gapic_v1.method.DEFAULT,
                  metadata=None):
        """
        Queries for entities.

        Example:
            >>> from google.cloud import datastore_v1
            >>>
            >>> client = datastore_v1.DatastoreClient()
            >>>
            >>> project_id = ''
            >>> partition_id = {}
            >>>
            >>> response = client.run_query(project_id, partition_id)

        Args:
            project_id (str): The ID of the project against which to make the request.
            partition_id (Union[dict, ~google.cloud.datastore_v1.types.PartitionId]): Entities are partitioned into subsets, identified by a partition ID.
                Queries are scoped to a single partition.
                This partition ID is normalized with the standard default context
                partition ID.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.PartitionId`
            read_options (Union[dict, ~google.cloud.datastore_v1.types.ReadOptions]): The options for this query.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.ReadOptions`
            query (Union[dict, ~google.cloud.datastore_v1.types.Query]): The query to run.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.Query`
            gql_query (Union[dict, ~google.cloud.datastore_v1.types.GqlQuery]): The GQL query to run.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.GqlQuery`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_v1.types.RunQueryResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            query=query,
            gql_query=gql_query,
        )

        request = datastore_pb2.RunQueryRequest(
            project_id=project_id,
            partition_id=partition_id,
            read_options=read_options,
            query=query,
            gql_query=gql_query,
        )
        return self._run_query(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def begin_transaction(self,
                          project_id,
                          transaction_options=None,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT,
                          metadata=None):
        """
        Begins a new transaction.

        Example:
            >>> from google.cloud import datastore_v1
            >>>
            >>> client = datastore_v1.DatastoreClient()
            >>>
            >>> project_id = ''
            >>>
            >>> response = client.begin_transaction(project_id)

        Args:
            project_id (str): The ID of the project against which to make the request.
            transaction_options (Union[dict, ~google.cloud.datastore_v1.types.TransactionOptions]): Options for a new transaction.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.TransactionOptions`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_v1.types.BeginTransactionResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = datastore_pb2.BeginTransactionRequest(
            project_id=project_id,
            transaction_options=transaction_options,
        )
        return self._begin_transaction(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def commit(self,
               project_id,
               mode,
               mutations,
               transaction=None,
               retry=google.api_core.gapic_v1.method.DEFAULT,
               timeout=google.api_core.gapic_v1.method.DEFAULT,
               metadata=None):
        """
        Commits a transaction, optionally creating, deleting or modifying some
        entities.

        Example:
            >>> from google.cloud import datastore_v1
            >>> from google.cloud.datastore_v1 import enums
            >>>
            >>> client = datastore_v1.DatastoreClient()
            >>>
            >>> project_id = ''
            >>> mode = enums.CommitRequest.Mode.MODE_UNSPECIFIED
            >>> mutations = []
            >>>
            >>> response = client.commit(project_id, mode, mutations)

        Args:
            project_id (str): The ID of the project against which to make the request.
            mode (~google.cloud.datastore_v1.types.Mode): The type of commit to perform. Defaults to ``TRANSACTIONAL``.
            mutations (list[Union[dict, ~google.cloud.datastore_v1.types.Mutation]]): The mutations to perform.

                When mode is ``TRANSACTIONAL``, mutations affecting a single entity are
                applied in order. The following sequences of mutations affecting a single
                entity are not permitted in a single ``Commit`` request:

                - ``insert`` followed by ``insert``
                - ``update`` followed by ``insert``
                - ``upsert`` followed by ``insert``
                - ``delete`` followed by ``update``

                When mode is ``NON_TRANSACTIONAL``, no two mutations may affect a single
                entity.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.Mutation`
            transaction (bytes): The identifier of the transaction associated with the commit. A
                transaction identifier is returned by a call to
                ``Datastore.BeginTransaction``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_v1.types.CommitResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(transaction=transaction, )

        request = datastore_pb2.CommitRequest(
            project_id=project_id,
            mode=mode,
            mutations=mutations,
            transaction=transaction,
        )
        return self._commit(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def rollback(self,
                 project_id,
                 transaction,
                 retry=google.api_core.gapic_v1.method.DEFAULT,
                 timeout=google.api_core.gapic_v1.method.DEFAULT,
                 metadata=None):
        """
        Rolls back a transaction.

        Example:
            >>> from google.cloud import datastore_v1
            >>>
            >>> client = datastore_v1.DatastoreClient()
            >>>
            >>> project_id = ''
            >>> transaction = b''
            >>>
            >>> response = client.rollback(project_id, transaction)

        Args:
            project_id (str): The ID of the project against which to make the request.
            transaction (bytes): The transaction identifier, returned by a call to
                ``Datastore.BeginTransaction``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_v1.types.RollbackResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = datastore_pb2.RollbackRequest(
            project_id=project_id,
            transaction=transaction,
        )
        return self._rollback(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def allocate_ids(self,
                     project_id,
                     keys,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT,
                     metadata=None):
        """
        Allocates IDs for the given keys, which is useful for referencing an entity
        before it is inserted.

        Example:
            >>> from google.cloud import datastore_v1
            >>>
            >>> client = datastore_v1.DatastoreClient()
            >>>
            >>> project_id = ''
            >>> keys = []
            >>>
            >>> response = client.allocate_ids(project_id, keys)

        Args:
            project_id (str): The ID of the project against which to make the request.
            keys (list[Union[dict, ~google.cloud.datastore_v1.types.Key]]): A list of keys with incomplete key paths for which to allocate IDs.
                No key may be reserved/read-only.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.Key`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_v1.types.AllocateIdsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = datastore_pb2.AllocateIdsRequest(
            project_id=project_id,
            keys=keys,
        )
        return self._allocate_ids(
            request, retry=retry, timeout=timeout, metadata=metadata)

    def reserve_ids(self,
                    project_id,
                    keys,
                    database_id=None,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT,
                    metadata=None):
        """
        Prevents the supplied keys' IDs from being auto-allocated by Cloud
        Datastore.

        Example:
            >>> from google.cloud import datastore_v1
            >>>
            >>> client = datastore_v1.DatastoreClient()
            >>>
            >>> project_id = ''
            >>> keys = []
            >>>
            >>> response = client.reserve_ids(project_id, keys)

        Args:
            project_id (str): The ID of the project against which to make the request.
            keys (list[Union[dict, ~google.cloud.datastore_v1.types.Key]]): A list of keys with complete key paths whose numeric IDs should not be
                auto-allocated.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.datastore_v1.types.Key`
            database_id (str): If not empty, the ID of the database against which to make the request.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.datastore_v1.types.ReserveIdsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = datastore_pb2.ReserveIdsRequest(
            project_id=project_id,
            keys=keys,
            database_id=database_id,
        )
        return self._reserve_ids(
            request, retry=retry, timeout=timeout, metadata=metadata)
