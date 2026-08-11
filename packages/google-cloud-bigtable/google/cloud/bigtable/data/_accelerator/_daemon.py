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
"""Subprocess lifecycle wrapper for the Go accelerator daemon binary.

The daemon binary embeds an in-process Go Bigtable client and exposes the
``google.bigtable.v2.Bigtable`` service over a Unix domain socket. This module
owns spawning the binary, waiting for the UDS to become connectable, and
tearing the process down. It does NOT speak gRPC; that's the
``_AcceleratorClient`` companion's job.
"""

from __future__ import annotations

import os
import shutil
import signal
import socket
import subprocess
import tempfile
import time
import typing
from typing import Sequence

# Environment variable that overrides the bundled binary location. Primarily
# for development against a locally-built daemon, and for tests pointing at a
# fake binary.
_BIN_ENV_VAR = "BIGTABLE_ACCELERATOR_BIN"

# Wheels ship the binary at this path relative to the `_accelerator/` package.
_DEFAULT_BIN_RELATIVE_PATH = "bin/accelerator"

# How long to wait for the daemon to start listening on its UDS before giving
# up at startup.
_DEFAULT_STARTUP_TIMEOUT = 10.0

# Sequence: close stdin, wait this long; SIGTERM, wait again; SIGKILL.
_STDIN_GRACE_SECONDS = 2.0
_SIGTERM_GRACE_SECONDS = 2.0


def _default_binary_path() -> str | None:
    bundled = os.path.join(os.path.dirname(__file__), _DEFAULT_BIN_RELATIVE_PATH)
    return bundled if os.path.isfile(bundled) else None


def _resolve_binary_path() -> str:
    override = os.environ.get(_BIN_ENV_VAR)
    if override:
        if not os.path.isfile(override):
            raise FileNotFoundError(
                f"{_BIN_ENV_VAR}={override!r} does not point at a regular file"
            )
        return override
    bundled = _default_binary_path()
    if bundled is None:
        raise FileNotFoundError(
            "No accelerator binary found. Set the "
            f"{_BIN_ENV_VAR} env var to a daemon binary path, or install a "
            "wheel that bundles the binary."
        )
    return bundled


