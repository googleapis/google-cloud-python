# Copyright 2018 Google LLC
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

import unittest

import mock


class Test_should_retry(unittest.TestCase):
    def _call_fut(self, exc):
        from google.cloud.storage.retry import _should_retry

        return _should_retry(exc)

    def test_wo_errors_attribute(self):
        self.assertFalse(self._call_fut(object()))

    def test_w_empty_errors(self):
        exc = mock.Mock(errors=[], spec=["errors"])
        self.assertFalse(self._call_fut(exc))

    def test_w_non_matching_reason(self):
        exc = mock.Mock(errors=[{"reason": "bogus"}], spec=["errors"])
        self.assertFalse(self._call_fut(exc))

    def test_w_backendError(self):
        exc = mock.Mock(errors=[{"reason": "backendError"}], spec=["errors"])
        self.assertTrue(self._call_fut(exc))

    def test_w_rateLimitExceeded(self):
        exc = mock.Mock(errors=[{"reason": "rateLimitExceeded"}], spec=["errors"])
        self.assertTrue(self._call_fut(exc))

    def test_w_unstructured_too_many_requests(self):
        from google.api_core.exceptions import TooManyRequests

        exc = TooManyRequests("testing")
        self.assertTrue(self._call_fut(exc))

    def test_w_internalError(self):
        exc = mock.Mock(errors=[{"reason": "internalError"}], spec=["errors"])
        self.assertTrue(self._call_fut(exc))

    def test_w_unstructured_internal_server_error(self):
        from google.api_core.exceptions import InternalServerError

        exc = InternalServerError("testing")
        self.assertTrue(self._call_fut(exc))

    def test_w_badGateway(self):
        exc = mock.Mock(errors=[{"reason": "badGateway"}], spec=["errors"])
        self.assertTrue(self._call_fut(exc))

    def test_w_unstructured_bad_gateway(self):
        from google.api_core.exceptions import BadGateway

        exc = BadGateway("testing")
        self.assertTrue(self._call_fut(exc))
