# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


class Build(object):
    class Status(enum.IntEnum):
        """
        Possible status of a build or build step.

        Attributes:
          STATUS_UNKNOWN (int): Status of the build is unknown.
          QUEUED (int): Build or step is queued; work has not yet begun.
          WORKING (int): Build or step is being executed.
          SUCCESS (int): Build or step finished successfully.
          FAILURE (int): Build or step failed to complete successfully.
          INTERNAL_ERROR (int): Build or step failed due to an internal cause.
          TIMEOUT (int): Build or step took longer than was allowed.
          CANCELLED (int): Build or step was canceled by a user.
          EXPIRED (int): Build was enqueued for longer than the value of ``queue_ttl``.
        """

        STATUS_UNKNOWN = 0
        QUEUED = 1
        WORKING = 2
        SUCCESS = 3
        FAILURE = 4
        INTERNAL_ERROR = 5
        TIMEOUT = 6
        CANCELLED = 7
        EXPIRED = 9


class BuildOptions(object):
    class LogStreamingOption(enum.IntEnum):
        """
        Specifies the behavior when writing build logs to Google Cloud Storage.

        Attributes:
          STREAM_DEFAULT (int): Service may automatically determine build log streaming behavior.
          STREAM_ON (int): Build logs should be streamed to Google Cloud Storage.
          STREAM_OFF (int): Build logs should not be streamed to Google Cloud Storage; they will be
          written when the build is completed.
        """

        STREAM_DEFAULT = 0
        STREAM_ON = 1
        STREAM_OFF = 2

    class LoggingMode(enum.IntEnum):
        """
        Specifies the logging mode.

        Attributes:
          LOGGING_UNSPECIFIED (int): The service determines the logging mode. The default is ``LEGACY``.
          Do not rely on the default logging behavior as it may change in the
          future.
          LEGACY (int): Stackdriver logging and Cloud Storage logging are enabled.
          GCS_ONLY (int): Only Cloud Storage logging is enabled.
        """

        LOGGING_UNSPECIFIED = 0
        LEGACY = 1
        GCS_ONLY = 2

    class MachineType(enum.IntEnum):
        """
        Supported VM sizes.

        Attributes:
          UNSPECIFIED (int): Standard machine type.
          N1_HIGHCPU_8 (int): Highcpu machine with 8 CPUs.
          N1_HIGHCPU_32 (int): Highcpu machine with 32 CPUs.
        """

        UNSPECIFIED = 0
        N1_HIGHCPU_8 = 1
        N1_HIGHCPU_32 = 2

    class SubstitutionOption(enum.IntEnum):
        """
        Specifies the behavior when there is an error in the substitution checks.

        Attributes:
          MUST_MATCH (int): Fails the build if error in substitutions checks, like missing
          a substitution in the template or in the map.
          ALLOW_LOOSE (int): Do not fail the build if error in substitutions checks.
        """

        MUST_MATCH = 0
        ALLOW_LOOSE = 1

    class VerifyOption(enum.IntEnum):
        """
        Specifies the manner in which the build should be verified, if at all.

        Attributes:
          NOT_VERIFIED (int): Not a verifiable build. (default)
          VERIFIED (int): Verified build.
        """

        NOT_VERIFIED = 0
        VERIFIED = 1


class Hash(object):
    class HashType(enum.IntEnum):
        """
        Specifies the hash algorithm, if any.

        Attributes:
          NONE (int): No hash requested.
          SHA256 (int): Use a sha256 hash.
          MD5 (int): Use a md5 hash.
        """

        NONE = 0
        SHA256 = 1
        MD5 = 2


class PullRequestFilter(object):
    class CommentControl(enum.IntEnum):
        """
        Controls behavior of Pull Request comments.

        Attributes:
          COMMENTS_DISABLED (int): Do not require comments on Pull Requests before builds are triggered.
          COMMENTS_ENABLED (int): Enforce that repository owners or collaborators must comment on Pull
          Requests before builds are triggered.
        """

        COMMENTS_DISABLED = 0
        COMMENTS_ENABLED = 1


class WorkerPool(object):
    class Region(enum.IntEnum):
        """
        Supported GCP regions to create the ``WorkerPool``.

        Attributes:
          REGION_UNSPECIFIED (int): no region
          US_CENTRAL1 (int): us-central1 region
          US_WEST1 (int): us-west1 region
          US_EAST1 (int): us-east1 region
          US_EAST4 (int): us-east4 region
        """

        REGION_UNSPECIFIED = 0
        US_CENTRAL1 = 1
        US_WEST1 = 2
        US_EAST1 = 3
        US_EAST4 = 4

    class Status(enum.IntEnum):
        """
        ``WorkerPool`` status

        Attributes:
          STATUS_UNSPECIFIED (int): Status of the ``WorkerPool`` is unknown.
          CREATING (int): ``WorkerPool`` is being created.
          RUNNING (int): ``WorkerPool`` is running.
          DELETING (int): ``WorkerPool`` is being deleted: cancelling builds and draining
          workers.
          DELETED (int): ``WorkerPool`` is deleted.
        """

        STATUS_UNSPECIFIED = 0
        CREATING = 1
        RUNNING = 2
        DELETING = 3
        DELETED = 4
