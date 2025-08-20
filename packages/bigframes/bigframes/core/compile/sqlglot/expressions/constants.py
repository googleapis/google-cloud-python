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

import sqlglot.expressions as sge

_ZERO = sge.Cast(this=sge.convert(0), to="INT64")
_NAN = sge.Cast(this=sge.convert("NaN"), to="FLOAT64")
_INF = sge.Cast(this=sge.convert("Infinity"), to="FLOAT64")
_NEG_INF = sge.Cast(this=sge.convert("-Infinity"), to="FLOAT64")

# Approx Highest number you can pass in to EXP function and get a valid FLOAT64 result
# FLOAT64 has 11 exponent bits, so max values is about 2**(2**10)
# ln(2**(2**10)) == (2**10)*ln(2) ~= 709.78, so EXP(x) for x>709.78 will overflow.
_FLOAT64_EXP_BOUND = sge.convert(709.78)
