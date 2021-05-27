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

import properties_ios_app_data_streams_list

TEST_PROPERTY_ID = os.getenv("GA_TEST_PROPERTY_ID")


def test_properties_ios_app_data_streams_list(capsys):
    properties_ios_app_data_streams_list.list_ios_app_data_streams(TEST_PROPERTY_ID)
    out, _ = capsys.readouterr()
    assert "Result" in out
