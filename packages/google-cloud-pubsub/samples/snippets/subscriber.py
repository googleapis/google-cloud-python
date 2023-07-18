#!/usr/bin/env python

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

"""This application demonstrates how to perform basic operations on
subscriptions with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse
import typing
from typing import Optional

if typing.TYPE_CHECKING:
    from google.pubsub_v1 import types as gapic_types


def list_subscriptions_in_topic(project_id: str, topic_id: str) -> None:
    """Lists all subscriptions for a given topic."""
    # [START pubsub_list_topic_subscriptions]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    response = publisher.list_topic_subscriptions(request={"topic": topic_path})
    for subscription in response:
        print(subscription)
    # [END pubsub_list_topic_subscriptions]


def list_subscriptions_in_project(project_id: str) -> None:
    """Lists all subscriptions in the current project."""
    # [START pubsub_list_subscriptions]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"

    subscriber = pubsub_v1.SubscriberClient()
    project_path = f"projects/{project_id}"

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        for subscription in subscriber.list_subscriptions(
            request={"project": project_path}
        ):
            print(subscription.name)
    # [END pubsub_list_subscriptions]


def create_subscription(project_id: str, topic_id: str, subscription_id: str) -> None:
    """Create a new pull subscription on the given topic."""
    # [START pubsub_create_pull_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )

    print(f"Subscription created: {subscription}")
    # [END pubsub_create_pull_subscription]


def create_subscription_with_dead_letter_topic(
    project_id: str,
    topic_id: str,
    subscription_id: str,
    dead_letter_topic_id: str,
    max_delivery_attempts: int = 5,
) -> None:
    """Create a subscription with dead letter policy."""
    # [START pubsub_dead_letter_create_subscription]
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.types import DeadLetterPolicy

    # TODO(developer)
    # project_id = "your-project-id"
    # endpoint = "https://my-test-project.appspot.com/push"
    # TODO(developer): This is an existing topic that the subscription
    # with dead letter policy is attached to.
    # topic_id = "your-topic-id"
    # TODO(developer): This is an existing subscription with a dead letter policy.
    # subscription_id = "your-subscription-id"
    # TODO(developer): This is an existing dead letter topic that the subscription
    # with dead letter policy will forward dead letter messages to.
    # dead_letter_topic_id = "your-dead-letter-topic-id"
    # TODO(developer): This is the maximum number of delivery attempts allowed
    # for a message before it gets delivered to a dead letter topic.
    # max_delivery_attempts = 5

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    dead_letter_policy = DeadLetterPolicy(
        dead_letter_topic=dead_letter_topic_path,
        max_delivery_attempts=max_delivery_attempts,
    )

    with subscriber:
        request = {
            "name": subscription_path,
            "topic": topic_path,
            "dead_letter_policy": dead_letter_policy,
        }
        subscription = subscriber.create_subscription(request)

    print(f"Subscription created: {subscription.name}")
    print(
        f"It will forward dead letter messages to: {subscription.dead_letter_policy.dead_letter_topic}."
    )
    print(
        f"After {subscription.dead_letter_policy.max_delivery_attempts} delivery attempts."
    )
    # [END pubsub_dead_letter_create_subscription]


def create_push_subscription(
    project_id: str, topic_id: str, subscription_id: str, endpoint: str
) -> None:
    """Create a new push subscription on the given topic."""
    # [START pubsub_create_push_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"
    # endpoint = "https://my-test-project.appspot.com/push"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "push_config": push_config,
            }
        )

    print(f"Push subscription created: {subscription}.")
    print(f"Endpoint for subscription is: {endpoint}")
    # [END pubsub_create_push_subscription]


def create_push_no_wrapper_subscription(
    project_id: str, topic_id: str, subscription_id: str, endpoint: str
) -> None:
    """Create a new push no wrapper subscription on the given topic."""
    # [START pubsub_create_push_no_wrapper_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"
    # endpoint = "https://my-test-project.appspot.com/push"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    no_wrapper = pubsub_v1.types.PushConfig.NoWrapper(write_metadata=True)
    push_config = pubsub_v1.types.PushConfig(
        push_endpoint=endpoint, no_wrapper=no_wrapper
    )

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "push_config": push_config,
            }
        )

    print(f"Push no wrapper subscription created: {subscription}.")
    print(f"Endpoint for subscription is: {endpoint}")
    print(f"No wrapper configuration for subscription is: {no_wrapper}")
    # [END pubsub_create_push_no_wrapper_subscription]


def create_subscription_with_ordering(
    project_id: str, topic_id: str, subscription_id: str
) -> None:
    """Create a subscription with ordering enabled."""
    # [START pubsub_enable_subscription_ordering]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "enable_message_ordering": True,
            }
        )
        print(f"Created subscription with ordering: {subscription}")
    # [END pubsub_enable_subscription_ordering]


def create_subscription_with_filtering(
    project_id: str,
    topic_id: str,
    subscription_id: str,
    filter: str,
) -> None:
    """Create a subscription with filtering enabled."""
    # [START pubsub_create_subscription_with_filter]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"
    # filter = "attributes.author=\"unknown\""

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    with subscriber:
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path, "filter": filter}
        )
        print(f"Created subscription with filtering enabled: {subscription}")
    # [END pubsub_create_subscription_with_filter]


def create_subscription_with_exactly_once_delivery(
    project_id: str, topic_id: str, subscription_id: str
) -> None:
    """Create a subscription with exactly once delivery enabled."""
    # [START pubsub_create_subscription_with_exactly_once_delivery]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "enable_exactly_once_delivery": True,
            }
        )
        print(
            f"Created subscription with exactly once delivery enabled: {subscription}"
        )
    # [END pubsub_create_subscription_with_exactly_once_delivery]


def create_bigquery_subscription(
    project_id: str, topic_id: str, subscription_id: str, bigquery_table_id: str
) -> None:
    """Create a new BigQuery subscription on the given topic."""
    # [START pubsub_create_bigquery_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"
    # bigquery_table_id = "your-project.your-dataset.your-table"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    bigquery_config = pubsub_v1.types.BigQueryConfig(
        table=bigquery_table_id, write_metadata=True
    )

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "bigquery_config": bigquery_config,
            }
        )

    print(f"BigQuery subscription created: {subscription}.")
    print(f"Table for subscription is: {bigquery_table_id}")
    # [END pubsub_create_bigquery_subscription]


def delete_subscription(project_id: str, subscription_id: str) -> None:
    """Deletes an existing Pub/Sub topic."""
    # [START pubsub_delete_subscription]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscriber.delete_subscription(request={"subscription": subscription_path})

    print(f"Subscription deleted: {subscription_path}.")
    # [END pubsub_delete_subscription]


def update_push_subscription(
    project_id: str, topic_id: str, subscription_id: str, endpoint: str
) -> None:
    """
    Updates an existing Pub/Sub subscription's push endpoint URL.
    Note that certain properties of a subscription, such as
    its topic, are not modifiable.
    """
    # [START pubsub_update_push_configuration]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # subscription_id = "your-subscription-id"
    # endpoint = "https://my-test-project.appspot.com/push"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

    subscription = pubsub_v1.types.Subscription(
        name=subscription_path, topic=topic_id, push_config=push_config
    )

    update_mask = {"paths": {"push_config"}}

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        result = subscriber.update_subscription(
            request={"subscription": subscription, "update_mask": update_mask}
        )

    print(f"Subscription updated: {subscription_path}")
    print(f"New endpoint for subscription is: {result.push_config}.")
    # [END pubsub_update_push_configuration]


def update_subscription_with_dead_letter_policy(
    project_id: str,
    topic_id: str,
    subscription_id: str,
    dead_letter_topic_id: str,
    max_delivery_attempts: int = 5,
) -> "gapic_types.Subscription":
    """Update a subscription's dead letter policy."""
    # [START pubsub_dead_letter_update_subscription]
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.types import DeadLetterPolicy, FieldMask

    # TODO(developer)
    # project_id = "your-project-id"
    # TODO(developer): This is an existing topic that the subscription
    # with dead letter policy is attached to.
    # topic_id = "your-topic-id"
    # TODO(developer): This is an existing subscription with a dead letter policy.
    # subscription_id = "your-subscription-id"
    # TODO(developer): This is an existing dead letter topic that the subscription
    # with dead letter policy will forward dead letter messages to.
    # dead_letter_topic_id = "your-dead-letter-topic-id"
    # TODO(developer): This is the maximum number of delivery attempts allowed
    # for a message before it gets delivered to a dead letter topic.
    # max_delivery_attempts = 5

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    subscription_before_update = subscriber.get_subscription(
        request={"subscription": subscription_path}
    )
    print(f"Before the update: {subscription_before_update}.")

    # Indicates which fields in the provided subscription to update.
    update_mask = FieldMask(paths=["dead_letter_policy"])

    # Construct a dead letter policy you expect to have after the update.
    dead_letter_policy = DeadLetterPolicy(
        dead_letter_topic=dead_letter_topic_path,
        max_delivery_attempts=max_delivery_attempts,
    )

    # Construct the subscription with the dead letter policy you expect to have
    # after the update. Here, values in the required fields (name, topic) help
    # identify the subscription.
    subscription = pubsub_v1.types.Subscription(
        name=subscription_path,
        topic=topic_path,
        dead_letter_policy=dead_letter_policy,
    )

    with subscriber:
        subscription_after_update = subscriber.update_subscription(
            request={"subscription": subscription, "update_mask": update_mask}
        )

    print(f"After the update: {subscription_after_update}.")
    # [END pubsub_dead_letter_update_subscription]
    return subscription_after_update


