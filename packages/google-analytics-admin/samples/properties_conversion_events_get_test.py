# Copyright 2021 Google LLC All Rights Reserved.
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

import os

import properties_conversion_events_get

TEST_PROPERTY_ID = os.getenv("GA_TEST_PROPERTY_ID")
TEST_CONVERSION_EVENT_ID = os.getenv("GA_TEST_CONVERSION_EVENT_ID")


def test_properties_conversion_events_get(capsys):
    properties_conversion_events_get.get_conversion_event(
        TEST_PROPERTY_ID, TEST_CONVERSION_EVENT_ID
    )
    out, _ = capsys.readouterr()
    assert "Result" in out
