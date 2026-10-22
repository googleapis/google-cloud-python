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
#
"""Background health monitor for the accelerator daemon.

Polls ``grpc.health.v1.Health/Check`` on the daemon's UDS and flips the
reversible "degraded" flag on the Table's :class:`AcceleratorBreaker`, which
routes calls to the native client while it is set.

**The probe timeout is the actual signal.** The daemon answers a health check
entirely out of its own process — no session, no Channel, no network — so the
call is a few microseconds of work plus however long the daemon's Go scheduler
took to get to it. A handler that cheap missing its deadline means the daemon is
not being scheduled, which is exactly the failure mode this guards against (an
undersized GOMAXPROCS, CFS throttling against a cgroup quota, a long
stop-the-world pause). The daemon deliberately never self-reports NOT_SERVING
under load: it cannot pick that threshold from the inside, so the caller
measures instead.

**This is a stall detector, not a latency monitor, and the difference matters.**
A measurably starved daemon runs on the order of tens of milliseconds behind on
each wakeup, which is well worth falling back from but sits uncomfortably close
to the noise floor of the measurement: the probe is issued from the caller's own
process, so a busy Python event loop inflates it just as a busy daemon does, and
a false positive there abandons the accelerator for a native path running in the
same busy process. A single-sample deadline cannot separate those two, so the
default is set to catch severe stalls confidently rather than mild degradation
unreliably. Catching the milder regime needs a different instrument — either the
daemon-side ``pacemaker_delays`` metric, which measures Go scheduling delay
directly and is already exported, or folding probe *latencies* into a
distribution here instead of thresholding each one.

Both the trip and the recovery need several consecutive probes to agree. A
single slow probe is a GC pause, not a starved process, and flapping the route
on every one of those would be worse than either steady state.
"""

from __future__ import annotations

import logging
import threading
from typing import Any

from grpc import StatusCode

from google.cloud.bigtable.data._accelerator._fallback import (
    AcceleratorBreaker,
    _grpc_code,
)
from google.cloud.bigtable.data._accelerator._health import ServingStatus
from google.cloud.bigtable.data._cross_sync import CrossSync

if CrossSync.is_async:
    from google.cloud.bigtable.data._async._accelerator_client import (
        _AsyncAcceleratorClient as AcceleratorClientType,
    )
else:
    from google.cloud.bigtable.data._sync_autogen._accelerator_client import (  # noqa: F401
        _AcceleratorClient as AcceleratorClientType,
    )

__CROSS_SYNC_OUTPUT__ = "google.cloud.bigtable.data._sync_autogen._accelerator_health"

_LOGGER = logging.getLogger(__name__)

#: Seconds between probes. Cheap enough to be frequent, sparse enough that the
#: monitor is never a meaningful share of the daemon's load.
DEFAULT_PROBE_INTERVAL = 5.0

#: Deadline for a single probe, and thereby the latency threshold that defines
#: "starved". A healthy round trip is well under a millisecond of actual work,
#: so this is enormous headroom -- deliberately. The probe is issued from the
#: caller's own process, so it measures that process's scheduling as well as the
#: daemon's, and on a busy event loop tens of milliseconds is normal for a
#: perfectly healthy daemon. Tightening this much further starts trading real
#: detection for false positives that fall back to a native path running in the
#: same busy process, which helps nobody. See the module docstring for what that
#: means for the failures this can and cannot see.
DEFAULT_PROBE_TIMEOUT = 0.25

#: Consecutive probes that must agree before the route changes: bad ones before
#: falling back, good ones before routing back. Three of them at the default
#: interval is roughly 10-15 seconds of sustained evidence in either direction —
#: a range rather than a figure because the loop waits before it probes, so a
#: change in the daemon is never seen sooner than the next scheduled probe.
DEFAULT_UNHEALTHY_THRESHOLD = 3
DEFAULT_HEALTHY_THRESHOLD = 3

#: How long ``close()`` waits for the polling loop to finish. It is already
#: cancelled (async) or signalled (sync) by then, so the only thing this covers
#: is a probe in flight, bounded by the probe timeout.
_CLOSE_WAIT_SECONDS = 1.0


