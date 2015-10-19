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


class _Dummy(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)
