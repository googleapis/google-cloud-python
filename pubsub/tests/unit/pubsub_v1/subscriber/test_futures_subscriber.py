# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import

import mock

from google.auth import credentials
from google.cloud.pubsub_v1 import subscriber
from google.cloud.pubsub_v1.subscriber import futures
from google.cloud.pubsub_v1.subscriber.policy import thread


def create_policy(**kwargs):
    creds = mock.Mock(spec=credentials.Credentials)
    client = subscriber.Client(credentials=creds)
    return thread.Policy(client, 'sub_name_c', **kwargs)


def create_future(policy=None):
    if policy is None:
        policy = create_policy()
    future = futures.Future(policy=policy)
    policy._future = future
    return future


def test_running():
    policy = create_policy()
    future = create_future(policy=policy)
    assert future.running() is True
    policy._future = None
    assert future.running() is False
