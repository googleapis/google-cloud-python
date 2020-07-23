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


from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.devtools.cloudbuild.v1",
    manifest={
        "RetryBuildRequest",
        "RunBuildTriggerRequest",
        "StorageSource",
        "RepoSource",
        "Source",
        "BuiltImage",
        "BuildStep",
        "Volume",
        "Results",
        "ArtifactResult",
        "Build",
        "Artifacts",
        "TimeSpan",
        "BuildOperationMetadata",
        "SourceProvenance",
        "FileHashes",
        "Hash",
        "Secret",
        "CreateBuildRequest",
        "GetBuildRequest",
        "ListBuildsRequest",
        "ListBuildsResponse",
        "CancelBuildRequest",
        "BuildTrigger",
        "GitHubEventsConfig",
        "PullRequestFilter",
        "PushFilter",
        "CreateBuildTriggerRequest",
        "GetBuildTriggerRequest",
        "ListBuildTriggersRequest",
        "ListBuildTriggersResponse",
        "DeleteBuildTriggerRequest",
        "UpdateBuildTriggerRequest",
        "BuildOptions",
        "WorkerPool",
        "WorkerConfig",
        "Network",
        "CreateWorkerPoolRequest",
        "GetWorkerPoolRequest",
        "DeleteWorkerPoolRequest",
        "UpdateWorkerPoolRequest",
        "ListWorkerPoolsRequest",
        "ListWorkerPoolsResponse",
    },
)


class RetryBuildRequest(proto.Message):
    r"""Specifies a build to retry.

    Attributes:
        project_id (str):
            Required. ID of the project.
        id (str):
            Required. Build ID of the original build.
    """

    project_id = proto.Field(proto.STRING, number=1)

    id = proto.Field(proto.STRING, number=2)


class RunBuildTriggerRequest(proto.Message):
    r"""Specifies a build trigger to run and the source to use.

    Attributes:
        project_id (str):
            Required. ID of the project.
        trigger_id (str):
            Required. ID of the trigger.
        source (~.cloudbuild.RepoSource):
            Required. Source to build against this
            trigger.
    """

    project_id = proto.Field(proto.STRING, number=1)

    trigger_id = proto.Field(proto.STRING, number=2)

    source = proto.Field(proto.MESSAGE, number=3, message="RepoSource",)


class StorageSource(proto.Message):
    r"""Location of the source in an archive file in Google Cloud
    Storage.

    Attributes:
        bucket (str):
            Google Cloud Storage bucket containing the source (see
            `Bucket Name
            Requirements <https://cloud.google.com/storage/docs/bucket-naming#requirements>`__).
        object (str):
            Google Cloud Storage object containing the source.

            This object must be a gzipped archive file (``.tar.gz``)
            containing source to build.
        generation (int):
            Google Cloud Storage generation for the
            object. If the generation is omitted, the latest
            generation will be used.
    """

    bucket = proto.Field(proto.STRING, number=1)

    object = proto.Field(proto.STRING, number=2)

    generation = proto.Field(proto.INT64, number=3)


class RepoSource(proto.Message):
    r"""Location of the source in a Google Cloud Source Repository.

    Attributes:
        project_id (str):
            ID of the project that owns the Cloud Source
            Repository. If omitted, the project ID
            requesting the build is assumed.
        repo_name (str):
            Required. Name of the Cloud Source
            Repository.
        branch_name (str):
            Regex matching branches to build.
            The syntax of the regular expressions accepted
            is the syntax accepted by RE2 and described at
            https://github.com/google/re2/wiki/Syntax
        tag_name (str):
            Regex matching tags to build.
            The syntax of the regular expressions accepted
            is the syntax accepted by RE2 and described at
            https://github.com/google/re2/wiki/Syntax
        commit_sha (str):
            Explicit commit SHA to build.
        dir (str):
            Directory, relative to the source root, in which to run the
            build.

            This must be a relative path. If a step's ``dir`` is
            specified and is an absolute path, this value is ignored for
            that step's execution.
        invert_regex (bool):
            Only trigger a build if the revision regex
            does NOT match the revision regex.
        substitutions (Sequence[~.cloudbuild.RepoSource.SubstitutionsEntry]):
            Substitutions to use in a triggered build.
            Should only be used with RunBuildTrigger
    """

    project_id = proto.Field(proto.STRING, number=1)

    repo_name = proto.Field(proto.STRING, number=2)

    branch_name = proto.Field(proto.STRING, number=3, oneof="revision")

    tag_name = proto.Field(proto.STRING, number=4, oneof="revision")

    commit_sha = proto.Field(proto.STRING, number=5, oneof="revision")

    dir = proto.Field(proto.STRING, number=7)

    invert_regex = proto.Field(proto.BOOL, number=8)

    substitutions = proto.MapField(proto.STRING, proto.STRING, number=9)


class Source(proto.Message):
    r"""Location of the source in a supported storage service.

    Attributes:
        storage_source (~.cloudbuild.StorageSource):
            If provided, get the source from this
            location in Google Cloud Storage.
        repo_source (~.cloudbuild.RepoSource):
            If provided, get the source from this
            location in a Cloud Source Repository.
    """

    storage_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message=StorageSource,
    )

    repo_source = proto.Field(
        proto.MESSAGE, number=3, oneof="source", message=RepoSource,
    )


class BuiltImage(proto.Message):
    r"""An image built by the pipeline.

    Attributes:
        name (str):
            Name used to push the container image to Google Container
            Registry, as presented to ``docker push``.
        digest (str):
            Docker Registry 2.0 digest.
        push_timing (~.cloudbuild.TimeSpan):
            Output only. Stores timing information for
            pushing the specified image.
    """

    name = proto.Field(proto.STRING, number=1)

    digest = proto.Field(proto.STRING, number=3)

    push_timing = proto.Field(proto.MESSAGE, number=4, message="TimeSpan",)


