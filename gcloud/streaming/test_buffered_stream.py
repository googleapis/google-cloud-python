import unittest2


class Test_BufferedStream(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.streaming.buffered_stream import BufferedStream
        return BufferedStream

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_start_zero_longer_than_buffer(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._makeOne(stream, START, BUFSIZE)
        self.assertTrue(bufstream._stream is stream)
        self.assertEqual(bufstream._start_pos, START)
        self.assertEqual(bufstream._buffer_pos, 0)
        self.assertEqual(bufstream._buffered_data, CONTENT[:BUFSIZE])
        self.assertEqual(len(bufstream), BUFSIZE)
        self.assertFalse(bufstream.stream_exhausted)
        self.assertEqual(bufstream.stream_end_position, BUFSIZE)

    def test_ctor_start_nonzero_shorter_than_buffer(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = 8
        BUFSIZE = 10
        stream = BytesIO(CONTENT)
        stream.read(START)  # already consumed
        bufstream = self._makeOne(stream, START, BUFSIZE)
        self.assertTrue(bufstream._stream is stream)
        self.assertEqual(bufstream._start_pos, START)
        self.assertEqual(bufstream._buffer_pos, 0)
        self.assertEqual(bufstream._buffered_data, CONTENT[START:])
        self.assertEqual(len(bufstream), len(CONTENT) - START)
        self.assertTrue(bufstream.stream_exhausted)
        self.assertEqual(bufstream.stream_end_position, len(CONTENT))

    def test__bytes_remaining_start_zero_longer_than_buffer(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._makeOne(stream, START, BUFSIZE)
        self.assertEqual(bufstream._bytes_remaining, BUFSIZE)

    def test__bytes_remaining_start_zero_shorter_than_buffer(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = 8
        BUFSIZE = 10
        stream = BytesIO(CONTENT)
        stream.read(START)  # already consumed
        bufstream = self._makeOne(stream, START, BUFSIZE)
        self.assertEqual(bufstream._bytes_remaining, len(CONTENT) - START)

    def test_read_w_none(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._makeOne(stream, START, BUFSIZE)
        with self.assertRaises(ValueError):
            bufstream.read(None)

    def test_read_w_negative_size(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._makeOne(stream, START, BUFSIZE)
        with self.assertRaises(ValueError):
            bufstream.read(-2)

    def test_read_from_start(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._makeOne(stream, START, BUFSIZE)
        self.assertEqual(bufstream.read(4), CONTENT[:4])

    def test_read_exhausted(self):
        from io import BytesIO
        CONTENT = b'CONTENT GOES HERE'
        START = len(CONTENT)
        BUFSIZE = 10
        stream = BytesIO(CONTENT)
        stream.read(START)  # already consumed
        bufstream = self._makeOne(stream, START, BUFSIZE)
        self.assertTrue(bufstream.stream_exhausted)
        self.assertEqual(bufstream.stream_end_position, len(CONTENT))
        self.assertEqual(bufstream._bytes_remaining, 0)
        self.assertEqual(bufstream.read(10), b'')
