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

"""Cancel superseded Cloud Build PR runs when a newer commit is pushed.

Cloud Build triggers do not provide a native ``cancel-in-progress`` setting
(unlike GitHub Actions ``concurrency`` or Kokoro's
``stop_outdated_presubmit_builds``). When Cloud Build concurrency slots are
saturated, a newly pushed commit sits in ``QUEUED`` and cannot even start its
first build step until an older ``WORKING`` build exits.

This script solves both cases using only the Python standard library and the
Cloud Build REST API (authenticated via the GCE metadata server):

1. ``--cancel-older`` (run once at build startup):
   Lists all ``QUEUED`` / ``WORKING`` builds for the same trigger and PR number
   whose ``createTime`` is earlier than this build and cancels them.
2. ``--watch`` (run in the background while tests execute):
   Polls every ``--interval`` seconds (default 30s) for any ``QUEUED`` /
   ``WORKING`` build for the same trigger and PR number whose ``createTime`` is
   newer than this build (whether from a new commit or a duplicate re-run). If
   found, this build cancels itself via ``builds:cancel`` so its concurrency
   slot is freed immediately for the newer run.

Requires ``PROJECT_ID``, ``LOCATION``, and ``BUILD_ID`` environment variables
(populated from Cloud Build built-in substitutions) and
``roles/cloudbuild.builds.editor`` on the build service account.

Non-PR builds (e.g. postsubmit pushes on ``main`` where ``_PR_NUMBER`` is
absent) exit cleanly as a no-op. Any transient API/network errors fail open
with a warning so cancellation checks never break CI test execution.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


METADATA_TOKEN_URL = (
    "http://metadata.google.internal/computeMetadata/v1/"
    "instance/service-accounts/default/token"
)


def _get_access_token() -> str:
    """Fetch a short-lived OAuth2 access token from the GCE metadata server."""
    req = urllib.request.Request(
        METADATA_TOKEN_URL,
        headers={"Metadata-Flavor": "Google"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]


def _api_request(
    method: str,
    url: str,
    token: str,
    body: bytes | None = None,
) -> dict:
    """Execute an authenticated JSON HTTP request against the Cloud Build API."""
    headers = {"Authorization": f"Bearer {token}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def _parse_timestamp(raw_ts: str) -> datetime:
    """Parse an RFC 3339 Cloud Build timestamp (e.g. ``2026-11-19T17:00:00.123Z``)."""
    # Python 3.11+ fromisoformat handles trailing "Z", normalize for 3.10 compatibility.
    normalized = raw_ts.replace("Z", "+00:00")
    # Truncate sub-microsecond nanoseconds (9 digits) to 6 digits if present.
    if "." in normalized:
        date_part, rest = normalized.split(".", 1)
        sign_idx = max(rest.find("+"), rest.find("-"))
        frac = rest[:sign_idx][:6].ljust(6, "0")
        tz = rest[sign_idx:]
        normalized = f"{date_part}.{frac}{tz}"
    return datetime.fromisoformat(normalized)


def _base_url(project_id: str, location: str) -> str:
    """Return the regional Cloud Build v1 builds endpoint."""
    return (
        f"https://cloudbuild.googleapis.com/v1/"
        f"projects/{project_id}/locations/{location}/builds"
    )


def _get_build(project_id: str, location: str, build_id: str, token: str) -> dict:
    """Fetch metadata (trigger ID, substitutions, createTime) for a single build."""
    url = f"{_base_url(project_id, location)}/{build_id}"
    return _api_request("GET", url, token)


def _list_active_trigger_builds(
    project_id: str,
    location: str,
    trigger_id: str,
    token: str,
) -> list[dict]:
    """List all QUEUED or WORKING builds belonging to the same Cloud Build trigger."""
    filter_expr = f'trigger_id="{trigger_id}" AND (status="QUEUED" OR status="WORKING")'
    builds: list[dict] = []
    page_token = ""

    while True:
        params = {"filter": filter_expr, "pageSize": "100"}
        if page_token:
            params["pageToken"] = page_token
        url = f"{_base_url(project_id, location)}?{urllib.parse.urlencode(params)}"
        data = _api_request("GET", url, token)
        builds.extend(data.get("builds", []))
        page_token = data.get("nextPageToken", "")
        if not page_token:
            break

    return builds


def _cancel_build(project_id: str, location: str, build_id: str, token: str) -> None:
    """Issue a Cloud Build CancelBuild request for ``build_id``."""
    url = f"{_base_url(project_id, location)}/{build_id}:cancel"
    _api_request("POST", url, token, body=b"{}")


def _extract_pr_context(build: dict) -> tuple[str, str, str, datetime] | None:
    """Extract ``(trigger_id, pr_number, commit_sha, create_time)`` for a PR build.

    Returns ``None`` if the build is not associated with a trigger or pull request
    (e.g. postsubmit continuous builds on ``main``).
    """
    trigger_id = build.get("buildTriggerId", "")
    substitutions = build.get("substitutions") or {}
    pr_number = substitutions.get("_PR_NUMBER", "")
    commit_sha = substitutions.get("COMMIT_SHA", "")
    create_time_raw = build.get("createTime", "")

    if not trigger_id or not pr_number or not create_time_raw:
        return None

    return trigger_id, pr_number, commit_sha, _parse_timestamp(create_time_raw)


def _cancel_older_builds(
    project_id: str,
    location: str,
    my_build_id: str,
    trigger_id: str,
    pr_number: str,
    my_commit_sha: str,
    my_create_time: datetime,
    token: str,
) -> None:
    """Cancel any older QUEUED/WORKING builds for the same PR and trigger."""
    active_builds = _list_active_trigger_builds(project_id, location, trigger_id, token)
    for other in active_builds:
        other_id = other.get("id", "")
        if not other_id or other_id == my_build_id:
            continue
        other_subs = other.get("substitutions") or {}
        if other_subs.get("_PR_NUMBER") != pr_number:
            continue
        other_sha = other_subs.get("COMMIT_SHA", "")
        other_create_raw = other.get("createTime", "")
        if not other_create_raw:
            continue
        # Cancel any earlier build for the same PR and trigger — including
        # duplicate runs / manual re-runs of the same commit SHA — using
        # build ID as a deterministic tie-breaker if timestamps match.
        if (_parse_timestamp(other_create_raw), other_id) < (
            my_create_time,
            my_build_id,
        ):
            print(
                f"[cancel-superseded] Cancelling older {other.get('status')} build "
                f"{other_id} (PR #{pr_number}, commit {other_sha[:8]}) superseded by "
                f"{my_build_id} (commit {my_commit_sha[:8]}).",
                flush=True,
            )
            try:
                _cancel_build(project_id, location, other_id, token)
            except urllib.error.URLError as exc:
                print(
                    f"[cancel-superseded] Warning: failed to cancel {other_id}: {exc}",
                    file=sys.stderr,
                    flush=True,
                )


def _watch_for_newer_build(
    project_id: str,
    location: str,
    my_build_id: str,
    trigger_id: str,
    pr_number: str,
    my_commit_sha: str,
    my_create_time: datetime,
    interval: int,
) -> None:
    """Poll until a newer commit build for the same PR + trigger appears, then self-cancel."""
    while True:
        time.sleep(interval)
        try:
            # Refresh metadata token each iteration so long-running builds never hit expiry.
            token = _get_access_token()
            active_builds = _list_active_trigger_builds(
                project_id, location, trigger_id, token
            )
            for other in active_builds:
                other_id = other.get("id", "")
                if not other_id or other_id == my_build_id:
                    continue
                other_subs = other.get("substitutions") or {}
                if other_subs.get("_PR_NUMBER") != pr_number:
                    continue
                other_sha = other_subs.get("COMMIT_SHA", "")
                other_create_raw = other.get("createTime", "")
                if not other_create_raw:
                    continue
                if (_parse_timestamp(other_create_raw), other_id) > (
                    my_create_time,
                    my_build_id,
                ):
                    print(
                        f"[cancel-superseded] Newer {other.get('status')} build {other_id} "
                        f"(PR #{pr_number}, commit {other_sha[:8]}) detected; "
                        f"self-cancelling {my_build_id} to free worker slot.",
                        flush=True,
                    )
                    _cancel_build(project_id, location, my_build_id, token)
                    return
        except Exception as exc:
            # Fail open on transient metadata/API errors and keep watching.
            print(
                f"[cancel-superseded] Watchdog warning (will retry): {exc}",
                file=sys.stderr,
                flush=True,
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cancel superseded Cloud Build PR runs for the same trigger."
    )
    parser.add_argument(
        "--cancel-older",
        action="store_true",
        help="Cancel older QUEUED/WORKING builds for the same PR and trigger.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Continuously watch for a newer commit on the same PR and self-cancel.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Polling interval in seconds for --watch mode (default: 30).",
    )
    args = parser.parse_args()

    project_id = os.environ.get("PROJECT_ID", "")
    location = os.environ.get("LOCATION", "")
    build_id = os.environ.get("BUILD_ID", "")
    if not project_id or not location or not build_id:
        return 0

    try:
        token = _get_access_token()
        current_build = _get_build(project_id, location, build_id, token)
    except Exception as exc:
        print(
            f"[cancel-superseded] Warning: unable to query build metadata ({exc}); skipping.",
            file=sys.stderr,
            flush=True,
        )
        return 0

    ctx = _extract_pr_context(current_build)
    if ctx is None:
        # Postsubmit push or manual build without _PR_NUMBER; nothing to cancel.
        return 0

    trigger_id, pr_number, my_commit_sha, my_create_time = ctx

    if args.cancel_older:
        try:
            _cancel_older_builds(
                project_id,
                location,
                build_id,
                trigger_id,
                pr_number,
                my_commit_sha,
                my_create_time,
                token,
            )
        except Exception as exc:
            print(
                f"[cancel-superseded] Warning: failed to cancel older builds ({exc}).",
                file=sys.stderr,
                flush=True,
            )

    if args.watch:
        _watch_for_newer_build(
            project_id,
            location,
            build_id,
            trigger_id,
            pr_number,
            my_commit_sha,
            my_create_time,
            args.interval,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
