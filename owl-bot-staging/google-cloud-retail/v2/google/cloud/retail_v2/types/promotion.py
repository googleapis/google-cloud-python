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
    package='google.cloud.retail.v2',
    manifest={
        'Promotion',
    },
)


class Promotion(proto.Message):
    r"""Promotion information.

    Attributes:
        promotion_id (str):
            ID of the promotion. For example, "free gift".

            The value must be a UTF-8 encoded string with a length limit
            of 128 characters, and match the pattern:
            ``[a-zA-Z][a-zA-Z0-9_]*``. For example, id0LikeThis or
            ID_1_LIKE_THIS. Otherwise, an INVALID_ARGUMENT error is
            returned.

            Corresponds to Google Merchant Center property
            `promotion_id <https://support.google.com/merchants/answer/7050148>`__.
    """

    promotion_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
