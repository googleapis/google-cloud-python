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

import mock
import urllib3

import google.auth.transport.urllib3
from tests.transport import compliance


class TestRequestResponse(compliance.RequestResponseTests):
    def make_request(self):
        http = urllib3.PoolManager()
        return google.auth.transport.urllib3.Request(http)


def test_timeout():
    http = mock.Mock()
    request = google.auth.transport.urllib3.Request(http)
    request(url='http://example.com', method='GET', timeout=5)

    assert http.request.call_args[1]['timeout'] == 5
