# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading

import pytest

from google.cloud.ndb import utils


def test___all__():
    assert utils.__all__ == []


def test_code_info():
    with pytest.raises(NotImplementedError):
        utils.code_info()


def test_DEBUG():
    assert utils.DEBUG is True


def test_decorator():
    with pytest.raises(NotImplementedError):
        utils.decorator()


def test_frame_info():
    with pytest.raises(NotImplementedError):
        utils.frame_info()


def test_func_info():
    with pytest.raises(NotImplementedError):
        utils.func_info()


def test_gen_info():
    with pytest.raises(NotImplementedError):
        utils.gen_info()


def test_get_stack():
    with pytest.raises(NotImplementedError):
        utils.get_stack()


def test_logging_debug():
    with pytest.raises(NotImplementedError):
        utils.logging_debug()


def test_positional():
    @utils.positional(2)
    def test_func(a=1, b=2, **kwargs):
        return a, b

    @utils.positional(1)
    def test_func2(a=3, **kwargs):
        return a

    with pytest.raises(TypeError):
        test_func(1, 2, 3)

    with pytest.raises(TypeError):
        test_func2(1, 2)

    assert test_func(4, 5, x=0) == (4, 5)
    assert test_func(6) == (6, 2)

    assert test_func2(6) == 6


def test_keyword_only():
    @utils.keyword_only(foo=1, bar=2, baz=3)
    def test_kwonly(**kwargs):
        return kwargs["foo"], kwargs["bar"], kwargs["baz"]

    with pytest.raises(TypeError):
        test_kwonly(faz=4)

    assert test_kwonly() == (1, 2, 3)
    assert test_kwonly(foo=3, bar=5, baz=7) == (3, 5, 7)
    assert test_kwonly(baz=7) == (1, 2, 7)


def test_threading_local():
    assert utils.threading_local is threading.local


def test_tweak_logging():
    with pytest.raises(NotImplementedError):
        utils.tweak_logging()


def test_wrapping():
    with pytest.raises(NotImplementedError):
        utils.wrapping()
