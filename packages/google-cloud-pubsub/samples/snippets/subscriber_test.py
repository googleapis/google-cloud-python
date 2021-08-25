# Copyright 2016 Google Inc. All Rights Reserved.
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

import os
import re
import sys
import time
from typing import Generator
import uuid

from _pytest.capture import CaptureFixture
import backoff
from flaky import flaky
from google.api_core.exceptions import InternalServerError
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import Unknown
from google.cloud import pubsub_v1
import pytest

import subscriber

UUID = uuid.uuid4().hex
PY_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TOPIC = f"subscription-test-topic-{PY_VERSION}-{UUID}"
DEAD_LETTER_TOPIC = f"subscription-test-dead-letter-topic-{PY_VERSION}-{UUID}"
SUBSCRIPTION_ADMIN = f"subscription-test-subscription-admin-{PY_VERSION}-{UUID}"
SUBSCRIPTION_ASYNC = f"subscription-test-subscription-async-{PY_VERSION}-{UUID}"
SUBSCRIPTION_SYNC = f"subscription-test-subscription-sync-{PY_VERSION}-{UUID}"
SUBSCRIPTION_DLQ = f"subscription-test-subscription-dlq-{PY_VERSION}-{UUID}"
ENDPOINT = f"https://{PROJECT_ID}.appspot.com/push"
NEW_ENDPOINT = f"https://{PROJECT_ID}.appspot.com/push2"
DEFAULT_MAX_DELIVERY_ATTEMPTS = 5
UPDATED_MAX_DELIVERY_ATTEMPTS = 20


@pytest.fixture(scope="module")
def publisher_client() -> Generator[pubsub_v1.PublisherClient, None, None]:
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def topic(publisher_client: pubsub_v1.PublisherClient) -> Generator[str, None, None]:
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC)

    try:
        topic = publisher_client.get_topic(request={"topic": topic_path})
    except:  # noqa
        topic = publisher_client.create_topic(request={"name": topic_path})

    yield topic.name

    publisher_client.delete_topic(request={"topic": topic.name})


@pytest.fixture(scope="module")
def dead_letter_topic(
    publisher_client: pubsub_v1.PublisherClient,
) -> Generator[str, None, None]:
    topic_path = publisher_client.topic_path(PROJECT_ID, DEAD_LETTER_TOPIC)

    try:
        dead_letter_topic = publisher_client.get_topic(request={"topic": topic_path})
    except NotFound:
        dead_letter_topic = publisher_client.create_topic(request={"name": topic_path})

    yield dead_letter_topic.name

    publisher_client.delete_topic(request={"topic": dead_letter_topic.name})


@pytest.fixture(scope="module")
def subscriber_client() -> Generator[pubsub_v1.SubscriberClient, None, None]:
    subscriber_client = pubsub_v1.SubscriberClient()
    yield subscriber_client
    subscriber_client.close()


@pytest.fixture(scope="module")
def subscription_admin(
    subscriber_client: pubsub_v1.SubscriberClient, topic: str
) -> Generator[str, None, None]:
    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, SUBSCRIPTION_ADMIN
    )

    try:
        subscription = subscriber_client.get_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        subscription = subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    yield subscription.name


@pytest.fixture(scope="module")
def subscription_sync(
    subscriber_client: pubsub_v1.SubscriberClient, topic: str
) -> Generator[str, None, None]:
    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, SUBSCRIPTION_SYNC
    )

    try:
        subscription = subscriber_client.get_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        subscription = subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    yield subscription.name

    @backoff.on_exception(backoff.expo, Unknown, max_time=300)
    def delete_subscription() -> None:
        try:
            subscriber_client.delete_subscription(
                request={"subscription": subscription.name}
            )
        except NotFound:
            print(
                "When Unknown error happens, the server might have"
                " successfully deleted the subscription under the cover, so"
                " we ignore NotFound"
            )

    delete_subscription()


