# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.auth
import google.auth.credentials
import google.auth.transport.grpc
from google.cloud.gapic.pubsub.v1 import publisher_api


def test_grpc_request(http_request):
    credentials, project_id = google.auth.default()
    credentials = google.auth.credentials.with_scopes_if_required(
        credentials, ['https://www.googleapis.com/auth/pubsub'])

    target = '{}:{}'.format(
        publisher_api.PublisherApi.SERVICE_ADDRESS,
        publisher_api.PublisherApi.DEFAULT_SERVICE_PORT)

    channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, target, http_request)

    # Create a pub/sub client.
    client = publisher_api.PublisherApi(channel=channel)

    # list the topics and drain the iterator to test that an authorized API
    # call works.
    list_topics_iter = client.list_topics(
        project='projects/{}'.format(project_id))
    list(list_topics_iter)
