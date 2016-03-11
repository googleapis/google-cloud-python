# Copyright 2016 Google Inc. All rights reserved.
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


class Test_logger_name_from_path(unittest2.TestCase):

    def _callFUT(self, path, project):
        from gcloud.logging._helpers import logger_name_from_path
        return logger_name_from_path(path, project)

    def test_w_simple_name(self):
        LOGGER_NAME = 'LOGGER_NAME'
        PROJECT = 'my-project-1234'
        PATH = 'projects/%s/logs/%s' % (PROJECT, LOGGER_NAME)
        logger_name = self._callFUT(PATH, PROJECT)
        self.assertEqual(logger_name, LOGGER_NAME)

    def test_w_name_w_all_extras(self):
        LOGGER_NAME = 'LOGGER_NAME-part.one~part.two%part-three'
        PROJECT = 'my-project-1234'
        PATH = 'projects/%s/logs/%s' % (PROJECT, LOGGER_NAME)
        logger_name = self._callFUT(PATH, PROJECT)
        self.assertEqual(logger_name, LOGGER_NAME)
