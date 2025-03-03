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

from google.cloud.support_v2.types import attachment


__protobuf__ = proto.module(
    package='google.cloud.support.v2',
    manifest={
        'ListAttachmentsRequest',
        'ListAttachmentsResponse',
    },
)


class ListAttachmentsRequest(proto.Message):
    r"""The request message for the ListAttachments endpoint.

    Attributes:
        parent (str):
            Required. The resource name of Case object
            for which attachments should be listed.
        page_size (int):
            The maximum number of attachments fetched
            with each request. If not provided, the default
            is 10. The maximum page size that will be
            returned is 100.
        page_token (str):
            A token identifying the page of results to
            return. If unspecified, the first page is
            retrieved.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListAttachmentsResponse(proto.Message):
    r"""The response message for the ListAttachments endpoint.

    Attributes:
        attachments (MutableSequence[google.cloud.support_v2.types.Attachment]):
            The list of attachments associated with the
            given case.
        next_page_token (str):
            A token to retrieve the next page of results. This should be
            set in the ``page_token`` field of subsequent
            ``cases.attachments.list`` requests. If unspecified, there
            are no more results to retrieve.
    """

    @property
    def raw_page(self):
        return self

    attachments: MutableSequence[attachment.Attachment] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=attachment.Attachment,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
