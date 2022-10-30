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
    package="google.maps.addressvalidation.v1",
    manifest={
        "AddressMetadata",
    },
)


class AddressMetadata(proto.Message):
    r"""The metadata for the address.

    Attributes:
        highrise (bool):
            Indicates that this address is a high-rise building. If
            unset, indicates that the value is unknown.

            DEPRECATED: Please use
            ```address_record_type`` <google.maps.addressvalidation.v1.ValidationResult.usps_data.address_record_type>`__
            instead. This field will be removed with the GA release.

            This field is a member of `oneof`_ ``_highrise``.
        business (bool):
            Indicates that this is the address of a
            business. If unset, indicates that the value is
            unknown.

            This field is a member of `oneof`_ ``_business``.
        po_box (bool):
            Indicates that the address of a PO box.
            If unset, indicates that the value is unknown.

            This field is a member of `oneof`_ ``_po_box``.
        multi_family (bool):
            Indicates that the address is of a
            multi-family building. If unset, indicates that
            the value is unknown.
            DEPRECATED: this field will be removed with the
            GA release.

            This field is a member of `oneof`_ ``_multi_family``.
        residential (bool):
            Indicates that this is the address of a
            residence. If unset, indicates that the value is
            unknown.

            This field is a member of `oneof`_ ``_residential``.
    """

    highrise = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    business = proto.Field(
        proto.BOOL,
        number=2,
        optional=True,
    )
    po_box = proto.Field(
        proto.BOOL,
        number=3,
        optional=True,
    )
    multi_family = proto.Field(
        proto.BOOL,
        number=4,
        optional=True,
    )
    residential = proto.Field(
        proto.BOOL,
        number=6,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
