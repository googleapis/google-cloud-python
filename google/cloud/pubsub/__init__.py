# Copyright 2015 Google Inc. All rights reserved.
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

"""Google Cloud Pubsub API wrapper.

The main concepts with this API are:

- :class:`gcloud.pubsub.topic.Topic` represents an endpoint to which messages
  can be published using the Cloud Storage Pubsub API.

- :class:`gcloud.pubsub.subscription.Subscription` represents a named
  subscription (either pull or push) to a topic.
"""

from gcloud.pubsub.client import Client
from gcloud.pubsub.connection import Connection
from gcloud.pubsub.subscription import Subscription
from gcloud.pubsub.topic import Topic


SCOPE = Connection.SCOPE