class BuildStep(proto.Message):
    r"""A step in the build pipeline.

    Attributes:
        name (str):
            Required. The name of the container image that will run this
            particular build step.

            If the image is available in the host's Docker daemon's
            cache, it will be run directly. If not, the host will
            attempt to pull the image first, using the builder service
            account's credentials if necessary.

            The Docker daemon's cache will already have the latest
            versions of all of the officially supported build steps
            (https://github.com/GoogleCloudPlatform/cloud-builders). The
            Docker daemon will also have cached many of the layers for
            some popular images, like "ubuntu", "debian", but they will
            be refreshed at the time you attempt to use them.

            If you built an image in a previous build step, it will be
            stored in the host's Docker daemon's cache and is available
            to use as the name for a later build step.
        env (Sequence[str]):
            A list of environment variable definitions to
            be used when running a step.
            The elements are of the form "KEY=VALUE" for the
            environment variable "KEY" being given the value
            "VALUE".
        args (Sequence[str]):
            A list of arguments that will be presented to the step when
            it is started.

            If the image used to run the step's container has an
            entrypoint, the ``args`` are used as arguments to that
            entrypoint. If the image does not define an entrypoint, the
            first element in args is used as the entrypoint, and the
            remainder will be used as arguments.
        dir (str):
            Working directory to use when running this step's container.

            If this value is a relative path, it is relative to the
            build's working directory. If this value is absolute, it may
            be outside the build's working directory, in which case the
            contents of the path may not be persisted across build step
            executions, unless a ``volume`` for that path is specified.

            If the build specifies a ``RepoSource`` with ``dir`` and a
            step with a ``dir``, which specifies an absolute path, the
            ``RepoSource`` ``dir`` is ignored for the step's execution.
        id (str):
            Unique identifier for this build step, used in ``wait_for``
            to reference this build step as a dependency.
        wait_for (Sequence[str]):
            The ID(s) of the step(s) that this build step depends on.
            This build step will not start until all the build steps in
            ``wait_for`` have completed successfully. If ``wait_for`` is
            empty, this build step will start when all previous build
            steps in the ``Build.Steps`` list have completed
            successfully.
        entrypoint (str):
            Entrypoint to be used instead of the build
            step image's default entrypoint. If unset, the
            image's default entrypoint is used.
        secret_env (Sequence[str]):
            A list of environment variables which are encrypted using a
            Cloud Key Management Service crypto key. These values must
            be specified in the build's ``Secret``.
        volumes (Sequence[~.cloudbuild.Volume]):
            List of volumes to mount into the build step.
            Each volume is created as an empty volume prior
            to execution of the build step. Upon completion
            of the build, volumes and their contents are
            discarded.

            Using a named volume in only one step is not
            valid as it is indicative of a build request
            with an incorrect configuration.
        timing (~.cloudbuild.TimeSpan):
            Output only. Stores timing information for
            executing this build step.
        pull_timing (~.cloudbuild.TimeSpan):
            Output only. Stores timing information for
            pulling this build step's builder image only.
        timeout (~.duration.Duration):
            Time limit for executing this build step. If
            not defined, the step has no time limit and will
            be allowed to continue to run until either it
            completes or the build itself times out.
        status (~.cloudbuild.Build.Status):
            Output only. Status of the build step. At
            this time, build step status is only updated on
            build completion; step status is not updated in
            real-time as the build progresses.
    """

    name = proto.Field(proto.STRING, number=1)

    env = proto.RepeatedField(proto.STRING, number=2)

    args = proto.RepeatedField(proto.STRING, number=3)

    dir = proto.Field(proto.STRING, number=4)

    id = proto.Field(proto.STRING, number=5)

    wait_for = proto.RepeatedField(proto.STRING, number=6)

    entrypoint = proto.Field(proto.STRING, number=7)

    secret_env = proto.RepeatedField(proto.STRING, number=8)

    volumes = proto.RepeatedField(proto.MESSAGE, number=9, message="Volume",)

    timing = proto.Field(proto.MESSAGE, number=10, message="TimeSpan",)

    pull_timing = proto.Field(proto.MESSAGE, number=13, message="TimeSpan",)

    timeout = proto.Field(proto.MESSAGE, number=11, message=duration.Duration,)

    status = proto.Field(proto.ENUM, number=12, enum="Build.Status",)


class Volume(proto.Message):
    r"""Volume describes a Docker container volume which is mounted
    into build steps in order to persist files across build step
    execution.

    Attributes:
        name (str):
            Name of the volume to mount.
            Volume names must be unique per build step and
            must be valid names for Docker volumes. Each
            named volume must be used by at least two build
            steps.
        path (str):
            Path at which to mount the volume.
            Paths must be absolute and cannot conflict with
            other volume paths on the same build step or
            with certain reserved volume paths.
    """

    name = proto.Field(proto.STRING, number=1)

    path = proto.Field(proto.STRING, number=2)


class Results(proto.Message):
    r"""Artifacts created by the build pipeline.

    Attributes:
        images (Sequence[~.cloudbuild.BuiltImage]):
            Container images that were built as a part of
            the build.
        build_step_images (Sequence[str]):
            List of build step digests, in the order
            corresponding to build step indices.
        artifact_manifest (str):
            Path to the artifact manifest. Only populated
            when artifacts are uploaded.
        num_artifacts (int):
            Number of artifacts uploaded. Only populated
            when artifacts are uploaded.
        build_step_outputs (Sequence[bytes]):
            List of build step outputs, produced by builder images, in
            the order corresponding to build step indices.

            `Cloud
            Builders <https://cloud.google.com/cloud-build/docs/cloud-builders>`__
            can produce this output by writing to
            ``$BUILDER_OUTPUT/output``. Only the first 4KB of data is
            stored.
        artifact_timing (~.cloudbuild.TimeSpan):
            Time to push all non-container artifacts.
    """

    images = proto.RepeatedField(proto.MESSAGE, number=2, message=BuiltImage,)

    build_step_images = proto.RepeatedField(proto.STRING, number=3)

    artifact_manifest = proto.Field(proto.STRING, number=4)

    num_artifacts = proto.Field(proto.INT64, number=5)

    build_step_outputs = proto.RepeatedField(proto.BYTES, number=6)

    artifact_timing = proto.Field(proto.MESSAGE, number=7, message="TimeSpan",)


