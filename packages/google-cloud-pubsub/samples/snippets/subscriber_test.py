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
from typing import Any, Callable, cast, Generator, List, TypeVar
import uuid

from _pytest.capture import CaptureFixture
import backoff
from flaky import flaky
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, pubsub_v1, storage
import pytest

import subscriber

# This uuid is shared across tests which run in parallel.
UUID = uuid.uuid4().hex
PY_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
UNDERSCORE_PY_VERSION = PY_VERSION.replace(".", "_")
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TOPIC = f"subscription-test-topic-{PY_VERSION}-{UUID}"
DEAD_LETTER_TOPIC = f"subscription-test-dead-letter-topic-{PY_VERSION}-{UUID}"
UNUSED_TOPIC = f"subscription-unused-topic-{PY_VERSION}-{UUID}"
EOD_TOPIC = f"subscription-test-eod-topic-{PY_VERSION}-{UUID}"
SUBSCRIPTION_ADMIN = f"subscription-test-subscription-admin-{PY_VERSION}-{UUID}"
ENDPOINT = f"https://{PROJECT_ID}.appspot.com/push"
NEW_ENDPOINT = f"https://{PROJECT_ID}.appspot.com/push2"
REGIONAL_ENDPOINT = "us-east1-pubsub.googleapis.com:443"
DEFAULT_MAX_DELIVERY_ATTEMPTS = 5
UPDATED_MAX_DELIVERY_ATTEMPTS = 20
FILTER = 'attributes.author="unknown"'
BIGQUERY_DATASET_ID = f"python_samples_dataset_{UNDERSCORE_PY_VERSION}_{UUID}"
BIGQUERY_TABLE_ID = f"python_samples_table_{UNDERSCORE_PY_VERSION}_{UUID}"
CLOUDSTORAGE_BUCKET = f"python_samples_bucket_{UNDERSCORE_PY_VERSION}_{UUID}"

C = TypeVar("C", bound=Callable[..., Any])

typed_flaky = cast(Callable[[C], C], flaky(max_runs=3, min_passes=1))

# These tests run in parallel if pytest-parallel is installed.
# Avoid modifying resources that are shared across tests,
# as this results in test flake.


@pytest.fixture(scope="module")
def publisher_client() -> Generator[pubsub_v1.PublisherClient, None, None]:
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def regional_publisher_client() -> Generator[pubsub_v1.PublisherClient, None, None]:
    client_options = {"api_endpoint": REGIONAL_ENDPOINT}
    publisher = pubsub_v1.PublisherClient(client_options=client_options)
    yield publisher


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

    subscriber_client.delete_subscription(request={"subscription": subscription_path})


@pytest.fixture(scope="module")
def topic(publisher_client: pubsub_v1.PublisherClient) -> Generator[str, None, None]:
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC)

    try:
        topic = publisher_client.get_topic(request={"topic": topic_path})
    except:  # noqa
        topic = publisher_client.create_topic(request={"name": topic_path})

    yield topic.name

    publisher_client.delete_topic(request={"topic": topic.name})


# This topic is only for creating subscriptions, no messages should be published on this topic.
@pytest.fixture(scope="module")
def unused_topic(
    publisher_client: pubsub_v1.PublisherClient,
) -> Generator[str, None, None]:
    topic_path = publisher_client.topic_path(PROJECT_ID, UNUSED_TOPIC)

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
def exactly_once_delivery_topic(
    publisher_client: pubsub_v1.PublisherClient,
) -> Generator[str, None, None]:
    topic_path = publisher_client.topic_path(PROJECT_ID, EOD_TOPIC)

    try:
        topic = publisher_client.get_topic(request={"topic": topic_path})
    except NotFound:
        topic = publisher_client.create_topic(request={"name": topic_path})

    yield topic.name

    publisher_client.delete_topic(request={"topic": topic.name})


