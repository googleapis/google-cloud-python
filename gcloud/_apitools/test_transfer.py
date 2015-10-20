# pylint: skip-file
import unittest2


class Test__Transfer(unittest2.TestCase):
    URL = 'http://example.com/api'

    def _getTargetClass(self):
        from gcloud._apitools.transfer import _Transfer
        return _Transfer

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        stream = _Stream()
        xfer = self._makeOne(stream)
        self.assertTrue(xfer.stream is stream)
        self.assertFalse(xfer.close_stream)
        self.assertEqual(xfer.chunksize, 1 << 20)
        self.assertTrue(xfer.auto_transfer)
        self.assertTrue(xfer.bytes_http is None)
        self.assertTrue(xfer.http is None)
        self.assertEqual(xfer.num_retries, 5)
        self.assertTrue(xfer.url is None)
        self.assertFalse(xfer.initialized)
        self.assertEqual(xfer._type_name, '_Transfer')

    def test_ctor_explicit(self):
        stream = _Stream()
        HTTP = object()
        CHUNK_SIZE = 1 << 18
        NUM_RETRIES = 8
        xfer = self._makeOne(stream,
                             close_stream=True,
                             chunksize=CHUNK_SIZE,
                             auto_transfer=False,
                             http=HTTP,
                             num_retries=NUM_RETRIES)
        self.assertTrue(xfer.stream is stream)
        self.assertTrue(xfer.close_stream)
        self.assertEqual(xfer.chunksize, CHUNK_SIZE)
        self.assertFalse(xfer.auto_transfer)
        self.assertTrue(xfer.bytes_http is HTTP)
        self.assertTrue(xfer.http is HTTP)
        self.assertEqual(xfer.num_retries, NUM_RETRIES)

    def test_bytes_http_fallback_to_http(self):
        stream = _Stream()
        HTTP = object()
        xfer = self._makeOne(stream, http=HTTP)
        self.assertTrue(xfer.bytes_http is HTTP)

    def test_bytes_http_setter(self):
        stream = _Stream()
        HTTP = object()
        BYTES_HTTP = object()
        xfer = self._makeOne(stream, http=HTTP)
        xfer.bytes_http = BYTES_HTTP
        self.assertTrue(xfer.bytes_http is BYTES_HTTP)

    def test_num_retries_setter_invalid(self):
        from gcloud._apitools.exceptions import TypecheckError
        stream = _Stream()
        xfer = self._makeOne(stream)
        with self.assertRaises(TypecheckError):
            xfer.num_retries = object()

    def test_num_retries_setter_negative(self):
        from gcloud._apitools.exceptions import InvalidDataError
        stream = _Stream()
        xfer = self._makeOne(stream)
        with self.assertRaises(InvalidDataError):
            xfer.num_retries = -1

    def test__Initialize_not_already_initialized_w_http(self):
        HTTP = object()
        stream = _Stream()
        xfer = self._makeOne(stream)
        xfer._Initialize(HTTP, self.URL)
        self.assertTrue(xfer.initialized)
        self.assertTrue(xfer.http is HTTP)
        self.assertTrue(xfer.url is self.URL)

    def test__Initialize_not_already_initialized_wo_http(self):
        from httplib2 import Http
        stream = _Stream()
        xfer = self._makeOne(stream)
        xfer._Initialize(None, self.URL)
        self.assertTrue(xfer.initialized)
        self.assertTrue(isinstance(xfer.http, Http))
        self.assertTrue(xfer.url is self.URL)

    def test__Initialize_w_existing_http(self):
        HTTP_1, HTTP_2 = object(), object()
        stream = _Stream()
        xfer = self._makeOne(stream, http=HTTP_1)
        xfer._Initialize(HTTP_2, self.URL)
        self.assertTrue(xfer.initialized)
        self.assertTrue(xfer.http is HTTP_1)
        self.assertTrue(xfer.url is self.URL)

    def test__Initialize_already_initialized(self):
        from gcloud._apitools.exceptions import TransferInvalidError
        URL_2 = 'http://example.com/other'
        HTTP_1, HTTP_2 = object(), object()
        stream = _Stream()
        xfer = self._makeOne(stream)
        xfer._Initialize(HTTP_1, self.URL)
        with self.assertRaises(TransferInvalidError):
            xfer._Initialize(HTTP_2, URL_2)

    def test_EnsureInitialized_hit(self):
        HTTP = object()
        stream = _Stream()
        xfer = self._makeOne(stream)
        xfer._Initialize(HTTP, self.URL)
        xfer.EnsureInitialized()  # no raise

    def test_EnsureInitialized_miss(self):
        from gcloud._apitools.exceptions import TransferInvalidError
        stream = _Stream()
        xfer = self._makeOne(stream)
        with self.assertRaises(TransferInvalidError):
            xfer.EnsureInitialized()

    def test_EnsureUninitialized_hit(self):
        stream = _Stream()
        xfer = self._makeOne(stream)
        xfer.EnsureUninitialized()  # no raise

    def test_EnsureUninitialized_miss(self):
        from gcloud._apitools.exceptions import TransferInvalidError
        stream = _Stream()
        HTTP = object()
        xfer = self._makeOne(stream)
        xfer._Initialize(HTTP, self.URL)
        with self.assertRaises(TransferInvalidError):
            xfer.EnsureUninitialized()

    def test___del___closes_stream(self):

        stream = _Stream()
        xfer = self._makeOne(stream, close_stream=True)

        self.assertFalse(stream._closed)
        del xfer
        self.assertTrue(stream._closed)


class _Stream(object):
    _closed = False

    def close(self):
        self._closed = True
