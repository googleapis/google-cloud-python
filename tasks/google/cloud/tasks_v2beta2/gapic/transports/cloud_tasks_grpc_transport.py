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

import google.api_core.grpc_helpers

from google.cloud.tasks_v2beta2.proto import cloudtasks_pb2_grpc


class CloudTasksGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.tasks.v2beta2 CloudTasks API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="cloudtasks.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {"cloud_tasks_stub": cloudtasks_pb2_grpc.CloudTasksStub(channel)}

    @classmethod
    def create_channel(cls, address="cloudtasks.googleapis.com:443", credentials=None):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_queues(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.list_queues`.

        Lists queues.

        Queues are returned in lexicographical order.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].ListQueues

    @property
    def get_queue(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.get_queue`.

        Gets a queue.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].GetQueue

    @property
    def create_queue(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.create_queue`.

        Creates a queue.

        Queues created with this method allow tasks to live for a maximum of 31
        days. After a task is 31 days old, the task will be deleted regardless
        of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if you are
        using an App Engine ``queue.yaml`` or ``queue.xml`` file to manage your
        queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__ before
        using this method.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].CreateQueue

    @property
    def update_queue(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.update_queue`.

        Updates a queue.

        This method creates the queue if it does not exist and updates the queue
        if it does exist.

        Queues created with this method allow tasks to live for a maximum of 31
        days. After a task is 31 days old, the task will be deleted regardless
        of whether it was dispatched or not.

        WARNING: Using this method may have unintended side effects if you are
        using an App Engine ``queue.yaml`` or ``queue.xml`` file to manage your
        queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__ before
        using this method.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].UpdateQueue

    @property
    def delete_queue(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.delete_queue`.

        Deletes a queue.

        This command will delete the queue even if it has tasks in it.

        Note: If you delete a queue, a queue with the same name can't be created
        for 7 days.

        WARNING: Using this method may have unintended side effects if you are
        using an App Engine ``queue.yaml`` or ``queue.xml`` file to manage your
        queues. Read `Overview of Queue Management and
        queue.yaml <https://cloud.google.com/tasks/docs/queue-yaml>`__ before
        using this method.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].DeleteQueue

    @property
    def purge_queue(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.purge_queue`.

        Purges a queue by deleting all of its tasks.

        All tasks created before this method is called are permanently deleted.

        Purge operations can take up to one minute to take effect. Tasks
        might be dispatched before the purge takes effect. A purge is irreversible.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].PurgeQueue

    @property
    def pause_queue(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.pause_queue`.

        Pauses the queue.

        If a queue is paused then the system will stop dispatching tasks until
        the queue is resumed via ``ResumeQueue``. Tasks can still be added when
        the queue is paused. A queue is paused if its ``state`` is ``PAUSED``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].PauseQueue

    @property
    def resume_queue(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.resume_queue`.

        Resume a queue.

        This method resumes a queue after it has been ``PAUSED`` or
        ``DISABLED``. The state of a queue is stored in the queue's ``state``;
        after calling this method it will be set to ``RUNNING``.

        WARNING: Resuming many high-QPS queues at the same time can lead to
        target overloading. If you are resuming high-QPS queues, follow the
        500/50/5 pattern described in `Managing Cloud Tasks Scaling
        Risks <https://cloud.google.com/tasks/docs/manage-cloud-task-scaling>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].ResumeQueue

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.get_iam_policy`.

        Gets the access control policy for a ``Queue``. Returns an empty policy
        if the resource exists and does not have a policy set.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the specified
        resource parent:

        -  ``cloudtasks.queues.getIamPolicy``

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].GetIamPolicy

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.set_iam_policy`.

        Sets the access control policy for a ``Queue``. Replaces any existing
        policy.

        Note: The Cloud Console does not check queue-level IAM permissions yet.
        Project-level permissions are required to use the Cloud Console.

        Authorization requires the following `Google
        IAM <https://cloud.google.com/iam>`__ permission on the specified
        resource parent:

        -  ``cloudtasks.queues.setIamPolicy``

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].SetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.test_iam_permissions`.

        Returns permissions that a caller has on a ``Queue``. If the resource
        does not exist, this will return an empty set of permissions, not a
        ``NOT_FOUND`` error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].TestIamPermissions

    @property
    def list_tasks(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.list_tasks`.

        Lists the tasks in a queue.

        By default, only the ``BASIC`` view is retrieved due to performance
        considerations; ``response_view`` controls the subset of information
        which is returned.

        The tasks may be returned in any order. The ordering may change at any
        time.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].ListTasks

    @property
    def get_task(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.get_task`.

        Gets a task.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].GetTask

    @property
    def create_task(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.create_task`.

        Creates a task and adds it to a queue.

        Tasks cannot be updated after creation; there is no UpdateTask command.

        -  For ``App Engine queues``, the maximum task size is 100KB.
        -  For ``pull queues``, the maximum task size is 1MB.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].CreateTask

    @property
    def delete_task(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.delete_task`.

        Deletes a task.

        A task can be deleted if it is scheduled or dispatched. A task
        cannot be deleted if it has completed successfully or permanently
        failed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].DeleteTask

    @property
    def lease_tasks(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.lease_tasks`.

        Leases tasks from a pull queue for ``lease_duration``.

        This method is invoked by the worker to obtain a lease. The worker must
        acknowledge the task via ``AcknowledgeTask`` after they have performed
        the work associated with the task.

        The ``payload`` is intended to store data that the worker needs to
        perform the work associated with the task. To return the payloads in the
        ``response``, set ``response_view`` to ``FULL``.

        A maximum of 10 qps of ``LeaseTasks`` requests are allowed per queue.
        ``RESOURCE_EXHAUSTED`` is returned when this limit is exceeded.
        ``RESOURCE_EXHAUSTED`` is also returned when
        ``max_tasks_dispatched_per_second`` is exceeded.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].LeaseTasks

    @property
    def acknowledge_task(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.acknowledge_task`.

        Acknowledges a pull task.

        The worker, that is, the entity that ``leased`` this task must call this
        method to indicate that the work associated with the task has finished.

        The worker must acknowledge a task within the ``lease_duration`` or the
        lease will expire and the task will become available to be leased again.
        After the task is acknowledged, it will not be returned by a later
        ``LeaseTasks``, ``GetTask``, or ``ListTasks``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].AcknowledgeTask

    @property
    def renew_lease(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.renew_lease`.

        Renew the current lease of a pull task.

        The worker can use this method to extend the lease by a new duration,
        starting from now. The new task lease will be returned in the task's
        ``schedule_time``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].RenewLease

    @property
    def cancel_lease(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.cancel_lease`.

        Cancel a pull task's lease.

        The worker can use this method to cancel a task's lease by setting its
        ``schedule_time`` to now. This will make the task available to be leased
        to the next caller of ``LeaseTasks``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].CancelLease

    @property
    def run_task(self):
        """Return the gRPC stub for :meth:`CloudTasksClient.run_task`.

        Forces a task to run now.

        When this method is called, Cloud Tasks will dispatch the task, even if
        the task is already running, the queue has reached its ``RateLimits`` or
        is ``PAUSED``.

        This command is meant to be used for manual debugging. For example,
        ``RunTask`` can be used to retry a failed task after a fix has been made
        or to manually force a task to be dispatched now.

        The dispatched task is returned. That is, the task that is returned
        contains the ``status`` after the task is dispatched but before the task
        is received by its target.

        If Cloud Tasks receives a successful response from the task's target,
        then the task will be deleted; otherwise the task's ``schedule_time``
        will be reset to the time that ``RunTask`` was called plus the retry
        delay specified in the queue's ``RetryConfig``.

        ``RunTask`` returns ``NOT_FOUND`` when it is called on a task that has
        already succeeded or permanently failed.

        ``RunTask`` cannot be called on a ``pull task``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["cloud_tasks_stub"].RunTask
