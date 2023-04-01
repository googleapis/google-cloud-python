#!/usr/bin/env python

# Copyright 2021 Google LLC. All Rights Reserved.
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
from typing import Any, Callable, Generator, TypeVar, cast
import uuid

from _pytest.capture import CaptureFixture
from flaky import flaky
from google.api_core.exceptions import InternalServerError, NotFound
from google.cloud import pubsub_v1
from google.cloud.pubsub import PublisherClient, SchemaServiceClient, SubscriberClient
from google.pubsub_v1.types import Encoding, Schema, Topic
import pytest

import schema

# This uuid is shared across tests which run in parallel.
UUID = uuid.uuid4().hex
try:
    PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
except KeyError:
    raise KeyError("Need to set GOOGLE_CLOUD_PROJECT as an environment variable.")
AVRO_TOPIC_ID = f"schema-test-avro-topic-{UUID}"
AVRO_TOPIC_ID_TO_CREATE = f"schema-test-avro-topic-to-create-{UUID}"
PROTO_TOPIC_ID = f"schema-test-proto-topic-{UUID}"
PROTO_WITH_REVISIONS_TOPIC_ID = f"schema-test-proto-with-revisions-topic-{UUID}"
PROTO_WITH_REVISIONS_TOPIC_ID_TO_CREATE = (
    f"schema-test-proto-with-revisions-topic-to-create-{UUID}"
)
AVRO_SUBSCRIPTION_ID = f"schema-test-avro-subscription-{UUID}"
PROTO_SUBSCRIPTION_ID = f"schema-test-proto-subscription-{UUID}"
AVRO_SCHEMA_ID = f"schema-test-avro-schema-{UUID}"
AVRO_SCHEMA_ID_TO_CREATE = f"schema-test-avro-schema-to-create-{UUID}"
PROTO_SCHEMA_ID = f"schema-test-proto-schema-{UUID}"
PROTO_SCHEMA_ID_TO_CREATE = f"schema-test-proto-schema-to-create-{UUID}"
PROTO_SCHEMA_ID_TO_DELETE = f"schema-test-proto-schema-to-delete-{UUID}"
AVSC_FILE = "resources/us-states.avsc"
AVSC_REVISION_FILE = "resources/us-states.avsc"
PROTO_FILE = "resources/us-states.proto"
PROTO_REVISION_FILE = "resources/us-states.proto"

# These tests run in parallel in continuous integration,
# with the same UUID.
# Avoid modifying resources that are shared across tests,
# as this results in test flake.


@pytest.fixture(scope="module")
def schema_client() -> Generator[pubsub_v1.SchemaServiceClient, None, None]:
    schema_client = SchemaServiceClient()
    yield schema_client


def ensure_schema_exists(
    name: str, type: Schema.Type, schema_client: pubsub_v1.SchemaServiceClient
) -> Schema:
    schema_path = schema_client.schema_path(PROJECT_ID, name)

    try:
        return schema_client.get_schema(request={"name": schema_path})
    except NotFound:
        project_path = f"projects/{PROJECT_ID}"
        with open(AVSC_FILE if type == Schema.Type.AVRO else PROTO_FILE, "rb") as f:
            definition_text = f.read().decode("utf-8")
        schema = Schema(name=schema_path, type_=type, definition=definition_text)
        return schema_client.create_schema(
            request={"parent": project_path, "schema": schema, "schema_id": name}
        )


@pytest.fixture(scope="module")
def avro_schema(
    schema_client: pubsub_v1.SchemaServiceClient,
) -> Generator[str, None, None]:
    avro_schema = ensure_schema_exists(AVRO_SCHEMA_ID, Schema.Type.AVRO, schema_client)

    yield avro_schema.name

    try:
        schema_client.delete_schema(request={"name": avro_schema.name})
    except (NotFound, InternalServerError):
        pass


