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

import pytest

import properties_google_ads_links_delete


FAKE_PROPERTY_ID = "1"
FAKE_GOOGLE_ADS_LINK_ID = "1"


def test_properties_google_ads_links_delete():
    # This test ensures that the call is valid and reaches the server, even
    # though the operation does not succeed due to permission error.
    with pytest.raises(Exception, match="403 The caller does not have permission"):
        properties_google_ads_links_delete.delete_google_ads_link(
            FAKE_PROPERTY_ID, FAKE_GOOGLE_ADS_LINK_ID
        )
