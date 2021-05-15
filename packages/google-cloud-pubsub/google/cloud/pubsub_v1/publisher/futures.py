# Copyright 2019, Google LLC All rights reserved.
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
    """This future object is returned from asychronous Pub/Sub publishing
    calls.

    Calling :meth:`result` will resolve the future by returning the message
    ID, unless an error occurs.
    """

    def cancel(self):
        """Actions in Pub/Sub generally may not be canceled.

        This method always returns ``False``.
        """
        return False

    def cancelled(self):
        """Actions in Pub/Sub generally may not be canceled.

        This method always returns ``False``.
        """
        return False

    def result(self, timeout=None):
        """Return the message ID or raise an exception.

        This blocks until the message has been published successfully and
        returns the message ID unless an exception is raised.

        Args:
            timeout (Union[int, float]): The number of seconds before this call
                times out and raises TimeoutError.

        Returns:
            str: The message ID.

        Raises:
            concurrent.futures.TimeoutError: If the request times out.
            Exception: For undefined exceptions in the underlying
                call execution.
        """
        return super().result(timeout=timeout)
