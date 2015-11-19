import unittest2


class Test_StreamSlice(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.streaming.stream_slice import StreamSlice
        return StreamSlice

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._makeOne(stream, MAXSIZE)
        self.assertTrue(stream_slice._stream is stream)
        self.assertEqual(stream_slice._remaining_bytes, MAXSIZE)
        self.assertEqual(stream_slice._max_bytes, MAXSIZE)
        self.assertEqual(len(stream_slice), MAXSIZE)
        self.assertEqual(stream_slice.length, MAXSIZE)

    def test___nonzero___empty(self):
        from io import BytesIO
        CONTENT = b''
        MAXSIZE = 0
        stream = BytesIO(CONTENT)
        stream_slice = self._makeOne(stream, MAXSIZE)
        self.assertFalse(stream_slice)

    def test___nonzero___nonempty(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._makeOne(stream, MAXSIZE)
        self.assertTrue(stream_slice)

    def test_read_exhausted(self):
        from io import BytesIO
        from six.moves import http_client
        CONTENT = b''
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._makeOne(stream, MAXSIZE)
        with self.assertRaises(http_client.IncompleteRead):
            stream_slice.read()

    def test_read_implicit_size(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._makeOne(stream, MAXSIZE)
        self.assertEqual(stream_slice.read(), CONTENT[:MAXSIZE])
        self.assertEqual(stream_slice._remaining_bytes, 0)

    def test_read_explicit_size(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        SIZE = 3
        stream = BytesIO(CONTENT)
        stream_slice = self._makeOne(stream, MAXSIZE)
        self.assertEqual(stream_slice.read(SIZE), CONTENT[:SIZE])
        self.assertEqual(stream_slice._remaining_bytes, MAXSIZE - SIZE)
