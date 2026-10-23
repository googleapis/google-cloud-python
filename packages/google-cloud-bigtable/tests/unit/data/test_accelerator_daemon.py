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
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest.mock

import pytest

from google.cloud.bigtable.data._accelerator import _daemon
from google.cloud.bigtable.data._accelerator._daemon import (
    _DEFAULT_STARTUP_TIMEOUT,
    _IDENTITY_FILENAME,
    _STARTUP_TIMEOUT_ENV_VAR,
    AcceleratorDaemon,
    _resolve_startup_timeout,  # noqa: F401 (used indirectly by AcceleratorDaemon)
)


def _make_daemon(tmp_path, **kwargs):
    # Use binary_path= so the constructor doesn't require the bundled binary;
    # tests that call start() monkeypatch Popen separately.
    fake_binary = tmp_path / "fake-binary"
    fake_binary.touch()
    kwargs.setdefault("binary_path", str(fake_binary))
    return AcceleratorDaemon(**kwargs)


# Captured at import time, before the autouse fixture patches _cleanup_tempdir
# to a no-op.  Tests that need to exercise the real implementation call this
# directly as _real_cleanup_tempdir(daemon_instance).
_real_cleanup_tempdir = AcceleratorDaemon._cleanup_tempdir

# Likewise for tempfile.mkdtemp/gettempdir, which the autouse fixture
# redirects into pytest's tmp_path.  The sweep tests need real, short /tmp
# paths: they bind Unix sockets, whose paths are capped at ~107 bytes, and
# pytest's per-test directory names alone eat most of that budget.
_real_mkdtemp = tempfile.mkdtemp
_real_gettempdir = tempfile.gettempdir

# Distinguishes "caller did not ask for a namespace stamp" (use our own, the
# ordinary case) from "caller asked for no stamp at all" (None).
_UNSET = object()


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

    # start() kicks off _sweep_stale_tempdirs on a background thread, and the
    # sweep reads gettempdir() rather than going through mkdtemp. Without this
    # the suite would glob — and rmtree — real bt-accel-* directories in the
    # developer's or CI machine's /tmp, including live ones.
    monkeypatch.setattr(_daemon.tempfile, "gettempdir", lambda: str(tmp_path))
    yield


# ---------------------------------------------------------------------------
# Properties before/after start
# ---------------------------------------------------------------------------


class TestPropertiesBeforeStart:
    def test_uds_path_before_start_raises(self, tmp_path):
        d = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="has not been started"):
            _ = d.uds_path

    def test_log_path_before_start_raises(self, tmp_path):
        d = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="has not been started"):
            _ = d.log_path

    def test_pid_before_start_raises(self, tmp_path):
        d = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="has not been started"):
            _ = d.pid

    def test_is_running_before_start_is_false(self, tmp_path):
        d = _make_daemon(tmp_path)
        assert d.is_running is False

    def test_is_running_with_live_proc(self, tmp_path):
        d = _make_daemon(tmp_path)
        proc_mock = unittest.mock.Mock()
        proc_mock.poll.return_value = None  # still running
        d._proc = proc_mock
        assert d.is_running is True

    def test_is_running_with_dead_proc(self, tmp_path):
        d = _make_daemon(tmp_path)
        proc_mock = unittest.mock.Mock()
        proc_mock.poll.return_value = 0  # exited
        d._proc = proc_mock
        assert d.is_running is False


# ---------------------------------------------------------------------------
# Binary resolution
# ---------------------------------------------------------------------------


class TestResolveBinaryPath:
    def test_missing_binary_raises_file_not_found(self, tmp_path):
        from google.cloud.bigtable.data._accelerator._daemon import _resolve_binary_path

        with unittest.mock.patch("os.path.isfile", return_value=False):
            with pytest.raises(FileNotFoundError, match="Accelerator binary not found"):
                _resolve_binary_path()


# ---------------------------------------------------------------------------
# start() failure modes
# ---------------------------------------------------------------------------


