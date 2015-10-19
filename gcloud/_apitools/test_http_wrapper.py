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


class _Dummy(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)
