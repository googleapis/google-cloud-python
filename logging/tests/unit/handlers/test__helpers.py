# Copyright 2017 Google Inc. All Rights Reserved.
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


class TestFlaskTrace(unittest.TestCase):

    def create_app(self):
        import flask

        app = flask.Flask(__name__)

        @app.route('/')
        def index():
            return 'test flask trace'

        return app

    def setUp(self):
        self.app = self.create_app()

    def test_trace_id_no_context_header(self):
        from google.cloud.logging.handlers._helpers import get_trace_id_from_flask
        from google.cloud.logging.handlers._helpers import _EMPTY_TRACE_ID

        with self.app.test_request_context(
                path='/',
                headers={}):
            trace_id = get_trace_id_from_flask()

        self.assertEqual(trace_id, _EMPTY_TRACE_ID)

    def test_trace_id_valid_context_header(self):
        from google.cloud.logging.handlers._helpers import get_trace_id_from_flask

        FLASK_TRACE_HEADER = 'X_CLOUD_TRACE_CONTEXT'
        FLASK_TRACE_ID = 'testtraceid/testspanid'

        with self.app.test_request_context(
                path='/',
                headers={FLASK_TRACE_HEADER:FLASK_TRACE_ID}):
            trace_id = get_trace_id_from_flask()

        EXPECTED_TRACE_ID = 'testtraceid'
        self.assertEqual(trace_id, EXPECTED_TRACE_ID)
