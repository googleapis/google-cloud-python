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

import proto  # type: ignore


__protobuf__ = proto.module(
    package='google.maps.addressvalidation.v1',
    manifest={
        'AddressMetadata',
    },
)


class AddressMetadata(proto.Message):
    r"""The metadata for the address. ``metadata`` is not guaranteed to be
    fully populated for every address sent to the Address Validation
    API.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        business (bool):
            Indicates that this is the address of a
            business. If unset, indicates that the value is
            unknown.

            This field is a member of `oneof`_ ``_business``.
        po_box (bool):
            Indicates that the address of a PO box.
            If unset, indicates that the value is unknown.

            This field is a member of `oneof`_ ``_po_box``.
        residential (bool):
            Indicates that this is the address of a
            residence. If unset, indicates that the value is
            unknown.

            This field is a member of `oneof`_ ``_residential``.
    """

    business: bool = proto.Field(
        proto.BOOL,
        number=2,
        optional=True,
    )
    po_box: bool = proto.Field(
        proto.BOOL,
        number=3,
        optional=True,
    )
    residential: bool = proto.Field(
        proto.BOOL,
        number=6,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
