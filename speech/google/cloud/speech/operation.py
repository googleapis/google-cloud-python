# Copyright 2016 Google LLC
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

"""Long running operation representation for Google Speech API"""

from google.cloud.proto.speech.v1 import cloud_speech_pb2

from google.cloud import operation
from google.cloud.speech.result import Result


operation.register_type(cloud_speech_pb2.LongRunningRecognizeMetadata)
operation.register_type(cloud_speech_pb2.LongRunningRecognizeResponse)


class Operation(operation.Operation):
    """Custom Long-Running Operation for Google Speech API.

    :type name: str
    :param name: The fully-qualified path naming the operation.

    :type client: :class:`~google.cloud.speech.client.Client`
    :param client: Client that created the current operation.

    :type caller_metadata: dict
    :param caller_metadata: caller-assigned metadata about the operation
    """

    results = None
    """List of transcriptions from the speech-to-text process."""

    def _update_state(self, operation_pb):
        """Update the state of the current object based on operation.

        This mostly does what the base class does, but all populates
        results.

        :type operation_pb:
            :class:`~google.longrunning.operations_pb2.Operation`
        :param operation_pb: Protobuf to be parsed.

        :raises ValueError: If there are no ``results`` from the operation.
        """
        super(Operation, self)._update_state(operation_pb)

        result_type = operation_pb.WhichOneof('result')
        if result_type != 'response':
            return

        # Retrieve the results.
        # If there were no results at all, raise an exception.
        pb_results = self.response.results
        if len(pb_results) == 0:
            raise ValueError('Speech API returned no results.')

        # Save the results to the Operation object.
        self.results = []
        for pb_result in pb_results:
            self.results.append(Result.from_pb(pb_result))
