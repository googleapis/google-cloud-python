# Copyright 2026 Google LLC
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
"""Unit tests for the UDS channel configuration in _accelerator_client.py."""

from unittest import mock

import pytest

from google.cloud.bigtable.data._async import _accelerator_client as async_module
from google.cloud.bigtable.data._sync_autogen import (
    _accelerator_client as sync_module,
)

_MODULES = pytest.mark.parametrize(
    "module, client_name",
    [
        (async_module, "_AsyncAcceleratorClient"),
        (sync_module, "_AcceleratorClient"),
    ],
    ids=["async", "sync"],
)


class TestChannelOptions:
    """The caps are load-bearing, and the option keys are easy to typo.

    A misspelled key is silently ignored by gRPC, which leaves the channel on
    the 4 MiB default and fails only on a large row.
    """

    @_MODULES
    def test_options_cap_each_direction_at_the_service_limit(self, module, client_name):
        # Inbound 256 MiB: the hard limit on all values in a single row.
        # Outbound 100 MB: the request size the service accepts.
        assert module._MAX_RECEIVE_MESSAGE_LENGTH == 256 * 1024 * 1024
        assert module._MAX_SEND_MESSAGE_LENGTH == 100 * 1024 * 1024
        assert module._CHANNEL_OPTIONS == (
            ("grpc.max_receive_message_length", 256 * 1024 * 1024),
            ("grpc.max_send_message_length", 100 * 1024 * 1024),
        )

    @_MODULES
    def test_channel_is_built_with_the_options(self, module, client_name):
        with mock.patch.object(module, "insecure_channel") as channel_mock:
            getattr(module, client_name)("/tmp/sock", "secret")
        channel_mock.assert_called_once_with(
            module._uds_target("/tmp/sock"), options=module._CHANNEL_OPTIONS
        )