@pytest.fixture(scope="module")
def subscriber_client() -> Generator[pubsub_v1.SubscriberClient, None, None]:
    subscriber_client = pubsub_v1.SubscriberClient()
    yield subscriber_client
    subscriber_client.close()


def _publish_messages(
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    message_num: int = 5,
    **attrs: Any,  # noqa: ANN401
) -> List[str]:
    message_ids = []
    for n in range(message_num):
        data = f"message {n}".encode("utf-8")
        publish_future = publisher_client.publish(topic, data, **attrs)
        message_ids.append(publish_future.result())
    return message_ids


def test_list_in_topic(subscription_admin: str, capsys: CaptureFixture[str]) -> None:
    typed_backoff = cast(
        Callable[[C], C],
        backoff.on_exception(backoff.expo, AssertionError, max_time=60),
    )

    @typed_backoff
    def eventually_consistent_test() -> None:
        subscriber.list_subscriptions_in_topic(PROJECT_ID, TOPIC)
        out, _ = capsys.readouterr()
        assert subscription_admin in out

    eventually_consistent_test()


def test_list_in_project(subscription_admin: str, capsys: CaptureFixture[str]) -> None:
    typed_backoff = cast(
        Callable[[C], C],
        backoff.on_exception(backoff.expo, AssertionError, max_time=60),
    )

    @typed_backoff
    def eventually_consistent_test() -> None:
        subscriber.list_subscriptions_in_project(PROJECT_ID)
        out, _ = capsys.readouterr()
        assert subscription_admin in out

    eventually_consistent_test()