@pytest.fixture(scope="module")
def avro_schema_to_create(
    schema_client: pubsub_v1.SchemaServiceClient,
) -> Generator[str, None, None]:
    avro_schema_path = schema_client.schema_path(PROJECT_ID, AVRO_SCHEMA_ID_TO_CREATE)

    yield avro_schema_path

    try:
        schema_client.delete_schema(request={"name": avro_schema_path})
    except (NotFound, InternalServerError):
        pass


@pytest.fixture(scope="module")
def proto_schema(
    schema_client: pubsub_v1.SchemaServiceClient,
) -> Generator[str, None, None]:
    proto_schema = ensure_schema_exists(
        PROTO_SCHEMA_ID, Schema.Type.PROTOCOL_BUFFER, schema_client
    )

    yield proto_schema.name

    try:
        schema_client.delete_schema(request={"name": proto_schema.name})
    except (NotFound, InternalServerError):
        pass


@pytest.fixture(scope="module")
def proto_schema_to_delete(
    schema_client: pubsub_v1.SchemaServiceClient,
) -> Generator[str, None, None]:
    proto_schema = ensure_schema_exists(
        PROTO_SCHEMA_ID_TO_DELETE, Schema.Type.PROTOCOL_BUFFER, schema_client
    )

    yield proto_schema.name

    try:
        schema_client.delete_schema(request={"name": proto_schema.name})
    except (NotFound, InternalServerError):
        pass


@pytest.fixture(scope="module")
def proto_schema_to_create(
    schema_client: pubsub_v1.SchemaServiceClient,
) -> Generator[str, None, None]:
    proto_schema_path = schema_client.schema_path(PROJECT_ID, PROTO_SCHEMA_ID_TO_CREATE)

    yield proto_schema_path

    try:
        schema_client.delete_schema(request={"name": proto_schema_path})
    except (NotFound, InternalServerError):
        pass


@pytest.fixture(scope="module")
def publisher_client() -> Generator[pubsub_v1.PublisherClient, None, None]:
    yield PublisherClient()


def ensure_topic_exists(
    name: str,
    schema_path: str,
    encoding: Encoding,
    publisher_client: pubsub_v1.PublisherClient,
) -> Topic:
    topic_path = publisher_client.topic_path(PROJECT_ID, name)

    try:
        return publisher_client.get_topic(request={"topic": topic_path})
    except NotFound:
        return publisher_client.create_topic(
            request={
                "name": topic_path,
                "schema_settings": {
                    "schema": schema_path,
                    "encoding": encoding,
                },
            }
        )


@pytest.fixture(scope="module")
def avro_topic(
    publisher_client: pubsub_v1.PublisherClient, avro_schema: str
) -> Generator[str, None, None]:
    avro_topic = ensure_topic_exists(
        AVRO_TOPIC_ID, avro_schema, Encoding.BINARY, publisher_client
    )

    yield avro_topic.name
    try:
        publisher_client.delete_topic(request={"topic": avro_topic.name})
    except NotFound:
        pass


@pytest.fixture(scope="module")
def avro_topic_to_create(
    publisher_client: pubsub_v1.PublisherClient, avro_schema: str
) -> Generator[str, None, None]:
    avro_topic_path = publisher_client.topic_path(PROJECT_ID, AVRO_TOPIC_ID_TO_CREATE)

    yield avro_topic_path
    try:
        publisher_client.delete_topic(request={"topic": avro_topic_path})
    except NotFound:
        pass


@pytest.fixture(scope="module")
def proto_topic(
    publisher_client: pubsub_v1.PublisherClient, proto_schema: str
) -> Generator[str, None, None]:
    proto_topic = ensure_topic_exists(
        PROTO_TOPIC_ID, proto_schema, Encoding.BINARY, publisher_client
    )

    yield proto_topic.name
    try:
        publisher_client.delete_topic(request={"topic": proto_topic.name})
    except NotFound:
        pass


@pytest.fixture(scope="module")
def proto_with_revisions_topic(
    publisher_client: pubsub_v1.PublisherClient, proto_schema: str
) -> Generator[str, None, None]:
    proto_topic = ensure_topic_exists(
        PROTO_WITH_REVISIONS_TOPIC_ID, proto_schema, Encoding.BINARY, publisher_client
    )

    yield proto_topic.name
    try:
        publisher_client.delete_topic(request={"topic": proto_topic.name})
    except NotFound:
        pass


