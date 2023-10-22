# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import (
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

from google.cloud.monitoring_v3 import gapic_version as package_version

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

from google.cloud.monitoring_v3.services.alert_policy_service import pagers
from google.cloud.monitoring_v3.types import alert
from google.cloud.monitoring_v3.types import alert_service
from google.cloud.monitoring_v3.types import mutation_record
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import AlertPolicyServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import AlertPolicyServiceGrpcAsyncIOTransport
from .client import AlertPolicyServiceClient


class AlertPolicyServiceAsyncClient:
    """The AlertPolicyService API is used to manage (list, create, delete,
    edit) alert policies in Cloud Monitoring. An alerting policy is a
    description of the conditions under which some aspect of your system
    is considered to be "unhealthy" and the ways to notify people or
    services about this state. In addition to using this API, alert
    policies can also be managed through `Cloud
    Monitoring <https://cloud.google.com/monitoring/docs/>`__, which can
    be reached by clicking the "Monitoring" tab in `Cloud
    console <https://console.cloud.google.com/>`__.
    """

    _client: AlertPolicyServiceClient

    DEFAULT_ENDPOINT = AlertPolicyServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AlertPolicyServiceClient.DEFAULT_MTLS_ENDPOINT

    alert_policy_path = staticmethod(AlertPolicyServiceClient.alert_policy_path)
    parse_alert_policy_path = staticmethod(
        AlertPolicyServiceClient.parse_alert_policy_path
    )
    alert_policy_condition_path = staticmethod(
        AlertPolicyServiceClient.alert_policy_condition_path
    )
    parse_alert_policy_condition_path = staticmethod(
        AlertPolicyServiceClient.parse_alert_policy_condition_path
    )
    common_billing_account_path = staticmethod(
        AlertPolicyServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AlertPolicyServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AlertPolicyServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AlertPolicyServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AlertPolicyServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AlertPolicyServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AlertPolicyServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        AlertPolicyServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(AlertPolicyServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        AlertPolicyServiceClient.parse_common_location_path
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
            AlertPolicyServiceAsyncClient: The constructed client.
        """
        return AlertPolicyServiceClient.from_service_account_info.__func__(AlertPolicyServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AlertPolicyServiceAsyncClient: The constructed client.
        """
        return AlertPolicyServiceClient.from_service_account_file.__func__(AlertPolicyServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return AlertPolicyServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AlertPolicyServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AlertPolicyServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(AlertPolicyServiceClient).get_transport_class,
        type(AlertPolicyServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, AlertPolicyServiceTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the alert policy service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.AlertPolicyServiceTransport]): The
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
        self._client = AlertPolicyServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_alert_policies(
        self,
        request: Optional[Union[alert_service.ListAlertPoliciesRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAlertPoliciesAsyncPager:
        r"""Lists the existing alerting policies for the
        workspace.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import monitoring_v3

            async def sample_list_alert_policies():
                # Create a client
                client = monitoring_v3.AlertPolicyServiceAsyncClient()

                # Initialize request argument(s)
                request = monitoring_v3.ListAlertPoliciesRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.list_alert_policies(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.monitoring_v3.types.ListAlertPoliciesRequest, dict]]):
                The request object. The protocol for the ``ListAlertPolicies`` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                whose alert policies are to be listed. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this field names the parent container in which
                the alerting policies to be listed are stored. To
                retrieve a single alerting policy by name, use the
                [GetAlertPolicy][google.monitoring.v3.AlertPolicyService.GetAlertPolicy]
                operation, instead.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.alert_policy_service.pagers.ListAlertPoliciesAsyncPager:
                The protocol for the ListAlertPolicies response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = alert_service.ListAlertPoliciesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_alert_policies,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAlertPoliciesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_alert_policy(
        self,
        request: Optional[Union[alert_service.GetAlertPolicyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> alert.AlertPolicy:
        r"""Gets a single alerting policy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import monitoring_v3

            async def sample_get_alert_policy():
                # Create a client
                client = monitoring_v3.AlertPolicyServiceAsyncClient()

                # Initialize request argument(s)
                request = monitoring_v3.GetAlertPolicyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_alert_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.monitoring_v3.types.GetAlertPolicyRequest, dict]]):
                The request object. The protocol for the ``GetAlertPolicy`` request.
            name (:class:`str`):
                Required. The alerting policy to retrieve. The format
                is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[ALERT_POLICY_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.AlertPolicy:
                A description of the conditions under which some aspect of your system is
                   considered to be "unhealthy" and the ways to notify
                   people or services about this state. For an overview
                   of alert policies, see [Introduction to
                   Alerting](\ https://cloud.google.com/monitoring/alerts/).

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

        request = alert_service.GetAlertPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_alert_policy,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_alert_policy(
        self,
        request: Optional[Union[alert_service.CreateAlertPolicyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        alert_policy: Optional[alert.AlertPolicy] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> alert.AlertPolicy:
        r"""Creates a new alerting policy.

        Design your application to single-thread API calls that
        modify the state of alerting policies in a single
        project. This includes calls to CreateAlertPolicy,
        DeleteAlertPolicy and UpdateAlertPolicy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import monitoring_v3

            async def sample_create_alert_policy():
                # Create a client
                client = monitoring_v3.AlertPolicyServiceAsyncClient()

                # Initialize request argument(s)
                request = monitoring_v3.CreateAlertPolicyRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.create_alert_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.monitoring_v3.types.CreateAlertPolicyRequest, dict]]):
                The request object. The protocol for the ``CreateAlertPolicy`` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                in which to create the alerting policy. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this field names the parent container in which
                the alerting policy will be written, not the name of the
                created policy. \|name\| must be a host project of a
                Metrics Scope, otherwise INVALID_ARGUMENT error will
                return. The alerting policy that is returned will have a
                name that contains a normalized representation of this
                name as a prefix but adds a suffix of the form
                ``/alertPolicies/[ALERT_POLICY_ID]``, identifying the
                policy in the container.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            alert_policy (:class:`google.cloud.monitoring_v3.types.AlertPolicy`):
                Required. The requested alerting policy. You should omit
                the ``name`` field in this policy. The name will be
                returned in the new policy, including a new
                ``[ALERT_POLICY_ID]`` value.

                This corresponds to the ``alert_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.AlertPolicy:
                A description of the conditions under which some aspect of your system is
                   considered to be "unhealthy" and the ways to notify
                   people or services about this state. For an overview
                   of alert policies, see [Introduction to
                   Alerting](\ https://cloud.google.com/monitoring/alerts/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, alert_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = alert_service.CreateAlertPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if alert_policy is not None:
            request.alert_policy = alert_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_alert_policy,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_alert_policy(
        self,
        request: Optional[Union[alert_service.DeleteAlertPolicyRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an alerting policy.

        Design your application to single-thread API calls that
        modify the state of alerting policies in a single
        project. This includes calls to CreateAlertPolicy,
        DeleteAlertPolicy and UpdateAlertPolicy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import monitoring_v3

            async def sample_delete_alert_policy():
                # Create a client
                client = monitoring_v3.AlertPolicyServiceAsyncClient()

                # Initialize request argument(s)
                request = monitoring_v3.DeleteAlertPolicyRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_alert_policy(request=request)

        Args:
            request (Optional[Union[google.cloud.monitoring_v3.types.DeleteAlertPolicyRequest, dict]]):
                The request object. The protocol for the ``DeleteAlertPolicy`` request.
            name (:class:`str`):
                Required. The alerting policy to delete. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[ALERT_POLICY_ID]

                For more information, see
                [AlertPolicy][google.monitoring.v3.AlertPolicy].

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
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

        request = alert_service.DeleteAlertPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_alert_policy,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def update_alert_policy(
        self,
        request: Optional[Union[alert_service.UpdateAlertPolicyRequest, dict]] = None,
        *,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        alert_policy: Optional[alert.AlertPolicy] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> alert.AlertPolicy:
        r"""Updates an alerting policy. You can either replace the entire
        policy with a new one or replace only certain fields in the
        current alerting policy by specifying the fields to be updated
        via ``updateMask``. Returns the updated alerting policy.

        Design your application to single-thread API calls that modify
        the state of alerting policies in a single project. This
        includes calls to CreateAlertPolicy, DeleteAlertPolicy and
        UpdateAlertPolicy.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import monitoring_v3

            async def sample_update_alert_policy():
                # Create a client
                client = monitoring_v3.AlertPolicyServiceAsyncClient()

                # Initialize request argument(s)
                request = monitoring_v3.UpdateAlertPolicyRequest(
                )

                # Make the request
                response = await client.update_alert_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.monitoring_v3.types.UpdateAlertPolicyRequest, dict]]):
                The request object. The protocol for the ``UpdateAlertPolicy`` request.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. A list of alerting policy field names. If this
                field is not empty, each listed field in the existing
                alerting policy is set to the value of the corresponding
                field in the supplied policy (``alert_policy``), or to
                the field's default value if the field is not in the
                supplied alerting policy. Fields not listed retain their
                previous value.

                Examples of valid field masks include ``display_name``,
                ``documentation``, ``documentation.content``,
                ``documentation.mime_type``, ``user_labels``,
                ``user_label.nameofkey``, ``enabled``, ``conditions``,
                ``combiner``, etc.

                If this field is empty, then the supplied alerting
                policy replaces the existing policy. It is the same as
                deleting the existing policy and adding the supplied
                policy, except for the following:

                -  The new policy will have the same
                   ``[ALERT_POLICY_ID]`` as the former policy. This
                   gives you continuity with the former policy in your
                   notifications and incidents.
                -  Conditions in the new policy will keep their former
                   ``[CONDITION_ID]`` if the supplied condition includes
                   the ``name`` field with that ``[CONDITION_ID]``. If
                   the supplied condition omits the ``name`` field, then
                   a new ``[CONDITION_ID]`` is created.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            alert_policy (:class:`google.cloud.monitoring_v3.types.AlertPolicy`):
                Required. The updated alerting policy or the updated
                values for the fields listed in ``update_mask``. If
                ``update_mask`` is not empty, any fields in this policy
                that are not in ``update_mask`` are ignored.

                This corresponds to the ``alert_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.AlertPolicy:
                A description of the conditions under which some aspect of your system is
                   considered to be "unhealthy" and the ways to notify
                   people or services about this state. For an overview
                   of alert policies, see [Introduction to
                   Alerting](\ https://cloud.google.com/monitoring/alerts/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([update_mask, alert_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = alert_service.UpdateAlertPolicyRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if update_mask is not None:
            request.update_mask = update_mask
        if alert_policy is not None:
            request.alert_policy = alert_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_alert_policy,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("alert_policy.name", request.alert_policy.name),)
            ),
        )

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "AlertPolicyServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AlertPolicyServiceAsyncClient",)