class ArtifactResult(proto.Message):
    r"""An artifact that was uploaded during a build. This
    is a single record in the artifact manifest JSON file.

    Attributes:
        location (str):
            The path of an artifact in a Google Cloud Storage bucket,
            with the generation number. For example,
            ``gs://mybucket/path/to/output.jar#generation``.
        file_hash (Sequence[~.cloudbuild.FileHashes]):
            The file hash of the artifact.
    """

    location = proto.Field(proto.STRING, number=1)

    file_hash = proto.RepeatedField(proto.MESSAGE, number=2, message="FileHashes",)


class Build(proto.Message):
    r"""A build resource in the Cloud Build API.

    At a high level, a ``Build`` describes where to find source code,
    how to build it (for example, the builder image to run on the
    source), and where to store the built artifacts.

    Fields can include the following variables, which will be expanded
    when the build is created:

    -  $PROJECT_ID: the project ID of the build.
    -  $BUILD_ID: the autogenerated ID of the build.
    -  $REPO_NAME: the source repository name specified by RepoSource.
    -  $BRANCH_NAME: the branch name specified by RepoSource.
    -  $TAG_NAME: the tag name specified by RepoSource.
    -  $REVISION_ID or $COMMIT_SHA: the commit SHA specified by
       RepoSource or resolved from the specified branch or tag.
    -  $SHORT_SHA: first 7 characters of $REVISION_ID or $COMMIT_SHA.

    Attributes:
        id (str):
            Output only. Unique identifier of the build.
        project_id (str):
            Output only. ID of the project.
        status (~.cloudbuild.Build.Status):
            Output only. Status of the build.
        status_detail (str):
            Output only. Customer-readable message about
            the current status.
        source (~.cloudbuild.Source):
            The location of the source files to build.
        steps (Sequence[~.cloudbuild.BuildStep]):
            Required. The operations to be performed on
            the workspace.
        results (~.cloudbuild.Results):
            Output only. Results of the build.
        create_time (~.timestamp.Timestamp):
            Output only. Time at which the request to
            create the build was received.
        start_time (~.timestamp.Timestamp):
            Output only. Time at which execution of the
            build was started.
        finish_time (~.timestamp.Timestamp):
            Output only. Time at which execution of the build was
            finished.

            The difference between finish_time and start_time is the
            duration of the build's execution.
        timeout (~.duration.Duration):
            Amount of time that this build should be allowed to run, to
            second granularity. If this amount of time elapses, work on
            the build will cease and the build status will be
            ``TIMEOUT``.

            Default time is ten minutes.
        images (Sequence[str]):
            A list of images to be pushed upon the successful completion
            of all build steps.

            The images are pushed using the builder service account's
            credentials.

            The digests of the pushed images will be stored in the
            ``Build`` resource's results field.

            If any of the images fail to be pushed, the build status is
            marked ``FAILURE``.
        queue_ttl (~.duration.Duration):
            TTL in queue for this build. If provided and the build is
            enqueued longer than this value, the build will expire and
            the build status will be ``EXPIRED``.

            The TTL starts ticking from create_time.
        artifacts (~.cloudbuild.Artifacts):
            Artifacts produced by the build that should
            be uploaded upon successful completion of all
            build steps.
        logs_bucket (str):
            Google Cloud Storage bucket where logs should be written
            (see `Bucket Name
            Requirements <https://cloud.google.com/storage/docs/bucket-naming#requirements>`__).
            Logs file names will be of the format
            ``${logs_bucket}/log-${build_id}.txt``.
        source_provenance (~.cloudbuild.SourceProvenance):
            Output only. A permanent fixed identifier for
            source.
        build_trigger_id (str):
            Output only. The ID of the ``BuildTrigger`` that triggered
            this build, if it was triggered automatically.
        options (~.cloudbuild.BuildOptions):
            Special options for this build.
        log_url (str):
            Output only. URL to logs for this build in
            Google Cloud Console.
        substitutions (Sequence[~.cloudbuild.Build.SubstitutionsEntry]):
            Substitutions data for ``Build`` resource.
        tags (Sequence[str]):
            Tags for annotation of a ``Build``. These are not docker
            tags.
        secrets (Sequence[~.cloudbuild.Secret]):
            Secrets to decrypt using Cloud Key Management
            Service.
        timing (Sequence[~.cloudbuild.Build.TimingEntry]):
            Output only. Stores timing information for phases of the
            build. Valid keys are:

            -  BUILD: time to execute all build steps
            -  PUSH: time to push all specified images.
            -  FETCHSOURCE: time to fetch source.

            If the build does not specify source or images, these keys
            will not be included.
    """

    class Status(proto.Enum):
        r"""Possible status of a build or build step."""
        STATUS_UNKNOWN = 0
        QUEUED = 1
        WORKING = 2
        SUCCESS = 3
        FAILURE = 4
        INTERNAL_ERROR = 5
        TIMEOUT = 6
        CANCELLED = 7
        EXPIRED = 9

    id = proto.Field(proto.STRING, number=1)

    project_id = proto.Field(proto.STRING, number=16)

    status = proto.Field(proto.ENUM, number=2, enum=Status,)

    status_detail = proto.Field(proto.STRING, number=24)

    source = proto.Field(proto.MESSAGE, number=3, message=Source,)

    steps = proto.RepeatedField(proto.MESSAGE, number=11, message=BuildStep,)

    results = proto.Field(proto.MESSAGE, number=10, message=Results,)

    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp.Timestamp,)

    start_time = proto.Field(proto.MESSAGE, number=7, message=timestamp.Timestamp,)

    finish_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp,)

    timeout = proto.Field(proto.MESSAGE, number=12, message=duration.Duration,)

    images = proto.RepeatedField(proto.STRING, number=13)

    queue_ttl = proto.Field(proto.MESSAGE, number=40, message=duration.Duration,)

    artifacts = proto.Field(proto.MESSAGE, number=37, message="Artifacts",)

    logs_bucket = proto.Field(proto.STRING, number=19)

    source_provenance = proto.Field(
        proto.MESSAGE, number=21, message="SourceProvenance",
    )

    build_trigger_id = proto.Field(proto.STRING, number=22)

    options = proto.Field(proto.MESSAGE, number=23, message="BuildOptions",)

    log_url = proto.Field(proto.STRING, number=25)

    substitutions = proto.MapField(proto.STRING, proto.STRING, number=29)

    tags = proto.RepeatedField(proto.STRING, number=31)

    secrets = proto.RepeatedField(proto.MESSAGE, number=32, message="Secret",)

    timing = proto.MapField(proto.STRING, proto.MESSAGE, number=33, message="TimeSpan",)