class TestStartFailures:
    def test_called_twice_raises(self, tmp_path, monkeypatch):
        def fake_popen(argv, **kwargs):
            raise _StopStart()

        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        d = _make_daemon(tmp_path)
        # Manually set _proc so it looks like it was already started.
        d._proc = unittest.mock.Mock()
        with pytest.raises(RuntimeError, match="called twice"):
            d.start()

    def test_popen_oserror_raises_runtime_error(self, tmp_path, monkeypatch):
        def bad_popen(argv, **kwargs):
            raise OSError("permission denied")

        monkeypatch.setattr(_daemon.subprocess, "Popen", bad_popen)
        d = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="Failed to spawn"):
            d.start()

    @pytest.mark.parametrize(
        "doomed",
        [
            _daemon._LOG_FILENAME,
            _daemon._STARTUP_DEADLINE_FILENAME,
            _daemon._PID_FILENAME,
        ],
    )
    def test_metadata_write_failure_cleans_up_and_raises(
        self, tmp_path, monkeypatch, doomed
    ):
        # An unwritable tempdir fails start() the same way a failed spawn
        # does, whichever of the files start() lays down hits the error. The
        # tempdir must not survive a failure before daemon.log exists, since
        # the sweep keys off that marker and would never reap it.
        monkeypatch.setattr(
            AcceleratorDaemon, "_cleanup_tempdir", _real_cleanup_tempdir
        )
        real_open = open

        def bad_open(path, *args, **kwargs):
            # The deadline file is written to a ".tmp" sibling and renamed, so
            # match on the prefix rather than the final name.
            if os.path.basename(str(path)).startswith(doomed):
                raise OSError("no space left on device")
            return real_open(path, *args, **kwargs)

        monkeypatch.setattr(_daemon, "open", bad_open, raising=False)
        d = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="Failed to write accelerator daemon"):
            d.start()
        assert d._tempdir is None
        assert not (tmp_path / "accel-tmp").exists()

    def test_process_exits_during_startup_raises(self, tmp_path, monkeypatch):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.poll.return_value = 1  # exited immediately
        proc_mock.stdin = unittest.mock.Mock()

        monkeypatch.setattr(_daemon.subprocess, "Popen", lambda *a, **kw: proc_mock)
        # _cleanup_tempdir is already a no-op via autouse fixture, but
        # _force_kill is too — that's fine, we just need the start to raise.
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "0.1")
        d = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="exited during startup"):
            d.start()

    def test_uds_never_appears_raises_timeout(self, tmp_path, monkeypatch):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.poll.return_value = None  # alive but UDS never arrives
        proc_mock.stdin = unittest.mock.Mock()

        monkeypatch.setattr(_daemon.subprocess, "Popen", lambda *a, **kw: proc_mock)
        # Make os.path.exists always False so UDS never appears.
        monkeypatch.setattr(_daemon.os.path, "exists", lambda p: False)
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "0.05")
        d = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="did not become ready"):
            d.start()

    def test_no_af_unix_raises_os_error(self, tmp_path, monkeypatch):
        import socket as _socket

        monkeypatch.delattr(_socket, "AF_UNIX", raising=False)
        # Reload the attribute check in _daemon
        monkeypatch.setattr(_daemon.socket, "AF_UNIX", None, raising=False)
        # Simpler: just check that hasattr(socket, "AF_UNIX") guards the call.
        with (
            unittest.mock.patch.object(_daemon.socket, "AF_UNIX", None, create=True),
            unittest.mock.patch(
                "google.cloud.bigtable.data._accelerator._daemon.hasattr",
                return_value=False,
            ),
        ):
            d = _make_daemon(tmp_path)
            with pytest.raises(OSError, match="AF_UNIX"):
                d.start()


# ---------------------------------------------------------------------------
# close() lifecycle
# ---------------------------------------------------------------------------


