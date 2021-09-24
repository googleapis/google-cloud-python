# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.devtools.artifactregistry.v1",
    manifest={
        "Repository",
        "ListRepositoriesRequest",
        "ListRepositoriesResponse",
        "GetRepositoryRequest",
    },
)


class Repository(proto.Message):
    r"""A Repository for storing artifacts with a specific format.

    Attributes:
        name (str):
            The name of the repository, for example:
            "projects/p1/locations/us-
            central1/repositories/repo1".
        format_ (google.cloud.artifactregistry_v1.types.Repository.Format):
            The format of packages that are stored in the
            repository.
        description (str):
            The user-provided description of the
            repository.
        labels (Sequence[google.cloud.artifactregistry_v1.types.Repository.LabelsEntry]):
            Labels with user-defined metadata.
            This field may contain up to 64 entries. Label
            keys and values may be no longer than 63
            characters. Label keys must begin with a
            lowercase letter and may only contain lowercase
            letters, numeric characters, underscores, and
            dashes.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the repository was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the repository was last
            updated.
        kms_key_name (str):
            The Cloud KMS resource name of the customer managed
            encryption key that’s used to encrypt the contents of the
            Repository. Has the form:
            ``projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key``.
            This value may not be changed after the Repository has been
            created.
    """

    class Format(proto.Enum):
        r"""A package format."""
        FORMAT_UNSPECIFIED = 0
        DOCKER = 1
        MAVEN = 2
        NPM = 3
        APT = 5
        YUM = 6
        PYTHON = 8

    name = proto.Field(proto.STRING, number=1,)
    format_ = proto.Field(proto.ENUM, number=2, enum=Format,)
    description = proto.Field(proto.STRING, number=3,)
    labels = proto.MapField(proto.STRING, proto.STRING, number=4,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    kms_key_name = proto.Field(proto.STRING, number=8,)


class ListRepositoriesRequest(proto.Message):
    r"""The request to list repositories.

    Attributes:
        parent (str):
            Required. The name of the parent resource
            whose repositories will be listed.
        page_size (int):
            The maximum number of repositories to return.
        page_token (str):
            The next_page_token value returned from a previous list
            request, if any.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListRepositoriesResponse(proto.Message):
    r"""The response from listing repositories.

    Attributes:
        repositories (Sequence[google.cloud.artifactregistry_v1.types.Repository]):
            The repositories returned.
        next_page_token (str):
            The token to retrieve the next page of
            repositories, or empty if there are no more
            repositories to return.
    """

    @property
    def raw_page(self):
        return self

    repositories = proto.RepeatedField(proto.MESSAGE, number=1, message="Repository",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetRepositoryRequest(proto.Message):
    r"""The request to retrieve a repository.

    Attributes:
        name (str):
            Required. The name of the repository to
            retrieve.
    """

    name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
