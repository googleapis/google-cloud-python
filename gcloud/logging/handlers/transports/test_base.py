# Copyright 2016 Google Inc. All Rights Reserved.
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


class TestBaseHandler(unittest2.TestCase):

    PROJECT = 'PROJECT'

    def _getTargetClass(self):
        from gcloud.logging.handlers.transports import Transport
        return Transport

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_send_is_abstract(self):
        client = _Client(self.PROJECT)
        NAME = "python_logger"
        target = self._makeOne(client, NAME)
        self.assertRaises(NotImplementedError, lambda: target.send(None, None))


class _Client(object):

    def __init__(self, project):
        self.project = project
