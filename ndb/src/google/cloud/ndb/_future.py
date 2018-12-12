# Copyright 2018 Google LLC
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

"""A Future class."""



class Future:
    """A future that waits on one or more gRPC futures.

    This class is meant to be subclassed with code to compute a result from the
    results of the wrapped gRPC futures. :method:`_compute_result` should be
    overriden to compute a result from the completed gRPC calls.
    """
    _NOT_COMPUTED = object()
    _result = _NOT_COMPUTED
    _complete = False

    def __init__(self, *grpc_futures):
        self._grpc_futures = grpc_futures

    def get_result(self):
        """Get the computed result for this future."""
        if self._result is Future._NOT_COMPUTED:
            self._result = self._compute_result(
                *[future.result() for future in self._grpc_futures])
        return self._result

    def _compute_result(self, *gprc_results):
        """Compute the result, given results from gRPC calls."""
        raise NotImplementedError(
            "Future._compute_result must be overridden by a subclass")
