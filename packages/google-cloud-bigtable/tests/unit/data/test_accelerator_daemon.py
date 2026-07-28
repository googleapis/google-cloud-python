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

import json
import os
import unittest.mock

import pytest

from google.cloud.bigtable.data._accelerator import _daemon
from google.cloud.bigtable.data._accelerator._daemon import (
    _IDENTITY_FILENAME,
    AcceleratorDaemon,
)


def _make_daemon(tmp_path, **kwargs):
    # Patch _resolve_binary_path so the constructor doesn't require the bundled
    # binary; tests that call start() monkeypatch Popen separately.
    fake_binary = tmp_path / "fake-binary"
    fake_binary.touch()
    with unittest.mock.patch(
        "google.cloud.bigtable.data._accelerator._daemon._resolve_binary_path",
        return_value=str(fake_binary),
    ):
        return AcceleratorDaemon(**kwargs)


class TestExtraEnv:
    def test_default_env_none(self, tmp_path, monkeypatch):
        captured = {}

        def fake_popen(argv, **kwargs):
            captured.update(kwargs)
            raise _StopStart()

        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        daemon = _make_daemon(tmp_path)
        with pytest.raises(_StopStart):
            daemon.start()
        # No extra_env -> inherit parent environment (env=None).
        assert captured["env"] is None

    def test_extra_env_merged_over_parent(self, tmp_path, monkeypatch):
        captured = {}

        def fake_popen(argv, **kwargs):
            captured.update(kwargs)
            raise _StopStart()

        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        monkeypatch.setenv("EXISTING", "keep")
        daemon = _make_daemon(
            tmp_path,
            extra_env={"GOOGLE_APPLICATION_CREDENTIALS": "/path/to/key.json"},
        )
        with pytest.raises(_StopStart):
            daemon.start()
        env = captured["env"]
        assert env["GOOGLE_APPLICATION_CREDENTIALS"] == "/path/to/key.json"
        # Parent env is preserved (merged, not replaced).
        assert env["EXISTING"] == "keep"


class TestReadIdentity:
    def test_reads_and_unlinks(self, tmp_path):
        daemon = _make_daemon(tmp_path)
        d = tmp_path / "accel-tmp"
        d.mkdir()
        daemon._tempdir = str(d)
        identity_path = d / _IDENTITY_FILENAME
        identity_path.write_text(
            json.dumps({"principal": "svc@proj.iam.gserviceaccount.com"})
        )
        result = daemon.read_identity()
        assert result["principal"] == "svc@proj.iam.gserviceaccount.com"
        # The identity is verified once, then consumed.
        assert not identity_path.exists()

    def test_not_started_raises(self, tmp_path):
        daemon = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="has not been started"):
            daemon.read_identity()

    def test_missing_file_raises(self, tmp_path):
        daemon = _make_daemon(tmp_path)
        d = tmp_path / "accel-tmp"
        d.mkdir()
        daemon._tempdir = str(d)
        with pytest.raises(RuntimeError, match="did not write"):
            daemon.read_identity()


class TestAuthSecret:
    def test_raises_before_start(self, tmp_path):
        daemon = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="has not been started"):
            _ = daemon.auth_secret

    def test_written_to_stdin_after_popen(self, tmp_path, monkeypatch):
        """start() mints a secret and writes 'secret\n' to the daemon's stdin."""
        written = []

        class FakeStdin:
            def write(self, data):
                written.append(data)

            def flush(self):
                pass

        class FakeProc:
            pid = 12345
            stdin = FakeStdin()

            def poll(self):
                return None

        def fake_popen(argv, **kwargs):
            raise _StopStart()

        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        daemon = _make_daemon(tmp_path)
        with pytest.raises(_StopStart):
            daemon.start()
        # Popen raises _StopStart before secret is written; check that the
        # secret is written when Popen succeeds by using a real pipe below.

    def test_secret_written_to_stdin(self, tmp_path, monkeypatch):
        """The secret is urlsafe and ends with a newline on the wire."""
        written = bytearray()

        class FakeStdin:
            def write(self, data):
                written.extend(data)

            def flush(self):
                pass

        class FakeProc:
            pid = 12345
            stdin = FakeStdin()

            def poll(self):
                return None

        def fake_popen(argv, **kwargs):
            return FakeProc()

        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        daemon = _make_daemon(tmp_path)
        # _wait_until_ready will fail immediately (process is fake); we just
        # need to get past the stdin-write step, so patch _wait_until_ready.
        monkeypatch.setattr(daemon, "_wait_until_ready", lambda timeout: None)
        daemon.start()
        payload = written.decode()
        assert payload.endswith("\n"), "secret payload must end with newline"
        token = payload.rstrip("\n")
        assert token == daemon.auth_secret
        # token_urlsafe(32) produces ≥32 chars of base64url characters.
        assert len(token) >= 32
        import re

        assert re.fullmatch(r"[A-Za-z0-9_\-]+", token), "expected urlsafe token"

    def test_broken_pipe_kills_and_reraises(self, tmp_path, monkeypatch):
        """A broken pipe during secret write force-kills the daemon and raises."""

        class FakeStdin:
            def write(self, data):
                raise OSError("broken pipe")

            def flush(self):
                pass

        class FakeProc:
            pid = 12345
            stdin = FakeStdin()

            def poll(self):
                return None

        def fake_popen(argv, **kwargs):
            return FakeProc()

        killed = []
        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        monkeypatch.setattr(
            AcceleratorDaemon, "_force_kill", lambda self: killed.append(True)
        )
        daemon = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="auth secret"):
            daemon.start()
        assert killed, "_force_kill should have been called on broken pipe"


class _StopStart(Exception):
    """Sentinel to abort AcceleratorDaemon.start() right after Popen so the test
    never waits on a real socket."""


@pytest.fixture(autouse=True)
def _no_cleanup_crash(monkeypatch, tmp_path):
    # start() force-kills and cleans up on the _StopStart exception; make those
    # no-ops so the fake (never-really-spawned) process doesn't blow up.
    monkeypatch.setattr(AcceleratorDaemon, "_force_kill", lambda self: None)
    monkeypatch.setattr(AcceleratorDaemon, "_cleanup_tempdir", lambda self: None)

    # Keep the daemon's tempdir inside pytest's tmp so nothing leaks to /tmp.
    def fake_mkdtemp(prefix=""):
        d = tmp_path / "accel-tmp"
        os.makedirs(d, exist_ok=True)
        return str(d)

    monkeypatch.setattr(_daemon.tempfile, "mkdtemp", fake_mkdtemp)
    yield
