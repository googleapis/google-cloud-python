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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta3", manifest={"Processor",},
)


class Processor(proto.Message):
    r"""The first-class citizen for DocumentAI. Each processor
    defines how to extract structural information from a document.

    Attributes:
        name (str):
            Output only. Immutable. The resource name of
            the processor. Format:
            projects/{project}/locations/{location}/processors/{processor}
        type_ (str):
            The processor type.
        display_name (str):
            The display name of the processor.
        state (google.cloud.documentai_v1beta3.types.Processor.State):
            Output only. The state of the processor.
        default_processor_version (str):
            The default processor version.
        process_endpoint (str):
            Output only. Immutable. The http endpoint
            that can be called to invoke processing.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the processor was created.
        kms_key_name (str):
            The KMS key used for encryption/decryption in
            CMEK scenarios. See
            https://cloud.google.com/security-key-
            management.
    """

    class State(proto.Enum):
        r"""The possible states of the processor."""
        STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        ENABLING = 3
        DISABLING = 4
        CREATING = 5
        FAILED = 6
        DELETING = 7

    name = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=3,)
    state = proto.Field(proto.ENUM, number=4, enum=State,)
    default_processor_version = proto.Field(proto.STRING, number=9,)
    process_endpoint = proto.Field(proto.STRING, number=6,)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    kms_key_name = proto.Field(proto.STRING, number=8,)


__all__ = tuple(sorted(__protobuf__.manifest))
