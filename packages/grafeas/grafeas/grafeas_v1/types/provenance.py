# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
    package="grafeas.v1",
    manifest={
        "BuildProvenance",
        "Source",
        "FileHashes",
        "Hash",
        "Command",
        "Artifact",
        "SourceContext",
        "AliasContext",
        "CloudRepoSourceContext",
        "GerritSourceContext",
        "GitSourceContext",
        "RepoId",
        "ProjectRepoId",
    },
)


class BuildProvenance(proto.Message):
    r"""Provenance of a build. Contains all information needed to
    verify the full details about the build from source to
    completion.

    Attributes:
        id (str):
            Required. Unique identifier of the build.
        project_id (str):
            ID of the project.
        commands (Sequence[grafeas.grafeas_v1.types.Command]):
            Commands requested by the build.
        built_artifacts (Sequence[grafeas.grafeas_v1.types.Artifact]):
            Output of the build.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Time at which the build was created.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Time at which execution of the build was
            started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Time at which execution of the build was
            finished.
        creator (str):
            E-mail address of the user who initiated this
            build. Note that this was the user's e-mail
            address at the time the build was initiated;
            this address may not represent the same end-user
            for all time.
        logs_uri (str):
            URI where any logs for this provenance were
            written.
        source_provenance (grafeas.grafeas_v1.types.Source):
            Details of the Source input to the build.
        trigger_id (str):
            Trigger identifier if the build was triggered
            automatically; empty if not.
        build_options (Sequence[grafeas.grafeas_v1.types.BuildProvenance.BuildOptionsEntry]):
            Special options applied to this build. This
            is a catch-all field where build providers can
            enter any desired additional details.
        builder_version (str):
            Version string of the builder at the time
            this build was executed.
    """

    id = proto.Field(proto.STRING, number=1,)
    project_id = proto.Field(proto.STRING, number=2,)
    commands = proto.RepeatedField(proto.MESSAGE, number=3, message="Command",)
    built_artifacts = proto.RepeatedField(proto.MESSAGE, number=4, message="Artifact",)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    start_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    creator = proto.Field(proto.STRING, number=8,)
    logs_uri = proto.Field(proto.STRING, number=9,)
    source_provenance = proto.Field(proto.MESSAGE, number=10, message="Source",)
    trigger_id = proto.Field(proto.STRING, number=11,)
    build_options = proto.MapField(proto.STRING, proto.STRING, number=12,)
    builder_version = proto.Field(proto.STRING, number=13,)


class Source(proto.Message):
    r"""Source describes the location of the source used for the
    build.

    Attributes:
        artifact_storage_source_uri (str):
            If provided, the input binary artifacts for
            the build came from this location.
        file_hashes (Sequence[grafeas.grafeas_v1.types.Source.FileHashesEntry]):
            Hash(es) of the build source, which can be
            used to verify that the original source
            integrity was maintained in the build.
            The keys to this map are file paths used as
            build source and the values contain the hash
            values for those files.

            If the build source came in a single package
            such as a gzipped tarfile (.tar.gz), the
            FileHash will be for the single path to that
            file.
        context (grafeas.grafeas_v1.types.SourceContext):
            If provided, the source code used for the
            build came from this location.
        additional_contexts (Sequence[grafeas.grafeas_v1.types.SourceContext]):
            If provided, some of the source code used for
            the build may be found in these locations, in
            the case where the source repository had
            multiple remotes or submodules. This list will
            not include the context specified in the context
            field.
    """

    artifact_storage_source_uri = proto.Field(proto.STRING, number=1,)
    file_hashes = proto.MapField(
        proto.STRING, proto.MESSAGE, number=2, message="FileHashes",
    )
    context = proto.Field(proto.MESSAGE, number=3, message="SourceContext",)
    additional_contexts = proto.RepeatedField(
        proto.MESSAGE, number=4, message="SourceContext",
    )


class FileHashes(proto.Message):
    r"""Container message for hashes of byte content of files, used
    in source messages to verify integrity of source input to the
    build.

    Attributes:
        file_hash (Sequence[grafeas.grafeas_v1.types.Hash]):
            Required. Collection of file hashes.
    """

    file_hash = proto.RepeatedField(proto.MESSAGE, number=1, message="Hash",)


class Hash(proto.Message):
    r"""Container message for hash values.

    Attributes:
        type_ (str):
            Required. The type of hash that was
            performed, e.g. "SHA-256".
        value (bytes):
            Required. The hash value.
    """

    type_ = proto.Field(proto.STRING, number=1,)
    value = proto.Field(proto.BYTES, number=2,)


class Command(proto.Message):
    r"""Command describes a step performed as part of the build
    pipeline.

    Attributes:
        name (str):
            Required. Name of the command, as presented on the command
            line, or if the command is packaged as a Docker container,
            as presented to ``docker pull``.
        env (Sequence[str]):
            Environment variables set before running this
            command.
        args (Sequence[str]):
            Command-line arguments used when executing
            this command.
        dir_ (str):
            Working directory (relative to project source
            root) used when running this command.
        id (str):
            Optional unique identifier for this command, used in
            wait_for to reference this command as a dependency.
        wait_for (Sequence[str]):
            The ID(s) of the command(s) that this command
            depends on.
    """

    name = proto.Field(proto.STRING, number=1,)
    env = proto.RepeatedField(proto.STRING, number=2,)
    args = proto.RepeatedField(proto.STRING, number=3,)
    dir_ = proto.Field(proto.STRING, number=4,)
    id = proto.Field(proto.STRING, number=5,)
    wait_for = proto.RepeatedField(proto.STRING, number=6,)


