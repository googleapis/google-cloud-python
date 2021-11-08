# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

OptionalRetry = Union[retries.Retry, object]

from google.cloud.datastore_v1.types import datastore
from google.cloud.datastore_v1.types import entity
from google.cloud.datastore_v1.types import query
from .transports.base import DatastoreTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DatastoreGrpcAsyncIOTransport
from .client import DatastoreClient


class DatastoreAsyncClient:
    """Each RPC normalizes the partition IDs of the keys in its
    input entities, and always returns entities with keys with
    normalized partition IDs. This applies to all keys and entities,
    including those in values, except keys with both an empty path
    and an empty or unset partition ID. Normalization of input keys
    sets the project ID (if not already set) to the project ID from
    the request.
    """

    _client: DatastoreClient

    DEFAULT_ENDPOINT = DatastoreClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DatastoreClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        DatastoreClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DatastoreClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DatastoreClient.common_folder_path)
    parse_common_folder_path = staticmethod(DatastoreClient.parse_common_folder_path)
    common_organization_path = staticmethod(DatastoreClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        DatastoreClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DatastoreClient.common_project_path)
    parse_common_project_path = staticmethod(DatastoreClient.parse_common_project_path)
    common_location_path = staticmethod(DatastoreClient.common_location_path)
    parse_common_location_path = staticmethod(
        DatastoreClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DatastoreAsyncClient: The constructed client.
        """
        return DatastoreClient.from_service_account_info.__func__(DatastoreAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DatastoreAsyncClient: The constructed client.
        """
        return DatastoreClient.from_service_account_file.__func__(DatastoreAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DatastoreTransport:
        """Returns the transport used by the client instance.

        Returns:
            DatastoreTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DatastoreClient).get_transport_class, type(DatastoreClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DatastoreTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the datastore client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DatastoreTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = DatastoreClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def lookup(
        self,
        request: Union[datastore.LookupRequest, dict] = None,
        *,
        project_id: str = None,
        read_options: datastore.ReadOptions = None,
        keys: Sequence[entity.Key] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datastore.LookupResponse:
        r"""Looks up entities by key.

        Args:
            request (Union[google.cloud.datastore_v1.types.LookupRequest, dict]):
                The request object. The request for
                [Datastore.Lookup][google.datastore.v1.Datastore.Lookup].
            project_id (:class:`str`):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            read_options (:class:`google.cloud.datastore_v1.types.ReadOptions`):
                The options for this lookup request.
                This corresponds to the ``read_options`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            keys (:class:`Sequence[google.cloud.datastore_v1.types.Key]`):
                Required. Keys of entities to look
                up.

                This corresponds to the ``keys`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_v1.types.LookupResponse:
                The response for
                [Datastore.Lookup][google.datastore.v1.Datastore.Lookup].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, read_options, keys])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore.LookupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if read_options is not None:
            request.read_options = read_options
        if keys:
            request.keys.extend(keys)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.lookup,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def run_query(
        self,
        request: Union[datastore.RunQueryRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datastore.RunQueryResponse:
        r"""Queries for entities.

        Args:
            request (Union[google.cloud.datastore_v1.types.RunQueryRequest, dict]):
                The request object. The request for
                [Datastore.RunQuery][google.datastore.v1.Datastore.RunQuery].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_v1.types.RunQueryResponse:
                The response for
                [Datastore.RunQuery][google.datastore.v1.Datastore.RunQuery].

        """
        # Create or coerce a protobuf request object.
        request = datastore.RunQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_query,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def begin_transaction(
        self,
        request: Union[datastore.BeginTransactionRequest, dict] = None,
        *,
        project_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datastore.BeginTransactionResponse:
        r"""Begins a new transaction.

        Args:
            request (Union[google.cloud.datastore_v1.types.BeginTransactionRequest, dict]):
                The request object. The request for
                [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].
            project_id (:class:`str`):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_v1.types.BeginTransactionResponse:
                The response for
                [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore.BeginTransactionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.begin_transaction,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def commit(
        self,
        request: Union[datastore.CommitRequest, dict] = None,
        *,
        project_id: str = None,
        mode: datastore.CommitRequest.Mode = None,
        transaction: bytes = None,
        mutations: Sequence[datastore.Mutation] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datastore.CommitResponse:
        r"""Commits a transaction, optionally creating, deleting
        or modifying some entities.

        Args:
            request (Union[google.cloud.datastore_v1.types.CommitRequest, dict]):
                The request object. The request for
                [Datastore.Commit][google.datastore.v1.Datastore.Commit].
            project_id (:class:`str`):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mode (:class:`google.cloud.datastore_v1.types.CommitRequest.Mode`):
                The type of commit to perform. Defaults to
                ``TRANSACTIONAL``.

                This corresponds to the ``mode`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            transaction (:class:`bytes`):
                The identifier of the transaction associated with the
                commit. A transaction identifier is returned by a call
                to
                [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

                This corresponds to the ``transaction`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mutations (:class:`Sequence[google.cloud.datastore_v1.types.Mutation]`):
                The mutations to perform.

                When mode is ``TRANSACTIONAL``, mutations affecting a
                single entity are applied in order. The following
                sequences of mutations affecting a single entity are not
                permitted in a single ``Commit`` request:

                -  ``insert`` followed by ``insert``
                -  ``update`` followed by ``insert``
                -  ``upsert`` followed by ``insert``
                -  ``delete`` followed by ``update``

                When mode is ``NON_TRANSACTIONAL``, no two mutations may
                affect a single entity.

                This corresponds to the ``mutations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_v1.types.CommitResponse:
                The response for
                [Datastore.Commit][google.datastore.v1.Datastore.Commit].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, mode, transaction, mutations])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore.CommitRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if mode is not None:
            request.mode = mode
        if transaction is not None:
            request.transaction = transaction
        if mutations:
            request.mutations.extend(mutations)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.commit,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def rollback(
        self,
        request: Union[datastore.RollbackRequest, dict] = None,
        *,
        project_id: str = None,
        transaction: bytes = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datastore.RollbackResponse:
        r"""Rolls back a transaction.

        Args:
            request (Union[google.cloud.datastore_v1.types.RollbackRequest, dict]):
                The request object. The request for
                [Datastore.Rollback][google.datastore.v1.Datastore.Rollback].
            project_id (:class:`str`):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            transaction (:class:`bytes`):
                Required. The transaction identifier, returned by a call
                to
                [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

                This corresponds to the ``transaction`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_v1.types.RollbackResponse:
                The response for [Datastore.Rollback][google.datastore.v1.Datastore.Rollback].
                   (an empty message).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, transaction])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore.RollbackRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if transaction is not None:
            request.transaction = transaction

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.rollback,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def allocate_ids(
        self,
        request: Union[datastore.AllocateIdsRequest, dict] = None,
        *,
        project_id: str = None,
        keys: Sequence[entity.Key] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datastore.AllocateIdsResponse:
        r"""Allocates IDs for the given keys, which is useful for
        referencing an entity before it is inserted.

        Args:
            request (Union[google.cloud.datastore_v1.types.AllocateIdsRequest, dict]):
                The request object. The request for
                [Datastore.AllocateIds][google.datastore.v1.Datastore.AllocateIds].
            project_id (:class:`str`):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            keys (:class:`Sequence[google.cloud.datastore_v1.types.Key]`):
                Required. A list of keys with
                incomplete key paths for which to
                allocate IDs. No key may be
                reserved/read-only.

                This corresponds to the ``keys`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_v1.types.AllocateIdsResponse:
                The response for
                [Datastore.AllocateIds][google.datastore.v1.Datastore.AllocateIds].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, keys])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore.AllocateIdsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if keys:
            request.keys.extend(keys)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.allocate_ids,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def reserve_ids(
        self,
        request: Union[datastore.ReserveIdsRequest, dict] = None,
        *,
        project_id: str = None,
        keys: Sequence[entity.Key] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> datastore.ReserveIdsResponse:
        r"""Prevents the supplied keys' IDs from being auto-
        llocated by Cloud Datastore.

        Args:
            request (Union[google.cloud.datastore_v1.types.ReserveIdsRequest, dict]):
                The request object. The request for
                [Datastore.ReserveIds][google.datastore.v1.Datastore.ReserveIds].
            project_id (:class:`str`):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            keys (:class:`Sequence[google.cloud.datastore_v1.types.Key]`):
                Required. A list of keys with
                complete key paths whose numeric IDs
                should not be auto-allocated.

                This corresponds to the ``keys`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.datastore_v1.types.ReserveIdsResponse:
                The response for
                [Datastore.ReserveIds][google.datastore.v1.Datastore.ReserveIds].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([project_id, keys])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = datastore.ReserveIdsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if project_id is not None:
            request.project_id = project_id
        if keys:
            request.keys.extend(keys)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.reserve_ids,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-datastore",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DatastoreAsyncClient",)
