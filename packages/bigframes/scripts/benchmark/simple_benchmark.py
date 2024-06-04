# Copyright 2024 Google LLC
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

import bigframes.pandas as bpd

# This is a placeholder benchmark.
# TODO(340278185): Add more data analysis tasks and benchmark files
# like this one.

print("Performing simple benchmark.")
df = bpd.DataFrame()
df["column_1"] = bpd.Series([i for i in range(100000)])
df["column_2"] = bpd.Series([i * 2 for i in range(100000)])
df["column_3"] = df["column_1"] + df["column_2"]
df.__repr__()
bpd.reset_session()
