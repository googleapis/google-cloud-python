# Copyright 2017, Google LLC
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

import pytest
import pytz

from google.api_core import datetime_helpers


ONE_MINUTE_IN_MICROSECONDS = 60 * 1e6


def test_utcnow():
    result = datetime_helpers.utcnow()
    assert isinstance(result, datetime.datetime)


def test_to_milliseconds():
    dt = datetime.datetime(1970, 1, 1, 0, 0, 1, tzinfo=pytz.utc)
    assert datetime_helpers.to_milliseconds(dt) == 1000


def test_to_microseconds():
    microseconds = 314159
    dt = datetime.datetime(
        1970, 1, 1, 0, 0, 0, microsecond=microseconds)
    assert datetime_helpers.to_microseconds(dt) == microseconds


def test_to_microseconds_non_utc():
    zone = pytz.FixedOffset(-1)
    dt = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=zone)
    assert datetime_helpers.to_microseconds(dt) == ONE_MINUTE_IN_MICROSECONDS


def test_to_microseconds_naive():
    microseconds = 314159
    dt = datetime.datetime(
        1970, 1, 1, 0, 0, 0, microsecond=microseconds, tzinfo=None)
    assert datetime_helpers.to_microseconds(dt) == microseconds


def test_from_microseconds():
    five_mins_from_epoch_in_microseconds = 5 * ONE_MINUTE_IN_MICROSECONDS
    five_mins_from_epoch_datetime = datetime.datetime(
        1970, 1, 1, 0, 5, 0, tzinfo=pytz.utc)

    result = datetime_helpers.from_microseconds(
        five_mins_from_epoch_in_microseconds)

    assert result == five_mins_from_epoch_datetime


def test_from_iso8601_date():
    today = datetime.date.today()
    iso_8601_today = today.strftime('%Y-%m-%d')

    assert datetime_helpers.from_iso8601_date(iso_8601_today) == today


def test_from_iso8601_time():
    assert (
        datetime_helpers.from_iso8601_time('12:09:42') ==
        datetime.time(12, 9, 42))


def test_from_rfc3339():
    value = '2009-12-17T12:44:32.123456Z'
    assert datetime_helpers.from_rfc3339(value) == datetime.datetime(
        2009, 12, 17, 12, 44, 32, 123456, pytz.utc)


def test_from_rfc3339_with_bad_tz():
    value = '2009-12-17T12:44:32.123456BAD'

    with pytest.raises(ValueError):
        datetime_helpers.from_rfc3339(value)


def test_from_rfc3339_with_nanos():
    value = '2009-12-17T12:44:32.123456789Z'

    with pytest.raises(ValueError):
        datetime_helpers.from_rfc3339(value)


def test_from_rfc3339_nanos_without_nanos():
    value = '2009-12-17T12:44:32Z'
    assert datetime_helpers.from_rfc3339_nanos(value) == datetime.datetime(
        2009, 12, 17, 12, 44, 32, 0, pytz.utc)


def test_from_rfc3339_nanos_with_bad_tz():
    value = '2009-12-17T12:44:32.123456789BAD'

    with pytest.raises(ValueError):
        datetime_helpers.from_rfc3339_nanos(value)


@pytest.mark.parametrize('truncated, micros', [
    ('12345678', 123456),
    ('1234567', 123456),
    ('123456', 123456),
    ('12345', 123450),
    ('1234', 123400),
    ('123', 123000),
    ('12', 120000),
    ('1', 100000)])
def test_from_rfc3339_nanos_with_truncated_nanos(truncated, micros):
    value = '2009-12-17T12:44:32.{}Z'.format(truncated)
    assert datetime_helpers.from_rfc3339_nanos(value) == datetime.datetime(
        2009, 12, 17, 12, 44, 32, micros, pytz.utc)


def test_to_rfc3339():
    value = datetime.datetime(2016, 4, 5, 13, 30, 0)
    expected = '2016-04-05T13:30:00.000000Z'
    assert datetime_helpers.to_rfc3339(value) == expected


