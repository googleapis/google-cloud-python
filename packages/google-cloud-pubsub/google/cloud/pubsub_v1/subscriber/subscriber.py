# Copyright 2017, Google LLC
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

from google.cloud.pubsub_v1 import types


class Subscriber(object):
    """A consumer class based on :class:`threading.Thread`.

    This consumer handles the connection to the Pub/Sub service and all of
    the concurrency needs.

    Args:
        client (~.pubsub_v1.subscriber.client): The subscriber client used
            to create this instance.
        subscription (str): The name of the subscription. The canonical
            format for this is
            ``projects/{project}/subscriptions/{subscription}``.
        flow_control (~google.cloud.pubsub_v1.types.FlowControl): The flow
            control settings.
        executor (~concurrent.futures.ThreadPoolExecutor): (Optional.) A
            ThreadPoolExecutor instance, or anything duck-type compatible
            with it.
        queue (~queue.Queue): (Optional.) A Queue instance, appropriate
            for crossing the concurrency boundary implemented by
            ``executor``.
    """

    def __init__(self, client, subscription, flow_control=types.FlowControl(),
                 scheduler_cls=None):
        raise NotImplementedError

    @property
    def is_active(self):
        raise NotImplementedError

    @property
    def flow_control(self):
        raise NotImplementedError

    @property
    def ack_histogram(self):
        raise NotImplementedError

    @property
    def future(self):
        raise NotImplementedError

    #
    # User-facing subscriber management methods.
    #

    def open(self, callback):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    #
    # Message management methods
    #

    def ack(self, items):
        raise NotImplementedError

    def drop(self, items):
        raise NotImplementedError

    def lease(self, items):
        raise NotImplementedError

    def modify_ack_deadline(self, items):
        raise NotImplementedError

    def nack(self, items):
        raise NotImplementedError
