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
"""Accesses the google.cloud.vision.v1 ImageAnnotator API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers

from google.cloud.vision_v1.gapic import enums
from google.cloud.vision_v1.gapic import image_annotator_client_config
from google.cloud.vision_v1.proto import image_annotator_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-vision', ).version


class ImageAnnotatorClient(object):
    """
    Service that performs Google Cloud Vision API detection tasks over client
    images, such as face, landmark, logo, label, and text detection. The
    ImageAnnotator service returns detected entities from the images.
    """

    SERVICE_ADDRESS = 'vision.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloud-vision',
    )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.cloud.vision.v1.ImageAnnotator'

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=image_annotator_client_config.config,
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
        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES,
            )

        # Create the gRPC stubs.
        self.image_annotator_stub = (
            image_annotator_pb2.ImageAnnotatorStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Write the "inner API call" methods to the class.
        # These are wrapped versions of the gRPC stub methods, with retry and
        # timeout configuration applied, called by the public methods on
        # this class.
        self._batch_annotate_images = google.api_core.gapic_v1.method.wrap_method(
            self.image_annotator_stub.BatchAnnotateImages,
            default_retry=method_configs['BatchAnnotateImages'].retry,
            default_timeout=method_configs['BatchAnnotateImages'].timeout,
            client_info=client_info,
        )

    # Service calls
    def batch_annotate_images(self,
                              requests,
                              retry=google.api_core.gapic_v1.method.DEFAULT,
                              timeout=google.api_core.gapic_v1.method.DEFAULT,
                              metadata=None):
        """
        Run image detection and annotation for a batch of images.

        Example:
            >>> from google.cloud import vision_v1
            >>>
            >>> client = vision_v1.ImageAnnotatorClient()
            >>>
            >>> requests = []
            >>>
            >>> response = client.batch_annotate_images(requests)

        Args:
            requests (list[Union[dict, ~google.cloud.vision_v1.types.AnnotateImageRequest]]): Individual image annotation requests for this batch.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.vision_v1.types.AnnotateImageRequest`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.vision_v1.types.BatchAnnotateImagesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        request = image_annotator_pb2.BatchAnnotateImagesRequest(
            requests=requests, )
        return self._batch_annotate_images(
            request, retry=retry, timeout=timeout, metadata=metadata)
