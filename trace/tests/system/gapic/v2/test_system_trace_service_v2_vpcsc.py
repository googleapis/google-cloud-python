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
from google.cloud import trace_v2
from test_utils.vpcsc_config import vpcsc_config

_VPCSC_PROHIBITED_MESSAGE = "Request is prohibited by organization's policy."


@pytest.fixture
def client():
    return trace_v2.TraceServiceClient()


@vpcsc_config.skip_unless_inside_vpcsc
def test_batch_write_spans_w_inside(client):
    project_inside = client.project_path(vpcsc_config.project_inside)
    client.batch_write_spans(project_inside, [])  # no raise


@vpcsc_config.skip_unless_inside_vpcsc
def test_batch_write_spans_w_outside(client):
    project_outside = client.project_path(vpcsc_config.project_outside)

    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.batch_write_spans(project_outside, [])

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message
