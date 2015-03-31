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

import time

import unittest2

from gcloud import _helpers
from gcloud import pubsub
from gcloud.pubsub.topic import Topic


_helpers._PROJECT_ENV_VAR_NAME = 'GCLOUD_TESTS_PROJECT_ID'
pubsub.set_defaults()


class TestPubsubTopics(unittest2.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_create_topic(self):
        new_topic_name = 'a-new-topic'
        topic = Topic(new_topic_name)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        self.assertTrue(topic.exists())
        self.assertEqual(topic.name, new_topic_name)

    def test_list_topics(self):
        topics_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        created_topics = []
        for topic_name in topics_to_create:
            topic = Topic(topic_name)
            topic.create()
            self.to_delete.append(topic)

        # Retrieve the topics.
        all_topics, _ = pubsub.list_topics()
        project_id = pubsub.get_default_project()
        created_topics = [topic for topic in all_topics
                          if topic.name in topics_to_create and
                          topic.project == project_id]
        self.assertEqual(len(created_topics), len(topics_to_create))
