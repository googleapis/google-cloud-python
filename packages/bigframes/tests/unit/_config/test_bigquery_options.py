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
import warnings

import pytest

import bigframes
import bigframes._config.bigquery_options as bigquery_options
import bigframes.exceptions


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
        ("kms_key_name", "kms/key/name/1", "kms/key/name/2"),
        ("skip_bq_connection_check", False, True),
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
            "bq_kms_key_name",
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


@pytest.mark.parametrize(
    [
        "valid_location",
    ],
    [
        (None,),
        ("us-central1",),
        ("us-Central1",),
        ("US-CENTRAL1",),
        ("US",),
        ("us",),
    ],
)
def test_location_set_to_valid_no_warning(valid_location):
    # test setting location through constructor
    def set_location_in_ctor():
        bigquery_options.BigQueryOptions(location=valid_location)

    # test setting location property
    def set_location_property():
        options = bigquery_options.BigQueryOptions()
        options.location = valid_location

    for op in [set_location_in_ctor, set_location_property]:
        # Ensure that no warnings are emitted.
        # https://docs.pytest.org/en/7.0.x/how-to/capture-warnings.html#additional-use-cases-of-warnings-in-tests
        with warnings.catch_warnings():
            # Turn matching UnknownLocationWarning into exceptions.
            # https://docs.python.org/3/library/warnings.html#warning-filter
            warnings.simplefilter(
                "error", category=bigframes.exceptions.UnknownLocationWarning
            )
            op()


@pytest.mark.parametrize(
    [
        "invalid_location",
        "possibility",
    ],
    [
        # Test with common mistakes, see article.
        # https://en.wikipedia.org/wiki/Edit_distance#Formal_definition_and_properties
        # Substitution
        ("us-wist3", "us-west3"),
        # Insertion
        ("us-central-1", "us-central1"),
        # Deletion
        ("asia-suth2", "asia-south2"),
    ],
)
def test_location_set_to_invalid_warning(invalid_location, possibility):
    # test setting location through constructor
    def set_location_in_ctor():
        bigquery_options.BigQueryOptions(location=invalid_location)

    # test setting location property
    def set_location_property():
        options = bigquery_options.BigQueryOptions()
        options.location = invalid_location

    for op in [set_location_in_ctor, set_location_property]:
        with pytest.warns(
            bigframes.exceptions.UnknownLocationWarning,
            match=re.escape(
                f"The location '{invalid_location}' is set to an unknown value. Did you mean '{possibility}'?"
            ),
        ):
            op()
