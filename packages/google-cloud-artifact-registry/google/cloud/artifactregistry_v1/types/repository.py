# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.devtools.artifactregistry.v1",
    manifest={
        "UpstreamPolicy",
        "CleanupPolicyCondition",
        "CleanupPolicyMostRecentVersions",
        "CleanupPolicy",
        "VirtualRepositoryConfig",
        "RemoteRepositoryConfig",
        "Repository",
        "ListRepositoriesRequest",
        "ListRepositoriesResponse",
        "GetRepositoryRequest",
        "CreateRepositoryRequest",
        "UpdateRepositoryRequest",
        "DeleteRepositoryRequest",
    },
)


class UpstreamPolicy(proto.Message):
    r"""Artifact policy configuration for the repository contents.

    Attributes:
        id (str):
            The user-provided ID of the upstream policy.
        repository (str):
            A reference to the repository resource, for example:
            ``projects/p1/locations/us-central1/repositories/repo1``.
        priority (int):
            Entries with a greater priority value take
            precedence in the pull order.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    repository: str = proto.Field(
        proto.STRING,
        number=2,
    )
    priority: int = proto.Field(
        proto.INT32,
        number=3,
    )


class CleanupPolicyCondition(proto.Message):
    r"""CleanupPolicyCondition is a set of conditions attached to a
    CleanupPolicy. If multiple entries are set, all must be
    satisfied for the condition to be satisfied.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        tag_state (google.cloud.artifactregistry_v1.types.CleanupPolicyCondition.TagState):
            Match versions by tag status.

            This field is a member of `oneof`_ ``_tag_state``.
        tag_prefixes (MutableSequence[str]):
            Match versions by tag prefix. Applied on any
            prefix match.
        version_name_prefixes (MutableSequence[str]):
            Match versions by version name prefix.
            Applied on any prefix match.
        package_name_prefixes (MutableSequence[str]):
            Match versions by package prefix. Applied on
            any prefix match.
        older_than (google.protobuf.duration_pb2.Duration):
            Match versions older than a duration.

            This field is a member of `oneof`_ ``_older_than``.
        newer_than (google.protobuf.duration_pb2.Duration):
            Match versions newer than a duration.

            This field is a member of `oneof`_ ``_newer_than``.
    """

    class TagState(proto.Enum):
        r"""Statuses applying to versions.

        Values:
            TAG_STATE_UNSPECIFIED (0):
                Tag status not specified.
            TAGGED (1):
                Applies to tagged versions only.
            UNTAGGED (2):
                Applies to untagged versions only.
            ANY (3):
                Applies to all versions.
        """
        TAG_STATE_UNSPECIFIED = 0
        TAGGED = 1
        UNTAGGED = 2
        ANY = 3

    tag_state: TagState = proto.Field(
        proto.ENUM,
        number=2,
        optional=True,
        enum=TagState,
    )
    tag_prefixes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    version_name_prefixes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    package_name_prefixes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    older_than: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=6,
        optional=True,
        message=duration_pb2.Duration,
    )
    newer_than: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=7,
        optional=True,
        message=duration_pb2.Duration,
    )


class CleanupPolicyMostRecentVersions(proto.Message):
    r"""CleanupPolicyMostRecentVersions is an alternate condition of
    a CleanupPolicy for retaining a minimum number of versions.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        package_name_prefixes (MutableSequence[str]):
            List of package name prefixes that will apply
            this rule.
        keep_count (int):
            Minimum number of versions to keep.

            This field is a member of `oneof`_ ``_keep_count``.
    """

    package_name_prefixes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    keep_count: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )


class CleanupPolicy(proto.Message):
    r"""Artifact policy configuration for repository cleanup
    policies.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        condition (google.cloud.artifactregistry_v1.types.CleanupPolicyCondition):
            Policy condition for matching versions.

            This field is a member of `oneof`_ ``condition_type``.
        most_recent_versions (google.cloud.artifactregistry_v1.types.CleanupPolicyMostRecentVersions):
            Policy condition for retaining a minimum
            number of versions. May only be specified with a
            Keep action.

            This field is a member of `oneof`_ ``condition_type``.
        id (str):
            The user-provided ID of the cleanup policy.
        action (google.cloud.artifactregistry_v1.types.CleanupPolicy.Action):
            Policy action.
    """

    class Action(proto.Enum):
        r"""Action type for a cleanup policy.

        Values:
            ACTION_UNSPECIFIED (0):
                Action not specified.
            DELETE (1):
                Delete action.
            KEEP (2):
                Keep action.
        """
        ACTION_UNSPECIFIED = 0
        DELETE = 1
        KEEP = 2

    condition: "CleanupPolicyCondition" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="condition_type",
        message="CleanupPolicyCondition",
    )
    most_recent_versions: "CleanupPolicyMostRecentVersions" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="condition_type",
        message="CleanupPolicyMostRecentVersions",
    )
    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    action: Action = proto.Field(
        proto.ENUM,
        number=3,
        enum=Action,
    )


class VirtualRepositoryConfig(proto.Message):
    r"""Virtual repository configuration.

    Attributes:
        upstream_policies (MutableSequence[google.cloud.artifactregistry_v1.types.UpstreamPolicy]):
            Policies that configure the upstream
            artifacts distributed by the Virtual Repository.
            Upstream policies cannot be set on a standard
            repository.
    """

    upstream_policies: MutableSequence["UpstreamPolicy"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="UpstreamPolicy",
    )


class RemoteRepositoryConfig(proto.Message):
    r"""Remote repository configuration.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        docker_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.DockerRepository):
            Specific settings for a Docker remote
            repository.

            This field is a member of `oneof`_ ``remote_source``.
        maven_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.MavenRepository):
            Specific settings for a Maven remote
            repository.

            This field is a member of `oneof`_ ``remote_source``.
        npm_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.NpmRepository):
            Specific settings for an Npm remote
            repository.

            This field is a member of `oneof`_ ``remote_source``.
        python_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.PythonRepository):
            Specific settings for a Python remote
            repository.

            This field is a member of `oneof`_ ``remote_source``.
        apt_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.AptRepository):
            Specific settings for an Apt remote
            repository.

            This field is a member of `oneof`_ ``remote_source``.
        yum_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.YumRepository):
            Specific settings for a Yum remote
            repository.

            This field is a member of `oneof`_ ``remote_source``.
        description (str):
            The description of the remote source.
        upstream_credentials (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.UpstreamCredentials):
            Optional. The credentials used to access the
            remote repository.
    """

    class UpstreamCredentials(proto.Message):
        r"""The credentials to access the remote repository.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            username_password_credentials (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.UpstreamCredentials.UsernamePasswordCredentials):
                Use username and password to access the
                remote repository.

                This field is a member of `oneof`_ ``credentials``.
        """

        class UsernamePasswordCredentials(proto.Message):
            r"""Username and password credentials.

            Attributes:
                username (str):
                    The username to access the remote repository.
                password_secret_version (str):
                    The Secret Manager key version that holds the password to
                    access the remote repository. Must be in the format of
                    ``projects/{project}/secrets/{secret}/versions/{version}``.
            """

            username: str = proto.Field(
                proto.STRING,
                number=1,
            )
            password_secret_version: str = proto.Field(
                proto.STRING,
                number=2,
            )

        username_password_credentials: "RemoteRepositoryConfig.UpstreamCredentials.UsernamePasswordCredentials" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="credentials",
            message="RemoteRepositoryConfig.UpstreamCredentials.UsernamePasswordCredentials",
        )

    class DockerRepository(proto.Message):
        r"""Configuration for a Docker remote repository.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            public_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.DockerRepository.PublicRepository):
                One of the publicly available Docker
                repositories supported by Artifact Registry.

                This field is a member of `oneof`_ ``upstream``.
        """

        class PublicRepository(proto.Enum):
            r"""Predefined list of publicly available Docker repositories
            like Docker Hub.

            Values:
                PUBLIC_REPOSITORY_UNSPECIFIED (0):
                    Unspecified repository.
                DOCKER_HUB (1):
                    Docker Hub.
            """
            PUBLIC_REPOSITORY_UNSPECIFIED = 0
            DOCKER_HUB = 1

        public_repository: "RemoteRepositoryConfig.DockerRepository.PublicRepository" = proto.Field(
            proto.ENUM,
            number=1,
            oneof="upstream",
            enum="RemoteRepositoryConfig.DockerRepository.PublicRepository",
        )

    class MavenRepository(proto.Message):
        r"""Configuration for a Maven remote repository.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            public_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.MavenRepository.PublicRepository):
                One of the publicly available Maven
                repositories supported by Artifact Registry.

                This field is a member of `oneof`_ ``upstream``.
        """

        class PublicRepository(proto.Enum):
            r"""Predefined list of publicly available Maven repositories like
            Maven Central.

            Values:
                PUBLIC_REPOSITORY_UNSPECIFIED (0):
                    Unspecified repository.
                MAVEN_CENTRAL (1):
                    Maven Central.
            """
            PUBLIC_REPOSITORY_UNSPECIFIED = 0
            MAVEN_CENTRAL = 1

        public_repository: "RemoteRepositoryConfig.MavenRepository.PublicRepository" = (
            proto.Field(
                proto.ENUM,
                number=1,
                oneof="upstream",
                enum="RemoteRepositoryConfig.MavenRepository.PublicRepository",
            )
        )

    class NpmRepository(proto.Message):
        r"""Configuration for a Npm remote repository.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            public_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.NpmRepository.PublicRepository):
                One of the publicly available Npm
                repositories supported by Artifact Registry.

                This field is a member of `oneof`_ ``upstream``.
        """

        class PublicRepository(proto.Enum):
            r"""Predefined list of publicly available NPM repositories like
            npmjs.

            Values:
                PUBLIC_REPOSITORY_UNSPECIFIED (0):
                    Unspecified repository.
                NPMJS (1):
                    npmjs.
            """
            PUBLIC_REPOSITORY_UNSPECIFIED = 0
            NPMJS = 1

        public_repository: "RemoteRepositoryConfig.NpmRepository.PublicRepository" = (
            proto.Field(
                proto.ENUM,
                number=1,
                oneof="upstream",
                enum="RemoteRepositoryConfig.NpmRepository.PublicRepository",
            )
        )

    class PythonRepository(proto.Message):
        r"""Configuration for a Python remote repository.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            public_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.PythonRepository.PublicRepository):
                One of the publicly available Python
                repositories supported by Artifact Registry.

                This field is a member of `oneof`_ ``upstream``.
        """

        class PublicRepository(proto.Enum):
            r"""Predefined list of publicly available Python repositories
            like PyPI.org.

            Values:
                PUBLIC_REPOSITORY_UNSPECIFIED (0):
                    Unspecified repository.
                PYPI (1):
                    PyPI.
            """
            PUBLIC_REPOSITORY_UNSPECIFIED = 0
            PYPI = 1

        public_repository: "RemoteRepositoryConfig.PythonRepository.PublicRepository" = proto.Field(
            proto.ENUM,
            number=1,
            oneof="upstream",
            enum="RemoteRepositoryConfig.PythonRepository.PublicRepository",
        )

    class AptRepository(proto.Message):
        r"""Configuration for an Apt remote repository.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            public_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.AptRepository.PublicRepository):
                One of the publicly available Apt
                repositories supported by Artifact Registry.

                This field is a member of `oneof`_ ``upstream``.
        """

        class PublicRepository(proto.Message):
            r"""Publicly available Apt repositories constructed from a common
            repository base and a custom repository path.

            Attributes:
                repository_base (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.AptRepository.PublicRepository.RepositoryBase):
                    A common public repository base for Apt.
                repository_path (str):
                    A custom field to define a path to a specific
                    repository from the base.
            """

            class RepositoryBase(proto.Enum):
                r"""Predefined list of publicly available repository bases for
                Apt.

                Values:
                    REPOSITORY_BASE_UNSPECIFIED (0):
                        Unspecified repository base.
                    DEBIAN (1):
                        Debian.
                    UBUNTU (2):
                        Ubuntu LTS/Pro.
                """
                REPOSITORY_BASE_UNSPECIFIED = 0
                DEBIAN = 1
                UBUNTU = 2

            repository_base: "RemoteRepositoryConfig.AptRepository.PublicRepository.RepositoryBase" = proto.Field(
                proto.ENUM,
                number=1,
                enum="RemoteRepositoryConfig.AptRepository.PublicRepository.RepositoryBase",
            )
            repository_path: str = proto.Field(
                proto.STRING,
                number=2,
            )

        public_repository: "RemoteRepositoryConfig.AptRepository.PublicRepository" = (
            proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="upstream",
                message="RemoteRepositoryConfig.AptRepository.PublicRepository",
            )
        )

    class YumRepository(proto.Message):
        r"""Configuration for a Yum remote repository.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            public_repository (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.YumRepository.PublicRepository):
                One of the publicly available Yum
                repositories supported by Artifact Registry.

                This field is a member of `oneof`_ ``upstream``.
        """

        class PublicRepository(proto.Message):
            r"""Publicly available Yum repositories constructed from a common
            repository base and a custom repository path.

            Attributes:
                repository_base (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig.YumRepository.PublicRepository.RepositoryBase):
                    A common public repository base for Yum.
                repository_path (str):
                    A custom field to define a path to a specific
                    repository from the base.
            """

            class RepositoryBase(proto.Enum):
                r"""Predefined list of publicly available repository bases for
                Yum.

                Values:
                    REPOSITORY_BASE_UNSPECIFIED (0):
                        Unspecified repository base.
                    CENTOS (1):
                        CentOS.
                    CENTOS_DEBUG (2):
                        CentOS Debug.
                    CENTOS_VAULT (3):
                        CentOS Vault.
                    CENTOS_STREAM (4):
                        CentOS Stream.
                    ROCKY (5):
                        Rocky.
                    EPEL (6):
                        Fedora Extra Packages for Enterprise Linux
                        (EPEL).
                """
                REPOSITORY_BASE_UNSPECIFIED = 0
                CENTOS = 1
                CENTOS_DEBUG = 2
                CENTOS_VAULT = 3
                CENTOS_STREAM = 4
                ROCKY = 5
                EPEL = 6

            repository_base: "RemoteRepositoryConfig.YumRepository.PublicRepository.RepositoryBase" = proto.Field(
                proto.ENUM,
                number=1,
                enum="RemoteRepositoryConfig.YumRepository.PublicRepository.RepositoryBase",
            )
            repository_path: str = proto.Field(
                proto.STRING,
                number=2,
            )

        public_repository: "RemoteRepositoryConfig.YumRepository.PublicRepository" = (
            proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="upstream",
                message="RemoteRepositoryConfig.YumRepository.PublicRepository",
            )
        )

    docker_repository: DockerRepository = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="remote_source",
        message=DockerRepository,
    )
    maven_repository: MavenRepository = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="remote_source",
        message=MavenRepository,
    )
    npm_repository: NpmRepository = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="remote_source",
        message=NpmRepository,
    )
    python_repository: PythonRepository = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="remote_source",
        message=PythonRepository,
    )
    apt_repository: AptRepository = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="remote_source",
        message=AptRepository,
    )
    yum_repository: YumRepository = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="remote_source",
        message=YumRepository,
    )
    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    upstream_credentials: UpstreamCredentials = proto.Field(
        proto.MESSAGE,
        number=9,
        message=UpstreamCredentials,
    )


class Repository(proto.Message):
    r"""A Repository for storing artifacts with a specific format.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        maven_config (google.cloud.artifactregistry_v1.types.Repository.MavenRepositoryConfig):
            Maven repository config contains repository
            level configuration for the repositories of
            maven type.

            This field is a member of `oneof`_ ``format_config``.
        docker_config (google.cloud.artifactregistry_v1.types.Repository.DockerRepositoryConfig):
            Docker repository config contains repository
            level configuration for the repositories of
            docker type.

            This field is a member of `oneof`_ ``format_config``.
        virtual_repository_config (google.cloud.artifactregistry_v1.types.VirtualRepositoryConfig):
            Configuration specific for a Virtual
            Repository.

            This field is a member of `oneof`_ ``mode_config``.
        remote_repository_config (google.cloud.artifactregistry_v1.types.RemoteRepositoryConfig):
            Configuration specific for a Remote
            Repository.

            This field is a member of `oneof`_ ``mode_config``.
        name (str):
            The name of the repository, for example:
            ``projects/p1/locations/us-central1/repositories/repo1``.
        format_ (google.cloud.artifactregistry_v1.types.Repository.Format):
            Optional. The format of packages that are
            stored in the repository.
        description (str):
            The user-provided description of the
            repository.
        labels (MutableMapping[str, str]):
            Labels with user-defined metadata.
            This field may contain up to 64 entries. Label
            keys and values may be no longer than 63
            characters. Label keys must begin with a
            lowercase letter and may only contain lowercase
            letters, numeric characters, underscores, and
            dashes.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the repository was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the repository was
            last updated.
        kms_key_name (str):
            The Cloud KMS resource name of the customer managed
            encryption key that's used to encrypt the contents of the
            Repository. Has the form:
            ``projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key``.
            This value may not be changed after the Repository has been
            created.
        mode (google.cloud.artifactregistry_v1.types.Repository.Mode):
            Optional. The mode of the repository.
        cleanup_policies (MutableMapping[str, google.cloud.artifactregistry_v1.types.CleanupPolicy]):
            Optional. Cleanup policies for this
            repository. Cleanup policies indicate when
            certain package versions can be automatically
            deleted. Map keys are policy IDs supplied by
            users during policy creation. They must unique
            within a repository and be under 128 characters
            in length.
        size_bytes (int):
            Output only. The size, in bytes, of all
            artifact storage in this repository.
            Repositories that are generally available or in
            public preview  use this to calculate storage
            costs.
        satisfies_pzs (bool):
            Output only. If set, the repository satisfies
            physical zone separation.
        cleanup_policy_dry_run (bool):
            Optional. If true, the cleanup pipeline is
            prevented from deleting versions in this
            repository.
    """

    class Format(proto.Enum):
        r"""A package format.

        Values:
            FORMAT_UNSPECIFIED (0):
                Unspecified package format.
            DOCKER (1):
                Docker package format.
            MAVEN (2):
                Maven package format.
            NPM (3):
                NPM package format.
            APT (5):
                APT package format.
            YUM (6):
                YUM package format.
            PYTHON (8):
                Python package format.
            KFP (9):
                Kubeflow Pipelines package format.
            GO (10):
                Go package format.
        """
        FORMAT_UNSPECIFIED = 0
        DOCKER = 1
        MAVEN = 2
        NPM = 3
        APT = 5
        YUM = 6
        PYTHON = 8
        KFP = 9
        GO = 10

    class Mode(proto.Enum):
        r"""The mode configures the repository to serve artifacts from
        different sources.

        Values:
            MODE_UNSPECIFIED (0):
                Unspecified mode.
            STANDARD_REPOSITORY (1):
                A standard repository storing artifacts.
            VIRTUAL_REPOSITORY (2):
                A virtual repository to serve artifacts from
                one or more sources.
            REMOTE_REPOSITORY (3):
                A remote repository to serve artifacts from a
                remote source.
        """
        MODE_UNSPECIFIED = 0
        STANDARD_REPOSITORY = 1
        VIRTUAL_REPOSITORY = 2
        REMOTE_REPOSITORY = 3

    class MavenRepositoryConfig(proto.Message):
        r"""MavenRepositoryConfig is maven related repository details.
        Provides additional configuration details for repositories of
        the maven format type.

        Attributes:
            allow_snapshot_overwrites (bool):
                The repository with this flag will allow
                publishing the same snapshot versions.
            version_policy (google.cloud.artifactregistry_v1.types.Repository.MavenRepositoryConfig.VersionPolicy):
                Version policy defines the versions that the
                registry will accept.
        """

        class VersionPolicy(proto.Enum):
            r"""VersionPolicy is the version policy for the repository.

            Values:
                VERSION_POLICY_UNSPECIFIED (0):
                    VERSION_POLICY_UNSPECIFIED - the version policy is not
                    defined. When the version policy is not defined, no
                    validation is performed for the versions.
                RELEASE (1):
                    RELEASE - repository will accept only Release
                    versions.
                SNAPSHOT (2):
                    SNAPSHOT - repository will accept only
                    Snapshot versions.
            """
            VERSION_POLICY_UNSPECIFIED = 0
            RELEASE = 1
            SNAPSHOT = 2

        allow_snapshot_overwrites: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        version_policy: "Repository.MavenRepositoryConfig.VersionPolicy" = proto.Field(
            proto.ENUM,
            number=2,
            enum="Repository.MavenRepositoryConfig.VersionPolicy",
        )

    class DockerRepositoryConfig(proto.Message):
        r"""DockerRepositoryConfig is docker related repository details.
        Provides additional configuration details for repositories of
        the docker format type.

        Attributes:
            immutable_tags (bool):
                The repository which enabled this flag
                prevents all tags from being modified, moved or
                deleted. This does not prevent tags from being
                created.
        """

        immutable_tags: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    maven_config: MavenRepositoryConfig = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="format_config",
        message=MavenRepositoryConfig,
    )
    docker_config: DockerRepositoryConfig = proto.Field(
        proto.MESSAGE,
        number=17,
        oneof="format_config",
        message=DockerRepositoryConfig,
    )
    virtual_repository_config: "VirtualRepositoryConfig" = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="mode_config",
        message="VirtualRepositoryConfig",
    )
    remote_repository_config: "RemoteRepositoryConfig" = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="mode_config",
        message="RemoteRepositoryConfig",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    format_: Format = proto.Field(
        proto.ENUM,
        number=2,
        enum=Format,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    kms_key_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    mode: Mode = proto.Field(
        proto.ENUM,
        number=10,
        enum=Mode,
    )
    cleanup_policies: MutableMapping[str, "CleanupPolicy"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=12,
        message="CleanupPolicy",
    )
    size_bytes: int = proto.Field(
        proto.INT64,
        number=13,
    )
    satisfies_pzs: bool = proto.Field(
        proto.BOOL,
        number=16,
    )
    cleanup_policy_dry_run: bool = proto.Field(
        proto.BOOL,
        number=18,
    )


class ListRepositoriesRequest(proto.Message):
    r"""The request to list repositories.

    Attributes:
        parent (str):
            Required. The name of the parent resource
            whose repositories will be listed.
        page_size (int):
            The maximum number of repositories to return.
            Maximum page size is 1,000.
        page_token (str):
            The next_page_token value returned from a previous list
            request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListRepositoriesResponse(proto.Message):
    r"""The response from listing repositories.

    Attributes:
        repositories (MutableSequence[google.cloud.artifactregistry_v1.types.Repository]):
            The repositories returned.
        next_page_token (str):
            The token to retrieve the next page of
            repositories, or empty if there are no more
            repositories to return.
    """

    @property
    def raw_page(self):
        return self

    repositories: MutableSequence["Repository"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Repository",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetRepositoryRequest(proto.Message):
    r"""The request to retrieve a repository.

    Attributes:
        name (str):
            Required. The name of the repository to
            retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateRepositoryRequest(proto.Message):
    r"""The request to create a new repository.

    Attributes:
        parent (str):
            Required. The name of the parent resource
            where the repository will be created.
        repository_id (str):
            Required. The repository id to use for this
            repository.
        repository (google.cloud.artifactregistry_v1.types.Repository):
            Required. The repository to be created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    repository_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    repository: "Repository" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Repository",
    )


class UpdateRepositoryRequest(proto.Message):
    r"""The request to update a repository.

    Attributes:
        repository (google.cloud.artifactregistry_v1.types.Repository):
            The repository that replaces the resource on
            the server.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The update mask applies to the resource. For the
            ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
    """

    repository: "Repository" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Repository",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteRepositoryRequest(proto.Message):
    r"""The request to delete a repository.

    Attributes:
        name (str):
            Required. The name of the repository to
            delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
