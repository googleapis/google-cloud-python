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

import re

import pytest

import bigframes._config.bigquery_options as bigquery_options


@pytest.mark.parametrize(
    ["attribute", "original_value", "new_value"],
    [
        ("application_name", None, "test-partner"),
        # For credentials, the match is by reference.
        ("credentials", object(), object()),
        ("location", "us-east1", "us-central1"),
        ("project", "my-project", "my-other-project"),
        ("bq_connection", "path/to/connection/1", "path/to/connection/2"),
        ("use_regional_endpoints", False, True),
    ],
)
def test_setter_raises_if_session_started(attribute, original_value, new_value):
    options = bigquery_options.BigQueryOptions()
    setattr(options, attribute, original_value)
    assert getattr(options, attribute) is original_value
    assert getattr(options, attribute) is not new_value

    options._session_started = True
    expected_message = re.escape(
        bigquery_options.SESSION_STARTED_MESSAGE.format(attribute=attribute)
    )
    with pytest.raises(ValueError, match=expected_message):
        setattr(options, attribute, new_value)

    assert getattr(options, attribute) is original_value
    assert getattr(options, attribute) is not new_value


@pytest.mark.parametrize(
    [
        "attribute",
    ],
    [
        (attribute,)
        for attribute in [
            "application_name",
            "credentials",
            "location",
            "project",
            "bq_connection",
            "use_regional_endpoints",
        ]
    ],
)
def test_setter_if_session_started_but_setting_the_same_value(attribute):
    options = bigquery_options.BigQueryOptions()
    original_object = object()
    setattr(options, attribute, original_object)
    assert getattr(options, attribute) is original_object

    # This should work fine since we're setting the same value as before.
    options._session_started = True
    setattr(options, attribute, original_object)

    assert getattr(options, attribute) is original_object