@pytest.fixture(scope="module")
def proto_with_revisions_topic_to_create(
    publisher_client: pubsub_v1.PublisherClient, proto_schema: str
) -> Generator[str, None, None]:
    topic_path = publisher_client.topic_path(
        PROJECT_ID, PROTO_WITH_REVISIONS_TOPIC_ID_TO_CREATE
    )

    yield topic_path
    try:
        publisher_client.delete_topic(request={"topic": topic_path})
    except NotFound:
        pass


@pytest.fixture(scope="module")
def subscriber_client() -> Generator[pubsub_v1.SubscriberClient, None, None]:
    subscriber_client = SubscriberClient()
    yield subscriber_client
    subscriber_client.close()


@pytest.fixture(scope="module")
def avro_subscription(
    subscriber_client: pubsub_v1.SubscriberClient, avro_topic: str
) -> Generator[str, None, None]:
    avro_subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, AVRO_SUBSCRIPTION_ID
    )

    try:
        avro_subscription = subscriber_client.get_subscription(
            request={"subscription": avro_subscription_path}
        )
    except NotFound:
        avro_subscription = subscriber_client.create_subscription(
            request={"name": avro_subscription_path, "topic": avro_topic}
        )

    yield avro_subscription.name

    try:
        subscriber_client.delete_subscription(
            request={"subscription": avro_subscription.name}
        )
    except NotFound:
        pass


@pytest.fixture(scope="module")
def proto_subscription(
    subscriber_client: pubsub_v1.SubscriberClient, proto_topic: str
) -> Generator[str, None, None]:
    proto_subscription_path = subscriber_client.subscription_path(
        PROJECT_ID, PROTO_SUBSCRIPTION_ID
    )

    try:
        proto_subscription = subscriber_client.get_subscription(
            request={"subscription": proto_subscription_path}
        )
    except NotFound:
        proto_subscription = subscriber_client.create_subscription(
            request={"name": proto_subscription_path, "topic": proto_topic}
        )

    yield proto_subscription.name

    try:
        subscriber_client.delete_subscription(
            request={"subscription": proto_subscription.name}
        )
    except NotFound:
        pass


def test_create_avro_schema(
    schema_client: pubsub_v1.SchemaServiceClient,
    avro_schema_to_create: str,
    capsys: CaptureFixture[str],
) -> None:
    try:
        schema_client.delete_schema(request={"name": avro_schema_to_create})
    except NotFound:
        pass

    schema.create_avro_schema(PROJECT_ID, AVRO_SCHEMA_ID_TO_CREATE, AVSC_FILE)

    out, _ = capsys.readouterr()
    assert "Created a schema using an Avro schema file:" in out
    assert f"{avro_schema_to_create}" in out


def test_create_proto_schema(
    schema_client: pubsub_v1.SchemaServiceClient,
    proto_schema_to_create: str,
    capsys: CaptureFixture[str],
) -> None:
    try:
        schema_client.delete_schema(request={"name": proto_schema_to_create})
    except NotFound:
        pass

    schema.create_proto_schema(PROJECT_ID, PROTO_SCHEMA_ID_TO_CREATE, PROTO_FILE)

    out, _ = capsys.readouterr()
    assert "Created a schema using a protobuf schema file:" in out
    assert f"{proto_schema_to_create}" in out


def test_commit_avro_schema(
    schema_client: pubsub_v1.SchemaServiceClient,
    avro_schema: str,
    capsys: CaptureFixture[str],
) -> None:
    schema.commit_avro_schema(PROJECT_ID, AVRO_SCHEMA_ID, AVSC_REVISION_FILE)

    out, _ = capsys.readouterr()
    assert "Committed a schema revision using an Avro schema file:" in out
    # assert f"{avro_schema}" in out