class TestClose:
    def test_close_before_start_is_noop(self, tmp_path):
        d = _make_daemon(tmp_path)
        d.close()  # should not raise

    def test_close_graceful_via_stdin_eof(self, tmp_path):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.poll.return_value = None
        proc_mock.stdin = unittest.mock.Mock()
        # First wait call returns True (exited after stdin close).
        d = _make_daemon(tmp_path)
        d._proc = proc_mock

        with (
            unittest.mock.patch.object(d, "_wait_for_exit", return_value=True),
            unittest.mock.patch.object(d, "_cleanup_tempdir"),
        ):
            d.close()

        proc_mock.stdin.close.assert_called_once()
        proc_mock.terminate.assert_not_called()
        proc_mock.kill.assert_not_called()

    def test_close_escalates_to_sigterm(self, tmp_path):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.poll.return_value = None
        proc_mock.stdin = unittest.mock.Mock()
        d = _make_daemon(tmp_path)
        d._proc = proc_mock

        wait_results = iter([False, True])  # stdin wait fails, sigterm wait succeeds

        with (
            unittest.mock.patch.object(d, "_wait_for_exit", side_effect=wait_results),
            unittest.mock.patch.object(d, "_cleanup_tempdir"),
        ):
            d.close()

        proc_mock.terminate.assert_called_once()
        proc_mock.kill.assert_not_called()

    def test_close_escalates_to_sigkill(self, tmp_path):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.poll.return_value = None
        proc_mock.stdin = unittest.mock.Mock()
        d = _make_daemon(tmp_path)
        d._proc = proc_mock

        # Both stdin and sigterm waits fail → sigkill.
        wait_results = iter([False, False, True])

        with (
            unittest.mock.patch.object(d, "_wait_for_exit", side_effect=wait_results),
            unittest.mock.patch.object(d, "_cleanup_tempdir"),
        ):
            d.close()

        proc_mock.terminate.assert_called_once()
        proc_mock.kill.assert_called_once()

    def test_close_clears_proc_reference(self, tmp_path):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.poll.return_value = None
        proc_mock.stdin = unittest.mock.Mock()
        d = _make_daemon(tmp_path)
        d._proc = proc_mock

        with (
            unittest.mock.patch.object(d, "_wait_for_exit", return_value=True),
            unittest.mock.patch.object(d, "_cleanup_tempdir"),
        ):
            d.close()

        assert d._proc is None


# ---------------------------------------------------------------------------
# _cleanup_tempdir: state clearing
# ---------------------------------------------------------------------------


class TestCleanupTempdir:
    def test_clears_all_state_fields(self, tmp_path):
        d = _make_daemon(tmp_path)
        d._tempdir = str(tmp_path / "accel-tmp")
        d._uds_path = str(tmp_path / "sock")
        d._log_path = str(tmp_path / "daemon.log")
        d._auth_secret = "super-secret"

        _real_cleanup_tempdir(d)

        assert d._tempdir is None
        assert d._uds_path is None
        assert d._log_path is None
        assert d._auth_secret is None

    def test_removes_tempdir_from_disk(self, tmp_path):
        d = _make_daemon(tmp_path)
        td = tmp_path / "accel-tmp"
        td.mkdir()
        d._tempdir = str(td)

        _real_cleanup_tempdir(d)

        assert not td.exists()

    def test_noop_when_tempdir_is_none(self, tmp_path):
        d = _make_daemon(tmp_path)
        _real_cleanup_tempdir(d)  # should not raise


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------


class TestContextManager:
    def test_enter_calls_start_and_returns_self(self, tmp_path, monkeypatch):
        def fake_popen(argv, **kwargs):
            raise _StopStart()

        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        d = _make_daemon(tmp_path)
        with (
            unittest.mock.patch.object(d, "start") as start_mock,
            unittest.mock.patch.object(d, "close"),
        ):
            result = d.__enter__()
        start_mock.assert_called_once()
        assert result is d

    def test_exit_calls_close(self, tmp_path):
        d = _make_daemon(tmp_path)
        with unittest.mock.patch.object(d, "close") as close_mock:
            d.__exit__(None, None, None)
        close_mock.assert_called_once()


# ---------------------------------------------------------------------------
# _read_log_tail
# ---------------------------------------------------------------------------


class TestReadLogTail:
    def test_reads_tail_of_log(self, tmp_path):
        d = _make_daemon(tmp_path)
        log = tmp_path / "daemon.log"
        log.write_bytes(b"hello world")
        d._log_path = str(log)
        tail = d._read_log_tail()
        assert "hello world" in tail

    def test_truncates_to_max_bytes(self, tmp_path):
        d = _make_daemon(tmp_path)
        log = tmp_path / "daemon.log"
        log.write_bytes(b"x" * 8192)
        d._log_path = str(log)
        tail = d._read_log_tail(max_bytes=100)
        assert len(tail) <= 100

    def test_missing_log_returns_empty(self, tmp_path):
        d = _make_daemon(tmp_path)
        d._log_path = str(tmp_path / "nonexistent.log")
        assert d._read_log_tail() == ""

    def test_no_log_path_returns_empty(self, tmp_path):
        d = _make_daemon(tmp_path)
        d._log_path = None
        assert d._read_log_tail() == ""