class Artifacts(proto.Message):
    r"""Artifacts produced by a build that should be uploaded upon
    successful completion of all build steps.

    Attributes:
        images (Sequence[str]):
            A list of images to be pushed upon the
            successful completion of all build steps.

            The images will be pushed using the builder
            service account's credentials.
            The digests of the pushed images will be stored
            in the Build resource's results field.

            If any of the images fail to be pushed, the
            build is marked FAILURE.
        objects (~.cloudbuild.Artifacts.ArtifactObjects):
            A list of objects to be uploaded to Cloud
            Storage upon successful completion of all build
            steps.
            Files in the workspace matching specified paths
            globs will be uploaded to the specified Cloud
            Storage location using the builder service
            account's credentials.

            The location and generation of the uploaded
            objects will be stored in the Build resource's
            results field.

            If any objects fail to be pushed, the build is
            marked FAILURE.
    """

    class ArtifactObjects(proto.Message):
        r"""Files in the workspace to upload to Cloud Storage upon
        successful completion of all build steps.

        Attributes:
            location (str):
                Cloud Storage bucket and optional object path, in the form
                "gs://bucket/path/to/somewhere/". (see `Bucket Name
                Requirements <https://cloud.google.com/storage/docs/bucket-naming#requirements>`__).

                Files in the workspace matching any path pattern will be
                uploaded to Cloud Storage with this location as a prefix.
            paths (Sequence[str]):
                Path globs used to match files in the build's
                workspace.
            timing (~.cloudbuild.TimeSpan):
                Output only. Stores timing information for
                pushing all artifact objects.
        """

        location = proto.Field(proto.STRING, number=1)

        paths = proto.RepeatedField(proto.STRING, number=2)

        timing = proto.Field(proto.MESSAGE, number=3, message="TimeSpan",)

    images = proto.RepeatedField(proto.STRING, number=1)

    objects = proto.Field(proto.MESSAGE, number=2, message=ArtifactObjects,)


class TimeSpan(proto.Message):
    r"""Start and end times for a build execution phase.

    Attributes:
        start_time (~.timestamp.Timestamp):
            Start of time span.
        end_time (~.timestamp.Timestamp):
            End of time span.
    """

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)


class BuildOperationMetadata(proto.Message):
    r"""Metadata for build operations.

    Attributes:
        build (~.cloudbuild.Build):
            The build that the operation is tracking.
    """

    build = proto.Field(proto.MESSAGE, number=1, message=Build,)


class SourceProvenance(proto.Message):
    r"""Provenance of the source. Ways to find the original source,
    or verify that some source was used for this build.

    Attributes:
        resolved_storage_source (~.cloudbuild.StorageSource):
            A copy of the build's ``source.storage_source``, if exists,
            with any generations resolved.
        resolved_repo_source (~.cloudbuild.RepoSource):
            A copy of the build's ``source.repo_source``, if exists,
            with any revisions resolved.
        file_hashes (Sequence[~.cloudbuild.SourceProvenance.FileHashesEntry]):
            Output only. Hash(es) of the build source, which can be used
            to verify that the original source integrity was maintained
            in the build. Note that ``FileHashes`` will only be
            populated if ``BuildOptions`` has requested a
            ``SourceProvenanceHash``.

            The keys to this map are file paths used as build source and
            the values contain the hash values for those files.

            If the build source came in a single package such as a
            gzipped tarfile (``.tar.gz``), the ``FileHash`` will be for
            the single path to that file.
    """

    resolved_storage_source = proto.Field(
        proto.MESSAGE, number=3, message=StorageSource,
    )

    resolved_repo_source = proto.Field(proto.MESSAGE, number=6, message=RepoSource,)

    file_hashes = proto.MapField(
        proto.STRING, proto.MESSAGE, number=4, message="FileHashes",
    )


class FileHashes(proto.Message):
    r"""Container message for hashes of byte content of files, used
    in SourceProvenance messages to verify integrity of source input
    to the build.

    Attributes:
        file_hash (Sequence[~.cloudbuild.Hash]):
            Collection of file hashes.
    """

    file_hash = proto.RepeatedField(proto.MESSAGE, number=1, message="Hash",)


class Hash(proto.Message):
    r"""Container message for hash values.

    Attributes:
        type (~.cloudbuild.Hash.HashType):
            The type of hash that was performed.
        value (bytes):
            The hash value.
    """

    class HashType(proto.Enum):
        r"""Specifies the hash algorithm, if any."""
        NONE = 0
        SHA256 = 1
        MD5 = 2

    type = proto.Field(proto.ENUM, number=1, enum=HashType,)

    value = proto.Field(proto.BYTES, number=2)


