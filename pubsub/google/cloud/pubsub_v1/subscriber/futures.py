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

    This object is returned from opening a Pub/Sub subscription, and is the
    interface to block on the subscription or query its status.

    This object should not be created directly, but is returned by other
    methods in this library.

    Args:
        policy (~.pubsub_v1.subscriber.policy.base.BasePolicy): The policy
            that creates this Future.
    """
    def __init__(self, policy):
        self._policy = policy
        super(Future, self).__init__()

    def running(self):
        """Return whether this subscription is opened with this Future.

        .. note::

            A ``False`` value here does not necessarily mean that the
            subscription is closed; it merely means that _this_ future is
            not the future applicable to it.

            Since futures have a single result (or exception) and there is
            not a concept of resetting them, a closing re-opening of a
            subscription will therefore return a new future.

        Returns:
            bool: ``True`` if this subscription is opened with this future,
                ``False`` otherwise.
        """
        return self._policy.future is self
