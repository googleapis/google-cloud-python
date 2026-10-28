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
"""Unit tests for the hand-rolled health codec and the breaker it drives.

The codec in ``_accelerator/_health.py`` exists so this package doesn't have to
depend on ``grpcio-health-checking`` for two trivial messages. That trade is only
sound if the bytes it produces and accepts are exactly what a real protobuf
implementation produces and accepts, so the tests here check it against
``google.protobuf.proto_builder`` — protobuf's own encoder, building a message
with the same field number and wire type as ``HealthCheckResponse.status``
rather than re-stating the byte strings the codec was written from.

The probe and polling loop are exercised over a real UDS gRPC server in
``tests/unit/data/_async/test__accelerator_health.py``.
"""

import pytest
from google.protobuf import descriptor_pb2, proto_builder

from google.cloud.bigtable.data._accelerator._fallback import AcceleratorBreaker
from google.cloud.bigtable.data._accelerator._health import (
    HEALTH_CHECK_METHOD,
    ServingStatus,
    parse_health_response,
    serialize_health_request,
)
from google.cloud.bigtable.data._sync_autogen._accelerator_health import (
    _AcceleratorHealthMonitor,
)

# A message shaped like HealthCheckResponse: one field, number 1, varint. An
# enum and an int32 share a wire type, so protobuf encodes these identically to
# the real generated class.
_ResponseLike = proto_builder.MakeSimpleProtoClass(
    {"status": descriptor_pb2.FieldDescriptorProto.TYPE_INT32},
    full_name="tests.bigtable.accelerator.HealthCheckResponseLike",
)


def _encode(status: int) -> bytes:
    return _ResponseLike(status=status).SerializeToString()


class TestHealthCodec:
    def test_request_is_the_empty_message(self):
        # HealthCheckRequest{service: ""} has every field at its proto3 default.
        assert serialize_health_request(None) == b""
        assert serialize_health_request(object()) == b""

    def test_method_name(self):
        assert HEALTH_CHECK_METHOD == "/grpc.health.v1.Health/Check"

    @pytest.mark.parametrize("status", list(ServingStatus))
    def test_parses_what_protobuf_encodes(self, status):
        assert parse_health_response(_encode(status.value)) == status

    def test_empty_payload_is_unknown(self):
        # proto3 omits a field at its default, so a real SERVING_STATUS of
        # UNKNOWN arrives as zero bytes. proto_builder emits proto2, which
        # writes the explicit zero instead; both must decode the same way.
        assert parse_health_response(b"") == ServingStatus.UNKNOWN
        assert parse_health_response(_encode(0)) == ServingStatus.UNKNOWN

    @pytest.mark.parametrize(
        "payload,reason",
        [
            (b"\x12\x01", "field 2, not the status field"),
            (b"\x09\x01", "field 1 but the wrong wire type"),
            (b"\x08", "tag with no varint after it"),
            (b"\x08\x80", "varint truncated mid-continuation"),
            (b"\x08\xac\x02", "a status value this client has never heard of"),
            (
                b"\x08\x01TRAILING_GARBAGE",
                "trailing unrecognized bytes after valid field",
            ),
            (bytes([0x08] + [0x80] * 9 + [0x02]), "10th byte shift >= 64 overflow"),
            (bytes([0x08] + [0x80] * 10 + [0x01]), "11-byte overlong varint"),
        ],
    )
    def test_unreadable_payloads_are_unknown(self, payload, reason):
        # UNKNOWN is what the monitor counts as a failed probe, which is the
        # safe reading of a response we cannot interpret.
        assert parse_health_response(payload) == ServingStatus.UNKNOWN, reason

    def test_repeated_field_last_one_wins(self):
        assert parse_health_response(b"\x08\x01\x08\x02") == ServingStatus.NOT_SERVING


class TestBreakerDegraded:
    def test_degraded_bypasses_and_clears(self):
        breaker = AcceleratorBreaker()
        assert not breaker.bypass()
        breaker.set_degraded(True)
        assert breaker.bypass() and breaker.is_degraded and not breaker.is_tripped
        breaker.set_degraded(False)
        assert not breaker.bypass()

    def test_clearing_degraded_cannot_undo_a_trip(self):
        # The whole point of keeping the two flags apart: a health recovery must
        # never resurrect an accelerator that replied UNIMPLEMENTED or died.
        breaker = AcceleratorBreaker()
        breaker.trip()
        breaker.set_degraded(True)
        breaker.set_degraded(False)
        assert breaker.bypass() and breaker.is_tripped and not breaker.is_degraded