@pytest.fixture(scope="module")
def subscription_async(
    subscriber_client: pubsub_v1.SubscriberClient, topic: str
) -> Generator[str, None, None]:
    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, SUBSCRIPTION_ASYNC
    )

    try:
        subscription = subscriber_client.get_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        subscription = subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    yield subscription.name

    subscriber_client.delete_subscription(request={"subscription": subscription.name})


@pytest.fixture(scope="module")
def subscription_dlq(
    subscriber_client: pubsub_v1.SubscriberClient, topic: str, dead_letter_topic: str
) -> Generator[str, None, None]:
    from google.cloud.pubsub_v1.types import DeadLetterPolicy

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, SUBSCRIPTION_DLQ
    )

    try:
        subscription = subscriber_client.get_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        request = {
            "name": subscription_path,
            "topic": topic,
            "dead_letter_policy": DeadLetterPolicy(
                dead_letter_topic=dead_letter_topic, max_delivery_attempts=10
            ),
        }
        subscription = subscriber_client.create_subscription(request)

    yield subscription.name

    subscriber_client.delete_subscription(request={"subscription": subscription.name})


def _publish_messages(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    message_num: int = 5,
    **attrs: dict,
) -> None:
    for n in range(message_num):
        data = f"message {n}".encode("utf-8")
        publish_future = publisher_client.publish(topic, data, **attrs)
        publish_future.result()


def test_list_in_topic(subscription_admin: str, capsys: CaptureFixture) -> None:
    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def eventually_consistent_test() -> None:
        subscriber.list_subscriptions_in_topic(PROJECT_ID, TOPIC)
        out, _ = capsys.readouterr()
        assert subscription_admin in out

    eventually_consistent_test()


def test_list_in_project(subscription_admin: str, capsys: CaptureFixture) -> None:
    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def eventually_consistent_test() -> None:
        subscriber.list_subscriptions_in_project(PROJECT_ID)
        out, _ = capsys.readouterr()
        assert subscription_admin in out

    eventually_consistent_test()


def test_create(
    subscriber_client: pubsub_v1.SubscriberClient,
    subscription_admin: str,
    capsys: CaptureFixture,
) -> None:
    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, SUBSCRIPTION_ADMIN
    )

    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription(PROJECT_ID, TOPIC, SUBSCRIPTION_ADMIN)

    out, _ = capsys.readouterr()
    assert f"{subscription_admin}" in out


def test_create_subscription_with_dead_letter_policy(
    subscriber_client: pubsub_v1.SubscriberClient,
    subscription_dlq: str,
    dead_letter_topic: str,
    capsys: CaptureFixture,
) -> None:
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_dlq}
        )
    except NotFound:
        pass

    subscriber.create_subscription_with_dead_letter_topic(
        PROJECT_ID, TOPIC, SUBSCRIPTION_DLQ, DEAD_LETTER_TOPIC
    )

    out, _ = capsys.readouterr()
    assert f"Subscription created: {subscription_dlq}" in out
    assert f"It will forward dead letter messages to: {dead_letter_topic}" in out
    assert f"After {DEFAULT_MAX_DELIVERY_ATTEMPTS} delivery attempts." in out


@flaky(max_runs=3, min_passes=1)
def test_receive_with_delivery_attempts(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    dead_letter_topic: str,
    subscription_dlq: str,
    capsys: CaptureFixture,
) -> None:

    # The dlq subscription raises 404 before it's ready.
    # We keep retrying up to 10 minutes for mitigating the flakiness.
    @backoff.on_exception(backoff.expo, (Unknown, NotFound), max_time=120)
    def run_sample() -> None:
        _publish_messages(publisher_client, topic)

        subscriber.receive_messages_with_delivery_attempts(
            PROJECT_ID, SUBSCRIPTION_DLQ, 90
        )

    run_sample()

    out, _ = capsys.readouterr()
    assert f"Listening for messages on {subscription_dlq}.." in out
    assert "With delivery attempts: " in out


