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
    package="google.cloud.securitycenter.v1",
    manifest={
        "ContactDetails",
        "Contact",
    },
)


class ContactDetails(proto.Message):
    r"""The details pertaining to specific contacts

    Attributes:
        contacts (Sequence[google.cloud.securitycenter_v1.types.Contact]):
            A list of contacts
    """

    contacts = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Contact",
    )


class Contact(proto.Message):
    r"""Representa a single contact's email address

    Attributes:
        email (str):
            An email address e.g. "person123@company.com".
    """

    email = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
