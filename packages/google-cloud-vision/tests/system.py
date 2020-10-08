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

import grpc
import io
import json
import os
import time
import unittest

import pytest

from google.api_core import exceptions
from google.cloud import storage
from google.cloud import vision
from google.protobuf import field_mask_pb2 as field_mask

from test_utils.retry import RetryErrors
from test_utils.system import unique_resource_id
from test_utils.vpcsc_config import vpcsc_config


_SYS_TESTS_DIR = os.path.realpath(os.path.dirname(__file__))
FACE_FILE = os.path.join(_SYS_TESTS_DIR, "data", "faces.jpg")
LOGO_FILE = os.path.join(_SYS_TESTS_DIR, "data", "logo.png")
PDF_FILE = os.path.join(_SYS_TESTS_DIR, "data", "pdf_test.pdf")
PROJECT_ID = os.environ.get("PROJECT_ID")
_VPCSC_PROHIBITED_MESSAGE = "Request is prohibited by organization's policy"


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
        assert response.logo_annotations[0].description.lower() == "google"

    def test_detect_logos_file_handler(self):
        # Get a file handler, and make the request using it.
        with io.open(LOGO_FILE, "rb") as image_file:
            response = self.client.logo_detection(image_file)

        # Check to ensure we got what we expect.
        assert len(response.logo_annotations) == 1
        assert response.logo_annotations[0].description.lower() == "google"

    def test_detect_logos_filename(self):
        # Make the request with the filename directly.
        response = self.client.logo_detection({"source": {"filename": LOGO_FILE}})

        # Check to ensure we got what we expect.
        assert len(response.logo_annotations) == 1
        assert response.logo_annotations[0].description.lower() == "google"

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
        assert response.logo_annotations[0].description.lower() == "google"

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
            "features": [{"type_": vision.Feature.Type.LOGO_DETECTION}],
        }
        method_name = "test_detect_logos_async"
        output_gcs_uri_prefix = "gs://{bucket}/{method_name}".format(
            bucket=self.test_bucket.name, method_name=method_name
        )
        output_config = {"gcs_destination": {"uri": output_gcs_uri_prefix}}
        response = self.client.async_batch_annotate_images(
            requests=[request], output_config=output_config
        )

        # Wait for the operation to complete.
        lro_waiting_seconds = 90
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
        assert logo_annotations[0]["description"].lower() == "google"


