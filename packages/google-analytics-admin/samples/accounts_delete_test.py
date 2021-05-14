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

import accounts_delete


FAKE_ACCOUNT_ID = "1"


def test_accounts_delete():
    # This test ensures that the call is valid and reaches the server. No
    # account is being deleted during the test as it is not trivial to
    # provision a new account for testing.
    with pytest.raises(Exception, match="403 The caller does not have permission"):
        accounts_delete.delete_account(FAKE_ACCOUNT_ID)