def remove_dead_letter_policy(
    project_id: str, topic_id: str, subscription_id: str
) -> "gapic_types.Subscription":
    """Remove dead letter policy from a subscription."""
    # [START pubsub_dead_letter_remove]
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.types import FieldMask

    # TODO(developer)
    # project_id = "your-project-id"
    # TODO(developer): This is an existing topic that the subscription
    # with dead letter policy is attached to.
    # topic_id = "your-topic-id"
    # TODO(developer): This is an existing subscription with a dead letter policy.
    # subscription_id = "your-subscription-id"

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    subscription_before_update = subscriber.get_subscription(
        request={"subscription": subscription_path}
    )
    print(f"Before removing the policy: {subscription_before_update}.")

    # Indicates which fields in the provided subscription to update.
    update_mask = FieldMask(paths=["dead_letter_policy"])

    # Construct the subscription (without any dead letter policy) that you
    # expect to have after the update.
    subscription = pubsub_v1.types.Subscription(
        name=subscription_path, topic=topic_path
    )

    with subscriber:
        subscription_after_update = subscriber.update_subscription(
            request={"subscription": subscription, "update_mask": update_mask}
        )

    print(f"After removing the policy: {subscription_after_update}.")
    # [END pubsub_dead_letter_remove]
    return subscription_after_update


