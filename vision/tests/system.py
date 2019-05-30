# Copyright 2017, Google LLC All rights reserved.
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

"""System tests for Vision API."""

import io
import json
import os
import time
import unittest

from google.cloud import exceptions
from google.cloud import storage
from google.cloud import vision

from test_utils.retry import RetryErrors
from test_utils.system import unique_resource_id


_SYS_TESTS_DIR = os.path.realpath(os.path.dirname(__file__))
LOGO_FILE = os.path.join(_SYS_TESTS_DIR, "data", "logo.png")
FACE_FILE = os.path.join(_SYS_TESTS_DIR, "data", "faces.jpg")
LABEL_FILE = os.path.join(_SYS_TESTS_DIR, "data", "car.jpg")
LANDMARK_FILE = os.path.join(_SYS_TESTS_DIR, "data", "landmark.jpg")
TEXT_FILE = os.path.join(_SYS_TESTS_DIR, "data", "text.jpg")
FULL_TEXT_FILE = os.path.join(_SYS_TESTS_DIR, "data", "full-text.jpg")
PROJECT_ID = os.environ.get("PROJECT_ID")


class VisionSystemTestBase(unittest.TestCase):
    client = None
    test_bucket = None

    def setUp(self):
        self.to_delete_by_case = []

    def tearDown(self):
        for value in self.to_delete_by_case:
            value.delete()


def setUpModule():
    VisionSystemTestBase.client = vision.ImageAnnotatorClient()
    VisionSystemTestBase.ps_client = vision.ProductSearchClient()
    storage_client = storage.Client()
    bucket_name = "new" + unique_resource_id()
    VisionSystemTestBase.test_bucket = storage_client.bucket(bucket_name)

    # 429 Too Many Requests in case API requests rate-limited.
    retry_429 = RetryErrors(exceptions.TooManyRequests)
    retry_429(VisionSystemTestBase.test_bucket.create)()


def tearDownModule():
    # 409 Conflict if the bucket is full.
    # 429 Too Many Requests in case API requests rate-limited.
    bucket_retry = RetryErrors((exceptions.TooManyRequests, exceptions.Conflict))
    bucket_retry(VisionSystemTestBase.test_bucket.delete)(force=True)


class TestVisionClientLogo(VisionSystemTestBase):
    def test_detect_logos_content(self):
        # Read the file.
        with io.open(LOGO_FILE, "rb") as image_file:
            content = image_file.read()

        # Make the request.
        response = self.client.logo_detection({"content": content})

        # Check to ensure we got what we expect.
        assert len(response.logo_annotations) == 1
        assert response.logo_annotations[0].description == "google"

    def test_detect_logos_file_handler(self):
        # Get a file handler, and make the request using it.
        with io.open(LOGO_FILE, "rb") as image_file:
            response = self.client.logo_detection(image_file)

        # Check to ensure we got what we expect.
        assert len(response.logo_annotations) == 1
        assert response.logo_annotations[0].description == "google"

    def test_detect_logos_filename(self):
        # Make the request with the filename directly.
        response = self.client.logo_detection({"source": {"filename": LOGO_FILE}})

        # Check to ensure we got what we expect.
        assert len(response.logo_annotations) == 1
        assert response.logo_annotations[0].description == "google"

    def test_detect_logos_gcs(self):
        # Upload the image to Google Cloud Storage.
        blob_name = "logo.png"
        blob = self.test_bucket.blob(blob_name)
        self.to_delete_by_case.append(blob)
        with io.open(LOGO_FILE, "rb") as image_file:
            blob.upload_from_file(image_file)

        # Make the request.
        response = self.client.logo_detection(
            {
                "source": {
                    "image_uri": "gs://{bucket}/{blob}".format(
                        bucket=self.test_bucket.name, blob=blob_name
                    )
                }
            }
        )

        # Check the response.
        assert len(response.logo_annotations) == 1
        assert response.logo_annotations[0].description == "google"

    def test_detect_logos_async(self):
        # Upload the image to Google Cloud Storage.
        blob_name = "logo_async.png"
        blob = self.test_bucket.blob(blob_name)
        self.to_delete_by_case.append(blob)
        with io.open(LOGO_FILE, "rb") as image_file:
            blob.upload_from_file(image_file)

        # Make the request.
        request = {
            "image": {
                "source": {
                    "image_uri": "gs://{bucket}/{blob}".format(
                        bucket=self.test_bucket.name, blob=blob_name
                    )
                }
            },
            "features": [{"type": vision.enums.Feature.Type.LOGO_DETECTION}],
        }
        method_name = "test_detect_logos_async"
        output_gcs_uri_prefix = "gs://{bucket}/{method_name}".format(
            bucket=self.test_bucket.name, method_name=method_name
        )
        output_config = {"gcs_destination": {"uri": output_gcs_uri_prefix}}
        response = self.client.async_batch_annotate_images([request], output_config)

        # Wait for the operation to complete.
        lro_waiting_seconds = 60
        start_time = time.time()
        while not response.done() and (time.time() - start_time) < lro_waiting_seconds:
            time.sleep(1)

        if not response.done():
            self.fail(
                "{method_name} timed out after {lro_waiting_seconds} seconds".format(
                    method_name=method_name, lro_waiting_seconds=lro_waiting_seconds
                )
            )

        # Make sure getting the result is not an error.
        response.result()

        # There should be exactly 1 output file in gcs at the prefix output_gcs_uri_prefix.
        blobs = list(self.test_bucket.list_blobs(prefix=method_name))
        assert len(blobs) == 1
        blob = blobs[0]

        # Download the output file and verify the result
        result_str = blob.download_as_string().decode("utf8")
        result = json.loads(result_str)
        responses = result["responses"]
        assert len(responses) == 1
        logo_annotations = responses[0]["logoAnnotations"]
        assert len(logo_annotations) == 1
        assert logo_annotations[0]["description"] == "google"


@unittest.skipUnless(PROJECT_ID, "PROJECT_ID not set in environment.")
class TestVisionClientProductSearch(VisionSystemTestBase):
    def setUp(self):
        self.product_sets_to_delete = []
        self.location = "us-west1"
        self.location_path = self.ps_client.location_path(
            project=PROJECT_ID, location=self.location
        )

    def tearDown(self):
        for product_set in self.product_sets_to_delete:
            self.ps_client.delete_product_set(name=product_set)

    def test_create_product_set(self):
        product_set = vision.types.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        self.product_sets_to_delete.append(product_set_path)
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.assertEqual(response.name, product_set_path)

    def test_get_product_set(self):
        product_set = vision.types.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        self.product_sets_to_delete.append(product_set_path)
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.assertEqual(response.name, product_set_path)
        get_response = self.ps_client.get_product_set(name=product_set_path)
        self.assertEqual(get_response.name, product_set_path)

    def test_list_product_sets(self):
        product_set = vision.types.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        self.product_sets_to_delete.append(product_set_path)
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.assertEqual(response.name, product_set_path)
        product_sets = self.ps_client.list_product_sets(parent=self.location_path)
        self.assertGreater(len(list(product_sets)), 0)

    def test_update_product_set(self):
        product_set = vision.types.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        self.product_sets_to_delete.append(product_set_path)
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.assertEqual(response.name, product_set_path)
        new_display_name = "updated name"
        updated_product_set_request = vision.types.ProductSet(
            name=product_set_path, display_name=new_display_name
        )
        update_mask = vision.types.FieldMask(paths=["display_name"])
        updated_product_set = self.ps_client.update_product_set(
            product_set=updated_product_set_request, update_mask=update_mask
        )
        self.assertEqual(updated_product_set.display_name, new_display_name)
