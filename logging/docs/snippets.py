# Copyright 2016 Google LLC
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

"""Testable usage examples for Stackdriver Logging API wrapper

Each example function takes a ``client`` argument (which must be an instance
of :class:`google.cloud.logging.client.Client`) and uses it to perform a task
with the API.

To facilitate running the examples as system tests, each example is also passed
a ``to_delete`` list;  the function adds to the list any objects created which
need to be deleted during teardown.
"""

import time

from google.cloud.logging.client import Client


def snippet(func):
    """Mark ``func`` as a snippet example function."""
    func._snippet = True
    return func


def _millis():
    return time.time() * 1000


def do_something_with(item):  # pylint: disable=unused-argument
    pass


# pylint: disable=reimported,unused-variable,unused-argument
@snippet
def instantiate_client(_unused_client, _unused_to_delete):
    """Instantiate client."""

    # [START client_create_default]
    from google.cloud import logging

    client = logging.Client()
    # [END client_create_default]

    credentials = object()
    # [START client_create_explicit]
    from google.cloud import logging

    client = logging.Client(project="my-project", credentials=credentials)
    # [END client_create_explicit]


# pylint: enable=reimported,unused-variable,unused-argument


@snippet
def client_list_entries(client, to_delete):  # pylint: disable=unused-argument
    """List entries via client."""

    # [START client_list_entries_default]
    for entry in client.list_entries():  # API call(s)
        do_something_with(entry)
    # [END client_list_entries_default]

    # [START client_list_entries_filter]
    FILTER = "logName:log_name AND textPayload:simple"
    for entry in client.list_entries(filter_=FILTER):  # API call(s)
        do_something_with(entry)
    # [END client_list_entries_filter]

    # [START client_list_entries_order_by]
    from google.cloud.logging import DESCENDING

    for entry in client.list_entries(order_by=DESCENDING):  # API call(s)
        do_something_with(entry)
    # [END client_list_entries_order_by]

    # [START client_list_entries_paged]
    iterator = client.list_entries()
    pages = iterator.pages

    page1 = next(pages)  # API call
    for entry in page1:
        do_something_with(entry)

    page2 = next(pages)  # API call
    for entry in page2:
        do_something_with(entry)
    # [END client_list_entries_paged]


# @snippet  Commented because we need real project IDs to test
def client_list_entries_multi_project(
    client, to_delete
):  # pylint: disable=unused-argument
    """List entries via client across multiple projects."""

    # [START client_list_entries_multi_project]
    PROJECT_IDS = ["one-project", "another-project"]
    for entry in client.list_entries(project_ids=PROJECT_IDS):  # API call(s)
        do_something_with(entry)
    # [END client_list_entries_multi_project]


@snippet
def logger_usage(client, to_delete):
    """Logger usage."""
    LOG_NAME = "logger_usage_%d" % (_millis())

    # [START logger_create]
    logger = client.logger(LOG_NAME)
    # [END logger_create]
    to_delete.append(logger)

    # [START logger_log_text]
    logger.log_text("A simple entry")  # API call
    # [END logger_log_text]

    # [START logger_log_struct]
    logger.log_struct(
        {"message": "My second entry", "weather": "partly cloudy"}
    )  # API call
    # [END logger_log_struct]

    # [START logger_list_entries]
    from google.cloud.logging import DESCENDING

    for entry in logger.list_entries(order_by=DESCENDING):  # API call(s)
        do_something_with(entry)
    # [END logger_list_entries]

    def _logger_delete():
        # [START logger_delete]
        logger.delete()  # API call
        # [END logger_delete]

    _backoff_not_found(_logger_delete)
    to_delete.remove(logger)


