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

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.automl_v1.types import annotation_payload
from google.cloud.automl_v1.types import data_items
from google.cloud.automl_v1.types import io
from google.cloud.automl_v1.types import operations
from google.cloud.automl_v1.types import prediction_service
from .transports.base import PredictionServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import PredictionServiceGrpcAsyncIOTransport
from .client import PredictionServiceClient


class PredictionServiceAsyncClient:
    """AutoML Prediction API.

    On any input that is documented to expect a string parameter in
    snake_case or kebab-case, either of those cases is accepted.
    """

    _client: PredictionServiceClient

    DEFAULT_ENDPOINT = PredictionServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = PredictionServiceClient.DEFAULT_MTLS_ENDPOINT

    model_path = staticmethod(PredictionServiceClient.model_path)
    parse_model_path = staticmethod(PredictionServiceClient.parse_model_path)
    common_billing_account_path = staticmethod(
        PredictionServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        PredictionServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(PredictionServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        PredictionServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        PredictionServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        PredictionServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(PredictionServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        PredictionServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(PredictionServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        PredictionServiceClient.parse_common_location_path
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
            PredictionServiceAsyncClient: The constructed client.
        """
        return PredictionServiceClient.from_service_account_info.__func__(PredictionServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            PredictionServiceAsyncClient: The constructed client.
        """
        return PredictionServiceClient.from_service_account_file.__func__(PredictionServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> PredictionServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            PredictionServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(PredictionServiceClient).get_transport_class, type(PredictionServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, PredictionServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the prediction service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.PredictionServiceTransport]): The
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
        self._client = PredictionServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def predict(
        self,
        request: prediction_service.PredictRequest = None,
        *,
        name: str = None,
        payload: data_items.ExamplePayload = None,
        params: Sequence[prediction_service.PredictRequest.ParamsEntry] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> prediction_service.PredictResponse:
        r"""Perform an online prediction. The prediction result is directly
        returned in the response. Available for following ML scenarios,
        and their expected request payloads:

        AutoML Vision Classification

        -  An image in .JPEG, .GIF or .PNG format, image_bytes up to
           30MB.

        AutoML Vision Object Detection

        -  An image in .JPEG, .GIF or .PNG format, image_bytes up to
           30MB.

        AutoML Natural Language Classification

        -  A TextSnippet up to 60,000 characters, UTF-8 encoded or a
           document in .PDF, .TIF or .TIFF format with size upto 2MB.

        AutoML Natural Language Entity Extraction

        -  A TextSnippet up to 10,000 characters, UTF-8 NFC encoded or a
           document in .PDF, .TIF or .TIFF format with size upto 20MB.

        AutoML Natural Language Sentiment Analysis

        -  A TextSnippet up to 60,000 characters, UTF-8 encoded or a
           document in .PDF, .TIF or .TIFF format with size upto 2MB.

        AutoML Translation

        -  A TextSnippet up to 25,000 characters, UTF-8 encoded.

        AutoML Tables

        -  A row with column values matching the columns of the model,
           up to 5MB. Not available for FORECASTING ``prediction_type``.

        Args:
            request (:class:`google.cloud.automl_v1.types.PredictRequest`):
                The request object. Request message for
                [PredictionService.Predict][google.cloud.automl.v1.PredictionService.Predict].
            name (:class:`str`):
                Required. Name of the model requested
                to serve the prediction.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            payload (:class:`google.cloud.automl_v1.types.ExamplePayload`):
                Required. Payload to perform a
                prediction on. The payload must match
                the problem type that the model was
                trained to solve.

                This corresponds to the ``payload`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            params (:class:`Sequence[google.cloud.automl_v1.types.PredictRequest.ParamsEntry]`):
                Additional domain-specific parameters, any string must
                be up to 25000 characters long.

                AutoML Vision Classification

                ``score_threshold`` : (float) A value from 0.0 to 1.0.
                When the model makes predictions for an image, it will
                only produce results that have at least this confidence
                score. The default is 0.5.

                AutoML Vision Object Detection

                ``score_threshold`` : (float) When Model detects objects
                on the image, it will only produce bounding boxes which
                have at least this confidence score. Value in 0 to 1
                range, default is 0.5.

                ``max_bounding_box_count`` : (int64) The maximum number
                of bounding boxes returned. The default is 100. The
                number of returned bounding boxes might be limited by
                the server.

                AutoML Tables

                ``feature_importance`` : (boolean) Whether

                [feature_importance][google.cloud.automl.v1.TablesModelColumnInfo.feature_importance]
                is populated in the returned list of
                [TablesAnnotation][google.cloud.automl.v1.TablesAnnotation]
                objects. The default is false.

                This corresponds to the ``params`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.automl_v1.types.PredictResponse:
                Response message for
                [PredictionService.Predict][google.cloud.automl.v1.PredictionService.Predict].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, payload, params])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = prediction_service.PredictRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if payload is not None:
            request.payload = payload

        if params:
            request.params.update(params)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.predict,
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

    async def batch_predict(
        self,
        request: prediction_service.BatchPredictRequest = None,
        *,
        name: str = None,
        input_config: io.BatchPredictInputConfig = None,
        output_config: io.BatchPredictOutputConfig = None,
        params: Sequence[prediction_service.BatchPredictRequest.ParamsEntry] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Perform a batch prediction. Unlike the online
        [Predict][google.cloud.automl.v1.PredictionService.Predict],
        batch prediction result won't be immediately available in the
        response. Instead, a long running operation object is returned.
        User can poll the operation result via
        [GetOperation][google.longrunning.Operations.GetOperation]
        method. Once the operation is done,
        [BatchPredictResult][google.cloud.automl.v1.BatchPredictResult]
        is returned in the
        [response][google.longrunning.Operation.response] field.
        Available for following ML scenarios:

        -  AutoML Vision Classification
        -  AutoML Vision Object Detection
        -  AutoML Video Intelligence Classification
        -  AutoML Video Intelligence Object Tracking \* AutoML Natural
           Language Classification
        -  AutoML Natural Language Entity Extraction
        -  AutoML Natural Language Sentiment Analysis
        -  AutoML Tables

        Args:
            request (:class:`google.cloud.automl_v1.types.BatchPredictRequest`):
                The request object. Request message for
                [PredictionService.BatchPredict][google.cloud.automl.v1.PredictionService.BatchPredict].
            name (:class:`str`):
                Required. Name of the model requested
                to serve the batch prediction.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            input_config (:class:`google.cloud.automl_v1.types.BatchPredictInputConfig`):
                Required. The input configuration for
                batch prediction.

                This corresponds to the ``input_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            output_config (:class:`google.cloud.automl_v1.types.BatchPredictOutputConfig`):
                Required. The Configuration
                specifying where output predictions
                should be written.

                This corresponds to the ``output_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            params (:class:`Sequence[google.cloud.automl_v1.types.BatchPredictRequest.ParamsEntry]`):
                Additional domain-specific parameters for the
                predictions, any string must be up to 25000 characters
                long.

                AutoML Natural Language Classification

                ``score_threshold`` : (float) A value from 0.0 to 1.0.
                When the model makes predictions for a text snippet, it
                will only produce results that have at least this
                confidence score. The default is 0.5.

                AutoML Vision Classification

                ``score_threshold`` : (float) A value from 0.0 to 1.0.
                When the model makes predictions for an image, it will
                only produce results that have at least this confidence
                score. The default is 0.5.

                AutoML Vision Object Detection

                ``score_threshold`` : (float) When Model detects objects
                on the image, it will only produce bounding boxes which
                have at least this confidence score. Value in 0 to 1
                range, default is 0.5.

                ``max_bounding_box_count`` : (int64) The maximum number
                of bounding boxes returned per image. The default is
                100, the number of bounding boxes returned might be
                limited by the server. AutoML Video Intelligence
                Classification

                ``score_threshold`` : (float) A value from 0.0 to 1.0.
                When the model makes predictions for a video, it will
                only produce results that have at least this confidence
                score. The default is 0.5.

                ``segment_classification`` : (boolean) Set to true to
                request segment-level classification. AutoML Video
                Intelligence returns labels and their confidence scores
                for the entire segment of the video that user specified
                in the request configuration. The default is true.

                ``shot_classification`` : (boolean) Set to true to
                request shot-level classification. AutoML Video
                Intelligence determines the boundaries for each camera
                shot in the entire segment of the video that user
                specified in the request configuration. AutoML Video
                Intelligence then returns labels and their confidence
                scores for each detected shot, along with the start and
                end time of the shot. The default is false.

                WARNING: Model evaluation is not done for this
                classification type, the quality of it depends on
                training data, but there are no metrics provided to
                describe that quality.

                ``1s_interval_classification`` : (boolean) Set to true
                to request classification for a video at one-second
                intervals. AutoML Video Intelligence returns labels and
                their confidence scores for each second of the entire
                segment of the video that user specified in the request
                configuration. The default is false.

                WARNING: Model evaluation is not done for this
                classification type, the quality of it depends on
                training data, but there are no metrics provided to
                describe that quality.

                AutoML Video Intelligence Object Tracking

                ``score_threshold`` : (float) When Model detects objects
                on video frames, it will only produce bounding boxes
                which have at least this confidence score. Value in 0 to
                1 range, default is 0.5.

                ``max_bounding_box_count`` : (int64) The maximum number
                of bounding boxes returned per image. The default is
                100, the number of bounding boxes returned might be
                limited by the server.

                ``min_bounding_box_size`` : (float) Only bounding boxes
                with shortest edge at least that long as a relative
                value of video frame size are returned. Value in 0 to 1
                range. Default is 0.

                This corresponds to the ``params`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.automl_v1.types.BatchPredictResult` Result of the Batch Predict. This message is returned in
                   [response][google.longrunning.Operation.response] of
                   the operation returned by the
                   [PredictionService.BatchPredict][google.cloud.automl.v1.PredictionService.BatchPredict].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, input_config, output_config, params])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = prediction_service.BatchPredictRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if input_config is not None:
            request.input_config = input_config
        if output_config is not None:
            request.output_config = output_config

        if params:
            request.params.update(params)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.batch_predict,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            prediction_service.BatchPredictResult,
            metadata_type=operations.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-automl",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("PredictionServiceAsyncClient",)
