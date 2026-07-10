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
"""Unit tests for how the client decides whether to start the accelerator
daemon. The accelerator is on by default and must degrade gracefully: it
disables itself (with a warning) when the emulator is set or the daemon can't
start, and only errors out on an explicit ``use_accelerator=True`` that
conflicts with the emulator. These exercise the pure enablement helpers on the
async target without spinning up a full client or event loop."""

from types import SimpleNamespace

import pytest

from google.cloud.bigtable.data._async.client import _DataApiTargetAsync


class _ConcreteTarget(_DataApiTargetAsync):
    """Minimal concrete subclass so the abstract base can be instantiated."""

    @property
    def _request_path(self):
        return {}


def _bare_target(start, emulator=None):
    """A target that skips __init__, wired with a fake client and a fake
    ``_start_accelerator`` so we can observe the enablement decision."""
    t = object.__new__(_ConcreteTarget)
    t.client = SimpleNamespace(_emulator_host=emulator, project="p")
    t.instance_id = "i"
    t.app_profile_id = None
    t._accelerator_daemon = "SENTINEL"
    t._accelerator_client = "SENTINEL"
    t._start_accelerator = start
    return t


def _ok_start(target):
    def _start():
        target._accelerator_client = "STARTED"
        target._accelerator_daemon = "STARTED"

    return _start


class TestMaybeStartAccelerator:
    def test_emulator_auto_disables_with_warning(self):
        """Default (non-explicit) + emulator: warn and use the native client."""
        called = []
        t = _bare_target(emulator="localhost:8086", start=lambda: called.append(1))
        with pytest.warns(RuntimeWarning, match="Accelerator disabled"):
            t._maybe_start_accelerator(explicit=False)
        assert called == []

    def test_emulator_explicit_raises(self):
        """Explicit use_accelerator=True + emulator is a hard misconfiguration."""
        t = _bare_target(emulator="localhost:8086", start=lambda: None)
        with pytest.raises(RuntimeError, match="use_accelerator=True is not supported"):
            t._maybe_start_accelerator(explicit=True)

    @pytest.mark.parametrize("explicit", [False, True])
    def test_start_failure_falls_back_to_native(self, explicit):
        """A daemon start failure (e.g. binary missing) never propagates; it
        warns and leaves the target on the native client."""

        def _boom():
            raise FileNotFoundError("no bundled binary")

        t = _bare_target(emulator=None, start=_boom)
        with pytest.warns(RuntimeWarning, match="Failed to start"):
            t._maybe_start_accelerator(explicit=explicit)
        assert t._accelerator_client is None
        assert t._accelerator_daemon is None

    def test_successful_start(self):
        t = _bare_target(emulator=None, start=None)
        t._start_accelerator = _ok_start(t)
        t._maybe_start_accelerator(explicit=False)
        assert t._accelerator_client == "STARTED"
        assert t._accelerator_daemon == "STARTED"

    def test_keyboard_interrupt_propagates(self):
        """Only Exception is swallowed; BaseException (Ctrl-C) must propagate."""

        def _interrupt():
            raise KeyboardInterrupt()

        t = _bare_target(emulator=None, start=_interrupt)
        with pytest.raises(KeyboardInterrupt):
            t._maybe_start_accelerator(explicit=False)
