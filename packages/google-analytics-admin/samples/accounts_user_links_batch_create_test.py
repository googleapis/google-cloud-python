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

import pytest

import accounts_user_links_batch_create


FAKE_ACCOUNT_ID = "1"
TEST_EMAIL_ADDRESS = os.getenv("GA_TEST_EMAIL_ADDRESS")


def test_accounts_user_links_batch_create():
    # This test ensures that the call is valid and reaches the server, even
    # though the operation does not succeed due to permission error.
    with pytest.raises(Exception, match="403 The caller does not have permission"):
        accounts_user_links_batch_create.batch_create_account_user_link(
            FAKE_ACCOUNT_ID, TEST_EMAIL_ADDRESS
        )
