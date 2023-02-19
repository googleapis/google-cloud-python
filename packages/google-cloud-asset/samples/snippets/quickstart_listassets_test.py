#!/usr/bin/env python

# Copyright 2020 Google LLC.
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

import quickstart_listassets

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.mark.parametrize("transport", ["grpc", "rest"])
def test_list_assets(transport, capsys):
    from google.cloud import asset_v1

    quickstart_listassets.list_assets(
        project_id=PROJECT,
        asset_types=["iam.googleapis.com/Role"],
        page_size=10,
        content_type=asset_v1.ContentType.RESOURCE,
        transport=transport,
    )
    out, _ = capsys.readouterr()
    assert "asset" in out

    quickstart_listassets.list_assets(
        project_id=PROJECT,
        asset_types=[],
        page_size=10,
        content_type=asset_v1.ContentType.RELATIONSHIP,
        transport=transport,
    )
    out_r, _ = capsys.readouterr()
    assert "asset" in out_r
