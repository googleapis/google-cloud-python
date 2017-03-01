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

import unittest

import mock


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestGAXClient(unittest.TestCase):
    def _get_target_class(self):
        from google.cloud.vision._gax import _GAPICVisionAPI

        return _GAPICVisionAPI

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_ctor(self):
        client = mock.Mock(
            _credentials=_make_credentials(),
            spec=['_credentials'],
        )
        with mock.patch('google.cloud.vision._gax.image_annotator_client.'
                        'ImageAnnotatorClient'):
            api = self._make_one(client)
        self.assertIs(api._client, client)

    def test_gapic_credentials(self):
        from google.cloud.gapic.vision.v1.image_annotator_client import (
            ImageAnnotatorClient)

        from google.cloud.vision import Client

        # Mock the GAPIC ImageAnnotatorClient, whose arguments we
        # want to check.
        with mock.patch.object(ImageAnnotatorClient, '__init__') as iac:
            iac.return_value = None

            # Create the GAX client.
            credentials = _make_credentials()
            client = Client(credentials=credentials, project='foo')
            self._make_one(client=client)

            # Assert that the GAPIC constructor was called once, and
            # that the credentials were sent.
            iac.assert_called_once()
            _, _, kwargs = iac.mock_calls[0]
            self.assertIs(kwargs['credentials'], credentials)

    def test_kwarg_lib_name(self):
        from google.cloud.gapic.vision.v1.image_annotator_client import (
            ImageAnnotatorClient)
        from google.cloud.vision import __version__
        from google.cloud.vision import Client

        # Mock the GAPIC ImageAnnotatorClient, whose arguments we
        # want to check.
        with mock.patch.object(ImageAnnotatorClient, '__init__') as iac:
            iac.return_value = None

            # Create the GAX client.
            client = Client(credentials=_make_credentials(), project='foo')
            self._make_one(client=client)

            # Assert that the GAPIC constructor was called once, and
            # that lib_name and lib_version were sent.
            iac.assert_called_once()
            _, _, kwargs = iac.mock_calls[0]
            self.assertEqual(kwargs['lib_name'], 'gccl')
            self.assertEqual(kwargs['lib_version'], __version__)

    def test_annotation(self):
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.vision.image import Image

        client = mock.Mock(spec_set=['_credentials'])
        feature = Feature(FeatureTypes.LABEL_DETECTION, 5)
        image_content = b'abc 1 2 3'
        image = Image(client, content=image_content)
        with mock.patch('google.cloud.vision._gax.image_annotator_client.'
                        'ImageAnnotatorClient'):
            gax_api = self._make_one(client)

        mock_response = {
            'batch_annotate_images.return_value':
            mock.Mock(responses=['mock response data']),
        }

        gax_api._annotator_client = mock.Mock(
            spec_set=['batch_annotate_images'], **mock_response)

        with mock.patch('google.cloud.vision._gax.Annotations') as mock_anno:
            images = ((image, [feature]),)
            gax_api.annotate(images)
            mock_anno.from_pb.assert_called_with('mock response data')
        gax_api._annotator_client.batch_annotate_images.assert_called()

    def test_annotate_no_requests(self):
        client = mock.Mock(spec_set=['_credentials'])
        with mock.patch('google.cloud.vision._gax.image_annotator_client.'
                        'ImageAnnotatorClient'):
            gax_api = self._make_one(client)

        response = gax_api.annotate()
        self.assertEqual(response, [])
        gax_api._annotator_client.batch_annotate_images.assert_not_called()

    def test_annotate_no_results(self):
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.vision.image import Image

        client = mock.Mock(spec_set=['_credentials'])
        feature = Feature(FeatureTypes.LABEL_DETECTION, 5)
        image_content = b'abc 1 2 3'
        image = Image(client, content=image_content)
        with mock.patch('google.cloud.vision._gax.image_annotator_client.'
                        'ImageAnnotatorClient'):
            gax_api = self._make_one(client)

        mock_response = {
            'batch_annotate_images.return_value': mock.Mock(responses=[]),
        }

        gax_api._annotator_client = mock.Mock(
            spec_set=['batch_annotate_images'], **mock_response)
        with mock.patch('google.cloud.vision._gax.Annotations'):
            images = ((image, [feature]),)
            response = gax_api.annotate(images)
        self.assertEqual(len(response), 0)
        self.assertIsInstance(response, list)

        gax_api._annotator_client.batch_annotate_images.assert_called()

    def test_annotate_multiple_results(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2
        from google.cloud.vision.annotations import Annotations
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.vision.image import Image

        client = mock.Mock(spec_set=['_credentials'])
        feature = Feature(FeatureTypes.LABEL_DETECTION, 5)
        image_content = b'abc 1 2 3'
        image = Image(client, content=image_content)
        with mock.patch('google.cloud.vision._gax.image_annotator_client.'
                        'ImageAnnotatorClient'):
            gax_api = self._make_one(client)

        responses = [
            image_annotator_pb2.AnnotateImageResponse(),
            image_annotator_pb2.AnnotateImageResponse(),
        ]
        response = image_annotator_pb2.BatchAnnotateImagesResponse(
            responses=responses)

        gax_api._annotator_client = mock.Mock(
            spec_set=['batch_annotate_images'])
        gax_api._annotator_client.batch_annotate_images.return_value = response
        images = ((image, [feature]),)
        responses = gax_api.annotate(images)

        self.assertEqual(len(responses), 2)
        self.assertIsInstance(responses[0], Annotations)
        self.assertIsInstance(responses[1], Annotations)
        gax_api._annotator_client.batch_annotate_images.assert_called()

    def test_annotate_with_pb_requests_results(self):
        from google.cloud.proto.vision.v1 import image_annotator_pb2
        from google.cloud.vision.annotations import Annotations

        client = mock.Mock(spec_set=['_credentials'])

        feature_type = image_annotator_pb2.Feature.CROP_HINTS
        feature = image_annotator_pb2.Feature(type=feature_type, max_results=2)

        image_content = b'abc 1 2 3'
        image = image_annotator_pb2.Image(content=image_content)

        aspect_ratios = [1.3333, 1.7777]
        crop_hints_params = image_annotator_pb2.CropHintsParams(
            aspect_ratios=aspect_ratios)
        image_context = image_annotator_pb2.ImageContext(
            crop_hints_params=crop_hints_params)
        request = image_annotator_pb2.AnnotateImageRequest(
            image=image, features=[feature], image_context=image_context)

        with mock.patch('google.cloud.vision._gax.image_annotator_client.'
                        'ImageAnnotatorClient'):
            gax_api = self._make_one(client)

        responses = [
            image_annotator_pb2.AnnotateImageResponse(),
            image_annotator_pb2.AnnotateImageResponse(),
        ]
        response = image_annotator_pb2.BatchAnnotateImagesResponse(
            responses=responses)

        gax_api._annotator_client = mock.Mock(
            spec_set=['batch_annotate_images'])
        gax_api._annotator_client.batch_annotate_images.return_value = response
        responses = gax_api.annotate(requests_pb=[request])

        self.assertEqual(len(responses), 2)
        for annotation in responses:
            self.assertIsInstance(annotation, Annotations)
        gax_api._annotator_client.batch_annotate_images.assert_called()


class Test__to_gapic_feature(unittest.TestCase):
    def _call_fut(self, feature):
        from google.cloud.vision._gax import _to_gapic_feature
        return _to_gapic_feature(feature)

    def test__to_gapic_feature(self):
        from google.cloud.vision.feature import Feature
        from google.cloud.vision.feature import FeatureTypes
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        feature = Feature(FeatureTypes.LABEL_DETECTION, 5)
        feature_pb = self._call_fut(feature)
        self.assertIsInstance(feature_pb, image_annotator_pb2.Feature)
        self.assertEqual(feature_pb.type, 4)
        self.assertEqual(feature_pb.max_results, 5)


class Test__to_gapic_image(unittest.TestCase):
    def _call_fut(self, image):
        from google.cloud.vision._gax import _to_gapic_image

        return _to_gapic_image(image)

    def test__to_gapic_image_content(self):
        from google.cloud.vision.image import Image
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        image_content = b'abc 1 2 3'
        client = object()
        image = Image(client, content=image_content)
        image_pb = self._call_fut(image)
        self.assertIsInstance(image_pb, image_annotator_pb2.Image)
        self.assertEqual(image_pb.content, image_content)

    def test__to_gapic_gcs_image_uri(self):
        from google.cloud.vision.image import Image
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        image_uri = 'gs://1234/34.jpg'
        client = object()
        image = Image(client, source_uri=image_uri)
        image_pb = self._call_fut(image)
        self.assertIsInstance(image_pb, image_annotator_pb2.Image)
        self.assertEqual(image_pb.source.gcs_image_uri, image_uri)

    def test__to_gapic_image_uri(self):
        from google.cloud.vision.image import Image
        from google.cloud.proto.vision.v1 import image_annotator_pb2

        image_uri = 'http://1234/34.jpg'
        client = object()
        image = Image(client, source_uri=image_uri)
        image_pb = self._call_fut(image)
        self.assertIsInstance(image_pb, image_annotator_pb2.Image)
        self.assertEqual(image_pb.source.image_uri, image_uri)

    def test__to_gapic_invalid_image_uri(self):
        from google.cloud.vision.image import Image

        image_uri = 'ftp://1234/34.jpg'
        client = object()
        image = Image(client, source_uri=image_uri)
        with self.assertRaises(ValueError):
            self._call_fut(image)

    def test__to_gapic_with_empty_image(self):
        image = mock.Mock(
            content=None, source=None, spec=['content', 'source'])
        with self.assertRaises(ValueError):
            self._call_fut(image)
