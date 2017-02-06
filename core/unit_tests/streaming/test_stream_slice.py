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


class Test_StreamSlice(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.streaming.stream_slice import StreamSlice

        return StreamSlice

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._make_one(stream, MAXSIZE)
        self.assertIs(stream_slice._stream, stream)
        self.assertEqual(stream_slice._remaining_bytes, MAXSIZE)
        self.assertEqual(stream_slice._max_bytes, MAXSIZE)
        self.assertEqual(len(stream_slice), MAXSIZE)
        self.assertEqual(stream_slice.length, MAXSIZE)

    def test___nonzero___empty(self):
        from io import BytesIO

        CONTENT = b''
        MAXSIZE = 0
        stream = BytesIO(CONTENT)
        stream_slice = self._make_one(stream, MAXSIZE)
        self.assertFalse(stream_slice)

    def test___nonzero___nonempty(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._make_one(stream, MAXSIZE)
        self.assertTrue(stream_slice)

    def test_read_exhausted(self):
        from io import BytesIO
        from six.moves import http_client

        CONTENT = b''
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._make_one(stream, MAXSIZE)
        with self.assertRaises(http_client.IncompleteRead):
            stream_slice.read()

    def test_read_implicit_size(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        stream = BytesIO(CONTENT)
        stream_slice = self._make_one(stream, MAXSIZE)
        self.assertEqual(stream_slice.read(), CONTENT[:MAXSIZE])
        self.assertEqual(stream_slice._remaining_bytes, 0)

    def test_read_explicit_size(self):
        from io import BytesIO

        CONTENT = b'CONTENT GOES HERE'
        MAXSIZE = 4
        SIZE = 3
        stream = BytesIO(CONTENT)
        stream_slice = self._make_one(stream, MAXSIZE)
        self.assertEqual(stream_slice.read(SIZE), CONTENT[:SIZE])
        self.assertEqual(stream_slice._remaining_bytes, MAXSIZE - SIZE)