class TestMonitorStateMachine:
    """Drives ``_record`` directly, so thresholds are checked without timing."""

    @staticmethod
    def _make_one(breaker, *, unhealthy=3, healthy=3):
        return _AcceleratorHealthMonitor(
            accelerator_client=None,
            breaker=breaker,
            unhealthy_threshold=unhealthy,
            healthy_threshold=healthy,
        )

    def test_degrades_only_on_the_full_streak(self):
        breaker = AcceleratorBreaker()
        monitor = self._make_one(breaker)
        for _ in range(2):
            monitor._record(False)
            assert not breaker.is_degraded
        monitor._record(False)
        assert breaker.is_degraded

    def test_one_good_probe_resets_the_failure_streak(self):
        # A daemon that is merely occasionally slow never trips: this is the
        # anti-flap property, and the reason a single GC pause is survivable.
        breaker = AcceleratorBreaker()
        monitor = self._make_one(breaker)
        for _ in range(10):
            monitor._record(False)
            monitor._record(False)
            monitor._record(True)
        assert not breaker.is_degraded

    def test_recovers_only_on_the_full_streak(self):
        breaker = AcceleratorBreaker()
        monitor = self._make_one(breaker)
        for _ in range(3):
            monitor._record(False)
        assert breaker.is_degraded
        for _ in range(2):
            monitor._record(True)
            assert breaker.is_degraded
        monitor._record(True)
        assert not breaker.is_degraded

    def test_one_bad_probe_resets_the_recovery_streak(self):
        breaker = AcceleratorBreaker()
        monitor = self._make_one(breaker)
        for _ in range(3):
            monitor._record(False)
        for _ in range(10):
            monitor._record(True)
            monitor._record(True)
            monitor._record(False)
        assert breaker.is_degraded

    def test_thresholds_of_one_flip_immediately(self):
        breaker = AcceleratorBreaker()
        monitor = self._make_one(breaker, unhealthy=1, healthy=1)
        monitor._record(False)
        assert breaker.is_degraded
        monitor._record(True)
        assert not breaker.is_degraded

    def test_never_clears_a_permanent_trip(self):
        breaker = AcceleratorBreaker()
        breaker.trip()
        monitor = self._make_one(breaker, healthy=1)
        monitor._record(True)
        assert breaker.bypass()


class TestSyncMonitorThread:
    """The sync monitor's thread, which has no counterpart in the async one."""

    @staticmethod
    def _make_one(**kwargs):
        kwargs.setdefault("interval", 0.01)
        return _AcceleratorHealthMonitor(
            accelerator_client=None, breaker=AcceleratorBreaker(), **kwargs
        )

    def test_loop_runs_on_a_daemon_thread(self):
        # Not a ThreadPoolExecutor worker: concurrent.futures joins its
        # non-daemon workers at interpreter exit, and this loop only ends on
        # close(), so a Table left unclosed would hang the process on the way
        # out. A daemon thread cannot hold exit up.
        monitor = self._make_one(interval=60.0)
        thread = None
        try:
            monitor.start()
            thread = monitor._task
            assert thread.daemon
            assert monitor.is_running
        finally:
            monitor.close()
        assert not thread.is_alive()

    def test_request_stop_ends_the_loop(self):
        # The weakref-finalizer path: sets a flag, waits for nothing, and the
        # loop notices at its next wakeup.
        monitor = self._make_one()
        monitor.start()
        thread = monitor._task
        try:
            monitor.request_stop()
            thread.join(timeout=10.0)
            assert not thread.is_alive()
            assert not monitor.is_running
        finally:
            monitor.close()

    def test_dead_daemon_trips_breaker_and_stops_loop(self):
        import unittest.mock

        breaker = AcceleratorBreaker()
        breaker.set_degraded(True)
        daemon = unittest.mock.Mock()
        daemon.is_running = False
        daemon._closed = False
        monitor = _AcceleratorHealthMonitor(
            accelerator_client=None,
            breaker=breaker,
            daemon=daemon,
            interval=0.01,
        )
        monitor.start()
        try:
            monitor._task.join(timeout=2.0)
            assert not monitor.is_running
            assert breaker.is_tripped
        finally:
            monitor.close()

    def test_post_probe_stop_does_not_mutate_breaker(self):
        import unittest.mock

        breaker = AcceleratorBreaker()
        client = unittest.mock.Mock()
        monitor = _AcceleratorHealthMonitor(
            accelerator_client=client,
            breaker=breaker,
            interval=0.01,
            unhealthy_threshold=1,
        )

        def fake_check_health(timeout=None):
            monitor.request_stop()
            raise RuntimeError("socket closed during teardown")

        client.check_health.side_effect = fake_check_health
        monitor.start()
        try:
            monitor._task.join(timeout=2.0)
            assert not monitor.is_running
            assert not breaker.is_degraded
        finally:
            monitor.close()
