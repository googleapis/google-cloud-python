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

import glob
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any, Mapping, Sequence

# Windows differs from every other supported platform in two ways that matter
# here, so it gets a named constant rather than scattered ``sys.platform``
# checks: the daemon binary carries a ``.exe`` suffix, and CPython's socket
# module exposes no ``AF_UNIX`` even though the OS and gRPC's C-core both speak
# it (see ``_socket_is_live``).
_IS_WINDOWS = sys.platform == "win32"

# Environment variable that overrides the daemon startup readiness timeout, in
# seconds (float). Lets a deployment tune the cold-start budget without a code
# change or rebuild — e.g. raise it on a very constrained/gVisor host, or (when
# a Cloud Run startup probe already gates traffic on daemon readiness) it can be
# left at the default since the platform absorbs the wait.
_STARTUP_TIMEOUT_ENV_VAR = "BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT"

# Wheels ship the binary at this path relative to the `_accelerator/` package.
# The Windows wheels (win_amd64, win32) stage it under the ``.exe`` name Go
# gives it, so the suffix is appended there.
_DEFAULT_BIN_RELATIVE_PATH = "bin/accelerator"
_WINDOWS_BIN_SUFFIX = ".exe"

# The daemon writes the principal it resolved to this file in its tempdir
# (alongside the socket) before binding, so the client can verify it matches
# its own locally-resolved identity before routing any RPC.
_IDENTITY_FILENAME = "identity.json"

# Prefix for the per-daemon tempdir (created by ``tempfile.mkdtemp``) that holds
# the socket, identity, and log. Used both when creating our own and to scope
# the startup sweep of leftovers.
_TEMPDIR_PREFIX = "bt-accel-"

# Names of the files a live daemon keeps inside its tempdir.
_SOCKET_FILENAME = "sock"
_LOG_FILENAME = "daemon.log"
# Absolute POSIX timestamp written by start() so the sweep knows when startup
# for *this specific* daemon was allowed to finish. Each process may have a
# different BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT, so the sweep cannot rely on
# its own env value when judging another process's tempdir.
_STARTUP_DEADLINE_FILENAME = "startup_deadline"
# PID of the Python process that spawned the daemon, written at start().  The
# sweep sends signal 0 to this PID to check liveness: if the spawner is alive
# the daemon is alive; if the spawner is dead (ESRCH) the daemon's stdin is
# closed and it will exit (or has already exited).
_PID_FILENAME = "daemon.pid"

# How long to wait for the daemon to start listening on its UDS before giving
# up at startup. Cold, constrained environments (e.g. Cloud Run's gVisor
# sandbox) spend ~10s in Go runtime init + ADC token fetch from the metadata
# server before the daemon binds, so a 10s budget misses and falls back to the
# native client; 20s covers that cold start with margin. Override per-deployment
# via the ``BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT`` env var (see
# ``_resolve_startup_timeout``).
_DEFAULT_STARTUP_TIMEOUT = 20.0

# Sequence: close stdin, wait this long; SIGTERM, wait again; SIGKILL.
_STDIN_GRACE_SECONDS = 2.0
_SIGTERM_GRACE_SECONDS = 2.0
_SIGKILL_GRACE_SECONDS = 2.0

# A freshly-created tempdir may not have bound its socket yet. Never sweep one
# younger than this, so a daemon another client is mid-way through starting is
# never mistaken for a stale leftover and reaped out from under it.
_STALE_SWEEP_MIN_AGE_SECONDS = 60.0


def _resolve_binary_path() -> str:
    """Return the path of the bundled daemon binary, raising if it is absent."""
    relative = _DEFAULT_BIN_RELATIVE_PATH + (_WINDOWS_BIN_SUFFIX if _IS_WINDOWS else "")
    bundled = os.path.join(os.path.dirname(__file__), relative)
    if not os.path.isfile(bundled):
        raise FileNotFoundError(
            "Accelerator binary not found. Install a wheel that bundles the binary."
        )
    return bundled


