# Copyright 2017 Google LLC All Rights Reserved.
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

import json
import unittest

import mock
import six

try:
    from webapp2 import RequestHandler
except SyntaxError:
    # webapp2 has not been ported to python3, so it will give a syntax
    # error if we try.  We'll just skip the webapp2 tests in that case.
    RequestHandler = object


class Test_get_trace_id_from_flask(unittest.TestCase):
    @staticmethod
    def _call_fut():
        from google.cloud.logging.handlers import _helpers

        return _helpers.get_trace_id_from_flask()

    @staticmethod
    def create_app():
        import flask

        app = flask.Flask(__name__)

        @app.route("/")
        def index():
            return "test flask trace"  # pragma: NO COVER

        return app

    def test_no_context_header(self):
        app = self.create_app()
        with app.test_request_context(path="/", headers={}):
            trace_id = self._call_fut()

        self.assertIsNone(trace_id)

    def test_valid_context_header(self):
        flask_trace_header = "X_CLOUD_TRACE_CONTEXT"
        expected_trace_id = "testtraceidflask"
        flask_trace_id = expected_trace_id + "/testspanid"

        app = self.create_app()
        context = app.test_request_context(
            path="/", headers={flask_trace_header: flask_trace_id}
        )

        with context:
            trace_id = self._call_fut()

        self.assertEqual(trace_id, expected_trace_id)


class _GetTraceId(RequestHandler):
    def get(self):
        from google.cloud.logging.handlers import _helpers

        trace_id = _helpers.get_trace_id_from_webapp2()
        self.response.content_type = "application/json"
        self.response.out.write(json.dumps(trace_id))


@unittest.skipIf(six.PY3, "webapp2 is Python 2 only")
class Test_get_trace_id_from_webapp2(unittest.TestCase):
    @staticmethod
    def create_app():
        import webapp2

        app = webapp2.WSGIApplication([("/", _GetTraceId)])

        return app

    def test_no_context_header(self):
        import webob

        req = webob.BaseRequest.blank("/")
        response = req.get_response(self.create_app())
        trace_id = json.loads(response.body)

        self.assertEqual(None, trace_id)

    def test_valid_context_header(self):
        import webob

        webapp2_trace_header = "X-Cloud-Trace-Context"
        expected_trace_id = "testtraceidwebapp2"
        webapp2_trace_id = expected_trace_id + "/testspanid"

        req = webob.BaseRequest.blank(
            "/", headers={webapp2_trace_header: webapp2_trace_id}
        )
        response = req.get_response(self.create_app())
        trace_id = json.loads(response.body)

        self.assertEqual(trace_id, expected_trace_id)


class Test_get_trace_id_from_django(unittest.TestCase):
    @staticmethod
    def _call_fut():
        from google.cloud.logging.handlers import _helpers

        return _helpers.get_trace_id_from_django()

    def setUp(self):
        from django.conf import settings
        from django.test.utils import setup_test_environment

        if not settings.configured:
            settings.configure()
        setup_test_environment()

    def tearDown(self):
        from django.test.utils import teardown_test_environment
        from google.cloud.logging.handlers.middleware import request

        teardown_test_environment()
        request._thread_locals.__dict__.clear()

    def test_no_context_header(self):
        from django.test import RequestFactory
        from google.cloud.logging.handlers.middleware import request

        django_request = RequestFactory().get("/")

        middleware = request.RequestMiddleware()
        middleware.process_request(django_request)
        trace_id = self._call_fut()
        self.assertIsNone(trace_id)

    def test_valid_context_header(self):
        from django.test import RequestFactory
        from google.cloud.logging.handlers.middleware import request

        django_trace_header = "HTTP_X_CLOUD_TRACE_CONTEXT"
        expected_trace_id = "testtraceiddjango"
        django_trace_id = expected_trace_id + "/testspanid"

        django_request = RequestFactory().get(
            "/", **{django_trace_header: django_trace_id}
        )

        middleware = request.RequestMiddleware()
        middleware.process_request(django_request)
        trace_id = self._call_fut()

        self.assertEqual(trace_id, expected_trace_id)


class Test_get_trace_id(unittest.TestCase):
    @staticmethod
    def _call_fut():
        from google.cloud.logging.handlers import _helpers

        return _helpers.get_trace_id()

    def _helper(self, django_return, flask_return):
        django_patch = mock.patch(
            "google.cloud.logging.handlers._helpers.get_trace_id_from_django",
            return_value=django_return,
        )
        flask_patch = mock.patch(
            "google.cloud.logging.handlers._helpers.get_trace_id_from_flask",
            return_value=flask_return,
        )

        with django_patch as django_mock:
            with flask_patch as flask_mock:
                trace_id = self._call_fut()

        return django_mock, flask_mock, trace_id

    def test_from_django(self):
        django_mock, flask_mock, trace_id = self._helper("test-django-trace-id", None)
        self.assertEqual(trace_id, django_mock.return_value)

        django_mock.assert_called_once_with()
        flask_mock.assert_not_called()

    def test_from_flask(self):
        django_mock, flask_mock, trace_id = self._helper(None, "test-flask-trace-id")
        self.assertEqual(trace_id, flask_mock.return_value)

        django_mock.assert_called_once_with()
        flask_mock.assert_called_once_with()

    def test_from_django_and_flask(self):
        django_mock, flask_mock, trace_id = self._helper(
            "test-django-trace-id", "test-flask-trace-id"
        )
        # Django wins.
        self.assertEqual(trace_id, django_mock.return_value)

        django_mock.assert_called_once_with()
        flask_mock.assert_not_called()

    def test_missing(self):
        django_mock, flask_mock, trace_id = self._helper(None, None)
        self.assertIsNone(trace_id)

        django_mock.assert_called_once_with()
        flask_mock.assert_called_once_with()
