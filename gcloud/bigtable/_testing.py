# Copyright 2015 Google Inc. All rights reserved.
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

"""Mocks used to emulate gRPC generated objects."""


class _FakeStub(object):
    """Acts as a gPRC stub."""

    def __init__(self, *results):
        self.results = results
        self.method_calls = []
        self._entered = 0
        self._exited = []

    def __enter__(self):
        self._entered += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exited.append((exc_type, exc_val, exc_tb))
        return True

    def __getattr__(self, name):
        # We need not worry about attributes set in constructor
        # since __getattribute__ will handle them.
        return _MethodMock(name, self)


class _MethodMock(object):
    """Mock for API method attached to a gRPC stub.

    In the beta implementation, these are of type.
    :class:`grpc.framework.crust.implementations._UnaryUnaryMultiCallable`
    """

    def __init__(self, name, factory):
        self._name = name
        self._factory = factory

    def __call__(self, *args, **kwargs):
        """Sync method meant to mock a gRPC stub request."""
        self._factory.method_calls.append((self._name, args, kwargs))
        curr_result, self._factory.results = (self._factory.results[0],
                                              self._factory.results[1:])
        return curr_result