def _resolve_startup_timeout() -> float:
    """Resolve the daemon startup timeout in seconds.

    Precedence: an explicit constructor argument wins; otherwise the
    ``BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT`` env var; otherwise the default.
    A malformed or non-positive env value is a deployment misconfiguration, so
    it is raised loudly rather than silently ignored.
    """
    raw = os.environ.get(_STARTUP_TIMEOUT_ENV_VAR)
    if raw is None or raw == "":
        return _DEFAULT_STARTUP_TIMEOUT
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(
            f"{_STARTUP_TIMEOUT_ENV_VAR}={raw!r} is not a valid number of seconds"
        ) from exc
    if value <= 0:
        raise ValueError(
            f"{_STARTUP_TIMEOUT_ENV_VAR}={raw!r} must be a positive number of seconds"
        )
    return value


def _socket_is_live(uds_path: str) -> bool:
    """Return True if something is currently accepting connections on the UDS."""
    if not os.path.exists(uds_path):
        return False
    if not hasattr(socket, "AF_UNIX"):
        # Windows. The OS (10 1803+ / Server 2019+) and gRPC's C-core both
        # support AF_UNIX, which is why the accelerator runs here at all, but
        # CPython's socket module still does not expose the family, so we
        # cannot open a probe connection from Python. The gate is
        # ``HAVE_SYS_UN_H``: ``PC/pyconfig.h`` leaves it commented out and
        # ``Modules/socketmodule.h`` responds with ``#undef AF_UNIX``, so the
        # attribute is absent on every current CPython for Windows. Testing
        # the attribute rather than the platform keeps this correct for any
        # other build that lacks the family, and is what lets the tests
        # exercise this branch from a POSIX run.
        #
        # Fall back to the bind artifact: the daemon's
        # ``net.Listen("unix", ...)`` creates this file and puts the socket in
        # the listen backlog inside one call, so the path existing means the
        # listener is up.
        return True
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.25)
        try:
            probe.connect(uds_path)
            return True
        except OSError:
            return False