def receive_messages(
    project_id: str, subscription_id: str, timeout: Optional[float] = None
) -> None:
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull]
    # [START pubsub_quickstart_subscriber]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscriber_async_pull]
    # [END pubsub_quickstart_subscriber]


def receive_messages_with_custom_attributes(
    project_id: str, subscription_id: str, timeout: Optional[float] = None
) -> None:
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull_custom_attributes]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message.data!r}.")
        if message.attributes:
            print("Attributes:")
            for key in message.attributes:
                value = message.attributes.get(key)
                print(f"{key}: {value}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscriber_async_pull_custom_attributes]


def receive_messages_with_flow_control(
    project_id: str, subscription_id: str, timeout: Optional[float] = None
) -> None:
    """Receives messages from a pull subscription with flow control."""
    # [START pubsub_subscriber_flow_settings]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message.data!r}.")
        message.ack()

    # Limit the subscriber to only have ten outstanding messages at a time.
    flow_control = pubsub_v1.types.FlowControl(max_messages=10)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, flow_control=flow_control
    )
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscriber_flow_settings]


def receive_messages_with_blocking_shutdown(
    project_id: str, subscription_id: str, timeout: float = 5.0
) -> None:
    """Shuts down a pull subscription by awaiting message callbacks to complete."""
    # [START pubsub_subscriber_blocking_shutdown]
    import time
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message.data!r}.")
        time.sleep(timeout + 3.0)  # Pocess longer than streaming pull future timeout.
        message.ack()
        print(f"Done processing the message {message.data!r}.")

    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback,
        await_callbacks_on_shutdown=True,
    )
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            print("Streaming pull future canceled.")
            streaming_pull_future.result()  # Blocks until shutdown complete.
            print("Done waiting for the stream shutdown.")

    # The "Done waiting..." message is only printed *after* the processing of all
    # received messages has completed.
    # [END pubsub_subscriber_blocking_shutdown]


