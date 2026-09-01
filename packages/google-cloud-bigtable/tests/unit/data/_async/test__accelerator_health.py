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

"""Probe and polling-loop tests for the accelerator health monitor.

These run against a real gRPC server on a real Unix domain socket, serving the
real ``/grpc.health.v1.Health/Check`` method name, reached through the real
``_AcceleratorClient`` and its hand-rolled codec. Nothing about the transport is
faked, so the slow-daemon case below genuinely exercises a gRPC deadline rather
than a raised sentinel — which matters, because a probe timeout is the whole
signal this monitor is built on.

The server replies with literal ``HealthCheckResponse`` bytes; that those
literals are what protobuf itself produces is established in
``tests/unit/data/test_accelerator_health.py``.
"""

import threading
import time
from concurrent import futures

import grpc
import pytest

from google.cloud.bigtable.data._accelerator._fallback import AcceleratorBreaker
from google.cloud.bigtable.data._accelerator._health import (
    HEALTH_CHECK_METHOD,
    ServingStatus,
)
from google.cloud.bigtable.data._cross_sync import CrossSync

if CrossSync.is_async:
    from google.cloud.bigtable.data._async._accelerator_client import (
        _AsyncAcceleratorClient as ClientType,
    )
    from google.cloud.bigtable.data._async._accelerator_health import (
        _AsyncAcceleratorHealthMonitor as MonitorType,
    )
else:
    from google.cloud.bigtable.data._sync_autogen._accelerator_client import (
        _AcceleratorClient as ClientType,
    )
    from google.cloud.bigtable.data._sync_autogen._accelerator_health import (
        _AcceleratorHealthMonitor as MonitorType,
    )

__CROSS_SYNC_OUTPUT__ = "tests.unit.data._sync_autogen.test__accelerator_health"

_AUTH_SECRET = "test-secret"

# HealthCheckResponse{status: S}: field 1, varint. See the codec test.
_WIRE_BY_STATUS = {
    ServingStatus.UNKNOWN: b"",
    ServingStatus.SERVING: b"\x08\x01",
    ServingStatus.NOT_SERVING: b"\x08\x02",
    ServingStatus.SERVICE_UNKNOWN: b"\x08\x03",
}


class _FakeDaemonHealthServer:
    """A real gRPC server standing in for the daemon's health service.

    Mirrors the daemon in the two ways that matter to the monitor: it serves the
    health method locally on the UDS, and (like the daemon's auth interceptor,
    which runs before the ``isProxied`` gate) it sees the accelerator token on
    every request. ``serve_health=False`` registers nothing, so gRPC itself
    answers ``UNIMPLEMENTED`` — the shape an older daemon presents.
    """

    def __init__(self, uds_path, *, status=ServingStatus.SERVING, serve_health=True):
        self.status = status
        self.delay = 0.0
        self.request_count = 0
        self.last_metadata = None
        self._lock = threading.Lock()
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        if serve_health:
            handler = grpc.unary_unary_rpc_method_handler(
                self._check,
                request_deserializer=lambda payload: payload,
                response_serializer=lambda payload: payload,
            )
            service, method = HEALTH_CHECK_METHOD.lstrip("/").split("/")
            self._server.add_generic_rpc_handlers(
                (grpc.method_handlers_generic_handler(service, {method: handler}),)
            )
        self._server.add_insecure_port(f"unix://{uds_path}")
        self._server.start()

    def _check(self, request, context):
        with self._lock:
            self.request_count += 1
            self.last_metadata = dict(context.invocation_metadata())
            delay, status = self.delay, self.status
        if delay:
            time.sleep(delay)
        return _WIRE_BY_STATUS[status]

    def stop(self):
        self._server.stop(None)


