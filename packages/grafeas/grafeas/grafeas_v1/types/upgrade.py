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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from grafeas.grafeas_v1.types import package as g_package


__protobuf__ = proto.module(
    package="grafeas.v1",
    manifest={
        "UpgradeNote",
        "UpgradeDistribution",
        "WindowsUpdate",
        "UpgradeOccurrence",
    },
)


class UpgradeNote(proto.Message):
    r"""An Upgrade Note represents a potential upgrade of a package to a
    given version. For each package version combination (i.e. bash 4.0,
    bash 4.1, bash 4.1.2), there will be an Upgrade Note. For Windows,
    windows_update field represents the information related to the
    update.

    Attributes:
        package (str):
            Required for non-Windows OS. The package this
            Upgrade is for.
        version (~.g_package.Version):
            Required for non-Windows OS. The version of
            the package in machine + human readable form.
        distributions (Sequence[~.upgrade.UpgradeDistribution]):
            Metadata about the upgrade for each specific
            operating system.
        windows_update (~.upgrade.WindowsUpdate):
            Required for Windows OS. Represents the
            metadata about the Windows update.
    """

    package = proto.Field(proto.STRING, number=1)

    version = proto.Field(proto.MESSAGE, number=2, message=g_package.Version,)

    distributions = proto.RepeatedField(
        proto.MESSAGE, number=3, message="UpgradeDistribution",
    )

    windows_update = proto.Field(proto.MESSAGE, number=4, message="WindowsUpdate",)


class UpgradeDistribution(proto.Message):
    r"""The Upgrade Distribution represents metadata about the
    Upgrade for each operating system (CPE). Some distributions have
    additional metadata around updates, classifying them into
    various categories and severities.

    Attributes:
        cpe_uri (str):
            Required - The specific operating system this
            metadata applies to. See
            https://cpe.mitre.org/specification/.
        classification (str):
            The operating system classification of this Upgrade, as
            specified by the upstream operating system upgrade feed. For
            Windows the classification is one of the category_ids listed
            at
            https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ff357803(v=vs.85)
        severity (str):
            The severity as specified by the upstream
            operating system.
        cve (Sequence[str]):
            The cve tied to this Upgrade.
    """

    cpe_uri = proto.Field(proto.STRING, number=1)

    classification = proto.Field(proto.STRING, number=2)

    severity = proto.Field(proto.STRING, number=3)

    cve = proto.RepeatedField(proto.STRING, number=4)


class WindowsUpdate(proto.Message):
    r"""Windows Update represents the metadata about the update for
    the Windows operating system. The fields in this message come
    from the Windows Update API documented at
    https://docs.microsoft.com/en-us/windows/win32/api/wuapi/nn-
    wuapi-iupdate.

    Attributes:
        identity (~.upgrade.WindowsUpdate.Identity):
            Required - The unique identifier for the
            update.
        title (str):
            The localized title of the update.
        description (str):
            The localized description of the update.
        categories (Sequence[~.upgrade.WindowsUpdate.Category]):
            The list of categories to which the update
            belongs.
        kb_article_ids (Sequence[str]):
            The Microsoft Knowledge Base article IDs that
            are associated with the update.
        support_url (str):
            The hyperlink to the support information for
            the update.
        last_published_timestamp (~.timestamp.Timestamp):
            The last published timestamp of the update.
    """

    class Identity(proto.Message):
        r"""The unique identifier of the update.

        Attributes:
            update_id (str):
                The revision independent identifier of the
                update.
            revision (int):
                The revision number of the update.
        """

        update_id = proto.Field(proto.STRING, number=1)

        revision = proto.Field(proto.INT32, number=2)

    class Category(proto.Message):
        r"""The category to which the update belongs.

        Attributes:
            category_id (str):
                The identifier of the category.
            name (str):
                The localized name of the category.
        """

        category_id = proto.Field(proto.STRING, number=1)

        name = proto.Field(proto.STRING, number=2)

    identity = proto.Field(proto.MESSAGE, number=1, message=Identity,)

    title = proto.Field(proto.STRING, number=2)

    description = proto.Field(proto.STRING, number=3)

    categories = proto.RepeatedField(proto.MESSAGE, number=4, message=Category,)

    kb_article_ids = proto.RepeatedField(proto.STRING, number=5)

    support_url = proto.Field(proto.STRING, number=6)

    last_published_timestamp = proto.Field(
        proto.MESSAGE, number=7, message=timestamp.Timestamp,
    )


class UpgradeOccurrence(proto.Message):
    r"""An Upgrade Occurrence represents that a specific resource_url could
    install a specific upgrade. This presence is supplied via local
    sources (i.e. it is present in the mirror and the running system has
    noticed its availability). For Windows, both distribution and
    windows_update contain information for the Windows update.

    Attributes:
        package (str):
            Required for non-Windows OS. The package this
            Upgrade is for.
        parsed_version (~.g_package.Version):
            Required for non-Windows OS. The version of
            the package in a machine + human readable form.
        distribution (~.upgrade.UpgradeDistribution):
            Metadata about the upgrade for available for the specific
            operating system for the resource_url. This allows efficient
            filtering, as well as making it easier to use the
            occurrence.
        windows_update (~.upgrade.WindowsUpdate):
            Required for Windows OS. Represents the
            metadata about the Windows update.
    """

    package = proto.Field(proto.STRING, number=1)

    parsed_version = proto.Field(proto.MESSAGE, number=3, message=g_package.Version,)

    distribution = proto.Field(proto.MESSAGE, number=4, message=UpgradeDistribution,)

    windows_update = proto.Field(proto.MESSAGE, number=5, message=WindowsUpdate,)


__all__ = tuple(sorted(__protobuf__.manifest))