@snippet
def metric_crud(client, to_delete):
    """Metric CRUD."""
    METRIC_NAME = "robots-%d" % (_millis(),)
    DESCRIPTION = "Robots all up in your server"
    FILTER = "logName:apache-access AND textPayload:robot"
    UPDATED_FILTER = "textPayload:robot"
    UPDATED_DESCRIPTION = "Danger, Will Robinson!"

    # [START client_list_metrics]
    for metric in client.list_metrics():  # API call(s)
        do_something_with(metric)
    # [END client_list_metrics]

    # [START metric_create]
    metric = client.metric(METRIC_NAME, filter_=FILTER, description=DESCRIPTION)
    assert not metric.exists()  # API call
    metric.create()  # API call
    assert metric.exists()  # API call
    # [END metric_create]
    to_delete.append(metric)

    # [START metric_reload]
    existing_metric = client.metric(METRIC_NAME)
    existing_metric.reload()  # API call
    # [END metric_reload]
    assert existing_metric.filter_ == FILTER
    assert existing_metric.description == DESCRIPTION

    # [START metric_update]
    existing_metric.filter_ = UPDATED_FILTER
    existing_metric.description = UPDATED_DESCRIPTION
    existing_metric.update()  # API call
    # [END metric_update]
    existing_metric.reload()
    assert existing_metric.filter_ == UPDATED_FILTER
    assert existing_metric.description == UPDATED_DESCRIPTION

    def _metric_delete():
        # [START metric_delete]
        metric.delete()
        # [END metric_delete]

    _backoff_not_found(_metric_delete)
    to_delete.remove(metric)


def _sink_storage_setup(client):
    from google.cloud import storage

    BUCKET_NAME = "sink-storage-%d" % (_millis(),)
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    bucket.create()

    # [START sink_bucket_permissions]
    bucket.acl.reload()  # API call
    logs_group = bucket.acl.group("cloud-logs@google.com")
    logs_group.grant_owner()
    bucket.acl.add_entity(logs_group)
    bucket.acl.save()  # API call
    # [END sink_bucket_permissions]

    return bucket


@snippet
def sink_storage(client, to_delete):
    """Sink log entries to storage."""
    bucket = _sink_storage_setup(client)
    to_delete.append(bucket)
    SINK_NAME = "robots-storage-%d" % (_millis(),)
    FILTER = "textPayload:robot"

    # [START sink_storage_create]
    DESTINATION = "storage.googleapis.com/%s" % (bucket.name,)
    sink = client.sink(SINK_NAME, filter_=FILTER, destination=DESTINATION)
    assert not sink.exists()  # API call
    sink.create()  # API call
    assert sink.exists()  # API call
    # [END sink_storage_create]
    to_delete.insert(0, sink)  # delete sink before bucket


def _sink_bigquery_setup(client):
    from google.cloud import bigquery

    DATASET_NAME = "sink_bigquery_%d" % (_millis(),)
    client = bigquery.Client()
    dataset = client.dataset(DATASET_NAME)
    dataset.create()
    dataset.reload()

    # [START sink_dataset_permissions]
    from google.cloud.bigquery.dataset import AccessGrant

    grants = dataset.access_grants
    grants.append(AccessGrant("WRITER", "groupByEmail", "cloud-logs@google.com"))
    dataset.access_grants = grants
    dataset.update()  # API call
    # [END sink_dataset_permissions]

    return dataset


@snippet
def sink_bigquery(client, to_delete):
    """Sink log entries to bigquery."""
    dataset = _sink_bigquery_setup(client)
    to_delete.append(dataset)
    SINK_NAME = "robots-bigquery-%d" % (_millis(),)
    FILTER = "textPayload:robot"

    # [START sink_bigquery_create]
    DESTINATION = "bigquery.googleapis.com%s" % (dataset.path,)
    sink = client.sink(SINK_NAME, filter_=FILTER, destination=DESTINATION)
    assert not sink.exists()  # API call
    sink.create()  # API call
    assert sink.exists()  # API call
    # [END sink_bigquery_create]
    to_delete.insert(0, sink)  # delete sink before dataset


