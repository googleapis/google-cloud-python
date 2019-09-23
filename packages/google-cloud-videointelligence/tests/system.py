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
import unittest

from google.auth.transport import requests as goog_auth_requests
from google.cloud import videointelligence
from google.oauth2 import service_account

CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
CREDENTIALS_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
OUTSIDE_BUCKET = os.environ.get("GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_BUCKET")
INSIDE_BUCKET = os.environ.get("GOOGLE_CLOUD_TESTS_VPCSC_INSIDE_PERIMETER_BUCKET")
IS_INSIDE_VPCSC = os.environ.get("GOOGLE_CLOUD_TESTS_IN_VPCSC")


def get_access_token():
    """Returns an access token.

  Generates access tokens using the provided service account key file.
  """
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=[CLOUD_PLATFORM_SCOPE]
    )
    with requests.Session() as session:
        creds.refresh(goog_auth_requests.Request(session=session))
    return creds.token


class VideoIntelligenceSystemTestBase(unittest.TestCase):
    client = None


def setUpModule():
    VideoIntelligenceSystemTestBase.client = (
        videointelligence.VideoIntelligenceServiceClient()
    )


@unittest.skipUnless(
    CREDENTIALS_FILE, "GOOGLE_APPLICATION_CREDENTIALS not set in environment."
)
class TestVideoIntelligenceClientVpcSc(VideoIntelligenceSystemTestBase):
    # Tests to verify VideoIntelligence service requests blocked when trying to
    # access resources outside of a secure perimeter.
    def setUp(self):
        VideoIntelligenceSystemTestBase.setUp(self)
        # api-endpoint
        self.url = "https://videointelligence.googleapis.com/v1/videos:annotate"
        self.body = {"features": ["LABEL_DETECTION"], "location_id": "us-west1"}

    @unittest.skipUnless(
        OUTSIDE_BUCKET,
        "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_BUCKET not set in environment.",
    )
    @unittest.skipUnless(
        IS_INSIDE_VPCSC, "GOOGLE_CLOUD_TESTS_IN_VPCSC not set in environment."
    )
    def test_outside_perimeter_blocked(self):
        headers = {
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        }
        self.body["input_uri"] = "gs://{bucket}/cat.mp4".format(bucket=OUTSIDE_BUCKET)
        r = requests.post(url=self.url, data=json.dumps(self.body), headers=headers)
        resp = json.loads(r.text)
        print(resp)
        # Assert it returns permission denied from VPC SC
        self.assertEqual(resp["error"]["code"], 403)
        self.assertEqual(resp["error"]["status"], "PERMISSION_DENIED")

    @unittest.skipUnless(
        INSIDE_BUCKET,
        "GOOGLE_CLOUD_TESTS_VPCSC_INSIDE_PERIMETER_BUCKET not set in environment.",
    )
    @unittest.skipUnless(
        IS_INSIDE_VPCSC, "GOOGLE_CLOUD_TESTS_IN_VPCSC not set in environment."
    )
    def test_inside_perimeter_allowed(self):
        headers = {
            "Authorization": "Bearer " + get_access_token(),
            "Content-Type": "application/json",
        }
        self.body["input_uri"] = "gs://{bucket}/cat.mp4".format(bucket=INSIDE_BUCKET)
        r = requests.post(url=self.url, data=json.dumps(self.body), headers=headers)
        operation = json.loads(r.text)
        print(operation)

        get_op_url = "https://videointelligence.googleapis.com/v1/" + operation["name"]
        get_op = requests.get(url=get_op_url, headers=headers)
        get_op_resp = json.loads(get_op.text)
        print(get_op_resp)
        # Assert that we do not get an error.
        self.assertEqual(get_op_resp["name"], operation["name"])
