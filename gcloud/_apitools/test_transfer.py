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


class Test_Download(unittest2.TestCase):
    URL = "http://example.com/api"

    def _getTargetClass(self):
        from gcloud._apitools.transfer import Download
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
        from gcloud._apitools.exceptions import InvalidUserInputError
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
                self.assertEqual(fileobj.read(), '')

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
        info = {'content-range': 'bytes=123-234/4567'}
        download = self._makeOne(_Stream(), total_size=SIZE)
        download._SetTotal(info)
        self.assertEqual(download.total_size, 4567)

    def test__SetTotal_w_content_range_w_asterisk_total(self):
        info = {'content-range': 'bytes=123-234/*'}
        download = self._makeOne(_Stream())
        download._SetTotal(info)
        self.assertEqual(download.total_size, 0)

    def test_InitializeDownload_already_initialized(self):
        from gcloud._apitools.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())
        download._Initialize(None, self.URL)
        with self.assertRaises(TransferInvalidError):
            download.InitializeDownload(request, http=object())

    def test_InitializeDownload_wo_http_or_client(self):
        from gcloud._apitools.exceptions import UserError
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
        from gcloud._apitools import transfer as MUT
        from gcloud._apitools.exceptions import HttpError
        request = _Request()
        http = object()
        download = self._makeOne(_Stream(), auto_transfer=True)

        response = _makeResponse(http_client.BAD_REQUEST)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     http_wrapper=_Dummy(MakeRequest=requester)):
            with self.assertRaises(HttpError):
                download.InitializeDownload(request, http)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)

    def test_InitializeDownload_w_autotransfer_w_content_location(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        REDIRECT_URL = 'http://example.com/other'
        request = _Request()
        http = object()
        info = {'content-location': REDIRECT_URL}
        download = self._makeOne(_Stream(), auto_transfer=True)

        response = _makeResponse(http_client.NO_CONTENT, info)
        requester = _MakeRequest(response)

        with _Monkey(MUT, http_wrapper=_Dummy(MakeRequest=requester)):
            download.InitializeDownload(request, http)

        self.assertTrue(download._initial_response is None)
        self.assertEqual(download.total_size, 0)
        self.assertTrue(download.http is http)
        self.assertEqual(download.url, REDIRECT_URL)
        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)

    def test__NormalizeStartEnd_w_end_w_start_lt_0(self):
        from gcloud._apitools.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())

        with self.assertRaises(TransferInvalidError):
            download._NormalizeStartEnd(-1, 0)

    def test__NormalizeStartEnd_w_end_w_start_gt_total(self):
        from gcloud._apitools.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes=0-1/2'})

        with self.assertRaises(TransferInvalidError):
            download._NormalizeStartEnd(3, 0)

    def test__NormalizeStartEnd_w_end_lt_start(self):
        from gcloud._apitools.exceptions import TransferInvalidError
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes=0-1/2'})

        with self.assertRaises(TransferInvalidError):
            download._NormalizeStartEnd(1, 0)

    def test__NormalizeStartEnd_w_end_gt_start(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes=0-1/2'})
        self.assertEqual(download._NormalizeStartEnd(1, 2), (1, 1))

    def test__NormalizeStartEnd_wo_end_w_start_lt_0(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes=0-1/2'})
        self.assertEqual(download._NormalizeStartEnd(-2), (0, 1))
        self.assertEqual(download._NormalizeStartEnd(-1), (1, 1))

    def test__NormalizeStartEnd_wo_end_w_start_ge_0(self):
        request = _Request()
        download = self._makeOne(_Stream())
        download._SetTotal({'content-range': 'bytes=0-1/100'})
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
        download._SetTotal({'content-range': 'bytes=0-1/10'})
        self.assertEqual(download._ComputeEndByte(0, 100, use_chunks=False), 9)
        self.assertEqual(download._ComputeEndByte(0, 8, use_chunks=False), 8)

    def test__ComputeEndByte_w_start_ge_0_wo_end_w_total_size(self):
        CHUNK_SIZE = 50
        download = self._makeOne(_Stream(), chunksize=CHUNK_SIZE)
        download._SetTotal({'content-range': 'bytes=0-1/10'})
        self.assertEqual(download._ComputeEndByte(0, use_chunks=False), 9)

    def test__GetChunk_not_initialized(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        from gcloud._apitools.exceptions import TransferInvalidError
        request = _Request()
        http = object()
        download = self._makeOne(_Stream())
        response = _Dummy(status_code=http_client.OK,
                          info={}, content='', request_url=request.URL)

        def _make_request(http, http_request, retry_func, retries):
            return response

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=_make_request)):
            with self.assertRaises(TransferInvalidError):
                found = download._GetChunk(0, 10)

    def test__GetChunk_wo_additional_headers(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        request = _Request()
        http = object()
        download = self._makeOne(_Stream())
        download._Initialize(http, request.URL)
        response = _makeResponse(http_client.OK)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            found = download._GetChunk(0, 10)

        self.assertTrue(found is response)
        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers['range'], 'bytes=0-10')

    def test__GetChunk_w_additional_headers(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        request = _Request()
        http = object()
        headers = {'foo': 'bar'}
        download = self._makeOne(_Stream())
        download._Initialize(http, request.URL)
        response = _makeResponse(http_client.OK)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            found = download._GetChunk(0, 10, additional_headers=headers)

        self.assertTrue(found is response)
        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers['range'], 'bytes=0-10')
        self.assertEqual(request.headers['foo'], 'bar')

    def test__ProcessResponse_w_FORBIDDEN(self):
        from gcloud._apitools.exceptions import HttpError
        from six.moves import http_client
        download = self._makeOne(_Stream())
        response = _makeResponse(http_client.FORBIDDEN)
        with self.assertRaises(HttpError):
            download._ProcessResponse(response)

    def test__ProcessResponse_w_NOT_FOUND(self):
        from gcloud._apitools.exceptions import HttpError
        from six.moves import http_client
        download = self._makeOne(_Stream())
        response = _makeResponse(http_client.NOT_FOUND)
        with self.assertRaises(HttpError):
            download._ProcessResponse(response)

    def test__ProcessResponse_w_other_error(self):
        from gcloud._apitools.exceptions import TransferRetryError
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
        from gcloud._apitools.exceptions import TransferInvalidError
        request = _Request()
        http = object()
        download = self._makeOne(_Stream())
        with self.assertRaises(TransferInvalidError):
            found = download.GetRange(0, 10)

    def test_GetRange_wo_total_size_complete(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        REQ_RANGE = 'bytes=0-%d' % (LEN,)
        RESP_RANGE = 'bytes=0-%d/%d' % (LEN - 1, LEN)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            download.GetRange(0, LEN)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_wo_total_size_wo_end(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        START = 5
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=%d-%d' % (START, START + CHUNK_SIZE - 1,)
        RESP_RANGE = 'bytes=%d-%d/%d' % (START, LEN - 1, LEN)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT[START:])
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            download.GetRange(START)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT[START:]])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_w_total_size_partial_w_additional_headers(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        PARTIAL_LEN = 5
        REQ_RANGE = 'bytes=0-%d' % (PARTIAL_LEN,)
        RESP_RANGE = 'bytes=0-%d/%d' % (PARTIAL_LEN, LEN,)
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
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            download.GetRange(0, PARTIAL_LEN, additional_headers=headers)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'foo': 'bar', 'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT[:PARTIAL_LEN]])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_w_empty_chunk(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        from gcloud._apitools.exceptions import TransferRetryError
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        START = 5
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=%d-%d' % (START, START + CHUNK_SIZE - 1,)
        RESP_RANGE = 'bytes=%d-%d/%d' % (START, LEN - 1, LEN)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
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
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        CHUNK_SIZE = 3
        REQ_RANGE = 'bytes=0-%d' % (LEN - 1,)
        RESP_RANGE = 'bytes=0-%d/%d' % (LEN - 1, LEN,)
        request = _Request()
        http = object()
        stream = _Stream()
        download = self._makeOne(stream, total_size=LEN, chunksize=CHUNK_SIZE)
        download._Initialize(http, request.URL)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            download.GetRange(0, use_chunks=False)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_GetRange_w_multiple_chunks(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDE'
        LEN = len(CONTENT)
        CHUNK_SIZE = 3
        REQ_RANGE_1 = 'bytes=0-%d' % (CHUNK_SIZE - 1,)
        RESP_RANGE_1 = 'bytes=0-%d/%d' % (CHUNK_SIZE - 1, LEN)
        REQ_RANGE_2 = 'bytes=%d-%d' % (CHUNK_SIZE, LEN - 1)
        RESP_RANGE_2 = 'bytes=%d-%d/%d' % (CHUNK_SIZE, LEN - 1, LEN)
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
                     http_wrapper=_Dummy(
                        Request=lambda url: _requests.pop(0),
                        MakeRequest=requester)):
            download.GetRange(0)

        self.assertTrue(len(requester._requested), 2)
        self.assertTrue(requester._requested[0][0] is request_1)
        self.assertEqual(request_1.headers, {'range': REQ_RANGE_1})
        self.assertTrue(requester._requested[1][0] is request_2)
        self.assertEqual(request_2.headers, {'range': REQ_RANGE_2})
        self.assertEqual(stream._written, ['ABC', 'DE'])
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
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        from gcloud._apitools.exceptions import TransferInvalidError
        download = self._makeOne(_Stream())

        with _Monkey(MUT, http_wrapper=_Dummy()):
            with self.assertRaises(TransferInvalidError):
                found = download.StreamMedia()

    def test_StreamMedia_w_initial_response_complete(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        RESP_RANGE = 'bytes=0-%d/%d' % (LEN - 1, LEN,)
        stream = _Stream()
        download = self._makeOne(stream, total_size=LEN)
        info = {'content-range': RESP_RANGE}
        download._initial_response = _makeResponse(
            http_client.OK, info, CONTENT)
        http = object()
        download._Initialize(http, _Request.URL)

        with _Monkey(MUT,
                     http_wrapper=_Dummy()):
            download.StreamMedia()

        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_StreamMedia_w_initial_response_incomplete(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        CHUNK_SIZE = 3
        CONTENT = 'ABCDEF'
        LEN = len(CONTENT)
        RESP_RANGE_1 = 'bytes=0-%d/%d' % (CHUNK_SIZE - 1, LEN,)
        REQ_RANGE_2 = 'bytes=%d-%d' % (CHUNK_SIZE, LEN - 1)
        RESP_RANGE_2 = 'bytes=%d-%d/%d' % (CHUNK_SIZE, LEN - 1, LEN,)
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
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
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
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=0-%d' % (CHUNK_SIZE - 1)
        RESP_RANGE = 'bytes=0-%d/%d' % (LEN - 1, LEN,)
        stream = _Stream()
        http = object()
        download = self._makeOne(stream, chunksize=CHUNK_SIZE)
        info = {'content-range': RESP_RANGE}
        response = _makeResponse(http_client.OK, info, CONTENT)
        requester = _MakeRequest(response)
        download._Initialize(http, _Request.URL)

        request = _Request()

        with _Monkey(MUT,
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            download.StreamMedia()

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)

    def test_StreamMedia_wo_initial_response_w_addl_headers_wo_chunks(self):
        from six.moves import http_client
        from gcloud._testing import _Monkey
        from gcloud._apitools import transfer as MUT
        CONTENT = 'ABCDEFGHIJ'
        LEN = len(CONTENT)
        CHUNK_SIZE = 123
        REQ_RANGE = 'bytes=0-'
        RESP_RANGE = 'bytes=0-%d/%d' % (LEN - 1, LEN,)
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
                     http_wrapper=_Dummy(
                        Request=lambda url: request,
                        MakeRequest=requester)):
            download.StreamMedia(additional_headers=headers, use_chunks=False)

        self.assertTrue(len(requester._requested), 1)
        self.assertTrue(requester._requested[0][0] is request)
        self.assertEqual(request.headers, {'foo': 'bar', 'range': REQ_RANGE})
        self.assertEqual(stream._written, [CONTENT])
        self.assertEqual(download.total_size, LEN)


class _Dummy(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


class _Stream(object):
    _closed = False

    def __init__(self):
        self._written = []

    def write(self, to_write):
        self._written.append(to_write)

    def close(self):
        self._closed = True


class _Request(object):
    __slots__ = ('url', 'http_method', 'body', 'headers',)
    URL = 'http://example.com/api'

    def __init__(self, url=URL, http_method='GET', body=''):
        self.url = url
        self.http_method = http_method
        self.body = body
        self.headers = {}


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
