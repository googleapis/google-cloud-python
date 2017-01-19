# Copyright 2016 Google Inc.
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


class Test_BufferedStream(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.streaming.buffered_stream import BufferedStream

        return BufferedStream

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_closed_stream(self):
        class _Stream(object):
            closed = True

        start = 0
        bufsize = 4
        bufstream = self._make_one(_Stream, start, bufsize)
        self.assertIs(bufstream._stream, _Stream)
        self.assertEqual(bufstream._start_pos, start)
        self.assertEqual(bufstream._buffer_pos, 0)
        self.assertEqual(bufstream._buffered_data, b'')
        self.assertTrue(bufstream._stream_at_end)
        self.assertEqual(bufstream._end_pos, 0)

    def test_ctor_start_zero_longer_than_buffer(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._make_one(stream, START, BUFSIZE)
        self.assertIs(bufstream._stream, stream)
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
        bufstream = self._make_one(stream, START, BUFSIZE)
        self.assertIs(bufstream._stream, stream)
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
        bufstream = self._make_one(stream, START, BUFSIZE)
        self.assertEqual(bufstream._bytes_remaining, BUFSIZE)

    def test__bytes_remaining_start_zero_shorter_than_buffer(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        START = 8
        BUFSIZE = 10
        stream = BytesIO(CONTENT)
        stream.read(START)  # already consumed
        bufstream = self._make_one(stream, START, BUFSIZE)
        self.assertEqual(bufstream._bytes_remaining, len(CONTENT) - START)

    def test_read_w_none(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._make_one(stream, START, BUFSIZE)
        with self.assertRaises(ValueError):
            bufstream.read(None)

    def test_read_w_negative_size(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._make_one(stream, START, BUFSIZE)
        with self.assertRaises(ValueError):
            bufstream.read(-2)

    def test_read_from_start(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        START = 0
        BUFSIZE = 4
        stream = BytesIO(CONTENT)
        bufstream = self._make_one(stream, START, BUFSIZE)
        self.assertEqual(bufstream.read(4), CONTENT[:4])

    def test_read_exhausted(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        START = len(CONTENT)
        BUFSIZE = 10
        stream = BytesIO(CONTENT)
        stream.read(START)  # already consumed
        bufstream = self._make_one(stream, START, BUFSIZE)
        self.assertTrue(bufstream.stream_exhausted)
        self.assertEqual(bufstream.stream_end_position, len(CONTENT))
        self.assertEqual(bufstream._bytes_remaining, 0)
        self.assertEqual(bufstream.read(10), b'')
