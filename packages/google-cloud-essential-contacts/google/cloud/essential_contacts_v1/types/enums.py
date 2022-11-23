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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.essentialcontacts.v1",
    manifest={
        "NotificationCategory",
        "ValidationState",
    },
)


class NotificationCategory(proto.Enum):
    r"""The notification categories that an essential contact can be
    subscribed to. Each notification will be categorized by the
    sender into one of the following categories. All contacts that
    are subscribed to that category will receive the notification.
    """
    NOTIFICATION_CATEGORY_UNSPECIFIED = 0
    ALL = 2
    SUSPENSION = 3
    SECURITY = 5
    TECHNICAL = 6
    BILLING = 7
    LEGAL = 8
    PRODUCT_UPDATES = 9
    TECHNICAL_INCIDENTS = 10


class ValidationState(proto.Enum):
    r"""A contact's validation state indicates whether or not it is
    the correct contact to be receiving notifications for a
    particular resource.
    """
    VALIDATION_STATE_UNSPECIFIED = 0
    VALID = 1
    INVALID = 2


__all__ = tuple(sorted(__protobuf__.manifest))
