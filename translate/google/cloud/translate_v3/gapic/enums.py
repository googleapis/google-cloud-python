# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

"""Wrappers for protocol buffer enum types."""

import enum


class BatchTranslateMetadata(object):
    class State(enum.IntEnum):
        """
        State of the job.

        Attributes:
          STATE_UNSPECIFIED (int): Invalid.
          RUNNING (int): Request is being processed.
          SUCCEEDED (int): The batch is processed, and at least one item was successfully
          processed.
          FAILED (int): The batch is done and no item was successfully processed.
          CANCELLING (int): Request is in the process of being canceled after caller invoked
          longrunning.Operations.CancelOperation on the request id.
          CANCELLED (int): The batch is done after the user has called the
          longrunning.Operations.CancelOperation. Any records processed before the
          cancel command are output as specified in the request.
        """

        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLING = 4
        CANCELLED = 5


class CreateGlossaryMetadata(object):
    class State(enum.IntEnum):
        """
        Enumerates the possible states that the creation request can be in.

        Attributes:
          STATE_UNSPECIFIED (int): Invalid.
          RUNNING (int): Request is being processed.
          SUCCEEDED (int): The glossary was successfully created.
          FAILED (int): Failed to create the glossary.
          CANCELLING (int): Request is in the process of being canceled after caller invoked
          longrunning.Operations.CancelOperation on the request id.
          CANCELLED (int): The glossary creation request was successfully canceled.
        """

        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLING = 4
        CANCELLED = 5


class DeleteGlossaryMetadata(object):
    class State(enum.IntEnum):
        """
        Enumerates the possible states that the creation request can be in.

        Attributes:
          STATE_UNSPECIFIED (int): Invalid.
          RUNNING (int): Request is being processed.
          SUCCEEDED (int): The glossary was successfully deleted.
          FAILED (int): Failed to delete the glossary.
          CANCELLING (int): Request is in the process of being canceled after caller invoked
          longrunning.Operations.CancelOperation on the request id.
          CANCELLED (int): The glossary deletion request was successfully canceled.
        """

        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLING = 4
        CANCELLED = 5
