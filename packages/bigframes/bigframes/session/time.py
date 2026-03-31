# Copyright 2024 Google LLC
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

import datetime
import threading
import time
from typing import cast, Optional

import google.cloud.bigquery as bigquery

MIN_RESYNC_SECONDS = 100


class BigQuerySyncedClock:
    """
    Local clock that attempts to synchronize its time with the bigquery service.
    """

    def __init__(self, bqclient: bigquery.Client):
        self._bqclient = bqclient
        self._sync_lock = threading.Lock()
        self._sync_remote_time: Optional[datetime.datetime] = None
        self._sync_monotonic_time: Optional[float] = None

    def get_time(self):
        if (self._sync_monotonic_time is None) or (self._sync_remote_time is None):
            self.sync()
        assert self._sync_remote_time is not None
        assert self._sync_monotonic_time is not None
        return self._sync_remote_time + datetime.timedelta(
            seconds=time.monotonic() - self._sync_monotonic_time
        )

    def sync(self):
        with self._sync_lock:
            if (self._sync_monotonic_time is not None) and (
                time.monotonic() - self._sync_monotonic_time
            ) < MIN_RESYNC_SECONDS:
                return
            current_bq_time = list(
                next(
                    self._bqclient.query_and_wait(
                        "SELECT CURRENT_TIMESTAMP() AS `current_timestamp`",
                    )
                )
            )[0]
            self._sync_remote_time = cast(datetime.datetime, current_bq_time)
            self._sync_monotonic_time = time.monotonic()