class Secret(proto.Message):
    r"""Pairs a set of secret environment variables containing
    encrypted values with the Cloud KMS key to use to decrypt the
    value.

    Attributes:
        kms_key_name (str):
            Cloud KMS key name to use to decrypt these
            envs.
        secret_env (Sequence[~.cloudbuild.Secret.SecretEnvEntry]):
            Map of environment variable name to its
            encrypted value.
            Secret environment variables must be unique
            across all of a build's secrets, and must be
            used by at least one build step. Values can be
            at most 64 KB in size. There can be at most 100
            secret values across all of a build's secrets.
    """

    kms_key_name = proto.Field(proto.STRING, number=1)

    secret_env = proto.MapField(proto.STRING, proto.BYTES, number=3)


class CreateBuildRequest(proto.Message):
    r"""Request to create a new build.

    Attributes:
        project_id (str):
            Required. ID of the project.
        build (~.cloudbuild.Build):
            Required. Build resource to create.
    """

    project_id = proto.Field(proto.STRING, number=1)

    build = proto.Field(proto.MESSAGE, number=2, message=Build,)


class GetBuildRequest(proto.Message):
    r"""Request to get a build.

    Attributes:
        project_id (str):
            Required. ID of the project.
        id (str):
            Required. ID of the build.
    """

    project_id = proto.Field(proto.STRING, number=1)

    id = proto.Field(proto.STRING, number=2)


class ListBuildsRequest(proto.Message):
    r"""Request to list builds.

    Attributes:
        project_id (str):
            Required. ID of the project.
        page_size (int):
            Number of results to return in the list.
        page_token (str):
            Token to provide to skip to a particular spot
            in the list.
        filter (str):
            The raw filter text to constrain the results.
    """

    project_id = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)

    filter = proto.Field(proto.STRING, number=8)


class ListBuildsResponse(proto.Message):
    r"""Response including listed builds.

    Attributes:
        builds (Sequence[~.cloudbuild.Build]):
            Builds will be sorted by ``create_time``, descending.
        next_page_token (str):
            Token to receive the next page of results.
    """

    @property
    def raw_page(self):
        return self

    builds = proto.RepeatedField(proto.MESSAGE, number=1, message=Build,)

    next_page_token = proto.Field(proto.STRING, number=2)


class CancelBuildRequest(proto.Message):
    r"""Request to cancel an ongoing build.

    Attributes:
        project_id (str):
            Required. ID of the project.
        id (str):
            Required. ID of the build.
    """

    project_id = proto.Field(proto.STRING, number=1)

    id = proto.Field(proto.STRING, number=2)


class BuildTrigger(proto.Message):
    r"""Configuration for an automated build in response to source
    repository changes.

    Attributes:
        id (str):
            Output only. Unique identifier of the
            trigger.
        description (str):
            Human-readable description of this trigger.
        name (str):
            User-assigned name of the trigger. Must be
            unique within the project. Trigger names must
            meet the following requirements:
            + They must contain only alphanumeric characters
            and dashes. + They can be 1-64 characters long.
            + They must begin and end with an alphanumeric
            character.
        tags (Sequence[str]):
            Tags for annotation of a ``BuildTrigger``
        trigger_template (~.cloudbuild.RepoSource):
            Template describing the types of source changes to trigger a
            build.

            Branch and tag names in trigger templates are interpreted as
            regular expressions. Any branch or tag change that matches
            that regular expression will trigger a build.

            Mutually exclusive with ``github``.
        github (~.cloudbuild.GitHubEventsConfig):
            GitHubEventsConfig describes the configuration of a trigger
            that creates a build whenever a GitHub event is received.

            Mutually exclusive with ``trigger_template``.
        build (~.cloudbuild.Build):
            Contents of the build template.
        filename (str):
            Path, from the source root, to a file whose
            contents is used for the template.
        create_time (~.timestamp.Timestamp):
            Output only. Time when the trigger was
            created.
        disabled (bool):
            If true, the trigger will never result in a
            build.
        substitutions (Sequence[~.cloudbuild.BuildTrigger.SubstitutionsEntry]):
            Substitutions for Build resource. The keys must match the
            following regular expression: ``^_[A-Z0-9_]+$``.The keys
            cannot conflict with the keys in bindings.
        ignored_files (Sequence[str]):
            ignored_files and included_files are file glob matches using
            https://golang.org/pkg/path/filepath/#Match extended with
            support for "**".

            If ignored_files and changed files are both empty, then they
            are not used to determine whether or not to trigger a build.

            If ignored_files is not empty, then we ignore any files that
            match any of the ignored_file globs. If the change has no
            files that are outside of the ignored_files globs, then we
            do not trigger a build.
        included_files (Sequence[str]):
            If any of the files altered in the commit pass the
            ignored_files filter and included_files is empty, then as
            far as this filter is concerned, we should trigger the
            build.

            If any of the files altered in the commit pass the
            ignored_files filter and included_files is not empty, then
            we make sure that at least one of those files matches a
            included_files glob. If not, then we do not trigger a build.
    """

    id = proto.Field(proto.STRING, number=1)

    description = proto.Field(proto.STRING, number=10)

    name = proto.Field(proto.STRING, number=21)

    tags = proto.RepeatedField(proto.STRING, number=19)

    trigger_template = proto.Field(proto.MESSAGE, number=7, message=RepoSource,)

    github = proto.Field(proto.MESSAGE, number=13, message="GitHubEventsConfig",)

    build = proto.Field(proto.MESSAGE, number=4, oneof="build_template", message=Build,)

    filename = proto.Field(proto.STRING, number=8, oneof="build_template")

    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)

    disabled = proto.Field(proto.BOOL, number=9)

    substitutions = proto.MapField(proto.STRING, proto.STRING, number=11)

    ignored_files = proto.RepeatedField(proto.STRING, number=15)

    included_files = proto.RepeatedField(proto.STRING, number=16)