class TestVisionClientFiles(VisionSystemTestBase):
    def test_async_batch_annotate_files(self):
        # Upload the image to Google Cloud Storage.
        blob_name = "async_batch_annotate_files.pdf"
        blob = self.test_bucket.blob(blob_name)
        self.to_delete_by_case.append(blob)
        with io.open(PDF_FILE, "rb") as image_file:
            blob.upload_from_file(image_file)

        # Make the request.
        method_name = "test_async_batch_annotate_files"
        output_gcs_uri_prefix = "gs://{bucket}/{method_name}".format(
            bucket=self.test_bucket.name, method_name=method_name
        )
        request = {
            "input_config": {
                "gcs_source": {
                    "uri": "gs://{bucket}/{blob}".format(
                        bucket=self.test_bucket.name, blob=blob_name
                    )
                },
                "mime_type": "application/pdf",
            },
            "features": [{"type_": vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
            "output_config": {"gcs_destination": {"uri": output_gcs_uri_prefix}},
        }
        response = self.client.async_batch_annotate_files(requests=[request])

        # Wait for the operation to complete.
        lro_waiting_seconds = 90
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
        text = responses[0]["fullTextAnnotation"]["text"]
        expected_text = "test text"
        self.assertTrue(
            expected_text in text,
            "'{expected_text}' not in '{text}'".format(
                expected_text=expected_text, text=text
            ),
        )


@unittest.skipUnless(PROJECT_ID, "PROJECT_ID not set in environment.")
class TestVisionClientProductSearch(VisionSystemTestBase):
    def setUp(self):
        VisionSystemTestBase.setUp(self)
        self.reference_images_to_delete = []
        self.products_to_delete = []
        self.product_sets_to_delete = []
        self.location = "us-west1"
        self.location_path = f"projects/{PROJECT_ID}/locations/{self.location}"

    def tearDown(self):
        VisionSystemTestBase.tearDown(self)
        for reference_image in self.reference_images_to_delete:
            self.ps_client.delete_reference_image(name=reference_image)
        for product in self.products_to_delete:
            self.ps_client.delete_product(name=product)
        for product_set in self.product_sets_to_delete:
            self.ps_client.delete_product_set(name=product_set)

    def _upload_image(self, image_name):
        blob = self.test_bucket.blob(image_name)
        self.to_delete_by_case.append(blob)
        with io.open(FACE_FILE, "rb") as image_file:
            blob.upload_from_file(image_file)
        return "gs://{bucket}/{blob}".format(
            bucket=self.test_bucket.name, blob=image_name
        )

    def test_create_product_set(self):
        # Create a ProductSet.
        product_set = vision.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.product_sets_to_delete.append(response.name)
        # Verify the ProductSet was successfully created.
        self.assertEqual(response.name, product_set_path)

    def test_get_product_set(self):
        # Create a ProductSet.
        product_set = vision.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.product_sets_to_delete.append(response.name)
        self.assertEqual(response.name, product_set_path)
        # Get the ProductSet.
        get_response = self.ps_client.get_product_set(name=product_set_path)
        self.assertEqual(get_response.name, product_set_path)

    def test_list_product_sets(self):
        # Create a ProductSet.
        product_set = vision.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.product_sets_to_delete.append(response.name)
        self.assertEqual(response.name, product_set_path)
        # Verify ProductSets can be listed.
        product_sets_iterator = self.ps_client.list_product_sets(
            parent=self.location_path
        )
        product_sets_exist = False
        for product_set in product_sets_iterator:
            product_sets_exist = True
            break
        self.assertTrue(product_sets_exist)

    def test_update_product_set(self):
        # Create a ProductSet.
        product_set = vision.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.product_sets_to_delete.append(response.name)
        self.assertEqual(response.name, product_set_path)
        # Update the ProductSet.
        new_display_name = "updated name"
        updated_product_set_request = vision.ProductSet(
            name=product_set_path, display_name=new_display_name
        )
        update_mask = field_mask.FieldMask(paths=["display_name"])
        updated_product_set = self.ps_client.update_product_set(
            product_set=updated_product_set_request, update_mask=update_mask
        )
        self.assertEqual(updated_product_set.display_name, new_display_name)

    def test_create_product(self):
        # Create a Product.
        product = vision.Product(
            display_name="product display name", product_category="apparel"
        )
        product_id = "product" + unique_resource_id()
        product_path = self.ps_client.product_path(
            project=PROJECT_ID, location=self.location, product=product_id
        )
        response = self.ps_client.create_product(
            parent=self.location_path, product=product, product_id=product_id
        )
        self.products_to_delete.append(response.name)
        # Verify the Product was successfully created.
        self.assertEqual(response.name, product_path)

    def test_get_product(self):
        # Create a Product.
        product = vision.Product(
            display_name="product display name", product_category="apparel"
        )
        product_id = "product" + unique_resource_id()
        product_path = self.ps_client.product_path(
            project=PROJECT_ID, location=self.location, product=product_id
        )
        response = self.ps_client.create_product(
            parent=self.location_path, product=product, product_id=product_id
        )
        self.products_to_delete.append(response.name)
        self.assertEqual(response.name, product_path)
        # Get the Product.
        get_response = self.ps_client.get_product(name=product_path)
        self.assertEqual(get_response.name, product_path)

    def test_update_product(self):
        # Create a Product.
        product = vision.Product(
            display_name="product display name", product_category="apparel"
        )
        product_id = "product" + unique_resource_id()
        product_path = self.ps_client.product_path(
            project=PROJECT_ID, location=self.location, product=product_id
        )
        response = self.ps_client.create_product(
            parent=self.location_path, product=product, product_id=product_id
        )
        self.products_to_delete.append(response.name)
        self.assertEqual(response.name, product_path)
        # Update the Product.
        new_display_name = "updated product name"
        updated_product_request = vision.Product(
            name=product_path, display_name=new_display_name
        )
        update_mask = field_mask.FieldMask(paths=["display_name"])
        updated_product = self.ps_client.update_product(
            product=updated_product_request, update_mask=update_mask
        )
        self.assertEqual(updated_product.display_name, new_display_name)

    def test_list_products(self):
        # Create a Product.
        product = vision.Product(
            display_name="product display name", product_category="apparel"
        )
        product_id = "product" + unique_resource_id()
        product_path = self.ps_client.product_path(
            project=PROJECT_ID, location=self.location, product=product_id
        )
        response = self.ps_client.create_product(
            parent=self.location_path, product=product, product_id=product_id
        )
        self.products_to_delete.append(response.name)
        self.assertEqual(response.name, product_path)
        # Verify Products can be listed.
        products_iterator = self.ps_client.list_products(parent=self.location_path)
        products_exist = False
        for product in products_iterator:
            products_exist = True
            break
        self.assertTrue(products_exist)

    def test_list_products_in_product_set(self):
        # Create a ProductSet.
        product_set = vision.ProductSet(display_name="display name")
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        response = self.ps_client.create_product_set(
            parent=self.location_path,
            product_set=product_set,
            product_set_id=product_set_id,
        )
        self.product_sets_to_delete.append(response.name)
        self.assertEqual(response.name, product_set_path)
        # Create a Product.
        product = vision.Product(
            display_name="product display name", product_category="apparel"
        )
        product_id = "product" + unique_resource_id()
        product_path = self.ps_client.product_path(
            project=PROJECT_ID, location=self.location, product=product_id
        )
        response = self.ps_client.create_product(
            parent=self.location_path, product=product, product_id=product_id
        )
        self.products_to_delete.append(response.name)
        self.assertEqual(response.name, product_path)
        # Add the Product to the ProductSet.
        self.ps_client.add_product_to_product_set(
            name=product_set_path, product=product_path
        )
        # List the Products in the ProductSet.
        listed_products = list(
            self.ps_client.list_products_in_product_set(name=product_set_path)
        )
        self.assertEqual(len(listed_products), 1)
        self.assertEqual(listed_products[0].name, product_path)
        # Remove the Product from the ProductSet.
        self.ps_client.remove_product_from_product_set(
            name=product_set_path, product=product_path
        )

    def test_reference_image(self):
        # Create a Product.
        product = vision.Product(
            display_name="product display name", product_category="apparel"
        )
        product_id = "product" + unique_resource_id()
        product_path = self.ps_client.product_path(
            project=PROJECT_ID, location=self.location, product=product_id
        )
        response = self.ps_client.create_product(
            parent=self.location_path, product=product, product_id=product_id
        )
        self.products_to_delete.append(response.name)
        self.assertEqual(response.name, product_path)

        # Upload image to gcs.
        gcs_uri = self._upload_image("reference_image_test.jpg")

        # Create a ReferenceImage.
        reference_image_id = "reference_image" + unique_resource_id()
        reference_image_path = self.ps_client.reference_image_path(
            project=PROJECT_ID,
            location=self.location,
            product=product_id,
            reference_image=reference_image_id,
        )
        reference_image = vision.ReferenceImage(uri=gcs_uri)
        response = self.ps_client.create_reference_image(
            parent=product_path,
            reference_image=reference_image,
            reference_image_id=reference_image_id,
        )
        self.reference_images_to_delete.append(response.name)
        self.assertEqual(response.name, reference_image_path)

        # Get the ReferenceImage.
        get_response = self.ps_client.get_reference_image(name=reference_image_path)
        self.assertEqual(get_response.name, reference_image_path)

        # List the ReferenceImages in the Product.
        listed_reference_images = list(
            self.ps_client.list_reference_images(parent=product_path)
        )
        self.assertEqual(len(listed_reference_images), 1)
        self.assertEqual(listed_reference_images[0].name, reference_image_path)

    def _build_csv_line(
        self, gcs_uri_image, reference_image_id, product_set_id, product_id
    ):
        return ",".join(
            [
                gcs_uri_image,
                reference_image_id,
                product_set_id,
                product_id,
                "apparel",
                "display name",
                '"color=black,style=formal"',
                "",
            ]
        )

    def test_import_product_sets(self):
        # Generate the ids that will be used in the import.
        product_set_id = "set" + unique_resource_id()
        product_set_path = self.ps_client.product_set_path(
            project=PROJECT_ID, location=self.location, product_set=product_set_id
        )
        self.product_sets_to_delete.append(product_set_path)
        product_id = "product" + unique_resource_id()
        product_path = self.ps_client.product_path(
            project=PROJECT_ID, location=self.location, product=product_id
        )
        self.products_to_delete.append(product_path)
        reference_image_id_1 = "reference_image_1" + unique_resource_id()
        reference_image_path = self.ps_client.reference_image_path(
            project=PROJECT_ID,
            location=self.location,
            product=product_id,
            reference_image=reference_image_id_1,
        )
        self.reference_images_to_delete.append(reference_image_path)
        reference_image_id_2 = "reference_image_2" + unique_resource_id()
        reference_image_path = self.ps_client.reference_image_path(
            project=PROJECT_ID,
            location=self.location,
            product=product_id,
            reference_image=reference_image_id_2,
        )
        self.reference_images_to_delete.append(reference_image_path)

        # Upload images to gcs.
        gcs_uri_image_1 = self._upload_image("import_sets_image_1.jpg")
        gcs_uri_image_2 = self._upload_image("import_sets_image_2.jpg")

        # Build the string that will be uploaded to gcs as a csv file.
        csv_data = "\n".join(
            [
                self._build_csv_line(
                    gcs_uri_image_1, reference_image_id_1, product_set_id, product_id
                ),
                self._build_csv_line(
                    gcs_uri_image_2, reference_image_id_2, product_set_id, product_id
                ),
            ]
        )

        # Upload a csv file to gcs.
        csv_filename = "import_sets.csv"
        blob = self.test_bucket.blob(csv_filename)
        self.to_delete_by_case.append(blob)
        blob.upload_from_string(csv_data)

        # Make the import_product_sets request.
        gcs_source = vision.ImportProductSetsGcsSource(
            csv_file_uri="gs://{bucket}/{blob}".format(
                bucket=self.test_bucket.name, blob=csv_filename
            )
        )
        input_config = vision.ImportProductSetsInputConfig(gcs_source=gcs_source)
        response = self.ps_client.import_product_sets(
            parent=self.location_path, input_config=input_config
        )

        # Verify the result.
        image_prefix = "import_sets_image_"
        for ref_image in response.result().reference_images:
            self.assertTrue(
                image_prefix in ref_image.uri,
                "'{image_prefix}' not in '{uri}'".format(
                    image_prefix=image_prefix, uri=ref_image.uri
                ),
            )
        for status in response.result().statuses:
            self.assertEqual(status.code, grpc.StatusCode.OK.value[0])


@vpcsc_config.skip_unless_outside_project
class TestVisionClientProductSearchVpcsc(VisionSystemTestBase):
    # Tests to verify ProductSearch is blocked by VPC SC when trying to access a resource outside of a secure perimeter.
    def setUp(self):
        super(TestVisionClientProductSearchVpcsc, self).setUp()
        uniq = unique_resource_id()
        self.location = "us-west1"
        self.location_path = (
            f"projects/{vpcsc_config.project_outside}/locations/{self.location}"
        )
        self.product_set_id = product_set_id = "set" + uniq
        self.product_set_path = self.ps_client.product_set_path(
            project=vpcsc_config.project_outside,
            location=self.location,
            product_set=product_set_id,
        )
        self.product_id = "product" + uniq
        self.product_path = self.ps_client.product_path(
            project=vpcsc_config.project_outside,
            location=self.location,
            product=self.product_id,
        )
        self.reference_image_id = "reference_image" + uniq
        self.reference_image_path = self.ps_client.reference_image_path(
            project=vpcsc_config.project_outside,
            location=self.location,
            product=self.product_id,
            reference_image=self.reference_image_id,
        )

    def test_create_product_set_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.create_product_set(
                parent=self.location_path,
                product_set={},
                product_set_id=self.product_set_id,
            )

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_get_product_set_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.get_product_set(name=self.product_set_path)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_delete_product_set_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.delete_product_set(name=self.product_set_path)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_list_product_sets_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(self.ps_client.list_product_sets(parent=self.location_path))

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_update_product_set_blocked(self):
        product_set = vision.ProductSet(name=self.product_set_path)
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.update_product_set(product_set=product_set)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_create_product_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.create_product(
                parent=self.location_path, product={}, product_id=self.product_id
            )

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_get_product_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.get_product(name=self.product_path)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_delete_product_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.delete_product(name=self.product_path)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_update_product_blocked(self):
        product = vision.Product(name=self.product_path)
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.update_product(product=product)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_list_products_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(self.ps_client.list_products(parent=self.location_path))

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_list_products_in_product_set_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(
                self.ps_client.list_products_in_product_set(name=self.product_set_path)
            )

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_add_product_to_product_set_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.add_product_to_product_set(
                name=self.product_set_path, product=self.product_path
            )

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_remove_product_from_product_set_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.remove_product_from_product_set(
                name=self.product_set_path, product=self.product_path
            )

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_create_reference_image_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.create_reference_image(
                parent=self.product_path,
                reference_image={},
                reference_image_id=self.reference_image_id,
            )

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_get_reference_image_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.get_reference_image(name=self.reference_image_path)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_delete_reference_image_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            self.ps_client.delete_reference_image(name=self.reference_image_path)

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)

    def test_list_reference_images_blocked(self):
        with pytest.raises(exceptions.PermissionDenied) as exc:
            list(self.ps_client.list_reference_images(parent=self.product_path))

        assert exc.value.message.startswith(_VPCSC_PROHIBITED_MESSAGE)


@vpcsc_config.skip_unless_inside_vpcsc
class TestVisionClientVpcsc(VisionSystemTestBase):
    # Tests to verify Vision API methods are blocked by VPC SC when trying to access a gcs resource outside of a secure perimeter.
    def setUp(self):
        super(TestVisionClientVpcsc, self).setUp()
        self.blocked_file = "LC08/01_$folder$"
        self.gcs_uri_blocked_file = "gs://{bucket}/{file}".format(
            bucket=vpcsc_config.bucket_outside, file=self.blocked_file
        )
        self.gcs_read_error_message = "Error opening file: gs://"
        self.gcs_write_error_message = "Error writing final output to"
        self.location = "us-west1"
        self.location_path = (
            f"projects/{vpcsc_config.project_inside}/locations/{self.location}"
        )

    def test_import_product_sets_blocked(self):
        # The csv file is outside the secure perimeter.
        gcs_source = vision.ImportProductSetsGcsSource(
            csv_file_uri=self.gcs_uri_blocked_file
        )
        input_config = vision.ImportProductSetsInputConfig(gcs_source=gcs_source)
        with pytest.raises(exceptions.Forbidden) as exc:
            self.ps_client.import_product_sets(
                parent=self.location_path, input_config=input_config
            )

        assert self.gcs_read_error_message in exc.value.message

    def test_async_batch_annotate_files_read_blocked(self):
        # Make the request.
        method_name = "test_async_batch_annotate_files_read_blocked"
        output_gcs_uri_prefix = "gs://{bucket}/{method_name}".format(
            bucket=self.test_bucket.name, method_name=method_name
        )
        # The input file is in a gcs bucket that is outside of the secure perimeter.
        request = {
            "input_config": {
                "gcs_source": {"uri": self.gcs_uri_blocked_file},
                "mime_type": "application/pdf",
            },
            "features": [{"type_": vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
            "output_config": {"gcs_destination": {"uri": output_gcs_uri_prefix}},
        }
        with pytest.raises(exceptions.Forbidden) as exc:
            self.client.async_batch_annotate_files(requests=[request])

        assert self.gcs_read_error_message in exc.value.message

    def test_async_batch_annotate_files_write_blocked(self):
        # Upload the image to Google Cloud Storage.
        blob_name = "async_batch_annotate_files_write_blocked.pdf"
        blob = self.test_bucket.blob(blob_name)
        self.to_delete_by_case.append(blob)
        with io.open(PDF_FILE, "rb") as image_file:
            blob.upload_from_file(image_file)

        method_name = "test_async_batch_annotate_files_write_blocked"
        # Write the result to a bucket outside of the secure perimeter.
        output_gcs_uri_prefix = "gs://{bucket}/{method_name}".format(
            bucket=vpcsc_config.bucket_outside, method_name=method_name
        )
        request = {
            "input_config": {
                "gcs_source": {
                    "uri": "gs://{bucket}/{blob}".format(
                        bucket=self.test_bucket.name, blob=blob_name
                    )
                },
                "mime_type": "application/pdf",
            },
            "features": [{"type_": vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
            "output_config": {"gcs_destination": {"uri": output_gcs_uri_prefix}},
        }
        response = self.client.async_batch_annotate_files(requests=[request])

        # Wait for the operation to complete.
        lro_waiting_seconds = 90
        start_time = time.time()
        while not response.done() and (time.time() - start_time) < lro_waiting_seconds:
            time.sleep(1)
        assert response.done

        # Verify there was an error writing to the output bucket.
        error = response.operation.error
        assert error.code == 7
        assert self.gcs_write_error_message in error.message

    def test_async_batch_annotate_images_read_blocked(self):
        request = {
            "image": {"source": {"image_uri": self.gcs_uri_blocked_file}},
            "features": [{"type_": vision.Feature.Type.LOGO_DETECTION}],
        }
        method_name = "test_async_batch_annotate_images_read_blocked"
        output_gcs_uri_prefix = "gs://{bucket}/{method_name}".format(
            bucket=self.test_bucket.name, method_name=method_name
        )
        output_config = {"gcs_destination": {"uri": output_gcs_uri_prefix}}
        response = self.client.async_batch_annotate_images(
            requests=[request], output_config=output_config
        )
        # Wait for the operation to complete.
        lro_waiting_seconds = 90
        start_time = time.time()
        while not response.done() and (time.time() - start_time) < lro_waiting_seconds:
            time.sleep(1)
        assert response.done()

        # Make sure getting the result is not an error.
        response.result()
        blobs = list(self.test_bucket.list_blobs(prefix=method_name))
        assert len(blobs) == 1
        blob = blobs[0]

        # Download the output file.
        result_str = blob.download_as_string().decode("utf8")
        result = json.loads(result_str)
        responses = result["responses"]
        assert len(responses) == 1

        # Verify the read error.
        error = responses[0]["error"]
        assert error["code"] == 7
        assert self.gcs_read_error_message in error["message"]

    def test_async_batch_annotate_images_write_blocked(self):
        request = {
            "image": {"source": {"image_uri": self.gcs_uri_blocked_file}},
            "features": [{"type_": vision.Feature.Type.LOGO_DETECTION}],
        }
        method_name = "test_async_batch_annotate_images_write_blocked"

        # Write the result to a bucket outside of the secure perimeter.
        output_gcs_uri_prefix = "gs://{bucket}/{method_name}".format(
            bucket=vpcsc_config.bucket_outside, method_name=method_name
        )
        output_config = {"gcs_destination": {"uri": output_gcs_uri_prefix}}
        response = self.client.async_batch_annotate_images(
            requests=[request], output_config=output_config
        )
        # Wait for the operation to complete.
        lro_waiting_seconds = 90
        start_time = time.time()
        while not response.done() and (time.time() - start_time) < lro_waiting_seconds:
            time.sleep(1)
        assert response.done()

        # Verify there was an error writing to the output bucket.
        error = response.operation.error
        assert error.code == 7
        assert self.gcs_write_error_message in error.message

    def test_batch_annotate_images_read_blocked(self):
        response = self.client.logo_detection(
            {"source": {"image_uri": self.gcs_uri_blocked_file}}
        )
        error = response.error
        assert error.code == 7
        assert self.gcs_read_error_message in error.message
