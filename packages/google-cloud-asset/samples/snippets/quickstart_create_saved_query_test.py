#!/usr/bin/env python

# Copyright 2022 Google LLC.
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
import uuid

import quickstart_create_saved_query


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
SAVED_QUERY_ID = f"saved-query-{uuid.uuid4().hex}"


@pytest.mark.parametrize("transport", ["grpc", "rest"])
def test_create_saved_query(transport, capsys, saved_query_deleter):
    saved_query = quickstart_create_saved_query.create_saved_query(
        project_id=PROJECT,
        saved_query_id=f"{SAVED_QUERY_ID}-{transport}",
        description="saved query foo",
        transport=transport,
    )
    saved_query_deleter.append(saved_query.name)
    expected_resource_name_suffix = f"savedQueries/{SAVED_QUERY_ID}-{transport}"
    assert saved_query.name.endswith(expected_resource_name_suffix)
