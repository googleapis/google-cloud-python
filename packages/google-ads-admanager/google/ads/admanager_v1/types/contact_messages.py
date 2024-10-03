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
    package="google.ads.admanager.v1",
    manifest={
        "Contact",
    },
)


class Contact(proto.Message):
    r"""A contact represents a person who is affiliated with a single
    company. A contact can have a variety of contact information
    associated to it, and can be invited to view their company's
    orders, line items, creatives, and reports.

    Attributes:
        name (str):
            Identifier. The resource name of the ``Contact``. Format:
            ``networks/{network_code}/contacts/{contact_id}``
        contact_id (int):
            Output only. The unique ID of the contact.
            This value is readonly and is assigned by
            Google.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    contact_id: int = proto.Field(
        proto.INT64,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