class GitHubEventsConfig(proto.Message):
    r"""GitHubEventsConfig describes the configuration of a trigger
    that creates a build whenever a GitHub event is received.
    This message is experimental.

    Attributes:
        installation_id (int):
            The installationID that emits the GitHub
            event.
        owner (str):
            Owner of the repository. For example: The
            owner for
            https://github.com/googlecloudplatform/cloud-
            builders is "googlecloudplatform".
        name (str):
            Name of the repository. For example: The name
            for
            https://github.com/googlecloudplatform/cloud-
            builders is "cloud-builders".
        pull_request (~.cloudbuild.PullRequestFilter):
            filter to match changes in pull requests.
        push (~.cloudbuild.PushFilter):
            filter to match changes in refs like
            branches, tags.
    """

    installation_id = proto.Field(proto.INT64, number=1)

    owner = proto.Field(proto.STRING, number=6)

    name = proto.Field(proto.STRING, number=7)

    pull_request = proto.Field(
        proto.MESSAGE, number=4, oneof="event", message="PullRequestFilter",
    )

    push = proto.Field(proto.MESSAGE, number=5, oneof="event", message="PushFilter",)


class PullRequestFilter(proto.Message):
    r"""PullRequestFilter contains filter properties for matching
    GitHub Pull Requests.

    Attributes:
        branch (str):
            Regex of branches to match.
            The syntax of the regular expressions accepted
            is the syntax accepted by RE2 and described at
            https://github.com/google/re2/wiki/Syntax
        comment_control (~.cloudbuild.PullRequestFilter.CommentControl):
            Whether to block builds on a "/gcbrun"
            comment from a repository admin or collaborator.
        invert_regex (bool):
            If true, branches that do NOT match the git_ref will trigger
            a build.
    """

    class CommentControl(proto.Enum):
        r"""Controls behavior of Pull Request comments."""
        COMMENTS_DISABLED = 0
        COMMENTS_ENABLED = 1

    branch = proto.Field(proto.STRING, number=2, oneof="git_ref")

    comment_control = proto.Field(proto.ENUM, number=5, enum=CommentControl,)

    invert_regex = proto.Field(proto.BOOL, number=6)


class PushFilter(proto.Message):
    r"""Push contains filter properties for matching GitHub git
    pushes.

    Attributes:
        branch (str):
            Regexes matching branches to build.
            The syntax of the regular expressions accepted
            is the syntax accepted by RE2 and described at
            https://github.com/google/re2/wiki/Syntax
        tag (str):
            Regexes matching tags to build.
            The syntax of the regular expressions accepted
            is the syntax accepted by RE2 and described at
            https://github.com/google/re2/wiki/Syntax
        invert_regex (bool):
            When true, only trigger a build if the revision regex does
            NOT match the git_ref regex.
    """

    branch = proto.Field(proto.STRING, number=2, oneof="git_ref")

    tag = proto.Field(proto.STRING, number=3, oneof="git_ref")

    invert_regex = proto.Field(proto.BOOL, number=4)


class CreateBuildTriggerRequest(proto.Message):
    r"""Request to create a new ``BuildTrigger``.

    Attributes:
        project_id (str):
            Required. ID of the project for which to
            configure automatic builds.
        trigger (~.cloudbuild.BuildTrigger):
            Required. ``BuildTrigger`` to create.
    """

    project_id = proto.Field(proto.STRING, number=1)

    trigger = proto.Field(proto.MESSAGE, number=2, message=BuildTrigger,)


class GetBuildTriggerRequest(proto.Message):
    r"""Returns the ``BuildTrigger`` with the specified ID.

    Attributes:
        project_id (str):
            Required. ID of the project that owns the
            trigger.
        trigger_id (str):
            Required. Identifier (``id`` or ``name``) of the
            ``BuildTrigger`` to get.
    """

    project_id = proto.Field(proto.STRING, number=1)

    trigger_id = proto.Field(proto.STRING, number=2)


class ListBuildTriggersRequest(proto.Message):
    r"""Request to list existing ``BuildTriggers``.

    Attributes:
        project_id (str):
            Required. ID of the project for which to list
            BuildTriggers.
        page_size (int):
            Number of results to return in the list.
        page_token (str):
            Token to provide to skip to a particular spot
            in the list.
    """

    project_id = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListBuildTriggersResponse(proto.Message):
    r"""Response containing existing ``BuildTriggers``.

    Attributes:
        triggers (Sequence[~.cloudbuild.BuildTrigger]):
            ``BuildTriggers`` for the project, sorted by ``create_time``
            descending.
        next_page_token (str):
            Token to receive the next page of results.
    """

    @property
    def raw_page(self):
        return self

    triggers = proto.RepeatedField(proto.MESSAGE, number=1, message=BuildTrigger,)

    next_page_token = proto.Field(proto.STRING, number=2)


class DeleteBuildTriggerRequest(proto.Message):
    r"""Request to delete a ``BuildTrigger``.

    Attributes:
        project_id (str):
            Required. ID of the project that owns the
            trigger.
        trigger_id (str):
            Required. ID of the ``BuildTrigger`` to delete.
    """

    project_id = proto.Field(proto.STRING, number=1)

    trigger_id = proto.Field(proto.STRING, number=2)


class UpdateBuildTriggerRequest(proto.Message):
    r"""Request to update an existing ``BuildTrigger``.

    Attributes:
        project_id (str):
            Required. ID of the project that owns the
            trigger.
        trigger_id (str):
            Required. ID of the ``BuildTrigger`` to update.
        trigger (~.cloudbuild.BuildTrigger):
            Required. ``BuildTrigger`` to update.
    """

    project_id = proto.Field(proto.STRING, number=1)

    trigger_id = proto.Field(proto.STRING, number=2)

    trigger = proto.Field(proto.MESSAGE, number=3, message=BuildTrigger,)