@CrossSync.convert_class(sync_name="_AcceleratorHealthMonitor")
class _AsyncAcceleratorHealthMonitor:
    """Polls the daemon's health and drives the breaker's degraded flag.

    One instance per Table, owned by the Table and stopped by ``Table.close``.
    """

    def __init__(
        self,
        accelerator_client: AcceleratorClientType,
        breaker: AcceleratorBreaker,
        *,
        interval: float = DEFAULT_PROBE_INTERVAL,
        timeout: float = DEFAULT_PROBE_TIMEOUT,
        unhealthy_threshold: int = DEFAULT_UNHEALTHY_THRESHOLD,
        healthy_threshold: int = DEFAULT_HEALTHY_THRESHOLD,
    ):
        self._client = accelerator_client
        self._breaker = breaker
        self._interval = interval
        self._timeout = timeout
        self._unhealthy_threshold = unhealthy_threshold
        self._healthy_threshold = healthy_threshold
        self._consecutive_failures = 0
        self._consecutive_successes = 0
        # A threading.Event in both variants, deliberately not CrossSync.Event:
        # an asyncio.Event may only be set from the loop thread, and this one
        # is also set by a weakref finalizer running on whatever thread the
        # collection happened on. Nothing ever *awaits* it — the sync loop
        # blocks on it, the async loop only reads it between sleeps — so it
        # needs no loop affinity. See _run() and request_stop().
        self._closed = threading.Event()
        # An asyncio.Task when async; a daemon thread when sync. See start().
        self._task: Any = None

    def start(self) -> None:
        """Launch the polling task. Idempotent."""
        if self._task is not None:
            return
        if CrossSync.is_async:
            self._task = CrossSync.create_task(
                self._run, task_name="bigtable-accelerator-health"
            )
        else:
            # A dedicated daemon thread rather than a ThreadPoolExecutor
            # worker: the loop runs for the life of the Table, and
            # concurrent.futures *joins* its (non-daemon) workers at
            # interpreter exit, so a Table that is never closed would hang the
            # process on the way out. A dedicated thread also keeps the loop
            # out of a pool slot other work is queued behind.
            self._task = threading.Thread(
                target=self._run,
                name="bigtable-accelerator-health",
                daemon=True,
            )
            self._task.start()

    @property
    def is_running(self) -> bool:
        """Whether the polling loop is still alive."""
        if self._task is None:
            return False
        if CrossSync.is_async:
            return not self._task.done()
        return self._task.is_alive()

    def request_stop(self) -> None:
        """Ask the loop to stop, without waiting for it to finish.

        For callers that cannot await ``close()`` — notably a weakref finalizer
        on the owning Table, which is what stops a monitor whose Table was
        dropped without being closed. Setting a threading.Event is safe from
        any thread and during interpreter shutdown. The sync loop wakes on it
        immediately; the async loop sees it at its next wakeup, since only
        ``close()`` can cancel the task outright.
        """
        self._closed.set()

    @CrossSync.convert
    async def _run(self) -> None:
        """Poll until closed, or until monitoring turns out to be pointless."""
        while not self._closed.is_set():
            if CrossSync.is_async:
                # Sleep rather than wait on the event: it is a threading.Event
                # (see __init__), so there is nothing here to await. close()
                # cancels this task, which interrupts the sleep, and
                # request_stop() is picked up by the check below.
                await CrossSync.sleep(self._interval)
            else:
                self._closed.wait(timeout=self._interval)
            if self._closed.is_set():
                return
            if self._breaker.is_tripped:
                # The accelerator has been permanently abandoned for some other
                # reason; nothing this monitor observes can change that.
                return
            healthy = await self._probe()
            if healthy is None:
                # The daemon does not serve health checks at all. Stop probing
                # and leave the breaker undegraded: an unmonitorable daemon is
                # not a degraded one, and treating it as one would disable the
                # accelerator against every daemon older than this feature.
                #
                # Clearing is not redundant. An earlier streak of probes can
                # have degraded the breaker already — a daemon too starved to
                # answer even UNIMPLEMENTED before the deadline looks exactly
                # like an unhealthy one — and this return is the last thing
                # that runs, so a flag left set here is never cleared by
                # anyone. (A permanent trip is handled above and stays.)
                self._breaker.set_degraded(False)
                _LOGGER.info(
                    "Accelerator daemon does not implement the gRPC health "
                    "service; health-based fallback is disabled for this table."
                )
                return
            self._record(healthy)

    @CrossSync.convert
    async def _probe(self) -> bool | None:
        """Run one probe.

        Returns True if the daemon answered SERVING within the timeout, False if
        it answered late, errored, or reported anything else, and None if it
        does not implement the health service (see :meth:`_run`).
        """
        # Deliberately silent per probe: a probe fails once every interval for as
        # long as the daemon is unwell, so anything logged here is unbounded. The
        # transitions in :meth:`_record` are the events worth reporting, and they
        # fire once each.
        try:
            status = await self._client.check_health(timeout=self._timeout)
        except Exception as exc:
            if _grpc_code(exc) == StatusCode.UNIMPLEMENTED:
                return None
            return False
        return status == ServingStatus.SERVING

    def _record(self, healthy: bool) -> None:
        """Fold one probe result into the streak counters and act on it."""
        if healthy:
            self._consecutive_failures = 0
            self._consecutive_successes += 1
            if (
                self._breaker.is_degraded
                and self._consecutive_successes >= self._healthy_threshold
            ):
                _LOGGER.info(
                    "Accelerator daemon is healthy again after %d consecutive "
                    "successful health checks; resuming accelerated routing.",
                    self._consecutive_successes,
                )
                self._breaker.set_degraded(False)
        else:
            self._consecutive_successes = 0
            self._consecutive_failures += 1
            if (
                not self._breaker.is_degraded
                and self._consecutive_failures >= self._unhealthy_threshold
            ):
                _LOGGER.warning(
                    "Accelerator daemon failed %d consecutive health checks "
                    "(%gs timeout); falling back to the native Bigtable client "
                    "until it recovers.",
                    self._consecutive_failures,
                    self._timeout,
                )
                self._breaker.set_degraded(True)

    @CrossSync.convert
    async def close(self) -> None:
        """Stop polling and wait for the loop to finish.

        Does not clear a degraded flag already set. Waiting is bounded by
        ``_CLOSE_WAIT_SECONDS``: the caller is entitled to have the monitor
        actually stopped when this returns, because the channel it probes over
        is closed immediately afterwards, and a probe still running into that
        would log an alarming "falling back" warning during orderly teardown.
        """
        self._closed.set()
        task, self._task = self._task, None
        if task is None:
            return
        if CrossSync.is_async:
            task.cancel()
            # Retrieve any exception so asyncio doesn't log "Task exception was
            # never retrieved" — as a callback too, in case the wait times out
            # and the task completes after we stop looking.
            task.add_done_callback(lambda t: None if t.cancelled() else t.exception())
            await CrossSync.wait([task], timeout=_CLOSE_WAIT_SECONDS)
        else:
            task.join(timeout=_CLOSE_WAIT_SECONDS)
