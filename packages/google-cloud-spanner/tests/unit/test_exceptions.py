# Copyright 2026 Google LLC All rights reserved.
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

"""Tests for Spanner exception handling with request IDs."""

import unittest

from google.api_core.exceptions import Aborted
from google.cloud.spanner_v1.exceptions import wrap_with_request_id


class TestWrapWithRequestId(unittest.TestCase):
    """Test wrap_with_request_id function."""

    def test_wrap_with_request_id_with_google_api_error(self):
        """Test adding request_id to GoogleAPICallError preserves original type."""
        error = Aborted("Transaction aborted")
        request_id = "1.12345.1.0.1.1"

        result = wrap_with_request_id(error, request_id)

        # Should return the same error object (not wrapped)
        self.assertIs(result, error)
        # Should still be the original exception type
        self.assertIsInstance(result, Aborted)
        # Should have request_id attribute
        self.assertEqual(result.request_id, request_id)
        # String representation should include request_id
        self.assertIn(request_id, str(result))
        self.assertIn("Transaction aborted", str(result))

    def test_wrap_with_request_id_without_request_id(self):
        """Test that without request_id, error is returned unchanged."""
        error = Aborted("Transaction aborted")

        result = wrap_with_request_id(error)

        self.assertIs(result, error)
        self.assertFalse(hasattr(result, "request_id"))

    def test_wrap_with_request_id_with_non_google_api_error(self):
        """Test that non-GoogleAPICallError is returned unchanged."""
        error = Exception("Some other error")
        request_id = "1.12345.1.0.1.1"

        result = wrap_with_request_id(error, request_id)

        # Non-GoogleAPICallError should be returned unchanged
        self.assertIs(result, error)
        self.assertFalse(hasattr(result, "request_id"))


if __name__ == "__main__":
    unittest.main()
