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
import itertools
import operator as op
import threading
import time

import mock
import pytest
import six

import google.auth
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1 import exceptions
from google.cloud.pubsub_v1 import futures
from google.cloud.pubsub_v1 import types


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


def test_creating_subscriptions_with_non_default_settings(
    publisher, subscriber, project, topic_path, subscription_path, cleanup
):
    # Make sure the topic and subscription get deleted.
    cleanup.append((publisher.delete_topic, topic_path))
    cleanup.append((subscriber.delete_subscription, subscription_path))

    # create a topic and a subscription, customize the latter's policy
    publisher.create_topic(topic_path)

    msg_retention_duration = {"seconds": 911}
    expiration_policy = {"ttl": {"seconds": 90210}}
    new_subscription = subscriber.create_subscription(
        subscription_path,
        topic_path,
        ack_deadline_seconds=30,
        retain_acked_messages=True,
        message_retention_duration=msg_retention_duration,
        expiration_policy=expiration_policy,
    )

    # fetch the subscription and check its settings
    project_path = subscriber.project_path(project)
    subscriptions = subscriber.list_subscriptions(project_path)

    subscriptions = [sub for sub in subscriptions if sub.topic == topic_path]
    assert len(subscriptions) == 1
    subscription = subscriptions[0]

    assert subscription == new_subscription
    assert subscription.ack_deadline_seconds == 30
    assert subscription.retain_acked_messages
    assert subscription.message_retention_duration.seconds == 911
    assert subscription.expiration_policy.ttl.seconds == 90210


def test_listing_project_topics(publisher, project, cleanup):
    topic_paths = [
        publisher.topic_path(project, "topic-{}".format(i) + unique_resource_id("."))
        for i in range(1, 4)
    ]
    for topic in topic_paths:
        cleanup.append((publisher.delete_topic, topic))
        publisher.create_topic(topic)

    project_path = publisher.project_path(project)
    project_topics = publisher.list_topics(project_path)
    project_topics = set(t.name for t in project_topics)

    # there might be other topics in the project, thus do a "is subset" check
    assert set(topic_paths) <= project_topics


def test_listing_project_subscriptions(publisher, subscriber, project, cleanup):
    # create topics
    topic_paths = [
        publisher.topic_path(project, "topic-1" + unique_resource_id(".")),
        publisher.topic_path(project, "topic-2" + unique_resource_id(".")),
    ]
    for topic in topic_paths:
        cleanup.append((publisher.delete_topic, topic))
        publisher.create_topic(topic)

    # create subscriptions
    subscription_paths = [
        subscriber.subscription_path(
            project, "sub-{}".format(i) + unique_resource_id(".")
        )
        for i in range(1, 4)
    ]
    for i, subscription in enumerate(subscription_paths):
        topic = topic_paths[i % 2]
        cleanup.append((subscriber.delete_subscription, subscription))
        subscriber.create_subscription(subscription, topic)

    # retrieve subscriptions and check that the list matches the expected
    project_path = subscriber.project_path(project)
    subscriptions = subscriber.list_subscriptions(project_path)
    subscriptions = set(s.name for s in subscriptions)

    # there might be other subscriptions in the project, thus do a "is subset" check
    assert set(subscription_paths) <= subscriptions


def test_listing_topic_subscriptions(publisher, subscriber, project, cleanup):
    # create topics
    topic_paths = [
        publisher.topic_path(project, "topic-1" + unique_resource_id(".")),
        publisher.topic_path(project, "topic-2" + unique_resource_id(".")),
    ]
    for topic in topic_paths:
        cleanup.append((publisher.delete_topic, topic))
        publisher.create_topic(topic)

    # create subscriptions
    subscription_paths = [
        subscriber.subscription_path(
            project, "sub-{}".format(i) + unique_resource_id(".")
        )
        for i in range(1, 4)
    ]
    for i, subscription in enumerate(subscription_paths):
        topic = topic_paths[i % 2]
        cleanup.append((subscriber.delete_subscription, subscription))
        subscriber.create_subscription(subscription, topic)

    # retrieve subscriptions and check that the list matches the expected
    subscriptions = publisher.list_topic_subscriptions(topic_paths[0])
    subscriptions = set(subscriptions)

    assert subscriptions == {subscription_paths[0], subscription_paths[2]}


def test_managing_topic_iam_policy(publisher, topic_path, cleanup):
    cleanup.append((publisher.delete_topic, topic_path))

    # create a topic and customize its policy
    publisher.create_topic(topic_path)
    topic_policy = publisher.get_iam_policy(topic_path)

    topic_policy.bindings.add(role="roles/pubsub.editor", members=["domain:google.com"])
    topic_policy.bindings.add(
        role="roles/pubsub.viewer", members=["group:cloud-logs@google.com"]
    )
    new_policy = publisher.set_iam_policy(topic_path, topic_policy)

    # fetch the topic policy again and check its values
    topic_policy = publisher.get_iam_policy(topic_path)
    assert topic_policy.bindings == new_policy.bindings
    assert len(topic_policy.bindings) == 2

    bindings = sorted(topic_policy.bindings, key=op.attrgetter("role"))
    assert bindings[0].role == "roles/pubsub.editor"
    assert bindings[0].members == ["domain:google.com"]

    assert bindings[1].role == "roles/pubsub.viewer"
    assert bindings[1].members == ["group:cloud-logs@google.com"]


