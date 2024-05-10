# Copyright 2023 Google LLC
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

"""
Utility functions for SQL construction.
"""

from typing import Iterable


def quote(value: str):
    """Return quoted input string."""

    # Let's use repr which also escapes any special characters
    #
    # >>> for val in [
    # ...     "123",
    # ...     "str with no special chars",
    # ...     "str with special chars.,'\"/\\"
    # ... ]:
    # ...     print(f"{val} -> {repr(val)}")
    # ...
    # 123 -> '123'
    # str with no special chars -> 'str with no special chars'
    # str with special chars.,'"/\ -> 'str with special chars.,\'"/\\'

    return repr(value)


def column_reference(column_name: str):
    """Return a string representing column reference in a SQL."""

    return f"`{column_name}`"


def cast_as_string(column_name: str):
    """Return a string representing string casting of a column."""

    return f"CAST({column_reference(column_name)} AS STRING)"


def csv(values: Iterable[str], quoted=False):
    """Return a string of comma separated values."""

    if quoted:
        values = [quote(val) for val in values]

    return ", ".join(values)