class AcceleratorDaemon:
    """Manages the Go accelerator daemon subprocess.

    The Python class is named for the thing it runs (the daemon hosts the
    actual gRPC server). Lifecycle:

    1. ``__init__`` validates and resolves the binary, picks the UDS path.
    2. ``start()`` spawns the subprocess and blocks until the UDS is
       connectable, or raises if the process dies first.
    3. ``close()`` closes stdin (the daemon shuts down on EOF), then escalates
       to SIGTERM and SIGKILL if it doesn't exit promptly. Cleans up the temp
       directory holding the socket.

    This class is intentionally sync-only: ``subprocess.Popen`` works
    identically for async and sync callers, and spawn/close happen once per
    client lifetime — there's nothing to await.
    """

    def __init__(
        self,
        cli_flags: Sequence[str] = (),
        *,
        binary_path: str | None = None,
        startup_timeout: float = _DEFAULT_STARTUP_TIMEOUT,
    ):
        self._binary_path = binary_path or _resolve_binary_path()
        self._cli_flags = list(cli_flags)
        self._startup_timeout = startup_timeout
        self._tempdir: str | None = None
        self._uds_path: str | None = None
        self._log_path: str | None = None
        self._log_file: "typing.IO[bytes] | None" = None
        self._proc: subprocess.Popen[bytes] | None = None

    @property
    def uds_path(self) -> str:
        if self._uds_path is None:
            raise RuntimeError("AcceleratorDaemon has not been started")
        return self._uds_path

    @property
    def log_path(self) -> str:
        if self._log_path is None:
            raise RuntimeError("AcceleratorDaemon has not been started")
        return self._log_path

    @property
    def pid(self) -> int:
        if self._proc is None:
            raise RuntimeError("AcceleratorDaemon has not been started")
        return self._proc.pid

    @property
    def is_running(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def start(self) -> None:
        """Spawn the daemon and wait for the UDS to become connectable."""
        if self._proc is not None:
            raise RuntimeError("AcceleratorDaemon.start() called twice")
        self._tempdir = tempfile.mkdtemp(prefix="bt-accel-")
        self._uds_path = os.path.join(self._tempdir, "sock")
        # Redirect the daemon's stdout/stderr to a log file rather than
        # subprocess.PIPE. Nothing drains those pipes for the daemon's
        # lifetime, so a PIPE's fixed OS buffer would eventually fill and
        # block (deadlock) the daemon on its next write. A regular file has no
        # such limit and stays on disk for post-mortem debugging. stdin stays a
        # PIPE — closing it is how close() signals the daemon to shut down.
        self._log_path = os.path.join(
            tempfile.gettempdir(),
            f"accelerator-daemon-{os.path.basename(self._tempdir)}.log",
        )
        self._log_file = open(self._log_path, "wb")
        argv = [self._binary_path, "--uds-path", self._uds_path, *self._cli_flags]
        try:
            self._proc = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE,
                stdout=self._log_file,
                stderr=subprocess.STDOUT,
                close_fds=True,
            )
        except OSError as exc:
            self._close_log_file()
            self._cleanup_tempdir()
            raise RuntimeError(
                f"Failed to spawn accelerator daemon at {self._binary_path}: {exc}"
            ) from exc
        # The child inherited its own dup of the log fd; the parent no longer
        # needs its copy. Startup failures read the tail back from the path.
        self._close_log_file()
        try:
            self._wait_until_ready()
        except BaseException:
            self._force_kill()
            self._cleanup_tempdir()
            raise

    def close(self) -> None:
        """Tear down the daemon and clean up the UDS tempdir."""
        proc = self._proc
        if proc is None:
            return
        try:
            if proc.poll() is None:
                # Step 1: close stdin → daemon's stdin-EOF watchdog triggers
                # graceful shutdown.
                if proc.stdin is not None:
                    try:
                        proc.stdin.close()
                    except OSError:
                        pass
                if not self._wait_for_exit(_STDIN_GRACE_SECONDS):
                    # Step 2: SIGTERM.
                    proc.terminate()
                    if not self._wait_for_exit(_SIGTERM_GRACE_SECONDS):
                        # Step 3: SIGKILL.
                        proc.kill()
                        proc.wait()
        finally:
            self._proc = None
            self._close_log_file()
            self._cleanup_tempdir()

    def _wait_until_ready(self) -> None:
        assert self._proc is not None and self._uds_path is not None
        deadline = time.monotonic() + self._startup_timeout
        while time.monotonic() < deadline:
            exit_code = self._proc.poll()
            if exit_code is not None:
                log_tail = self._read_log_tail()
                raise RuntimeError(
                    "Accelerator daemon exited during startup "
                    f"(exit code {exit_code}). log: {log_tail!r}"
                )
            if os.path.exists(self._uds_path):
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe:
                    probe.settimeout(0.25)
                    try:
                        probe.connect(self._uds_path)
                        return
                    except (ConnectionRefusedError, FileNotFoundError, OSError):
                        pass
            time.sleep(0.05)
        log_tail = self._read_log_tail()
        raise RuntimeError(
            "Accelerator daemon did not become ready within "
            f"{self._startup_timeout}s. log: {log_tail!r}"
        )

    def _read_log_tail(self, max_bytes: int = 4096) -> str:
        """Best-effort read of the tail of the daemon's log file.

        Used only to enrich startup-failure error messages with whatever the
        daemon wrote to stdout/stderr (both are redirected to the log file).
        The log is a regular file, so this is a plain bounded read with no risk
        of blocking on an alive-but-silent daemon. Returns "" if the log is
        unavailable.
        """
        if self._log_path is None:
            return ""
        try:
            with open(self._log_path, "rb") as fh:
                try:
                    fh.seek(-max_bytes, os.SEEK_END)
                except OSError:
                    fh.seek(0)
                data = fh.read()
        except OSError:
            return ""
        return data.decode("utf-8", errors="replace")

    def _close_log_file(self) -> None:
        if self._log_file is not None:
            try:
                self._log_file.close()
            except OSError:
                pass
            self._log_file = None

    def _wait_for_exit(self, timeout: float) -> bool:
        assert self._proc is not None
        try:
            self._proc.wait(timeout=timeout)
            return True
        except subprocess.TimeoutExpired:
            return False

    def _force_kill(self) -> None:
        if self._proc is None or self._proc.poll() is not None:
            return
        try:
            self._proc.send_signal(signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass
        try:
            self._proc.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            pass

    def _cleanup_tempdir(self) -> None:
        if self._tempdir is not None and os.path.isdir(self._tempdir):
            shutil.rmtree(self._tempdir, ignore_errors=True)
        self._tempdir = None
        self._uds_path = None
