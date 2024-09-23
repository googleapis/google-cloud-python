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
    package="google.cloud.oracledatabase.v1",
    manifest={
        "CustomerContact",
    },
)


class CustomerContact(proto.Message):
    r"""The CustomerContact reference as defined by Oracle.
    https://docs.oracle.com/en-us/iaas/api/#/en/database/20160918/datatypes/CustomerContact

    Attributes:
        email (str):
            Required. The email address used by Oracle to
            send notifications regarding databases and
            infrastructure.
    """

    email: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
