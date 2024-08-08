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
#

import pytest
import grpc
from google.api_core import exceptions as core_exceptions
import google.cloud.bigtable.data._helpers as _helpers
from google.cloud.bigtable.data._helpers import TABLE_DEFAULT

import mock


class TestMakeMetadata:
    @pytest.mark.parametrize(
        "table,profile,instance,expected",
        [
            ("table", "profile", None, "table_name=table&app_profile_id=profile"),
            ("table", None, None, "table_name=table"),
            (None, None, "instance", "name=instance"),
            (None, "profile", None, "app_profile_id=profile"),
            (None, "profile", "instance", "name=instance&app_profile_id=profile"),
        ],
    )
    def test__make_metadata(self, table, profile, instance, expected):
        metadata = _helpers._make_metadata(table, profile, instance)
        assert metadata == [("x-goog-request-params", expected)]

    @pytest.mark.parametrize(
        "table,profile,instance",
        [
            ("table", None, "instance"),
            ("table", "profile", "instance"),
            (None, None, None),
        ],
    )
    def test__make_metadata_invalid_params(self, table, profile, instance):
        with pytest.raises(ValueError):
            _helpers._make_metadata(table, profile, instance)


class TestAttemptTimeoutGenerator:
    @pytest.mark.parametrize(
        "request_t,operation_t,expected_list",
        [
            (1, 3.5, [1, 1, 1, 0.5, 0, 0]),
            (None, 3.5, [3.5, 2.5, 1.5, 0.5, 0, 0]),
            (10, 5, [5, 4, 3, 2, 1, 0, 0]),
            (3, 3, [3, 2, 1, 0, 0, 0, 0]),
            (0, 3, [0, 0, 0]),
            (3, 0, [0, 0, 0]),
            (-1, 3, [0, 0, 0]),
            (3, -1, [0, 0, 0]),
        ],
    )
    def test_attempt_timeout_generator(self, request_t, operation_t, expected_list):
        """
        test different values for timeouts. Clock is incremented by 1 second for each item in expected_list
        """
        timestamp_start = 123
        with mock.patch("time.monotonic") as mock_monotonic:
            mock_monotonic.return_value = timestamp_start
            generator = _helpers._attempt_timeout_generator(request_t, operation_t)
            for val in expected_list:
                mock_monotonic.return_value += 1
                assert next(generator) == val

    @pytest.mark.parametrize(
        "request_t,operation_t,expected",
        [
            (1, 3.5, 1),
            (None, 3.5, 3.5),
            (10, 5, 5),
            (5, 10, 5),
            (3, 3, 3),
            (0, 3, 0),
            (3, 0, 0),
            (-1, 3, 0),
            (3, -1, 0),
        ],
    )
    def test_attempt_timeout_frozen_time(self, request_t, operation_t, expected):
        """test with time.monotonic frozen"""
        timestamp_start = 123
        with mock.patch("time.monotonic") as mock_monotonic:
            mock_monotonic.return_value = timestamp_start
            generator = _helpers._attempt_timeout_generator(request_t, operation_t)
            assert next(generator) == expected
            # value should not change without time.monotonic changing
            assert next(generator) == expected

    def test_attempt_timeout_w_sleeps(self):
        """use real sleep values to make sure it matches expectations"""
        from time import sleep

        operation_timeout = 1
        generator = _helpers._attempt_timeout_generator(None, operation_timeout)
        expected_value = operation_timeout
        sleep_time = 0.1
        for i in range(3):
            found_value = next(generator)
            assert abs(found_value - expected_value) < 0.001
            sleep(sleep_time)
            expected_value -= sleep_time


class TestValidateTimeouts:
    def test_validate_timeouts_error_messages(self):
        with pytest.raises(ValueError) as e:
            _helpers._validate_timeouts(operation_timeout=1, attempt_timeout=-1)
        assert "attempt_timeout must be greater than 0" in str(e.value)
        with pytest.raises(ValueError) as e:
            _helpers._validate_timeouts(operation_timeout=-1, attempt_timeout=1)
        assert "operation_timeout must be greater than 0" in str(e.value)

    @pytest.mark.parametrize(
        "args,expected",
        [
            ([1, None, False], False),
            ([1, None, True], True),
            ([1, 1, False], True),
            ([1, 1, True], True),
            ([1, 1], True),
            ([1, None], False),
            ([2, 1], True),
            ([0, 1], False),
            ([1, 0], False),
            ([60, None], False),
            ([600, None], False),
            ([600, 600], True),
        ],
    )
    def test_validate_with_inputs(self, args, expected):
        """
        test whether an exception is thrown with different inputs
        """
        success = False
        try:
            _helpers._validate_timeouts(*args)
            success = True
        except ValueError:
            pass
        assert success == expected


