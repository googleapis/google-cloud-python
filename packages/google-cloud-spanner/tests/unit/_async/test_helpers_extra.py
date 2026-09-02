# Copyright 2024 Google LLC All rights reserved.
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

import unittest
from unittest import mock

from google.cloud.spanner_v1._async import _helpers as MUT


class TestHelpersExtra(unittest.IsolatedAsyncioTestCase):
    async def test_retry_allowed_exceptions_match(self):
        # coverage for line 54-58
        count = 0

        def func():
            nonlocal count
            count += 1
            if count == 1:
                raise ValueError("retry me")
            return "done"

        allowed = {ValueError: None}
        res = await MUT._retry(func, allowed_exceptions=allowed, delay=0.01)
        self.assertEqual(res, "done")
        self.assertEqual(count, 2)

    async def test_retry_allowed_exceptions_mismatch(self):
        # coverage for line 55-56
        def func():
            raise TypeError("don't retry me")

        allowed = {ValueError: None}
        with self.assertRaises(TypeError):
            await MUT._retry(func, allowed_exceptions=allowed, delay=0.01)

    async def test_retry_allowed_exceptions_callable_check(self):
        # coverage for line 57-59
        count = 0

        def func():
            nonlocal count
            count += 1
            raise ValueError("check me")

        def check_err(exc):
            return False  # don't retry

        allowed = {ValueError: check_err}
        with self.assertRaises(ValueError):
            await MUT._retry(
                func, allowed_exceptions=allowed, delay=0.01, retry_count=2
            )
        self.assertEqual(count, 1)

    async def test_retry_max_retries(self):
        # coverage for line 60-61
        def func():
            raise ValueError("always fail")

        with self.assertRaises(ValueError):
            await MUT._retry(func, retry_count=1, delay=0.01)

    async def test_retry_before_next_retry_callback(self):
        # coverage for line 62-65
        count = 0

        def func():
            nonlocal count
            count += 1
            if count == 1:
                raise ValueError("retry")
            return "done"

        callback_called = False

        async def before_retry(retries, delay):
            nonlocal callback_called
            callback_called = True

        res = await MUT._retry(func, before_next_retry=before_retry, delay=0.01)
        self.assertEqual(res, "done")
        self.assertTrue(callback_called)

    async def test_create_experimental_host_transport_tls_mtls(self):
        # coverage for lines 106-124
        from google.cloud.spanner_admin_instance_v1.services.instance_admin.transports.grpc_asyncio import (
            InstanceAdminGrpcAsyncIOTransport as InstanceAdminGrpcTransport,
        )

        with mock.patch("builtins.open", mock.mock_open(read_data=b"cert_data")):
            # Test TLS
            with mock.patch("grpc.aio.secure_channel") as mock_channel:
                MUT._create_experimental_host_transport(
                    InstanceAdminGrpcTransport, "host", False, "ca_cert", None, None
                )
                self.assertTrue(mock_channel.called)

            # Test mTLS
            with mock.patch("grpc.aio.secure_channel") as mock_channel:
                MUT._create_experimental_host_transport(
                    InstanceAdminGrpcTransport,
                    "host",
                    False,
                    "ca_cert",
                    "client_cert",
                    "client_key",
                )
                self.assertTrue(mock_channel.called)

    async def test_create_experimental_host_transport_errors(self):
        # coverage for line 118-130
        from google.cloud.spanner_admin_instance_v1.services.instance_admin.transports.grpc_asyncio import (
            InstanceAdminGrpcAsyncIOTransport as InstanceAdminGrpcTransport,
        )

        with mock.patch("builtins.open", mock.mock_open(read_data=b"cert_data")):
            # Missing client_key
            with self.assertRaises(ValueError):
                MUT._create_experimental_host_transport(
                    InstanceAdminGrpcTransport,
                    "host",
                    False,
                    "ca_cert",
                    "client_cert",
                    None,
                )

            # No TLS/mTLS config
            with self.assertRaises(ValueError):
                MUT._create_experimental_host_transport(
                    InstanceAdminGrpcTransport, "host", False, None, None, None
                )
