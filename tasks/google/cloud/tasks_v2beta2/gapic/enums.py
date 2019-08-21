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
    The HTTP method used to execute the task.

    Attributes:
      HTTP_METHOD_UNSPECIFIED (int): HTTP method unspecified
      POST (int): HTTP POST
      GET (int): HTTP GET
      HEAD (int): HTTP HEAD
      PUT (int): HTTP PUT
      DELETE (int): HTTP DELETE
    """

    HTTP_METHOD_UNSPECIFIED = 0
    POST = 1
    GET = 2
    HEAD = 3
    PUT = 4
    DELETE = 5


class Queue(object):
    class State(enum.IntEnum):
        """
        State of the queue.

        Attributes:
          STATE_UNSPECIFIED (int): Unspecified state.
          RUNNING (int): The queue is running. Tasks can be dispatched.

          If the queue was created using Cloud Tasks and the queue has had no
          activity (method calls or task dispatches) for 30 days, the queue may
          take a few minutes to re-activate. Some method calls may return
          ``NOT_FOUND`` and tasks may not be dispatched for a few minutes until
          the queue has been re-activated.
          PAUSED (int): Tasks are paused by the user. If the queue is paused then Cloud Tasks
          will stop delivering tasks from it, but more tasks can still be added to
          it by the user. When a pull queue is paused, all ``LeaseTasks`` calls
          will return a ``FAILED_PRECONDITION``.
          DISABLED (int): The queue is disabled.

          A queue becomes ``DISABLED`` when
          `queue.yaml <https://cloud.google.com/appengine/docs/python/config/queueref>`__
          or
          `queue.xml <https://cloud.google.com/appengine/docs/standard/java/config/queueref>`__
          is uploaded which does not contain the queue. You cannot directly
          disable a queue.

          When a queue is disabled, tasks can still be added to a queue but the
          tasks are not dispatched and ``LeaseTasks`` calls return a
          ``FAILED_PRECONDITION`` error.

          To permanently delete this queue and all of its tasks, call
          ``DeleteQueue``.
        """

        STATE_UNSPECIFIED = 0
        RUNNING = 1
        PAUSED = 2
        DISABLED = 3


class Task(object):
    class View(enum.IntEnum):
        """
        The view specifies a subset of ``Task`` data.

        When a task is returned in a response, not all information is retrieved
        by default because some data, such as payloads, might be desirable to
        return only when needed because of its large size or because of the
        sensitivity of data that it contains.

        Attributes:
          VIEW_UNSPECIFIED (int): Unspecified. Defaults to BASIC.
          BASIC (int): The basic view omits fields which can be large or can contain sensitive
          data.

          This view does not include the (``payload in AppEngineHttpRequest`` and
          ``payload in PullMessage``). These payloads are desirable to return only
          when needed, because they can be large and because of the sensitivity of
          the data that you choose to store in it.
          FULL (int): All information is returned.

          Authorization for ``FULL`` requires ``cloudtasks.tasks.fullView``
          `Google IAM <https://cloud.google.com/iam/>`__ permission on the
          ``Queue`` resource.
        """

        VIEW_UNSPECIFIED = 0
        BASIC = 1
        FULL = 2
