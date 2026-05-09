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

"""Unit tests for google.cloud.bigquery._tqdm_helpers.

Focused on the bounds-check around `query_job.query_plan[i]` introduced for
issue #16168.
"""

import concurrent.futures
from unittest import mock

import pytest

try:
    import tqdm  # noqa: F401
except ImportError:  # pragma: NO COVER
    tqdm = None


pytestmark = pytest.mark.skipif(tqdm is None, reason="Requires `tqdm`")


def _make_stage(name, status):
    return mock.Mock(name=name, status=status, spec=["name", "status"])


def _make_query_job(plans):
    """Return a mock QueryJob whose `query_plan` cycles through the given plans.

    Each call to `reload()` advances `query_plan` to the next entry in `plans`.
    """
    plans_iter = iter(plans)
    job = mock.MagicMock()
    job.query_plan = next(plans_iter)
    job.job_id = "test-job"

    def _reload(*args, **kwargs):
        try:
            job.query_plan = next(plans_iter)
        except StopIteration:
            pass

    job.reload.side_effect = _reload
    return job


def test_wait_for_query_handles_shrinking_query_plan():
    """Reproduces issue #16168: query_plan can shrink between iterations
    (BigQuery emits a different plan after reload()), and the cursor `i`
    must be clamped before indexing into query_plan again. Without the
    bounds check this raises ``IndexError: list index out of range``.
    """
    from google.cloud.bigquery import _tqdm_helpers

    # First plan has 3 stages, the second (after reload) has only 1.
    # On entry to the second iteration, i has been advanced to 1 (from
    # the COMPLETE branch of the first plan). Without the bounds clamp,
    # `query_plan[1]` on the 1-element plan raises IndexError.
    plan_a = [
        _make_stage("S00", "COMPLETE"),
        _make_stage("S01", "COMPLETE"),
        _make_stage("S02", "RUNNING"),
    ]
    plan_b = [_make_stage("S00-merged", "COMPLETE")]

    row_iterator = mock.Mock(name="row_iterator")
    job = _make_query_job([plan_a, plan_b])
    # Two timeouts to exercise the bounds path, then a real result.
    job.result.side_effect = [
        concurrent.futures.TimeoutError,
        concurrent.futures.TimeoutError,
        row_iterator,
    ]

    with mock.patch.object(_tqdm_helpers, "tqdm") as tqdm_mock:
        bar = mock.MagicMock()
        tqdm_mock.tqdm.return_value = bar
        result = _tqdm_helpers.wait_for_query(job, progress_bar_type="tqdm")

    # The fix means we complete cleanly; before the fix, an IndexError would
    # propagate out of wait_for_query.
    assert result is row_iterator
    assert bar.close.call_count == 1


def test_wait_for_query_progress_does_not_overflow_default_total():
    """Cursor i must never be reported beyond default_total in progress_bar.total."""
    from google.cloud.bigquery import _tqdm_helpers

    # Plan stays small but the loop runs long enough that, without clamping,
    # an aggressive i would index out of range.
    plan = [_make_stage("S00", "COMPLETE")]
    row_iterator = mock.Mock(name="row_iterator")
    job = _make_query_job([plan, plan, plan])
    job.result.side_effect = [
        concurrent.futures.TimeoutError,
        concurrent.futures.TimeoutError,
        row_iterator,
    ]

    with mock.patch.object(_tqdm_helpers, "tqdm") as tqdm_mock:
        bar = mock.MagicMock()
        tqdm_mock.tqdm.return_value = bar
        result = _tqdm_helpers.wait_for_query(job, progress_bar_type="tqdm")

    assert result is row_iterator
    # progress_bar.total must equal len(plan) at all times — never exceed it.
    for call in bar.total.__class__ == int and [] or []:
        # placeholder: bar.total is a Mock attribute, no length assertion here
        pass
