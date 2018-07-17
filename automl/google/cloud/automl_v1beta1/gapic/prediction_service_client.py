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
"""Accesses the google.cloud.automl.v1beta1 PredictionService API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.automl_v1beta1.gapic import enums
from google.cloud.automl_v1beta1.gapic import prediction_service_client_config
from google.cloud.automl_v1beta1.proto import data_items_pb2
from google.cloud.automl_v1beta1.proto import prediction_service_pb2
from google.cloud.automl_v1beta1.proto import prediction_service_pb2_grpc

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-automl', ).version


class PredictionServiceClient(object):
    """AutoML Prediction API."""

    SERVICE_ADDRESS = 'automl.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.automl.v1beta1.PredictionService'

    @classmethod
    def model_path(cls, project, location, model):
        """Return a fully-qualified model string."""
        return google.api_core.path_template.expand(
            'projects/{project}/locations/{location}/models/{model}',
            project=project,
            location=location,
            model=model,
        )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=prediction_service_client_config.config,
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
        self.channel = channel
        if self.channel is None:
            self.channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self._prediction_service_stub = (
            prediction_service_pb2_grpc.PredictionServiceStub(self.channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        self._inner_api_calls = {}

    def _intercept_channel(self, *interceptors):
        """ Experimental. Bind gRPC interceptors to the gRPC channel.

        Args:
            interceptors (*Union[grpc.UnaryUnaryClientInterceptor, grpc.UnaryStreamingClientInterceptor, grpc.StreamingUnaryClientInterceptor, grpc.StreamingStreamingClientInterceptor]):
              Zero or more gRPC interceptors. Interceptors are given control in the order
              they are listed.
        Raises:
            TypeError: If interceptor does not derive from any of
              UnaryUnaryClientInterceptor,
              UnaryStreamClientInterceptor,
              StreamUnaryClientInterceptor, or
              StreamStreamClientInterceptor.
        """
        self.channel = grpc.intercept_channel(self.channel, *interceptors)
        self._prediction_service_stub = (
            prediction_service_pb2_grpc.PredictionServiceStub(self.channel))
        self._inner_api_calls.clear()

    # Service calls
    def predict(self,
                name,
                payload,
                params=None,
                retry=google.api_core.gapic_v1.method.DEFAULT,
                timeout=google.api_core.gapic_v1.method.DEFAULT,
                metadata=None):
        """
        Perform a prediction.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.PredictionServiceClient()
            >>>
            >>> name = client.model_path('[PROJECT]', '[LOCATION]', '[MODEL]')
            >>>
            >>> # TODO: Initialize ``payload``:
            >>> payload = {}
            >>>
            >>> response = client.predict(name, payload)

        Args:
            name (str): Name of the model requested to serve the prediction.
            payload (Union[dict, ~google.cloud.automl_v1beta1.types.ExamplePayload]): Required.
                Payload to perform a prediction on. The payload must match the
                problem type that the model was trained to solve.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.automl_v1beta1.types.ExamplePayload`
            params (dict[str -> str]): Additional domain-specific parameters, any string must be up to 25000
                characters long.

                *  For Translation:

                   ``translation_allow_fallback`` - If specified, AutoML will fallback to
                   use a Google translation model for translation requests if the
                   the specified AutoML translation model cannot serve the request.
                   The ``PredictResponse.metadata`` field provides additional data to the
                   caller.

                *  For Image Classification:

                   ``score_threshold`` - (float) A value from 0.0 to 1.0. When the model
                ::

                    makes predictions for an
                    image, it will only produce results that have at least this confidence
                    score threshold. The default is 0.5.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.PredictResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if 'predict' not in self._inner_api_calls:
            self._inner_api_calls[
                'predict'] = google.api_core.gapic_v1.method.wrap_method(
                    self._prediction_service_stub.Predict,
                    default_retry=self._method_configs['Predict'].retry,
                    default_timeout=self._method_configs['Predict'].timeout,
                    client_info=self._client_info,
                )

        request = prediction_service_pb2.PredictRequest(
            name=name,
            payload=payload,
            params=params,
        )
        return self._inner_api_calls['predict'](
            request, retry=retry, timeout=timeout, metadata=metadata)
