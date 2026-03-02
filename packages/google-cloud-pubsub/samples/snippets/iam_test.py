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
from typing import Generator
import uuid

from _pytest.capture import CaptureFixture
from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1
import pytest

import iam

UUID = uuid.uuid4().hex
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TOPIC_ID = "iam-test-topic-" + UUID
SUBSCRIPTION_ID = "iam-test-subscription-" + UUID


@pytest.fixture(scope="module")
def publisher_client() -> Generator[pubsub_v1.PublisherClient, None, None]:
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def topic_path(
    publisher_client: pubsub_v1.PublisherClient,
) -> Generator[str, None, None]:
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    try:
        topic = publisher_client.get_topic(request={"topic": topic_path})
    except NotFound:
        topic = publisher_client.create_topic(request={"name": topic_path})

    yield topic.name

    try:
        publisher_client.delete_topic(request={"topic": topic.name})
    except NotFound:
        pass


@pytest.fixture(scope="module")
def subscriber_client() -> Generator[pubsub_v1.SubscriberClient, None, None]:
    subscriber_client = pubsub_v1.SubscriberClient()
    yield subscriber_client
    subscriber_client.close()


@pytest.fixture(scope="module")
def subscription_path(
    subscriber_client: pubsub_v1.SubscriberClient,
    topic_path: str,
) -> Generator[str, None, None]:
    subscription_path = subscriber_client.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    subscription = subscriber_client.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )
    yield subscription.name

    try:
        subscriber_client.delete_subscription(
            request={"subscription": subscription_path}
        )
    except NotFound:
        pass


def test_get_topic_policy(topic_path: str, capsys: CaptureFixture[str]) -> None:
    iam.get_topic_policy(PROJECT_ID, TOPIC_ID)
    out, _ = capsys.readouterr()
    assert topic_path in out


def test_get_subscription_policy(
    subscription_path: str, capsys: CaptureFixture[str]
) -> None:
    iam.get_subscription_policy(PROJECT_ID, SUBSCRIPTION_ID)
    out, _ = capsys.readouterr()
    assert subscription_path in out


def test_set_topic_policy(
    publisher_client: pubsub_v1.PublisherClient, topic_path: str
) -> None:
    iam.set_topic_policy(PROJECT_ID, TOPIC_ID)
    policy = publisher_client.get_iam_policy(request={"resource": topic_path})
    assert "roles/pubsub.publisher" in str(policy)
    assert "domain:google.com" in str(policy)


def test_set_subscription_policy(
    subscriber_client: pubsub_v1.SubscriberClient,
    subscription_path: str,
) -> None:
    iam.set_subscription_policy(PROJECT_ID, SUBSCRIPTION_ID)
    policy = subscriber_client.get_iam_policy(request={"resource": subscription_path})
    assert "roles/pubsub.viewer" in str(policy)
    assert "domain:google.com" in str(policy)


def test_check_topic_permissions(topic_path: str, capsys: CaptureFixture[str]) -> None:
    iam.check_topic_permissions(PROJECT_ID, TOPIC_ID)
    out, _ = capsys.readouterr()
    assert topic_path in out
    assert "pubsub.topics.publish" in out


def test_check_subscription_permissions(
    subscription_path: str,
    capsys: CaptureFixture[str],
) -> None:
    iam.check_subscription_permissions(PROJECT_ID, SUBSCRIPTION_ID)
    out, _ = capsys.readouterr()
    assert subscription_path in out
    assert "pubsub.subscriptions.consume" in out