@flaky(max_runs=3, min_passes=1)
def test_update_dead_letter_policy(
    subscription_dlq: str, dead_letter_topic: str, capsys: CaptureFixture
) -> None:

    # We saw internal server error that suggests to retry.

    @backoff.on_exception(backoff.expo, (Unknown, InternalServerError), max_time=60)
    def run_sample() -> None:
        subscriber.update_subscription_with_dead_letter_policy(
            PROJECT_ID,
            TOPIC,
            SUBSCRIPTION_DLQ,
            DEAD_LETTER_TOPIC,
            UPDATED_MAX_DELIVERY_ATTEMPTS,
        )

    run_sample()

    out, _ = capsys.readouterr()
    assert dead_letter_topic in out
    assert subscription_dlq in out
    assert f"max_delivery_attempts: {UPDATED_MAX_DELIVERY_ATTEMPTS}" in out


@flaky(max_runs=3, min_passes=1)
def test_remove_dead_letter_policy(
    subscription_dlq: str, capsys: CaptureFixture
) -> None:
    subscription_after_update = subscriber.remove_dead_letter_policy(
        PROJECT_ID, TOPIC, SUBSCRIPTION_DLQ
    )

    out, _ = capsys.readouterr()
    assert subscription_dlq in out
    assert subscription_after_update.dead_letter_policy.dead_letter_topic == ""


def test_create_subscription_with_ordering(
    subscriber_client: pubsub_v1.SubscriberClient,
    subscription_admin: str,
    capsys: CaptureFixture,
) -> None:
    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, SUBSCRIPTION_ADMIN
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription_with_ordering(PROJECT_ID, TOPIC, SUBSCRIPTION_ADMIN)

    out, _ = capsys.readouterr()
    assert "Created subscription with ordering" in out
    assert f"{subscription_admin}" in out
    assert "enable_message_ordering: true" in out


def test_create_push(
    subscriber_client: pubsub_v1.SubscriberClient,
    subscription_admin: str,
    capsys: CaptureFixture,
) -> None:
    # The scope of `subscription_path` is limited to this function.
    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, SUBSCRIPTION_ADMIN
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_push_subscription(PROJECT_ID, TOPIC, SUBSCRIPTION_ADMIN, ENDPOINT)

    out, _ = capsys.readouterr()
    assert f"{subscription_admin}" in out


def test_update(subscription_admin: str, capsys: CaptureFixture) -> None:
    subscriber.update_push_subscription(
        PROJECT_ID, TOPIC, SUBSCRIPTION_ADMIN, NEW_ENDPOINT
    )

    out, _ = capsys.readouterr()
    assert "Subscription updated" in out
    assert f"{subscription_admin}" in out


def test_delete(
    subscriber_client: pubsub_v1.SubscriberClient, subscription_admin: str
) -> None:
    subscriber.delete_subscription(PROJECT_ID, SUBSCRIPTION_ADMIN)

    @backoff.on_exception(backoff.expo, AssertionError, max_time=60)
    def eventually_consistent_test() -> None:
        with pytest.raises(Exception):
            subscriber_client.get_subscription(
                request={"subscription": subscription_admin}
            )

    eventually_consistent_test()


def test_receive(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    subscription_async: str,
    capsys: CaptureFixture,
) -> None:
    _publish_messages(publisher_client, topic)

    subscriber.receive_messages(PROJECT_ID, SUBSCRIPTION_ASYNC, 5)

    out, _ = capsys.readouterr()
    assert "Listening" in out
    assert subscription_async in out
    assert "message" in out


def test_receive_with_custom_attributes(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    subscription_async: str,
    capsys: CaptureFixture,
) -> None:

    _publish_messages(publisher_client, topic, origin="python-sample")

    subscriber.receive_messages_with_custom_attributes(
        PROJECT_ID, SUBSCRIPTION_ASYNC, 5
    )

    out, _ = capsys.readouterr()
    assert subscription_async in out
    assert "message" in out
    assert "origin" in out
    assert "python-sample" in out