def test_managing_subscription_iam_policy(
    publisher, subscriber, topic_path, subscription_path, cleanup
):
    # Make sure the topic and subscription get deleted.
    cleanup.append((publisher.delete_topic, topic_path))
    cleanup.append((subscriber.delete_subscription, subscription_path))

    # create a topic and a subscription, customize the latter's policy
    publisher.create_topic(topic_path)
    subscriber.create_subscription(subscription_path, topic_path)
    sub_policy = subscriber.get_iam_policy(subscription_path)

    sub_policy.bindings.add(role="roles/pubsub.editor", members=["domain:google.com"])
    sub_policy.bindings.add(
        role="roles/pubsub.viewer", members=["group:cloud-logs@google.com"]
    )
    new_policy = subscriber.set_iam_policy(subscription_path, sub_policy)

    # fetch the subscription policy again and check its values
    sub_policy = subscriber.get_iam_policy(subscription_path)
    assert sub_policy.bindings == new_policy.bindings
    assert len(sub_policy.bindings) == 2

    bindings = sorted(sub_policy.bindings, key=op.attrgetter("role"))
    assert bindings[0].role == "roles/pubsub.editor"
    assert bindings[0].members == ["domain:google.com"]

    assert bindings[1].role == "roles/pubsub.viewer"
    assert bindings[1].members == ["group:cloud-logs@google.com"]


class TestStreamingPull(object):
    def test_streaming_pull_callback_error_propagation(
        self, publisher, topic_path, subscriber, subscription_path, cleanup
    ):
        # Make sure the topic and subscription get deleted.
        cleanup.append((publisher.delete_topic, topic_path))
        cleanup.append((subscriber.delete_subscription, subscription_path))

        # create a topic and subscribe to it
        publisher.create_topic(topic_path)
        subscriber.create_subscription(subscription_path, topic_path)

        # publish a messages and wait until published
        future = publisher.publish(topic_path, b"hello!")
        future.result(timeout=30)

        # Now subscribe to the topic and verify that an error in the callback
        # is propagated through the streaming pull future.
        class CallbackError(Exception):
            pass

        callback = mock.Mock(side_effect=CallbackError)
        future = subscriber.subscribe(subscription_path, callback)

        with pytest.raises(CallbackError):
            future.result(timeout=30)

    def test_streaming_pull_max_messages(
        self, publisher, topic_path, subscriber, subscription_path, cleanup
    ):
        # Make sure the topic and subscription get deleted.
        cleanup.append((publisher.delete_topic, topic_path))
        cleanup.append((subscriber.delete_subscription, subscription_path))

        # create a topic and subscribe to it
        publisher.create_topic(topic_path)
        subscriber.create_subscription(subscription_path, topic_path)

        batch_sizes = (7, 4, 8, 2, 10, 1, 3, 8, 6, 1)  # total: 50
        self._publish_messages(publisher, topic_path, batch_sizes=batch_sizes)

        # now subscribe and do the main part, check for max pending messages
        total_messages = sum(batch_sizes)
        flow_control = types.FlowControl(max_messages=5)
        callback = StreamingPullCallback(
            processing_time=1, resolve_at_msg_count=total_messages
        )

        subscription_future = subscriber.subscribe(
            subscription_path, callback, flow_control=flow_control
        )

        # Expected time to process all messages in ideal case:
        #     (total_messages / FlowControl.max_messages) * processing_time
        #
        # With total=50, max messages=5, and processing_time=1 this amounts to
        # 10 seconds (+ overhead), thus a full minute should be more than enough
        # for the processing to complete. If not, fail the test with a timeout.
        try:
            callback.done_future.result(timeout=60)
        except exceptions.TimeoutError:
            pytest.fail(
                "Timeout: receiving/processing streamed messages took too long."
            )

        # The callback future gets resolved once total_messages have been processed,
        # but we want to wait for just a little bit longer to possibly catch cases
        # when the callback gets invoked *more* than total_messages times.
        time.sleep(3)

        try:
            # All messages should have been processed exactly once, and no more
            # than max_messages simultaneously at any time.
            assert callback.completed_calls == total_messages
            assert sorted(callback.seen_message_ids) == list(
                range(1, total_messages + 1)
            )
            assert callback.max_pending_ack <= flow_control.max_messages
        finally:
            subscription_future.cancel()  # trigger clean shutdown

    def _publish_messages(self, publisher, topic_path, batch_sizes):
        """Publish ``count`` messages in batches and wait until completion."""
        publish_futures = []
        msg_counter = itertools.count(start=1)

        for batch_size in batch_sizes:
            msg_batch = self._make_messages(count=batch_size)
            for msg in msg_batch:
                future = publisher.publish(
                    topic_path, msg, seq_num=str(next(msg_counter))
                )
                publish_futures.append(future)
            time.sleep(0.1)

        # wait untill all messages have been successfully published
        for future in publish_futures:
            future.result(timeout=30)

    def _make_messages(self, count):
        messages = [
            u"message {}/{}".format(i, count).encode("utf-8")
            for i in range(1, count + 1)
        ]
        return messages


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


class StreamingPullCallback(object):
    def __init__(self, processing_time, resolve_at_msg_count):
        self._lock = threading.Lock()
        self._processing_time = processing_time
        self._pending_ack = 0
        self.max_pending_ack = 0
        self.completed_calls = 0
        self.seen_message_ids = []

        self._resolve_at_msg_count = resolve_at_msg_count
        self.done_future = futures.Future()

    def __call__(self, message):
        with self._lock:
            self._pending_ack += 1
            self.max_pending_ack = max(self.max_pending_ack, self._pending_ack)
            self.seen_message_ids.append(int(message.attributes["seq_num"]))

        time.sleep(self._processing_time)

        with self._lock:
            self._pending_ack -= 1
            message.ack()
            self.completed_calls += 1

            if self.completed_calls >= self._resolve_at_msg_count:
                if not self.done_future.done():
                    self.done_future.set_result(None)
