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

from __future__ import annotations

import bigframes_vendored.sqlglot.expressions as sge


def round_towards_zero(expr: sge.Expression):
    """
    Round a float value to to an integer, always rounding towards zero.

    This is used to handle duration/timedelta emulation mostly.
    """
    return sge.Cast(
        this=sge.If(
            this=sge.GT(this=expr, expression=sge.convert(0)),
            true=sge.Floor(this=expr),
            false=sge.Ceil(this=expr),
        ),
        to="INT64",
    )
