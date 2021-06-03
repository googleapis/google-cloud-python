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

"""Google Analytics Admin API sample application which deletes the Firebase
link from the Google Analytics 4 property.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.firebaseLinks/delete
for more information.
"""
# [START analyticsadmin_properties_firebase_links_delete]
from google.analytics.admin import AnalyticsAdminServiceClient


def run_sample():
    """Runs the sample."""

    # !!! ATTENTION !!!
    #  Running this sample may change/delete your Google Analytics account
    #  configuration. Make sure to not use the Google Analytics property ID from
    #  your production environment below.

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"

    # TODO(developer): Replace this variable with your Firebase link ID
    #  (e.g. "123456") before running the sample.
    firebase_link_id = "YOUR-FIREBASE-LINK-ID"

    delete_firebase_link(property_id, firebase_link_id)


def delete_firebase_link(property_id, firebase_link_id):
    """Deletes the Firebase link."""
    client = AnalyticsAdminServiceClient()
    client.delete_firebase_link(
        name=f"properties/{property_id}/firebaseLinks/{firebase_link_id}"
    )
    print("Firebase link deleted")


# [END analyticsadmin_properties_firebase_links_delete]


if __name__ == "__main__":
    run_sample()
