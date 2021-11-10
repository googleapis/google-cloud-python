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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.dialogflowcx_v3.services.test_cases import pagers
from google.cloud.dialogflowcx_v3.types import test_case
from google.cloud.dialogflowcx_v3.types import test_case as gcdc_test_case
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import TestCasesTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TestCasesGrpcAsyncIOTransport
from .client import TestCasesClient


class TestCasesAsyncClient:
    """Service for managing [Test
    Cases][google.cloud.dialogflow.cx.v3.TestCase] and [Test Case
    Results][google.cloud.dialogflow.cx.v3.TestCaseResult].
    """

    _client: TestCasesClient

    DEFAULT_ENDPOINT = TestCasesClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TestCasesClient.DEFAULT_MTLS_ENDPOINT

    agent_path = staticmethod(TestCasesClient.agent_path)
    parse_agent_path = staticmethod(TestCasesClient.parse_agent_path)
    entity_type_path = staticmethod(TestCasesClient.entity_type_path)
    parse_entity_type_path = staticmethod(TestCasesClient.parse_entity_type_path)
    environment_path = staticmethod(TestCasesClient.environment_path)
    parse_environment_path = staticmethod(TestCasesClient.parse_environment_path)
    flow_path = staticmethod(TestCasesClient.flow_path)
    parse_flow_path = staticmethod(TestCasesClient.parse_flow_path)
    intent_path = staticmethod(TestCasesClient.intent_path)
    parse_intent_path = staticmethod(TestCasesClient.parse_intent_path)
    page_path = staticmethod(TestCasesClient.page_path)
    parse_page_path = staticmethod(TestCasesClient.parse_page_path)
    test_case_path = staticmethod(TestCasesClient.test_case_path)
    parse_test_case_path = staticmethod(TestCasesClient.parse_test_case_path)
    test_case_result_path = staticmethod(TestCasesClient.test_case_result_path)
    parse_test_case_result_path = staticmethod(
        TestCasesClient.parse_test_case_result_path
    )
    transition_route_group_path = staticmethod(
        TestCasesClient.transition_route_group_path
    )
    parse_transition_route_group_path = staticmethod(
        TestCasesClient.parse_transition_route_group_path
    )
    webhook_path = staticmethod(TestCasesClient.webhook_path)
    parse_webhook_path = staticmethod(TestCasesClient.parse_webhook_path)
    common_billing_account_path = staticmethod(
        TestCasesClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TestCasesClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TestCasesClient.common_folder_path)
    parse_common_folder_path = staticmethod(TestCasesClient.parse_common_folder_path)
    common_organization_path = staticmethod(TestCasesClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        TestCasesClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TestCasesClient.common_project_path)
    parse_common_project_path = staticmethod(TestCasesClient.parse_common_project_path)
    common_location_path = staticmethod(TestCasesClient.common_location_path)
    parse_common_location_path = staticmethod(
        TestCasesClient.parse_common_location_path
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
            TestCasesAsyncClient: The constructed client.
        """
        return TestCasesClient.from_service_account_info.__func__(TestCasesAsyncClient, info, *args, **kwargs)  # type: ignore

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
            TestCasesAsyncClient: The constructed client.
        """
        return TestCasesClient.from_service_account_file.__func__(TestCasesAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> TestCasesTransport:
        """Returns the transport used by the client instance.

        Returns:
            TestCasesTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TestCasesClient).get_transport_class, type(TestCasesClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TestCasesTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the test cases client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TestCasesTransport]): The
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
        self._client = TestCasesClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_test_cases(
        self,
        request: Union[test_case.ListTestCasesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTestCasesAsyncPager:
        r"""Fetches a list of test cases for a given agent.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ListTestCasesRequest, dict]):
                The request object. The request message for
                [TestCases.ListTestCases][google.cloud.dialogflow.cx.v3.TestCases.ListTestCases].
            parent (:class:`str`):
                Required. The agent to list all pages for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.services.test_cases.pagers.ListTestCasesAsyncPager:
                The response message for
                [TestCases.ListTestCases][google.cloud.dialogflow.cx.v3.TestCases.ListTestCases].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = test_case.ListTestCasesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_test_cases,
            default_timeout=None,
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
        response = pagers.ListTestCasesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def batch_delete_test_cases(
        self,
        request: Union[test_case.BatchDeleteTestCasesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Batch deletes test cases.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.BatchDeleteTestCasesRequest, dict]):
                The request object. The request message for
                [TestCases.BatchDeleteTestCases][google.cloud.dialogflow.cx.v3.TestCases.BatchDeleteTestCases].
            parent (:class:`str`):
                Required. The agent to delete test cases from. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = test_case.BatchDeleteTestCasesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_delete_test_cases,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def get_test_case(
        self,
        request: Union[test_case.GetTestCaseRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> test_case.TestCase:
        r"""Gets a test case.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.GetTestCaseRequest, dict]):
                The request object. The request message for
                [TestCases.GetTestCase][google.cloud.dialogflow.cx.v3.TestCases.GetTestCase].
            name (:class:`str`):
                Required. The name of the testcase. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/testCases/<TestCase ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.TestCase:
                Represents a test case.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = test_case.GetTestCaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_test_case,
            default_timeout=None,
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

    async def create_test_case(
        self,
        request: Union[gcdc_test_case.CreateTestCaseRequest, dict] = None,
        *,
        parent: str = None,
        test_case: gcdc_test_case.TestCase = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_test_case.TestCase:
        r"""Creates a test case for the given agent.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.CreateTestCaseRequest, dict]):
                The request object. The request message for
                [TestCases.CreateTestCase][google.cloud.dialogflow.cx.v3.TestCases.CreateTestCase].
            parent (:class:`str`):
                Required. The agent to create the test case for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            test_case (:class:`google.cloud.dialogflowcx_v3.types.TestCase`):
                Required. The test case to create.
                This corresponds to the ``test_case`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.TestCase:
                Represents a test case.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, test_case])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_test_case.CreateTestCaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if test_case is not None:
            request.test_case = test_case

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_test_case,
            default_timeout=None,
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

    async def update_test_case(
        self,
        request: Union[gcdc_test_case.UpdateTestCaseRequest, dict] = None,
        *,
        test_case: gcdc_test_case.TestCase = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcdc_test_case.TestCase:
        r"""Updates the specified test case.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.UpdateTestCaseRequest, dict]):
                The request object. The request message for
                [TestCases.UpdateTestCase][google.cloud.dialogflow.cx.v3.TestCases.UpdateTestCase].
            test_case (:class:`google.cloud.dialogflowcx_v3.types.TestCase`):
                Required. The test case to update.
                This corresponds to the ``test_case`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to specify which fields should be
                updated. The
                [``creationTime``][google.cloud.dialogflow.cx.v3.TestCase.creation_time]
                and
                [``lastTestResult``][google.cloud.dialogflow.cx.v3.TestCase.last_test_result]
                cannot be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.TestCase:
                Represents a test case.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([test_case, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_test_case.UpdateTestCaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if test_case is not None:
            request.test_case = test_case
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_test_case,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("test_case.name", request.test_case.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def run_test_case(
        self,
        request: Union[test_case.RunTestCaseRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Kicks off a test case run.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [RunTestCaseMetadata][google.cloud.dialogflow.cx.v3.RunTestCaseMetadata]
        -  ``response``:
           [RunTestCaseResponse][google.cloud.dialogflow.cx.v3.RunTestCaseResponse]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.RunTestCaseRequest, dict]):
                The request object. The request message for
                [TestCases.RunTestCase][google.cloud.dialogflow.cx.v3.TestCases.RunTestCase].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3.types.RunTestCaseResponse`
                The response message for
                [TestCases.RunTestCase][google.cloud.dialogflow.cx.v3.TestCases.RunTestCase].

        """
        # Create or coerce a protobuf request object.
        request = test_case.RunTestCaseRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_test_case,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            test_case.RunTestCaseResponse,
            metadata_type=test_case.RunTestCaseMetadata,
        )

        # Done; return the response.
        return response

    async def batch_run_test_cases(
        self,
        request: Union[test_case.BatchRunTestCasesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Kicks off a batch run of test cases.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [BatchRunTestCasesMetadata][google.cloud.dialogflow.cx.v3.BatchRunTestCasesMetadata]
        -  ``response``:
           [BatchRunTestCasesResponse][google.cloud.dialogflow.cx.v3.BatchRunTestCasesResponse]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.BatchRunTestCasesRequest, dict]):
                The request object. The request message for
                [TestCases.BatchRunTestCases][google.cloud.dialogflow.cx.v3.TestCases.BatchRunTestCases].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3.types.BatchRunTestCasesResponse`
                The response message for
                [TestCases.BatchRunTestCases][google.cloud.dialogflow.cx.v3.TestCases.BatchRunTestCases].

        """
        # Create or coerce a protobuf request object.
        request = test_case.BatchRunTestCasesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_run_test_cases,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            test_case.BatchRunTestCasesResponse,
            metadata_type=test_case.BatchRunTestCasesMetadata,
        )

        # Done; return the response.
        return response

    async def calculate_coverage(
        self,
        request: Union[test_case.CalculateCoverageRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> test_case.CalculateCoverageResponse:
        r"""Calculates the test coverage for an agent.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.CalculateCoverageRequest, dict]):
                The request object. The request message for
                [TestCases.CalculateCoverage][google.cloud.dialogflow.cx.v3.TestCases.CalculateCoverage].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.CalculateCoverageResponse:
                The response message for
                [TestCases.CalculateCoverage][google.cloud.dialogflow.cx.v3.TestCases.CalculateCoverage].

        """
        # Create or coerce a protobuf request object.
        request = test_case.CalculateCoverageRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.calculate_coverage,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("agent", request.agent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def import_test_cases(
        self,
        request: Union[test_case.ImportTestCasesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Imports the test cases from a Cloud Storage bucket or a local
        file. It always creates new test cases and won't overwite any
        existing ones. The provided ID in the imported test case is
        neglected.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [ImportTestCasesMetadata][google.cloud.dialogflow.cx.v3.ImportTestCasesMetadata]
        -  ``response``:
           [ImportTestCasesResponse][google.cloud.dialogflow.cx.v3.ImportTestCasesResponse]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ImportTestCasesRequest, dict]):
                The request object. The request message for
                [TestCases.ImportTestCases][google.cloud.dialogflow.cx.v3.TestCases.ImportTestCases].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3.types.ImportTestCasesResponse`
                The response message for
                [TestCases.ImportTestCases][google.cloud.dialogflow.cx.v3.TestCases.ImportTestCases].

        """
        # Create or coerce a protobuf request object.
        request = test_case.ImportTestCasesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.import_test_cases,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            test_case.ImportTestCasesResponse,
            metadata_type=test_case.ImportTestCasesMetadata,
        )

        # Done; return the response.
        return response

    async def export_test_cases(
        self,
        request: Union[test_case.ExportTestCasesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports the test cases under the agent to a Cloud Storage bucket
        or a local file. Filter can be applied to export a subset of
        test cases.

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [ExportTestCasesMetadata][google.cloud.dialogflow.cx.v3.ExportTestCasesMetadata]
        -  ``response``:
           [ExportTestCasesResponse][google.cloud.dialogflow.cx.v3.ExportTestCasesResponse]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ExportTestCasesRequest, dict]):
                The request object. The request message for
                [TestCases.ExportTestCases][google.cloud.dialogflow.cx.v3.TestCases.ExportTestCases].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3.types.ExportTestCasesResponse`
                The response message for
                [TestCases.ExportTestCases][google.cloud.dialogflow.cx.v3.TestCases.ExportTestCases].

        """
        # Create or coerce a protobuf request object.
        request = test_case.ExportTestCasesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_test_cases,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            test_case.ExportTestCasesResponse,
            metadata_type=test_case.ExportTestCasesMetadata,
        )

        # Done; return the response.
        return response

    async def list_test_case_results(
        self,
        request: Union[test_case.ListTestCaseResultsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTestCaseResultsAsyncPager:
        r"""Fetches a list of results for a given test case.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ListTestCaseResultsRequest, dict]):
                The request object. The request message for
                [TestCases.ListTestCaseResults][google.cloud.dialogflow.cx.v3.TestCases.ListTestCaseResults].
            parent (:class:`str`):
                Required. The test case to list results for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/ testCases/<TestCase ID>``.
                Specify a ``-`` as a wildcard for TestCase ID to list
                results across multiple test cases.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.services.test_cases.pagers.ListTestCaseResultsAsyncPager:
                The response message for
                [TestCases.ListTestCaseResults][google.cloud.dialogflow.cx.v3.TestCases.ListTestCaseResults].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = test_case.ListTestCaseResultsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_test_case_results,
            default_timeout=None,
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
        response = pagers.ListTestCaseResultsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_test_case_result(
        self,
        request: Union[test_case.GetTestCaseResultRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> test_case.TestCaseResult:
        r"""Gets a test case result.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.GetTestCaseResultRequest, dict]):
                The request object. The request message for
                [TestCases.GetTestCaseResult][google.cloud.dialogflow.cx.v3.TestCases.GetTestCaseResult].
            name (:class:`str`):
                Required. The name of the testcase. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/testCases/<TestCase ID>/results/<TestCaseResult ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.TestCaseResult:
                Represents a result from running a
                test case in an agent environment.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = test_case.GetTestCaseResultRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_test_case_result,
            default_timeout=None,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TestCasesAsyncClient",)