# ---------------------------------------------------------------------------
# _wait_for_exit
# ---------------------------------------------------------------------------


class TestWaitForExit:
    def test_returns_true_when_no_proc(self, tmp_path):
        d = _make_daemon(tmp_path)
        assert d._wait_for_exit(1.0) is True

    def test_returns_true_when_proc_exits_in_time(self, tmp_path):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.wait.return_value = 0  # exited
        d = _make_daemon(tmp_path)
        d._proc = proc_mock
        assert d._wait_for_exit(1.0) is True

    def test_returns_false_on_timeout(self, tmp_path):
        import subprocess

        proc_mock = unittest.mock.Mock(spec=subprocess.Popen)
        proc_mock.wait.side_effect = subprocess.TimeoutExpired(cmd="x", timeout=0.1)
        d = _make_daemon(tmp_path)
        d._proc = proc_mock
        assert d._wait_for_exit(0.1) is False


# ---------------------------------------------------------------------------
# read_identity: corrupt JSON
# ---------------------------------------------------------------------------


class TestReadIdentityCorruptJson:
    def test_corrupt_json_raises_runtime_error(self, tmp_path):
        d = _make_daemon(tmp_path)
        dd = tmp_path / "accel-tmp"
        dd.mkdir(exist_ok=True)
        d._tempdir = str(dd)
        identity_path = dd / _IDENTITY_FILENAME
        identity_path.write_text("{not valid json}")
        with pytest.raises(RuntimeError, match="Failed to read"):
            d.read_identity()

    def test_read_identity_unlinks_even_on_error(self, tmp_path):
        d = _make_daemon(tmp_path)
        dd = tmp_path / "accel-tmp2"
        dd.mkdir(exist_ok=True)
        d._tempdir = str(dd)
        identity_path = dd / _IDENTITY_FILENAME
        identity_path.write_text("{bad json}")
        try:
            d.read_identity()
        except RuntimeError:
            pass
        # File should be unlinked regardless of the parse error.
        assert not identity_path.exists()


# ---------------------------------------------------------------------------
# CLI flags passed to Popen
# ---------------------------------------------------------------------------


class TestCliFlags:
    def test_cli_flags_appended_to_argv(self, tmp_path, monkeypatch):
        captured = {}

        def fake_popen(argv, **kwargs):
            captured["argv"] = argv
            raise _StopStart()

        monkeypatch.setattr(_daemon.subprocess, "Popen", fake_popen)
        d = _make_daemon(
            tmp_path,
            cli_flags=[
                "--project",
                "proj",
                "--instance",
                "inst",
                "--app-profile",
                "prof",
            ],
        )
        with pytest.raises(_StopStart):
            d.start()

        argv = captured["argv"]
        assert "--uds-path" in argv
        assert "--project" in argv
        assert argv[argv.index("--project") + 1] == "proj"
        assert "--instance" in argv
        assert argv[argv.index("--instance") + 1] == "inst"
        assert "--app-profile" in argv
        assert argv[argv.index("--app-profile") + 1] == "prof"


# ---------------------------------------------------------------------------
# Startup timeout env variable (_resolve_startup_timeout)
# ---------------------------------------------------------------------------


