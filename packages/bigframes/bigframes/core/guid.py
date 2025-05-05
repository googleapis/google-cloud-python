# Copyright 2023 Google LLC
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
import threading
import typing

_GUID_LOCK = threading.Lock()
_GUID_COUNTER = 0


def generate_guid(prefix="col_"):
    global _GUID_LOCK
    with _GUID_LOCK:
        global _GUID_COUNTER
        _GUID_COUNTER += 1
        return f"bfuid_{prefix}{_GUID_COUNTER}"


class SequentialUIDGenerator:
    """Produces a sequence of UIDs, such as {"t0", "t1", "c0", "t2", ...}, by
    cycling through provided prefixes (e.g., "t" and "c").
    Note: this function is not thread-safe.
    """

    def __init__(self):
        self.prefix_counters: typing.Dict[str, int] = {}

    def get_uid_stream(self, prefix: str) -> typing.Generator[str, None, None]:
        """Yields a continuous stream of raw UID strings for the given prefix."""
        if prefix not in self.prefix_counters:
            self.prefix_counters[prefix] = 0

        while True:
            uid = f"{prefix}{self.prefix_counters[prefix]}"
            self.prefix_counters[prefix] += 1
            yield uid
