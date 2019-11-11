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
from google.cloud import trace_v1
from test_utils.vpcsc_config import vpcsc_config

_VPCSC_PROHIBITED_MESSAGE = "Request is prohibited by organization's policy."


@pytest.fixture
def client():
    return trace_v1.TraceServiceClient()


@vpcsc_config.skip_unless_inside_vpcsc
def test_list_traces_w_inside(client):
    list(client.list_traces(vpcsc_config.project_inside))  # no perms issue


@vpcsc_config.skip_unless_inside_vpcsc
def test_list_traces_w_outside(client):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        list(client.list_traces(vpcsc_config.project_outside))

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@vpcsc_config.skip_unless_inside_vpcsc
def test_get_trace_w_inside(client):
    with pytest.raises(exceptions.InvalidArgument):
        client.get_trace(vpcsc_config.project_inside, "")  # no perms issue


@vpcsc_config.skip_unless_inside_vpcsc
def test_get_trace_w_outside(client):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.get_trace(vpcsc_config.project_outside, "")

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message


@vpcsc_config.skip_unless_inside_vpcsc
def test_patch_traces_w_inside(client):
    with pytest.raises(exceptions.InvalidArgument):
        client.patch_traces(vpcsc_config.project_inside, {})  # no perms issue


@vpcsc_config.skip_unless_inside_vpcsc
def test_patch_traces_w_ouside(client):
    with pytest.raises(exceptions.PermissionDenied) as exc:
        client.patch_traces(vpcsc_config.project_outside, {})

    assert _VPCSC_PROHIBITED_MESSAGE in exc.value.message