def _sink_pubsub_setup(client):
    from google.cloud import pubsub

    TOPIC_NAME = "sink-pubsub-%d" % (_millis(),)
    client = pubsub.Client()
    topic = client.topic(TOPIC_NAME)
    topic.create()

    # [START sink_topic_permissions]
    policy = topic.get_iam_policy()  # API call
    policy.owners.add(policy.group("cloud-logs@google.com"))
    topic.set_iam_policy(policy)  # API call
    # [END sink_topic_permissions]

    return topic


@snippet
def sink_pubsub(client, to_delete):
    """Sink log entries to pubsub."""
    topic = _sink_pubsub_setup(client)
    to_delete.append(topic)
    SINK_NAME = "robots-pubsub-%d" % (_millis(),)
    FILTER = "logName:apache-access AND textPayload:robot"
    UPDATED_FILTER = "textPayload:robot"

    # [START sink_pubsub_create]
    DESTINATION = "pubsub.googleapis.com/%s" % (topic.full_name,)
    sink = client.sink(SINK_NAME, filter_=FILTER, destination=DESTINATION)
    assert not sink.exists()  # API call
    sink.create()  # API call
    assert sink.exists()  # API call
    # [END sink_pubsub_create]
    to_delete.insert(0, sink)  # delete sink before topic

    # [START client_list_sinks]
    for sink in client.list_sinks():  # API call(s)
        do_something_with(sink)
    # [END client_list_sinks]

    # [START sink_reload]
    existing_sink = client.sink(SINK_NAME)
    existing_sink.reload()
    # [END sink_reload]
    assert existing_sink.filter_ == FILTER
    assert existing_sink.destination == DESTINATION

    # [START sink_update]
    existing_sink.filter_ = UPDATED_FILTER
    existing_sink.update()
    # [END sink_update]
    existing_sink.reload()
    assert existing_sink.filter_ == UPDATED_FILTER

    # [START sink_delete]
    sink.delete()
    # [END sink_delete]
    to_delete.pop(0)


@snippet
def logging_handler(client):
    # [START create_default_handler]
    import logging

    handler = client.get_default_handler()
    cloud_logger = logging.getLogger("cloudLogger")
    cloud_logger.setLevel(logging.INFO)
    cloud_logger.addHandler(handler)
    cloud_logger.error("bad news")
    # [END create_default_handler]

    # [START create_cloud_handler]
    from google.cloud.logging.handlers import CloudLoggingHandler

    handler = CloudLoggingHandler(client)
    cloud_logger = logging.getLogger("cloudLogger")
    cloud_logger.setLevel(logging.INFO)
    cloud_logger.addHandler(handler)
    cloud_logger.error("bad news")
    # [END create_cloud_handler]

    # [START create_named_handler]
    handler = CloudLoggingHandler(client, name="mycustomlog")
    # [END create_named_handler]


@snippet
def setup_logging(client):
    import logging

    # [START setup_logging]
    client.setup_logging(log_level=logging.INFO)
    # [END setup_logging]

    # [START setup_logging_excludes]
    client.setup_logging(log_level=logging.INFO, excluded_loggers=("werkzeug",))
    # [END setup_logging_excludes]


def _line_no(func):
    return func.__code__.co_firstlineno


def _find_examples():
    funcs = [obj for obj in globals().values() if getattr(obj, "_snippet", False)]
    for func in sorted(funcs, key=_line_no):
        yield func


def _name_and_doc(func):
    return func.__name__, func.__doc__


def _backoff_not_found(deleter):
    from google.cloud.exceptions import NotFound

    timeouts = [1, 2, 4, 8, 16]
    while timeouts:
        try:
            deleter()
        except NotFound:
            time.sleep(timeouts.pop(0))
        else:
            break


def main():
    client = Client()
    for example in _find_examples():
        to_delete = []
        print("%-25s: %s" % _name_and_doc(example))
        try:
            example(client, to_delete)
        except AssertionError as failure:
            print("   FAIL: %s" % (failure,))
        except Exception as error:  # pylint: disable=broad-except
            print("  ERROR: %r" % (error,))
        for item in to_delete:
            _backoff_not_found(item.delete)


if __name__ == "__main__":
    main()
