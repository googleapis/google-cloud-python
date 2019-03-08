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


class ClusterOperationStatus(object):
    class State(enum.IntEnum):
        """
        The operation state.

        Attributes:
          UNKNOWN (int): Unused.
          PENDING (int): The operation has been created.
          RUNNING (int): The operation is running.
          DONE (int): The operation is done; either cancelled or completed.
        """

        UNKNOWN = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3


class ClusterStatus(object):
    class State(enum.IntEnum):
        """
        The cluster state.

        Attributes:
          UNKNOWN (int): The cluster state is unknown.
          CREATING (int): The cluster is being created and set up. It is not ready for use.
          RUNNING (int): The cluster is currently running and healthy. It is ready for use.
          ERROR (int): The cluster encountered an error. It is not ready for use.
          DELETING (int): The cluster is being deleted. It cannot be used.
          UPDATING (int): The cluster is being updated. It continues to accept and process jobs.
        """

        UNKNOWN = 0
        CREATING = 1
        RUNNING = 2
        ERROR = 3
        DELETING = 4
        UPDATING = 5

    class Substate(enum.IntEnum):
        """
        The cluster substate.

        Attributes:
          UNSPECIFIED (int): The cluster substate is unknown.
          UNHEALTHY (int): The cluster is known to be in an unhealthy state
          (for example, critical daemons are not running or HDFS capacity is
          exhausted).

          Applies to RUNNING state.
          STALE_STATUS (int): The agent-reported status is out of date (may occur if
          Cloud Dataproc loses communication with Agent).

          Applies to RUNNING state.
        """

        UNSPECIFIED = 0
        UNHEALTHY = 1
        STALE_STATUS = 2


class JobStatus(object):
    class State(enum.IntEnum):
        """
        The job state.

        Attributes:
          STATE_UNSPECIFIED (int): The job state is unknown.
          PENDING (int): The job is pending; it has been submitted, but is not yet running.
          SETUP_DONE (int): Job has been received by the service and completed initial setup;
          it will soon be submitted to the cluster.
          RUNNING (int): The job is running on the cluster.
          CANCEL_PENDING (int): A CancelJob request has been received, but is pending.
          CANCEL_STARTED (int): Transient in-flight resources have been canceled, and the request to
          cancel the running job has been issued to the cluster.
          CANCELLED (int): The job cancellation was successful.
          DONE (int): The job has completed successfully.
          ERROR (int): The job has completed, but encountered an error.
          ATTEMPT_FAILURE (int): Job attempt has failed. The detail field contains failure details for
          this attempt.

          Applies to restartable jobs only.
        """

        STATE_UNSPECIFIED = 0
        PENDING = 1
        SETUP_DONE = 8
        RUNNING = 2
        CANCEL_PENDING = 3
        CANCEL_STARTED = 7
        CANCELLED = 4
        DONE = 5
        ERROR = 6
        ATTEMPT_FAILURE = 9

    class Substate(enum.IntEnum):
        """
        The job substate.

        Attributes:
          UNSPECIFIED (int): The job substate is unknown.
          SUBMITTED (int): The Job is submitted to the agent.

          Applies to RUNNING state.
          QUEUED (int): The Job has been received and is awaiting execution (it may be waiting
          for a condition to be met). See the "details" field for the reason for
          the delay.

          Applies to RUNNING state.
          STALE_STATUS (int): The agent-reported status is out of date, which may be caused by a
          loss of communication between the agent and Cloud Dataproc. If the
          agent does not send a timely update, the job will fail.

          Applies to RUNNING state.
        """

        UNSPECIFIED = 0
        SUBMITTED = 1
        QUEUED = 2
        STALE_STATUS = 3


class ListJobsRequest(object):
    class JobStateMatcher(enum.IntEnum):
        """
        A matcher that specifies categories of job states.

        Attributes:
          ALL (int): Match all jobs, regardless of state.
          ACTIVE (int): Only match jobs in non-terminal states: PENDING, RUNNING, or
          CANCEL\_PENDING.
          NON_ACTIVE (int): Only match jobs in terminal states: CANCELLED, DONE, or ERROR.
        """

        ALL = 0
        ACTIVE = 1
        NON_ACTIVE = 2


class LoggingConfig(object):
    class Level(enum.IntEnum):
        """
        The Log4j level for job execution. When running an `Apache
        Hive <http://hive.apache.org/>`__ job, Cloud Dataproc configures the
        Hive client to an equivalent verbosity level.

        Attributes:
          LEVEL_UNSPECIFIED (int): Level is unspecified. Use default level for log4j.
          ALL (int): Use ALL level for log4j.
          TRACE (int): Use TRACE level for log4j.
          DEBUG (int): Use DEBUG level for log4j.
          INFO (int): Use INFO level for log4j.
          WARN (int): Use WARN level for log4j.
          ERROR (int): Use ERROR level for log4j.
          FATAL (int): Use FATAL level for log4j.
          OFF (int): Turn off log4j.
        """

        LEVEL_UNSPECIFIED = 0
        ALL = 1
        TRACE = 2
        DEBUG = 3
        INFO = 4
        WARN = 5
        ERROR = 6
        FATAL = 7
        OFF = 8


class WorkflowMetadata(object):
    class State(enum.IntEnum):
        """
        The operation state.

        Attributes:
          UNKNOWN (int): Unused.
          PENDING (int): The operation has been created.
          RUNNING (int): The operation is running.
          DONE (int): The operation is done; either cancelled or completed.
        """

        UNKNOWN = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3


class WorkflowNode(object):
    class NodeState(enum.IntEnum):
        """
        The workflow node state.

        Attributes:
          NODE_STATE_UNSPECIFIED (int): State is unspecified.
          BLOCKED (int): The node is awaiting prerequisite node to finish.
          RUNNABLE (int): The node is runnable but not running.
          RUNNING (int): The node is running.
          COMPLETED (int): The node completed successfully.
          FAILED (int): The node failed. A node can be marked FAILED because
          its ancestor or peer failed.
        """

        NODE_STATE_UNSPECIFIED = 0
        BLOCKED = 1
        RUNNABLE = 2
        RUNNING = 3
        COMPLETED = 4
        FAILED = 5


class YarnApplication(object):
    class State(enum.IntEnum):
        """
        The application state, corresponding to
        <code>YarnProtos.YarnApplicationStateProto</code>.

        Attributes:
          STATE_UNSPECIFIED (int): Status is unspecified.
          NEW (int): Status is NEW.
          NEW_SAVING (int): Status is NEW\_SAVING.
          SUBMITTED (int): Status is SUBMITTED.
          ACCEPTED (int): Status is ACCEPTED.
          RUNNING (int): Status is RUNNING.
          FINISHED (int): Status is FINISHED.
          FAILED (int): Status is FAILED.
          KILLED (int): Status is KILLED.
        """

        STATE_UNSPECIFIED = 0
        NEW = 1
        NEW_SAVING = 2
        SUBMITTED = 3
        ACCEPTED = 4
        RUNNING = 5
        FINISHED = 6
        FAILED = 7
        KILLED = 8
