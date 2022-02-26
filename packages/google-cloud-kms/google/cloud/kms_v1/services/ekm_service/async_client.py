# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.kms_v1.services.ekm_service import pagers
from google.cloud.kms_v1.types import ekm_service
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import EkmServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import EkmServiceGrpcAsyncIOTransport
from .client import EkmServiceClient


class EkmServiceAsyncClient:
    """Google Cloud Key Management EKM Service

    Manages external cryptographic keys and operations using those keys.
    Implements a REST model with the following objects:

    -  [EkmConnection][google.cloud.kms.v1.EkmConnection]
    """

    _client: EkmServiceClient

    DEFAULT_ENDPOINT = EkmServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = EkmServiceClient.DEFAULT_MTLS_ENDPOINT

    ekm_connection_path = staticmethod(EkmServiceClient.ekm_connection_path)
    parse_ekm_connection_path = staticmethod(EkmServiceClient.parse_ekm_connection_path)
    service_path = staticmethod(EkmServiceClient.service_path)
    parse_service_path = staticmethod(EkmServiceClient.parse_service_path)
    common_billing_account_path = staticmethod(
        EkmServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        EkmServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(EkmServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(EkmServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(EkmServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        EkmServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(EkmServiceClient.common_project_path)
    parse_common_project_path = staticmethod(EkmServiceClient.parse_common_project_path)
    common_location_path = staticmethod(EkmServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        EkmServiceClient.parse_common_location_path
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
            EkmServiceAsyncClient: The constructed client.
        """
        return EkmServiceClient.from_service_account_info.__func__(EkmServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            EkmServiceAsyncClient: The constructed client.
        """
        return EkmServiceClient.from_service_account_file.__func__(EkmServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.


        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return EkmServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> EkmServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            EkmServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(EkmServiceClient).get_transport_class, type(EkmServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, EkmServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the ekm service client.


        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.EkmServiceTransport]): The
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
        self._client = EkmServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_ekm_connections(
        self,
        request: Union[ekm_service.ListEkmConnectionsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEkmConnectionsAsyncPager:
        r"""Lists [EkmConnections][google.cloud.kms.v1.EkmConnection].

        .. code-block:: python

            from google.cloud import kms_v1

            def sample_list_ekm_connections():
                # Create a client
                client = kms_v1.EkmServiceClient()

                # Initialize request argument(s)
                request = kms_v1.ListEkmConnectionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_ekm_connections(request=request)

                # Handle the response
                for response in page_result:
                    print(response)


        Args:
            request (Union[google.cloud.kms_v1.types.ListEkmConnectionsRequest, dict]):
                The request object. Request message for
                [KeyManagementService.ListEkmConnections][].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [EkmConnections][google.cloud.kms.v1.EkmConnection] to
                list, in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.kms_v1.services.ekm_service.pagers.ListEkmConnectionsAsyncPager:
                Response message for
                [KeyManagementService.ListEkmConnections][].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = ekm_service.ListEkmConnectionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_ekm_connections,
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListEkmConnectionsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_ekm_connection(
        self,
        request: Union[ekm_service.GetEkmConnectionRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ekm_service.EkmConnection:
        r"""Returns metadata for a given
        [EkmConnection][google.cloud.kms.v1.EkmConnection].


        .. code-block:: python

            from google.cloud import kms_v1

            def sample_get_ekm_connection():
                # Create a client
                client = kms_v1.EkmServiceClient()

                # Initialize request argument(s)
                request = kms_v1.GetEkmConnectionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_ekm_connection(request=request)

                # Handle the response
                print(response)


        Args:
            request (Union[google.cloud.kms_v1.types.GetEkmConnectionRequest, dict]):
                The request object. Request message for
                [KeyManagementService.GetEkmConnection][].
            name (:class:`str`):
                Required. The
                [name][google.cloud.kms.v1.EkmConnection.name] of the
                [EkmConnection][google.cloud.kms.v1.EkmConnection] to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.kms_v1.types.EkmConnection:
                An [EkmConnection][google.cloud.kms.v1.EkmConnection] represents an
                   individual EKM connection. It can be used for
                   creating [CryptoKeys][google.cloud.kms.v1.CryptoKey]
                   and
                   [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                   with a
                   [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                   of
                   [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC],
                   as well as performing cryptographic operations using
                   keys created within the
                   [EkmConnection][google.cloud.kms.v1.EkmConnection].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = ekm_service.GetEkmConnectionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_ekm_connection,
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_ekm_connection(
        self,
        request: Union[ekm_service.CreateEkmConnectionRequest, dict] = None,
        *,
        parent: str = None,
        ekm_connection_id: str = None,
        ekm_connection: ekm_service.EkmConnection = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ekm_service.EkmConnection:
        r"""Creates a new [EkmConnection][google.cloud.kms.v1.EkmConnection]
        in a given Project and Location.


        .. code-block:: python

            from google.cloud import kms_v1

            def sample_create_ekm_connection():
                # Create a client
                client = kms_v1.EkmServiceClient()

                # Initialize request argument(s)
                request = kms_v1.CreateEkmConnectionRequest(
                    parent="parent_value",
                    ekm_connection_id="ekm_connection_id_value",
                )

                # Make the request
                response = client.create_ekm_connection(request=request)

                # Handle the response
                print(response)


        Args:
            request (Union[google.cloud.kms_v1.types.CreateEkmConnectionRequest, dict]):
                The request object. Request message for
                [KeyManagementService.CreateEkmConnection][].
            parent (:class:`str`):
                Required. The resource name of the location associated
                with the
                [EkmConnection][google.cloud.kms.v1.EkmConnection], in
                the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ekm_connection_id (:class:`str`):
                Required. It must be unique within a location and match
                the regular expression ``[a-zA-Z0-9_-]{1,63}``.

                This corresponds to the ``ekm_connection_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            ekm_connection (:class:`google.cloud.kms_v1.types.EkmConnection`):
                Required. An
                [EkmConnection][google.cloud.kms.v1.EkmConnection] with
                initial field values.

                This corresponds to the ``ekm_connection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.kms_v1.types.EkmConnection:
                An [EkmConnection][google.cloud.kms.v1.EkmConnection] represents an
                   individual EKM connection. It can be used for
                   creating [CryptoKeys][google.cloud.kms.v1.CryptoKey]
                   and
                   [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                   with a
                   [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                   of
                   [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC],
                   as well as performing cryptographic operations using
                   keys created within the
                   [EkmConnection][google.cloud.kms.v1.EkmConnection].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, ekm_connection_id, ekm_connection])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = ekm_service.CreateEkmConnectionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if ekm_connection_id is not None:
            request.ekm_connection_id = ekm_connection_id
        if ekm_connection is not None:
            request.ekm_connection = ekm_connection

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_ekm_connection,
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_ekm_connection(
        self,
        request: Union[ekm_service.UpdateEkmConnectionRequest, dict] = None,
        *,
        ekm_connection: ekm_service.EkmConnection = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> ekm_service.EkmConnection:
        r"""Updates an [EkmConnection][google.cloud.kms.v1.EkmConnection]'s
        metadata.


        .. code-block:: python

            from google.cloud import kms_v1

            def sample_update_ekm_connection():
                # Create a client
                client = kms_v1.EkmServiceClient()

                # Initialize request argument(s)
                request = kms_v1.UpdateEkmConnectionRequest(
                )

                # Make the request
                response = client.update_ekm_connection(request=request)

                # Handle the response
                print(response)


        Args:
            request (Union[google.cloud.kms_v1.types.UpdateEkmConnectionRequest, dict]):
                The request object. Request message for
                [KeyManagementService.UpdateEkmConnection][].
            ekm_connection (:class:`google.cloud.kms_v1.types.EkmConnection`):
                Required.
                [EkmConnection][google.cloud.kms.v1.EkmConnection] with
                updated values.

                This corresponds to the ``ekm_connection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. List of fields to be
                updated in this request.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.kms_v1.types.EkmConnection:
                An [EkmConnection][google.cloud.kms.v1.EkmConnection] represents an
                   individual EKM connection. It can be used for
                   creating [CryptoKeys][google.cloud.kms.v1.CryptoKey]
                   and
                   [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
                   with a
                   [ProtectionLevel][google.cloud.kms.v1.ProtectionLevel]
                   of
                   [EXTERNAL_VPC][CryptoKeyVersion.ProtectionLevel.EXTERNAL_VPC],
                   as well as performing cryptographic operations using
                   keys created within the
                   [EkmConnection][google.cloud.kms.v1.EkmConnection].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([ekm_connection, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = ekm_service.UpdateEkmConnectionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if ekm_connection is not None:
            request.ekm_connection = ekm_connection
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_ekm_connection,
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

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("ekm_connection.name", request.ekm_connection.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM access control policy on the specified function.

        Replaces any existing policy.


        Args:
            request (:class:`~.policy_pb2.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM access control policy for a function.

        Returns an empty policy if the function exists and does
        not have a policy set.


        Args:
            request (:class:`~.iam_policy_pb2.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**::

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests the specified permissions against the IAM access control
            policy for a function.

        If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.


        Args:
            request (:class:`~.iam_policy_pb2.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~iam_policy_pb2.PolicyTestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
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
        gapic_version=pkg_resources.get_distribution("google-cloud-kms",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("EkmServiceAsyncClient",)
