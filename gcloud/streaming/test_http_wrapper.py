import unittest2


class Test__httplib2_debug_level(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.streaming.http_wrapper import _httplib2_debug_level
        return _httplib2_debug_level

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_wo_loggable_body_wo_http(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT

        request = _Request()
        LEVEL = 1
        _httplib2 = _Dummy(debuglevel=0)
        with _Monkey(MUT, httplib2=_httplib2):
            with self._makeOne(request, LEVEL):
                self.assertEqual(_httplib2.debuglevel, 0)

    def test_w_loggable_body_wo_http(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT

        request = _Request(loggable_body=object())
        LEVEL = 1
        _httplib2 = _Dummy(debuglevel=0)
        with _Monkey(MUT, httplib2=_httplib2):
            with self._makeOne(request, LEVEL):
                self.assertEqual(_httplib2.debuglevel, LEVEL)
        self.assertEqual(_httplib2.debuglevel, 0)

    def test_w_loggable_body_w_http(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT

        class _Connection(object):
            debuglevel = 0

            def set_debuglevel(self, value):
                self.debuglevel = value

        request = _Request(loggable_body=object())
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
        from gcloud.streaming.http_wrapper import Request
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
        from gcloud.streaming.exceptions import RequestError
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
        from gcloud.streaming.http_wrapper import Response
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
        info = {
            'status': '200',
            'retry-after': '123',
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertEqual(response.retry_after, 123)

    def test_is_redirect_w_code_wo_location(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        info = {
            'status': '301',
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertFalse(response.is_redirect)

    def test_is_redirect_w_code_w_location(self):
        CONTENT = 'CONTENT'
        URL = 'http://example.com/api'
        info = {
            'status': '301',
            'location': 'http://example.com/other',
        }
        response = self._makeOne(info, CONTENT, URL)
        self.assertTrue(response.is_redirect)


class Test__check_response(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.http_wrapper import _check_response
        return _check_response(*args, **kw)

    def test_w_none(self):
        from gcloud.streaming.exceptions import RequestError
        with self.assertRaises(RequestError):
            self._callFUT(None)

    def test_w_TOO_MANY_REQUESTS(self):
        from gcloud.streaming.exceptions import BadStatusCodeError
        from gcloud.streaming.http_wrapper import TOO_MANY_REQUESTS

        with self.assertRaises(BadStatusCodeError):
            self._callFUT(_Response(TOO_MANY_REQUESTS))

    def test_w_50x(self):
        from gcloud.streaming.exceptions import BadStatusCodeError

        with self.assertRaises(BadStatusCodeError):
            self._callFUT(_Response(500))

        with self.assertRaises(BadStatusCodeError):
            self._callFUT(_Response(503))

    def test_w_retry_after(self):
        from gcloud.streaming.exceptions import RetryAfterError

        with self.assertRaises(RetryAfterError):
            self._callFUT(_Response(200, 20))

    def test_pass(self):
        self._callFUT(_Response(200))


class Test__reset_http_connections(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.http_wrapper import _reset_http_connections
        return _reset_http_connections(*args, **kw)

    def test_wo_connections(self):
        http = object()
        self._callFUT(http)

    def test_w_connections(self):
        connections = {'delete:me': object(), 'skip_me': object()}
        http = _Dummy(connections=connections)
        self._callFUT(http)
        self.assertFalse('delete:me' in connections)
        self.assertTrue('skip_me' in connections)


class Test___make_api_request_no_retry(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.http_wrapper import _make_api_request_no_retry
        return _make_api_request_no_retry(*args, **kw)

    def _verify_requested(self, http, request,
                          redirections=5, connection_type=None):
        self.assertEqual(len(http._requested), 1)
        url, kw = http._requested[0]
        self.assertEqual(url, request.url)
        self.assertEqual(kw['method'], request.http_method)
        self.assertEqual(kw['body'], request.body)
        self.assertEqual(kw['headers'], request.headers)
        self.assertEqual(kw['redirections'], redirections)
        self.assertEqual(kw['connection_type'], connection_type)

    def test_defaults_wo_connections(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        INFO = {'status': '200'}
        CONTENT = 'CONTENT'
        _http = _Http((INFO, CONTENT))
        _httplib2 = _Dummy(debuglevel=1)
        _request = _Request()
        _checked = []
        with _Monkey(MUT, httplib2=_httplib2):
            response = self._callFUT(_http, _request,
                                     check_response_func=_checked.append)
        self.assertTrue(isinstance(response, MUT.Response))
        self.assertEqual(response.info, INFO)
        self.assertEqual(response.content, CONTENT)
        self.assertEqual(response.request_url, _request.url)
        self.assertEqual(_checked, [response])
        self._verify_requested(_http, _request)

    def test_w_explicit_redirections(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        INFO = {'status': '200'}
        CONTENT = 'CONTENT'
        _http = _Http((INFO, CONTENT))
        _httplib2 = _Dummy(debuglevel=1)
        _request = _Request()
        _checked = []
        with _Monkey(MUT, httplib2=_httplib2):
            response = self._callFUT(_http, _request,
                                     redirections=10,
                                     check_response_func=_checked.append)
        self.assertTrue(isinstance(response, MUT.Response))
        self.assertEqual(response.info, INFO)
        self.assertEqual(response.content, CONTENT)
        self.assertEqual(response.request_url, _request.url)
        self.assertEqual(_checked, [response])
        self._verify_requested(_http, _request, redirections=10)

    def test_w_http_connections_miss(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        INFO = {'status': '200'}
        CONTENT = 'CONTENT'
        CONN_TYPE = object()
        _http = _Http((INFO, CONTENT))
        _http.connections = {'https': CONN_TYPE}
        _httplib2 = _Dummy(debuglevel=1)
        _request = _Request()
        _checked = []
        with _Monkey(MUT, httplib2=_httplib2):
            response = self._callFUT(_http, _request,
                                     check_response_func=_checked.append)
        self.assertTrue(isinstance(response, MUT.Response))
        self.assertEqual(response.info, INFO)
        self.assertEqual(response.content, CONTENT)
        self.assertEqual(response.request_url, _request.url)
        self.assertEqual(_checked, [response])
        self._verify_requested(_http, _request)

    def test_w_http_connections_hit(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        INFO = {'status': '200'}
        CONTENT = 'CONTENT'
        CONN_TYPE = object()
        _http = _Http((INFO, CONTENT))
        _http.connections = {'http': CONN_TYPE}
        _httplib2 = _Dummy(debuglevel=1)
        _request = _Request()
        _checked = []
        with _Monkey(MUT, httplib2=_httplib2):
            response = self._callFUT(_http, _request,
                                     check_response_func=_checked.append)
        self.assertTrue(isinstance(response, MUT.Response))
        self.assertEqual(response.info, INFO)
        self.assertEqual(response.content, CONTENT)
        self.assertEqual(response.request_url, _request.url)
        self.assertEqual(_checked, [response])
        self._verify_requested(_http, _request, connection_type=CONN_TYPE)

    def test_w_request_returning_None(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        from gcloud.streaming.exceptions import RequestError
        INFO = None
        CONTENT = None
        CONN_TYPE = object()
        _http = _Http((INFO, CONTENT))
        _http.connections = {'http': CONN_TYPE}
        _httplib2 = _Dummy(debuglevel=1)
        _request = _Request()
        with _Monkey(MUT, httplib2=_httplib2):
            with self.assertRaises(RequestError):
                self._callFUT(_http, _request)
        self._verify_requested(_http, _request, connection_type=CONN_TYPE)


class Test_make_api_request(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.http_wrapper import make_api_request
        return make_api_request(*args, **kw)

    def test_wo_exception(self):
        HTTP, REQUEST, RESPONSE = object(), object(), object()
        _created, _checked = [], []

        def _wo_exception(*args, **kw):
            _created.append((args, kw))
            return RESPONSE

        response = self._callFUT(HTTP, REQUEST,
                                 wo_retry_func=_wo_exception,
                                 check_response_func=_checked.append)

        self.assertTrue(response is RESPONSE)
        expected_kw = {
            'redirections': 5,
            'check_response_func': _checked.append,
        }
        self.assertEqual(_created, [((HTTP, REQUEST), expected_kw)])
        self.assertEqual(_checked, [])  # not called by '_wo_exception'

    def test_w_exceptions_lt_max_retries(self):
        from gcloud.streaming.exceptions import RetryAfterError
        HTTP, RESPONSE = object(), object()
        REQUEST = _Request()
        WAIT = 10,
        _created, _checked = [], []
        _counter = [None] * 4

        def _wo_exception(*args, **kw):
            _created.append((args, kw))
            if _counter:
                _counter.pop()
                raise RetryAfterError(RESPONSE, '', REQUEST.url, 0.1)
            return RESPONSE

        response = self._callFUT(HTTP, REQUEST,
                                 retries=5,
                                 max_retry_wait=WAIT,
                                 wo_retry_func=_wo_exception,
                                 check_response_func=_checked.append)

        self.assertTrue(response is RESPONSE)
        self.assertEqual(len(_created), 5)
        expected_kw = {
            'redirections': 5,
            'check_response_func': _checked.append,
        }
        for attempt in _created:
            self.assertEqual(attempt, ((HTTP, REQUEST), expected_kw))
        self.assertEqual(_checked, [])  # not called by '_wo_exception'

    def test_w_exceptions_gt_max_retries(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        HTTP = object()
        REQUEST = _Request()
        WAIT = 10,
        _created, _checked = [], []

        def _wo_exception(*args, **kw):
            _created.append((args, kw))
            raise ValueError('Retryable')

        with _Monkey(MUT, calculate_wait_for_retry=lambda *ignored: 0.1):
            with self.assertRaises(ValueError):
                self._callFUT(HTTP, REQUEST,
                              retries=3,
                              max_retry_wait=WAIT,
                              wo_retry_func=_wo_exception,
                              check_response_func=_checked.append)

        self.assertEqual(len(_created), 3)
        expected_kw = {
            'redirections': 5,
            'check_response_func': _checked.append,
        }
        for attempt in _created:
            self.assertEqual(attempt, ((HTTP, REQUEST), expected_kw))
        self.assertEqual(_checked, [])  # not called by '_wo_exception'


class Test__register_http_factory(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.http_wrapper import _register_http_factory
        return _register_http_factory(*args, **kw)

    def test_it(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        _factories = []

        FACTORY = object()

        with _Monkey(MUT, _HTTP_FACTORIES=_factories):
            self._callFUT(FACTORY)
            self.assertEqual(_factories, [FACTORY])


class Test_get_http(unittest2.TestCase):

    def _callFUT(self, *args, **kw):
        from gcloud.streaming.http_wrapper import get_http
        return get_http(*args, **kw)

    def test_wo_registered_factories(self):
        from httplib2 import Http
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT
        _factories = []

        with _Monkey(MUT, _HTTP_FACTORIES=_factories):
            http = self._callFUT()

        self.assertTrue(isinstance(http, Http))

    def test_w_registered_factories(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import http_wrapper as MUT

        FOUND = object()

        _misses = []

        def _miss(**kw):
            _misses.append(kw)
            return None

        _hits = []

        def _hit(**kw):
            _hits.append(kw)
            return FOUND

        _factories = [_miss, _hit]

        with _Monkey(MUT, _HTTP_FACTORIES=_factories):
            http = self._callFUT(foo='bar')

        self.assertTrue(http is FOUND)
        self.assertEqual(_misses, [{'foo': 'bar'}])
        self.assertEqual(_hits, [{'foo': 'bar'}])


class _Dummy(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _Request(object):
    __slots__ = ('url', 'http_method', 'body', 'headers', 'loggable_body',)
    URL = 'http://example.com/api'

    def __init__(self, url=URL, http_method='GET', body='',
                 loggable_body=None):
        self.url = url
        self.http_method = http_method
        self.body = body
        self.headers = {}
        self.loggable_body = loggable_body


class _Response(object):
    content = ''
    request_url = _Request.URL

    def __init__(self, status_code, retry_after=None):
        self.info = {'status': status_code}
        self.status_code = status_code
        self.retry_after = retry_after


class _Http(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def request(self, url, **kw):
        self._requested.append((url, kw))
        response, self._responses = self._responses[0], self._responses[1:]
        return response
