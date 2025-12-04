# Copyright 2020 Google LLC
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

import os
import pytest

from google.auth import _default_async
from google.auth.exceptions import RefreshError

EXPECT_PROJECT_ID = os.getenv("EXPECT_PROJECT_ID")
CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")


@pytest.mark.asyncio
async def test_application_default_credentials(verify_refresh):
    credentials, project_id = _default_async.default_async()

    if EXPECT_PROJECT_ID is not None:
        assert project_id is not None

    try:
        await verify_refresh(credentials)
    except RefreshError as e:
        # allow expired credentials for explicit_authorized_user tests
        # TODO: https://github.com/googleapis/google-auth-library-python/issues/1882
        if not CREDENTIALS.endswith("authorized_user.json") or "Token has been expired or revoked" not in str(e):
            raise