class Artifact(proto.Message):
    r"""Artifact describes a build product.

    Attributes:
        checksum (str):
            Hash or checksum value of a binary, or Docker
            Registry 2.0 digest of a container.
        id (str):
            Artifact ID, if any; for container images, this will be a
            URL by digest like
            ``gcr.io/projectID/imagename@sha256:123456``.
        names (Sequence[str]):
            Related artifact names. This may be the path to a binary or
            jar file, or in the case of a container build, the name used
            to push the container image to Google Container Registry, as
            presented to ``docker push``. Note that a single Artifact ID
            can have multiple names, for example if two tags are applied
            to one image.
    """

    checksum = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.STRING, number=2,)
    names = proto.RepeatedField(proto.STRING, number=3,)


class SourceContext(proto.Message):
    r"""A SourceContext is a reference to a tree of files. A
    SourceContext together with a path point to a unique revision of
    a single file or directory.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        cloud_repo (grafeas.grafeas_v1.types.CloudRepoSourceContext):
            A SourceContext referring to a revision in a
            Google Cloud Source Repo.

            This field is a member of `oneof`_ ``context``.
        gerrit (grafeas.grafeas_v1.types.GerritSourceContext):
            A SourceContext referring to a Gerrit
            project.

            This field is a member of `oneof`_ ``context``.
        git (grafeas.grafeas_v1.types.GitSourceContext):
            A SourceContext referring to any third party
            Git repo (e.g., GitHub).

            This field is a member of `oneof`_ ``context``.
        labels (Sequence[grafeas.grafeas_v1.types.SourceContext.LabelsEntry]):
            Labels with user defined metadata.
    """

    cloud_repo = proto.Field(
        proto.MESSAGE, number=1, oneof="context", message="CloudRepoSourceContext",
    )
    gerrit = proto.Field(
        proto.MESSAGE, number=2, oneof="context", message="GerritSourceContext",
    )
    git = proto.Field(
        proto.MESSAGE, number=3, oneof="context", message="GitSourceContext",
    )
    labels = proto.MapField(proto.STRING, proto.STRING, number=4,)


class AliasContext(proto.Message):
    r"""An alias to a repo revision.

    Attributes:
        kind (grafeas.grafeas_v1.types.AliasContext.Kind):
            The alias kind.
        name (str):
            The alias name.
    """

    class Kind(proto.Enum):
        r"""The type of an alias."""
        KIND_UNSPECIFIED = 0
        FIXED = 1
        MOVABLE = 2
        OTHER = 4

    kind = proto.Field(proto.ENUM, number=1, enum=Kind,)
    name = proto.Field(proto.STRING, number=2,)


class CloudRepoSourceContext(proto.Message):
    r"""A CloudRepoSourceContext denotes a particular revision in a
    Google Cloud Source Repo.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        repo_id (grafeas.grafeas_v1.types.RepoId):
            The ID of the repo.
        revision_id (str):
            A revision ID.

            This field is a member of `oneof`_ ``revision``.
        alias_context (grafeas.grafeas_v1.types.AliasContext):
            An alias, which may be a branch or tag.

            This field is a member of `oneof`_ ``revision``.
    """

    repo_id = proto.Field(proto.MESSAGE, number=1, message="RepoId",)
    revision_id = proto.Field(proto.STRING, number=2, oneof="revision",)
    alias_context = proto.Field(
        proto.MESSAGE, number=3, oneof="revision", message="AliasContext",
    )


class GerritSourceContext(proto.Message):
    r"""A SourceContext referring to a Gerrit project.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        host_uri (str):
            The URI of a running Gerrit instance.
        gerrit_project (str):
            The full project name within the host.
            Projects may be nested, so "project/subproject"
            is a valid project name. The "repo name" is the
            hostURI/project.
        revision_id (str):
            A revision (commit) ID.

            This field is a member of `oneof`_ ``revision``.
        alias_context (grafeas.grafeas_v1.types.AliasContext):
            An alias, which may be a branch or tag.

            This field is a member of `oneof`_ ``revision``.
    """

    host_uri = proto.Field(proto.STRING, number=1,)
    gerrit_project = proto.Field(proto.STRING, number=2,)
    revision_id = proto.Field(proto.STRING, number=3, oneof="revision",)
    alias_context = proto.Field(
        proto.MESSAGE, number=4, oneof="revision", message="AliasContext",
    )


class GitSourceContext(proto.Message):
    r"""A GitSourceContext denotes a particular revision in a third
    party Git repository (e.g., GitHub).

    Attributes:
        url (str):
            Git repository URL.
        revision_id (str):
            Git commit hash.
    """

    url = proto.Field(proto.STRING, number=1,)
    revision_id = proto.Field(proto.STRING, number=2,)


class RepoId(proto.Message):
    r"""A unique identifier for a Cloud Repo.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        project_repo_id (grafeas.grafeas_v1.types.ProjectRepoId):
            A combination of a project ID and a repo
            name.

            This field is a member of `oneof`_ ``id``.
        uid (str):
            A server-assigned, globally unique
            identifier.

            This field is a member of `oneof`_ ``id``.
    """

    project_repo_id = proto.Field(
        proto.MESSAGE, number=1, oneof="id", message="ProjectRepoId",
    )
    uid = proto.Field(proto.STRING, number=2, oneof="id",)


class ProjectRepoId(proto.Message):
    r"""Selects a repo using a Google Cloud Platform project ID
    (e.g., winged-cargo-31) and a repo name within that project.

    Attributes:
        project_id (str):
            The ID of the project.
        repo_name (str):
            The name of the repo. Leave empty for the
            default repo.
    """

    project_id = proto.Field(proto.STRING, number=1,)
    repo_name = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
