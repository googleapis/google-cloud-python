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


__protobuf__ = proto.module(
    package="google.cloud.osconfig.v1", manifest={"Inventory",},
)


class Inventory(proto.Message):
    r"""The inventory details of a VM.

    Attributes:
        os_info (~.inventory.Inventory.OsInfo):
            Base level operating system information for
            the VM.
        items (Sequence[~.inventory.Inventory.ItemsEntry]):
            Inventory items related to the VM keyed by an
            opaque unique identifier for each inventory
            item.  The identifier is unique to each distinct
            and addressable inventory item and will change,
            when there is a new package version.
    """

    class OsInfo(proto.Message):
        r"""Operating system information for the VM.

        Attributes:
            hostname (str):
                The VM hostname.
            long_name (str):
                The operating system long name.
                For example 'Debian GNU/Linux 9' or 'Microsoft
                Window Server 2019 Datacenter'.
            short_name (str):
                The operating system short name.
                For example, 'windows' or 'debian'.
            version (str):
                The version of the operating system.
            architecture (str):
                The system architecture of the operating
                system.
            kernel_version (str):
                The kernel version of the operating system.
            kernel_release (str):
                The kernel release of the operating system.
            osconfig_agent_version (str):
                The current version of the OS Config agent
                running on the VM.
        """

        hostname = proto.Field(proto.STRING, number=9)

        long_name = proto.Field(proto.STRING, number=2)

        short_name = proto.Field(proto.STRING, number=3)

        version = proto.Field(proto.STRING, number=4)

        architecture = proto.Field(proto.STRING, number=5)

        kernel_version = proto.Field(proto.STRING, number=6)

        kernel_release = proto.Field(proto.STRING, number=7)

        osconfig_agent_version = proto.Field(proto.STRING, number=8)

    class Item(proto.Message):
        r"""A single piece of inventory on a VM.

        Attributes:
            id (str):
                Identifier for this item, unique across items
                for this VM.
            origin_type (~.inventory.Inventory.Item.OriginType):
                The origin of this inventory item.
            create_time (~.timestamp.Timestamp):
                When this inventory item was first detected.
            update_time (~.timestamp.Timestamp):
                When this inventory item was last modified.
            type_ (~.inventory.Inventory.Item.Type):
                The specific type of inventory, correlating
                to its specific details.
            installed_package (~.inventory.Inventory.SoftwarePackage):
                Software package present on the VM instance.
            available_package (~.inventory.Inventory.SoftwarePackage):
                Software package available to be installed on
                the VM instance.
        """

        class OriginType(proto.Enum):
            r"""The origin of a specific inventory item."""
            ORIGIN_TYPE_UNSPECIFIED = 0
            INVENTORY_REPORT = 1

        class Type(proto.Enum):
            r"""The different types of inventory that are tracked on a VM."""
            TYPE_UNSPECIFIED = 0
            INSTALLED_PACKAGE = 1
            AVAILABLE_PACKAGE = 2

        id = proto.Field(proto.STRING, number=1)

        origin_type = proto.Field(
            proto.ENUM, number=2, enum="Inventory.Item.OriginType",
        )

        create_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp,)

        update_time = proto.Field(proto.MESSAGE, number=9, message=timestamp.Timestamp,)

        type_ = proto.Field(proto.ENUM, number=5, enum="Inventory.Item.Type",)

        installed_package = proto.Field(
            proto.MESSAGE,
            number=6,
            oneof="details",
            message="Inventory.SoftwarePackage",
        )

        available_package = proto.Field(
            proto.MESSAGE,
            number=7,
            oneof="details",
            message="Inventory.SoftwarePackage",
        )

    class SoftwarePackage(proto.Message):
        r"""Software package information of the operating system.

        Attributes:
            yum_package (~.inventory.Inventory.VersionedPackage):
                Yum package info. For details about the yum package manager,
                see
                https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/ch-yum.
            apt_package (~.inventory.Inventory.VersionedPackage):
                Details of an APT package.
                For details about the apt package manager, see
                https://wiki.debian.org/Apt.
            zypper_package (~.inventory.Inventory.VersionedPackage):
                Details of a Zypper package. For details about the Zypper
                package manager, see
                https://en.opensuse.org/SDB:Zypper_manual.
            googet_package (~.inventory.Inventory.VersionedPackage):
                Details of a Googet package.
                For details about the googet package manager,
                see  https://github.com/google/googet.
            zypper_patch (~.inventory.Inventory.ZypperPatch):
                Details of a Zypper patch. For details about the Zypper
                package manager, see
                https://en.opensuse.org/SDB:Zypper_manual.
            wua_package (~.inventory.Inventory.WindowsUpdatePackage):
                Details of a Windows Update package. See
                https://docs.microsoft.com/en-us/windows/win32/api/_wua/ for
                information about Windows Update.
            qfe_package (~.inventory.Inventory.WindowsQuickFixEngineeringPackage):
                Details of a Windows Quick Fix engineering
                package. See
                https://docs.microsoft.com/en-
                us/windows/win32/cimwin32prov/win32-quickfixengineering
                for info in Windows Quick Fix Engineering.
            cos_package (~.inventory.Inventory.VersionedPackage):
                Details of a COS package.
        """

        yum_package = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="details",
            message="Inventory.VersionedPackage",
        )

        apt_package = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="details",
            message="Inventory.VersionedPackage",
        )

        zypper_package = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="details",
            message="Inventory.VersionedPackage",
        )

        googet_package = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="details",
            message="Inventory.VersionedPackage",
        )

        zypper_patch = proto.Field(
            proto.MESSAGE, number=5, oneof="details", message="Inventory.ZypperPatch",
        )

        wua_package = proto.Field(
            proto.MESSAGE,
            number=6,
            oneof="details",
            message="Inventory.WindowsUpdatePackage",
        )

        qfe_package = proto.Field(
            proto.MESSAGE,
            number=7,
            oneof="details",
            message="Inventory.WindowsQuickFixEngineeringPackage",
        )

        cos_package = proto.Field(
            proto.MESSAGE,
            number=8,
            oneof="details",
            message="Inventory.VersionedPackage",
        )

    class VersionedPackage(proto.Message):
        r"""Information related to the a standard versioned package.
        This includes package info for APT, Yum, Zypper, and Googet
        package managers.

        Attributes:
            package_name (str):
                The name of the package.
            architecture (str):
                The system architecture this package is
                intended for.
            version (str):
                The version of the package.
        """

        package_name = proto.Field(proto.STRING, number=4)

        architecture = proto.Field(proto.STRING, number=2)

        version = proto.Field(proto.STRING, number=3)

    class WindowsUpdatePackage(proto.Message):
        r"""Details related to a Windows Update package. Field data and names
        are taken from Windows Update API IUpdate Interface:
        https://docs.microsoft.com/en-us/windows/win32/api/_wua/ Descriptive
        fields like title, and description are localized based on the locale
        of the VM being updated.

        Attributes:
            title (str):
                The localized title of the update package.
            description (str):
                The localized description of the update
                package.
            categories (Sequence[~.inventory.Inventory.WindowsUpdatePackage.WindowsUpdateCategory]):
                The categories that are associated with this
                update package.
            kb_article_ids (Sequence[str]):
                A collection of Microsoft Knowledge Base
                article IDs that are associated with the update
                package.
            support_url (str):
                A hyperlink to the language-specific support
                information for the update.
            more_info_urls (Sequence[str]):
                A collection of URLs that provide more
                information about the update package.
            update_id (str):
                Gets the identifier of an update package.
                Stays the same across revisions.
            revision_number (int):
                The revision number of this update package.
            last_deployment_change_time (~.timestamp.Timestamp):
                The last published date of the update, in
                (UTC) date and time.
        """

        class WindowsUpdateCategory(proto.Message):
            r"""Categories specified by the Windows Update.

            Attributes:
                id (str):
                    The identifier of the windows update
                    category.
                name (str):
                    The name of the windows update category.
            """

            id = proto.Field(proto.STRING, number=1)

            name = proto.Field(proto.STRING, number=2)

        title = proto.Field(proto.STRING, number=1)

        description = proto.Field(proto.STRING, number=2)

        categories = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="Inventory.WindowsUpdatePackage.WindowsUpdateCategory",
        )

        kb_article_ids = proto.RepeatedField(proto.STRING, number=4)

        support_url = proto.Field(proto.STRING, number=11)

        more_info_urls = proto.RepeatedField(proto.STRING, number=5)

        update_id = proto.Field(proto.STRING, number=6)

        revision_number = proto.Field(proto.INT32, number=7)

        last_deployment_change_time = proto.Field(
            proto.MESSAGE, number=10, message=timestamp.Timestamp,
        )

    class ZypperPatch(proto.Message):
        r"""Details related to a Zypper Patch.

        Attributes:
            patch_name (str):
                The name of the patch.
            category (str):
                The category of the patch.
            severity (str):
                The severity specified for this patch
            summary (str):
                Any summary information provided about this
                patch.
        """

        patch_name = proto.Field(proto.STRING, number=5)

        category = proto.Field(proto.STRING, number=2)

        severity = proto.Field(proto.STRING, number=3)

        summary = proto.Field(proto.STRING, number=4)

    class WindowsQuickFixEngineeringPackage(proto.Message):
        r"""Information related to a Quick Fix Engineering package.
        Fields are taken from Windows QuickFixEngineering Interface and
        match the source names:
        https://docs.microsoft.com/en-
        us/windows/win32/cimwin32prov/win32-quickfixengineering

        Attributes:
            caption (str):
                A short textual description of the QFE
                update.
            description (str):
                A textual description of the QFE update.
            hot_fix_id (str):
                Unique identifier associated with a
                particular QFE update.
            install_time (~.timestamp.Timestamp):
                Date that the QFE update was installed. Mapped from
                installed_on field.
        """

        caption = proto.Field(proto.STRING, number=1)

        description = proto.Field(proto.STRING, number=2)

        hot_fix_id = proto.Field(proto.STRING, number=3)

        install_time = proto.Field(
            proto.MESSAGE, number=5, message=timestamp.Timestamp,
        )

    os_info = proto.Field(proto.MESSAGE, number=1, message=OsInfo,)

    items = proto.MapField(proto.STRING, proto.MESSAGE, number=2, message=Item,)


__all__ = tuple(sorted(__protobuf__.manifest))
