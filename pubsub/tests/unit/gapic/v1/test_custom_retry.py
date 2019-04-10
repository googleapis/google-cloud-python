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
"""Unit tests."""

import mock
import pytest

from google.api_core import retry
from google.api_core import exceptions
from google.api_core.gapic_v1 import config
from google.cloud.pubsub_v1.gapic import custom_retry


_DEFAULT_RETVAL = object()  # fake return value of the default retry predicate


@pytest.fixture
def method_config():
    mock_predicate = mock.Mock(return_value=_DEFAULT_RETVAL)
    meth_config = config.MethodConfig(
        retry=retry.Retry(predicate=mock_predicate), timeout=mock.Mock()
    )
    return meth_config


class TestPatchRetryPredicate(object):
    """Unit tests for the custom_retry.patch_retry_predicate() function."""

    def test_noop_if_retry_none(self, method_config):
        method_config = method_config._replace(retry=None)
        patched_config = custom_retry.patch_retry_predicate(method_config)
        assert patched_config is method_config

    def test_no_retry_if_invalid_grant(self, method_config):
        patched_config = custom_retry.patch_retry_predicate(method_config)

        exc = exceptions.ServiceUnavailable(
            "invalid_grant: Not a valid email or user ID."
        )
        new_predicate = patched_config.retry._predicate

        assert not new_predicate(exc)

    def test_default_retry_if_service_unavailable(self, method_config):
        patched_config = custom_retry.patch_retry_predicate(method_config)

        exc = exceptions.ServiceUnavailable("temporarily offline")
        new_predicate = patched_config.retry._predicate

        assert new_predicate(exc) is _DEFAULT_RETVAL

    def test_default_retry_if_service_unavailable(self, method_config):
        patched_config = custom_retry.patch_retry_predicate(method_config)

        exc = exceptions.Aborted("request aborted")
        new_predicate = patched_config.retry._predicate

        assert new_predicate(exc) is _DEFAULT_RETVAL
