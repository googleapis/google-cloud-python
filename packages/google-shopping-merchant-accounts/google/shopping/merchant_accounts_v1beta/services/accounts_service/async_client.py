# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import re
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.shopping.merchant_accounts_v1beta import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.type import datetime_pb2  # type: ignore

from google.shopping.merchant_accounts_v1beta.services.accounts_service import pagers
from google.shopping.merchant_accounts_v1beta.types import accounts

from .client import AccountsServiceClient
from .transports.base import DEFAULT_CLIENT_INFO, AccountsServiceTransport
from .transports.grpc_asyncio import AccountsServiceGrpcAsyncIOTransport


class AccountsServiceAsyncClient:
    """Service to support Accounts API."""

    _client: AccountsServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = AccountsServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AccountsServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = AccountsServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = AccountsServiceClient._DEFAULT_UNIVERSE

    account_path = staticmethod(AccountsServiceClient.account_path)
    parse_account_path = staticmethod(AccountsServiceClient.parse_account_path)
    terms_of_service_path = staticmethod(AccountsServiceClient.terms_of_service_path)
    parse_terms_of_service_path = staticmethod(
        AccountsServiceClient.parse_terms_of_service_path
    )
    user_path = staticmethod(AccountsServiceClient.user_path)
    parse_user_path = staticmethod(AccountsServiceClient.parse_user_path)
    common_billing_account_path = staticmethod(
        AccountsServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AccountsServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AccountsServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AccountsServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AccountsServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AccountsServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AccountsServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        AccountsServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(AccountsServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        AccountsServiceClient.parse_common_location_path
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
            AccountsServiceAsyncClient: The constructed client.
        """
        return AccountsServiceClient.from_service_account_info.__func__(AccountsServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AccountsServiceAsyncClient: The constructed client.
        """
        return AccountsServiceClient.from_service_account_file.__func__(AccountsServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        default mTLS endpoint; if the environment variable is "never", use the default API
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
        return AccountsServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AccountsServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AccountsServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = AccountsServiceClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str, AccountsServiceTransport, Callable[..., AccountsServiceTransport]
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the accounts service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,AccountsServiceTransport,Callable[..., AccountsServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the AccountsServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = AccountsServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_account(
        self,
        request: Optional[Union[accounts.GetAccountRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accounts.Account:
        r"""Retrieves an account from your Merchant Center
        account. After inserting, updating, or deleting an
        account, it may take several minutes before changes take
        effect.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_accounts_v1beta

            async def sample_get_account():
                # Create a client
                client = merchant_accounts_v1beta.AccountsServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_accounts_v1beta.GetAccountRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_accounts_v1beta.types.GetAccountRequest, dict]]):
                The request object. Request message for the ``GetAccount`` method.
            name (:class:`str`):
                Required. The name of the account to retrieve. Format:
                ``accounts/{account}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_accounts_v1beta.types.Account:
                An account.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, accounts.GetAccountRequest):
            request = accounts.GetAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_account
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_and_configure_account(
        self,
        request: Optional[
            Union[accounts.CreateAndConfigureAccountRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accounts.Account:
        r"""Creates a standalone Merchant Center account with
        additional configuration. Adds the user that makes the
        request as an admin for the new account.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_accounts_v1beta

            async def sample_create_and_configure_account():
                # Create a client
                client = merchant_accounts_v1beta.AccountsServiceAsyncClient()

                # Initialize request argument(s)
                account = merchant_accounts_v1beta.Account()
                account.account_name = "account_name_value"
                account.language_code = "language_code_value"

                request = merchant_accounts_v1beta.CreateAndConfigureAccountRequest(
                    account=account,
                )

                # Make the request
                response = await client.create_and_configure_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_accounts_v1beta.types.CreateAndConfigureAccountRequest, dict]]):
                The request object. Request message for the ``CreateAndConfigureAccount``
                method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_accounts_v1beta.types.Account:
                An account.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, accounts.CreateAndConfigureAccountRequest):
            request = accounts.CreateAndConfigureAccountRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.create_and_configure_account
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_account(
        self,
        request: Optional[Union[accounts.DeleteAccountRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified account regardless of its type:
        standalone, MCA or sub-account. Deleting an MCA leads to the
        deletion of all of its sub-accounts. Executing this method
        requires admin access. The deletion succeeds only if the account
        does not provide services to any other account and has no
        processed offers. You can use the ``force`` parameter to
        override this.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_accounts_v1beta

            async def sample_delete_account():
                # Create a client
                client = merchant_accounts_v1beta.AccountsServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_accounts_v1beta.DeleteAccountRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_account(request=request)

        Args:
            request (Optional[Union[google.shopping.merchant_accounts_v1beta.types.DeleteAccountRequest, dict]]):
                The request object. Request message for the ``DeleteAccount`` method.
            name (:class:`str`):
                Required. The name of the account to delete. Format:
                ``accounts/{account}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, accounts.DeleteAccountRequest):
            request = accounts.DeleteAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_account
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def update_account(
        self,
        request: Optional[Union[accounts.UpdateAccountRequest, dict]] = None,
        *,
        account: Optional[accounts.Account] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> accounts.Account:
        r"""Updates an account regardless of its type:
        standalone, MCA or sub-account. Executing this method
        requires admin access.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_accounts_v1beta

            async def sample_update_account():
                # Create a client
                client = merchant_accounts_v1beta.AccountsServiceAsyncClient()

                # Initialize request argument(s)
                account = merchant_accounts_v1beta.Account()
                account.account_name = "account_name_value"
                account.language_code = "language_code_value"

                request = merchant_accounts_v1beta.UpdateAccountRequest(
                    account=account,
                )

                # Make the request
                response = await client.update_account(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_accounts_v1beta.types.UpdateAccountRequest, dict]]):
                The request object. Request message for the ``UpdateAccount`` method.
            account (:class:`google.shopping.merchant_accounts_v1beta.types.Account`):
                Required. The new version of the
                account.

                This corresponds to the ``account`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. List of fields being
                updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_accounts_v1beta.types.Account:
                An account.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([account, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, accounts.UpdateAccountRequest):
            request = accounts.UpdateAccountRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if account is not None:
            request.account = account
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.update_account
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("account.name", request.account.name),)
            ),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_accounts(
        self,
        request: Optional[Union[accounts.ListAccountsRequest, dict]] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAccountsAsyncPager:
        r"""Lists accounts accessible to the calling user and
        matching the constraints of the request such as page
        size or filters. This is not just listing the
        sub-accounts of an MCA, but all accounts the calling
        user has access to including other MCAs, linked
        accounts, standalone accounts and so on. If no filter is
        provided, then it returns accounts the user is directly
        added to.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_accounts_v1beta

            async def sample_list_accounts():
                # Create a client
                client = merchant_accounts_v1beta.AccountsServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_accounts_v1beta.ListAccountsRequest(
                )

                # Make the request
                page_result = client.list_accounts(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_accounts_v1beta.types.ListAccountsRequest, dict]]):
                The request object. Request message for the ``ListAccounts`` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_accounts_v1beta.services.accounts_service.pagers.ListAccountsAsyncPager:
                Response message for the ListAccounts method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, accounts.ListAccountsRequest):
            request = accounts.ListAccountsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_accounts
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAccountsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_sub_accounts(
        self,
        request: Optional[Union[accounts.ListSubAccountsRequest, dict]] = None,
        *,
        provider: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListSubAccountsAsyncPager:
        r"""List all sub-accounts for a given multi client account. This is
        a convenience wrapper for the more powerful ``ListAccounts``
        method. This method will produce the same results as calling
        ``ListsAccounts`` with the following filter:
        ``relationship(providerId={parent} AND service(type="ACCOUNT_AGGREGATION"))``

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.shopping import merchant_accounts_v1beta

            async def sample_list_sub_accounts():
                # Create a client
                client = merchant_accounts_v1beta.AccountsServiceAsyncClient()

                # Initialize request argument(s)
                request = merchant_accounts_v1beta.ListSubAccountsRequest(
                    provider="provider_value",
                )

                # Make the request
                page_result = client.list_sub_accounts(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.shopping.merchant_accounts_v1beta.types.ListSubAccountsRequest, dict]]):
                The request object. Request message for the ``ListSubAccounts`` method.
            provider (:class:`str`):
                Required. The parent account. Format:
                ``accounts/{account}``

                This corresponds to the ``provider`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.shopping.merchant_accounts_v1beta.services.accounts_service.pagers.ListSubAccountsAsyncPager:
                Response message for the ListSubAccounts method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([provider])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, accounts.ListSubAccountsRequest):
            request = accounts.ListSubAccountsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if provider is not None:
            request.provider = provider

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_sub_accounts
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("provider", request.provider),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListSubAccountsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "AccountsServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AccountsServiceAsyncClient",)
