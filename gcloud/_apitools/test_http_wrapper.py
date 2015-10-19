# pylint: skip-file
import unittest2


class Test__Httplib2Debuglevel(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._apitools.http_wrapper import _Httplib2Debuglevel
        return _Httplib2Debuglevel

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_wo_loggable_body_wo_http(self):
        from gcloud._testing import _Monkey
        from gcloud._apitools import http_wrapper as MUT

        class _Request(object):
            __slots__ = ('loggable_body',)  # no other attrs
            loggable_body = None

        request = _Request()
        LEVEL = 1
        _httplib2 = _Dummy(debuglevel=0)
        with _Monkey(MUT, httplib2=_httplib2):
            with self._makeOne(request, LEVEL):
                self.assertEqual(_httplib2.debuglevel, 0)

    def test_w_loggable_body_wo_http(self):
        from gcloud._testing import _Monkey
        from gcloud._apitools import http_wrapper as MUT

        class _Request(object):
            __slots__ = ('loggable_body',)  # no other attrs
            loggable_body = object()

        request = _Request()
        LEVEL = 1
        _httplib2 = _Dummy(debuglevel=0)
        with _Monkey(MUT, httplib2=_httplib2):
            with self._makeOne(request, LEVEL):
                self.assertEqual(_httplib2.debuglevel, LEVEL)
        self.assertEqual(_httplib2.debuglevel, 0)

    def test_w_loggable_body_w_http(self):
        from gcloud._testing import _Monkey
        from gcloud._apitools import http_wrapper as MUT

        class _Request(object):
            __slots__ = ('loggable_body',)  # no other attrs
            loggable_body = object()

        class _Connection(object):
            debuglevel = 0
            def set_debuglevel(self, value):
                self.debuglevel = value

        request = _Request()
        LEVEL = 1
        _httplib2 = _Dummy(debuglevel=0)
        update_me = _Connection()
        skip_me = _Connection()
        connections = {'update:me': update_me, 'skip_me': skip_me}
        _http = _Dummy(connections=connections)
        with _Monkey(MUT, httplib2=_httplib2):
            with self._makeOne(request, LEVEL, _http):
                self.assertEqual(_httplib2.debuglevel, LEVEL)
                self.assertEqual(update_me.debuglevel, LEVEL)
                self.assertEqual(skip_me.debuglevel, 0)
        self.assertEqual(_httplib2.debuglevel, 0)
        self.assertEqual(update_me.debuglevel, 0)
        self.assertEqual(skip_me.debuglevel, 0)


class Test_Request(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._apitools.http_wrapper import Request
        return Request

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        request = self._makeOne()
        self.assertEqual(request.url, '')
        self.assertEqual(request.http_method, 'GET')
        self.assertEqual(request.headers, {'content-length': '0'})
        self.assertEqual(request.body, '')
        self.assertEqual(request.loggable_body, None)

    def test_loggable_body_setter_w_body_None(self):
        from gcloud._apitools.exceptions import RequestError
        request = self._makeOne(body=None)
        with self.assertRaises(RequestError):
            request.loggable_body = 'abc'

    def test_body_setter_w_None(self):
        request = self._makeOne()
        request.loggable_body = 'abc'
        request.body = None
        self.assertEqual(request.headers, {})
        self.assertEqual(request.body, None)
        self.assertEqual(request.loggable_body, 'abc')

    def test_body_setter_w_non_string(self):
        request = self._makeOne()
        request.loggable_body = 'abc'
        request.body = body = _Dummy(length=123)
        self.assertEqual(request.headers, {'content-length': '123'})
        self.assertTrue(request.body is body)
        self.assertEqual(request.loggable_body, '<media body>')


class Test_Response(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud._apitools.http_wrapper import Response
        return Response

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        info = {'status': '200'}
        response = self._makeOne(info, CONTENT, URL)
        self.assertEqual(len(response), len(CONTENT))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.retry_after, None)
        self.assertFalse(response.is_redirect)

    def test_length_w_content_encoding_w_content_range(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        RANGE = 'bytes 0-122/5678'
        info = {
            'status': '200',
            'content-length': len(CONTENT),
            'content-encoding': 'testing',
            'content-range': RANGE,
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertEqual(len(response), 123)

    def test_length_w_content_encoding_wo_content_range(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        info = {
            'status': '200',
            'content-length': len(CONTENT),
            'content-encoding': 'testing',
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertEqual(len(response), len(CONTENT))

    def test_length_w_content_length_w_content_range(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        RANGE = 'bytes 0-12/5678'
        info = {
            'status': '200',
            'content-length': len(CONTENT) * 2,
            'content-range': RANGE,
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertEqual(len(response), len(CONTENT) * 2)

    def test_length_wo_content_length_w_content_range(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        RANGE = 'bytes 0-122/5678'
        info = {
            'status': '200',
            'content-range': RANGE,
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertEqual(len(response), 123)

    def test_retry_after_w_header(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        RANGE = 'bytes 0-122/5678'
        info = {
            'status': '200',
            'retry-after': '123',
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertEqual(response.retry_after, 123)

    def test_is_redirect_w_code_wo_location(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        RANGE = 'bytes 0-122/5678'
        info = {
            'status': '301',
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertFalse(response.is_redirect)

    def test_is_redirect_w_code_w_location(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        RANGE = 'bytes 0-122/5678'
        info = {
            'status': '301',
            'location': 'http://example.com/other',
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertTrue(response.is_redirect)


class Test_CheckResponse(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud._apitools.http_wrapper import CheckResponse
        return CheckResponse(*args, **kw)

    def test_w_none(self):
        from gcloud._apitools.exceptions import RequestError
        with self.assertRaises(RequestError):
            self._callFUT(None)

    def test_w_TOO_MANY_REQUESTS(self):
        from gcloud._apitools.exceptions import BadStatusCodeError
        from gcloud._apitools.http_wrapper import TOO_MANY_REQUESTS

        with self.assertRaises(BadStatusCodeError):
            self._callFUT(_Response(TOO_MANY_REQUESTS))

    def test_w_50x(self):
        from gcloud._apitools.exceptions import BadStatusCodeError

        with self.assertRaises(BadStatusCodeError):
            self._callFUT(_Response(500))

        with self.assertRaises(BadStatusCodeError):
            self._callFUT(_Response(503))

    def test_w_retry_after(self):
        from gcloud._apitools.exceptions import RetryAfterError

        with self.assertRaises(RetryAfterError):
            self._callFUT(_Response(200, 20))

    def test_pass(self):
        self._callFUT(_Response(200))


class Test_RebuildHttpConnections(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud._apitools.http_wrapper import RebuildHttpConnections
        return RebuildHttpConnections(*args, **kw)

    def test_wo_connections(self):
        http = object()
        self._callFUT(http)

    def test_w_connections(self):
        connections = {'delete:me': object(), 'skip_me': object()}
        http = _Dummy(connections=connections)
        self._callFUT(http)
        self.assertFalse('delete:me' in connections)
        self.assertTrue('skip_me' in connections)


class Test_HandleExceptionsAndRebuildHttpConnections(unittest2.TestCase):
    URL = 'http://example.com/api'

    def _callFUT(self, *args, **kw):
        from gcloud._apitools.http_wrapper import (
            HandleExceptionsAndRebuildHttpConnections)
        return HandleExceptionsAndRebuildHttpConnections(*args, **kw)

    def _monkeyMUT(self):
        from gcloud._testing import _Monkey
        from gcloud._apitools import http_wrapper as MUT
        _logged = []

        def _debug(msg, *args):
            _logged.append((msg, args))

        _logging = _Dummy(debug=_debug)
        _slept = []

        def _sleep(value):
            _slept.append(value)

        _time = _Dummy(sleep=_sleep)
        monkey = _Monkey(MUT, logging=_logging, time=_time)
        return monkey, _logged, _slept

    def _build_retry_args(self, exc,
                          url=URL, num_retries=0, max_retry_wait=10):
        retry_args = _Dummy(exc=exc,
                            num_retries=num_retries,
                            max_retry_wait=max_retry_wait)
        retry_args.http_request = _Dummy(url=url)
        connections = {'delete:me': object(), 'skip_me': object()}
        retry_args.http = _Dummy(connections=connections)
        return retry_args

    def _verify_logged_slept(self, logged, slept,
                             expected_msg, expected_args, expected_sleep=1.25):
        self.assertEqual(len(logged), 2)

        msg, args = logged[0]
        self.assertEqual(msg, expected_msg)
        self.assertEqual(args, expected_args)

        msg, args = logged[1]
        self.assertEqual(msg, 'Retrying request to url %s after exception %s')
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], self.URL)

        self.assertEqual(slept, [expected_sleep])

    def test_w_BadStatusLine(self):
        import random
        from gcloud._testing import _Monkey
        from six.moves.http_client import BadStatusLine
        exc = BadStatusLine('invalid')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Caught HTTP error %s, retrying: %s',
            ('BadStatusLine', exc))

    def test_w_IncompleteRead(self):
        import random
        from gcloud._testing import _Monkey
        from six.moves.http_client import IncompleteRead
        exc = IncompleteRead(50, 100)
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Caught HTTP error %s, retrying: %s',
            ('IncompleteRead', exc))

    def test_w_ResponseNotReady(self):
        import random
        from gcloud._testing import _Monkey
        from six.moves.http_client import ResponseNotReady
        exc = ResponseNotReady('uh oh')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Caught HTTP error %s, retrying: %s',
            ('ResponseNotReady', exc))

    def test_w_socket_gaierror(self):
        import random
        from gcloud._testing import _Monkey
        import socket
        exc = socket.gaierror('uh oh')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Caught socket address error, retrying: %s', (exc,))

    def test_w_socket_timeout(self):
        import random
        from gcloud._testing import _Monkey
        import socket
        exc = socket.timeout('uh oh')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Caught socket timeout error, retrying: %s', (exc,))

    def test_w_socket_error(self):
        import random
        from gcloud._testing import _Monkey
        import socket
        exc = socket.error('uh oh')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Caught socket error, retrying: %s', (exc,))

    def test_w_httplib2_ServerNotFoundError(self):
        import random
        from gcloud._testing import _Monkey
        import httplib2
        exc = httplib2.ServerNotFoundError('uh oh')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept,
            'Caught server not found error, retrying: %s', (exc,))

    def test_w_ValueError(self):
        import random
        from gcloud._testing import _Monkey
        exc = ValueError('uh oh')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept,
            'Response content was invalid (%s), retrying', (exc,))

    def test_w_RequestError(self):
        import random
        from gcloud._testing import _Monkey
        from gcloud._apitools.exceptions import RequestError
        exc = RequestError('uh oh')
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Request returned no response, retrying', ())

    def test_w_BadStatusCodeError(self):
        import random
        from gcloud._testing import _Monkey
        from gcloud._apitools.exceptions import BadStatusCodeError
        response = _Response(500)
        exc = BadStatusCodeError.FromResponse(response)
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept, 'Response returned status %s, retrying', (500,))

    def test_w_RetryAfterError(self):
        import random
        from gcloud._testing import _Monkey
        from gcloud._apitools.exceptions import RetryAfterError
        from gcloud._apitools.http_wrapper import TOO_MANY_REQUESTS
        RETRY_AFTER = 25
        response = _Response(TOO_MANY_REQUESTS, RETRY_AFTER)
        exc = RetryAfterError.FromResponse(response)
        retry_args = self._build_retry_args(exc)
        monkey, logged, slept = self._monkeyMUT()

        with _Monkey(random, uniform=lambda lower, upper: upper):
            with monkey:
                self._callFUT(retry_args)

        self._verify_logged_slept(
            logged, slept,
            'Response returned a retry-after header, retrying', (), RETRY_AFTER)

    def test_wo_matching_type(self):

        class _Nonesuch(Exception):
            pass

        def _raises():
            raise _Nonesuch

        monkey, logged, slept = self._monkeyMUT()

        with monkey:
            with self.assertRaises(_Nonesuch):
                try:
                    _raises()
                except Exception as exc:
                    retry_args = _Dummy(exc=exc)
                    self._callFUT(retry_args)


class _Dummy(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _Response(object):
    content = ''
    request_url = 'http://example.com/api'

    def __init__(self, status_code, retry_after=None):
        self.info = {'status': status_code}
        self.status_code = status_code
        self.retry_after = retry_after