def test_receive_with_flow_control(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    subscription_async: str,
    capsys: CaptureFixture,
) -> None:

    _publish_messages(publisher_client, topic)

    subscriber.receive_messages_with_flow_control(PROJECT_ID, SUBSCRIPTION_ASYNC, 5)

    out, _ = capsys.readouterr()
    assert "Listening" in out
    assert subscription_async in out
    assert "message" in out


def test_receive_with_blocking_shutdown(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    subscription_async: str,
    capsys: CaptureFixture,
) -> None:
    _publish_messages(publisher_client, topic, message_num=3)

    subscriber.receive_messages_with_blocking_shutdown(
        PROJECT_ID, SUBSCRIPTION_ASYNC, timeout=5.0
    )

    out, _ = capsys.readouterr()
    out_lines = out.splitlines()

    msg_received_lines = [
        i
        for i, line in enumerate(out_lines)
        if re.search(r".*received.*message.*", line, flags=re.IGNORECASE)
    ]
    msg_done_lines = [
        i
        for i, line in enumerate(out_lines)
        if re.search(r".*done processing.*message.*", line, flags=re.IGNORECASE)
    ]
    stream_canceled_lines = [
        i
        for i, line in enumerate(out_lines)
        if re.search(r".*streaming pull future canceled.*", line, flags=re.IGNORECASE)
    ]
    shutdown_done_waiting_lines = [
        i
        for i, line in enumerate(out_lines)
        if re.search(r".*done waiting.*stream shutdown.*", line, flags=re.IGNORECASE)
    ]

    try:
        assert "Listening" in out
        assert subscription_async in out

        assert len(stream_canceled_lines) == 1
        assert len(shutdown_done_waiting_lines) == 1
        assert len(msg_received_lines) == 3
        assert len(msg_done_lines) == 3

        # The stream should have been canceled *after* receiving messages, but before
        # message processing was done.
        assert msg_received_lines[-1] < stream_canceled_lines[0] < msg_done_lines[0]

        # Yet, waiting on the stream shutdown should have completed *after*
        # the processing of received messages has ended.
        assert msg_done_lines[-1] < shutdown_done_waiting_lines[0]
    except AssertionError:  # pragma: NO COVER
        from pprint import pprint

        pprint(out_lines)  # To make possible flakiness debugging easier.
        raise


def test_listen_for_errors(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    subscription_async: str,
    capsys: CaptureFixture,
) -> None:

    _publish_messages(publisher_client, topic)

    subscriber.listen_for_errors(PROJECT_ID, SUBSCRIPTION_ASYNC, 5)

    out, _ = capsys.readouterr()
    assert subscription_async in out
    assert "threw an exception" in out


def test_receive_synchronously(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    subscription_sync: str,
    capsys: CaptureFixture,
) -> None:
    _publish_messages(publisher_client, topic)

    subscriber.synchronous_pull(PROJECT_ID, SUBSCRIPTION_SYNC)

    out, _ = capsys.readouterr()

    assert "Received" in out
    assert f"{subscription_sync}" in out


@flaky(max_runs=3, min_passes=1)
def test_receive_synchronously_with_lease(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    subscription_sync: str,
    capsys: CaptureFixture,
) -> None:
    @backoff.on_exception(backoff.expo, Unknown, max_time=300)
    def run_sample() -> None:
        _publish_messages(publisher_client, topic, message_num=10)
        # Pausing 10s to allow the subscriber to establish the connection
        # because sync pull often returns fewer messages than requested.
        # The intention is to fix flaky tests reporting errors like
        # `google.api_core.exceptions.Unknown: None Stream removed` as
        # in https://github.com/googleapis/python-pubsub/issues/341.
        time.sleep(10)
        subscriber.synchronous_pull_with_lease_management(PROJECT_ID, SUBSCRIPTION_SYNC)

    run_sample()

    out, _ = capsys.readouterr()

    # Sometimes the subscriber only gets 1 or 2 messages and test fails.
    # I think it's ok to consider those cases as passing.
    assert "Received and acknowledged" in out
    assert f"messages from {subscription_sync}." in out
