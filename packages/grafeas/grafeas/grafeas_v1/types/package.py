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


__protobuf__ = proto.module(
    package="grafeas.v1",
    manifest={
        "Architecture",
        "Distribution",
        "Location",
        "PackageNote",
        "PackageOccurrence",
        "Version",
    },
)


class Architecture(proto.Enum):
    r"""Instruction set architectures supported by various package
    managers.
    """
    ARCHITECTURE_UNSPECIFIED = 0
    X86 = 1
    X64 = 2


class Distribution(proto.Message):
    r"""This represents a particular channel of distribution for a
    given package. E.g., Debian's jessie-backports dpkg mirror.

    Attributes:
        cpe_uri (str):
            Required. The cpe_uri in `CPE
            format <https://cpe.mitre.org/specification/>`__ denoting
            the package manager version distributing a package.
        architecture (grafeas.grafeas_v1.types.Architecture):
            The CPU architecture for which packages in
            this distribution channel were built.
        latest_version (grafeas.grafeas_v1.types.Version):
            The latest available version of this package
            in this distribution channel.
        maintainer (str):
            A freeform string denoting the maintainer of
            this package.
        url (str):
            The distribution channel-specific homepage
            for this package.
        description (str):
            The distribution channel-specific description
            of this package.
    """

    cpe_uri = proto.Field(proto.STRING, number=1,)
    architecture = proto.Field(proto.ENUM, number=2, enum="Architecture",)
    latest_version = proto.Field(proto.MESSAGE, number=3, message="Version",)
    maintainer = proto.Field(proto.STRING, number=4,)
    url = proto.Field(proto.STRING, number=5,)
    description = proto.Field(proto.STRING, number=6,)


class Location(proto.Message):
    r"""An occurrence of a particular package installation found within a
    system's filesystem. E.g., glibc was found in
    ``/var/lib/dpkg/status``.

    Attributes:
        cpe_uri (str):
            Required. The CPE URI in `CPE
            format <https://cpe.mitre.org/specification/>`__ denoting
            the package manager version distributing a package.
        version (grafeas.grafeas_v1.types.Version):
            The version installed at this location.
        path (str):
            The path from which we gathered that this
            package/version is installed.
    """

    cpe_uri = proto.Field(proto.STRING, number=1,)
    version = proto.Field(proto.MESSAGE, number=2, message="Version",)
    path = proto.Field(proto.STRING, number=3,)


class PackageNote(proto.Message):
    r"""This represents a particular package that is distributed over
    various channels. E.g., glibc (aka libc6) is distributed by
    many, at various versions.

    Attributes:
        name (str):
            Required. Immutable. The name of the package.
        distribution (Sequence[grafeas.grafeas_v1.types.Distribution]):
            The various channels by which a package is
            distributed.
    """

    name = proto.Field(proto.STRING, number=1,)
    distribution = proto.RepeatedField(
        proto.MESSAGE, number=10, message="Distribution",
    )


class PackageOccurrence(proto.Message):
    r"""Details on how a particular software package was installed on
    a system.

    Attributes:
        name (str):
            Output only. The name of the installed
            package.
        location (Sequence[grafeas.grafeas_v1.types.Location]):
            Required. All of the places within the
            filesystem versions of this package have been
            found.
    """

    name = proto.Field(proto.STRING, number=1,)
    location = proto.RepeatedField(proto.MESSAGE, number=2, message="Location",)


class Version(proto.Message):
    r"""Version contains structured information about the version of
    a package.

    Attributes:
        epoch (int):
            Used to correct mistakes in the version
            numbering scheme.
        name (str):
            Required only when version kind is NORMAL.
            The main part of the version name.
        revision (str):
            The iteration of the package build from the
            above version.
        inclusive (bool):
            Whether this version is specifying part of an
            inclusive range. Grafeas does not have the
            capability to specify version ranges; instead we
            have fields that specify start version and end
            versions. At times this is insufficient - we
            also need to specify whether the version is
            included in the range or is excluded from the
            range. This boolean is expected to be set to
            true when the version is included in a range.
        kind (grafeas.grafeas_v1.types.Version.VersionKind):
            Required. Distinguishes between sentinel
            MIN/MAX versions and normal versions.
        full_name (str):
            Human readable version string. This string is
            of the form <epoch>:<name>-<revision> and is
            only set when kind is NORMAL.
    """

    class VersionKind(proto.Enum):
        r"""Whether this is an ordinary package version or a sentinel
        MIN/MAX version.
        """
        VERSION_KIND_UNSPECIFIED = 0
        NORMAL = 1
        MINIMUM = 2
        MAXIMUM = 3

    epoch = proto.Field(proto.INT32, number=1,)
    name = proto.Field(proto.STRING, number=2,)
    revision = proto.Field(proto.STRING, number=3,)
    inclusive = proto.Field(proto.BOOL, number=6,)
    kind = proto.Field(proto.ENUM, number=4, enum=VersionKind,)
    full_name = proto.Field(proto.STRING, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
