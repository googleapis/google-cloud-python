# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import

from google.cloud.pubsub_v1 import futures


class Future(futures.Future):
    """Encapsulation of the asynchronous execution of an action.

    This object is returned from asychronous Pub/Sub publishing calls, and is
    the interface to determine the status of those calls.

    This object should not be created directly, but is returned by other
    methods in this library.

    Args:
        completed (Optional[Any]): An event, with the same interface as
            :class:`threading.Event`. This is provided so that callers
            with different concurrency models (e.g. ``threading`` or
            ``multiprocessing``) can supply an event that is compatible
            with that model. The ``wait()`` and ``set()`` methods will be
            used. If this argument is not provided, then a new
            :class:`threading.Event` will be created and used.
    """
    # The publishing-side subclass does not need any special behavior
    # at this time.
    #
    # However, there is still a subclass so that if someone attempts
    # isinstance checks against a publisher-returned or subscriber-returned
    # future, trying either one against the other returns False.
    pass


__all__ = (
    'Future',
)
