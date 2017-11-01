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

"""Image represented by either a URI or byte stream."""


from base64 import b64encode

from google.cloud.vision_v1.proto import image_annotator_pb2

from google.cloud.vision._gax import _to_gapic_image
from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _bytes_to_unicode
from google.cloud.vision.feature import Feature
from google.cloud.vision.feature import FeatureTypes


class Image(object):
    """Image representation containing information to be annotate.

    :type content: bytes
    :param content: Byte stream of an image.

    :type filename: str
    :param filename: Filename to image.

    :type source_uri: str
    :param source_uri: URL or Google Cloud Storage URI of image.

    :type client: :class:`~google.cloud.vision.client.Client`
    :param client: Instance of Vision client.
    """

    def __init__(self, client, content=None, filename=None, source_uri=None):
        sources = [source for source in (content, filename, source_uri)
                   if source is not None]
        if len(sources) != 1:
            raise ValueError(
                'Specify exactly one of "content", "filename", or '
                '"source_uri".')

        self.client = client

        if filename is not None:
            with open(filename, 'rb') as file_obj:
                content = file_obj.read()

        if content is not None:
            content = _to_bytes(content)

        self._content = content
        self._source = source_uri

    def as_dict(self):
        """Generate dictionary structure for request.

        :rtype: dict
        :returns: Dictionary with source information for image.
        """
        if self.content:
            return {
                'content': _bytes_to_unicode(b64encode(self.content))
            }
        elif self.source.startswith('gs://'):
            return {
                'source': {
                    'gcs_image_uri': self.source
                }
            }
        elif self.source.startswith(('http://', 'https://')):
            return {
                'source': {
                    'image_uri': self.source
                }
            }
        raise ValueError('No image content or source found.')

    @property
    def content(self):
        """Base64 encoded image content.

        :rtype: str
        :returns: Base64 encoded image bytes.
        """
        return self._content

    @property
    def source(self):
        """Google Cloud Storage URI.

        :rtype: str
        :returns: String of Google Cloud Storage URI.
        """
        return self._source

    def _detect_annotation(self, images):
        """Generic method for detecting annotations.

        :type images: list
        :param images: List of :class:`~google.cloud.vision.image.Image`.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.annotations.Annotations`.
        """
        return self.client._vision_api.annotate(images)

    def _detect_annotation_from_pb(self, requests_pb=None):
        """Helper for pre-made requests.

        :type requests_pb: list
        :param requests_pb: List of :class:`google.cloud.vision_v1.proto.\
                            image_annotator_pb2.AnnotateImageRequest`

        :rtype: :class:`~google.cloud.vision.annotations.Annotations`
        :returns: Instance of ``Annotations``.
        """
        return self.client._vision_api.annotate(self, requests_pb=requests_pb)

    def detect(self, features):
        """Detect multiple feature types.

        :type features: list of :class:`~google.cloud.vision.feature.Feature`
        :param features: List of the ``Feature`` indication the type of
                         annotation to perform.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        images = ((self, features),)
        return self._detect_annotation(images)

    def detect_crop_hints(self, aspect_ratios=None, limit=10):
        """Detect crop hints in image.

        :type aspect_ratios: list
        :param aspect_ratios: (Optional) List of floats i.e. 4/3 == 1.33333. A
                              maximum of 16 aspect ratios can be given.

        :type limit: int
        :param limit: (Optional) The number of crop hints to detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.crop_hint.CropHints`.
        """
        feature_type = image_annotator_pb2.Feature.CROP_HINTS
        feature = image_annotator_pb2.Feature(type=feature_type,
                                              max_results=limit)
        image = _to_gapic_image(self)
        crop_hints_params = image_annotator_pb2.CropHintsParams(
            aspect_ratios=aspect_ratios)
        image_context = image_annotator_pb2.ImageContext(
            crop_hints_params=crop_hints_params)
        request = image_annotator_pb2.AnnotateImageRequest(
            image=image, features=[feature], image_context=image_context)

        annotations = self._detect_annotation_from_pb([request])
        return annotations[0].crop_hints

    def detect_faces(self, limit=10):
        """Detect faces in image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.face.Face`.
        """
        features = [Feature(FeatureTypes.FACE_DETECTION, limit)]
        annotations = self.detect(features)
        return annotations[0].faces

    def detect_full_text(self, language_hints=None, limit=10):
        """Detect a full document's text.

        :type language_hints: list
        :param language_hints: (Optional) A list of BCP-47 language codes. See
                               https://cloud.google.com/vision/docs/languages

        :type limit: int
        :param limit: (Optional) The number of documents to detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.text.TextAnnotation`.
        """
        feature_type = image_annotator_pb2.Feature.DOCUMENT_TEXT_DETECTION
        feature = image_annotator_pb2.Feature(type=feature_type,
                                              max_results=limit)
        image = _to_gapic_image(self)
        image_context = image_annotator_pb2.ImageContext(
            language_hints=language_hints)
        request = image_annotator_pb2.AnnotateImageRequest(
            image=image, features=[feature], image_context=image_context)
        annotations = self._detect_annotation_from_pb([request])
        return annotations[0].full_texts

    def detect_labels(self, limit=10):
        """Detect labels that describe objects in an image.

        :type limit: int
        :param limit: The maximum number of labels to try and detect.

        :rtype: list
        :returns: List of :class:`~google.cloud.vision.entity.EntityAnnotation`
        """
        features = [Feature(FeatureTypes.LABEL_DETECTION, limit)]
        annotations = self.detect(features)
        return annotations[0].labels

    def detect_landmarks(self, limit=10):
        """Detect landmarks in an image.

        :type limit: int
        :param limit: The maximum number of landmarks to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.LANDMARK_DETECTION, limit)]
        annotations = self.detect(features)
        return annotations[0].landmarks

    def detect_logos(self, limit=10):
        """Detect logos in an image.

        :type limit: int
        :param limit: The maximum number of logos to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.LOGO_DETECTION, limit)]
        annotations = self.detect(features)
        return annotations[0].logos

    def detect_properties(self, limit=10):
        """Detect the color properties of an image.

        :type limit: int
        :param limit: The maximum number of image properties to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.color.ImagePropertiesAnnotation`.
        """
        features = [Feature(FeatureTypes.IMAGE_PROPERTIES, limit)]
        annotations = self.detect(features)
        return annotations[0].properties

    def detect_safe_search(self, limit=10):
        """Retreive safe search properties from an image.

        :type limit: int
        :param limit: The number of faces to try and detect.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.sage.SafeSearchAnnotation`.
        """
        features = [Feature(FeatureTypes.SAFE_SEARCH_DETECTION, limit)]
        annotations = self.detect(features)
        return annotations[0].safe_searches

    def detect_text(self, limit=10):
        """Detect text in an image.

        :type limit: int
        :param limit: The maximum instances of text to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.TEXT_DETECTION, limit)]
        annotations = self.detect(features)
        return annotations[0].texts

    def detect_web(self, limit=10):
        """Detect similar images elsewhere on the web.

        :type limit: int
        :param limit: The maximum instances of text to find.

        :rtype: list
        :returns: List of
                  :class:`~google.cloud.vision.entity.EntityAnnotation`.
        """
        features = [Feature(FeatureTypes.WEB_DETECTION, limit)]
        annotations = self.detect(features)
        return annotations[0].web
