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
from distutils import util
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

OptionalRetry = Union[retries.Retry, object]

from google.cloud.datastore_v1.types import datastore
from google.cloud.datastore_v1.types import entity
from google.cloud.datastore_v1.types import query
from .transports.base import DatastoreTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DatastoreGrpcTransport
from .transports.grpc_asyncio import DatastoreGrpcAsyncIOTransport


class DatastoreClientMeta(type):
    """Metaclass for the Datastore client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[DatastoreTransport]]
    _transport_registry["grpc"] = DatastoreGrpcTransport
    _transport_registry["grpc_asyncio"] = DatastoreGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[DatastoreTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class DatastoreClient(metaclass=DatastoreClientMeta):
    """Each RPC normalizes the partition IDs of the keys in its
    input entities, and always returns entities with keys with
    normalized partition IDs. This applies to all keys and entities,
    including those in values, except keys with both an empty path
    and an empty or unset partition ID. Normalization of input keys
    sets the project ID (if not already set) to the project ID from
    the request.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "datastore.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
            DatastoreClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            DatastoreClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DatastoreTransport:
        """Returns the transport used by the client instance.

        Returns:
            DatastoreTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, DatastoreTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the datastore client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DatastoreTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, DatastoreTransport):
            # transport is a DatastoreTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def lookup(
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
            project_id (str):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            read_options (google.cloud.datastore_v1.types.ReadOptions):
                The options for this lookup request.
                This corresponds to the ``read_options`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            keys (Sequence[google.cloud.datastore_v1.types.Key]):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore.LookupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore.LookupRequest):
            request = datastore.LookupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if read_options is not None:
                request.read_options = read_options
            if keys is not None:
                request.keys = keys

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.lookup]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def run_query(
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
        # Minor optimization to avoid making a copy if the user passes
        # in a datastore.RunQueryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore.RunQueryRequest):
            request = datastore.RunQueryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_query]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def begin_transaction(
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
            project_id (str):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore.BeginTransactionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore.BeginTransactionRequest):
            request = datastore.BeginTransactionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.begin_transaction]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def commit(
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
            project_id (str):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mode (google.cloud.datastore_v1.types.CommitRequest.Mode):
                The type of commit to perform. Defaults to
                ``TRANSACTIONAL``.

                This corresponds to the ``mode`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            transaction (bytes):
                The identifier of the transaction associated with the
                commit. A transaction identifier is returned by a call
                to
                [Datastore.BeginTransaction][google.datastore.v1.Datastore.BeginTransaction].

                This corresponds to the ``transaction`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mutations (Sequence[google.cloud.datastore_v1.types.Mutation]):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore.CommitRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore.CommitRequest):
            request = datastore.CommitRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if mode is not None:
                request.mode = mode
            if transaction is not None:
                request.transaction = transaction
            if mutations is not None:
                request.mutations = mutations

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.commit]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def rollback(
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
            project_id (str):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            transaction (bytes):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore.RollbackRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore.RollbackRequest):
            request = datastore.RollbackRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if transaction is not None:
                request.transaction = transaction

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.rollback]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def allocate_ids(
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
            project_id (str):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            keys (Sequence[google.cloud.datastore_v1.types.Key]):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore.AllocateIdsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore.AllocateIdsRequest):
            request = datastore.AllocateIdsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if keys is not None:
                request.keys = keys

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.allocate_ids]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def reserve_ids(
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
            project_id (str):
                Required. The ID of the project
                against which to make the request.

                This corresponds to the ``project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            keys (Sequence[google.cloud.datastore_v1.types.Key]):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a datastore.ReserveIdsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, datastore.ReserveIdsRequest):
            request = datastore.ReserveIdsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if project_id is not None:
                request.project_id = project_id
            if keys is not None:
                request.keys = keys

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reserve_ids]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-datastore",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DatastoreClient",)