class TestGetTimeouts:
    @pytest.mark.parametrize(
        "input_times,input_table,expected",
        [
            ((2, 1), {}, (2, 1)),
            ((2, 4), {}, (2, 2)),
            ((2, None), {}, (2, 2)),
            (
                (TABLE_DEFAULT.DEFAULT, TABLE_DEFAULT.DEFAULT),
                {"operation": 3, "attempt": 2},
                (3, 2),
            ),
            (
                (TABLE_DEFAULT.READ_ROWS, TABLE_DEFAULT.READ_ROWS),
                {"read_rows_operation": 3, "read_rows_attempt": 2},
                (3, 2),
            ),
            (
                (TABLE_DEFAULT.MUTATE_ROWS, TABLE_DEFAULT.MUTATE_ROWS),
                {"mutate_rows_operation": 3, "mutate_rows_attempt": 2},
                (3, 2),
            ),
            ((10, TABLE_DEFAULT.DEFAULT), {"attempt": None}, (10, 10)),
            ((10, TABLE_DEFAULT.DEFAULT), {"attempt": 5}, (10, 5)),
            ((10, TABLE_DEFAULT.DEFAULT), {"attempt": 100}, (10, 10)),
            ((TABLE_DEFAULT.DEFAULT, 10), {"operation": 12}, (12, 10)),
            ((TABLE_DEFAULT.DEFAULT, 10), {"operation": 3}, (3, 3)),
        ],
    )
    def test_get_timeouts(self, input_times, input_table, expected):
        """
        test input/output mappings for a variety of valid inputs
        """
        fake_table = mock.Mock()
        for key in input_table.keys():
            # set the default fields in our fake table mock
            setattr(fake_table, f"default_{key}_timeout", input_table[key])
        t1, t2 = _helpers._get_timeouts(input_times[0], input_times[1], fake_table)
        assert t1 == expected[0]
        assert t2 == expected[1]

    @pytest.mark.parametrize(
        "input_times,input_table",
        [
            ([0, 1], {}),
            ([1, 0], {}),
            ([None, 1], {}),
            ([TABLE_DEFAULT.DEFAULT, 1], {"operation": None}),
            ([TABLE_DEFAULT.DEFAULT, 1], {"operation": 0}),
            ([1, TABLE_DEFAULT.DEFAULT], {"attempt": 0}),
        ],
    )
    def test_get_timeouts_invalid(self, input_times, input_table):
        """
        test with inputs that should raise error during validation step
        """
        fake_table = mock.Mock()
        for key in input_table.keys():
            # set the default fields in our fake table mock
            setattr(fake_table, f"default_{key}_timeout", input_table[key])
        with pytest.raises(ValueError):
            _helpers._get_timeouts(input_times[0], input_times[1], fake_table)


class TestGetRetryableErrors:
    @pytest.mark.parametrize(
        "input_codes,input_table,expected",
        [
            ((), {}, []),
            ((Exception,), {}, [Exception]),
            (TABLE_DEFAULT.DEFAULT, {"default": [Exception]}, [Exception]),
            (
                TABLE_DEFAULT.READ_ROWS,
                {"default_read_rows": (RuntimeError, ValueError)},
                [RuntimeError, ValueError],
            ),
            (
                TABLE_DEFAULT.MUTATE_ROWS,
                {"default_mutate_rows": (ValueError,)},
                [ValueError],
            ),
            ((4,), {}, [core_exceptions.DeadlineExceeded]),
            (
                [grpc.StatusCode.DEADLINE_EXCEEDED],
                {},
                [core_exceptions.DeadlineExceeded],
            ),
            (
                (14, grpc.StatusCode.ABORTED, RuntimeError),
                {},
                [
                    core_exceptions.ServiceUnavailable,
                    core_exceptions.Aborted,
                    RuntimeError,
                ],
            ),
        ],
    )
    def test_get_retryable_errors(self, input_codes, input_table, expected):
        """
        test input/output mappings for a variety of valid inputs
        """
        fake_table = mock.Mock()
        for key in input_table.keys():
            # set the default fields in our fake table mock
            setattr(fake_table, f"{key}_retryable_errors", input_table[key])
        result = _helpers._get_retryable_errors(input_codes, fake_table)
        assert result == expected