class TestResolveStartupTimeout:
    """Tests for the BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT env-var override.

    The remote implementation raises ValueError for invalid values rather than
    warning and falling back — invalid env vars are deployment misconfigurations
    and should surface loudly.
    """

    def test_no_env_var_returns_default(self, monkeypatch):
        monkeypatch.delenv(_STARTUP_TIMEOUT_ENV_VAR, raising=False)
        assert _resolve_startup_timeout() == _DEFAULT_STARTUP_TIMEOUT

    def test_empty_string_returns_default(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "")
        assert _resolve_startup_timeout() == _DEFAULT_STARTUP_TIMEOUT

    def test_valid_integer_string_overrides(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "30")
        assert _resolve_startup_timeout() == 30.0

    def test_valid_float_string_overrides(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "0.5")
        assert _resolve_startup_timeout() == 0.5

    def test_non_numeric_string_raises_value_error(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "not-a-number")
        with pytest.raises(ValueError, match="not a valid number of seconds"):
            _resolve_startup_timeout()

    def test_whitespace_only_raises_value_error(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "   ")
        with pytest.raises(ValueError, match="not a valid number of seconds"):
            _resolve_startup_timeout()

    def test_negative_value_raises_value_error(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "-1")
        with pytest.raises(ValueError, match="must be a positive, finite "):
            _resolve_startup_timeout()

    def test_zero_raises_value_error(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "0")
        with pytest.raises(ValueError, match="must be a positive, finite "):
            _resolve_startup_timeout()

    def test_zero_float_raises_value_error(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "0.0")
        with pytest.raises(ValueError, match="must be a positive, finite "):
            _resolve_startup_timeout()

    @pytest.mark.parametrize("raw", ["inf", "Infinity", "+inf", "-inf", "nan", "NaN"])
    def test_non_finite_value_raises_value_error(self, monkeypatch, raw):
        # float() happily parses these. "inf" clears the `> 0` check and would
        # hang startup forever; "nan" clears it too (NaN comparisons are always
        # False) and poisons the readiness loop's deadline arithmetic.
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, raw)
        with pytest.raises(ValueError, match="must be a positive, finite "):
            _resolve_startup_timeout()

    def test_error_message_includes_env_var_name_and_value(self, monkeypatch):
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "bad")
        with pytest.raises(ValueError) as exc_info:
            _resolve_startup_timeout()
        msg = str(exc_info.value)
        assert _STARTUP_TIMEOUT_ENV_VAR in msg
        assert "bad" in msg

    def test_daemon_constructor_picks_up_env_var(self, tmp_path, monkeypatch):
        """End-to-end: env var flows into AcceleratorDaemon._startup_timeout."""
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "42")
        d = _make_daemon(tmp_path)
        assert d._startup_timeout == 42.0

    def test_daemon_constructor_invalid_env_var_raises(self, tmp_path, monkeypatch):
        """Invalid env var causes constructor to raise ValueError."""
        monkeypatch.setenv(_STARTUP_TIMEOUT_ENV_VAR, "xyz")
        with pytest.raises(ValueError, match="not a valid number of seconds"):
            _make_daemon(tmp_path)


