# Copyright 2023 Google LLC
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

"""Constants used across BigQuery DataFrames.

This module should not depend on any others in the package.
"""

import datetime

import bigframes_vendored.constants

BF_VERSION = bigframes_vendored.constants.BF_VERSION
FEEDBACK_LINK = bigframes_vendored.constants.FEEDBACK_LINK
ABSTRACT_METHOD_ERROR_MESSAGE = (
    bigframes_vendored.constants.ABSTRACT_METHOD_ERROR_MESSAGE
)

DEFAULT_EXPIRATION = datetime.timedelta(days=7)

# https://cloud.google.com/bigquery/docs/locations
ALL_BIGQUERY_LOCATIONS = frozenset(
    {
        # regions
        "us-east5",
        "us-south1",
        "us-central1",
        "us-west4",
        "us-west2",
        "northamerica-northeast1",
        "us-east4",
        "us-west1",
        "us-west3",
        "southamerica-east1",
        "southamerica-west1",
        "us-east1",
        "northamerica-northeast2",
        "asia-south2",
        "asia-east2",
        "asia-southeast2",
        "australia-southeast2",
        "asia-south1",
        "asia-northeast2",
        "asia-northeast3",
        "asia-southeast1",
        "australia-southeast1",
        "asia-east1",
        "asia-northeast1",
        "europe-west1",
        "europe-west10",
        "europe-north1",
        "europe-west3",
        "europe-west2",
        "europe-southwest1",
        "europe-west8",
        "europe-west4",
        "europe-west9",
        "europe-west12",
        "europe-central2",
        "europe-west6",
        "me-central2",
        "me-central1",
        "me-west1",
        "me-central2",
        "me-central1",
        "me-west1",
        "africa-south1",
        # multi-regions
        "US",
        "EU",
    }
)

# https://cloud.google.com/storage/docs/regional-endpoints
REP_ENABLED_BIGQUERY_LOCATIONS = frozenset(
    {
        "me-central2",
        "europe-west9",
        "europe-west3",
        "us-east4",
        "us-west1",
    }
)

# https://cloud.google.com/storage/docs/locational-endpoints
LEP_ENABLED_BIGQUERY_LOCATIONS = frozenset(
    ALL_BIGQUERY_LOCATIONS - REP_ENABLED_BIGQUERY_LOCATIONS
)

# BigQuery default is 10000, leave 100 for overhead
MAX_COLUMNS = 9900

SUGGEST_PEEK_PREVIEW = "Use .peek(n) to preview n arbitrary rows."
