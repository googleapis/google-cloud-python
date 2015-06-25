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

import unittest2


class Test_topic_name_from_path(unittest2.TestCase):

    def _callFUT(self, path, project):
        from gcloud.pubsub._helpers import topic_name_from_path
        return topic_name_from_path(path, project)

    def test_invalid_path_length(self):
        PATH = 'projects/foo'
        PROJECT = None
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT)

    def test_invalid_path_format(self):
        TOPIC_NAME = 'TOPIC_NAME'
        PROJECT = 'PROJECT'
        PATH = 'foo/%s/bar/%s' % (PROJECT, TOPIC_NAME)
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT)

    def test_invalid_project(self):
        TOPIC_NAME = 'TOPIC_NAME'
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        PATH = 'projects/%s/topics/%s' % (PROJECT1, TOPIC_NAME)
        self.assertRaises(ValueError, self._callFUT, PATH, PROJECT2)

    def test_valid_data(self):
        TOPIC_NAME = 'TOPIC_NAME'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        topic_name = self._callFUT(PATH, PROJECT)
        self.assertEqual(topic_name, TOPIC_NAME)