@pytest.mark.skipif(
    not hasattr(_daemon.socket, "AF_UNIX"),
    reason="Unix domain sockets (AF_UNIX) are not supported on this platform",
)
class TestSweepStaleTempdirs:
    """_sweep_stale_tempdirs reaps leftover daemon tempdirs, keyed on the
    daemon.log marker, and deletes only on proof that the spawner is gone."""

    @pytest.fixture
    def tmp_root(self, monkeypatch):
        # Point the sweep's tempdir root at an isolated directory of our own.
        # dir= is explicit because mkdtemp would otherwise resolve its default
        # through the gettempdir() the autouse fixture has already patched.
        root = pathlib.Path(_real_mkdtemp(prefix="bt-sweep-", dir=_real_gettempdir()))
        monkeypatch.setattr(_daemon.tempfile, "gettempdir", lambda: str(root))
        yield root
        shutil.rmtree(root, ignore_errors=True)

    @staticmethod
    def _dead_pid():
        """A PID that is guaranteed not to resolve to a running process."""
        proc = subprocess.Popen([sys.executable, "-c", ""])
        proc.wait()
        return proc.pid

    @staticmethod
    def _make_leftover(
        root,
        name,
        *,
        with_log=True,
        age_seconds=0.0,
        deadline_offset=None,
        pid=None,
        namespace=_UNSET,
    ):
        """Create a fake leftover daemon tempdir.

        deadline_offset: seconds relative to now for the startup deadline file.
        Negative = deadline already passed (stale); positive = still in future
        (mid-startup). None = omit the file (tests the fallback heuristic).
        pid: if given, write a daemon.pid naming this PID. Pass a dead PID to
        simulate a crashed spawner, or os.getpid() for "alive".
        namespace: what to stamp next to the PID. Defaults to this process's
        own, so the sweep accepts it; pass something else to simulate a
        tempdir written in a different PID namespace, or None to omit the
        stamp entirely (a tempdir predating it).
        """
        d = root / name
        d.mkdir()
        if with_log:
            log = d / _daemon._LOG_FILENAME
            log.write_bytes(b"hi")
            if age_seconds:
                past = time.time() - age_seconds
                os.utime(log, (past, past))
        if deadline_offset is not None:
            dl = d / _daemon._STARTUP_DEADLINE_FILENAME
            dl.write_text(repr(time.time() + deadline_offset))
        if pid is not None:
            if namespace is _UNSET:
                namespace = _daemon._pid_namespace()
            stamp = str(pid) if namespace is None else f"{pid} {namespace}"
            (d / _daemon._PID_FILENAME).write_text(stamp)
        return d

    # -- the one path that deletes -------------------------------------------

    def test_removes_stale_dir(self, tmp_root):
        # Expired deadline, old log, and the kernel says the spawner's PID
        # does not resolve to any process. That ESRCH is the only thing that
        # may lead to a delete.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-dead",
            age_seconds=120,
            deadline_offset=-70,
            pid=self._dead_pid(),
        )
        _daemon._sweep_stale_tempdirs()
        assert not d.exists()

    def test_removes_stale_dir_without_deadline_file(self, tmp_root):
        # A tempdir predating the deadline file still gets judged, via the
        # log-mtime fallback -- but only because the pid check proves death.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-nodl",
            age_seconds=120,
            deadline_offset=None,
            pid=self._dead_pid(),
        )
        _daemon._sweep_stale_tempdirs()
        assert not d.exists()

    # -- everything else keeps ------------------------------------------------

    def test_keeps_dir_with_live_spawner(self, tmp_root):
        # Well past every age gate, but the spawning process is alive, so its
        # daemon is alive and the directory is not a leftover.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-live",
            age_seconds=86400,
            deadline_offset=-86400,
            pid=os.getpid(),
        )
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_live_dir_from_an_older_client(self, tmp_root):
        # A tempdir written by a previously released client has a daemon.log
        # and no metadata at all. There is no owner to probe, so there is no
        # proof of death, so it must survive -- its daemon may well be
        # serving. Mixed versions share one /tmp whenever two virtualenvs (or
        # a rolling restart) run side by side.
        d = self._make_leftover(
            tmp_root, "bt-accel-legacy", age_seconds=86400, deadline_offset=None
        )
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_dir_from_another_pid_namespace(self, tmp_root):
        # Containers sharing a /tmp volume have separate PID numbering, so a
        # PID written over there means something else (or nothing) here.
        # Signalling it would give a confident, repeatable wrong answer, so
        # the sweep declines to judge. The dead PID makes the point: without
        # the namespace check this directory would be deleted.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-otherns",
            age_seconds=86400,
            deadline_offset=-86400,
            pid=self._dead_pid(),
            namespace="4:4026531999",
        )
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_dir_with_unstamped_pid_file(self, tmp_root):
        # A pid file written before the namespace was recorded cannot be
        # checked either, for the same reason.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-nostamp",
            age_seconds=86400,
            deadline_offset=-86400,
            pid=self._dead_pid(),
            namespace=None,
        )
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    @pytest.mark.parametrize("contents", ["", "   ", "not-a-pid", "garbage stamp"])
    def test_keeps_dir_with_unusable_pid_file(self, tmp_root, contents):
        # A crash mid-write can leave the pid file empty or truncated. That is
        # a deliberate, permanent leak: unreadable is not proof of death.
        d = self._make_leftover(
            tmp_root, "bt-accel-badpid", age_seconds=86400, deadline_offset=-86400
        )
        (d / _daemon._PID_FILENAME).write_text(contents)
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_dir_when_pid_file_is_unreadable(self, tmp_root, monkeypatch):
        # An OSError other than "missing" tells us nothing about the owner.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-unreadable",
            age_seconds=86400,
            deadline_offset=-86400,
            pid=self._dead_pid(),
        )
        real_open = open

        def bad_open(path, *args, **kwargs):
            if os.path.basename(str(path)) == _daemon._PID_FILENAME:
                raise PermissionError("EACCES")
            return real_open(path, *args, **kwargs)

        monkeypatch.setattr(_daemon, "open", bad_open, raising=False)
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_dir_when_pid_is_not_ours_to_signal(self, tmp_root, monkeypatch):
        # EPERM from os.kill means the PID exists under another user: alive.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-eperm",
            age_seconds=86400,
            deadline_offset=-86400,
            pid=os.getpid(),
        )

        def eperm(pid, sig):
            raise PermissionError("EPERM")

        monkeypatch.setattr(_daemon.os, "kill", eperm)
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_dir_whose_pid_was_recycled(self, tmp_root):
        # A recycled PID now belonging to some unrelated long-lived process
        # reads as alive, so the directory is pinned forever. That leak is the
        # accepted cost of never deleting a live daemon; detecting reuse means
        # a heuristic, and a wrong "recycled" verdict deletes a live daemon.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-recycled",
            age_seconds=86400,
            deadline_offset=-86400,
            pid=os.getpid(),
        )
        pid_file = d / _daemon._PID_FILENAME
        old = time.time() - 86400
        os.utime(pid_file, (old, old))
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_young_dir(self, tmp_root):
        # No deadline file: fallback uses log mtime + buffer; log is fresh.
        d = self._make_leftover(
            tmp_root, "bt-accel-young", age_seconds=0, pid=self._dead_pid()
        )
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_keeps_dir_with_future_deadline(self, tmp_root):
        # Log is old (a long-timeout override) but the daemon is still inside
        # its own startup budget, when the pid file may not be written yet.
        d = self._make_leftover(
            tmp_root, "bt-accel-slow", age_seconds=120, deadline_offset=+200
        )
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_ignores_dir_without_log_marker(self, tmp_root):
        # Prefix matches but there's no daemon.log, so it isn't one of ours.
        d = tmp_root / "bt-accel-foreign"
        d.mkdir()
        (d / "something-else").write_bytes(b"x")
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_budget_exhausted_leaves_dirs_for_next_sweep(self, tmp_root, monkeypatch):
        # Same inputs as test_removes_stale_dir, but the time budget is already
        # spent: the walk bails out rather than running long on a huge /tmp.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-dead",
            age_seconds=120,
            deadline_offset=-70,
            pid=self._dead_pid(),
        )
        monkeypatch.setattr(_daemon, "_SWEEP_BUDGET_SECONDS", -1.0)
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    def test_glob_failure_is_swallowed(self, tmp_root, monkeypatch):
        # Enumeration can fail outright (a vanished or unreadable /tmp). The
        # sweep is opportunistic, so that must not propagate to start().
        def boom(*args, **kwargs):
            raise OSError("EIO")

        monkeypatch.setattr(_daemon.glob, "iglob", boom)
        _daemon._sweep_stale_tempdirs()

    def test_no_af_unix_is_a_noop(self, tmp_root, monkeypatch):
        # Without AF_UNIX the accelerator cannot have run here at all.
        d = self._make_leftover(
            tmp_root,
            "bt-accel-dead",
            age_seconds=120,
            deadline_offset=-70,
            pid=self._dead_pid(),
        )
        monkeypatch.delattr(_daemon.socket, "AF_UNIX")
        _daemon._sweep_stale_tempdirs()
        assert d.exists()

    # -- wiring into start() --------------------------------------------------

    def test_start_invokes_sweep(self, tmp_path, monkeypatch):
        done = threading.Event()

        def _fake_sweep():
            done.set()

        monkeypatch.setattr(_daemon, "_sweep_stale_tempdirs", _fake_sweep)

        def boom(*args, **kwargs):
            raise OSError("refusing to spawn in test")

        monkeypatch.setattr(_daemon.subprocess, "Popen", boom)
        daemon = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError):
            daemon.start()
        assert done.wait(timeout=2.0), "sweep thread did not run within 2 s"

    def test_start_survives_sweep_thread_failure(self, tmp_path, monkeypatch):
        # At the process thread ceiling, Thread.start() raises. Tidying /tmp
        # is the least important thing start() does; it must not be the thing
        # that costs the caller a working client.
        class NoThreads:
            def __init__(self, *args, **kwargs):
                pass

            def start(self):
                raise RuntimeError("can't start new thread")

        monkeypatch.setattr(_daemon.threading, "Thread", NoThreads)
        popen_called = []

        def boom(*args, **kwargs):
            popen_called.append(True)
            raise OSError("refusing to spawn in test")

        monkeypatch.setattr(_daemon.subprocess, "Popen", boom)
        daemon = _make_daemon(tmp_path)
        # Reaches Popen and fails there, rather than at Thread.start().
        with pytest.raises(RuntimeError, match="Failed to spawn"):
            daemon.start()
        assert popen_called

    def test_start_stamps_pid_and_namespace(self, tmp_path, monkeypatch):
        # The file start() writes must be the one the sweep knows how to read.
        def boom(*args, **kwargs):
            raise OSError("refusing to spawn in test")

        monkeypatch.setattr(_daemon.subprocess, "Popen", boom)
        monkeypatch.setattr(AcceleratorDaemon, "_cleanup_tempdir", lambda self: None)
        daemon = _make_daemon(tmp_path)
        with pytest.raises(RuntimeError, match="Failed to spawn"):
            daemon.start()
        written = (pathlib.Path(daemon._tempdir) / _daemon._PID_FILENAME).read_text()
        assert written.split() == [str(os.getpid()), _daemon._pid_namespace()]


