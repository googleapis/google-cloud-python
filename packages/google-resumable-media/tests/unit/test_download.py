# Copyright 2017 Google Inc.
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

import pytest


def get_download_class():
    from gooresmed import download

    return download.Download


def make_download(*args, **kwargs):
    klass = get_download_class()
    return klass(*args, **kwargs)


def test_constructor():
    with pytest.raises(NotImplementedError):
        make_download()


def test_consume():
    klass = get_download_class()
    with pytest.raises(NotImplementedError):
        klass.consume(None)
