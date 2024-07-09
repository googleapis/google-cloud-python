# Copyright 2024 Google LLC All rights reserved.
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

"""Classes for iterating over stream results async for the Google Cloud
Firestore API.
"""

from collections import abc


class AsyncStreamGenerator(abc.AsyncGenerator):
    """Asynchronous generator for the streamed results."""

    def __init__(self, response_generator):
        self._generator = response_generator

    def __aiter__(self):
        return self._generator

    def __anext__(self):
        return self._generator.__anext__()

    def asend(self, value=None):
        return self._generator.asend(value)

    def athrow(self, exp=None):
        return self._generator.athrow(exp)

    def aclose(self):
        return self._generator.aclose()