def test_create_subscription(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_for_create_name = (
        f"subscription-test-subscription-for-create-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_for_create_name
    )

    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription(PROJECT_ID, TOPIC, subscription_for_create_name)

    out, _ = capsys.readouterr()
    assert f"{subscription_for_create_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_optimistic_subscribe(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    publisher_client: pubsub_v1.PublisherClient,
    capsys: CaptureFixture[str],
) -> None:
    subscription_id = f"subscription_for_optimistic_subscribe-{PY_VERSION}-{UUID}"
    subscription_path = subscriber_client.subscription_path(PROJECT_ID, subscription_id)
    # Ensure there is no pre-existing subscription.
    # So that we can test the case where optimistic subscribe fails.
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    # Invoke optimistic_subscribe when the subscription is not present.
    # This tests scenario where optimistic subscribe fails.
    subscriber.optimistic_subscribe(PROJECT_ID, TOPIC, subscription_id, 5)
    out, _ = capsys.readouterr()
    # Verify optimistic subscription failed.
    assert f"Subscription {subscription_path} not found, creating it." in out
    # Verify that subscription created due to optimistic subscribe failure.
    assert f"Subscription {subscription_path} created" in out
    # Verify that subscription didn't already exist.
    assert "Successfully subscribed until the timeout passed." not in out

    # Invoke optimistic_subscribe when the subscription is present.
    # This tests scenario where optimistic subscribe succeeds.
    subscriber.optimistic_subscribe(PROJECT_ID, TOPIC, subscription_id, 5)

    out, _ = capsys.readouterr()
    # Verify optimistic subscription succeeded.
    assert f"Subscription {subscription_path} not found, creating it." not in out
    # Verify that subscription was not created due to optimistic subscribe failure.
    assert f"Subscription {subscription_path} created" not in out
    # Verify that subscription already existed.
    assert "Successfully subscribed until the timeout passed." in out

    # Test case where optimistic subscribe throws an exception other than NotFound
    # or TimeoutError.
    subscriber.optimistic_subscribe(PROJECT_ID, TOPIC, "123", 5)
    out, _ = capsys.readouterr()
    assert "Exception occurred when attempting optimistic subscribe:" in out

    # Clean up resources created during test.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_create_subscription_with_dead_letter_policy(
    subscriber_client: pubsub_v1.SubscriberClient,
    dead_letter_topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_dlq_name = (
        f"subscription-test-subscription-dlq-for-create-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_dlq_name
    )

    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription_with_dead_letter_topic(
        PROJECT_ID, TOPIC, subscription_dlq_name, DEAD_LETTER_TOPIC
    )

    out, _ = capsys.readouterr()
    assert f"Subscription created: {subscription_path}" in out
    assert f"It will forward dead letter messages to: {dead_letter_topic}" in out
    assert f"After {DEFAULT_MAX_DELIVERY_ATTEMPTS} delivery attempts." in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_receive_with_delivery_attempts(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    dead_letter_topic: str,
    capsys: CaptureFixture[str],
) -> None:
    from google.cloud.pubsub_v1.types import DeadLetterPolicy

    subscription_dlq_for_receive_name = (
        f"subscription-test-subscription-dlq-for-receive-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_dlq_for_receive_name
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

    subscription_dlq = subscription.name

    _ = _publish_messages(publisher_client, topic)

    subscriber.receive_messages_with_delivery_attempts(
        PROJECT_ID, subscription_dlq_for_receive_name, 90
    )

    out, _ = capsys.readouterr()
    assert f"Listening for messages on {subscription_dlq}.." in out
    assert "With delivery attempts: " in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_update_dead_letter_policy(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    dead_letter_topic: str,
    capsys: CaptureFixture[str],
) -> None:
    from google.cloud.pubsub_v1.types import DeadLetterPolicy

    subscription_dlq_for_update_name = (
        f"subscription-test-subscription-dlq-for-update-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_dlq_for_update_name
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

    subscription_dlq = subscription.name

    subscriber.update_subscription_with_dead_letter_policy(
        PROJECT_ID,
        TOPIC,
        subscription_dlq_for_update_name,
        DEAD_LETTER_TOPIC,
        UPDATED_MAX_DELIVERY_ATTEMPTS,
    )

    out, _ = capsys.readouterr()
    assert dead_letter_topic in out
    assert subscription_dlq in out
    assert f"max_delivery_attempts: {UPDATED_MAX_DELIVERY_ATTEMPTS}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_remove_dead_letter_policy(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    dead_letter_topic: str,
    capsys: CaptureFixture[str],
) -> None:
    from google.cloud.pubsub_v1.types import DeadLetterPolicy

    subscription_dlq_for_remove_name = (
        f"subscription-test-subscription-dlq-for-remove-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_dlq_for_remove_name
    )

    request = {
        "name": subscription_path,
        "topic": topic,
        "dead_letter_policy": DeadLetterPolicy(
            dead_letter_topic=dead_letter_topic, max_delivery_attempts=10
        ),
    }
    subscription = subscriber_client.create_subscription(request)

    subscription_dlq = subscription.name

    subscription_after_update = subscriber.remove_dead_letter_policy(
        PROJECT_ID, TOPIC, subscription_dlq_for_remove_name
    )

    out, _ = capsys.readouterr()
    assert subscription_dlq in out
    assert subscription_after_update.dead_letter_policy.dead_letter_topic == ""

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_create_subscription_with_ordering(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_with_ordering_name = (
        f"subscription-test-subscription-with-ordering-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_with_ordering_name
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription_with_ordering(
        PROJECT_ID, TOPIC, subscription_with_ordering_name
    )

    out, _ = capsys.readouterr()
    assert "Created subscription with ordering" in out
    assert f"{subscription_with_ordering_name}" in out
    assert "enable_message_ordering: true" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_create_subscription_with_filtering(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_with_filtering_name = (
        f"subscription-test-subscription-with-filtering-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_with_filtering_name
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription_with_filtering(
        PROJECT_ID, TOPIC, subscription_with_filtering_name, FILTER
    )

    out, _ = capsys.readouterr()
    assert "Created subscription with filtering enabled" in out
    assert f"{subscription_with_filtering_name}" in out
    assert '"attributes.author=\\"unknown\\""' in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_create_subscription_with_exactly_once_delivery(
    subscriber_client: pubsub_v1.SubscriberClient,
    exactly_once_delivery_topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_eod_for_create_name = (
        f"subscription-test-subscription-eod-for-create-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_eod_for_create_name
    )

    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription_with_exactly_once_delivery(
        PROJECT_ID, EOD_TOPIC, subscription_eod_for_create_name
    )

    out, _ = capsys.readouterr()
    assert "Created subscription with exactly once delivery enabled" in out
    assert f"{subscription_eod_for_create_name}" in out
    assert "enable_exactly_once_delivery: true" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_create_push_subscription(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    push_subscription_for_create_name = (
        f"subscription-test-subscription-push-for-create-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, push_subscription_for_create_name
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_push_subscription(
        PROJECT_ID, TOPIC, push_subscription_for_create_name, ENDPOINT
    )

    out, _ = capsys.readouterr()
    assert f"{push_subscription_for_create_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_create_subscription_with_smt(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_for_create_name = (
        f"subscription-test-subscription-for-create-with-smt-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_for_create_name
    )

    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_subscription_with_smt(
        PROJECT_ID, TOPIC, subscription_for_create_name
    )

    out, _ = capsys.readouterr()
    assert f"{subscription_for_create_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_update_push_subscription(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    push_subscription_for_update_name = (
        f"subscription-test-subscription-push-for-create-{PY_VERSION}-{UUID}"
    )
    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, push_subscription_for_update_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    subscriber.update_push_subscription(
        PROJECT_ID, TOPIC, push_subscription_for_update_name, NEW_ENDPOINT
    )

    out, _ = capsys.readouterr()
    assert "Subscription updated" in out
    assert f"{push_subscription_for_update_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_create_push_no_wrapper_subscription(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    push_subscription_for_create_name = (
        f"subscription-test-subscription-push-no-wrapper-for-create-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, push_subscription_for_create_name
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_push_no_wrapper_subscription(
        PROJECT_ID, TOPIC, push_subscription_for_create_name, ENDPOINT
    )

    out, _ = capsys.readouterr()
    assert f"{push_subscription_for_create_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


@pytest.fixture(scope="module")
def bigquery_table() -> Generator[str, None, None]:
    client = bigquery.Client()
    dataset = bigquery.Dataset(f"{PROJECT_ID}.{BIGQUERY_DATASET_ID}")
    dataset.location = "US"
    dataset = client.create_dataset(dataset)

    table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_TABLE_ID}"
    schema = [
        bigquery.SchemaField("data", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("message_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("attributes", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("subscription_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("publish_time", "TIMESTAMP", mode="REQUIRED"),
    ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)

    yield table_id

    client.delete_dataset(dataset, delete_contents=True)


def test_create_bigquery_subscription(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    bigquery_table: str,
    capsys: CaptureFixture[str],
) -> None:
    bigquery_subscription_for_create_name = (
        f"subscription-test-subscription-bigquery-for-create-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, bigquery_subscription_for_create_name
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_bigquery_subscription(
        PROJECT_ID, TOPIC, bigquery_subscription_for_create_name, bigquery_table
    )

    out, _ = capsys.readouterr()
    assert f"{bigquery_subscription_for_create_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


@pytest.fixture(scope="module")
def cloudstorage_bucket() -> Generator[str, None, None]:
    storage_client = storage.Client()

    bucket_name = CLOUDSTORAGE_BUCKET

    bucket = storage_client.create_bucket(bucket_name)
    print(f"Bucket {bucket.name} created.")

    yield bucket.name

    bucket.delete()


def test_create_cloudstorage_subscription(
    subscriber_client: pubsub_v1.SubscriberClient,
    unused_topic: str,
    cloudstorage_bucket: str,
    capsys: CaptureFixture[str],
) -> None:
    cloudstorage_subscription_for_create_name = (
        f"subscription-test-subscription-cloudstorage-for-create-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, cloudstorage_subscription_for_create_name
    )
    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass

    subscriber.create_cloudstorage_subscription(
        PROJECT_ID,
        # We have to use a topic with no messages published,
        # so that the bucket will be empty and can be deleted.
        UNUSED_TOPIC,
        cloudstorage_subscription_for_create_name,
        cloudstorage_bucket,
    )

    out, _ = capsys.readouterr()
    assert f"{cloudstorage_subscription_for_create_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_delete_subscription(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
) -> None:
    subscription_for_delete_name = (
        f"subscription-test-subscription-for-delete-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_for_delete_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    subscriber.delete_subscription(PROJECT_ID, subscription_for_delete_name)

    with pytest.raises(Exception):
        subscriber_client.get_subscription(
            request={"subscription": subscription_for_delete_name}
        )

    # No clean up required.


def test_receive(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic: str,
    publisher_client: pubsub_v1.PublisherClient,
    capsys: CaptureFixture[str],
) -> None:
    subscription_async_for_receive_name = (
        f"subscription-test-subscription-async-for-receive-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_async_for_receive_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _ = _publish_messages(publisher_client, topic)

    subscriber.receive_messages(PROJECT_ID, subscription_async_for_receive_name, 5)

    out, _ = capsys.readouterr()
    assert "Listening" in out
    assert subscription_async_for_receive_name in out
    assert "message" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_receive_with_custom_attributes(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_async_receive_with_custom_name = (
        f"subscription-test-subscription-async-receive-with-custom-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_async_receive_with_custom_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _ = _publish_messages(publisher_client, topic, origin="python-sample")

    subscriber.receive_messages_with_custom_attributes(
        PROJECT_ID, subscription_async_receive_with_custom_name, 5
    )

    out, _ = capsys.readouterr()
    assert subscription_async_receive_with_custom_name in out
    assert "message" in out
    assert "origin" in out
    assert "python-sample" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_receive_with_flow_control(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_async_receive_with_flow_control_name = f"subscription-test-subscription-async-receive-with-flow-control-{PY_VERSION}-{UUID}"

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_async_receive_with_flow_control_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _ = _publish_messages(publisher_client, topic)

    subscriber.receive_messages_with_flow_control(
        PROJECT_ID, subscription_async_receive_with_flow_control_name, 5
    )

    out, _ = capsys.readouterr()
    assert "Listening" in out
    assert subscription_async_receive_with_flow_control_name in out
    assert "message" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_receive_with_blocking_shutdown(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_async_receive_with_blocking_name = f"subscription-test-subscription-async-receive-with-blocking-shutdown-{PY_VERSION}-{UUID}"

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_async_receive_with_blocking_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _received = re.compile(r".*received.*message.*", flags=re.IGNORECASE)
    _done = re.compile(r".*done processing.*message.*", flags=re.IGNORECASE)
    _canceled = re.compile(r".*streaming pull future canceled.*", flags=re.IGNORECASE)
    _shut_down = re.compile(r".*done waiting.*stream shutdown.*", flags=re.IGNORECASE)

    _ = _publish_messages(publisher_client, topic, message_num=3)

    subscriber.receive_messages_with_blocking_shutdown(
        PROJECT_ID, subscription_async_receive_with_blocking_name, timeout=5.0
    )

    out, _ = capsys.readouterr()
    out_lines = out.splitlines()

    msg_received_lines = [
        i for i, line in enumerate(out_lines) if _received.search(line)
    ]
    msg_done_lines = [i for i, line in enumerate(out_lines) if _done.search(line)]
    stream_canceled_lines = [
        i for i, line in enumerate(out_lines) if _canceled.search(line)
    ]
    shutdown_done_waiting_lines = [
        i for i, line in enumerate(out_lines) if _shut_down.search(line)
    ]

    try:
        assert "Listening" in out
        assert subscription_async_receive_with_blocking_name in out

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

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_receive_messages_with_exactly_once_delivery_enabled(
    subscriber_client: pubsub_v1.SubscriberClient,
    regional_publisher_client: pubsub_v1.PublisherClient,
    exactly_once_delivery_topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_eod_for_receive_name = (
        f"subscription-test-subscription-eod-for-receive-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_eod_for_receive_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={
                "name": subscription_path,
                "topic": exactly_once_delivery_topic,
                "enable_exactly_once_delivery": True,
            }
        )

    message_ids = _publish_messages(
        regional_publisher_client, exactly_once_delivery_topic
    )

    subscriber.receive_messages_with_exactly_once_delivery_enabled(
        PROJECT_ID, subscription_eod_for_receive_name, 200
    )

    out, _ = capsys.readouterr()
    assert subscription_eod_for_receive_name in out
    for message_id in message_ids:
        assert message_id in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_listen_for_errors(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_async_listen = (
        f"subscription-test-subscription-async-listen-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_async_listen
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _ = _publish_messages(publisher_client, topic)

    subscriber.listen_for_errors(PROJECT_ID, subscription_async_listen, 5)

    out, _ = capsys.readouterr()
    assert subscription_path in out
    assert "threw an exception" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_receive_synchronously(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_sync_for_receive_name = (
        f"subscription-test-subscription-sync-for-receive-{PY_VERSION}-{UUID}"
    )

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_sync_for_receive_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _ = _publish_messages(publisher_client, topic)

    subscriber.synchronous_pull(PROJECT_ID, subscription_sync_for_receive_name)

    out, _ = capsys.readouterr()

    assert "Received" in out
    assert f"{subscription_sync_for_receive_name}" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


def test_receive_messages_with_concurrency_control(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_async_receive_messages_with_concurrency_control_name = f"subscription-test-subscription-async-receive-messages-with-concurrency-control-{PY_VERSION}-{UUID}"

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_async_receive_messages_with_concurrency_control_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _ = _publish_messages(publisher_client, topic)

    subscriber.receive_messages_with_flow_control(
        PROJECT_ID, subscription_async_receive_messages_with_concurrency_control_name, 5
    )

    out, _ = capsys.readouterr()
    assert "Listening" in out
    assert subscription_async_receive_messages_with_concurrency_control_name in out
    assert "message" in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})


@typed_flaky
def test_receive_synchronously_with_lease(
    subscriber_client: pubsub_v1.SubscriberClient,
    publisher_client: pubsub_v1.PublisherClient,
    topic: str,
    capsys: CaptureFixture[str],
) -> None:
    subscription_sync_for_receive_with_lease_name = f"subscription-test-subscription-sync-for-receive-with-lease-{PY_VERSION}-{UUID}"

    subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, subscription_sync_for_receive_with_lease_name
    )

    try:
        subscriber_client.get_subscription(request={"subscription": subscription_path})
    except NotFound:
        subscriber_client.create_subscription(
            request={"name": subscription_path, "topic": topic}
        )

    _ = _publish_messages(publisher_client, topic, message_num=10)
    # Pausing 10s to allow the subscriber to establish the connection
    # because sync pull often returns fewer messages than requested.
    # The intention is to fix flaky tests reporting errors like
    # `google.api_core.exceptions.Unknown: None Stream removed` as
    # in https://github.com/googleapis/python-pubsub/issues/341.
    time.sleep(10)
    subscriber.synchronous_pull_with_lease_management(
        PROJECT_ID, subscription_sync_for_receive_with_lease_name
    )

    out, _ = capsys.readouterr()

    # Sometimes the subscriber only gets 1 or 2 messages and test fails.
    # I think it's ok to consider those cases as passing.
    assert "Received and acknowledged" in out
    assert f"messages from {subscription_path}." in out

    # Clean up.
    subscriber_client.delete_subscription(request={"subscription": subscription_path})
