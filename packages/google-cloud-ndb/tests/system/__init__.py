# Copyright 2018 Google LLC
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

import time

KIND = "SomeKind"
OTHER_NAMESPACE = "other-namespace"


def eventually(predicate, timeout=30, interval=1):
    """Runs `predicate` in a loop, hoping for eventual success.

    Some things we're trying to test in Datastore are eventually
    consistent—we'll write something to the Datastore and can read back out
    data, eventually. This is particularly true for metadata, where we can
    write an entity to Datastore and it takes some amount of time for metadata
    about the entity's "kind" to update to match the new data just written,
    which can be challenging for system testing.

    With `eventually`, you can pass in a callable `predicate` which can tell us
    whether the Datastore is now in a consistent state, at least for the piece
    we're trying to test. This function will call the predicate repeatedly in a
    loop until it either returns `True` or `timeout` is exceeded.

    Args:
        predicate (Callable[[], bool]): A function to be called. A return value
            of `True` indicates a consistent state and will cause `eventually`
            to return so execution can proceed in the calling context.
        timeout (float): Time in seconds to wait for predicate to return
            `True`. After this amount of time, `eventually` will return
            regardless of `predicate` return value.
        interval (float): Time in seconds to wait in between invocations of
            `predicate`.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            break
        time.sleep(interval)
