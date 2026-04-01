# Copyright 2025 Google LLC
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
import decimal

import pytest

from bigframes.functions import function_typing


def test_unsupported_type_error_init_with_dict():
    err = function_typing.UnsupportedTypeError(
        decimal.Decimal, {int: "INT64", float: "FLOAT64"}
    )

    message = str(err)

    assert "Decimal" in message
    assert "float, int" in message


def test_unsupported_type_error_init_with_set():
    err = function_typing.UnsupportedTypeError(decimal.Decimal, {int, float})

    message = str(err)

    assert "Decimal" in message
    assert "float, int" in message


def test_sdk_type_from_python_type_raises_unsupported_type_error():
    with pytest.raises(function_typing.UnsupportedTypeError) as excinfo:
        function_typing.sdk_type_from_python_type(datetime.datetime)

    message = str(excinfo.value)

    assert "datetime" in message
    assert "bool, bytes, float, int, str" in message
