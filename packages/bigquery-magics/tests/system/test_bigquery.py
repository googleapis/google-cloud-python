# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""System tests for Jupyter/IPython connector."""

import contextlib
import gc
import re
import time

import pandas
import psutil
from IPython.testing import globalipapp
from IPython.utils import io


@contextlib.contextmanager
def patch_tracked_requests():
    """Context manager to patch google-auth requests and track/close their HTTP sessions.

    This prevents socket leaks in system tests that use Workload Identity or metadata server auth.
    """
    import google.auth.transport.requests

    original_init = google.auth.transport.requests.Request.__init__
    tracked_requests = []

    def patched_init(self, session=None):
        original_init(self, session=session)
        if session is None:
            tracked_requests.append(self)

    google.auth.transport.requests.Request.__init__ = patched_init
    try:
        yield tracked_requests
    finally:
        google.auth.transport.requests.Request.__init__ = original_init
        for req in tracked_requests:
            if hasattr(req, "session") and req.session is not None:
                req.session.close()


def test_bigquery_magic():
    globalipapp.start_ipython()
    ip = globalipapp.get_ipython()
    current_process = psutil.Process()

    # GC to ensure clean starting state
    gc.collect()
    conn_count_start = len(current_process.net_connections())

    with patch_tracked_requests():
        ip.extension_manager.load_extension("bigquery_magics")
        sql = """
            SELECT
                CONCAT(
                'https://stackoverflow.com/questions/',
                CAST(id as STRING)) as url,
                view_count
            FROM `bigquery-public-data.stackoverflow.posts_questions`
            WHERE tags like '%google-bigquery%'
            ORDER BY view_count DESC
            LIMIT 10
        """
        with io.capture_output() as captured:
            result = ip.run_cell_magic("bigquery", "--use_rest_api", sql)

    # Force garbage collection to sweep unreferenced socket objects
    gc.collect()

    # Wait a bit for the asynchronous channel teardown to complete and the socket to be closed.
    for _ in range(30):
        conn_count_end = len(current_process.net_connections())
        if conn_count_end <= conn_count_start:
            break
        time.sleep(0.1)

    lines = re.split("\n|\r", captured.stdout)
    # Removes blanks & terminal code (result of display clearing)
    updates = list(filter(lambda x: bool(x) and x != "\x1b[2K", lines))
    assert re.match("Executing query with job ID: .*", updates[0])
    assert (re.match("Query executing: .*s", line) for line in updates[1:-1])
    assert isinstance(result, pandas.DataFrame)
    assert len(result) == 10  # verify row count
    assert list(result) == ["url", "view_count"]  # verify column names

    # NOTE: For some reason, the number of open sockets is sometimes one *less*
    # than expected when running system tests on Kokoro, thus using the <= assertion.
    # That's still fine, however, since the sockets are apparently not leaked.
    assert conn_count_end <= conn_count_start  # system resources are released
