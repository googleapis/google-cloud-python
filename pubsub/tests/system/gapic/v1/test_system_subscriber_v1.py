# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import mock
import pytest

from google.api_core import exceptions
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.gapic import subscriber_client_config


@pytest.fixture(scope="module")
def invalid_credentials_file():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(script_dir, "assets", "project-credentials-invalid.json")
    return config_file


class TestSystemSubscriber(object):
    def test_no_account_no_retry_timeout_sync(self, invalid_credentials_file):
        messaging_config = subscriber_client_config.config["interfaces"][
            "google.pubsub.v1.Subscriber"
        ]["retry_params"]["messaging"]

        with mock.patch.dict(messaging_config, total_timeout_millis=10000):
            client = pubsub_v1.SubscriberClient.from_service_account_json(
                invalid_credentials_file
            )

        project_id = os.environ["PROJECT_ID"]
        subscription_name = "foo_events"
        subscription_path = client.subscription_path(project_id, subscription_name)

        # If the client tries to retry the failed request, the assertion below
        # will fail with a timeout (RefreshError).
        with pytest.raises(exceptions.ServiceUnavailable):
            client.pull(subscription_path, max_messages=100)

    def test_no_account_no_retry_timeout_async(self, invalid_credentials_file):
        client = pubsub_v1.SubscriberClient.from_service_account_json(
            invalid_credentials_file
        )

        project_id = os.environ["PROJECT_ID"]
        subscription_name = "foo_events"
        subscription_path = client.subscription_path(project_id, subscription_name)

        future = client.subscribe(subscription_path, callback=lambda msg: None)

        with pytest.raises(exceptions.ServiceUnavailable):
            future.result(timeout=10)
