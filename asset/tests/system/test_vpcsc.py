# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# flake8: noqa

import os
import pytest

from google.api_core import exceptions
from google.cloud import asset_v1
from google.cloud.asset_v1 import enums
from test_utils.vpcsc_config import vpcsc_config

_VPCSC_PROHIBITED_MESSAGE = "Request is prohibited by organization's policy"


@pytest.fixture
def client():
    return asset_v1.AssetServiceClient()


@pytest.fixture
def output_config():
    bucket_uri = "gs:{}/g-c-p-export-test".format(vpcsc_config.bucket_outside)
    output_config = {"gcsDestination": {"uri": bucket_uri}}


@pytest.fixture
def parent_inside():
    return "projects/" + vpcsc_config.project_inside


@pytest.fixture
def parent_outside():
    return "projects/" + vpcsc_config.project_outside


@vpcsc_config.skip_unless_inside_vpcsc
def test_export_assets_inside(client, output_config, parent_inside):
    with pytest.raises(exceptions.InvalidArgument):
        client.export_assets(parent_inside, output_config)


@vpcsc_config.skip_unless_inside_vpcsc
def test_export_assets_outside(client, output_config, parent_outside):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.export_assets(parent_outside, output_config)

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@vpcsc_config.skip_unless_inside_vpcsc
def test_batch_get_assets_history_inside(client, parent_inside):
    read_time_window = {}
    client.batch_get_assets_history(
        parent_inside,
        content_type=enums.ContentType.CONTENT_TYPE_UNSPECIFIED,
        read_time_window={},
    )


@vpcsc_config.skip_unless_inside_vpcsc
def test_batch_get_assets_history_outside(client, parent_outside):
    content_type = enums.ContentType.CONTENT_TYPE_UNSPECIFIED
    read_time_window = {}
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.batch_get_assets_history(
            parent_outside,
            content_type=enums.ContentType.CONTENT_TYPE_UNSPECIFIED,
            read_time_window={},
        )

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message