def receive_messages_with_exactly_once_delivery_enabled(
    project_id: str, subscription_id: str, timeout: Optional[float] = None
) -> None:
    """Receives messages from a pull subscription with exactly-once delivery enabled.
    This is a preview feature. For more details, see:
    https://cloud.google.com/pubsub/docs/exactly-once-delivery."
    """
    # [START pubsub_subscriber_exactly_once]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.subscriber import exceptions as sub_exceptions

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")

        # Use `ack_with_response()` instead of `ack()` to get a future that tracks
        # the result of the acknowledge call. When exactly-once delivery is enabled
        # on the subscription, the message is guaranteed to not be delivered again
        # if the ack future succeeds.
        ack_future = message.ack_with_response()

        try:
            # Block on result of acknowledge call.
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            ack_future.result(timeout=timeout)
            print(f"Ack for message {message.message_id} successful.")
        except sub_exceptions.AcknowledgeError as e:
            print(
                f"Ack for message {message.message_id} failed with error: {e.error_code}"
            )

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscriber_exactly_once]


def synchronous_pull(project_id: str, subscription_id: str) -> None:
    """Pulling messages synchronously."""
    # [START pubsub_subscriber_sync_pull]
    from google.api_core import retry
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    NUM_MESSAGES = 3

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        # The subscriber pulls a specific number of messages. The actual
        # number of messages pulled may be smaller than max_messages.
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
            retry=retry.Retry(deadline=300),
        )

        if len(response.received_messages) == 0:
            return

        ack_ids = []
        for received_message in response.received_messages:
            print(f"Received: {received_message.message.data}.")
            ack_ids.append(received_message.ack_id)

        # Acknowledges the received messages so they will not be sent again.
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

        print(
            f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
        )
    # [END pubsub_subscriber_sync_pull]


def synchronous_pull_with_lease_management(
    project_id: str, subscription_id: str
) -> None:
    """Pulling messages synchronously with lease management"""
    # [START pubsub_subscriber_sync_pull_with_lease]
    import logging
    import multiprocessing
    import sys
    import time

    from google.api_core import retry
    from google.cloud import pubsub_v1

    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    processes = dict()

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 3},
        retry=retry.Retry(deadline=300),
    )

    if len(response.received_messages) == 0:
        return

    # Start a process for each message based on its size modulo 10.
    for message in response.received_messages:
        process = multiprocessing.Process(
            target=time.sleep, args=(sys.getsizeof(message) % 10,)
        )
        processes[process] = (message.ack_id, message.message.data)
        process.start()

    while processes:
        # Take a break every second.
        if processes:
            time.sleep(1)

        for process in list(processes):
            ack_id, msg_data = processes[process]
            # If the process is running, reset the ack deadline.
            if process.is_alive():
                subscriber.modify_ack_deadline(
                    request={
                        "subscription": subscription_path,
                        "ack_ids": [ack_id],
                        # Must be between 10 and 600.
                        "ack_deadline_seconds": 15,
                    }
                )
                logger.debug(f"Reset ack deadline for {msg_data}.")

            # If the process is complete, acknowledge the message.
            else:
                subscriber.acknowledge(
                    request={"subscription": subscription_path, "ack_ids": [ack_id]}
                )
                logger.debug(f"Acknowledged {msg_data}.")
                processes.pop(process)
    print(
        f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
    )

    # Close the underlying gPRC channel. Alternatively, wrap subscriber in
    # a 'with' block to automatically call close() when done.
    subscriber.close()
    # [END pubsub_subscriber_sync_pull_with_lease]