@CrossSync.convert_class(sync_name="TestAcceleratorHealthMonitor")
class TestAsyncAcceleratorHealthMonitor:
    @staticmethod
    def _start_server(tmp_path, **kwargs):
        return _FakeDaemonHealthServer(str(tmp_path / "bt_proxy.sock"), **kwargs)

    @staticmethod
    @CrossSync.convert
    def _make_client(tmp_path):
        return ClientType(str(tmp_path / "bt_proxy.sock"), _AUTH_SECRET)

    @staticmethod
    def _make_monitor(client, breaker, **kwargs):
        kwargs.setdefault("interval", 0.02)
        kwargs.setdefault("timeout", 5.0)
        kwargs.setdefault("unhealthy_threshold", 2)
        kwargs.setdefault("healthy_threshold", 2)
        return MonitorType(client, breaker, **kwargs)

    @staticmethod
    @CrossSync.convert
    async def _wait_for(predicate, timeout=15.0):
        """Poll ``predicate`` until true or the deadline passes."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return True
            await CrossSync.sleep(0.01)
        return predicate()

    @CrossSync.pytest
    @pytest.mark.parametrize(
        "status,expected",
        [
            (ServingStatus.SERVING, True),
            (ServingStatus.NOT_SERVING, False),
            (ServingStatus.UNKNOWN, False),
            (ServingStatus.SERVICE_UNKNOWN, False),
        ],
    )
    async def test_probe_reads_status_off_the_wire(self, tmp_path, status, expected):
        server = self._start_server(tmp_path, status=status)
        client = self._make_client(tmp_path)
        try:
            monitor = self._make_monitor(client, AcceleratorBreaker())
            assert await monitor._probe() is expected
        finally:
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_probe_sends_the_accelerator_token(self, tmp_path):
        # The daemon's auth interceptor is chained onto the whole server and
        # runs ahead of the Bigtable-only proxy gate, so an unauthenticated
        # probe would be rejected and every daemon would look degraded.
        server = self._start_server(tmp_path)
        client = self._make_client(tmp_path)
        try:
            monitor = self._make_monitor(client, AcceleratorBreaker())
            assert await monitor._probe() is True
            assert server.last_metadata["x-accelerator-token"] == _AUTH_SECRET
        finally:
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_probe_times_out_on_a_starved_daemon(self, tmp_path):
        # The case the whole feature exists for: the daemon is up and would
        # answer SERVING, but cannot get scheduled in time to say so.
        server = self._start_server(tmp_path)
        server.delay = 1.0
        client = self._make_client(tmp_path)
        try:
            monitor = self._make_monitor(client, AcceleratorBreaker(), timeout=0.05)
            started = time.monotonic()
            assert await monitor._probe() is False
            # Failed on the deadline, not by waiting out the slow handler.
            assert time.monotonic() - started < 0.9
        finally:
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_probe_reports_unimplemented_distinctly(self, tmp_path):
        server = self._start_server(tmp_path, serve_health=False)
        client = self._make_client(tmp_path)
        try:
            monitor = self._make_monitor(client, AcceleratorBreaker())
            # None, not False: an unmonitorable daemon is not a degraded one.
            assert await monitor._probe() is None
        finally:
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_probe_fails_when_nothing_is_listening(self, tmp_path):
        client = self._make_client(tmp_path)
        try:
            monitor = self._make_monitor(client, AcceleratorBreaker(), timeout=1.0)
            assert await monitor._probe() is False
        finally:
            await client.close()

    @CrossSync.pytest
    async def test_loop_degrades_then_recovers(self, tmp_path):
        server = self._start_server(tmp_path)
        client = self._make_client(tmp_path)
        breaker = AcceleratorBreaker()
        monitor = self._make_monitor(client, breaker)
        try:
            monitor.start()
            assert await self._wait_for(lambda: server.request_count >= 2)
            assert not breaker.bypass()

            server.status = ServingStatus.NOT_SERVING
            assert await self._wait_for(lambda: breaker.is_degraded)
            assert breaker.bypass()
            # Reversible, and never a permanent trip.
            assert not breaker.is_tripped

            server.status = ServingStatus.SERVING
            assert await self._wait_for(lambda: not breaker.is_degraded)
            assert not breaker.bypass()
        finally:
            await monitor.close()
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_loop_stops_against_a_daemon_without_health(self, tmp_path):
        # An older daemon must keep serving accelerated traffic, not be
        # abandoned because it can't be monitored.
        server = self._start_server(tmp_path, serve_health=False)
        client = self._make_client(tmp_path)
        breaker = AcceleratorBreaker()
        monitor = self._make_monitor(client, breaker, unhealthy_threshold=1)
        try:
            monitor.start()
            # The loop exits outright rather than backing off, and — with an
            # unhealthy_threshold of 1, which would otherwise degrade on the
            # very first probe — leaves the breaker alone.
            assert await self._wait_for(lambda: monitor._task.done())
            assert not breaker.bypass()
        finally:
            await monitor.close()
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_loop_stops_once_the_breaker_is_tripped(self, tmp_path):
        server = self._start_server(tmp_path)
        client = self._make_client(tmp_path)
        breaker = AcceleratorBreaker()
        monitor = self._make_monitor(client, breaker)
        try:
            monitor.start()
            assert await self._wait_for(lambda: server.request_count >= 1)
            breaker.trip()
            assert await self._wait_for(lambda: monitor._task.done())
        finally:
            await monitor.close()
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_close_stops_polling(self, tmp_path):
        server = self._start_server(tmp_path)
        client = self._make_client(tmp_path)
        monitor = self._make_monitor(client, AcceleratorBreaker())
        try:
            monitor.start()
            assert await self._wait_for(lambda: server.request_count >= 1)
            await monitor.close()
            await CrossSync.sleep(0.2)
            counted = server.request_count
            await CrossSync.sleep(0.2)
            assert server.request_count == counted
        finally:
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_close_leaves_a_degraded_flag_set(self, tmp_path):
        # Closing the monitor is a teardown step, not a verdict that the daemon
        # got better; it must not silently re-enable accelerated routing.
        server = self._start_server(tmp_path, status=ServingStatus.NOT_SERVING)
        client = self._make_client(tmp_path)
        breaker = AcceleratorBreaker()
        monitor = self._make_monitor(client, breaker)
        try:
            monitor.start()
            assert await self._wait_for(lambda: breaker.is_degraded)
            await monitor.close()
            assert breaker.bypass()
        finally:
            await client.close()
            server.stop()

    @CrossSync.pytest
    async def test_start_is_idempotent(self):
        # A long interval keeps the task parked in its first wait, so no probe
        # is attempted and the client is never touched.
        monitor = self._make_monitor(None, AcceleratorBreaker(), interval=60.0)
        try:
            monitor.start()
            first = monitor._task
            monitor.start()
            assert monitor._task is first
        finally:
            await monitor.close()
