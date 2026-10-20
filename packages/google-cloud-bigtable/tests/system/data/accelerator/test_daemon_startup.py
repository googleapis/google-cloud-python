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

import time

import pytest

from google.cloud.bigtable.data._accelerator._daemon import AcceleratorDaemon

from . import _harness

_FLAGS = ["--project", "p", "--instance", "i", "--app-profile", "ap"]


def test_nonexecutable_binary_raises_on_start(tmp_bin_dir, monkeypatch):
    monkeypatch.setenv("BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT", "2.0")
    path = _harness.nonexecutable_binary(tmp_bin_dir)
    daemon = AcceleratorDaemon(_FLAGS, binary_path=path)
    with pytest.raises(RuntimeError, match="spawn"):
        _harness.call_with_timeout(daemon.start, timeout=5.0)
    _harness.force_kill_daemon(daemon)


def test_exit_during_startup_raises_promptly(tmp_bin_dir, monkeypatch):
    monkeypatch.setenv("BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT", "5.0")
    path = _harness.immediately_exiting_binary(tmp_bin_dir, exit_code=3)
    daemon = AcceleratorDaemon(_FLAGS, binary_path=path)
    started = time.monotonic()
    with pytest.raises(RuntimeError, match="exited during startup"):
        _harness.call_with_timeout(daemon.start, timeout=5.0)
    elapsed = time.monotonic() - started
    assert elapsed < 3.0, f"exit-during-startup took {elapsed:.2f}s; not prompt"
    _harness.force_kill_daemon(daemon)


def test_never_binds_honors_startup_timeout(tmp_bin_dir, monkeypatch):
    monkeypatch.setenv("BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT", "1.0")
    path = _harness.never_binds_binary(tmp_bin_dir)
    daemon = AcceleratorDaemon(_FLAGS, binary_path=path)
    started = time.monotonic()
    try:
        with pytest.raises(RuntimeError, match="did not become ready"):
            _harness.call_with_timeout(daemon.start, timeout=4.0)
        elapsed = time.monotonic() - started
        assert elapsed < 3.0, f"never-binds took {elapsed:.2f}s; not honoring timeout"
    finally:
        _harness.force_kill_daemon(daemon)
