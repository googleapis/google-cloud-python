# Copyright 2016 Google Inc.
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

"""GAX Client for interacting with the Google Cloud Vision API."""

from google.cloud.gapic.vision.v1 import image_annotator_client
from google.cloud.grpc.vision.v1 import image_annotator_pb2

from google.cloud._helpers import _to_bytes


class _GAPICVisionAPI(object):
    """Vision API for interacting with the gRPC version of Vision.

    :type client: :class:`~google.cloud.vision.client.Client`
    :param client: Instance of ``Client`` object.
    """
    def __init__(self, client=None):
        self._client = client
        self._api = image_annotator_client.ImageAnnotatorClient()


def _to_gapic_feature(feature):
    """Helper function to convert a ``Feature`` to a gRPC ``Feature``.

    :type feature: :class:`~google.cloud.vision.feature.Feature`
    :param feature: Local ``Feature`` class to be converted to gRPC ``Feature``
                    instance.

    :rtype: :class:`~google.cloud.grpc.vision.v1.image_annotator_pb2.Feature`
    :returns: gRPC ``Feature`` converted from
              :class:`~google.cloud.vision.feature.Feature`.
    """
    return image_annotator_pb2.Feature(
        type=getattr(image_annotator_pb2.Feature, feature.feature_type),
        max_results=feature.max_results)


def _to_gapic_image(image):
    """Helper function to convert an ``Image`` to a gRPC ``Image``.

    :type image: :class:`~google.cloud.vision.image.Image`
    :param image: Local ``Image`` class to be converted to gRPC ``Image``.

    :rtype: :class:`~google.cloud.grpc.vision.v1.image_annotator_pb2.Image`
    :returns: gRPC ``Image`` converted from
              :class:`~google.cloud.vision.image.Image`.
    """
    if image.content is not None:
        return image_annotator_pb2.Image(content=_to_bytes(image.content))
    if image.source is not None:
        return image_annotator_pb2.Image(
            source=image_annotator_pb2.ImageSource(
                gcs_image_uri=image.source
            ),
        )
    raise ValueError('No image content or source found.')
