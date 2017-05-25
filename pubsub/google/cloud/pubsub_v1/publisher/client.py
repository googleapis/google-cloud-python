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
import multiprocessing
import pkg_resources

import six

from google.cloud.gapic.pubsub.v1 import publisher_client

from google.cloud.pubsub_v1 import types


__VERSION__ = pkg_resources.get_distribution('google-cloud-pubsub').version


@_gapic.add_methods(publisher_client.PublisherClient, blacklist=('publish',))
class PublisherClient(object):
    """A publisher client for Cloud Pub/Sub.

    This creates an object that is capable of publishing messages.
    Generally, you can instantiate this client with no arguments, and you
    get sensible defaults.

    Args:
        batching (:class:`google.cloud.pubsub_v1.types.Batching`): The
            settings for batch publishing.
        thread_class (class): Any class that is duck-type compatible with
            :class:`threading.Thread`.
            The default is :class:`multiprocessing.Process`
        kwargs (dict): Any additional arguments provided are sent as keyword
            arguments to the underlying
            :class:`~gapic.pubsub.v1.publisher_client.PublisherClient`.
            Generally, you should not need to set additional keyword arguments.
    """

    def __init__(self, batching=(), thread_class=multiprocessing.Process,
                 queue_class=multiprocessing.Queue, **kwargs):
        # Add the metrics headers, and instantiate the underlying GAPIC
        # client.
        kwargs['lib_name'] = 'gccl'
        kwargs['lib_version'] = __VERSION__
        self.api = publisher_client.PublisherClient(*args, **kwargs)
        self.batching = types.Batching(batching)

        # Set the thread class.
        self._thread_class = thread_class

        # The batch on the publisher client is responsible for holding
        # messages.
        #
        # We set this to None for now; the first message that is published
        # will create it (in order to ensure that the start time is correct).
        self._batch = None

    @property
    def batch(self):
        """Return the current batch.

        This will create a new batch if no batch currently exists.

        Returns:
            :class:~`pubsub_v1.batch.Batch` The batch object.
        """
        if self._batch is None:
            self_batch = Batch(client=self, settings=self.batching)
        return self._batch

    @property
    def thread_class(self):
        """Return the thread class provided at instantiation.

        Returns:
            class: A class duck-type compatible with :class:`threading.Thread`.
        """
        return self._thread_class

    @functools.wraps(Batch.publish)
    def publish(self, data, **attrs):
        return self.batch.publish(data, *attrs)