def test_to_rfc3339_with_utc():
    value = datetime.datetime(2016, 4, 5, 13, 30, 0, tzinfo=pytz.utc)
    expected = '2016-04-05T13:30:00.000000Z'
    assert datetime_helpers.to_rfc3339(value, ignore_zone=False) == expected


def test_to_rfc3339_with_non_utc():
    zone = pytz.FixedOffset(-60)
    value = datetime.datetime(2016, 4, 5, 13, 30, 0, tzinfo=zone)
    expected = '2016-04-05T14:30:00.000000Z'
    assert datetime_helpers.to_rfc3339(value, ignore_zone=False) == expected


def test_to_rfc3339_with_non_utc_ignore_zone():
    zone = pytz.FixedOffset(-60)
    value = datetime.datetime(2016, 4, 5, 13, 30, 0, tzinfo=zone)
    expected = '2016-04-05T13:30:00.000000Z'
    assert datetime_helpers.to_rfc3339(value, ignore_zone=True) == expected


def test_datetimewithnanos_ctor_wo_nanos():
    stamp = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47, 123456)
    assert stamp.year == 2016
    assert stamp.month == 12
    assert stamp.day == 20
    assert stamp.hour == 21
    assert stamp.minute == 13
    assert stamp.second == 47
    assert stamp.microsecond == 123456
    assert stamp.nanosecond == 0


def test_datetimewithnanos_ctor_w_nanos():
    stamp = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47, nanosecond=123456789)
    assert stamp.year == 2016
    assert stamp.month == 12
    assert stamp.day == 20
    assert stamp.hour == 21
    assert stamp.minute == 13
    assert stamp.second == 47
    assert stamp.microsecond == 123456
    assert stamp.nanosecond == 123456789


def test_datetimewithnanos_ctor_w_micros_positional_and_nanos():
    with pytest.raises(TypeError):
        datetime_helpers.DatetimeWithNanoseconds(
            2016, 12, 20, 21, 13, 47, 123456, nanosecond=123456789)


def test_datetimewithnanos_ctor_w_micros_keyword_and_nanos():
    with pytest.raises(TypeError):
        datetime_helpers.DatetimeWithNanoseconds(
            2016, 12, 20, 21, 13, 47,
            microsecond=123456, nanosecond=123456789)


def test_datetimewithnanos_rfc339_wo_nanos():
    stamp = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47, 123456)
    assert stamp.rfc3339() == '2016-12-20T21:13:47.123456Z'


def test_datetimewithnanos_rfc339_w_nanos():
    stamp = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47, nanosecond=123456789)
    assert stamp.rfc3339() == '2016-12-20T21:13:47.123456789Z'


def test_datetimewithnanos_rfc339_w_nanos_no_trailing_zeroes():
    stamp = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47, nanosecond=100000000)
    assert stamp.rfc3339() == '2016-12-20T21:13:47.1Z'


def test_datetimewithnanos_from_rfc3339_w_invalid():
    stamp = '2016-12-20T21:13:47'
    with pytest.raises(ValueError):
        datetime_helpers.DatetimeWithNanoseconds.from_rfc3339(stamp)


def test_datetimewithnanos_from_rfc3339_wo_fraction():
    timestamp = '2016-12-20T21:13:47Z'
    expected = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47,
        tzinfo=pytz.UTC)
    stamp = datetime_helpers.DatetimeWithNanoseconds.from_rfc3339(timestamp)
    assert (stamp == expected)


def test_datetimewithnanos_from_rfc3339_w_partial_precision():
    timestamp = '2016-12-20T21:13:47.1Z'
    expected = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47,
        microsecond=100000,
        tzinfo=pytz.UTC)
    stamp = datetime_helpers.DatetimeWithNanoseconds.from_rfc3339(timestamp)
    assert stamp == expected


def test_datetimewithnanos_from_rfc3339_w_full_precision():
    timestamp = '2016-12-20T21:13:47.123456789Z'
    expected = datetime_helpers.DatetimeWithNanoseconds(
        2016, 12, 20, 21, 13, 47,
        nanosecond=123456789,
        tzinfo=pytz.UTC)
    stamp = datetime_helpers.DatetimeWithNanoseconds.from_rfc3339(timestamp)
    assert stamp == expected
