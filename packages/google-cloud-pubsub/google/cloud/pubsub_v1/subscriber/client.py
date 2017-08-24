# Copyright 2017, Google Inc. All rights reserved.
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

import pkg_resources

from google.cloud.gapic.pubsub.v1 import subscriber_client

from google.cloud.pubsub_v1 import _gapic
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.subscriber.policy import thread


__VERSION__ = pkg_resources.get_distribution('google-cloud-pubsub').version


@_gapic.add_methods(subscriber_client.SubscriberClient,
                    blacklist=('pull', 'streaming_pull'))
class Client(object):
    """A subscriber client for Google Cloud Pub/Sub.

    This creates an object that is capable of subscribing to messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        policy_class (class): A class that describes how to handle
            subscriptions. You may subclass the
            :class:`.pubsub_v1.subscriber.policy.base.BasePolicy`
            class in order to define your own consumer. This is primarily
            provided to allow use of different concurrency models; the default
            is based on :class:`threading.Thread`.
        kwargs (dict): Any additional arguments provided are sent as keyword
            keyword arguments to the underlying
            :class:`~.gapic.pubsub.v1.subscriber_client.SubscriberClient`.
            Generally, you should not need to set additional keyword
            arguments.
    """
    def __init__(self, policy_class=thread.Policy, **kwargs):
        # Add the metrics headers, and instantiate the underlying GAPIC
        # client.
        kwargs['lib_name'] = 'gccl'
        kwargs['lib_version'] = __VERSION__
        self.api = subscriber_client.SubscriberClient(**kwargs)

        # The subcription class is responsible to retrieving and dispatching
        # messages.
        self._policy_class = policy_class

    def subscribe(self, subscription, callback=None, flow_control=()):
        """Return a representation of an individual subscription.

        This method creates and returns a ``Consumer`` object (that is, a
        :class:`~.pubsub_v1.subscriber.consumer.base.BaseConsumer`)
        subclass) bound to the topic. It does `not` create the subcription
        on the backend (or do any API call at all); it simply returns an
        object capable of doing these things.

        If the ``callback`` argument is provided, then the :meth:`open` method
        is automatically called on the returned object. If ``callback`` is
        not provided, the subscription is returned unopened.

        .. note::
            It only makes sense to provide ``callback`` here if you have
            already created the subscription manually in the API.

        Args:
            subscription (str): The name of the subscription. The
                subscription should have already been created (for example,
                by using :meth:`create_subscription`).
            callback (function): The callback function. This function receives
                the :class:`~.pubsub_v1.types.PubsubMessage` as its only
                argument.
            flow_control (~.pubsub_v1.types.FlowControl): The flow control
                settings. Use this to prevent situations where you are
                inundated with too many messages at once.

        Returns:
            ~.pubsub_v1.subscriber.consumer.base.BaseConsumer: An instance
                of the defined ``consumer_class`` on the client.
        """
        flow_control = types.FlowControl(*flow_control)
        subscr = self._policy_class(self, subscription, flow_control)
        if callable(callback):
            subscr.open(callback)
        return subscr
