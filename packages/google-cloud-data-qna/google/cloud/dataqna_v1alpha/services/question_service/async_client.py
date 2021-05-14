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

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dataqna_v1alpha.types import question
from google.cloud.dataqna_v1alpha.types import question as gcd_question
from google.cloud.dataqna_v1alpha.types import question_service
from google.cloud.dataqna_v1alpha.types import user_feedback
from google.cloud.dataqna_v1alpha.types import user_feedback as gcd_user_feedback
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import QuestionServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import QuestionServiceGrpcAsyncIOTransport
from .client import QuestionServiceClient


class QuestionServiceAsyncClient:
    """Service to interpret natural language queries. The service allows to
    create ``Question`` resources that are interpreted and are filled
    with one or more interpretations if the question could be
    interpreted. Once a ``Question`` resource is created and has at
    least one interpretation, an interpretation can be chosen for
    execution, which triggers a query to the backend (for BigQuery, it
    will create a job). Upon successful execution of that
    interpretation, backend specific information will be returned so
    that the client can retrieve the results from the backend.

    The ``Question`` resources are named
    ``projects/*/locations/*/questions/*``.

    The ``Question`` resource has a singletion sub-resource
    ``UserFeedback`` named
    ``projects/*/locations/*/questions/*/userFeedback``, which allows
    access to user feedback.
    """

    _client: QuestionServiceClient

    DEFAULT_ENDPOINT = QuestionServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = QuestionServiceClient.DEFAULT_MTLS_ENDPOINT

    question_path = staticmethod(QuestionServiceClient.question_path)
    parse_question_path = staticmethod(QuestionServiceClient.parse_question_path)
    user_feedback_path = staticmethod(QuestionServiceClient.user_feedback_path)
    parse_user_feedback_path = staticmethod(
        QuestionServiceClient.parse_user_feedback_path
    )
    common_billing_account_path = staticmethod(
        QuestionServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        QuestionServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(QuestionServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        QuestionServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        QuestionServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        QuestionServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(QuestionServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        QuestionServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(QuestionServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        QuestionServiceClient.parse_common_location_path
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
            QuestionServiceAsyncClient: The constructed client.
        """
        return QuestionServiceClient.from_service_account_info.__func__(QuestionServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            QuestionServiceAsyncClient: The constructed client.
        """
        return QuestionServiceClient.from_service_account_file.__func__(QuestionServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> QuestionServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            QuestionServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(QuestionServiceClient).get_transport_class, type(QuestionServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, QuestionServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the question service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.QuestionServiceTransport]): The
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
        self._client = QuestionServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def get_question(
        self,
        request: question_service.GetQuestionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> question.Question:
        r"""Gets a previously created question.

        Args:
            request (:class:`google.cloud.dataqna_v1alpha.types.GetQuestionRequest`):
                The request object. A request to get a previously
                created question.
            name (:class:`str`):
                Required. The unique identifier for the question.
                Example: ``projects/foo/locations/bar/questions/1234``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataqna_v1alpha.types.Question:
                The question resource represents a
                natural language query, its settings,
                understanding generated by the system,
                and answer retrieval status. A question
                cannot be modified.

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

        request = question_service.GetQuestionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_question,
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

    async def create_question(
        self,
        request: question_service.CreateQuestionRequest = None,
        *,
        parent: str = None,
        question: gcd_question.Question = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_question.Question:
        r"""Creates a question.

        Args:
            request (:class:`google.cloud.dataqna_v1alpha.types.CreateQuestionRequest`):
                The request object. Request to create a question
                resource.
            parent (:class:`str`):
                Required. The name of the project this data source
                reference belongs to. Example:
                ``projects/foo/locations/bar``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            question (:class:`google.cloud.dataqna_v1alpha.types.Question`):
                Required. The question to create.
                This corresponds to the ``question`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataqna_v1alpha.types.Question:
                The question resource represents a
                natural language query, its settings,
                understanding generated by the system,
                and answer retrieval status. A question
                cannot be modified.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, question])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = question_service.CreateQuestionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if question is not None:
            request.question = question

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_question,
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

    async def execute_question(
        self,
        request: question_service.ExecuteQuestionRequest = None,
        *,
        name: str = None,
        interpretation_index: int = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> question.Question:
        r"""Executes an interpretation.

        Args:
            request (:class:`google.cloud.dataqna_v1alpha.types.ExecuteQuestionRequest`):
                The request object. Request to execute an
                interpretation.
            name (:class:`str`):
                Required. The unique identifier for the question.
                Example: ``projects/foo/locations/bar/questions/1234``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            interpretation_index (:class:`int`):
                Required. Index of the interpretation
                to execute.

                This corresponds to the ``interpretation_index`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataqna_v1alpha.types.Question:
                The question resource represents a
                natural language query, its settings,
                understanding generated by the system,
                and answer retrieval status. A question
                cannot be modified.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, interpretation_index])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = question_service.ExecuteQuestionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if interpretation_index is not None:
            request.interpretation_index = interpretation_index

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.execute_question,
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

    async def get_user_feedback(
        self,
        request: question_service.GetUserFeedbackRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> user_feedback.UserFeedback:
        r"""Gets previously created user feedback.

        Args:
            request (:class:`google.cloud.dataqna_v1alpha.types.GetUserFeedbackRequest`):
                The request object. Request to get user feedback.
            name (:class:`str`):
                Required. The unique identifier for the user feedback.
                User feedback is a singleton resource on a Question.
                Example:
                ``projects/foo/locations/bar/questions/1234/userFeedback``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataqna_v1alpha.types.UserFeedback:
                Feedback provided by a user.
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

        request = question_service.GetUserFeedbackRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_user_feedback,
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

    async def update_user_feedback(
        self,
        request: question_service.UpdateUserFeedbackRequest = None,
        *,
        user_feedback: gcd_user_feedback.UserFeedback = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcd_user_feedback.UserFeedback:
        r"""Updates user feedback. This creates user feedback if
        there was none before (upsert).

        Args:
            request (:class:`google.cloud.dataqna_v1alpha.types.UpdateUserFeedbackRequest`):
                The request object. Request to updates user feedback.
            user_feedback (:class:`google.cloud.dataqna_v1alpha.types.UserFeedback`):
                Required. The user feedback to
                update. This can be called even if there
                is no user feedback so far. The
                feedback's name field is used to
                identify the user feedback (and the
                corresponding question) to update.

                This corresponds to the ``user_feedback`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataqna_v1alpha.types.UserFeedback:
                Feedback provided by a user.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([user_feedback, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = question_service.UpdateUserFeedbackRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if user_feedback is not None:
            request.user_feedback = user_feedback
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_user_feedback,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("user_feedback.name", request.user_feedback.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dataqna",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("QuestionServiceAsyncClient",)