def test_commit_proto_schema(
    schema_client: pubsub_v1.SchemaServiceClient,
    proto_schema: str,
    capsys: CaptureFixture[str],
) -> None:
    schema.commit_proto_schema(PROJECT_ID, PROTO_SCHEMA_ID, PROTO_REVISION_FILE)

    out, _ = capsys.readouterr()
    assert "Committed a schema revision using a protobuf schema file:" in out
    # assert f"{proto_schema}" in out


def test_get_schema(avro_schema: str, capsys: CaptureFixture[str]) -> None:
    schema.get_schema(PROJECT_ID, AVRO_SCHEMA_ID)
    out, _ = capsys.readouterr()
    assert "Got a schema" in out
    assert f"{avro_schema}" in out


def test_get_schema_revision(avro_schema: str, capsys: CaptureFixture[str]) -> None:
    committed_schema = schema.commit_avro_schema(
        PROJECT_ID, AVRO_SCHEMA_ID, AVSC_REVISION_FILE
    )
    schema.get_schema_revision(PROJECT_ID, AVRO_SCHEMA_ID, committed_schema.revision_id)
    out, _ = capsys.readouterr()
    assert "Got a schema revision" in out
    assert f"{avro_schema}" in out


def test_rollback_schema_revision(
    avro_schema: str, capsys: CaptureFixture[str]
) -> None:
    committed_schema = schema.commit_avro_schema(
        PROJECT_ID, AVRO_SCHEMA_ID, AVSC_REVISION_FILE
    )
    schema.commit_avro_schema(PROJECT_ID, AVRO_SCHEMA_ID, AVSC_REVISION_FILE)
    schema.rollback_schema_revision(
        PROJECT_ID, AVRO_SCHEMA_ID, committed_schema.revision_id
    )
    out, _ = capsys.readouterr()
    assert "Rolled back a schema revision" in out
    # assert f"{avro_schema}" in out


def test_delete_schema_revision(avro_schema: str, capsys: CaptureFixture[str]) -> None:
    committed_schema = schema.commit_avro_schema(
        PROJECT_ID, AVRO_SCHEMA_ID, AVSC_REVISION_FILE
    )
    schema.commit_avro_schema(PROJECT_ID, AVRO_SCHEMA_ID, AVSC_REVISION_FILE)
    schema.delete_schema_revision(
        PROJECT_ID, AVRO_SCHEMA_ID, committed_schema.revision_id
    )
    out, _ = capsys.readouterr()
    assert "Deleted a schema revision" in out
    # assert f"{avro_schema}" in out


