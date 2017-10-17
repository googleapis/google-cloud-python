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

import datetime
import time
import uuid

import mock
import six

from google import auth
from google.cloud import pubsub_v1


def _resource_name(resource_type):
    """Return a randomly selected name for a resource.

    Args:
        resource_type (str): The resource for which a name is being
            generated. Should be singular (e.g. "topic", "subscription")
    """
    return 'projects/{project}/{resource_type}s/st-n{random}'.format(
        project=auth.default()[1],
        random=str(uuid.uuid4())[0:8],
        resource_type=resource_type,
    )


def test_publish_messages():
    publisher = pubsub_v1.PublisherClient()
    topic_name = _resource_name('topic')
    futures = []

    try:
        publisher.create_topic(topic_name)
        for i in range(0, 500):
            futures.append(
                publisher.publish(
                    topic_name,
                    b'The hail in Wales falls mainly on the snails.',
                    num=str(i),
                ),
            )
        for future in futures:
            result = future.result()
            assert isinstance(result, (six.text_type, six.binary_type))
    finally:
        publisher.delete_topic(topic_name)


def test_subscribe_to_messages():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_name = _resource_name('topic')
    sub_name = _resource_name('subscription')

    try:
        # Create a topic.
        publisher.create_topic(topic_name)

        # Subscribe to the topic. This must happen before the messages
        # are published.
        subscriber.create_subscription(sub_name, topic_name)
        subscription = subscriber.subscribe(sub_name)

        # Publish some messages.
        futures = [publisher.publish(
            topic_name,
            b'Wooooo! The claaaaaw!',
            num=str(i),
        ) for i in range(0, 50)]

        # Make sure the publish completes.
        [f.result() for f in futures]

        # The callback should process the message numbers to prove
        # that we got everything at least once.
        callback = mock.Mock(wraps=lambda message: message.ack())

        # Actually open the subscription and hold it open for a few seconds.
        subscription.open(callback)
        for second in range(0, 10):
            time.sleep(1)

            # The callback should have fired at least fifty times, but it
            # may take some time.
            if callback.call_count >= 50:
                return

        # Okay, we took too long; fail out.
        assert callback.call_count >= 50
    finally:
        publisher.delete_topic(topic_name)


def test_subscribe_to_messages_async_callbacks():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_name = _resource_name('topic')
    sub_name = _resource_name('subscription')

    try:
        # Create a topic.
        publisher.create_topic(topic_name)

        # Subscribe to the topic. This must happen before the messages
        # are published.
        subscriber.create_subscription(sub_name, topic_name)
        subscription = subscriber.subscribe(sub_name)

        # Publish some messages.
        futures = [publisher.publish(
            topic_name,
            b'Wooooo! The claaaaaw!',
            num=str(i),
        ) for i in range(0, 2)]

        # Make sure the publish completes.
        [f.result() for f in futures]

        # We want to make sure that the callback was called asynchronously. So
        # track when each call happened and make sure below.
        call_times = []

        def process_message(message):
            # list.append() is thread-safe.
            call_times.append(datetime.datetime.now())
            time.sleep(2)
            message.ack()

        callback = mock.Mock(wraps=process_message)
        side_effect = mock.Mock()
        callback.side_effect = side_effect

        # Actually open the subscription and hold it open for a few seconds.
        subscription.open(callback)
        for second in range(0, 5):
            time.sleep(4)

            # The callback should have fired at least two times, but it may
            # take some time.
            if callback.call_count >= 2 and side_effect.call_count >= 2:
                first = min(call_times[:2])
                last = max(call_times[:2])
                diff = last - first
                # "Ensure" the first two callbacks were executed asynchronously
                # (sequentially would have resulted in a difference of 2+
                # seconds).
                assert diff.days == 0
                assert diff.seconds < 2

        # Okay, we took too long; fail out.
        assert callback.call_count >= 2
    finally:
        publisher.delete_topic(topic_name)
