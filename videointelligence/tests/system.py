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

"""System tests for VideoIntelligence API."""

import json
import os
import requests
import time
import unittest

from google.cloud import videointelligence
from google.cloud.videointelligence_v1 import enums

PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER")
OUTSIDE_PROJECT_API_KEY = os.environ.get(
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT_API_KEY"
)
OUTSIDE_IP = os.environ.get("GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_IP")
INSIDE_IP = os.environ.get("GOOGLE_CLOUD_TESTS_VPCSC_INSIDE_IP")


class VideoIntelligenceSystemTestBase(unittest.TestCase):
    client = None

    def setUp(self):
        self.input_uri = "gs://cloud-samples-data/video/cat.mp4"


def setUpModule():
    VideoIntelligenceSystemTestBase.client = (
        videointelligence.VideoIntelligenceServiceClient()
    )


class TestVideoIntelligenceClient(VideoIntelligenceSystemTestBase):
    def test_annotate_video(self):
        features_element = enums.Feature.LABEL_DETECTION
        features = [features_element]
        response = self.client.annotate_video(
            input_uri=self.input_uri, features=features
        )

        # Wait for the operation to complete.
        # Long timeout value warranted due to https://github.com/grpc/grpc/issues/19173
        lro_timeout_seconds = 180
        start_time = time.time()
        cnt = 0
        while not response.done() and (time.time() - start_time) < lro_timeout_seconds:
            time.sleep(1)
            cnt += 1
        if not response.done():
            self.fail(
                "wait for operation timed out after {lro_timeout_seconds} seconds".format(
                    lro_timeout_seconds=lro_timeout_seconds
                )
            )

        result = response.result()
        annotations = result.annotation_results[0]
        assert len(annotations.segment_label_annotations) > 0


@unittest.skipUnless(
    OUTSIDE_PROJECT_API_KEY,
    "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT_API_KEY not set in environment.",
)
class TestVideoIntelligenceClientVpcSc(VideoIntelligenceSystemTestBase):
    # Tests to verify VideoIntelligence service requests blocked when trying to access resources outside of a secure perimeter.
    def setUp(self):
        VideoIntelligenceSystemTestBase.setUp(self)
        # api-endpoint
        self.url = "https://videointelligence.googleapis.com/v1/videos:annotate?key={}".format(
            OUTSIDE_PROJECT_API_KEY
        )
        self.body = {
            "input_uri": self.input_uri,
            "features": ["LABEL_DETECTION"],
            "location_id": "us-west1",
        }

    @unittest.skipUnless(PROJECT_NUMBER, "PROJECT_NUMBER not set in environment.")
    @unittest.skipUnless(
        OUTSIDE_IP, "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_IP not set in environment."
    )
    def test_outside_ip_address_blocked(self):
        headers = {
            "Content-Type": "application/json",
            "X-User-IP": OUTSIDE_IP,
            "X-Google-GFE-Cloud-Client-Network-Project-Number": PROJECT_NUMBER,
        }
        r = requests.post(url=self.url, data=json.dumps(self.body), headers=headers)
        outside_project_operation = json.loads(r.text)
        print(outside_project_operation)
        # Assert it returns permission denied from VPC SC
        self.assertEqual(outside_project_operation["error"]["code"], 403)
        self.assertEqual(
            outside_project_operation["error"]["status"], "PERMISSION_DENIED"
        )
        self.assertEqual(
            outside_project_operation["error"]["details"][0]["violations"][0]["type"],
            "VPC_SERVICE_CONTROLS",
        )
        self.assertEqual(
            outside_project_operation["error"]["message"],
            "Request is prohibited by organization's policy",
        )

    @unittest.skipUnless(PROJECT_NUMBER, "PROJECT_NUMBER not set in environment.")
    @unittest.skipUnless(
        INSIDE_IP, "GOOGLE_CLOUD_TESTS_VPCSC_INSIDE_IP not set in environment."
    )
    def test_inside_ip_address_allowed(self):
        headers = {
            "Content-Type": "application/json",
            "X-User-IP": INSIDE_IP,
            "X-Google-GFE-Cloud-Client-Network-Project-Number": PROJECT_NUMBER,
        }
        r = requests.post(url=self.url, data=json.dumps(self.body), headers=headers)
        operation = json.loads(r.text)
        # Assert it returns non-empty operation name.
        self.assertNotEqual(operation["name"], "")
