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


__protobuf__ = proto.module(
    package="google.cloud.channel.v1", manifest={"OperationMetadata",},
)


class OperationMetadata(proto.Message):
    r"""Provides contextual information about a
    [google.longrunning.Operation][google.longrunning.Operation].

    Attributes:
        operation_type (google.cloud.channel_v1.types.OperationMetadata.OperationType):
            The RPC that initiated this Long Running
            Operation.
    """

    class OperationType(proto.Enum):
        r"""RPCs that return a Long Running Operation."""
        OPERATION_TYPE_UNSPECIFIED = 0
        CREATE_ENTITLEMENT = 1
        CHANGE_RENEWAL_SETTINGS = 3
        START_PAID_SERVICE = 5
        ACTIVATE_ENTITLEMENT = 7
        SUSPEND_ENTITLEMENT = 8
        CANCEL_ENTITLEMENT = 9
        TRANSFER_ENTITLEMENTS = 10
        TRANSFER_ENTITLEMENTS_TO_GOOGLE = 11
        CHANGE_OFFER = 14
        CHANGE_PARAMETERS = 15
        PROVISION_CLOUD_IDENTITY = 16

    operation_type = proto.Field(proto.ENUM, number=1, enum=OperationType,)


__all__ = tuple(sorted(__protobuf__.manifest))
