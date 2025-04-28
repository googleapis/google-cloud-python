#!/usr/bin/env python

# Copyright 2016 Google LLC. All Rights Reserved.
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

"""This application demonstrates how to perform basic operations on topics
with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse


def list_topics(project_id: str) -> None:
    """Lists all Pub/Sub topics in the given project."""
    # [START pubsub_list_topics]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"

    publisher = pubsub_v1.PublisherClient()
    project_path = f"projects/{project_id}"

    for topic in publisher.list_topics(request={"project": project_path}):
        print(topic)
    # [END pubsub_list_topics]


def create_topic(project_id: str, topic_id: str) -> None:
    """Create a new Pub/Sub topic."""
    # [START pubsub_quickstart_create_topic]
    # [START pubsub_create_topic]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")
    # [END pubsub_quickstart_create_topic]
    # [END pubsub_create_topic]


def create_topic_with_kinesis_ingestion(
    project_id: str,
    topic_id: str,
    stream_arn: str,
    consumer_arn: str,
    aws_role_arn: str,
    gcp_service_account: str,
) -> None:
    """Create a new Pub/Sub topic with AWS Kinesis Ingestion Settings."""
    # [START pubsub_create_topic_with_kinesis_ingestion]
    from google.cloud import pubsub_v1
    from google.pubsub_v1.types import Topic
    from google.pubsub_v1.types import IngestionDataSourceSettings

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # stream_arn = "your-stream-arn"
    # consumer_arn = "your-consumer-arn"
    # aws_role_arn = "your-aws-role-arn"
    # gcp_service_account = "your-gcp-service-account"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    request = Topic(
        name=topic_path,
        ingestion_data_source_settings=IngestionDataSourceSettings(
            aws_kinesis=IngestionDataSourceSettings.AwsKinesis(
                stream_arn=stream_arn,
                consumer_arn=consumer_arn,
                aws_role_arn=aws_role_arn,
                gcp_service_account=gcp_service_account,
            )
        ),
    )

    topic = publisher.create_topic(request=request)

    print(f"Created topic: {topic.name} with AWS Kinesis Ingestion Settings")
    # [END pubsub_create_topic_with_kinesis_ingestion]


def create_topic_with_cloud_storage_ingestion(
    project_id: str,
    topic_id: str,
    bucket: str,
    input_format: str,
    text_delimiter: str,
    match_glob: str,
    minimum_object_create_time: str,
) -> None:
    """Create a new Pub/Sub topic with Cloud Storage Ingestion Settings."""
    # [START pubsub_create_topic_with_cloud_storage_ingestion]
    from google.cloud import pubsub_v1
    from google.protobuf import timestamp_pb2
    from google.pubsub_v1.types import Topic
    from google.pubsub_v1.types import IngestionDataSourceSettings

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # bucket = "your-bucket"
    # input_format = "text"  (can be one of "text", "avro", "pubsub_avro")
    # text_delimiter = "\n"
    # match_glob = "**.txt"
    # minimum_object_create_time = "YYYY-MM-DDThh:mm:ssZ"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    cloud_storage_settings = IngestionDataSourceSettings.CloudStorage(
        bucket=bucket,
    )
    if input_format == "text":
        cloud_storage_settings.text_format = (
            IngestionDataSourceSettings.CloudStorage.TextFormat(
                delimiter=text_delimiter
            )
        )
    elif input_format == "avro":
        cloud_storage_settings.avro_format = (
            IngestionDataSourceSettings.CloudStorage.AvroFormat()
        )
    elif input_format == "pubsub_avro":
        cloud_storage_settings.pubsub_avro_format = (
            IngestionDataSourceSettings.CloudStorage.PubSubAvroFormat()
        )
    else:
        print(
            "Invalid input_format: "
            + input_format
            + "; must be in ('text', 'avro', 'pubsub_avro')"
        )
        return

    if match_glob:
        cloud_storage_settings.match_glob = match_glob

    if minimum_object_create_time:
        try:
            minimum_object_create_time_timestamp = timestamp_pb2.Timestamp()
            minimum_object_create_time_timestamp.FromJsonString(
                minimum_object_create_time
            )
            cloud_storage_settings.minimum_object_create_time = (
                minimum_object_create_time_timestamp
            )
        except ValueError:
            print("Invalid minimum_object_create_time: " + minimum_object_create_time)
            return

    request = Topic(
        name=topic_path,
        ingestion_data_source_settings=IngestionDataSourceSettings(
            cloud_storage=cloud_storage_settings,
        ),
    )

    topic = publisher.create_topic(request=request)

    print(f"Created topic: {topic.name} with Cloud Storage Ingestion Settings")
    # [END pubsub_create_topic_with_cloud_storage_ingestion]


def create_topic_with_aws_msk_ingestion(
    project_id: str,
    topic_id: str,
    cluster_arn: str,
    msk_topic: str,
    aws_role_arn: str,
    gcp_service_account: str,
) -> None:
    """Create a new Pub/Sub topic with AWS MSK Ingestion Settings."""
    # [START pubsub_create_topic_with_aws_msk_ingestion]
    from google.cloud import pubsub_v1
    from google.pubsub_v1.types import Topic
    from google.pubsub_v1.types import IngestionDataSourceSettings

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # cluster_arn = "your-cluster-arn"
    # msk_topic = "your-msk-topic"
    # aws_role_arn = "your-aws-role-arn"
    # gcp_service_account = "your-gcp-service-account"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    request = Topic(
        name=topic_path,
        ingestion_data_source_settings=IngestionDataSourceSettings(
            aws_msk=IngestionDataSourceSettings.AwsMsk(
                cluster_arn=cluster_arn,
                topic=msk_topic,
                aws_role_arn=aws_role_arn,
                gcp_service_account=gcp_service_account,
            )
        ),
    )

    topic = publisher.create_topic(request=request)

    print(f"Created topic: {topic.name} with AWS MSK Ingestion Settings")
    # [END pubsub_create_topic_with_aws_msk_ingestion]


def create_topic_with_azure_event_hubs_ingestion(
    project_id: str,
    topic_id: str,
    resource_group: str,
    namespace: str,
    event_hub: str,
    client_id: str,
    tenant_id: str,
    subscription_id: str,
    gcp_service_account: str,
) -> None:
    """Create a new Pub/Sub topic with Azure Event Hubs Ingestion Settings."""
    # [START pubsub_create_topic_with_azure_event_hubs_ingestion]
    from google.cloud import pubsub_v1
    from google.pubsub_v1.types import Topic
    from google.pubsub_v1.types import IngestionDataSourceSettings

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # resource_group = "your-resource-group"
    # namespace = "your-namespace"
    # event_hub = "your-event-hub"
    # client_id = "your-client-id"
    # tenant_id = "your-tenant-id"
    # subscription_id = "your-subscription-id"
    # gcp_service_account = "your-gcp-service-account"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    request = Topic(
        name=topic_path,
        ingestion_data_source_settings=IngestionDataSourceSettings(
            azure_event_hubs=IngestionDataSourceSettings.AzureEventHubs(
                resource_group=resource_group,
                namespace=namespace,
                event_hub=event_hub,
                client_id=client_id,
                tenant_id=tenant_id,
                subscription_id=subscription_id,
                gcp_service_account=gcp_service_account,
            )
        ),
    )

    topic = publisher.create_topic(request=request)

    print(f"Created topic: {topic.name} with Azure Event Hubs Ingestion Settings")
    # [END pubsub_create_topic_with_azure_event_hubs_ingestion]


def create_topic_with_confluent_cloud_ingestion(
    project_id: str,
    topic_id: str,
    bootstrap_server: str,
    cluster_id: str,
    confluent_topic: str,
    identity_pool_id: str,
    gcp_service_account: str,
) -> None:
    """Create a new Pub/Sub topic with Confluent Cloud Ingestion Settings."""
    # [START pubsub_create_topic_with_confluent_cloud_ingestion]
    from google.cloud import pubsub_v1
    from google.pubsub_v1.types import Topic
    from google.pubsub_v1.types import IngestionDataSourceSettings

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # bootstrap_server = "your-bootstrap-server"
    # cluster_id = "your-cluster-id"
    # confluent_topic = "your-confluent-topic"
    # identity_pool_id = "your-identity-pool-id"
    # gcp_service_account = "your-gcp-service-account"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    request = Topic(
        name=topic_path,
        ingestion_data_source_settings=IngestionDataSourceSettings(
            confluent_cloud=IngestionDataSourceSettings.ConfluentCloud(
                bootstrap_server=bootstrap_server,
                cluster_id=cluster_id,
                topic=confluent_topic,
                identity_pool_id=identity_pool_id,
                gcp_service_account=gcp_service_account,
            )
        ),
    )

    topic = publisher.create_topic(request=request)

    print(f"Created topic: {topic.name} with Confluent Cloud Ingestion Settings")
    # [END pubsub_create_topic_with_confluent_cloud_ingestion]


def create_topic_with_smt(
    project_id: str,
    topic_id: str,
) -> None:
    """Create a new Pub/Sub topic with a UDF SMT."""
    # [START pubsub_create_topic_with_smt]
    from google.cloud import pubsub_v1
    from google.pubsub_v1.types import JavaScriptUDF, MessageTransform, Topic

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    code = """function redactSSN(message, metadata) {
                const data = JSON.parse(message.data);
                delete data['ssn'];
                message.data = JSON.stringify(data);
                return message;
                }"""
    udf = JavaScriptUDF(code=code, function_name="redactSSN")
    transforms = [MessageTransform(javascript_udf=udf)]

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    request = Topic(name=topic_path, message_transforms=transforms)

    topic = publisher.create_topic(request=request)

    print(f"Created topic: {topic.name} with SMT")
    # [END pubsub_create_topic_with_smt]


def update_topic_type(
    project_id: str,
    topic_id: str,
    stream_arn: str,
    consumer_arn: str,
    aws_role_arn: str,
    gcp_service_account: str,
) -> None:
    """Update Pub/Sub topic with AWS Kinesis Ingestion Settings."""
    # [START pubsub_update_topic_type]
    from google.cloud import pubsub_v1
    from google.pubsub_v1.types import Topic
    from google.pubsub_v1.types import IngestionDataSourceSettings
    from google.pubsub_v1.types import UpdateTopicRequest
    from google.protobuf import field_mask_pb2

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # stream_arn = "your-stream-arn"
    # consumer_arn = "your-consumer-arn"
    # aws_role_arn = "your-aws-role-arn"
    # gcp_service_account = "your-gcp-service-account"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    update_request = UpdateTopicRequest(
        topic=Topic(
            name=topic_path,
            ingestion_data_source_settings=IngestionDataSourceSettings(
                aws_kinesis=IngestionDataSourceSettings.AwsKinesis(
                    stream_arn=stream_arn,
                    consumer_arn=consumer_arn,
                    aws_role_arn=aws_role_arn,
                    gcp_service_account=gcp_service_account,
                )
            ),
        ),
        update_mask=field_mask_pb2.FieldMask(paths=["ingestion_data_source_settings"]),
    )

    topic = publisher.update_topic(request=update_request)
    print(f"Updated topic: {topic.name} with AWS Kinesis Ingestion Settings")


# [END pubsub_update_topic_type]


def delete_topic(project_id: str, topic_id: str) -> None:
    """Deletes an existing Pub/Sub topic."""
    # [START pubsub_delete_topic]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    publisher.delete_topic(request={"topic": topic_path})

    print(f"Topic deleted: {topic_path}")
    # [END pubsub_delete_topic]


def pubsub_publish_otel_tracing(
    topic_project_id: str, trace_project_id: str, topic_id: str
) -> None:
    """
    Publish to `topic_id` in `topic_project_id` with OpenTelemetry enabled.
    Export the OpenTelemetry traces to Google Cloud Trace in project
    `trace_project_id`

    Args:
        topic_project_id: project ID of the topic to publish to.
        trace_project_id: project ID to export Cloud Trace to.
        topic_id: topic ID to publish to.

    Returns:
        None
    """
    # [START pubsub_publish_otel_tracing]

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
    )
    from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
    from opentelemetry.sdk.trace.sampling import TraceIdRatioBased, ParentBased

    from google.cloud.pubsub_v1 import PublisherClient
    from google.cloud.pubsub_v1.types import PublisherOptions

    # TODO(developer)
    # topic_project_id = "your-topic-project-id"
    # trace_project_id = "your-trace-project-id"
    # topic_id = "your-topic-id"

    # In this sample, we use a Google Cloud Trace to export the OpenTelemetry
    # traces: https://cloud.google.com/trace/docs/setup/python-ot
    # Choose and configure the exporter for your set up accordingly.

    sampler = ParentBased(root=TraceIdRatioBased(1))
    trace.set_tracer_provider(TracerProvider(sampler=sampler))

    # Export to Google Trace.
    cloud_trace_exporter = CloudTraceSpanExporter(
        project_id=trace_project_id,
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(cloud_trace_exporter)
    )

    # Set the `enable_open_telemetry_tracing` option to True when creating
    # the publisher client. This in itself is necessary and sufficient for
    # the library to export OpenTelemetry traces. However, where the traces
    # must be exported to needs to be configured based on your OpenTelemetry
    # set up. Refer: https://opentelemetry.io/docs/languages/python/exporters/
    publisher = PublisherClient(
        publisher_options=PublisherOptions(
            enable_open_telemetry_tracing=True,
        ),
    )

    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(topic_project_id, topic_id)
    # Publish messages.
    for n in range(1, 10):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data)
        print(future.result())

    print(f"Published messages to {topic_path}.")

    # [END pubsub_publish_otel_tracing]


def publish_messages(project_id: str, topic_id: str) -> None:
    """Publishes multiple messages to a Pub/Sub topic."""
    # [START pubsub_quickstart_publisher]
    # [START pubsub_publish]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    for n in range(1, 10):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data)
        print(future.result())

    print(f"Published messages to {topic_path}.")
    # [END pubsub_quickstart_publisher]
    # [END pubsub_publish]


def publish_messages_with_custom_attributes(project_id: str, topic_id: str) -> None:
    """Publishes multiple messages with custom attributes
    to a Pub/Sub topic."""
    # [START pubsub_publish_custom_attributes]
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    for n in range(1, 10):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        # Add two attributes, origin and username, to the message
        future = publisher.publish(
            topic_path, data, origin="python-sample", username="gcp"
        )
        print(future.result())

    print(f"Published messages with custom attributes to {topic_path}.")
    # [END pubsub_publish_custom_attributes]


def publish_messages_with_error_handler(project_id: str, topic_id: str) -> None:
    # [START pubsub_publish_with_error_handler]
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    from concurrent import futures
    from google.cloud import pubsub_v1
    from typing import Callable

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    publish_futures = []

    def get_callback(
        publish_future: pubsub_v1.publisher.futures.Future, data: str
    ) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
        def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
            try:
                # Wait 60 seconds for the publish call to succeed.
                print(publish_future.result(timeout=60))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")

        return callback

    for i in range(10):
        data = str(i)
        # When you publish a message, the client returns a future.
        publish_future = publisher.publish(topic_path, data.encode("utf-8"))
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)

    # Wait for all the publish futures to resolve before exiting.
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with error handler to {topic_path}.")
    # [END pubsub_publish_with_error_handler]


def publish_messages_with_batch_settings(project_id: str, topic_id: str) -> None:
    """Publishes multiple messages to a Pub/Sub topic with batch settings."""
    # [START pubsub_publisher_batch_settings]
    from concurrent import futures
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    # Configure the batch to publish as soon as there are 10 messages
    # or 1 KiB of data, or 1 second has passed.
    batch_settings = pubsub_v1.types.BatchSettings(
        max_messages=10,  # default 100
        max_bytes=1024,  # default 1 MB
        max_latency=1,  # default 10 ms
    )
    publisher = pubsub_v1.PublisherClient(batch_settings)
    topic_path = publisher.topic_path(project_id, topic_id)
    publish_futures = []

    # Resolve the publish future in a separate thread.
    def callback(future: pubsub_v1.publisher.futures.Future) -> None:
        message_id = future.result()
        print(message_id)

    for n in range(1, 10):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        publish_future = publisher.publish(topic_path, data)
        # Non-blocking. Allow the publisher client to batch multiple messages.
        publish_future.add_done_callback(callback)
        publish_futures.append(publish_future)

    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with batch settings to {topic_path}.")
    # [END pubsub_publisher_batch_settings]


def publish_messages_with_flow_control_settings(project_id: str, topic_id: str) -> None:
    """Publishes messages to a Pub/Sub topic with flow control settings."""
    # [START pubsub_publisher_flow_control]
    from concurrent import futures
    from google.cloud import pubsub_v1
    from google.cloud.pubsub_v1.types import (
        LimitExceededBehavior,
        PublisherOptions,
        PublishFlowControl,
    )

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    # Configure how many messages the publisher client can hold in memory
    # and what to do when messages exceed the limit.
    flow_control_settings = PublishFlowControl(
        message_limit=100,  # 100 messages
        byte_limit=10 * 1024 * 1024,  # 10 MiB
        limit_exceeded_behavior=LimitExceededBehavior.BLOCK,
    )
    publisher = pubsub_v1.PublisherClient(
        publisher_options=PublisherOptions(flow_control=flow_control_settings)
    )
    topic_path = publisher.topic_path(project_id, topic_id)
    publish_futures = []

    # Resolve the publish future in a separate thread.
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        message_id = publish_future.result()
        print(message_id)

    # Publish 1000 messages in quick succession may be constrained by
    # publisher flow control.
    for n in range(1, 1000):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        publish_future = publisher.publish(topic_path, data)
        # Non-blocking. Allow the publisher client to batch messages.
        publish_future.add_done_callback(callback)
        publish_futures.append(publish_future)

    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published messages with flow control settings to {topic_path}.")
    # [END pubsub_publisher_flow_control]


def publish_messages_with_retry_settings(project_id: str, topic_id: str) -> None:
    """Publishes messages with custom retry settings."""
    # [START pubsub_publisher_retry_settings]
    from google import api_core
    from google.cloud import pubsub_v1

    # TODO(developer)
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    # Configure the retry settings. Defaults shown in comments are values applied
    # by the library by default, instead of default values in the Retry object.
    custom_retry = api_core.retry.Retry(
        initial=0.250,  # seconds (default: 0.1)
        maximum=90.0,  # seconds (default: 60.0)
        multiplier=1.45,  # default: 1.3
        deadline=300.0,  # seconds (default: 60.0)
        predicate=api_core.retry.if_exception_type(
            api_core.exceptions.Aborted,
            api_core.exceptions.DeadlineExceeded,
            api_core.exceptions.InternalServerError,
            api_core.exceptions.ResourceExhausted,
            api_core.exceptions.ServiceUnavailable,
            api_core.exceptions.Unknown,
            api_core.exceptions.Cancelled,
        ),
    )

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    for n in range(1, 10):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        future = publisher.publish(topic=topic_path, data=data, retry=custom_retry)
        print(future.result())

    print(f"Published messages with retry settings to {topic_path}.")
    # [END pubsub_publisher_retry_settings]


def publish_with_ordering_keys(project_id: str, topic_id: str) -> None:
    """Publishes messages with ordering keys."""
    # [START pubsub_publish_with_ordering_keys]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
    # Sending messages to the same region ensures they are received in order
    # even when multiple publishers are used.
    client_options = {"api_endpoint": "us-east1-pubsub.googleapis.com:443"}
    publisher = pubsub_v1.PublisherClient(
        publisher_options=publisher_options, client_options=client_options
    )
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    for message in [
        ("message1", "key1"),
        ("message2", "key2"),
        ("message3", "key1"),
        ("message4", "key2"),
    ]:
        # Data must be a bytestring
        data = message[0].encode("utf-8")
        ordering_key = message[1]
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data, ordering_key=ordering_key)
        print(future.result())

    print(f"Published messages with ordering keys to {topic_path}.")
    # [END pubsub_publish_with_ordering_keys]


def resume_publish_with_ordering_keys(project_id: str, topic_id: str) -> None:
    """Resume publishing messages with ordering keys when unrecoverable errors occur."""
    # [START pubsub_resume_publish_with_ordering_keys]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
    # Sending messages to the same region ensures they are received in order
    # even when multiple publishers are used.
    client_options = {"api_endpoint": "us-east1-pubsub.googleapis.com:443"}
    publisher = pubsub_v1.PublisherClient(
        publisher_options=publisher_options, client_options=client_options
    )
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_id}`
    topic_path = publisher.topic_path(project_id, topic_id)

    for message in [
        ("message1", "key1"),
        ("message2", "key2"),
        ("message3", "key1"),
        ("message4", "key2"),
    ]:
        # Data must be a bytestring
        data = message[0].encode("utf-8")
        ordering_key = message[1]
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data, ordering_key=ordering_key)
        try:
            print(future.result())
        except RuntimeError:
            # Resume publish on an ordering key that has had unrecoverable errors.
            publisher.resume_publish(topic_path, ordering_key)

    print(f"Resumed publishing messages with ordering keys to {topic_path}.")
    # [END pubsub_resume_publish_with_ordering_keys]


def detach_subscription(project_id: str, subscription_id: str) -> None:
    """Detaches a subscription from a topic and drops all messages retained in it."""
    # [START pubsub_detach_subscription]
    from google.api_core.exceptions import GoogleAPICallError, RetryError
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing subscription.
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    publisher_client = pubsub_v1.PublisherClient()
    subscriber_client = pubsub_v1.SubscriberClient()
    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    try:
        publisher_client.detach_subscription(
            request={"subscription": subscription_path}
        )
    except (GoogleAPICallError, RetryError, ValueError, Exception) as err:
        print(err)

    subscription = subscriber_client.get_subscription(
        request={"subscription": subscription_path}
    )
    if subscription.detached:
        print(f"{subscription_path} is detached.")
    else:
        print(f"{subscription_path} is NOT detached.")
    # [END pubsub_detach_subscription]


if __name__ == "__main__":  # noqa: C901
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help=list_topics.__doc__)

    create_parser = subparsers.add_parser("create", help=create_topic.__doc__)
    create_parser.add_argument("topic_id")

    pubsub_publish_otel_tracing_parser = subparsers.add_parser(
        "pubsub-publish-otel-tracing", help=pubsub_publish_otel_tracing.__doc__
    )
    pubsub_publish_otel_tracing_parser.add_argument("topic_project_id")
    pubsub_publish_otel_tracing_parser.add_argument("trace_project_id")
    pubsub_publish_otel_tracing_parser.add_argument("topic_id")

    create_topic_with_kinesis_ingestion_parser = subparsers.add_parser(
        "create_kinesis_ingestion", help=create_topic_with_kinesis_ingestion.__doc__
    )
    create_topic_with_kinesis_ingestion_parser.add_argument("topic_id")
    create_topic_with_kinesis_ingestion_parser.add_argument("stream_arn")
    create_topic_with_kinesis_ingestion_parser.add_argument("consumer_arn")
    create_topic_with_kinesis_ingestion_parser.add_argument("aws_role_arn")
    create_topic_with_kinesis_ingestion_parser.add_argument("gcp_service_account")

    create_topic_with_cloud_storage_ingestion_parser = subparsers.add_parser(
        "create_cloud_storage_ingestion",
        help=create_topic_with_cloud_storage_ingestion.__doc__,
    )
    create_topic_with_cloud_storage_ingestion_parser.add_argument("topic_id")
    create_topic_with_cloud_storage_ingestion_parser.add_argument("bucket")
    create_topic_with_cloud_storage_ingestion_parser.add_argument("input_format")
    create_topic_with_cloud_storage_ingestion_parser.add_argument("text_delimiter")
    create_topic_with_cloud_storage_ingestion_parser.add_argument("match_glob")
    create_topic_with_cloud_storage_ingestion_parser.add_argument(
        "minimum_object_create_time"
    )

    create_topic_with_aws_msk_ingestion_parser = subparsers.add_parser(
        "create_aws_msk_ingestion", help=create_topic_with_aws_msk_ingestion.__doc__
    )
    create_topic_with_aws_msk_ingestion_parser.add_argument("topic_id")
    create_topic_with_aws_msk_ingestion_parser.add_argument("cluster_arn")
    create_topic_with_aws_msk_ingestion_parser.add_argument("msk_topic")
    create_topic_with_aws_msk_ingestion_parser.add_argument("aws_role_arn")
    create_topic_with_aws_msk_ingestion_parser.add_argument("gcp_service_account")

    create_topic_with_azure_event_hubs_ingestion_parser = subparsers.add_parser(
        "create_azure_event_hubs_ingestion",
        help=create_topic_with_azure_event_hubs_ingestion.__doc__,
    )
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument("topic_id")
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument("resource_group")
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument("namespace")
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument("event_hub")
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument("client_id")
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument("tenant_id")
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument("subscription_id")
    create_topic_with_azure_event_hubs_ingestion_parser.add_argument(
        "gcp_service_account"
    )

    create_topic_with_confluent_cloud_ingestion_parser = subparsers.add_parser(
        "create_confluent_cloud_ingestion",
        help=create_topic_with_confluent_cloud_ingestion.__doc__,
    )
    create_topic_with_confluent_cloud_ingestion_parser.add_argument("topic_id")
    create_topic_with_confluent_cloud_ingestion_parser.add_argument("bootstrap_server")
    create_topic_with_confluent_cloud_ingestion_parser.add_argument("cluster_id")
    create_topic_with_confluent_cloud_ingestion_parser.add_argument("confluent_topic")
    create_topic_with_confluent_cloud_ingestion_parser.add_argument("identity_pool_id")
    create_topic_with_confluent_cloud_ingestion_parser.add_argument(
        "gcp_service_account"
    )

    create_parser = subparsers.add_parser(
        "create_smt", help=create_topic_with_smt.__doc__
    )
    create_parser.add_argument("topic_id")

    update_topic_type_parser = subparsers.add_parser(
        "update_kinesis_ingestion", help=update_topic_type.__doc__
    )
    update_topic_type_parser.add_argument("topic_id")
    update_topic_type_parser.add_argument("stream_arn")
    update_topic_type_parser.add_argument("consumer_arn")
    update_topic_type_parser.add_argument("aws_role_arn")
    update_topic_type_parser.add_argument("gcp_service_account")

    delete_parser = subparsers.add_parser("delete", help=delete_topic.__doc__)
    delete_parser.add_argument("topic_id")

    publish_parser = subparsers.add_parser("publish", help=publish_messages.__doc__)
    publish_parser.add_argument("topic_id")

    publish_with_custom_attributes_parser = subparsers.add_parser(
        "publish-with-custom-attributes",
        help=publish_messages_with_custom_attributes.__doc__,
    )
    publish_with_custom_attributes_parser.add_argument("topic_id")

    publish_with_error_handler_parser = subparsers.add_parser(
        "publish-with-error-handler",
        help=publish_messages_with_error_handler.__doc__,
    )
    publish_with_error_handler_parser.add_argument("topic_id")

    publish_with_batch_settings_parser = subparsers.add_parser(
        "publish-with-batch-settings",
        help=publish_messages_with_batch_settings.__doc__,
    )
    publish_with_batch_settings_parser.add_argument("topic_id")

    publish_with_flow_control_settings_parser = subparsers.add_parser(
        "publish-with-flow-control",
        help=publish_messages_with_flow_control_settings.__doc__,
    )
    publish_with_flow_control_settings_parser.add_argument("topic_id")

    publish_with_retry_settings_parser = subparsers.add_parser(
        "publish-with-retry-settings",
        help=publish_messages_with_retry_settings.__doc__,
    )
    publish_with_retry_settings_parser.add_argument("topic_id")

    publish_with_ordering_keys_parser = subparsers.add_parser(
        "publish-with-ordering-keys",
        help=publish_with_ordering_keys.__doc__,
    )
    publish_with_ordering_keys_parser.add_argument("topic_id")

    resume_publish_with_ordering_keys_parser = subparsers.add_parser(
        "resume-publish-with-ordering-keys",
        help=resume_publish_with_ordering_keys.__doc__,
    )
    resume_publish_with_ordering_keys_parser.add_argument("topic_id")

    detach_subscription_parser = subparsers.add_parser(
        "detach-subscription",
        help=detach_subscription.__doc__,
    )
    detach_subscription_parser.add_argument("subscription_id")

    args = parser.parse_args()

    if args.command == "list":
        list_topics(args.project_id)
    elif args.command == "create":
        create_topic(args.project_id, args.topic_id)
    elif args.command == "create_kinesis_ingestion":
        create_topic_with_kinesis_ingestion(
            args.project_id,
            args.topic_id,
            args.stream_arn,
            args.consumer_arn,
            args.aws_role_arn,
            args.gcp_service_account,
        )
    elif args.command == "create_cloud_storage_ingestion":
        create_topic_with_cloud_storage_ingestion(
            args.project_id,
            args.topic_id,
            args.bucket,
            args.input_format,
            args.text_delimiter,
            args.match_glob,
            args.minimum_object_create_time,
        )
    elif args.command == "create_aws_msk_ingestion":
        create_topic_with_aws_msk_ingestion(
            args.project_id,
            args.topic_id,
            args.cluster_arn,
            args.msk_topic,
            args.aws_role_arn,
            args.gcp_service_account,
        )
    elif args.command == "create_azure_event_hubs_ingestion":
        create_topic_with_azure_event_hubs_ingestion(
            args.project_id,
            args.topic_id,
            args.resource_group,
            args.namespace,
            args.event_hub,
            args.client_id,
            args.tenant_id,
            args.subscription_id,
            args.gcp_service_account,
        )
    elif args.command == "create_confluent_cloud_ingestion":
        create_topic_with_confluent_cloud_ingestion(
            args.project_id,
            args.topic_id,
            args.bootstrap_server,
            args.cluster_id,
            args.confluent_topic,
            args.identity_pool_id,
            args.gcp_service_account,
        )
    elif args.command == "create_smt":
        create_topic_with_smt(
            args.project_id,
            args.topic_id,
        )
    elif args.command == "update_kinesis_ingestion":
        update_topic_type(
            args.project_id,
            args.topic_id,
            args.stream_arn,
            args.consumer_arn,
            args.aws_role_arn,
            args.gcp_service_account,
        )
    elif args.command == "delete":
        delete_topic(args.project_id, args.topic_id)
    elif args.command == "publish":
        publish_messages(args.project_id, args.topic_id)
    elif args.command == "publish-with-custom-attributes":
        publish_messages_with_custom_attributes(args.project_id, args.topic_id)
    elif args.command == "publish-with-error-handler":
        publish_messages_with_error_handler(args.project_id, args.topic_id)
    elif args.command == "publish-with-batch-settings":
        publish_messages_with_batch_settings(args.project_id, args.topic_id)
    elif args.command == "publish-with-flow-control":
        publish_messages_with_flow_control_settings(args.project_id, args.topic_id)
    elif args.command == "publish-with-retry-settings":
        publish_messages_with_retry_settings(args.project_id, args.topic_id)
    elif args.command == "publish-with-ordering-keys":
        publish_with_ordering_keys(args.project_id, args.topic_id)
    elif args.command == "resume-publish-with-ordering-keys":
        resume_publish_with_ordering_keys(args.project_id, args.topic_id)
    elif args.command == "detach-subscription":
        detach_subscription(args.project_id, args.subscription_id)
    elif args.command == "pubsub-publish-otel-tracing":
        pubsub_publish_otel_tracing(
            args.topic_project_id, args.trace_project_id, args.topic_id
        )
