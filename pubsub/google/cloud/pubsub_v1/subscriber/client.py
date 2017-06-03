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

import functools
import pkg_resources

import six

from google.cloud.gapic.pubsub.v1 import subscriber_client

from google.cloud.pubsub_v1 import _gapic
from google.cloud.pubsub_v1 import types


__VERSION__ = pkg_resources.get_distribution('google-cloud-pubsub').version


@_gapic.add_methods(subscriber_client.SubscriberClient,
                    blacklist=('pull', 'streaming_pull')):
class SubscriberClient(object):
    """A subscriber client for Google Cloud Pub/Sub.

    This creates an object that is capable of subscribing to messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        flow_control (~.pubsub_v1.types.FlowControl): The flow control
            settings to be used on individual subscriptions.
        subscription_class (class): A class that describes how to handle
            subscriptions. You may subclass the
            :class:`.pubsub_v1.subscriber.subscription.base.BaseSubscription`
            class in order to define your own subscriber. This is primarily
            provided to allow use of different concurrency models; the default
            is based on :class:`multiprocessing.Process`.
        **kwargs (dict): Any additional arguments provided are sent as keyword
            keyword arguments to the underlying
            :class:`~.gapic.pubsub.v1.subscriber_client.SubscriberClient`.
            Generally, you should not need to set additional keyword
            arguments.
    """
    def __init__(self, flow_control=(), subscription_class=mp.Subscription,
                 **kwargs):
        # Add the metrics headers, and instantiate the underlying GAPIC
        # client.
        kwargs['lib_name'] = 'gccl'
        kwargs['lib_version'] = __VERSION__
        self.api = subscriber_client.SubscriberClient(**kwargs)

        # The subcription class is responsible to retrieving and dispatching
        # messages.
        self._subscription_class = subscription_class
