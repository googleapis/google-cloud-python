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


class HttpMethod(enum.IntEnum):
    """
    The HTTP method used to execute the job.

    Attributes:
      HTTP_METHOD_UNSPECIFIED (int): HTTP method unspecified. Defaults to POST.
      POST (int): HTTP POST
      GET (int): HTTP GET
      HEAD (int): HTTP HEAD
      PUT (int): HTTP PUT
      DELETE (int): HTTP DELETE
      PATCH (int): HTTP PATCH
      OPTIONS (int): HTTP OPTIONS
    """

    HTTP_METHOD_UNSPECIFIED = 0
    POST = 1
    GET = 2
    HEAD = 3
    PUT = 4
    DELETE = 5
    PATCH = 6
    OPTIONS = 7


class Job(object):
    class State(enum.IntEnum):
        """
        State of the job.

        Attributes:
          STATE_UNSPECIFIED (int): Unspecified state.
          ENABLED (int): The job is executing normally.
          PAUSED (int): The job is paused by the user. It will not execute. A user can
          intentionally pause the job using ``PauseJobRequest``.
          DISABLED (int): The job is disabled by the system due to error. The user
          cannot directly set a job to be disabled.
          UPDATE_FAILED (int): The job state resulting from a failed ``CloudScheduler.UpdateJob``
          operation. To recover a job from this state, retry
          ``CloudScheduler.UpdateJob`` until a successful response is received.
        """

        STATE_UNSPECIFIED = 0
        ENABLED = 1
        PAUSED = 2
        DISABLED = 3
        UPDATE_FAILED = 4
