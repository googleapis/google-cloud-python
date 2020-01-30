# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Accesses the google.cloud.automl.v1 PredictionService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.path_template
import grpc

from google.cloud.automl_v1.gapic import enums
from google.cloud.automl_v1.gapic import prediction_service_client_config
from google.cloud.automl_v1.gapic.transports import prediction_service_grpc_transport
from google.cloud.automl_v1.proto import annotation_spec_pb2
from google.cloud.automl_v1.proto import data_items_pb2
from google.cloud.automl_v1.proto import dataset_pb2
from google.cloud.automl_v1.proto import image_pb2
from google.cloud.automl_v1.proto import io_pb2
from google.cloud.automl_v1.proto import model_evaluation_pb2
from google.cloud.automl_v1.proto import model_pb2
from google.cloud.automl_v1.proto import operations_pb2 as proto_operations_pb2
from google.cloud.automl_v1.proto import prediction_service_pb2
from google.cloud.automl_v1.proto import prediction_service_pb2_grpc
from google.cloud.automl_v1.proto import service_pb2
from google.cloud.automl_v1.proto import service_pb2_grpc
from google.longrunning import operations_pb2 as longrunning_operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-automl").version


class PredictionServiceClient(object):
    """
    AutoML Prediction API.

    On any input that is documented to expect a string parameter in
    snake\_case or kebab-case, either of those cases is accepted.
    """

    SERVICE_ADDRESS = "automl.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.cloud.automl.v1.PredictionService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            PredictionServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def model_path(cls, project, location, model):
        """Return a fully-qualified model string."""
        return google.api_core.path_template.expand(
            "projects/{project}/locations/{location}/models/{model}",
            project=project,
            location=location,
            model=model,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.PredictionServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.PredictionServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = prediction_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=prediction_service_grpc_transport.PredictionServiceGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = prediction_service_grpc_transport.PredictionServiceGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def predict(
        self,
        name,
        payload,
        params=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Perform an online prediction. The prediction result will be directly
        returned in the response. Available for following ML problems, and their
        expected request payloads:

        -  Image Classification - Image in .JPEG, .GIF or .PNG format,
           image\_bytes up to 30MB.
        -  Image Object Detection - Image in .JPEG, .GIF or .PNG format,
           image\_bytes up to 30MB.
        -  Text Classification - TextSnippet, content up to 60,000 characters,
           UTF-8 encoded.
        -  Text Extraction - TextSnippet, content up to 30,000 characters, UTF-8
           NFC encoded.
        -  Translation - TextSnippet, content up to 25,000 characters, UTF-8
           encoded.
        -  Text Sentiment - TextSnippet, content up 500 characters, UTF-8
           encoded.

        Example:
            >>> from google.cloud import automl_v1
            >>>
            >>> client = automl_v1.PredictionServiceClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> # TODO: Initialize `payload`:
            >>> payload = {}
            >>>
            >>> response = client.predict(name, payload)

        Args:
            name (str): Name of the model requested to serve the prediction.
            payload (Union[dict, ~google.cloud.automl_v1.types.ExamplePayload]): Required. Payload to perform a prediction on. The payload must match the
                problem type that the model was trained to solve.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1.types.ExamplePayload`
            params (dict[str -> str]): Additional domain-specific parameters, any string must be up to 25000
                characters long.

                -  For Image Classification:

                   ``score_threshold`` - (float) A value from 0.0 to 1.0. When the model
                   makes predictions for an image, it will only produce results that
                   have at least this confidence score. The default is 0.5.

                -  For Image Object Detection: ``score_threshold`` - (float) When Model
                   detects objects on the image, it will only produce bounding boxes
                   which have at least this confidence score. Value in 0 to 1 range,
                   default is 0.5. ``max_bounding_box_count`` - (int64) No more than
                   this number of bounding boxes will be returned in the response.
                   Default is 100, the requested value may be limited by server.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1.types.PredictResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "predict" not in self._inner_api_calls:
            self._inner_api_calls[
                "predict"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.predict,
                default_retry=self._method_configs["Predict"].retry,
                default_timeout=self._method_configs["Predict"].timeout,
                client_info=self._client_info,
            )

        request = prediction_service_pb2.PredictRequest(
            name=name, payload=payload, params=params
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["predict"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def batch_predict(
        self,
        name,
        input_config,
        output_config,
        params=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Perform a batch prediction. Unlike the online ``Predict``, batch
        prediction result won't be immediately available in the response.
        Instead, a long running operation object is returned. User can poll the
        operation result via ``GetOperation`` method. Once the operation is
        done, ``BatchPredictResult`` is returned in the ``response`` field.
        Available for following ML problems:

        -  Image Classification
        -  Image Object Detection
        -  Text Extraction

        Example:
            >>> from google.cloud import automl_v1
            >>>
            >>> client = automl_v1.PredictionServiceClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> # TODO: Initialize `input_config`:
            >>> input_config = {}
            >>>
            >>> # TODO: Initialize `output_config`:
            >>> output_config = {}
            >>>
            >>> response = client.batch_predict(name, input_config, output_config)
            >>>
            >>> def callback(operation_future):
            ...     # Handle result.
            ...     result = operation_future.result()
            >>>
            >>> response.add_done_callback(callback)
            >>>
            >>> # Handle metadata.
            >>> metadata = response.metadata()

        Args:
            name (str): Name of the model requested to serve the batch prediction.
            input_config (Union[dict, ~google.cloud.automl_v1.types.BatchPredictInputConfig]): Required. The input configuration for batch prediction.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1.types.BatchPredictInputConfig`
            output_config (Union[dict, ~google.cloud.automl_v1.types.BatchPredictOutputConfig]): Required. The Configuration specifying where output predictions should
                be written.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1.types.BatchPredictOutputConfig`
            params (dict[str -> str]): Additional domain-specific parameters for the predictions, any string
                must be up to 25000 characters long.

                -  For Text Classification:

                   ``score_threshold`` - (float) A value from 0.0 to 1.0. When the model
                   makes predictions for a text snippet, it will only produce results
                   that have at least this confidence score. The default is 0.5.

                -  For Image Classification:

                   ``score_threshold`` - (float) A value from 0.0 to 1.0. When the model
                   makes predictions for an image, it will only produce results that
                   have at least this confidence score. The default is 0.5.

                -  For Image Object Detection:

                   ``score_threshold`` - (float) When Model detects objects on the
                   image, it will only produce bounding boxes which have at least this
                   confidence score. Value in 0 to 1 range, default is 0.5.
                   ``max_bounding_box_count`` - (int64) No more than this number of
                   bounding boxes will be produced per image. Default is 100, the
                   requested value may be limited by server.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_predict" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_predict"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_predict,
                default_retry=self._method_configs["BatchPredict"].retry,
                default_timeout=self._method_configs["BatchPredict"].timeout,
                client_info=self._client_info,
            )

        request = prediction_service_pb2.BatchPredictRequest(
            name=name,
            input_config=input_config,
            output_config=output_config,
            params=params,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        operation = self._inner_api_calls["batch_predict"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            prediction_service_pb2.BatchPredictResult,
            metadata_type=proto_operations_pb2.OperationMetadata,
        )
