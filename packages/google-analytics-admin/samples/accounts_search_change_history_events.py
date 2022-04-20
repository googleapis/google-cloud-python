#!/usr/bin/env python

# Copyright 2021 Google LLC All Rights Reserved.
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

"""Google Analytics Admin API sample application which displays the change
history for the Google Analytics account.

See https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts/searchChangeHistoryEvents
for more information.
"""
# [START analyticsadmin_properties_conversion_events_create]
from datetime import datetime, timedelta

from google.analytics.admin import (
    AnalyticsAdminServiceClient,
    SearchChangeHistoryEventsRequest,
)
from google.analytics.admin_v1alpha.types import ActionType, ActorType
from google.protobuf.timestamp_pb2 import Timestamp


def run_sample():
    """Runs the sample."""
    # TODO(developer): Replace this variable with your Google Analytics
    #  account ID (e.g. "123456") before running the sample.
    account_id = "YOUR-GA-ACCOUNT-ID"

    # TODO(developer): Replace this variable with your Google Analytics 4
    #  property ID (e.g. "123456") before running the sample.
    property_id = "YOUR-GA4-PROPERTY-ID"
    search_change_history_events(account_id, property_id)


def search_change_history_events(account_id: str, property_id: str):
    """Lists the change history events for the Google Analytics 4 property
    within the specified date range."""
    client = AnalyticsAdminServiceClient()
    # Create a timestamp object and subtract 7 days from the current date/time.
    earliest_change_time = Timestamp()
    earliest_change_time.FromDatetime(datetime.now() - timedelta(days=7))

    results = client.search_change_history_events(
        SearchChangeHistoryEventsRequest(
            account=f"accounts/{account_id}",
            property=f"properties/{property_id}",
            action=["CREATED", "UPDATED"],
            earliest_change_time=earliest_change_time,
        )
    )

    print("Result:")
    for event in results:
        print(f"Event ID: {event.id}")
        print(f"Change time: {event.change_time}")
        print(f"Actor type: {ActorType(event.actor_type).name}")
        print(f"User actor e-mail: {event.user_actor_email}")
        print(f"Changes filtered: {event.changes_filtered}")
        for change in event.changes:
            print(" Change details")
            print(f"  Resource name: {change.resource}")
            print(f"  Action: {ActionType(change.action).name}")
            print("  Resource before change: ")
            print_resource(change.resource_before_change)
            print("  Resource after change: ")
            print_resource(change.resource_after_change)
        print()


def print_resource(resource):
    """Prints the change history resource."""
    # Detect the type of the resource by checking value of a oneof field.
    if resource.property:
        print("  Property resource")
    elif resource.account:
        print("  Account resource")
    elif resource.data_stream:
        print("  DataStream resource")
    elif resource.firebase_link:
        print("  FirebaseLink resource")
    elif resource.google_ads_link:
        print("  GoogleAdsLink resource")
    elif resource.google_signals_settings:
        print("  GoogleSignalsSettings resource")
    elif resource.display_video_360_advertiser_link:
        print("  DisplayVideo360AdvertiserLink resource")
    elif resource.display_video_360_advertiser_link_proposal:
        print("  DisplayVideo360AdvertiserLinkProposal resource")
    elif resource.conversion_event:
        print("  ConversionEvent resource")
    elif resource.measurement_protocol_secret:
        print("  MeasurementProtocolSecret resource")
    elif resource.custom_dimension:
        print("  CustomDimension resource")
    elif resource.custom_metric:
        print("  CustomMetric resource")
    elif resource.data_retention_settings:
        print("  DataRetentionSettings resource")
    else:
        print("  Resource not set")
    print(f"  Resource value: {resource}")
    print()


# [END analyticsadmin_properties_conversion_events_create]

if __name__ == "__main__":
    run_sample()
