# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from grafeas.grafeas_v1.types import common

__protobuf__ = proto.module(
    package="grafeas.v1",
    manifest={
        "SecretKind",
        "SecretNote",
        "SecretOccurrence",
        "SecretLocation",
        "SecretStatus",
    },
)


class SecretKind(proto.Enum):
    r"""Kind of secret.

    Values:
        SECRET_KIND_UNSPECIFIED (0):
            Unspecified
        SECRET_KIND_UNKNOWN (1):
            The secret kind is unknown.
        SECRET_KIND_GCP_SERVICE_ACCOUNT_KEY (2):
            A GCP service account key per:

            https://cloud.google.com/iam/docs/creating-managing-service-account-keys
    """
    SECRET_KIND_UNSPECIFIED = 0
    SECRET_KIND_UNKNOWN = 1
    SECRET_KIND_GCP_SERVICE_ACCOUNT_KEY = 2


class SecretNote(proto.Message):
    r"""The note representing a secret."""


class SecretOccurrence(proto.Message):
    r"""The occurrence provides details of a secret.

    Attributes:
        kind (grafeas.grafeas_v1.types.SecretKind):
            Type of secret.
        locations (MutableSequence[grafeas.grafeas_v1.types.SecretLocation]):
            Locations where the secret is detected.
        statuses (MutableSequence[grafeas.grafeas_v1.types.SecretStatus]):
            Status of the secret.
    """

    kind: "SecretKind" = proto.Field(
        proto.ENUM,
        number=1,
        enum="SecretKind",
    )
    locations: MutableSequence["SecretLocation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="SecretLocation",
    )
    statuses: MutableSequence["SecretStatus"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="SecretStatus",
    )


class SecretLocation(proto.Message):
    r"""The location of the secret.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        file_location (grafeas.grafeas_v1.types.FileLocation):
            The secret is found from a file.

            This field is a member of `oneof`_ ``location``.
    """

    file_location: common.FileLocation = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="location",
        message=common.FileLocation,
    )


class SecretStatus(proto.Message):
    r"""The status of the secret with a timestamp.

    Attributes:
        status (grafeas.grafeas_v1.types.SecretStatus.Status):
            The status of the secret.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the secret status was last updated.
        message (str):
            Optional message about the status code.
    """

    class Status(proto.Enum):
        r"""The status of the secret.

        Values:
            STATUS_UNSPECIFIED (0):
                Unspecified
            UNKNOWN (1):
                The status of the secret is unknown.
            VALID (2):
                The secret is valid.
            INVALID (3):
                The secret is invalid.
        """
        STATUS_UNSPECIFIED = 0
        UNKNOWN = 1
        VALID = 2
        INVALID = 3

    status: Status = proto.Field(
        proto.ENUM,
        number=1,
        enum=Status,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    message: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
