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


__protobuf__ = proto.module(
    package="google.cloud.osconfig.v1alpha", manifest={"OSPolicy",},
)


class OSPolicy(proto.Message):
    r"""An OS policy defines the desired state configuration for a
    VM.

    Attributes:
        id (str):
            Required. The id of the OS policy with the following
            restrictions:

            -  Must contain only lowercase letters, numbers, and
               hyphens.
            -  Must start with a letter.
            -  Must be between 1-63 characters.
            -  Must end with a number or a letter.
            -  Must be unique within the assignment.
        description (str):
            Policy description.
            Length of the description is limited to 1024
            characters.
        mode (google.cloud.osconfig_v1alpha.types.OSPolicy.Mode):
            Required. Policy mode
        resource_groups (Sequence[google.cloud.osconfig_v1alpha.types.OSPolicy.ResourceGroup]):
            Required. List of resource groups for the policy. For a
            particular VM, resource groups are evaluated in the order
            specified and the first resource group that is applicable is
            selected and the rest are ignored.

            If none of the resource groups are applicable for a VM, the
            VM is considered to be non-compliant w.r.t this policy. This
            behavior can be toggled by the flag
            ``allow_no_resource_group_match``
        allow_no_resource_group_match (bool):
            This flag determines the OS policy compliance status when
            none of the resource groups within the policy are applicable
            for a VM. Set this value to ``true`` if the policy needs to
            be reported as compliant even if the policy has nothing to
            validate or enforce.
    """

    class Mode(proto.Enum):
        r"""Policy mode"""
        MODE_UNSPECIFIED = 0
        VALIDATION = 1
        ENFORCEMENT = 2

    class OSFilter(proto.Message):
        r"""The ``OSFilter`` is used to specify the OS filtering criteria for
        the resource group.

        Attributes:
            os_short_name (str):
                This should match OS short name emitted by
                the OS inventory agent. An empty value matches
                any OS.
            os_version (str):
                This value should match the version emitted by the OS
                inventory agent. Prefix matches are supported if asterisk(*)
                is provided as the last character. For example, to match all
                versions with a major version of ``7``, specify the
                following value for this field ``7.*``
        """

        os_short_name = proto.Field(proto.STRING, number=1,)
        os_version = proto.Field(proto.STRING, number=2,)

    class Resource(proto.Message):
        r"""An OS policy resource is used to define the desired state
        configuration and provides a specific functionality like
        installing/removing packages, executing a script etc.

        The system ensures that resources are always in their desired
        state by taking necessary actions if they have drifted from
        their desired state.

        Attributes:
            id (str):
                Required. The id of the resource with the following
                restrictions:

                -  Must contain only lowercase letters, numbers, and
                   hyphens.
                -  Must start with a letter.
                -  Must be between 1-63 characters.
                -  Must end with a number or a letter.
                -  Must be unique within the OS policy.
            pkg (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource):
                Package resource
            repository (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.RepositoryResource):
                Package repository resource
            exec_ (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.ExecResource):
                Exec resource
            file (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.FileResource):
                File resource
        """

        class File(proto.Message):
            r"""A remote or local file.

            Attributes:
                remote (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.File.Remote):
                    A generic remote file.
                gcs (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.File.Gcs):
                    A Cloud Storage object.
                local_path (str):
                    A local path within the VM to use.
                allow_insecure (bool):
                    Defaults to false. When false, files are
                    subject to validations based on the file type:
                    Remote: A checksum must be specified.
                    Cloud Storage: An object generation number must
                    be specified.
            """

            class Remote(proto.Message):
                r"""Specifies a file available via some URI.

                Attributes:
                    uri (str):
                        Required. URI from which to fetch the object. It should
                        contain both the protocol and path following the format
                        ``{protocol}://{location}``.
                    sha256_checksum (str):
                        SHA256 checksum of the remote file.
                """

                uri = proto.Field(proto.STRING, number=1,)
                sha256_checksum = proto.Field(proto.STRING, number=2,)

            class Gcs(proto.Message):
                r"""Specifies a file available as a Cloud Storage Object.

                Attributes:
                    bucket (str):
                        Required. Bucket of the Cloud Storage object.
                    object_ (str):
                        Required. Name of the Cloud Storage object.
                    generation (int):
                        Generation number of the Cloud Storage
                        object.
                """

                bucket = proto.Field(proto.STRING, number=1,)
                object_ = proto.Field(proto.STRING, number=2,)
                generation = proto.Field(proto.INT64, number=3,)

            remote = proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="type",
                message="OSPolicy.Resource.File.Remote",
            )
            gcs = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="type",
                message="OSPolicy.Resource.File.Gcs",
            )
            local_path = proto.Field(proto.STRING, number=3, oneof="type",)
            allow_insecure = proto.Field(proto.BOOL, number=4,)

        class PackageResource(proto.Message):
            r"""A resource that manages a system package.

            Attributes:
                desired_state (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.DesiredState):
                    Required. The desired state the agent should
                    maintain for this package.
                apt (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.APT):
                    A package managed by Apt.
                deb (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.Deb):
                    A deb package file.
                yum (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.YUM):
                    A package managed by YUM.
                zypper (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.Zypper):
                    A package managed by Zypper.
                rpm (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.RPM):
                    An rpm package file.
                googet (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.GooGet):
                    A package managed by GooGet.
                msi (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.PackageResource.MSI):
                    An MSI package.
            """

            class DesiredState(proto.Enum):
                r"""The desired state that the OS Config agent maintains on the
                VM.
                """
                DESIRED_STATE_UNSPECIFIED = 0
                INSTALLED = 1
                REMOVED = 2

            class Deb(proto.Message):
                r"""A deb package file. dpkg packages only support INSTALLED
                state.

                Attributes:
                    source (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.File):
                        Required. A deb package.
                    pull_deps (bool):
                        Whether dependencies should also be installed.

                        -  install when false: ``dpkg -i package``
                        -  install when true:
                           ``apt-get update && apt-get -y install package.deb``
                """

                source = proto.Field(
                    proto.MESSAGE, number=1, message="OSPolicy.Resource.File",
                )
                pull_deps = proto.Field(proto.BOOL, number=2,)

            class APT(proto.Message):
                r"""A package managed by APT.

                -  install: ``apt-get update && apt-get -y install [name]``
                -  remove: ``apt-get -y remove [name]``

                Attributes:
                    name (str):
                        Required. Package name.
                """

                name = proto.Field(proto.STRING, number=1,)

            class RPM(proto.Message):
                r"""An RPM package file. RPM packages only support INSTALLED
                state.

                Attributes:
                    source (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.File):
                        Required. An rpm package.
                    pull_deps (bool):
                        Whether dependencies should also be installed.

                        -  install when false:
                           ``rpm --upgrade --replacepkgs package.rpm``
                        -  install when true: ``yum -y install package.rpm`` or
                           ``zypper -y install package.rpm``
                """

                source = proto.Field(
                    proto.MESSAGE, number=1, message="OSPolicy.Resource.File",
                )
                pull_deps = proto.Field(proto.BOOL, number=2,)

            class YUM(proto.Message):
                r"""A package managed by YUM.

                -  install: ``yum -y install package``
                -  remove: ``yum -y remove package``

                Attributes:
                    name (str):
                        Required. Package name.
                """

                name = proto.Field(proto.STRING, number=1,)

            class Zypper(proto.Message):
                r"""A package managed by Zypper.

                -  install: ``zypper -y install package``
                -  remove: ``zypper -y rm package``

                Attributes:
                    name (str):
                        Required. Package name.
                """

                name = proto.Field(proto.STRING, number=1,)

            class GooGet(proto.Message):
                r"""A package managed by GooGet.

                -  install: ``googet -noconfirm install package``
                -  remove: ``googet -noconfirm remove package``

                Attributes:
                    name (str):
                        Required. Package name.
                """

                name = proto.Field(proto.STRING, number=1,)

            class MSI(proto.Message):
                r"""An MSI package. MSI packages only support INSTALLED state.

                Attributes:
                    source (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.File):
                        Required. The MSI package.
                    properties (Sequence[str]):
                        Additional properties to use during installation. This
                        should be in the format of Property=Setting. Appended to the
                        defaults of ``ACTION=INSTALL REBOOT=ReallySuppress``.
                """

                source = proto.Field(
                    proto.MESSAGE, number=1, message="OSPolicy.Resource.File",
                )
                properties = proto.RepeatedField(proto.STRING, number=2,)

            desired_state = proto.Field(
                proto.ENUM,
                number=1,
                enum="OSPolicy.Resource.PackageResource.DesiredState",
            )
            apt = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="system_package",
                message="OSPolicy.Resource.PackageResource.APT",
            )
            deb = proto.Field(
                proto.MESSAGE,
                number=3,
                oneof="system_package",
                message="OSPolicy.Resource.PackageResource.Deb",
            )
            yum = proto.Field(
                proto.MESSAGE,
                number=4,
                oneof="system_package",
                message="OSPolicy.Resource.PackageResource.YUM",
            )
            zypper = proto.Field(
                proto.MESSAGE,
                number=5,
                oneof="system_package",
                message="OSPolicy.Resource.PackageResource.Zypper",
            )
            rpm = proto.Field(
                proto.MESSAGE,
                number=6,
                oneof="system_package",
                message="OSPolicy.Resource.PackageResource.RPM",
            )
            googet = proto.Field(
                proto.MESSAGE,
                number=7,
                oneof="system_package",
                message="OSPolicy.Resource.PackageResource.GooGet",
            )
            msi = proto.Field(
                proto.MESSAGE,
                number=8,
                oneof="system_package",
                message="OSPolicy.Resource.PackageResource.MSI",
            )

        class RepositoryResource(proto.Message):
            r"""A resource that manages a package repository.

            Attributes:
                apt (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.RepositoryResource.AptRepository):
                    An Apt Repository.
                yum (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.RepositoryResource.YumRepository):
                    A Yum Repository.
                zypper (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.RepositoryResource.ZypperRepository):
                    A Zypper Repository.
                goo (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.RepositoryResource.GooRepository):
                    A Goo Repository.
            """

            class AptRepository(proto.Message):
                r"""Represents a single apt package repository. These will be added to a
                repo file that will be managed at
                ``/etc/apt/sources.list.d/google_osconfig.list``.

                Attributes:
                    archive_type (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.RepositoryResource.AptRepository.ArchiveType):
                        Required. Type of archive files in this
                        repository.
                    uri (str):
                        Required. URI for this repository.
                    distribution (str):
                        Required. Distribution of this repository.
                    components (Sequence[str]):
                        Required. List of components for this
                        repository. Must contain at least one item.
                    gpg_key (str):
                        URI of the key file for this repository. The agent maintains
                        a keyring at
                        ``/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg``.
                """

                class ArchiveType(proto.Enum):
                    r"""Type of archive."""
                    ARCHIVE_TYPE_UNSPECIFIED = 0
                    DEB = 1
                    DEB_SRC = 2

                archive_type = proto.Field(
                    proto.ENUM,
                    number=1,
                    enum="OSPolicy.Resource.RepositoryResource.AptRepository.ArchiveType",
                )
                uri = proto.Field(proto.STRING, number=2,)
                distribution = proto.Field(proto.STRING, number=3,)
                components = proto.RepeatedField(proto.STRING, number=4,)
                gpg_key = proto.Field(proto.STRING, number=5,)

            class YumRepository(proto.Message):
                r"""Represents a single yum package repository. These are added to a
                repo file that is managed at
                ``/etc/yum.repos.d/google_osconfig.repo``.

                Attributes:
                    id (str):
                        Required. A one word, unique name for this repository. This
                        is the ``repo id`` in the yum config file and also the
                        ``display_name`` if ``display_name`` is omitted. This id is
                        also used as the unique identifier when checking for
                        resource conflicts.
                    display_name (str):
                        The display name of the repository.
                    base_url (str):
                        Required. The location of the repository
                        directory.
                    gpg_keys (Sequence[str]):
                        URIs of GPG keys.
                """

                id = proto.Field(proto.STRING, number=1,)
                display_name = proto.Field(proto.STRING, number=2,)
                base_url = proto.Field(proto.STRING, number=3,)
                gpg_keys = proto.RepeatedField(proto.STRING, number=4,)

            class ZypperRepository(proto.Message):
                r"""Represents a single zypper package repository. These are added to a
                repo file that is managed at
                ``/etc/zypp/repos.d/google_osconfig.repo``.

                Attributes:
                    id (str):
                        Required. A one word, unique name for this repository. This
                        is the ``repo id`` in the zypper config file and also the
                        ``display_name`` if ``display_name`` is omitted. This id is
                        also used as the unique identifier when checking for
                        GuestPolicy conflicts.
                    display_name (str):
                        The display name of the repository.
                    base_url (str):
                        Required. The location of the repository
                        directory.
                    gpg_keys (Sequence[str]):
                        URIs of GPG keys.
                """

                id = proto.Field(proto.STRING, number=1,)
                display_name = proto.Field(proto.STRING, number=2,)
                base_url = proto.Field(proto.STRING, number=3,)
                gpg_keys = proto.RepeatedField(proto.STRING, number=4,)

            class GooRepository(proto.Message):
                r"""Represents a Goo package repository. These are added to a repo file
                that is managed at
                ``C:/ProgramData/GooGet/repos/google_osconfig.repo``.

                Attributes:
                    name (str):
                        Required. The name of the repository.
                    url (str):
                        Required. The url of the repository.
                """

                name = proto.Field(proto.STRING, number=1,)
                url = proto.Field(proto.STRING, number=2,)

            apt = proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="repository",
                message="OSPolicy.Resource.RepositoryResource.AptRepository",
            )
            yum = proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="repository",
                message="OSPolicy.Resource.RepositoryResource.YumRepository",
            )
            zypper = proto.Field(
                proto.MESSAGE,
                number=3,
                oneof="repository",
                message="OSPolicy.Resource.RepositoryResource.ZypperRepository",
            )
            goo = proto.Field(
                proto.MESSAGE,
                number=4,
                oneof="repository",
                message="OSPolicy.Resource.RepositoryResource.GooRepository",
            )

        class ExecResource(proto.Message):
            r"""A resource that allows executing scripts on the VM.

            The ``ExecResource`` has 2 stages: ``validate`` and ``enforce`` and
            both stages accept a script as an argument to execute.

            When the ``ExecResource`` is applied by the agent, it first executes
            the script in the ``validate`` stage. The ``validate`` stage can
            signal that the ``ExecResource`` is already in the desired state by
            returning an exit code of ``100``. If the ``ExecResource`` is not in
            the desired state, it should return an exit code of ``101``. Any
            other exit code returned by this stage is considered an error.

            If the ``ExecResource`` is not in the desired state based on the
            exit code from the ``validate`` stage, the agent proceeds to execute
            the script from the ``enforce`` stage. If the ``ExecResource`` is
            already in the desired state, the ``enforce`` stage will not be run.
            Similar to ``validate`` stage, the ``enforce`` stage should return
            an exit code of ``100`` to indicate that the resource in now in its
            desired state. Any other exit code is considered an error.

            NOTE: An exit code of ``100`` was chosen over ``0`` (and ``101`` vs
            ``1``) to have an explicit indicator of ``in desired state``,
            ``not in desired state`` and errors. Because, for example,
            Powershell will always return an exit code of ``0`` unless an
            ``exit`` statement is provided in the script. So, for reasons of
            consistency and being explicit, exit codes ``100`` and ``101`` were
            chosen.

            Attributes:
                validate (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.ExecResource.Exec):
                    Required. What to run to validate this
                    resource is in the desired state. An exit code
                    of 100 indicates "in desired state", and exit
                    code of 101 indicates "not in desired state".
                    Any other exit code indicates a failure running
                    validate.
                enforce (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.ExecResource.Exec):
                    What to run to bring this resource into the
                    desired state. An exit code of 100 indicates
                    "success", any other exit code indicates a
                    failure running enforce.
            """

            class Exec(proto.Message):
                r"""A file or script to execute.

                Attributes:
                    file (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.File):
                        A remote or local file.
                    script (str):
                        An inline script.
                        The size of the script is limited to 1024
                        characters.
                    args (Sequence[str]):
                        Optional arguments to pass to the source
                        during execution.
                    interpreter (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.ExecResource.Exec.Interpreter):
                        Required. The script interpreter to use.
                    output_file_path (str):
                        Only recorded for enforce Exec.
                        Path to an output file (that is created by this
                        Exec) whose content will be recorded in
                        OSPolicyResourceCompliance after a successful
                        run. Absence or failure to read this file will
                        result in this ExecResource being non-compliant.
                        Output file size is limited to 100K bytes.
                """

                class Interpreter(proto.Enum):
                    r"""The interpreter to use."""
                    INTERPRETER_UNSPECIFIED = 0
                    NONE = 1
                    SHELL = 2
                    POWERSHELL = 3

                file = proto.Field(
                    proto.MESSAGE,
                    number=1,
                    oneof="source",
                    message="OSPolicy.Resource.File",
                )
                script = proto.Field(proto.STRING, number=2, oneof="source",)
                args = proto.RepeatedField(proto.STRING, number=3,)
                interpreter = proto.Field(
                    proto.ENUM,
                    number=4,
                    enum="OSPolicy.Resource.ExecResource.Exec.Interpreter",
                )
                output_file_path = proto.Field(proto.STRING, number=5,)

            validate = proto.Field(
                proto.MESSAGE, number=1, message="OSPolicy.Resource.ExecResource.Exec",
            )
            enforce = proto.Field(
                proto.MESSAGE, number=2, message="OSPolicy.Resource.ExecResource.Exec",
            )

        class FileResource(proto.Message):
            r"""A resource that manages the state of a file.

            Attributes:
                file (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.File):
                    A remote or local source.
                content (str):
                    A a file with this content.
                    The size of the content is limited to 1024
                    characters.
                path (str):
                    Required. The absolute path of the file
                    within the VM.
                state (google.cloud.osconfig_v1alpha.types.OSPolicy.Resource.FileResource.DesiredState):
                    Required. Desired state of the file.
                permissions (str):
                    Consists of three octal digits which
                    represent, in order, the permissions of the
                    owner, group, and other users for the file
                    (similarly to the numeric mode used in the linux
                    chmod utility). Each digit represents a three
                    bit number with the 4 bit corresponding to the
                    read permissions, the 2 bit corresponds to the
                    write bit, and the one bit corresponds to the
                    execute permission. Default behavior is 755.

                    Below are some examples of permissions and their
                    associated values: read, write, and execute: 7
                    read and execute: 5
                    read and write: 6
                    read only: 4
            """

            class DesiredState(proto.Enum):
                r"""Desired state of the file."""
                DESIRED_STATE_UNSPECIFIED = 0
                PRESENT = 1
                ABSENT = 2
                CONTENTS_MATCH = 3

            file = proto.Field(
                proto.MESSAGE,
                number=1,
                oneof="source",
                message="OSPolicy.Resource.File",
            )
            content = proto.Field(proto.STRING, number=2, oneof="source",)
            path = proto.Field(proto.STRING, number=3,)
            state = proto.Field(
                proto.ENUM,
                number=4,
                enum="OSPolicy.Resource.FileResource.DesiredState",
            )
            permissions = proto.Field(proto.STRING, number=5,)

        id = proto.Field(proto.STRING, number=1,)
        pkg = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="resource_type",
            message="OSPolicy.Resource.PackageResource",
        )
        repository = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="resource_type",
            message="OSPolicy.Resource.RepositoryResource",
        )
        exec_ = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="resource_type",
            message="OSPolicy.Resource.ExecResource",
        )
        file = proto.Field(
            proto.MESSAGE,
            number=5,
            oneof="resource_type",
            message="OSPolicy.Resource.FileResource",
        )

    class ResourceGroup(proto.Message):
        r"""Resource groups provide a mechanism to group OS policy resources.

        Resource groups enable OS policy authors to create a single OS
        policy to be applied to VMs running different operating Systems.

        When the OS policy is applied to a target VM, the appropriate
        resource group within the OS policy is selected based on the
        ``OSFilter`` specified within the resource group.

        Attributes:
            os_filter (google.cloud.osconfig_v1alpha.types.OSPolicy.OSFilter):
                Used to specify the OS filter for a resource
                group
            resources (Sequence[google.cloud.osconfig_v1alpha.types.OSPolicy.Resource]):
                Required. List of resources configured for
                this resource group. The resources are executed
                in the exact order specified here.
        """

        os_filter = proto.Field(proto.MESSAGE, number=1, message="OSPolicy.OSFilter",)
        resources = proto.RepeatedField(
            proto.MESSAGE, number=2, message="OSPolicy.Resource",
        )

    id = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    mode = proto.Field(proto.ENUM, number=3, enum=Mode,)
    resource_groups = proto.RepeatedField(
        proto.MESSAGE, number=4, message=ResourceGroup,
    )
    allow_no_resource_group_match = proto.Field(proto.BOOL, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