class TestPidNamespace:
    """_pid_namespace identifies the namespace a process's PIDs belong to."""

    @pytest.mark.skipif(
        not os.path.exists("/proc/self/ns/pid"), reason="requires Linux namespaces"
    )
    def test_reports_own_namespace(self):
        ns = _daemon._pid_namespace()
        assert ns != _daemon._NO_PID_NAMESPACE
        # Stable for the life of the process, and shared with our children.
        assert ns == _daemon._pid_namespace()
        child = subprocess.run(
            [
                sys.executable,
                "-c",
                "import os;st=os.stat('/proc/self/ns/pid');"
                "print(f'{st.st_dev}:{st.st_ino}')",
            ],
            capture_output=True,
            text=True,
        )
        assert child.stdout.strip() == ns

    def test_falls_back_when_proc_is_absent(self, monkeypatch):
        # macOS and friends have no /proc, and also no PID namespaces, so the
        # sentinel compares equal to itself and the check is a no-op there.
        def no_proc(path, *args, **kwargs):
            raise FileNotFoundError(path)

        monkeypatch.setattr(_daemon.os, "stat", no_proc)
        assert _daemon._pid_namespace() == _daemon._NO_PID_NAMESPACE


@pytest.mark.skipif(not hasattr(_daemon.socket, "AF_UNIX"), reason="requires AF_UNIX")
class TestSocketIsLive:
    """_socket_is_live backs the _wait_until_ready poll: is the daemon up?"""

    def test_true_while_listening(self, tmp_path):
        path = str(tmp_path / "sock")
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.bind(path)
            sock.listen(1)
            assert _daemon._socket_is_live(path) is True

    def test_false_when_path_is_absent(self, tmp_path):
        assert _daemon._socket_is_live(str(tmp_path / "nope")) is False

    def test_false_for_socket_file_whose_owner_exited(self, tmp_path):
        # The socket file outlives the process that bound it; nothing is
        # accepting, so the daemon is not up yet (or any more).
        path = str(tmp_path / "sock")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(path)
        sock.listen(1)
        sock.close()
        assert os.path.exists(path)
        assert _daemon._socket_is_live(path) is False