class BuildOptions(proto.Message):
    r"""Optional arguments to enable specific features of builds.

    Attributes:
        source_provenance_hash (Sequence[~.cloudbuild.Hash.HashType]):
            Requested hash for SourceProvenance.
        requested_verify_option (~.cloudbuild.BuildOptions.VerifyOption):
            Requested verifiability options.
        machine_type (~.cloudbuild.BuildOptions.MachineType):
            Compute Engine machine type on which to run
            the build.
        disk_size_gb (int):
            Requested disk size for the VM that runs the build. Note
            that this is *NOT* "disk free"; some of the space will be
            used by the operating system and build utilities. Also note
            that this is the minimum disk size that will be allocated
            for the build -- the build may run with a larger disk than
            requested. At present, the maximum disk size is 1000GB;
            builds that request more than the maximum are rejected with
            an error.
        substitution_option (~.cloudbuild.BuildOptions.SubstitutionOption):
            Option to specify behavior when there is an
            error in the substitution checks.
        log_streaming_option (~.cloudbuild.BuildOptions.LogStreamingOption):
            Option to define build log streaming behavior
            to Google Cloud Storage.
        worker_pool (str):
            Option to specify a ``WorkerPool`` for the build. Format:
            projects/{project}/workerPools/{workerPool}

            This field is experimental.
        logging (~.cloudbuild.BuildOptions.LoggingMode):
            Option to specify the logging mode, which
            determines where the logs are stored.
        env (Sequence[str]):
            A list of global environment variable
            definitions that will exist for all build steps
            in this build. If a variable is defined in both
            globally and in a build step, the variable will
            use the build step value.
            The elements are of the form "KEY=VALUE" for the
            environment variable "KEY" being given the value
            "VALUE".
        secret_env (Sequence[str]):
            A list of global environment variables, which are encrypted
            using a Cloud Key Management Service crypto key. These
            values must be specified in the build's ``Secret``. These
            variables will be available to all build steps in this
            build.
        volumes (Sequence[~.cloudbuild.Volume]):
            Global list of volumes to mount for ALL build
            steps
            Each volume is created as an empty volume prior
            to starting the build process. Upon completion
            of the build, volumes and their contents are
            discarded. Global volume names and paths cannot
            conflict with the volumes defined a build step.

            Using a global volume in a build with only one
            step is not valid as it is indicative of a build
            request with an incorrect configuration.
    """

    class VerifyOption(proto.Enum):
        r"""Specifies the manner in which the build should be verified,
        if at all.
        """
        NOT_VERIFIED = 0
        VERIFIED = 1

    class MachineType(proto.Enum):
        r"""Supported VM sizes."""
        UNSPECIFIED = 0
        N1_HIGHCPU_8 = 1
        N1_HIGHCPU_32 = 2

    class SubstitutionOption(proto.Enum):
        r"""Specifies the behavior when there is an error in the
        substitution checks.
        """
        MUST_MATCH = 0
        ALLOW_LOOSE = 1

    class LogStreamingOption(proto.Enum):
        r"""Specifies the behavior when writing build logs to Google
        Cloud Storage.
        """
        STREAM_DEFAULT = 0
        STREAM_ON = 1
        STREAM_OFF = 2

    class LoggingMode(proto.Enum):
        r"""Specifies the logging mode."""
        LOGGING_UNSPECIFIED = 0
        LEGACY = 1
        GCS_ONLY = 2

    source_provenance_hash = proto.RepeatedField(
        proto.ENUM, number=1, enum=Hash.HashType,
    )

    requested_verify_option = proto.Field(proto.ENUM, number=2, enum=VerifyOption,)

    machine_type = proto.Field(proto.ENUM, number=3, enum=MachineType,)

    disk_size_gb = proto.Field(proto.INT64, number=6)

    substitution_option = proto.Field(proto.ENUM, number=4, enum=SubstitutionOption,)

    log_streaming_option = proto.Field(proto.ENUM, number=5, enum=LogStreamingOption,)

    worker_pool = proto.Field(proto.STRING, number=7)

    logging = proto.Field(proto.ENUM, number=11, enum=LoggingMode,)

    env = proto.RepeatedField(proto.STRING, number=12)

    secret_env = proto.RepeatedField(proto.STRING, number=13)

    volumes = proto.RepeatedField(proto.MESSAGE, number=14, message=Volume,)


class WorkerPool(proto.Message):
    r"""Configuration for a WorkerPool to run the builds.
    Workers are machines that Cloud Build uses to run your builds.
    By default, all workers run in a project owned by Cloud Build.
    To have full control over the workers that execute your builds
    -- such as enabling them to access private resources on your
    private network -- you can request Cloud Build to run the
    workers in your own project by creating a custom workers pool.

    Attributes:
        name (str):
            User-defined name of the ``WorkerPool``.
        project_id (str):
            The project ID of the GCP project for which the
            ``WorkerPool`` is created.
        service_account_email (str):
            Output only. The service account used to manage the
            ``WorkerPool``. The service account must have the Compute
            Instance Admin (Beta) permission at the project level.
        worker_count (int):
            Total number of workers to be created across
            all requested regions.
        worker_config (~.cloudbuild.WorkerConfig):
            Configuration to be used for a creating workers in the
            ``WorkerPool``.
        regions (Sequence[~.cloudbuild.WorkerPool.Region]):
            List of regions to create the ``WorkerPool``. Regions can't
            be empty. If Cloud Build adds a new GCP region in the
            future, the existing ``WorkerPool`` will not be enabled in
            the new region automatically; you must add the new region to
            the ``regions`` field to enable the ``WorkerPool`` in that
            region.
        create_time (~.timestamp.Timestamp):
            Output only. Time at which the request to create the
            ``WorkerPool`` was received.
        update_time (~.timestamp.Timestamp):
            Output only. Time at which the request to update the
            ``WorkerPool`` was received.
        delete_time (~.timestamp.Timestamp):
            Output only. Time at which the request to delete the
            ``WorkerPool`` was received.
        status (~.cloudbuild.WorkerPool.Status):
            Output only. WorkerPool Status.
    """

    class Region(proto.Enum):
        r"""Supported GCP regions to create the ``WorkerPool``."""
        REGION_UNSPECIFIED = 0
        US_CENTRAL1 = 1
        US_WEST1 = 2
        US_EAST1 = 3
        US_EAST4 = 4

    class Status(proto.Enum):
        r"""``WorkerPool`` status"""
        STATUS_UNSPECIFIED = 0
        CREATING = 1
        RUNNING = 2
        DELETING = 3
        DELETED = 4

    name = proto.Field(proto.STRING, number=14)

    project_id = proto.Field(proto.STRING, number=2)

    service_account_email = proto.Field(proto.STRING, number=3)

    worker_count = proto.Field(proto.INT64, number=4)

    worker_config = proto.Field(proto.MESSAGE, number=16, message="WorkerConfig",)

    regions = proto.RepeatedField(proto.ENUM, number=9, enum=Region,)

    create_time = proto.Field(proto.MESSAGE, number=11, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=17, message=timestamp.Timestamp,)

    delete_time = proto.Field(proto.MESSAGE, number=12, message=timestamp.Timestamp,)

    status = proto.Field(proto.ENUM, number=13, enum=Status,)


