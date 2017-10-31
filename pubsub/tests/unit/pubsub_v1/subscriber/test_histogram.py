# Copyright 2017, Google LLC All rights reserved.
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

from google.cloud.pubsub_v1.subscriber import _histogram


def test_init():
    data = {}
    histo = _histogram.Histogram(data=data)
    assert histo._data is data
    assert len(histo) == 0


def test_contains():
    histo = _histogram.Histogram()
    histo.add(10)
    histo.add(20)
    assert 10 in histo
    assert 20 in histo
    assert 30 not in histo


def test_max():
    histo = _histogram.Histogram()
    assert histo.max == 600
    histo.add(120)
    assert histo.max == 120
    histo.add(150)
    assert histo.max == 150
    histo.add(20)
    assert histo.max == 150


def test_min():
    histo = _histogram.Histogram()
    assert histo.min == 10
    histo.add(60)
    assert histo.min == 60
    histo.add(30)
    assert histo.min == 30
    histo.add(120)
    assert histo.min == 30


def test_add():
    histo = _histogram.Histogram()
    histo.add(60)
    assert histo._data[60] == 1
    histo.add(60)
    assert histo._data[60] == 2


def test_add_lower_limit():
    histo = _histogram.Histogram()
    histo.add(5)
    assert 5 not in histo
    assert 10 in histo


def test_add_upper_limit():
    histo = _histogram.Histogram()
    histo.add(12000)
    assert 12000 not in histo
    assert 600 in histo


def test_percentile():
    histo = _histogram.Histogram()
    [histo.add(i) for i in range(101, 201)]
    assert histo.percentile(100) == 200
    assert histo.percentile(101) == 200
    assert histo.percentile(99) == 199
    assert histo.percentile(1) == 101
