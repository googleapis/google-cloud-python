#!/usr/bin/env python

# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Analytics Admin API sample application which creates a Firebase link
for the Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.firebaseLinks/create
for more information.
"""
# [START analyticsadmin_properties_firebase_links_create]
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import FirebaseLink


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics account ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with a Firebase project id.
    #  This project will be linked to the GA4 property.
    firebase_project_id = "YOUR-FIREBASE-PROJECT-ID"

    create_firebase_link(property_id, firebase_project_id)


def create_firebase_link(property_id, firebase_project_id):
    """Creates a Firebase link for the Google Analytics 4 property."""
    client = AnalyticsAdminServiceClient()
    firebase_link = client.create_firebase_link(
        parent=f"properties/{property_id}",
        firebase_link=FirebaseLink(
            project=f"projects/{firebase_project_id}",
            maximum_user_access="READ_AND_ANALYZE",
        ),
    )

    print("Result:")
    print(firebase_link)


# [END analyticsadmin_properties_firebase_links_create]

if __name__ == "__main__":
    run_sample()
