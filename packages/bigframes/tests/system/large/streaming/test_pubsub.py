# Copyright 2025 Google LLC
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

from concurrent import futures
from typing import Generator
import uuid

import pytest

import bigframes

pytest.importorskip("google.cloud.pubsub")
from google.cloud import pubsub  # type: ignore # noqa


def resource_name_full(project_id: str, resource_type: str, resource_id: str):
    """Used for bigtable or pubsub resources."""
    return f"projects/{project_id}/{resource_type}/{resource_id}"


@pytest.fixture(scope="function")
def pubsub_topic_id(session_load: bigframes.Session) -> Generator[str, None, None]:
    publisher = pubsub.PublisherClient()
    topic_id = "bigframes_test_topic_" + uuid.uuid4().hex

    topic_name = resource_name_full(session_load._project, "topics", topic_id)

    publisher.create_topic(name=topic_name)
    yield topic_id
    publisher.delete_topic(topic=topic_name)


@pytest.fixture(scope="function")
def pubsub_topic_subscription_ids(
    session_load: bigframes.Session, pubsub_topic_id: str
) -> Generator[tuple[str, str], None, None]:
    subscriber = pubsub.SubscriberClient()
    subscription_id = "bigframes_test_subscription_" + uuid.uuid4().hex

    subscription_name = resource_name_full(
        session_load._project, "subscriptions", subscription_id
    )
    topic_name = resource_name_full(session_load._project, "topics", pubsub_topic_id)

    subscriber.create_subscription(name=subscription_name, topic=topic_name)
    yield (pubsub_topic_id, subscription_id)
    subscriber.delete_subscription(subscription=subscription_name)


@pytest.mark.flaky(retries=3, delay=10)
def test_streaming_df_to_pubsub(
    session_load: bigframes.Session, pubsub_topic_subscription_ids: tuple[str, str]
):
    topic_id, subscription_id = pubsub_topic_subscription_ids

    subscriber = pubsub.SubscriberClient()

    subscription_name = "projects/{project_id}/subscriptions/{sub}".format(
        project_id=session_load._project,
        sub=subscription_id,
    )

    # launch a continuous query
    job_id_prefix = "test_streaming_pubsub_"
    sdf = session_load.read_gbq_table_streaming("birds.penguins_bigtable_streaming")

    sdf = sdf[sdf["body_mass_g"] < 4000]
    sdf = sdf[["island"]]

    try:

        def counter(func):
            def wrapper(*args, **kwargs):
                wrapper.count += 1  # type: ignore
                return func(*args, **kwargs)

            wrapper.count = 0  # type: ignore
            return wrapper

        @counter
        def callback(message):
            message.ack()

        future = subscriber.subscribe(subscription_name, callback)

        query_job = sdf.to_pubsub(
            topic=topic_id,
            service_account_email="streaming-testing@bigframes-load-testing.iam.gserviceaccount.com",
            job_id=None,
            job_id_prefix=job_id_prefix,
        )
        try:
            # wait 100 seconds in order to ensure the query doesn't stop
            # (i.e. it is continuous)
            future.result(timeout=100)
        except futures.TimeoutError:
            future.cancel()
        assert query_job.running()
        assert query_job.error_result is None
        assert str(query_job.job_id).startswith(job_id_prefix)
        assert callback.count > 0  # type: ignore
    finally:
        query_job.cancel()