def listen_for_errors(
    project_id: str, subscription_id: str, timeout: Optional[float] = None
) -> None:
    """Receives messages and catches errors from a pull subscription."""
    # [START pubsub_subscriber_error_listener]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber should listen for messages
    # timeout = 5.0

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        try:
            streaming_pull_future.result(timeout=timeout)
        except Exception as e:
            print(
                f"Listening for messages on {subscription_path} threw an exception: {e}."
            )
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscriber_error_listener]


def receive_messages_with_delivery_attempts(
    project_id: str, subscription_id: str, timeout: Optional[float] = None
) -> None:
    # [START pubsub_dead_letter_delivery_attempt]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message}.")
        print(f"With delivery attempts: {message.delivery_attempt}.")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_dead_letter_delivery_attempt]


if __name__ == "__main__":  # noqa
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")
    list_in_topic_parser = subparsers.add_parser(
        "list-in-topic", help=list_subscriptions_in_topic.__doc__
    )
    list_in_topic_parser.add_argument("topic_id")

    list_in_project_parser = subparsers.add_parser(
        "list-in-project", help=list_subscriptions_in_project.__doc__
    )

    create_parser = subparsers.add_parser("create", help=create_subscription.__doc__)
    create_parser.add_argument("topic_id")
    create_parser.add_argument("subscription_id")

    create_with_dead_letter_policy_parser = subparsers.add_parser(
        "create-with-dead-letter-policy",
        help=create_subscription_with_dead_letter_topic.__doc__,
    )
    create_with_dead_letter_policy_parser.add_argument("topic_id")
    create_with_dead_letter_policy_parser.add_argument("subscription_id")
    create_with_dead_letter_policy_parser.add_argument("dead_letter_topic_id")
    create_with_dead_letter_policy_parser.add_argument(
        "max_delivery_attempts", type=int, nargs="?", default=5
    )

    create_push_parser = subparsers.add_parser(
        "create-push", help=create_push_subscription.__doc__
    )
    create_push_parser.add_argument("topic_id")
    create_push_parser.add_argument("subscription_id")
    create_push_parser.add_argument("endpoint")

    create_push_no_wrapper_parser = subparsers.add_parser(
        "create-push-no-wrapper", help=create_push_no_wrapper_subscription.__doc__
    )
    create_push_no_wrapper_parser.add_argument("topic_id")
    create_push_no_wrapper_parser.add_argument("subscription_id")
    create_push_no_wrapper_parser.add_argument("endpoint")

    create_subscription_with_ordering_parser = subparsers.add_parser(
        "create-with-ordering", help=create_subscription_with_ordering.__doc__
    )
    create_subscription_with_ordering_parser.add_argument("topic_id")
    create_subscription_with_ordering_parser.add_argument("subscription_id")

    create_subscription_with_filtering_parser = subparsers.add_parser(
        "create-with-filtering", help=create_subscription_with_filtering.__doc__
    )
    create_subscription_with_filtering_parser.add_argument("topic_id")
    create_subscription_with_filtering_parser.add_argument("subscription_id")
    create_subscription_with_filtering_parser.add_argument("filter")

    create_subscription_with_exactly_once_delivery_parser = subparsers.add_parser(
        "create-with-exactly-once",
        help=create_subscription_with_exactly_once_delivery.__doc__,
    )
    create_subscription_with_exactly_once_delivery_parser.add_argument("topic_id")
    create_subscription_with_exactly_once_delivery_parser.add_argument(
        "subscription_id"
    )

    create_bigquery_subscription_parser = subparsers.add_parser(
        "create-biquery",
        help=create_bigquery_subscription.__doc__,
    )
    create_bigquery_subscription_parser.add_argument("topic_id")
    create_bigquery_subscription_parser.add_argument("subscription_id")
    create_bigquery_subscription_parser.add_argument("bigquery_table_id")

    delete_parser = subparsers.add_parser("delete", help=delete_subscription.__doc__)
    delete_parser.add_argument("subscription_id")

    update_push_parser = subparsers.add_parser(
        "update-push", help=update_push_subscription.__doc__
    )
    update_push_parser.add_argument("topic_id")
    update_push_parser.add_argument("subscription_id")
    update_push_parser.add_argument("endpoint")

    update_dead_letter_policy_parser = subparsers.add_parser(
        "update-dead-letter-policy",
        help=update_subscription_with_dead_letter_policy.__doc__,
    )
    update_dead_letter_policy_parser.add_argument("topic_id")
    update_dead_letter_policy_parser.add_argument("subscription_id")
    update_dead_letter_policy_parser.add_argument("dead_letter_topic_id")
    update_dead_letter_policy_parser.add_argument(
        "max_delivery_attempts", type=int, nargs="?", default=5
    )

    remove_dead_letter_policy_parser = subparsers.add_parser(
        "remove-dead-letter-policy", help=remove_dead_letter_policy.__doc__
    )
    remove_dead_letter_policy_parser.add_argument("topic_id")
    remove_dead_letter_policy_parser.add_argument("subscription_id")

    receive_parser = subparsers.add_parser("receive", help=receive_messages.__doc__)
    receive_parser.add_argument("subscription_id")
    receive_parser.add_argument("timeout", default=None, type=float, nargs="?")

    receive_with_custom_attributes_parser = subparsers.add_parser(
        "receive-custom-attributes",
        help=receive_messages_with_custom_attributes.__doc__,
    )
    receive_with_custom_attributes_parser.add_argument("subscription_id")
    receive_with_custom_attributes_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    receive_with_flow_control_parser = subparsers.add_parser(
        "receive-flow-control", help=receive_messages_with_flow_control.__doc__
    )
    receive_with_flow_control_parser.add_argument("subscription_id")
    receive_with_flow_control_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    receive_with_blocking_shutdown_parser = subparsers.add_parser(
        "receive-blocking-shutdown",
        help=receive_messages_with_blocking_shutdown.__doc__,
    )
    receive_with_blocking_shutdown_parser.add_argument("subscription_id")
    receive_with_blocking_shutdown_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    receive_messages_with_exactly_once_delivery_enabled_parser = subparsers.add_parser(
        "receive-messages-with-exactly-once-delivery-enabled",
        help=receive_messages_with_exactly_once_delivery_enabled.__doc__,
    )
    receive_messages_with_exactly_once_delivery_enabled_parser.add_argument(
        "subscription_id"
    )
    receive_messages_with_exactly_once_delivery_enabled_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    synchronous_pull_parser = subparsers.add_parser(
        "receive-synchronously", help=synchronous_pull.__doc__
    )
    synchronous_pull_parser.add_argument("subscription_id")

    synchronous_pull_with_lease_management_parser = subparsers.add_parser(
        "receive-synchronously-with-lease",
        help=synchronous_pull_with_lease_management.__doc__,
    )
    synchronous_pull_with_lease_management_parser.add_argument("subscription_id")

    listen_for_errors_parser = subparsers.add_parser(
        "listen-for-errors", help=listen_for_errors.__doc__
    )
    listen_for_errors_parser.add_argument("subscription_id")
    listen_for_errors_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    receive_messages_with_delivery_attempts_parser = subparsers.add_parser(
        "receive-messages-with-delivery-attempts",
        help=receive_messages_with_delivery_attempts.__doc__,
    )
    receive_messages_with_delivery_attempts_parser.add_argument("subscription_id")
    receive_messages_with_delivery_attempts_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    args = parser.parse_args()

    if args.command == "list-in-topic":
        list_subscriptions_in_topic(args.project_id, args.topic_id)
    elif args.command == "list-in-project":
        list_subscriptions_in_project(args.project_id)
    elif args.command == "create":
        create_subscription(args.project_id, args.topic_id, args.subscription_id)
    elif args.command == "create-with-dead-letter-policy":
        create_subscription_with_dead_letter_topic(
            args.project_id,
            args.topic_id,
            args.subscription_id,
            args.dead_letter_topic_id,
            args.max_delivery_attempts,
        )
    elif args.command == "create-push":
        create_push_subscription(
            args.project_id, args.topic_id, args.subscription_id, args.endpoint
        )
    elif args.command == "create-push-no-wrapper":
        create_push_no_wrapper_subscription(
            args.project_id, args.topic_id, args.subscription_id, args.endpoint
        )
    elif args.command == "create-with-ordering":
        create_subscription_with_ordering(
            args.project_id, args.topic_id, args.subscription_id
        )
    elif args.command == "create-with-filtering":
        create_subscription_with_filtering(
            args.project_id, args.topic_id, args.subscription_id, args.filter
        )
    elif args.command == "create-with-exactly-once":
        create_subscription_with_exactly_once_delivery(
            args.project_id, args.topic_id, args.subscription_id
        )
    elif args.command == "create-bigquery":
        create_bigquery_subscription(
            args.project_id,
            args.topic_id,
            args.subscription_id,
            args.bigquery_table_id,
        )
    elif args.command == "delete":
        delete_subscription(args.project_id, args.subscription_id)
    elif args.command == "update-push":
        update_push_subscription(
            args.project_id, args.topic_id, args.subscription_id, args.endpoint
        )
    elif args.command == "update-dead-letter-policy":
        update_subscription_with_dead_letter_policy(
            args.project_id,
            args.topic_id,
            args.subscription_id,
            args.dead_letter_topic_id,
            args.max_delivery_attempts,
        )
    elif args.command == "remove-dead-letter-policy":
        remove_dead_letter_policy(args.project_id, args.topic_id, args.subscription_id)
    elif args.command == "receive":
        receive_messages(args.project_id, args.subscription_id, args.timeout)
    elif args.command == "receive-custom-attributes":
        receive_messages_with_custom_attributes(
            args.project_id, args.subscription_id, args.timeout
        )
    elif args.command == "receive-flow-control":
        receive_messages_with_flow_control(
            args.project_id, args.subscription_id, args.timeout
        )
    elif args.command == "receive-blocking-shutdown":
        receive_messages_with_blocking_shutdown(
            args.project_id, args.subscription_id, args.timeout
        )
    elif args.command == "receive-messages-with-exactly-once-delivery-enabled":
        receive_messages_with_exactly_once_delivery_enabled(
            args.project_id, args.subscription_id, args.timeout
        )
    elif args.command == "receive-synchronously":
        synchronous_pull(args.project_id, args.subscription_id)
    elif args.command == "receive-synchronously-with-lease":
        synchronous_pull_with_lease_management(args.project_id, args.subscription_id)
    elif args.command == "listen-for-errors":
        listen_for_errors(args.project_id, args.subscription_id, args.timeout)
    elif args.command == "receive-messages-with-delivery-attempts":
        receive_messages_with_delivery_attempts(
            args.project_id, args.subscription_id, args.timeout
        )
