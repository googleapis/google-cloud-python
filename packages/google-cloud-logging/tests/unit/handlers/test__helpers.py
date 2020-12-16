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

import unittest

import mock

_FLASK_TRACE_ID = "flask-id"
_FLASK_HTTP_REQUEST = {"request_url": "https://flask.palletsprojects.com/en/1.1.x/"}
_DJANGO_TRACE_ID = "django-id"
_DJANGO_HTTP_REQUEST = {"request_url": "https://www.djangoproject.com/"}


class Test_get_request_data_from_flask(unittest.TestCase):
    @staticmethod
    def _call_fut():
        from google.cloud.logging_v2.handlers import _helpers

        return _helpers.get_request_data_from_flask()

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
            http_request, trace_id = self._call_fut()

        self.assertIsNone(trace_id)
        self.assertEqual(http_request.request_method, "GET")

    def test_valid_context_header(self):
        flask_trace_header = "X_CLOUD_TRACE_CONTEXT"
        expected_trace_id = _FLASK_TRACE_ID
        flask_trace_id = expected_trace_id + "/testspanid"

        app = self.create_app()
        context = app.test_request_context(
            path="/", headers={flask_trace_header: flask_trace_id}
        )

        with context:
            http_request, trace_id = self._call_fut()

        self.assertEqual(trace_id, expected_trace_id)
        self.assertEqual(http_request.request_method, "GET")

    def test_http_request_populated(self):
        expected_path = "http://testserver/123"
        expected_agent = "Mozilla/5.0"
        expected_referrer = "self"
        expected_ip = "10.1.2.3"
        body_content = "test"
        headers = {
            "User-Agent": expected_agent,
            "Referer": expected_referrer,
        }

        app = self.create_app()
        with app.test_client() as c:
            c.put(
                path=expected_path,
                data=body_content,
                environ_base={"REMOTE_ADDR": expected_ip},
                headers=headers,
            )
            http_request, trace_id = self._call_fut()

        self.assertEqual(http_request.request_method, "PUT")
        self.assertEqual(http_request.request_url, expected_path)
        self.assertEqual(http_request.user_agent, expected_agent)
        self.assertEqual(http_request.referer, expected_referrer)
        self.assertEqual(http_request.remote_ip, expected_ip)
        self.assertEqual(http_request.request_size, len(body_content))
        self.assertEqual(http_request.protocol, "HTTP/1.1")

    def test_http_request_sparse(self):
        expected_path = "http://testserver/123"
        app = self.create_app()
        with app.test_client() as c:
            c.put(path=expected_path)
            http_request, trace_id = self._call_fut()
        self.assertEqual(http_request.request_method, "PUT")
        self.assertEqual(http_request.request_url, expected_path)
        self.assertEqual(http_request.protocol, "HTTP/1.1")


class Test_get_request_data_from_django(unittest.TestCase):
    @staticmethod
    def _call_fut():
        from google.cloud.logging_v2.handlers import _helpers

        return _helpers.get_request_data_from_django()

    def setUp(self):
        from django.conf import settings
        from django.test.utils import setup_test_environment

        if not settings.configured:
            settings.configure()
        setup_test_environment()

    def tearDown(self):
        from django.test.utils import teardown_test_environment
        from google.cloud.logging_v2.handlers.middleware import request

        teardown_test_environment()
        request._thread_locals.__dict__.clear()

    def test_no_context_header(self):
        from django.test import RequestFactory
        from google.cloud.logging_v2.handlers.middleware import request

        django_request = RequestFactory().get("/")

        middleware = request.RequestMiddleware(None)
        middleware.process_request(django_request)
        http_request, trace_id = self._call_fut()
        self.assertEqual(http_request.request_method, "GET")
        self.assertIsNone(trace_id)

    def test_valid_context_header(self):
        from django.test import RequestFactory
        from google.cloud.logging_v2.handlers.middleware import request

        django_trace_header = "HTTP_X_CLOUD_TRACE_CONTEXT"
        expected_trace_id = "testtraceiddjango"
        django_trace_id = expected_trace_id + "/testspanid"

        django_request = RequestFactory().get(
            "/", **{django_trace_header: django_trace_id}
        )

        middleware = request.RequestMiddleware(None)
        middleware.process_request(django_request)
        http_request, trace_id = self._call_fut()

        self.assertEqual(trace_id, expected_trace_id)
        self.assertEqual(http_request.request_method, "GET")

    def test_http_request_populated(self):
        from django.test import RequestFactory
        from google.cloud.logging_v2.handlers.middleware import request

        expected_path = "http://testserver/123"
        expected_agent = "Mozilla/5.0"
        expected_referrer = "self"
        body_content = "test"
        django_request = RequestFactory().put(
            expected_path,
            data=body_content,
            HTTP_USER_AGENT=expected_agent,
            HTTP_REFERER=expected_referrer,
        )

        middleware = request.RequestMiddleware(None)
        middleware.process_request(django_request)
        http_request, trace_id = self._call_fut()
        self.assertEqual(http_request.request_method, "PUT")
        self.assertEqual(http_request.request_url, expected_path)
        self.assertEqual(http_request.user_agent, expected_agent)
        self.assertEqual(http_request.referer, expected_referrer)
        self.assertEqual(http_request.remote_ip, "127.0.0.1")
        self.assertEqual(http_request.request_size, len(body_content))
        self.assertEqual(http_request.protocol, "HTTP/1.1")

    def test_http_request_sparse(self):
        from django.test import RequestFactory
        from google.cloud.logging_v2.handlers.middleware import request

        expected_path = "http://testserver/123"
        django_request = RequestFactory().put(expected_path)
        middleware = request.RequestMiddleware(None)
        middleware.process_request(django_request)
        http_request, trace_id = self._call_fut()
        self.assertEqual(http_request.request_method, "PUT")
        self.assertEqual(http_request.request_url, expected_path)
        self.assertEqual(http_request.remote_ip, "127.0.0.1")
        self.assertEqual(http_request.protocol, "HTTP/1.1")