def test_list_schemas(capsys: CaptureFixture[str]) -> None:
    schema.list_schemas(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "Listed schemas." in out


def test_list_schema_revisions(capsys: CaptureFixture[str]) -> None:
    schema.list_schema_revisions(PROJECT_ID, AVRO_SCHEMA_ID)
    out, _ = capsys.readouterr()
    assert "Listed schema revisions." in out


def test_create_topic_with_schema(
    avro_schema: str,
    avro_topic_to_create: str,
    publisher_client: pubsub_v1.PublisherClient,
    capsys: CaptureFixture[str],
) -> None:
    schema.create_topic_with_schema(
        PROJECT_ID, AVRO_TOPIC_ID_TO_CREATE, AVRO_SCHEMA_ID, "BINARY"
    )
    out, _ = capsys.readouterr()
    assert "Created a topic" in out
    assert f"{AVRO_TOPIC_ID_TO_CREATE}" in out
    assert f"{avro_schema}" in out
    assert "BINARY" in out or "2" in out


def test_create_topic_with_schema_revisions(
    proto_schema: str,
    proto_with_revisions_topic_to_create: str,
    publisher_client: pubsub_v1.PublisherClient,
    capsys: CaptureFixture[str],
) -> None:
    committed_schema = schema.commit_proto_schema(
        PROJECT_ID, PROTO_SCHEMA_ID, PROTO_REVISION_FILE
    )

    schema.create_topic_with_schema_revisions(
        PROJECT_ID,
        PROTO_WITH_REVISIONS_TOPIC_ID_TO_CREATE,
        PROTO_SCHEMA_ID,
        committed_schema.revision_id,
        committed_schema.revision_id,
        "BINARY",
    )
    out, _ = capsys.readouterr()
    assert "Created a topic" in out
    assert f"{PROTO_WITH_REVISIONS_TOPIC_ID_TO_CREATE}" in out
    assert f"{proto_schema}" in out
    assert "BINARY" in out or "2" in out


def test_update_topic_schema(
    proto_schema: str, proto_with_revisions_topic: str, capsys: CaptureFixture[str]
) -> None:
    committed_schema = schema.commit_proto_schema(
        PROJECT_ID, PROTO_SCHEMA_ID, PROTO_REVISION_FILE
    )

    schema.update_topic_schema(
        PROJECT_ID,
        PROTO_WITH_REVISIONS_TOPIC_ID,
        committed_schema.revision_id,
        committed_schema.revision_id,
    )
    out, _ = capsys.readouterr()
    assert "Updated a topic schema" in out
    assert f"{PROTO_WITH_REVISIONS_TOPIC_ID}" in out
    assert f"{proto_schema}" in out


def test_publish_avro_records(
    avro_schema: str, avro_topic: str, capsys: CaptureFixture[str]
) -> None:
    schema.publish_avro_records(PROJECT_ID, AVRO_TOPIC_ID, AVSC_FILE)
    out, _ = capsys.readouterr()
    assert "Preparing a binary-encoded message" in out
    assert "Published message ID" in out


def test_subscribe_with_avro_schema(
    avro_schema: str,
    avro_topic: str,
    avro_subscription: str,
    capsys: CaptureFixture[str],
) -> None:
    schema.publish_avro_records(PROJECT_ID, AVRO_TOPIC_ID, AVSC_FILE)

    schema.subscribe_with_avro_schema(PROJECT_ID, AVRO_SUBSCRIPTION_ID, AVSC_FILE, 9)
    out, _ = capsys.readouterr()
    assert "Received a binary-encoded message:" in out


def test_subscribe_with_avro_schema_revisions(
    avro_schema: str,
    avro_topic: str,
    avro_subscription: str,
    capsys: CaptureFixture[str],
) -> None:
    schema.publish_avro_records(PROJECT_ID, AVRO_TOPIC_ID, AVSC_FILE)

    schema.subscribe_with_avro_schema_with_revisions(
        PROJECT_ID, AVRO_SUBSCRIPTION_ID, AVSC_FILE, 9
    )
    out, _ = capsys.readouterr()
    assert "Received a binary-encoded message:" in out


def test_publish_proto_records(proto_topic: str, capsys: CaptureFixture[str]) -> None:
    schema.publish_proto_messages(PROJECT_ID, PROTO_TOPIC_ID)
    out, _ = capsys.readouterr()
    assert "Preparing a binary-encoded message" in out
    assert "Published message ID" in out


def test_subscribe_with_proto_schema(
    proto_schema: str,
    proto_topic: str,
    proto_subscription: str,
    capsys: CaptureFixture[str],
) -> None:
    schema.publish_proto_messages(PROJECT_ID, PROTO_TOPIC_ID)

    schema.subscribe_with_proto_schema(PROJECT_ID, PROTO_SUBSCRIPTION_ID, 9)
    out, _ = capsys.readouterr()
    assert "Received a binary-encoded message" in out


C = TypeVar("C", bound=Callable[..., Any])
typed_flaky = cast(Callable[[C], C], flaky(max_runs=3, min_passes=1))


@typed_flaky
def test_delete_schema(
    proto_schema_to_delete: str, capsys: CaptureFixture[str]
) -> None:
    schema.delete_schema(PROJECT_ID, PROTO_SCHEMA_ID_TO_DELETE)
    out, _ = capsys.readouterr()
    assert "Deleted a schema" in out
    assert f"{proto_schema_to_delete}" in out
