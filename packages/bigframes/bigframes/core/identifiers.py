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

# Later, plan on migrating ids to use integers to reduce memory usage allow use of bitmaps to represent column sets

from typing import Generator

ID_TYPE = str


def standard_identifiers() -> Generator[ID_TYPE, None, None]:
    i = 0
    while True:
        yield f"col_{i}"
        i = i + 1
