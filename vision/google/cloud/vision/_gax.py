# Copyright 2016 Google LLC
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

from google.cloud.vision_v1.gapic import image_annotator_client
from google.cloud.vision_v1.proto import image_annotator_pb2

from google.cloud.vision import __version__
from google.cloud.vision.annotations import Annotations


class _GAPICVisionAPI(object):
    """Vision API for interacting with the gRPC version of Vision.

    :type client: :class:`~google.cloud.vision.client.Client`
    :param client: Instance of ``Client`` object.
    """
    def __init__(self, client=None):
        self._client = client
        self._annotator_client = image_annotator_client.ImageAnnotatorClient(
            credentials=client._credentials, lib_name='gccl',
            lib_version=__version__)

    def annotate(self, images=None, requests_pb=None):
        """Annotate images through GAX.

        :type images: list
        :param images: List containing pairs of
                       :class:`~google.cloud.vision.image.Image` and
                       :class:`~google.cloud.vision.feature.Feature`.
                       e.g. [(image, [feature_one, feature_two]),]

        :type requests_pb: list
        :param requests_pb: List of :class:`google.cloud.vision_v1.proto.\
                            image_annotator_pb2.AnnotateImageRequest`

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.annotations.Annotations`.
        """
        if any([images, requests_pb]) is False:
            return []

        if requests_pb is None:
            requests = []
            for image, features in images:
                gapic_features = [_to_gapic_feature(feature)
                                  for feature in features]
                gapic_image = _to_gapic_image(image)
                request = image_annotator_pb2.AnnotateImageRequest(
                    image=gapic_image, features=gapic_features)
                requests.append(request)
        else:
            requests = requests_pb

        annotator_client = self._annotator_client
        responses = annotator_client.batch_annotate_images(requests).responses
        return [Annotations.from_pb(response) for response in responses]


def _to_gapic_feature(feature):
    """Helper function to convert a ``Feature`` to a gRPC ``Feature``.

    :type feature: :class:`~google.cloud.vision.feature.Feature`
    :param feature: Local ``Feature`` class to be converted to gRPC ``Feature``
                    instance.

    :rtype: :class:`~google.cloud.vision_v1.proto.image_annotator_pb2.Feature`
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

    :rtype: :class:`~google.cloud.vision_v1.proto.image_annotator_pb2.Image`
    :returns: gRPC ``Image`` converted from
              :class:`~google.cloud.vision.image.Image`.
    """
    if image.content is not None:
        return image_annotator_pb2.Image(content=image.content)
    if image.source is not None:
        if image.source.startswith('gs://'):
            return image_annotator_pb2.Image(
                source=image_annotator_pb2.ImageSource(
                    gcs_image_uri=image.source
                ),
            )
        elif image.source.startswith(('http://', 'https://')):
            return image_annotator_pb2.Image(
                source=image_annotator_pb2.ImageSource(
                    image_uri=image.source
                ),
            )
    raise ValueError('No image content or source found.')