class Test_get_request_data(unittest.TestCase):
    @staticmethod
    def _call_fut():
        from google.cloud.logging_v2.handlers import _helpers

        return _helpers.get_request_data()

    def _helper(self, django_return, flask_return):
        django_patch = mock.patch(
            "google.cloud.logging_v2.handlers._helpers.get_request_data_from_django",
            return_value=django_return,
        )
        flask_patch = mock.patch(
            "google.cloud.logging_v2.handlers._helpers.get_request_data_from_flask",
            return_value=flask_return,
        )

        with django_patch as django_mock:
            with flask_patch as flask_mock:
                result = self._call_fut()

        return django_mock, flask_mock, result

    def test_from_django(self):
        django_expected = (_DJANGO_HTTP_REQUEST, _DJANGO_TRACE_ID)
        flask_expected = (None, None)
        django_mock, flask_mock, output = self._helper(django_expected, flask_expected)
        self.assertEqual(output, django_expected)

        django_mock.assert_called_once_with()
        flask_mock.assert_not_called()

    def test_from_flask(self):
        django_expected = (None, None)
        flask_expected = (_FLASK_HTTP_REQUEST, _FLASK_TRACE_ID)

        django_mock, flask_mock, output = self._helper(django_expected, flask_expected)
        self.assertEqual(output, flask_expected)

        django_mock.assert_called_once_with()
        flask_mock.assert_called_once_with()

    def test_from_django_and_flask(self):
        django_expected = (_DJANGO_HTTP_REQUEST, _DJANGO_TRACE_ID)
        flask_expected = (_FLASK_HTTP_REQUEST, _FLASK_TRACE_ID)

        django_mock, flask_mock, output = self._helper(django_expected, flask_expected)

        # Django wins.
        self.assertEqual(output, django_expected)

        django_mock.assert_called_once_with()
        flask_mock.assert_not_called()

    def test_missing_http_request(self):
        flask_expected = (None, _FLASK_TRACE_ID)
        django_expected = (None, _DJANGO_TRACE_ID)
        django_mock, flask_mock, output = self._helper(django_expected, flask_expected)

        # function only returns trace if http_request data is present
        self.assertEqual(output, (None, None))

        django_mock.assert_called_once_with()
        flask_mock.assert_called_once_with()

    def test_missing_trace_id(self):
        flask_expected = (_FLASK_HTTP_REQUEST, None)
        django_expected = (None, _DJANGO_TRACE_ID)
        django_mock, flask_mock, output = self._helper(django_expected, flask_expected)

        # trace_id is optional
        self.assertEqual(output, flask_expected)

        django_mock.assert_called_once_with()
        flask_mock.assert_called_once_with()

    def test_missing_both(self):
        flask_expected = (None, None)
        django_expected = (None, None)
        django_mock, flask_mock, output = self._helper(django_expected, flask_expected)
        self.assertEqual(output, (None, None))

        django_mock.assert_called_once_with()
        flask_mock.assert_called_once_with()

    def test_wo_libraries(self):
        output = self._call_fut()
        self.assertEqual(output, (None, None))
