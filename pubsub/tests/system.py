# Copyright 2017, Google Inc. All rights reserved.
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

import uuid

import six

from google import auth
from google.cloud import pubsub_v1


def _resource_name(resource_type):
    """Return a randomly selected name for a resource.

    Args:
        resource_type (str): The resource for which a name is being
            generated. Should be singular (e.g. "topic", "subscription")
    """
    return 'projects/{project}/{resource_type}s/st-{random}'.format(
        project=auth.default()[1],
        random=str(uuid.uuid4())[0:8],
        resource_type=resource_type,
    )


def test_publish_messages():
    publisher = pubsub_v1.PublisherClient()
    topic_name = _resource_name('topic')
    futures = []

    try:
        publisher.create_topic(topic_name)
        for i in range(0, 500):
            futures.append(
                publisher.publish(
                    topic_name,
                    b'The hail in Wales falls mainly on the snails.',
                    num=str(i),
                ),
            )
        for future in futures:
            result = future.result()
            assert isinstance(result, (six.text_type, six.binary_type))
    finally:
        publisher.delete_topic(topic_name)
