# Copyright 2021 Google LLC
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

import datetime
import logging
import random
import time
from typing import List
from unittest.mock import patch

import proto
import pytest
import requests

from google.api_core import rest_streaming
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2


__protobuf__ = proto.module(package=__name__)
SEED = int(time.time())
logging.info(f"Starting rest streaming tests with random seed: {SEED}")
random.seed(SEED)


class Genre(proto.Enum):
    GENRE_UNSPECIFIED = 0
    CLASSICAL = 1
    JAZZ = 2
    ROCK = 3


class Composer(proto.Message):
    given_name = proto.Field(proto.STRING, number=1)
    family_name = proto.Field(proto.STRING, number=2)
    relateds = proto.RepeatedField(proto.STRING, number=3)
    indices = proto.MapField(proto.STRING, proto.STRING, number=4)


class Song(proto.Message):
    composer = proto.Field(Composer, number=1)
    title = proto.Field(proto.STRING, number=2)
    lyrics = proto.Field(proto.STRING, number=3)
    year = proto.Field(proto.INT32, number=4)
    genre = proto.Field(Genre, number=5)
    is_five_mins_longer = proto.Field(proto.BOOL, number=6)
    score = proto.Field(proto.DOUBLE, number=7)
    likes = proto.Field(proto.INT64, number=8)
    duration = proto.Field(duration_pb2.Duration, number=9)
    date_added = proto.Field(timestamp_pb2.Timestamp, number=10)


class EchoResponse(proto.Message):
    content = proto.Field(proto.STRING, number=1)


class ResponseMock(requests.Response):
    class _ResponseItr:
        def __init__(self, _response_bytes: bytes, random_split=False):
            self._responses_bytes = _response_bytes
            self._i = 0
            self._random_split = random_split

        def __next__(self):
            if self._i == len(self._responses_bytes):
                raise StopIteration
            if self._random_split:
                n = random.randint(1, len(self._responses_bytes[self._i :]))
            else:
                n = 1
            x = self._responses_bytes[self._i : self._i + n]
            self._i += n
            return x.decode("utf-8")

    def __init__(
        self,
        responses: List[proto.Message],
        response_cls,
        random_split=False,
    ):
        super().__init__()
        self._responses = responses
        self._random_split = random_split
        self._response_message_cls = response_cls

    def _parse_responses(self, responses: List[proto.Message]) -> bytes:
        # json.dumps returns a string surrounded with quotes that need to be stripped
        # in order to be an actual JSON.
        json_responses = [
            self._response_message_cls.to_json(r).strip('"') for r in responses
        ]
        logging.info(f"Sending JSON stream: {json_responses}")
        ret_val = "[{}]".format(",".join(json_responses))
        return bytes(ret_val, "utf-8")

    def close(self):
        raise NotImplementedError()

    def iter_content(self, *args, **kwargs):
        return self._ResponseItr(
            self._parse_responses(self._responses),
            random_split=self._random_split,
        )


@pytest.mark.parametrize("random_split", [False])
def test_next_simple(random_split):
    responses = [EchoResponse(content="hello world"), EchoResponse(content="yes")]
    resp = ResponseMock(
        responses=responses, random_split=random_split, response_cls=EchoResponse
    )
    itr = rest_streaming.ResponseIterator(resp, EchoResponse)
    assert list(itr) == responses


@pytest.mark.parametrize("random_split", [True, False])
def test_next_nested(random_split):
    responses = [
        Song(title="some song", composer=Composer(given_name="some name")),
        Song(title="another song", date_added=datetime.datetime(2021, 12, 17)),
    ]
    resp = ResponseMock(
        responses=responses, random_split=random_split, response_cls=Song
    )
    itr = rest_streaming.ResponseIterator(resp, Song)
    assert list(itr) == responses


@pytest.mark.parametrize("random_split", [True, False])
def test_next_stress(random_split):
    n = 50
    responses = [
        Song(title="title_%d" % i, composer=Composer(given_name="name_%d" % i))
        for i in range(n)
    ]
    resp = ResponseMock(
        responses=responses, random_split=random_split, response_cls=Song
    )
    itr = rest_streaming.ResponseIterator(resp, Song)
    assert list(itr) == responses


@pytest.mark.parametrize("random_split", [True, False])
def test_next_escaped_characters_in_string(random_split):
    composer_with_relateds = Composer()
    relateds = ["Artist A", "Artist B"]
    composer_with_relateds.relateds = relateds

    responses = [
        Song(title='ti"tle\nfoo\tbar{}', composer=Composer(given_name="name\n\n\n")),
        Song(
            title='{"this is weird": "totally"}', composer=Composer(given_name="\\{}\\")
        ),
        Song(title='\\{"key": ["value",]}\\', composer=composer_with_relateds),
    ]
    resp = ResponseMock(
        responses=responses, random_split=random_split, response_cls=Song
    )
    itr = rest_streaming.ResponseIterator(resp, Song)
    assert list(itr) == responses


def test_next_not_array():
    with patch.object(
        ResponseMock, "iter_content", return_value=iter('{"hello": 0}')
    ) as mock_method:

        resp = ResponseMock(responses=[], response_cls=EchoResponse)
        itr = rest_streaming.ResponseIterator(resp, EchoResponse)
        with pytest.raises(ValueError):
            next(itr)
        mock_method.assert_called_once()


def test_cancel():
    with patch.object(ResponseMock, "close", return_value=None) as mock_method:
        resp = ResponseMock(responses=[], response_cls=EchoResponse)
        itr = rest_streaming.ResponseIterator(resp, EchoResponse)
        itr.cancel()
        mock_method.assert_called_once()


def test_check_buffer():
    with patch.object(
        ResponseMock,
        "_parse_responses",
        return_value=bytes('[{"content": "hello"}, {', "utf-8"),
    ):
        resp = ResponseMock(responses=[], response_cls=EchoResponse)
        itr = rest_streaming.ResponseIterator(resp, EchoResponse)
        with pytest.raises(ValueError):
            next(itr)
            next(itr)


def test_next_html():
    with patch.object(
        ResponseMock, "iter_content", return_value=iter("<!DOCTYPE html><html></html>")
    ) as mock_method:

        resp = ResponseMock(responses=[], response_cls=EchoResponse)
        itr = rest_streaming.ResponseIterator(resp, EchoResponse)
        with pytest.raises(ValueError):
            next(itr)
        mock_method.assert_called_once()
