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
import time
import typing
from typing import Any, Callable, cast, Iterator, TypeVar, Union
import uuid

from _pytest.capture import CaptureFixture
import backoff
from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1
import mock
import pytest

import publisher


# This uuid is shared across tests which run in parallel.
UUID = uuid.uuid4().hex
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
TOPIC_ID = "publisher-test-topic-" + UUID
SUBSCRIPTION_ID = "publisher-test-subscription-" + UUID
# Allow 60s for tests to finish.
MAX_TIME = 60

# These tests run in parallel if pytest-parallel is installed.
# Avoid modifying resources that are shared across tests,
# as this results in test flake.

if typing.TYPE_CHECKING:
    from unittest.mock import AsyncMock, MagicMock

    MockType = Union[MagicMock, AsyncMock]


@pytest.fixture(scope="module")
def publisher_client() -> Iterator[pubsub_v1.PublisherClient]:
    yield pubsub_v1.PublisherClient()


@pytest.fixture(scope="module")
def subscriber_client() -> Iterator[pubsub_v1.SubscriberClient]:
    subscriber_client = pubsub_v1.SubscriberClient()
    yield subscriber_client
    # Close the subscriber client properly during teardown.
    subscriber_client.close()


@pytest.fixture(scope="module")
def topic_path(publisher_client: pubsub_v1.PublisherClient) -> Iterator[str]:
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
def subscription_path(
    subscriber_client: pubsub_v1.SubscriberClient, topic_path: str
) -> Iterator[str]:
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


def _make_sleep_patch() -> 'mock.mock._patch["MockType"]':
    real_sleep = time.sleep

    def new_sleep(period: float) -> None:
        if period == 60:
            real_sleep(5)
            raise RuntimeError("sigil")
        else:
            real_sleep(period)

    return mock.patch("time.sleep", new=new_sleep)