class WorkerConfig(proto.Message):
    r"""WorkerConfig defines the configuration to be used for a
    creating workers in the pool.

    Attributes:
        machine_type (str):
            Machine Type of the worker, such as n1-standard-1. See
            https://cloud.google.com/compute/docs/machine-types. If left
            blank, Cloud Build will use a standard unspecified machine
            to create the worker pool. ``machine_type`` is overridden if
            you specify a different machine type in ``build_options``.
            In this case, the VM specified in the ``build_options`` will
            be created on demand at build time. For more information see
            https://cloud.google.com/cloud-build/docs/speeding-up-builds#using_custom_virtual_machine_sizes
        disk_size_gb (int):
            Size of the disk attached to the worker, in GB. See
            https://cloud.google.com/compute/docs/disks/ If ``0`` is
            specified, Cloud Build will use a standard disk size.
            ``disk_size`` is overridden if you specify a different disk
            size in ``build_options``. In this case, a VM with a disk
            size specified in the ``build_options`` will be created on
            demand at build time. For more information see
            https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.builds#buildoptions
        network (~.cloudbuild.Network):
            The network definition used to create the worker. If this
            section is left empty, the workers will be created in
            WorkerPool.project_id on the default network.
        tag (str):
            The tag applied to the worker, and the same tag used by the
            firewall rule. It is used to identify the Cloud Build
            workers among other VMs. The default value for tag is
            ``worker``.
    """

    machine_type = proto.Field(proto.STRING, number=1)

    disk_size_gb = proto.Field(proto.INT64, number=2)

    network = proto.Field(proto.MESSAGE, number=3, message="Network",)

    tag = proto.Field(proto.STRING, number=4)


class Network(proto.Message):
    r"""Network describes the GCP network used to create workers in.

    Attributes:
        project_id (str):
            Project id containing the defined network and subnetwork.
            For a peered VPC, this will be the same as the project_id in
            which the workers are created. For a shared VPC, this will
            be the project sharing the network with the project_id
            project in which workers will be created. For custom workers
            with no VPC, this will be the same as project_id.
        network (str):
            Network on which the workers are created.
            "default" network is used if empty.
        subnetwork (str):
            Subnetwork on which the workers are created.
            "default" subnetwork is used if empty.
    """

    project_id = proto.Field(proto.STRING, number=1)

    network = proto.Field(proto.STRING, number=2)

    subnetwork = proto.Field(proto.STRING, number=3)


class CreateWorkerPoolRequest(proto.Message):
    r"""Request to create a new ``WorkerPool``.

    Attributes:
        parent (str):
            ID of the parent project.
        worker_pool (~.cloudbuild.WorkerPool):
            ``WorkerPool`` resource to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    worker_pool = proto.Field(proto.MESSAGE, number=2, message=WorkerPool,)


class GetWorkerPoolRequest(proto.Message):
    r"""Request to get a ``WorkerPool`` with the specified name.

    Attributes:
        name (str):
            The field will contain name of the resource
            requested, for example:
            "projects/project-1/workerPools/workerpool-name".
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteWorkerPoolRequest(proto.Message):
    r"""Request to delete a ``WorkerPool``.

    Attributes:
        name (str):
            The field will contain name of the resource
            requested, for example:
            "projects/project-1/workerPools/workerpool-name".
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateWorkerPoolRequest(proto.Message):
    r"""Request to update a ``WorkerPool``.

    Attributes:
        name (str):
            The field will contain name of the resource
            requested, for example:
            "projects/project-1/workerPools/workerpool-name".
        worker_pool (~.cloudbuild.WorkerPool):
            ``WorkerPool`` resource to update.
    """

    name = proto.Field(proto.STRING, number=2)

    worker_pool = proto.Field(proto.MESSAGE, number=3, message=WorkerPool,)


class ListWorkerPoolsRequest(proto.Message):
    r"""Request to list ``WorkerPools``.

    Attributes:
        parent (str):
            ID of the parent project.
    """

    parent = proto.Field(proto.STRING, number=1)


class ListWorkerPoolsResponse(proto.Message):
    r"""Response containing existing ``WorkerPools``.

    Attributes:
        worker_pools (Sequence[~.cloudbuild.WorkerPool]):
            ``WorkerPools`` for the project.
    """

    worker_pools = proto.RepeatedField(proto.MESSAGE, number=1, message=WorkerPool,)


__all__ = tuple(sorted(__protobuf__.manifest))
