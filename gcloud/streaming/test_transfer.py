# pylint: skip-file
import unittest2


class Test__Transfer(unittest2.TestCase):
    URL = 'http://example.com/api'

    def _getTargetClass(self):
        from gcloud.streaming.transfer import _Transfer
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
        from gcloud.streaming.exceptions import TypecheckError
        stream = _Stream()
        xfer = self._makeOne(stream)
        with self.assertRaises(TypecheckError):
            xfer.num_retries = object()

    def test_num_retries_setter_negative(self):
        from gcloud.streaming.exceptions import InvalidDataError
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
        from gcloud.streaming.exceptions import TransferInvalidError
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
        from gcloud.streaming.exceptions import TransferInvalidError
        stream = _Stream()
        xfer = self._makeOne(stream)
        with self.assertRaises(TransferInvalidError):
            xfer.EnsureInitialized()

    def test_EnsureUninitialized_hit(self):
        stream = _Stream()
        xfer = self._makeOne(stream)
        xfer.EnsureUninitialized()  # no raise

    def test_EnsureUninitialized_miss(self):
        from gcloud.streaming.exceptions import TransferInvalidError
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


class Test_Download(unittest2.TestCase):
    URL = "http://example.com/api"

    def _getTargetClass(self):
        from gcloud.streaming.transfer import Download
        return Download

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        stream = _Stream()
        download = self._makeOne(stream)
        self.assertTrue(download.stream is stream)
        self.assertTrue(download._initial_response is None)
        self.assertEqual(download.progress, 0)
        self.assertTrue(download.total_size is None)
        self.assertTrue(download.encoding is None)

    def test_ctor_w_kwds(self):
        stream = _Stream()
        CHUNK_SIZE = 123
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        self.assertTrue(download.stream is stream)
        self.assertEqual(download.chunksize, CHUNK_SIZE)

    def test_ctor_w_total_size(self):
        stream = _Stream()
        SIZE = 123
        download = self._makeOne(stream, total_size=SIZE)
        self.assertTrue(download.stream is stream)
        self.assertEqual(download.total_size, SIZE)

    def test_FromFile_w_existing_file_no_override(self):
        import os
        from gcloud.streaming.exceptions import InvalidUserInputError
        klass = self._getTargetClass()
        with _tempdir() as tempdir:
            filename = os.path.join(tempdir, 'file.out')
            with open(filename, 'w') as fileobj:
                fileobj.write('EXISTING FILE')
            with self.assertRaises(InvalidUserInputError):
                klass.FromFile(filename)

    def test_FromFile_w_existing_file_w_override_wo_auto_transfer(self):
        import os
        klass = self._getTargetClass()
        with _tempdir() as tempdir:
            filename = os.path.join(tempdir, 'file.out')
            with open(filename, 'w') as fileobj:
                fileobj.write('EXISTING FILE')
            download = klass.FromFile(filename, overwrite=True,
                                      auto_transfer=False)
            self.assertFalse(download.auto_transfer)
            del download  # closes stream
            with open(filename, 'rb') as fileobj:
                self.assertEqual(fileobj.read(), b'')

    def test_FromStream_defaults(self):
        stream = _Stream()
        klass = self._getTargetClass()
        download = klass.FromStream(stream)
        self.assertTrue(download.stream is stream)
        self.assertTrue(download.auto_transfer)
        self.assertTrue(download.total_size is None)

    def test_FromStream_explicit(self):
        CHUNK_SIZE = 1 << 18
        SIZE = 123
        stream = _Stream()
        klass = self._getTargetClass()
        download = klass.FromStream(stream, auto_transfer=False,
                                    total_size=SIZE, chunksize=CHUNK_SIZE)
        self.assertTrue(download.stream is stream)
        self.assertFalse(download.auto_transfer)
        self.assertEqual(download.total_size, SIZE)
        self.assertEqual(download.chunksize, CHUNK_SIZE)

    def test_ConfigureRequest(self):
        CHUNK_SIZE = 100
        download = self._makeOne(_Stream(), chunksize=CHUNK_SIZE)
        request = _Dummy(headers={})
        url_builder = _Dummy(query_params={})
        download.ConfigureRequest(request, url_builder)
        self.assertEqual(request.headers, {'Range': 'bytes=0-99'})
        self.assertEqual(url_builder.query_params, {'alt': 'media'})

    def test__SetTotal_wo_content_range_wo_existing_total(self):
        info = {}
        download = self._makeOne(_Stream())
        download._SetTotal(info)
        self.assertEqual(download.total_size, 0)

    def test__SetTotal_wo_content_range_w_existing_total(self):
        SIZE = 123
        info = {}
        download = self._makeOne(_Stream(), total_size=SIZE)
        download._SetTotal(info)
        self.assertEqual(download.total_size, SIZE)

    def test__SetTotal_w_content_range_w_existing_total(self):
        SIZE = 123
        info = {'content-range': 'bytes 123-234/4567'}
        download = self._makeOne(_Stream(), total_size=SIZE)
        download._SetTotal(info)
        self.assertEqual(download.total_size, 4567)

    def test__SetTotal_w_content_range_w_asterisk_total(self):
        info = {'content-range': 'bytes 123-234/*'}
        download = self._makeOne(_Stream())
        download._SetTotal(info)
        self.assertEqual(download.total_size, 0)

    def test_InitializeDownload_already_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())
        download._Initialize(None, self.URL)
        with self.assertRaises(TransferInvalidError):
            download.InitializeDownload(request, http=object())

    def test_InitializeDownload_wo_http_or_client(self):
        from gcloud.streaming.exceptions import UserError
        request = _Request()
        download = self._makeOne(_Stream())
        with self.assertRaises(UserError):
            download.InitializeDownload(request)

    def test_InitializeDownload_wo_client_wo_autotransfer(self):
        request = _Request()
        http = object()
        download = self._makeOne(_Stream(), auto_transfer=False)
        download.InitializeDownload(request, http)
        self.assertTrue(download.http is http)
        self.assertEqual(download.url, request.url)

    def test_InitializeDownload_w_client_wo_autotransfer(self):
        FINALIZED_URL = 'http://example.com/other'
        request = _Request()
        http = object()
        client = _Client(http, FINALIZED_URL)
        download = self._makeOne(_Stream(), auto_transfer=False)
        download.InitializeDownload(request, client=client)
        self.assertTrue(download.http is http)
        self.assertEqual(download.url, FINALIZED_URL)

    def test_InitializeDownload_w_autotransfer_failing(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.exceptions import HttpError
        request = _Request()
        http = object()
        download = self._makeOne(_Stream(), auto_transfer=True)

        response = _makeResponse(http_client.BAD_REQUEST)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     MakeRequest=requester):
            with self.assertRaises(HttpError):
                download.InitializeDownload(request, http)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)

    def test_InitializeDownload_w_autotransfer_w_content_location(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        REDIRECT_URL = 'http://example.com/other'
        request = _Request()
        http = object()
        info = {'content-location': REDIRECT_URL}
        download = self._makeOne(_Stream(), auto_transfer=True)

        response = _makeResponse(http_client.NO_CONTENT, info)
        requester = _MakeRequest(response)

        with _Monkey(MUT, MakeRequest=requester):
            download.InitializeDownload(request, http)

        self.assertTrue(download._initial_response is None)
        self.assertEqual(download.total_size, 0)
        self.assertTrue(download.http is http)
        self.assertEqual(download.url, REDIRECT_URL)
        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)

    def test__NormalizeStartEnd_w_end_w_start_lt_0(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())

        with self.assertRaises(TransferInvalidError):
            download._NormalizeStartEnd(-1, 0)

    def test__NormalizeStartEnd_w_end_w_start_gt_total(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes 0-1/2'})

        with self.assertRaises(TransferInvalidError):
            download._NormalizeStartEnd(3, 0)

    def test__NormalizeStartEnd_w_end_lt_start(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes 0-1/2'})

        with self.assertRaises(TransferInvalidError):
            download._NormalizeStartEnd(1, 0)

    def test__NormalizeStartEnd_w_end_gt_start(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes 0-1/2'})
        self.assertEqual(download._NormalizeStartEnd(1, 2), (1, 1))

    def test__NormalizeStartEnd_wo_end_w_start_lt_0(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes 0-1/2'})
        self.assertEqual(download._NormalizeStartEnd(-2), (0, 1))
        self.assertEqual(download._NormalizeStartEnd(-1), (1, 1))

    def test__NormalizeStartEnd_wo_end_w_start_ge_0(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes 0-1/100'})
        self.assertEqual(download._NormalizeStartEnd(0), (0, 99))
        self.assertEqual(download._NormalizeStartEnd(1), (1, 99))

    def test__SetRangeHeader_w_start_lt_0(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetRangeHeader(request, -1)
        self.assertEqual(request.headers['range'], 'bytes=-1')

    def test__SetRangeHeader_w_start_ge_0_wo_end(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetRangeHeader(request, 0)
        self.assertEqual(request.headers['range'], 'bytes=0-')

    def test__SetRangeHeader_w_start_ge_0_w_end(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetRangeHeader(request, 0, 1)
        self.assertEqual(request.headers['range'], 'bytes=0-1')

    def test__ComputeEndByte_w_start_lt_0_w_end(self):
        download = self._makeOne(_Stream())
        self.assertEqual(download._ComputeEndByte(-1, 1), 1)

    def test__ComputeEndByte_w_start_ge_0_wo_end_w_use_chunks(self):
        CHUNK_SIZE = 5
        download = self._makeOne(_Stream(), chunksize=CHUNK_SIZE)
        self.assertEqual(download._ComputeEndByte(0, use_chunks=True), 4)

    def test__ComputeEndByte_w_start_ge_0_w_end_w_use_chunks(self):
        CHUNK_SIZE = 5
        download = self._makeOne(_Stream(), chunksize=CHUNK_SIZE)
        self.assertEqual(download._ComputeEndByte(0, 3, use_chunks=True), 3)
        self.assertEqual(download._ComputeEndByte(0, 5, use_chunks=True), 4)

    def test__ComputeEndByte_w_start_ge_0_w_end_w_total_size(self):
        CHUNK_SIZE = 50
        download = self._makeOne(_Stream(), chunksize=CHUNK_SIZE)
        download._SetTotal({'content-range': 'bytes 0-1/10'})
        self.assertEqual(download._ComputeEndByte(0, 100, use_chunks=False), 9)
        self.assertEqual(download._ComputeEndByte(0, 8, use_chunks=False), 8)

    def test__ComputeEndByte_w_start_ge_0_wo_end_w_total_size(self):
        CHUNK_SIZE = 50
        download = self._makeOne(_Stream(), chunksize=CHUNK_SIZE)
        download._SetTotal({'content-range': 'bytes 0-1/10'})
        self.assertEqual(download._ComputeEndByte(0, use_chunks=False), 9)

    def test__GetChunk_not_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        request = _Request()
        http = object()
        download = self._makeOne(_Stream())

        with self.assertRaises(TransferInvalidError):
            found = download._GetChunk(0, 10)

    def test__GetChunk_wo_additional_headers(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        request = _Request()
        http = object()
        download = self._makeOne(_Stream())
        download._Initialize(http, request.URL)
        response = _makeResponse(http_client.OK)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            found = download._GetChunk(0, 10)

        self.assertTrue(found is response)
        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers['range'], 'bytes=0-10')

    def test__GetChunk_w_additional_headers(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        request = _Request()
        http = object()
        headers = {'foo': 'bar'}
        download = self._makeOne(_Stream())
        download._Initialize(http, request.URL)
        response = _makeResponse(http_client.OK)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            found = download._GetChunk(0, 10, additional_headers=headers)

        self.assertTrue(found is response)
        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers['range'], 'bytes=0-10')
        self.assertEqual(request.headers['foo'], 'bar')

    def test__ProcessResponse_w_FORBIDDEN(self):
        from gcloud.streaming.exceptions import HttpError
        from six.moves import http_client
        download = self._makeOne(_Stream())
        response = _makeResponse(http_client.FORBIDDEN)
        with self.assertRaises(HttpError):
            download._ProcessResponse(response)

    def test__ProcessResponse_w_NOT_FOUND(self):
        from gcloud.streaming.exceptions import HttpError
        from six.moves import http_client
        download = self._makeOne(_Stream())
        response = _makeResponse(http_client.NOT_FOUND)
        with self.assertRaises(HttpError):
            download._ProcessResponse(response)

    def test__ProcessResponse_w_other_error(self):
        from gcloud.streaming.exceptions import TransferRetryError
        from six.moves import http_client
        download = self._makeOne(_Stream())
        response = _makeResponse(http_client.BAD_REQUEST)
        with self.assertRaises(TransferRetryError):
            download._ProcessResponse(response)

    def test__ProcessResponse_w_OK_wo_encoding(self):
        from six.moves import http_client
        stream = _Stream()
        download = self._makeOne(stream)
        response = _makeResponse(http_client.OK, content='OK')
        found = download._ProcessResponse(response)
        self.assertTrue(found is response)
        self.assertEqual(stream._written, ['OK'])
        self.assertEqual(download.progress, 2)
        self.assertEqual(download.encoding, None)

    def test__ProcessResponse_w_PARTIAL_CONTENT_w_encoding(self):
        from six.moves import http_client
        stream = _Stream()
        download = self._makeOne(stream)
        info = {'content-encoding': 'blah'}
        response = _makeResponse(http_client.OK, info, 'PARTIAL')
        found = download._ProcessResponse(response)
        self.assertTrue(found is response)
        self.assertEqual(stream._written, ['PARTIAL'])
        self.assertEqual(download.progress, 7)
        self.assertEqual(download.encoding, 'blah')

    def test__ProcessResponse_w_REQUESTED_RANGE_NOT_SATISFIABLE(self):
        from six.moves import http_client
        stream = _Stream()
        download = self._makeOne(stream)
        response = _makeResponse(
            http_client.REQUESTED_RANGE_NOT_SATISFIABLE)
        found = download._ProcessResponse(response)
        self.assertTrue(found is response)
        self.assertEqual(stream._written, [])
        self.assertEqual(download.progress, 0)
        self.assertEqual(download.encoding, None)

    def test__ProcessResponse_w_NO_CONTENT(self):
        from six.moves import http_client
        stream = _Stream()
        download = self._makeOne(stream)
        response = _makeResponse(status_code=http_client.NO_CONTENT)
        found = download._ProcessResponse(response)
        self.assertTrue(found is response)
        self.assertEqual(stream._written, [''])
        self.assertEqual(download.progress, 0)
        self.assertEqual(download.encoding, None)

    def test_GetRange_not_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        request = _Request()
        http = object()
        download = self._makeOne(_Stream())
        with self.assertRaises(TransferInvalidError):
            found = download.GetRange(0, 10)

    def test_GetRange_wo_total_size_complete(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        REQ_RANGE = 'bytes=0-%d' % (LEN,)
        RESP_RANGE = 'bytes 0-%d/%d' % (LEN - 1, LEN)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            download.GetRange(0, LEN)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_wo_total_size_wo_end(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        START = 5
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=%d-%d' % (START, START + CHUNK_SIZE - 1,)
        RESP_RANGE = 'bytes %d-%d/%d' % (START, LEN - 1, LEN)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT[START:])
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            download.GetRange(START)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT[START:]])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_w_total_size_partial_w_additional_headers(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        PARTIAL_LEN = 5
        REQ_RANGE = 'bytes=0-%d' % (PARTIAL_LEN,)
        RESP_RANGE = 'bytes 0-%d/%d' % (PARTIAL_LEN, LEN,)
        request = _Request()
        headers = {'foo': 'bar'}
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, total_size=LEN)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info,
                                      CONTENT[:PARTIAL_LEN])
        response.length = LEN
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            download.GetRange(0, PARTIAL_LEN, additional_headers=headers)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'foo': 'bar', 'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT[:PARTIAL_LEN]])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_w_empty_chunk(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.exceptions import TransferRetryError
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        START = 5
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=%d-%d' % (START, START + CHUNK_SIZE - 1,)
        RESP_RANGE = 'bytes %d-%d/%d' % (START, LEN - 1, LEN)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            with self.assertRaises(TransferRetryError):
                download.GetRange(START)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [''])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_w_total_size_wo_use_chunks(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        CHUNK_SIZE = 3
        REQ_RANGE = 'bytes=0-%d' % (LEN - 1,)
        RESP_RANGE = 'bytes 0-%d/%d' % (LEN - 1, LEN,)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, total_size=LEN, chunksize=CHUNK_SIZE)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            download.GetRange(0, use_chunks=False)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_w_multiple_chunks(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CONTENT = b'ABCDE'
        LEN = len(CONTENT)
        CHUNK_SIZE = 3
        REQ_RANGE_1 = 'bytes=0-%d' % (CHUNK_SIZE - 1,)
        RESP_RANGE_1 = 'bytes 0-%d/%d' % (CHUNK_SIZE - 1, LEN)
        REQ_RANGE_2 = 'bytes=%d-%d' % (CHUNK_SIZE, LEN - 1)
        RESP_RANGE_2 = 'bytes %d-%d/%d' % (CHUNK_SIZE, LEN - 1, LEN)
        request_1, request_2 = _Request(), _Request()
        _requests = [request_1, request_2]
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        download._Initialize(http, request_1.URL)
        info_1 = {'content-range': RESP_RANGE_1}
        response_1 = _makeResponse(http_client.PARTIAL_CONTENT, info_1,
                                        CONTENT[:CHUNK_SIZE])
        info_2 = {'content-range': RESP_RANGE_2}
        response_2 = _makeResponse(http_client.OK, info_2,
                                        CONTENT[CHUNK_SIZE:])
        requester = _MakeRequest(response_1, response_2)

        with _Monkey(MUT,
                     Request=lambda url: _requests.pop(0),
                     MakeRequest=requester):
            download.GetRange(0)

        self.assertTrue(len(requester._requested), 2)
        self.assertTrue(requester._requested[0][0] is request_1)
        self.assertEqual(request_1.headers, {'range': REQ_RANGE_1})
        self.assertTrue(requester._requested[1][0] is request_2)
        self.assertEqual(request_2.headers, {'range': REQ_RANGE_2})
        self.assertEqual(stream._written, [b'ABC', b'DE'])
        self.assertEqual(download.total_size, LEN)

    def test_StreamInChunks_wo_additional_headers(self):
        download = self._makeOne(_Stream())
        _called_with = []

        def _stream_media(additional_headers=None, use_chunks=False):
            _called_with.append((additional_headers, use_chunks))

        download.StreamMedia = _stream_media

        download.StreamInChunks()

        self.assertEqual(_called_with, [(None, True)])

    def test_StreamInChunks_w_additional_headers(self):
        download = self._makeOne(_Stream())
        _called_with = []

        def _stream_media(additional_headers=None, use_chunks=False):
            _called_with.append((additional_headers, use_chunks))

        download.StreamMedia = _stream_media

        headers = {'foo': 'bar'}
        download.StreamInChunks(headers)

        self.assertEqual(_called_with, [(headers, True)])

    def test_StreamMedia_not_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        download = self._makeOne(_Stream())

        with self.assertRaises(TransferInvalidError):
            found = download.StreamMedia()

    def test_StreamMedia_w_initial_response_complete(self):
        from six.moves import http_client
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        RESP_RANGE = 'bytes 0-%d/%d' % (LEN - 1, LEN,)
        stream = _Stream()
        download = self._makeOne(stream, total_size=LEN)
        info = {'content-range': RESP_RANGE}
        download._initial_response = _makeResponse(
            http_client.OK, info, CONTENT)
        http = object()
        download._Initialize(http, _Request.URL)

        download.StreamMedia()

        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_StreamMedia_w_initial_response_incomplete(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CHUNK_SIZE = 3
        CONTENT = b'ABCDEF'
        LEN = len(CONTENT)
        RESP_RANGE_1 = 'bytes 0-%d/%d' % (CHUNK_SIZE - 1, LEN,)
        REQ_RANGE_2 = 'bytes=%d-%d' % (CHUNK_SIZE, LEN - 1)
        RESP_RANGE_2 = 'bytes %d-%d/%d' % (CHUNK_SIZE, LEN - 1, LEN,)
        stream = _Stream()
        http = object()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        info_1 = {'content-range': RESP_RANGE_1}
        download._initial_response = _makeResponse(
            http_client.PARTIAL_CONTENT, info_1, CONTENT[:CHUNK_SIZE])
        info_2 = {'content-range': RESP_RANGE_2}
        response_2 = _makeResponse(
            http_client.OK, info_2, CONTENT[CHUNK_SIZE:])
        requester = _MakeRequest(response_2)

        download._Initialize(http, _Request.URL)

        request = _Request()

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            download.StreamMedia()

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE_2})
        self.assertEqual(stream._written,
                         [CONTENT[:CHUNK_SIZE], CONTENT[CHUNK_SIZE:]])
        self.assertEqual(download.total_size, LEN)

    def test_StreamMedia_wo_initial_response_wo_total_size(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=0-%d' % (CHUNK_SIZE - 1)
        RESP_RANGE = 'bytes 0-%d/%d' % (LEN - 1, LEN,)
        stream = _Stream()
        http = object()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)
        download._Initialize(http, _Request.URL)

        request = _Request()

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            download.StreamMedia()

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_StreamMedia_wo_initial_response_w_addl_headers_wo_chunks(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=0-'
        RESP_RANGE = 'bytes 0-%d/%d' % (LEN - 1, LEN,)
        stream = _Stream()
        http = object()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)
        download._Initialize(http, _Request.URL)

        headers = {'foo': 'bar'}
        request = _Request()

        with _Monkey(MUT,
                     Request=lambda url: request,
                     MakeRequest=requester):
            download.StreamMedia(additional_headers=headers, use_chunks=False)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'foo': 'bar', 'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)


class Test_Upload(unittest2.TestCase):
    URL = "http://example.com/api"
    MIME_TYPE = 'application/octet-stream'
    UPLOAD_URL = 'http://example.com/upload/id=foobar'

    def _getTargetClass(self):
        from gcloud.streaming.transfer import Upload
        return Upload

    def _makeOne(self, stream, mime_type=MIME_TYPE, *args, **kw):
        return self._getTargetClass()(stream, mime_type, *args, **kw)

    def test_ctor_defaults(self):
        stream = _Stream()
        upload = self._makeOne(stream)
        self.assertTrue(upload.stream is stream)
        self.assertTrue(upload._final_response is None)
        self.assertTrue(upload._server_chunk_granularity is None)
        self.assertFalse(upload.complete)
        self.assertEqual(upload.mime_type, self.MIME_TYPE)
        self.assertEqual(upload.progress, 0)
        self.assertTrue(upload.strategy is None)
        self.assertTrue(upload.total_size is None)

    def test_ctor_w_kwds(self):
        stream = _Stream()
        CHUNK_SIZE = 123
        upload = self._makeOne(stream, chunksize=CHUNK_SIZE)
        self.assertTrue(upload.stream is stream)
        self.assertEqual(upload.mime_type, self.MIME_TYPE)
        self.assertEqual(upload.chunksize, CHUNK_SIZE)

    def test_FromFile_w_nonesuch_file(self):
        from gcloud.streaming.exceptions import NotFoundError
        klass = self._getTargetClass()
        filename = '~nosuchuser/file.txt'
        with self.assertRaises(NotFoundError):
            klass.FromFile(filename)

    def test_FromFile_wo_mimetype_w_unguessable_filename(self):
        import os
        from gcloud.streaming.exceptions import InvalidUserInputError
        klass = self._getTargetClass()
        CONTENT = b'EXISTING FILE W/ UNGUESSABLE MIMETYPE'
        with _tempdir() as tempdir:
            filename = os.path.join(tempdir, 'file.unguessable')
            with open(filename, 'wb') as fileobj:
                fileobj.write(CONTENT)
            with self.assertRaises(InvalidUserInputError):
                klass.FromFile(filename)

    def test_FromFile_wo_mimetype_w_guessable_filename(self):
        import os
        klass = self._getTargetClass()
        CONTENT = b'EXISTING FILE W/ GUESSABLE MIMETYPE'
        with _tempdir() as tempdir:
            filename = os.path.join(tempdir, 'file.txt')
            with open(filename, 'wb') as fileobj:
                fileobj.write(CONTENT)
            upload = klass.FromFile(filename)
            self.assertEqual(upload.mime_type, 'text/plain')
            self.assertTrue(upload.auto_transfer)
            self.assertEqual(upload.total_size, len(CONTENT))

    def test_FromFile_w_mimetype_w_auto_transfer_w_kwds(self):
        import os
        klass = self._getTargetClass()
        CONTENT = b'EXISTING FILE W/ GUESSABLE MIMETYPE'
        CHUNK_SIZE = 3
        with _tempdir() as tempdir:
            filename = os.path.join(tempdir, 'file.unguessable')
            with open(filename, 'wb') as fileobj:
                fileobj.write(CONTENT)
            upload = klass.FromFile(
                filename,
                mime_type=self.MIME_TYPE,
                auto_transfer=False,
                chunksize=CHUNK_SIZE)
            self.assertEqual(upload.mime_type, self.MIME_TYPE)
            self.assertFalse(upload.auto_transfer)
            self.assertEqual(upload.total_size, len(CONTENT))
            self.assertEqual(upload.chunksize, CHUNK_SIZE)

    def test_FromStream_wo_mimetype(self):
        from gcloud.streaming.exceptions import InvalidUserInputError
        klass = self._getTargetClass()
        stream = _Stream()
        with self.assertRaises(InvalidUserInputError):
            klass.FromStream(stream, mime_type=None)

    def test_FromStream_defaults(self):
        klass = self._getTargetClass()
        stream = _Stream()
        upload = klass.FromStream(stream, mime_type=self.MIME_TYPE)
        self.assertEqual(upload.mime_type, self.MIME_TYPE)
        self.assertTrue(upload.auto_transfer)
        self.assertEqual(upload.total_size, None)

    def test_FromStream_explicit(self):
        klass = self._getTargetClass()
        stream = _Stream()
        SIZE = 10
        CHUNK_SIZE = 3
        upload = klass.FromStream(
            stream,
            mime_type=self.MIME_TYPE,
            auto_transfer=False,
            total_size=SIZE,
            chunksize=CHUNK_SIZE)
        self.assertEqual(upload.mime_type, self.MIME_TYPE)
        self.assertFalse(upload.auto_transfer)
        self.assertEqual(upload.total_size, SIZE)
        self.assertEqual(upload.chunksize, CHUNK_SIZE)

    def test_strategy_setter_invalid(self):
        from gcloud.streaming.exceptions import UserError
        upload = self._makeOne(_Stream())
        with self.assertRaises(UserError):
            upload.strategy = object()
        with self.assertRaises(UserError):
            upload.strategy = 'unknown'

    def test_strategy_setter_SIMPLE_UPLOAD(self):
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        upload = self._makeOne(_Stream())
        upload.strategy = SIMPLE_UPLOAD
        self.assertEqual(upload.strategy, SIMPLE_UPLOAD)

    def test_strategy_setter_RESUMABLE_UPLOAD(self):
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        upload = self._makeOne(_Stream())
        upload.strategy = RESUMABLE_UPLOAD
        self.assertEqual(upload.strategy, RESUMABLE_UPLOAD)

    def test_total_size_setter_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        SIZE = 123
        upload = self._makeOne(_Stream)
        http = object()
        upload._Initialize(http, _Request.URL)
        with self.assertRaises(TransferInvalidError):
            upload.total_size = SIZE

    def test_total_size_setter_not_initialized(self):
        SIZE = 123
        upload = self._makeOne(_Stream)
        http = object()
        upload.total_size = SIZE
        self.assertEqual(upload.total_size, SIZE)

    def test__SetDefaultUploadStrategy_w_existing_strategy(self):
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        config = _Dummy(
            resumable_path='/resumable/endpoint',
            simple_multipart=True,
            simple_path='/upload/endpoint',
        )
        request = _Request()
        upload = self._makeOne(_Stream)
        upload.strategy = RESUMABLE_UPLOAD
        upload._SetDefaultUploadStrategy(config, request)
        self.assertEqual(upload.strategy, RESUMABLE_UPLOAD)

    def test__SetDefaultUploadStrategy_wo_resumable_path(self):
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        config = _Dummy(
            resumable_path=None,
            simple_multipart=True,
            simple_path='/upload/endpoint',
        )
        request = _Request()
        upload = self._makeOne(_Stream())
        upload._SetDefaultUploadStrategy(config, request)
        self.assertEqual(upload.strategy, SIMPLE_UPLOAD)

    def test__SetDefaultUploadStrategy_w_total_size_gt_threshhold(self):
        from gcloud.streaming.transfer import _RESUMABLE_UPLOAD_THRESHOLD
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        config = _UploadConfig()
        request = _Request()
        upload = self._makeOne(
            _Stream(), total_size=_RESUMABLE_UPLOAD_THRESHOLD + 1)
        upload._SetDefaultUploadStrategy(config, request)
        self.assertEqual(upload.strategy, RESUMABLE_UPLOAD)

    def test__SetDefaultUploadStrategy_w_body_wo_multipart(self):
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        config = _UploadConfig()
        config.simple_multipart = False
        request = _Request(body=CONTENT)
        upload = self._makeOne(_Stream(), total_size=len(CONTENT))
        upload._SetDefaultUploadStrategy(config, request)
        self.assertEqual(upload.strategy, RESUMABLE_UPLOAD)

    def test__SetDefaultUploadStrategy_w_body_w_multipart_wo_simple_path(self):
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        config = _UploadConfig()
        config.simple_path = None
        request = _Request(body=CONTENT)
        upload = self._makeOne(_Stream(), total_size=len(CONTENT))
        upload._SetDefaultUploadStrategy(config, request)
        self.assertEqual(upload.strategy, RESUMABLE_UPLOAD)

    def test__SetDefaultUploadStrategy_w_body_w_multipart_w_simple_path(self):
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        config = _UploadConfig()
        request = _Request(body=CONTENT)
        upload = self._makeOne(_Stream(), total_size=len(CONTENT))
        upload._SetDefaultUploadStrategy(config, request)
        self.assertEqual(upload.strategy, SIMPLE_UPLOAD)

    def test_ConfigureRequest_w_total_size_gt_max_size(self):
        from gcloud.streaming.exceptions import InvalidUserInputError
        MAX_SIZE = 1000
        config = _UploadConfig()
        config.max_size = MAX_SIZE
        request = _Request()
        url_builder = _Dummy()
        upload = self._makeOne(_Stream(), total_size=MAX_SIZE + 1)
        with self.assertRaises(InvalidUserInputError):
            upload.ConfigureRequest(config, request, url_builder)

    def test_ConfigureRequest_w_invalid_mimetype(self):
        from gcloud.streaming.exceptions import InvalidUserInputError
        config = _UploadConfig()
        config.accept = ('text/*',)
        request = _Request()
        url_builder = _Dummy()
        upload = self._makeOne(_Stream())
        with self.assertRaises(InvalidUserInputError):
            upload.ConfigureRequest(config, request, url_builder)

    def test_ConfigureRequest_w_simple_wo_body(self):
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        CONTENT = b'CONTENT'
        config = _UploadConfig()
        request = _Request()
        url_builder = _Dummy(query_params={})
        upload = self._makeOne(_Stream(CONTENT))
        upload.strategy = SIMPLE_UPLOAD

        upload.ConfigureRequest(config, request, url_builder)

        self.assertEqual(url_builder.query_params, {'uploadType': 'media'}) 
        self.assertEqual(url_builder.relative_path, config.simple_path)

        self.assertEqual(request.headers, {'content-type': self.MIME_TYPE})
        self.assertEqual(request.body, CONTENT)
        self.assertEqual(request.loggable_body, '<media body>')

    def test_ConfigureRequest_w_simple_w_body(self):
        from email.parser import Parser
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        CONTENT = b'CONTENT'
        BODY = b'BODY'
        config = _UploadConfig()
        request = _Request(body=BODY)
        request.headers['content-type'] = 'text/plain'
        url_builder = _Dummy(query_params={})
        upload = self._makeOne(_Stream(CONTENT))
        upload.strategy = SIMPLE_UPLOAD

        upload.ConfigureRequest(config, request, url_builder)

        self.assertEqual(url_builder.query_params, {'uploadType': 'multipart'}) 
        self.assertEqual(url_builder.relative_path, config.simple_path)

        parser = Parser()
        self.assertEqual(list(request.headers), ['content-type'])
        ctype, boundary = [x.strip()
                           for x in request.headers['content-type'].split(';')]
        self.assertEqual(ctype, 'multipart/related')
        self.assertTrue(boundary.startswith('boundary="=='))
        self.assertTrue(boundary.endswith('=="'))

        divider = '--' + boundary[len('boundary="'):-1]
        chunks = request.body.split(divider)[1:-1]  # discard prolog / epilog
        self.assertEqual(len(chunks), 2)

        text_msg = parser.parsestr(chunks[0].strip())
        self.assertEqual(dict(text_msg._headers),
                         {'Content-Type': 'text/plain',
                          'MIME-Version': '1.0'})
        self.assertEqual(text_msg._payload, BODY.decode('ascii'))

        app_msg = parser.parsestr(chunks[1].strip())
        self.assertEqual(dict(app_msg._headers),
                         {'Content-Type': self.MIME_TYPE,
                          'Content-Transfer-Encoding': 'binary',
                          'MIME-Version': '1.0'})
        self.assertEqual(app_msg._payload, CONTENT.decode('ascii'))
        self.assertTrue('<media body>' in request.loggable_body)

    def test_ConfigureRequest_w_resumable_wo_total_size(self):
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'CONTENT'
        config = _UploadConfig()
        request = _Request()
        url_builder = _Dummy(query_params={})
        upload = self._makeOne(_Stream(CONTENT))
        upload.strategy = RESUMABLE_UPLOAD

        upload.ConfigureRequest(config, request, url_builder)

        self.assertEqual(url_builder.query_params, {'uploadType': 'resumable'}) 
        self.assertEqual(url_builder.relative_path, config.resumable_path)

        self.assertEqual(request.headers,
                         {'X-Upload-Content-Type': self.MIME_TYPE})

    def test_ConfigureRequest_w_resumable_w_total_size(self):
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'CONTENT'
        LEN = len(CONTENT)
        config = _UploadConfig()
        request = _Request()
        url_builder = _Dummy(query_params={})
        upload = self._makeOne(_Stream(CONTENT))
        upload.total_size = LEN
        upload.strategy = RESUMABLE_UPLOAD

        upload.ConfigureRequest(config, request, url_builder)

        self.assertEqual(url_builder.query_params, {'uploadType': 'resumable'}) 
        self.assertEqual(url_builder.relative_path, config.resumable_path)

        self.assertEqual(request.headers,
                         {'X-Upload-Content-Type': self.MIME_TYPE,
                          'X-Upload-Content-Length': '%d' % (LEN,)})

    def test_RefreshResumableUploadState_w_simple_strategy(self):
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        upload = self._makeOne(_Stream())
        upload.strategy = SIMPLE_UPLOAD
        upload.RefreshResumableUploadState()  # no-op

    def test_RefreshResumableUploadState_not_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        upload = self._makeOne(_Stream())
        upload.strategy = RESUMABLE_UPLOAD
        with self.assertRaises(TransferInvalidError):
            upload.RefreshResumableUploadState()

    def test_RefreshResumableUploadState_w_OK(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        RESP_RANGE = 'bytes 0-%d/%d' % (LEN - 1, LEN,)
        http = object()
        stream = _Stream()
        upload = self._makeOne(stream, total_size=LEN)
        upload.strategy = RESUMABLE_UPLOAD
        upload._Initialize(http, _Request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=_Request,
                     MakeRequest=requester):
            upload.RefreshResumableUploadState()

        self.assertTrue(upload.complete)
        self.assertEqual(upload.progress, LEN)
        self.assertEqual(stream.tell(), LEN)
        self.assertTrue(upload._final_response is response)

    def test_RefreshResumableUploadState_w_CREATED(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        RESP_RANGE = 'bytes 0-%d/%d' % (LEN - 1, LEN,)
        http = object()
        stream = _Stream()
        upload = self._makeOne(stream, total_size=LEN)
        upload.strategy = RESUMABLE_UPLOAD
        upload._Initialize(http, _Request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.CREATED, info, CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=_Request,
                     MakeRequest=requester):
            upload.RefreshResumableUploadState()

        self.assertTrue(upload.complete)
        self.assertEqual(upload.progress, LEN)
        self.assertEqual(stream.tell(), LEN)
        self.assertTrue(upload._final_response is response)

    def test_RefreshResumableUploadState_w_RESUME_INCOMPLETE_w_range(self):
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.http_wrapper import RESUME_INCOMPLETE
        from gcloud._testing import _Monkey
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        LAST = 5
        http = object()
        stream = _Stream()
        upload = self._makeOne(stream, total_size=LEN)
        upload.strategy = RESUMABLE_UPLOAD
        upload._Initialize(http, _Request.URL)
        info = {'range': '0-%d' % (LAST - 1,)}
        response = _makeResponse(RESUME_INCOMPLETE, info, CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=_Request,
                     MakeRequest=requester):
            upload.RefreshResumableUploadState()

        self.assertFalse(upload.complete)
        self.assertEqual(upload.progress, LAST)
        self.assertEqual(stream.tell(), LAST)
        self.assertFalse(upload._final_response is response)

    def test_RefreshResumableUploadState_w_RESUME_INCOMPLETE_wo_range(self):
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.http_wrapper import RESUME_INCOMPLETE
        from gcloud._testing import _Monkey
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        LAST = 5
        http = object()
        stream = _Stream()
        upload = self._makeOne(stream, total_size=LEN)
        upload.strategy = RESUMABLE_UPLOAD
        upload._Initialize(http, _Request.URL)
        response = _makeResponse(RESUME_INCOMPLETE, content=CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=_Request,
                     MakeRequest=requester):
            upload.RefreshResumableUploadState()

        self.assertFalse(upload.complete)
        self.assertEqual(upload.progress, 0)
        self.assertEqual(stream.tell(), 0)
        self.assertFalse(upload._final_response is response)

    def test_RefreshResumableUploadState_w_error(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.exceptions import HttpError
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        http = object()
        stream = _Stream()
        upload = self._makeOne(stream, total_size=LEN)
        upload.strategy = RESUMABLE_UPLOAD
        upload._Initialize(http, _Request.URL)
        response = _makeResponse(http_client.FORBIDDEN)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=_Request,
                     MakeRequest=requester):
            with self.assertRaises(HttpError):
                upload.RefreshResumableUploadState()

    def test__GetRangeHeaderFromResponse_miss(self):
        upload = self._makeOne(_Stream())
        response = _makeResponse(None)
        self.assertTrue(upload._GetRangeHeaderFromResponse(response) is None)

    def test__GetRangeHeaderFromResponse_w_Range(self):
        upload = self._makeOne(_Stream())
        response = _makeResponse(None, {'Range': '123'})
        self.assertEqual(upload._GetRangeHeaderFromResponse(response), '123')

    def test__GetRangeHeaderFromResponse_w_range(self):
        upload = self._makeOne(_Stream())
        response = _makeResponse(None, {'range': '123'})
        self.assertEqual(upload._GetRangeHeaderFromResponse(response), '123')

    def test_InitializeUpload_no_strategy(self):
        from gcloud.streaming.exceptions import UserError
        request = _Request()
        upload = self._makeOne(_Stream())
        with self.assertRaises(UserError):
            upload.InitializeUpload(request, http=object())

    def test_InitializeUpload_wo_client_wo_http(self):
        from gcloud.streaming.exceptions import UserError
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        request = _Request()
        upload = self._makeOne(_Stream())
        upload.strategy = SIMPLE_UPLOAD
        with self.assertRaises(UserError):
            upload.InitializeUpload(request)

    def test_InitializeUpload_simple_w_http(self):
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        request = _Request()
        upload = self._makeOne(_Stream())
        upload.strategy = SIMPLE_UPLOAD
        upload.InitializeUpload(request, http=object())  # no-op

    def test_InitializeUpload_resumable_already_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        request = _Request()
        upload = self._makeOne(_Stream())
        upload.strategy = RESUMABLE_UPLOAD
        upload._Initialize(None, self.URL)
        with self.assertRaises(TransferInvalidError):
            upload.InitializeUpload(request, http=object())

    def test_InitializeUpload_w_http_resumable_not_initialized_w_error(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.exceptions import HttpError
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        request = _Request()
        upload = self._makeOne(_Stream())
        upload.strategy = RESUMABLE_UPLOAD
        response = _makeResponse(http_client.FORBIDDEN)
        requester = _MakeRequest(response)

        with _Monkey(MUT, MakeRequest=requester):
            with self.assertRaises(HttpError):
                upload.InitializeUpload(request, http=object())

    def test_InitializeUpload_w_http_wo_auto_transfer_w_OK(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        request = _Request()
        upload = self._makeOne(_Stream(), auto_transfer=False)
        upload.strategy = RESUMABLE_UPLOAD
        info = {'location': self.UPLOAD_URL}
        response = _makeResponse(http_client.OK, info)
        requester = _MakeRequest(response)

        with _Monkey(MUT, MakeRequest=requester):
            upload.InitializeUpload(request, http=object())

        self.assertEqual(upload._server_chunk_granularity, None)
        self.assertEqual(upload.url, self.UPLOAD_URL)
        self.assertEqual(requester._responses, [])
        self.assertEqual(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)

    def test_InitializeUpload_w_client_w_auto_transfer_w_OK(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        LEN = len(CONTENT)
        FINALIZED_URL = 'http://example.com/upload?id=foobar&final'
        http = object()
        client = _Client(http, FINALIZED_URL)
        request = _Request()
        upload = self._makeOne(_Stream(CONTENT), chunksize=1000)
        upload.strategy = RESUMABLE_UPLOAD
        info = {'X-Goog-Upload-Chunk-Granularity': '100',
                'location': self.UPLOAD_URL}
        response = _makeResponse(http_client.OK, info)
        chunk_response = _makeResponse(http_client.OK)
        requester = _MakeRequest(response, chunk_response)

        with _Monkey(MUT,
                     Request=lambda url, http_method, body:
                            _Request(url, http_method, body),
                     MakeRequest=requester):
            upload.InitializeUpload(request, client=client)

        self.assertEqual(upload._server_chunk_granularity, 100)
        self.assertEqual(upload.url, FINALIZED_URL)
        self.assertEqual(requester._responses, [])
        self.assertEqual(len(requester._requested), 2)
        self.assertTrue(requester._requested[0][0] is request)
        chunk_request = requester._requested[1][0]
        self.assertTrue(isinstance(chunk_request, _Request))
        self.assertEqual(chunk_request.url, FINALIZED_URL)
        self.assertEqual(chunk_request.http_method, 'PUT')
        self.assertEqual(chunk_request.body, CONTENT)

    def test__GetLastByte(self):
        upload = self._makeOne(_Stream())
        self.assertEqual(upload._GetLastByte('123-456'), 456)

    def test__ValidateChunkSize_wo__server_chunk_granularity(self):
        upload = self._makeOne(_Stream())
        upload._ValidateChunksize(123)  # no-op

    def test__ValidateChunkSize_w__server_chunk_granularity_miss(self):
        from gcloud.streaming.exceptions import ConfigurationValueError
        upload = self._makeOne(_Stream())
        upload._server_chunk_granularity = 100
        with self.assertRaises(ConfigurationValueError):
            upload._ValidateChunksize(123)

    def test__ValidateChunkSize_w__server_chunk_granularity_hit(self):
        upload = self._makeOne(_Stream())
        upload._server_chunk_granularity = 100
        upload._ValidateChunksize(400)

    def test__StreamMedia_w_simple_strategy(self):
        from gcloud.streaming.exceptions import InvalidUserInputError
        from gcloud.streaming.transfer import SIMPLE_UPLOAD
        upload = self._makeOne(_Stream())
        upload.strategy = SIMPLE_UPLOAD
        with self.assertRaises(InvalidUserInputError):
            upload._StreamMedia()

    def test__StreamMedia_w_use_chunks_invalid_chunk_size(self):
        from gcloud.streaming.exceptions import ConfigurationValueError
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        upload = self._makeOne(_Stream(), chunksize=1024)
        upload.strategy = RESUMABLE_UPLOAD
        upload._server_chunk_granularity = 100
        with self.assertRaises(ConfigurationValueError):
            upload._StreamMedia(use_chunks=True)

    def test__StreamMedia_not_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        upload = self._makeOne(_Stream(), chunksize=1024)
        upload.strategy = RESUMABLE_UPLOAD
        upload._server_chunk_granularity = 128
        with self.assertRaises(TransferInvalidError):
            upload._StreamMedia()

    def test__StreamMedia_already_complete_w_unseekable_stream(self):
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        http = object()
        stream = object()
        response = object()
        upload = self._makeOne(stream, chunksize=1024)
        upload.strategy = RESUMABLE_UPLOAD
        upload._server_chunk_granularity = 128
        upload._Initialize(http, _Request.URL)
        upload._final_response = response
        upload._complete = True
        self.assertTrue(upload._StreamMedia() is response)

    def test__StreamMedia_already_complete_w_seekable_stream_unsynced(self):
        from gcloud.streaming.exceptions import CommunicationError
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        http = object()
        stream = _Stream(CONTENT)
        response = object()
        upload = self._makeOne(stream, chunksize=1024)
        upload.strategy = RESUMABLE_UPLOAD
        upload._server_chunk_granularity = 128
        upload._Initialize(http, _Request.URL)
        upload._final_response = response
        upload._complete = True
        with self.assertRaises(CommunicationError):
            upload._StreamMedia()

    def test__StreamMedia_already_complete_w_seekable_stream_synced(self):
        import os
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        http = object()
        stream = _Stream(CONTENT)
        stream.seek(0, os.SEEK_END)
        response = object()
        upload = self._makeOne(stream, chunksize=1024)
        upload.strategy = RESUMABLE_UPLOAD
        upload._server_chunk_granularity = 128
        upload._Initialize(http, _Request.URL)
        upload._final_response = response
        upload._complete = True
        self.assertTrue(upload._StreamMedia(use_chunks=False) is response)

    def test__StreamMedia_incomplete(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.http_wrapper import RESUME_INCOMPLETE
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        http = object()
        stream = _Stream(CONTENT)
        upload = self._makeOne(stream, chunksize=6)
        upload.strategy = RESUMABLE_UPLOAD
        upload._server_chunk_granularity = 6
        upload._Initialize(http, self.UPLOAD_URL)

        info_1 = {'content-length': '0', 'range': 'bytes=0-5'}
        response_1 = _makeResponse(RESUME_INCOMPLETE, info_1)
        info_2 = {'content-length': '0', 'range': 'bytes=6-9'}
        response_2 = _makeResponse(http_client.OK, info_2)
        requester = _MakeRequest(response_1, response_2)

        with _Monkey(MUT,
                     Request=lambda url, http_method, body:
                            _Request(url, http_method, body),
                     MakeRequest=requester):
            response = upload._StreamMedia()

        self.assertEqual(len(requester._responses), 0)
        self.assertEqual(len(requester._requested), 2)

        request_1 = requester._requested[0][0]
        self.assertEqual(request_1.url, self.UPLOAD_URL)
        self.assertEqual(request_1.http_method, 'PUT')
        self.assertEqual(request_1.headers,
                         {'Content-Range': 'bytes 0-5/*',
                          'Content-Type': self.MIME_TYPE})
        self.assertEqual(request_1.body, CONTENT[:6])

        request_2 = requester._requested[1][0]
        self.assertEqual(request_2.url, self.UPLOAD_URL)
        self.assertEqual(request_2.http_method, 'PUT')
        self.assertEqual(request_2.headers,
                         {'Content-Range': 'bytes 6-9/10',
                          'Content-Type': self.MIME_TYPE})
        self.assertEqual(request_2.body, CONTENT[6:])

    def test__StreamMedia_incomplete_w_transfer_error_w_addl_headers(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.exceptions import CommunicationError
        from gcloud.streaming.http_wrapper import RESUME_INCOMPLETE
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        http = object()
        stream = _Stream(CONTENT)
        headers = {'foo': 'bar'}
        upload = self._makeOne(stream, chunksize=6)
        upload.strategy = RESUMABLE_UPLOAD
        upload._server_chunk_granularity = 6
        upload._Initialize(http, self.UPLOAD_URL)

        info = {'content-length': '0',
                'range': 'bytes=0-4',  # simulate error, s.b. '0-5'
               }
        response = _makeResponse(RESUME_INCOMPLETE, info)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     Request=lambda url, http_method, body:
                            _Request(url, http_method, body),
                     MakeRequest=requester):
            with self.assertRaises(CommunicationError):
                upload._StreamMedia(additional_headers=headers)

        self.assertEqual(len(requester._responses), 0)
        self.assertEqual(len(requester._requested), 1)

        request = requester._requested[0][0]
        self.assertEqual(request.url, self.UPLOAD_URL)
        self.assertEqual(request.http_method, 'PUT')
        self.assertEqual(request.headers,
                         {'Content-Range': 'bytes 0-5/*',
                          'Content-Type': self.MIME_TYPE,
                          'foo': 'bar'})
        self.assertEqual(request.body, CONTENT[:6])

    def test_StreamMedia_defaults(self):
        upload = self._makeOne(_Stream())
        response = object()
        upload._StreamMedia = streamer = _MediaStreamer(response)
        self.assertTrue(upload.StreamMedia() is response)
        self.assertEqual(streamer._called_with, (None, False))

    def test_StreamMedia_explicit(self):
        upload = self._makeOne(_Stream())
        response = object()
        headers = {'foo': 'bar'}
        upload._StreamMedia = streamer = _MediaStreamer(response)
        self.assertTrue(upload.StreamMedia(headers) is response)
        self.assertEqual(streamer._called_with, (headers, False))

    def test_StreamInChunks_defaults(self):
        upload = self._makeOne(_Stream())
        response = object()
        upload._StreamMedia = streamer = _MediaStreamer(response)
        self.assertTrue(upload.StreamInChunks() is response)
        self.assertEqual(streamer._called_with, (None, True))

    def test_StreamInChunks_explicit(self):
        upload = self._makeOne(_Stream())
        response = object()
        headers = {'foo': 'bar'}
        upload._StreamMedia = streamer = _MediaStreamer(response)
        self.assertTrue(upload.StreamInChunks(headers) is response)
        self.assertEqual(streamer._called_with, (headers, True))

    def test__SendMediaRequest_wo_error(self):
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.http_wrapper import RESUME_INCOMPLETE
        CONTENT = b'ABCDEFGHIJ'
        bytes_http = object()
        stream = _Stream(CONTENT)
        upload = self._makeOne(stream)
        upload.bytes_http = bytes_http

        headers = {'Content-Range': 'bytes 0-9/10',
                   'Content-Type': self.MIME_TYPE}
        request = _Request(self.UPLOAD_URL, 'PUT', CONTENT, headers)
        info = {'content-length': '0', 'range': 'bytes=0-4'}
        response = _makeResponse(RESUME_INCOMPLETE, info)
        requester = _MakeRequest(response)

        with _Monkey(MUT, MakeRequest=requester):
            upload._SendMediaRequest(request, 9)

        self.assertEqual(len(requester._responses), 0)
        self.assertEqual(len(requester._requested), 1)
        used_request, used_http, _ = requester._requested[0]
        self.assertTrue(used_request is request)
        self.assertTrue(used_http is bytes_http)
        self.assertEqual(stream.tell(), 4)

    def test__SendMediaRequest_w_error(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud.streaming import transfer as MUT
        from gcloud.streaming.exceptions import HttpError
        from gcloud.streaming.http_wrapper import RESUME_INCOMPLETE
        from gcloud.streaming.transfer import RESUMABLE_UPLOAD
        CONTENT = b'ABCDEFGHIJ'
        bytes_http = object()
        http = object()
        stream = _Stream(CONTENT)
        upload = self._makeOne(stream)
        upload.strategy = RESUMABLE_UPLOAD
        upload._Initialize(http, self.UPLOAD_URL)
        upload.bytes_http = bytes_http

        headers = {'Content-Range': 'bytes 0-9/10',
                   'Content-Type': self.MIME_TYPE}
        request = _Request(self.UPLOAD_URL, 'PUT', CONTENT, headers)
        info_1 = {'content-length': '0', 'range': 'bytes=0-4'}
        response_1 = _makeResponse(http_client.FORBIDDEN, info_1)
        info_2 = {'Content-Length': '0', 'Range': 'bytes=0-4'}
        response_2 = _makeResponse(RESUME_INCOMPLETE, info_2)
        requester = _MakeRequest(response_1, response_2)

        with _Monkey(MUT,
                     Request=_Request,
                     MakeRequest=requester):
            with self.assertRaises(HttpError):
                upload._SendMediaRequest(request, 9)

        self.assertEqual(len(requester._responses), 0)
        self.assertEqual(len(requester._requested), 2)
        first_request, first_http, _ = requester._requested[0]
        self.assertTrue(first_request is request)
        self.assertTrue(first_http is bytes_http)
        second_request, second_http, _ = requester._requested[1]
        self.assertEqual(second_request.url, self.UPLOAD_URL)
        self.assertEqual(second_request.http_method, 'PUT')  # ACK!
        self.assertEqual(second_request.headers,
                         {'Content-Range': 'bytes */*'})
        self.assertTrue(second_http is http)

    def test__SendMediaBody_not_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        upload = self._makeOne(_Stream())
        with self.assertRaises(TransferInvalidError):
            upload._SendMediaBody(0)

    def test__SendMediaBody_wo_total_size(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        http = object()
        upload = self._makeOne(_Stream())
        upload._Initialize(http, _Request.URL)
        with self.assertRaises(TransferInvalidError):
            upload._SendMediaBody(0)

    def test__SendMediaBody_wo_additional_headers_start_lt_total_size(self):
        from gcloud.streaming.stream_slice import StreamSlice
        SIZE = 1234
        http = object()
        stream = _Stream()
        upload = self._makeOne(stream, total_size=SIZE)
        upload._Initialize(http, self.UPLOAD_URL)
        headers = {'foo': 'bar'}
        _called_with = []
        response = object()

        def _send_media_request(request, end):
            _called_with.append((request, end))
            return response

        upload._SendMediaRequest = _send_media_request

        found = upload._SendMediaBody(0)

        self.assertTrue(found is response)
        self.assertEqual(len(_called_with), 1)
        request, end = _called_with[0]
        self.assertEqual(request.url, self.UPLOAD_URL)
        self.assertEqual(request.http_method, 'PUT')
        body_stream = request.body
        self.assertTrue(isinstance(body_stream, StreamSlice))
        self.assertTrue(body_stream._stream is stream)
        self.assertEqual(len(body_stream), SIZE)
        self.assertEqual(request.headers,
                         {'content-length': '%d' % (SIZE,),  # speling!
                          'Content-Type': self.MIME_TYPE,
                          'Content-Range': 'bytes 0-%d/%d' % (SIZE - 1, SIZE)})
        self.assertEqual(end, SIZE)

    def test__SendMediaBody_w_additional_headers_start_eq_total_size(self):
        from gcloud.streaming.stream_slice import StreamSlice
        SIZE = 1234
        http = object()
        stream = _Stream()
        upload = self._makeOne(stream, total_size=SIZE)
        upload._Initialize(http, self.UPLOAD_URL)
        headers = {'foo': 'bar'}
        _called_with = []
        response = object()

        def _send_media_request(request, end):
            _called_with.append((request, end))
            return response

        upload._SendMediaRequest = _send_media_request

        found = upload._SendMediaBody(SIZE, additional_headers=headers)

        self.assertTrue(found is response)
        self.assertEqual(len(_called_with), 1)
        request, end = _called_with[0]
        self.assertEqual(request.url, self.UPLOAD_URL)
        self.assertEqual(request.http_method, 'PUT')
        body_stream = request.body
        self.assertTrue(isinstance(body_stream, StreamSlice))
        self.assertTrue(body_stream._stream is stream)
        self.assertEqual(len(body_stream), 0)
        self.assertEqual(request.headers,
                         {'content-length': '0',  # speling!
                          'foo': 'bar',
                          'Content-Type': self.MIME_TYPE,
                          'Content-Range': 'bytes */%d' % (SIZE,)})
        self.assertEqual(end, SIZE)

    def test__SendChunk_not_initialized(self):
        from gcloud.streaming.exceptions import TransferInvalidError
        upload = self._makeOne(_Stream())
        with self.assertRaises(TransferInvalidError):
            upload._SendChunk(0)

    def test__SendChunk_wo_total_size_stream_exhausted(self):
        CONTENT = b'ABCDEFGHIJ'
        SIZE = len(CONTENT)
        http = object()
        upload = self._makeOne(_Stream(CONTENT), chunksize=1000)
        upload._Initialize(http, self.UPLOAD_URL)
        _called_with = []
        response = object()

        def _send_media_request(request, end):
            _called_with.append((request, end))
            return response

        upload._SendMediaRequest = _send_media_request
        self.assertEqual(upload.total_size, None)

        found = upload._SendChunk(0)

        self.assertTrue(found is response)
        self.assertEqual(upload.total_size, SIZE)
        self.assertEqual(len(_called_with), 1)
        request, end = _called_with[0]
        self.assertEqual(request.url, self.UPLOAD_URL)
        self.assertEqual(request.http_method, 'PUT')
        self.assertEqual(request.body, CONTENT)
        self.assertEqual(request.headers,
                         {'content-length': '%d' % SIZE,  # speling!
                          'Content-Type': self.MIME_TYPE,
                          'Content-Range': 'bytes 0-%d/%d' % (SIZE - 1, SIZE)})
        self.assertEqual(end, SIZE)

    def test__SendChunk_wo_total_size_stream_not_exhausted(self):
        CONTENT = b'ABCDEFGHIJ'
        SIZE = len(CONTENT)
        CHUNK_SIZE = SIZE - 5
        http = object()
        upload = self._makeOne(_Stream(CONTENT), chunksize=CHUNK_SIZE)
        upload._Initialize(http, self.UPLOAD_URL)
        _called_with = []
        response = object()

        def _send_media_request(request, end):
            _called_with.append((request, end))
            return response

        upload._SendMediaRequest = _send_media_request
        self.assertEqual(upload.total_size, None)

        found = upload._SendChunk(0)

        self.assertTrue(found is response)
        self.assertEqual(upload.total_size, None)
        self.assertEqual(len(_called_with), 1)
        request, end = _called_with[0]
        self.assertEqual(request.url, self.UPLOAD_URL)
        self.assertEqual(request.http_method, 'PUT')
        self.assertEqual(request.body, CONTENT[:CHUNK_SIZE])
        self.assertEqual(request.headers,
                         {'content-length': '%d' % CHUNK_SIZE,  # speling!
                          'Content-Type': self.MIME_TYPE,
                          'Content-Range': 'bytes 0-%d/*' % (CHUNK_SIZE- 1,)})
        self.assertEqual(end, CHUNK_SIZE)

    def test__SendChunk_w_total_size_stream_not_exhausted(self):
        from gcloud.streaming.stream_slice import StreamSlice
        CONTENT = b'ABCDEFGHIJ'
        SIZE = len(CONTENT)
        CHUNK_SIZE = SIZE - 5
        http = object()
        stream = _Stream(CONTENT)
        upload = self._makeOne(stream, total_size=SIZE, chunksize=CHUNK_SIZE)
        upload._Initialize(http, self.UPLOAD_URL)
        _called_with = []
        response = object()

        def _send_media_request(request, end):
            _called_with.append((request, end))
            return response

        upload._SendMediaRequest = _send_media_request
        found = upload._SendChunk(0)

        self.assertTrue(found is response)
        request, end = _called_with[0]
        self.assertEqual(request.url, self.UPLOAD_URL)
        self.assertEqual(request.http_method, 'PUT')
        body_stream = request.body
        self.assertTrue(isinstance(body_stream, StreamSlice))
        self.assertTrue(body_stream._stream is stream)
        self.assertEqual(len(body_stream), CHUNK_SIZE)
        self.assertEqual(request.headers,
                         {'content-length': '%d' % CHUNK_SIZE,  # speling!
                          'Content-Type': self.MIME_TYPE,
                          'Content-Range': 'bytes 0-%d/%d'
                            % (CHUNK_SIZE- 1, SIZE)})
        self.assertEqual(end, CHUNK_SIZE)

    def test__SendChunk_w_total_size_stream_exhausted_w_addl_headers(self):
        from gcloud.streaming.stream_slice import StreamSlice
        CONTENT = b'ABCDEFGHIJ'
        SIZE = len(CONTENT)
        CHUNK_SIZE = 1000
        http = object()
        headers = {'foo': 'bar'}
        stream = _Stream(CONTENT)
        upload = self._makeOne(stream, total_size=SIZE, chunksize=CHUNK_SIZE)
        upload._Initialize(http, self.UPLOAD_URL)
        _called_with = []
        response = object()

        def _send_media_request(request, end):
            _called_with.append((request, end))
            return response

        upload._SendMediaRequest = _send_media_request

        found = upload._SendChunk(SIZE, additional_headers=headers)

        self.assertTrue(found is response)
        self.assertEqual(len(_called_with), 1)
        request, end = _called_with[0]
        self.assertEqual(request.url, self.UPLOAD_URL)
        self.assertEqual(request.http_method, 'PUT')
        body_stream = request.body
        self.assertTrue(isinstance(body_stream, StreamSlice))
        self.assertTrue(body_stream._stream is stream)
        self.assertEqual(len(body_stream), 0)
        self.assertEqual(request.headers,
                         {'content-length': '0',  # speling!
                          'foo': 'bar',
                          'Content-Type': self.MIME_TYPE,
                          'Content-Range': 'bytes */%d' % (SIZE,)})
        self.assertEqual(end, SIZE)


class _Dummy(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _UploadConfig(object):
    accept = ('*/*',)
    max_size = None
    resumable_path = '/resumable/endpoint'
    simple_multipart = True
    simple_path = '/upload/endpoint'
    

class _Stream(object):
    _closed = False

    def __init__(self, to_read=b''):
        import io
        self._written = []
        self._to_read = io.BytesIO(to_read)

    def write(self, to_write):
        self._written.append(to_write)

    def seek(self, offset, whence=0):
        self._to_read.seek(offset, whence)

    def read(self, size=None):
        if size is not None:
            return self._to_read.read(size)
        return self._to_read.read()

    def tell(self):
        return self._to_read.tell()

    def close(self):
        self._closed = True


class _Request(object):
    __slots__ = ('url', 'http_method', 'body', 'headers', 'loggable_body')
    URL = 'http://example.com/api'

    def __init__(self, url=URL, http_method='GET', body='', headers=None):
        self.url = url
        self.http_method = http_method
        self.body = self.loggable_body = body
        if headers is None:
            headers = {}
        self.headers = headers


class _Client(object):

    def __init__(self, http, finalized_url):
        self.http = http
        self._finalized_url = finalized_url

    def FinalizeTransferUrl(self, existing_url):
        return self._finalized_url


class _MakeRequest(object):

    def __init__(self, *responses):
        self._responses = list(responses)
        self._requested = []

    def __call__(self, http, request, **kw):
        self._requested.append((request, http, kw))
        return self._responses.pop(0)


def _makeResponse(status_code, info=None, content='',
                  request_url=_Request.URL):
    if info is None:
        info = {}
    return _Dummy(status_code=status_code,
                  info=info,
                  content=content,
                  length=len(content),
                  request_url=request_url)


class _MediaStreamer(object):

    _called_with = None

    def __init__(self, response):
        self._response = response

    def __call__(self, additional_headers=None, use_chunks=True):
        assert self._called_with is None
        self._called_with = (additional_headers, use_chunks)
        return self._response


def _tempdir():
    import contextlib
    import shutil
    import tempfile

    @contextlib.contextmanager
    def _tempdir():
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    return _tempdir

_tempdir = _tempdir()