def test_create(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path}" in out

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_create_topic_with_kinesis_ingestion(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    # Outside of automated CI tests, these values must be of actual AWS resources for the test to pass.
    stream_arn = "arn:aws:kinesis:us-west-2:111111111111:stream/fake-stream-name"
    consumer_arn = "arn:aws:kinesis:us-west-2:111111111111:stream/fake-stream-name/consumer/consumer-1:1111111111"
    aws_role_arn = "arn:aws:iam::111111111111:role/fake-role-name"
    gcp_service_account = (
        "fake-service-account@fake-gcp-project.iam.gserviceaccount.com"
    )

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic_with_kinesis_ingestion(
        PROJECT_ID,
        TOPIC_ID,
        stream_arn,
        consumer_arn,
        aws_role_arn,
        gcp_service_account,
    )

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path} with AWS Kinesis Ingestion Settings" in out

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_create_topic_with_cloud_storage_ingestion(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    bucket = "pubsub-cloud-storage-bucket"
    input_format = "text"
    text_delimiter = ","
    match_glob = "**.txt"
    minimum_object_create_time = "1970-01-01T00:00:01Z"

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic_with_cloud_storage_ingestion(
        PROJECT_ID,
        TOPIC_ID,
        bucket,
        input_format,
        text_delimiter,
        match_glob,
        minimum_object_create_time,
    )

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path} with Cloud Storage Ingestion Settings" in out

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_create_topic_with_aws_msk_ingestion(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    # Outside of automated CI tests, these values must be of actual AWS resources for the test to pass.
    cluster_arn = (
        "arn:aws:kafka:us-east-1:111111111111:cluster/fake-cluster-name/11111111-1111-1"
    )
    msk_topic = "fake-msk-topic-name"
    aws_role_arn = "arn:aws:iam::111111111111:role/fake-role-name"
    gcp_service_account = (
        "fake-service-account@fake-gcp-project.iam.gserviceaccount.com"
    )

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic_with_aws_msk_ingestion(
        PROJECT_ID,
        TOPIC_ID,
        cluster_arn,
        msk_topic,
        aws_role_arn,
        gcp_service_account,
    )

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path} with AWS MSK Ingestion Settings" in out

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_create_topic_with_azure_event_hubs_ingestion(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    # Outside of automated CI tests, these values must be of actual Azure resources for the test to pass.
    resource_group = "fake-resource-group"
    namespace = "fake-namespace"
    event_hub = "fake-event-hub"
    client_id = "fake-client-id"
    tenant_id = "fake-tenant-id"
    subcription_id = "fake-subscription-id"
    gcp_service_account = (
        "fake-service-account@fake-gcp-project.iam.gserviceaccount.com"
    )

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic_with_azure_event_hubs_ingestion(
        PROJECT_ID,
        TOPIC_ID,
        resource_group,
        namespace,
        event_hub,
        client_id,
        tenant_id,
        subcription_id,
        gcp_service_account,
    )

    out, _ = capsys.readouterr()
    assert (
        f"Created topic: {topic_path} with Azure Event Hubs Ingestion Settings" in out
    )

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_create_topic_with_confluent_cloud_ingestion(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    # Outside of automated CI tests, these values must be of actual Confluent resources for the test to pass.
    bootstrap_server = "fake-bootstrap-server-id.us-south1.gcp.confluent.cloud:9092"
    cluster_id = "fake-cluster-id"
    confluent_topic = "fake-confluent-topic-name"
    identity_pool_id = "fake-identity-pool-id"
    gcp_service_account = (
        "fake-service-account@fake-gcp-project.iam.gserviceaccount.com"
    )

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic_with_confluent_cloud_ingestion(
        PROJECT_ID,
        TOPIC_ID,
        bootstrap_server,
        cluster_id,
        confluent_topic,
        identity_pool_id,
        gcp_service_account,
    )

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path} with Confluent Cloud Ingestion Settings" in out

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_create_with_smt(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic_with_smt(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path} with SMT" in out

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_update_topic_type(
    publisher_client: pubsub_v1.PublisherClient, capsys: CaptureFixture[str]
) -> None:
    # The scope of `topic_path` is limited to this function.
    topic_path = publisher_client.topic_path(PROJECT_ID, TOPIC_ID)

    # Outside of automated CI tests, these values must be of actual AWS resources for the test to pass.
    stream_arn = "arn:aws:kinesis:us-west-2:111111111111:stream/fake-stream-name"
    consumer_arn = "arn:aws:kinesis:us-west-2:111111111111:stream/fake-stream-name/consumer/consumer-1:1111111111"
    aws_role_arn = "arn:aws:iam::111111111111:role/fake-role-name"
    gcp_service_account = (
        "fake-service-account@fake-gcp-project.iam.gserviceaccount.com"
    )

    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass

    publisher.create_topic(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Created topic: {topic_path}" in out

    publisher.update_topic_type(
        PROJECT_ID,
        TOPIC_ID,
        stream_arn,
        consumer_arn,
        aws_role_arn,
        gcp_service_account,
    )

    out, _ = capsys.readouterr()
    assert f"Updated topic: {topic_path} with AWS Kinesis Ingestion Settings" in out

    # Clean up resource created for the test.
    publisher_client.delete_topic(request={"topic": topic_path})


def test_list(topic_path: str, capsys: CaptureFixture[str]) -> None:
    publisher.list_topics(PROJECT_ID)
    out, _ = capsys.readouterr()

    assert topic_path in out


def test_publish(topic_path: str, capsys: CaptureFixture[str]) -> None:
    publisher.publish_messages(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages to {topic_path}." in out


def test_publish_with_custom_attributes(
    topic_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.publish_messages_with_custom_attributes(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with custom attributes to {topic_path}." in out


def test_publish_with_batch_settings(
    topic_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.publish_messages_with_batch_settings(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with batch settings to {topic_path}." in out


def test_publish_with_flow_control_settings(
    topic_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.publish_messages_with_flow_control_settings(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with flow control settings to {topic_path}." in out


def test_publish_with_retry_settings(
    topic_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.publish_messages_with_retry_settings(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with retry settings to {topic_path}." in out


def test_publish_with_error_handler(
    topic_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.publish_messages_with_error_handler(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with error handler to {topic_path}." in out


def test_publish_with_ordering_keys(
    topic_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.publish_with_ordering_keys(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Published messages with ordering keys to {topic_path}." in out


def test_resume_publish_with_error_handler(
    topic_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.resume_publish_with_ordering_keys(PROJECT_ID, TOPIC_ID)

    out, _ = capsys.readouterr()
    assert f"Resumed publishing messages with ordering keys to {topic_path}." in out


def test_detach_subscription(
    subscription_path: str, capsys: CaptureFixture[str]
) -> None:
    publisher.detach_subscription(PROJECT_ID, SUBSCRIPTION_ID)

    out, _ = capsys.readouterr()
    assert f"{subscription_path} is detached." in out


def test_delete(publisher_client: pubsub_v1.PublisherClient) -> None:
    publisher.delete_topic(PROJECT_ID, TOPIC_ID)

    C = TypeVar("C", bound=Callable[..., Any])

    typed_backoff = cast(
        Callable[[C], C],
        backoff.on_exception(backoff.expo, AssertionError, max_time=MAX_TIME),
    )

    @typed_backoff
    def eventually_consistent_test() -> None:
        with pytest.raises(Exception):
            publisher_client.get_topic(
                request={"topic": publisher_client.topic_path(PROJECT_ID, TOPIC_ID)}
            )

    eventually_consistent_test()