class TestWriteMetadataFile:
    """_write_metadata_file swaps contents in atomically."""

    def test_writes_contents(self, tmp_path):
        target = tmp_path / "daemon.pid"
        _daemon._write_metadata_file(str(target), "1234")
        assert target.read_text() == "1234"
        # The staging file must not be left behind on success.
        assert not (tmp_path / "daemon.pid.tmp").exists()

    def test_target_is_absent_until_contents_are_complete(self, tmp_path):
        # A reader racing the write sees no file rather than a truncated one:
        # everything lands in the ".tmp" sibling and is complete and closed by
        # the time the rename publishes it under the real name.
        target = tmp_path / "daemon.pid"
        observed = {}
        real_replace = _daemon.os.replace

        def spy_replace(src, dst):
            observed["target_existed"] = target.exists()
            observed["staged"] = pathlib.Path(src).read_text()
            return real_replace(src, dst)

        with unittest.mock.patch.object(_daemon.os, "replace", spy_replace):
            _daemon._write_metadata_file(str(target), "1234")
        assert observed == {"target_existed": False, "staged": "1234"}
        assert target.read_text() == "1234"

    def test_overwrites_existing_file(self, tmp_path):
        target = tmp_path / "daemon.pid"
        target.write_text("stale-and-longer")
        _daemon._write_metadata_file(str(target), "7")
        assert target.read_text() == "7"
