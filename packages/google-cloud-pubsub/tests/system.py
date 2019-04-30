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

import datetime
import threading
import time

import pytest
import six

import google.auth
from google.cloud import pubsub_v1


from test_utils.system import unique_resource_id


@pytest.fixture(scope=u"module")
def project():
    _, default_project = google.auth.default()
    yield default_project


@pytest.fixture(scope=u"module")
def publisher():
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope=u"module")
def subscriber():
    yield pubsub_v1.SubscriberClient()


@pytest.fixture
def topic_path(project, publisher):
    topic_name = "t" + unique_resource_id("-")
    yield publisher.topic_path(project, topic_name)


@pytest.fixture
def subscription_path(project, subscriber):
    sub_name = "s" + unique_resource_id("-")
    yield subscriber.subscription_path(project, sub_name)


@pytest.fixture
def cleanup():
    registry = []
    yield registry

    # Perform all clean up.
    for to_call, argument in registry:
        to_call(argument)

def test_publish_messages(publisher, topic_path, cleanup):
    futures = []
    # Make sure the topic gets deleted.
    cleanup.append((publisher.delete_topic, topic_path))

    publisher.create_topic(topic_path)
    for index in six.moves.range(500):
        futures.append(
            publisher.publish(
                topic_path,
                b"The hail in Wales falls mainly on the snails.",
                num=str(index),
            )
        )
    for future in futures:
        result = future.result()
        assert isinstance(result, six.string_types)


def test_subscribe_to_messages(
    publisher, topic_path, subscriber, subscription_path, cleanup
):
    # Make sure the topic and subscription get deleted.
    cleanup.append((publisher.delete_topic, topic_path))
    cleanup.append((subscriber.delete_subscription, subscription_path))

    # Create a topic.
    publisher.create_topic(topic_path)

    # Subscribe to the topic. This must happen before the messages
    # are published.
    subscriber.create_subscription(subscription_path, topic_path)

    # Publish some messages.
    futures = [
        publisher.publish(topic_path, b"Wooooo! The claaaaaw!", num=str(index))
        for index in six.moves.range(50)
    ]

    # Make sure the publish completes.
    for future in futures:
        future.result()

    # Actually open the subscription and hold it open for a few seconds.
    # The callback should process the message numbers to prove
    # that we got everything at least once.
    callback = AckCallback()
    future = subscriber.subscribe(subscription_path, callback)
    for second in six.moves.range(10):
        time.sleep(1)

        # The callback should have fired at least fifty times, but it
        # may take some time.
        if callback.calls >= 50:
            return

    # Okay, we took too long; fail out.
    assert callback.calls >= 50

    future.cancel()


def test_subscribe_to_messages_async_callbacks(
    publisher, topic_path, subscriber, subscription_path, cleanup
):
    # Make sure the topic and subscription get deleted.
    cleanup.append((publisher.delete_topic, topic_path))
    cleanup.append((subscriber.delete_subscription, subscription_path))

    # Create a topic.
    publisher.create_topic(topic_path)

    # Subscribe to the topic. This must happen before the messages
    # are published.
    subscriber.create_subscription(subscription_path, topic_path)

    # Publish some messages.
    futures = [
        publisher.publish(topic_path, b"Wooooo! The claaaaaw!", num=str(index))
        for index in six.moves.range(2)
    ]

    # Make sure the publish completes.
    for future in futures:
        future.result()

    # We want to make sure that the callback was called asynchronously. So
    # track when each call happened and make sure below.
    callback = TimesCallback(2)

    # Actually open the subscription and hold it open for a few seconds.
    future = subscriber.subscribe(subscription_path, callback)
    for second in six.moves.range(5):
        time.sleep(4)

        # The callback should have fired at least two times, but it may
        # take some time.
        if callback.calls >= 2:
            first, last = sorted(callback.call_times[:2])
            diff = last - first
            # "Ensure" the first two callbacks were executed asynchronously
            # (sequentially would have resulted in a difference of 2+
            # seconds).
            assert diff.days == 0
            assert diff.seconds < callback.sleep_time

    # Okay, we took too long; fail out.
    assert callback.calls >= 2

    future.cancel()


class AckCallback(object):
    def __init__(self):
        self.calls = 0
        self.lock = threading.Lock()

    def __call__(self, message):
        message.ack()
        # Only increment the number of calls **after** finishing.
        with self.lock:
            self.calls += 1


class TimesCallback(object):
    def __init__(self, sleep_time):
        self.sleep_time = sleep_time
        self.calls = 0
        self.call_times = []
        self.lock = threading.Lock()

    def __call__(self, message):
        now = datetime.datetime.now()
        time.sleep(self.sleep_time)
        message.ack()
        # Only increment the number of calls **after** finishing.
        with self.lock:
            # list.append() is thread-safe, but we still wait until
            # ``calls`` is incremented to do it.
            self.call_times.append(now)
            self.calls += 1