def _sweep_stale_tempdirs() -> None:
    """Best-effort reaping of leftover daemon tempdirs at startup.

    A clean ``close()`` removes its own tempdir, but a crash or ``SIGKILL``
    leaves the socket and log behind. We reap those on the next start.

    Rather than treating any ``bt-accel-*`` directory as ours, we key off the
    ``daemon.log`` marker file we write inside each one: a directory is a
    candidate only if it actually contains that log. This avoids deleting an
    unrelated directory that merely shares the tempdir prefix. A candidate is
    removed only when the spawning Python process (tracked via ``daemon.pid``)
    is no longer alive *and* the tempdir is old enough that a daemon still
    mid-startup would already have bound or died. ``os.kill(pid, 0)`` is
    instant and kernel-guaranteed: the lock is implicitly released the moment
    the process exits for any reason, including SIGKILL.

    All failures are swallowed — sweeping is opportunistic and must never break
    startup.

    Skipped entirely on Windows: see the guard below.
    """
    if _IS_WINDOWS:
        # The liveness check below is ``os.kill(pid, 0)``, which is a probe
        # only on POSIX. On Windows os.kill routes every signal that is not a
        # console control event to TerminateProcess, so that same call would
        # *kill* the spawning Python process it is supposed to be asking
        # about — someone else's live application. Porting it needs an
        # OpenProcess/WaitForSingleObject check instead, which is left for a
        # follow-up; until then the safe failure is to leave the tempdirs
        # alone. They are four small files under the per-user %TEMP%.
        return
    root = tempfile.gettempdir()
    try:
        logs = glob.glob(os.path.join(root, _TEMPDIR_PREFIX + "*", _LOG_FILENAME))
    except OSError:
        return
    now = time.time()
    for log_path in logs:
        path = os.path.dirname(log_path)
        try:
            # Each tempdir records its own startup deadline so this sweep is
            # correct even when the sweeping process has a different
            # BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT than the process that
            # started the daemon being evaluated.
            deadline_path = os.path.join(path, _STARTUP_DEADLINE_FILENAME)
            try:
                with open(deadline_path) as _f:
                    deadline = float(_f.read())
            except (OSError, ValueError):
                # Older daemon without a deadline file: fall back to a simple
                # age heuristic relative to the log's mtime.
                deadline = os.path.getmtime(log_path) + _STALE_SWEEP_MIN_AGE_SECONDS
            if now < deadline + _STALE_SWEEP_MIN_AGE_SECONDS:
                continue
            pid_path = os.path.join(path, _PID_FILENAME)
            try:
                with open(pid_path) as _f:
                    pid = int(_f.read().strip())
                os.kill(pid, 0)
                continue  # spawning process alive → daemon alive → skip
            except ProcessLookupError:
                pass  # ESRCH: spawner is dead → stdin closed → daemon exiting
            except (OSError, ValueError):
                # No PID file (tempdir predates this change) or EPERM (process
                # exists but unreadable) → assume alive and skip.
                continue
        except OSError:
            continue
        shutil.rmtree(path, ignore_errors=True)


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
        extra_env: Mapping[str, str] | None = None,
    ):
        """Resolve the binary and pick the UDS path (does not spawn anything).

        Args:
            cli_flags: extra arguments appended after ``--uds-path`` when
                spawning the daemon (e.g. ``--project``/``--instance``).
            startup_timeout: seconds ``start()`` waits for the daemon's UDS to
                become connectable before raising.

        Raises:
            FileNotFoundError: the bundled binary is not present in this wheel.
        """
        self._binary_path = (
            binary_path if binary_path is not None else _resolve_binary_path()
        )
        self._cli_flags = list(cli_flags)
        # ``None`` (the default) defers to the env var / module default; an
        # explicit float overrides both. Resolved here, not as a signature
        # default, so the env var is read at instantiation time.
        self._startup_timeout = _resolve_startup_timeout()
        # Extra environment for the subprocess, merged over the inherited env.
        # Used to forward GOOGLE_APPLICATION_CREDENTIALS (path only) so the
        # daemon's ADC resolves the caller's credentials_file.
        self._extra_env = dict(extra_env) if extra_env else {}
        self._tempdir: str | None = None
        self._uds_path: str | None = None
        self._log_path: str | None = None
        self._proc: subprocess.Popen[bytes] | None = None
        self._auth_secret: str | None = None

    def __enter__(self) -> "AcceleratorDaemon":
        """Start the daemon on ``with`` entry and return it."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Tear the daemon down on ``with`` exit."""
        self.close()

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

    @property
    def auth_secret(self) -> str:
        if self._auth_secret is None:
            raise RuntimeError("AcceleratorDaemon has not been started with a secret")
        return self._auth_secret

    def start(self) -> None:
        """Spawn the daemon and wait for the UDS to become connectable.

        Raises:
            RuntimeError: called twice, the daemon failed to spawn, exited
                during startup, or did not become ready within
                ``startup_timeout``. On any of these the child is killed and the
                tempdir removed before the error propagates.
        """
        if self._proc is not None:
            raise RuntimeError("AcceleratorDaemon.start() called twice")

        # The daemon only listens on AF_UNIX, so a platform without it cannot
        # run the accelerator at all. Windows is the one case where a missing
        # ``socket.AF_UNIX`` says nothing about the platform — the OS and
        # gRPC's C-core both support the family, only CPython's socket module
        # does not — so it is excluded from the check.
        if not hasattr(socket, "AF_UNIX") and not _IS_WINDOWS:
            raise OSError(
                "Unix domain sockets (AF_UNIX) are not supported on this platform."
            )

        # Reap tempdirs leaked by daemons from prior runs that crashed or were
        # killed before close() could clean up after them. Fire-and-forget on a
        # daemon thread so it never blocks startup (sweep probes dead sockets
        # with a 0.25 s timeout each).
        threading.Thread(target=_sweep_stale_tempdirs, daemon=True).start()
        # mkdtemp is what confines the socket to this user: 0700 on POSIX, and
        # on Windows an inherited ACL from the per-user %TEMP% tree. The latter
        # is the only access control the socket gets there — Windows has no
        # umask and chmod only toggles the read-only bit — so the daemon
        # deliberately relies on the directory we pick here.
        self._tempdir = tempfile.mkdtemp(prefix=_TEMPDIR_PREFIX)
        self._uds_path = os.path.join(self._tempdir, _SOCKET_FILENAME)
        # Write the absolute time by which startup must complete. The sweep
        # reads this per-directory so it uses the right deadline regardless of
        # what BIGTABLE_ACCELERATOR_STARTUP_TIMEOUT the sweeping process has.
        with open(os.path.join(self._tempdir, _STARTUP_DEADLINE_FILENAME), "w") as _f:
            _f.write(repr(time.time() + self._startup_timeout))
        with open(os.path.join(self._tempdir, _PID_FILENAME), "w") as _f:
            _f.write(str(os.getpid()))

        # Redirect the daemon's stdout/stderr to a log file rather than
        # subprocess.PIPE. Nothing drains those pipes for the daemon's
        # lifetime, so a PIPE's fixed OS buffer would eventually fill and
        # block (deadlock) the daemon on its next write. A regular file has no
        # such limit. The log lives alongside the socket in the daemon's
        # tempdir so it's cleaned up with everything else in close(). stdin
        # stays a PIPE — closing it is how close() signals the daemon to shut
        # down.
        self._log_path = os.path.join(self._tempdir, _LOG_FILENAME)
        # The log file handle only needs to live long enough for Popen to dup
        # it into the child, so it stays local to start() rather than being an
        # attribute. Startup failures read the tail back from the path.
        argv = [self._binary_path, "--uds-path", self._uds_path, *self._cli_flags]
        log_file = None
        env = None
        if self._extra_env:
            env = {**os.environ, **self._extra_env}
        try:
            log_file = open(self._log_path, "wb")
            self._proc = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                close_fds=True,
                env=env,
            )
        except OSError as exc:
            self._cleanup_tempdir()
            raise RuntimeError(
                f"Failed to spawn accelerator daemon at {self._binary_path}: {exc}"
            ) from exc
        finally:
            # Whether or not the spawn succeeded, the parent no longer needs its
            # copy of the log fd: on success the child holds its own dup, and on
            # failure there is nothing to keep open.
            if log_file is not None:
                try:
                    log_file.close()
                except OSError:
                    pass

        # Mint a 256-bit secret and write it to the daemon's stdin before it
        # binds the socket. The daemon reads this line synchronously before
        # accepting connections, then validates it on every RPC via metadata.
        # Check the pipe exists before minting — a secret is only worth
        # generating if there is a process to send it to.
        if self._proc is None or self._proc.stdin is None:
            try:
                self._force_kill()
            finally:
                self._cleanup_tempdir()
            raise RuntimeError(
                "Accelerator daemon process or its stdin is not initialized."
            )
        self._auth_secret = secrets.token_urlsafe(32)
        try:
            self._proc.stdin.write(f"{self._auth_secret}\n".encode())
            self._proc.stdin.flush()
        except (OSError, ValueError) as exc:
            try:
                self._force_kill()
            finally:
                self._cleanup_tempdir()
            raise RuntimeError(
                "Failed to send auth secret to accelerator daemon (process died): "
                f"{exc}"
            ) from exc

        try:
            self._wait_until_ready(self._startup_timeout)
        except BaseException:
            try:
                self._force_kill()
            finally:
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
                    # Step 2: SIGTERM. On Windows this is TerminateProcess, so
                    # steps 2 and 3 are the same hard kill and the daemon's one
                    # chance to shut down cleanly is the stdin EOF above —
                    # which is also the signal it uses there to notice the
                    # parent died, since a ppid watchdog cannot work on
                    # Windows.
                    try:
                        proc.terminate()
                    except OSError:
                        pass
                    if not self._wait_for_exit(_SIGTERM_GRACE_SECONDS):
                        # Step 3: SIGKILL. Bounded wait so teardown can't hang
                        # forever if the process is stuck unreapable.
                        try:
                            proc.kill()
                        except OSError:
                            pass
                        self._wait_for_exit(_SIGKILL_GRACE_SECONDS)
        finally:
            self._proc = None
            self._cleanup_tempdir()

    def read_identity(self) -> dict[str, Any]:
        """Read and consume the daemon's ``identity.json``.

        The daemon writes the principal it resolved to this file (in the same
        0700 tempdir as the socket) before it binds, so it is guaranteed present
        once ``start()`` returns. Read it once, then unlink it — the identity is
        verified a single time at connect and never needs re-reading.

        Raises:
            RuntimeError: if the daemon was never started, or if it did not
                write an ``identity.json`` (e.g. an older binary), so the caller
                can fall back to the native client rather than route blindly.
        """
        if self._tempdir is None:
            raise RuntimeError("AcceleratorDaemon has not been started")
        path = os.path.join(self._tempdir, _IDENTITY_FILENAME)
        try:
            with open(path, "rb") as f:
                return json.load(f)
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"Accelerator daemon did not write {_IDENTITY_FILENAME}; "
                "cannot verify its identity"
            ) from exc
        except (OSError, ValueError) as exc:
            raise RuntimeError(f"Failed to read {_IDENTITY_FILENAME}: {exc}") from exc
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _wait_until_ready(self, timeout: float) -> None:
        """Poll until the UDS accepts a connection, the child dies, or timeout.

        Raises RuntimeError if the daemon exits during startup or does not
        become connectable within ``timeout`` seconds.
        """
        if self._proc is None or self._uds_path is None:
            raise RuntimeError("AcceleratorDaemon._wait_until_ready() before spawn")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            exit_code = self._proc.poll()
            if exit_code is not None:
                log_tail = self._read_log_tail()
                raise RuntimeError(
                    "Accelerator daemon exited during startup "
                    f"(exit code {exit_code}). log: {log_tail!r}"
                )
            if _socket_is_live(self._uds_path):
                return
            time.sleep(0.05)
        log_tail = self._read_log_tail()
        raise RuntimeError(
            "Accelerator daemon did not become ready within "
            f"{timeout}s. log: {log_tail!r}"
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
                # Bound the read too, so a log smaller than max_bytes (seek
                # failed, fell back to seek(0)) is still capped.
                data = fh.read(max_bytes)
        except OSError:
            return ""
        return data.decode("utf-8", errors="replace")

    def _wait_for_exit(self, timeout: float) -> bool:
        """Wait up to ``timeout`` seconds for the child to exit.

        Returns True if it has exited (or there is no child), False on timeout.
        """
        if self._proc is None:
            return True
        try:
            self._proc.wait(timeout=timeout)
            return True
        except subprocess.TimeoutExpired:
            return False

    def _force_kill(self) -> None:
        """SIGKILL the child and reap it; a no-op if it is already gone."""
        if self._proc is None or self._proc.poll() is not None:
            return
        try:
            self._proc.kill()
        except (OSError, ProcessLookupError):
            pass
        try:
            self._proc.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            pass

    def _cleanup_tempdir(self) -> None:
        """Remove the tempdir holding the socket and log; clear derived paths."""
        if self._tempdir is not None and os.path.isdir(self._tempdir):
            shutil.rmtree(self._tempdir, ignore_errors=True)
        self._tempdir = None
        self._uds_path = None
        self._log_path = None
        self._auth_secret = None
