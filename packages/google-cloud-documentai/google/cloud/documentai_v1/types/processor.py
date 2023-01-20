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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.documentai_v1.types import document_schema as gcd_document_schema

__protobuf__ = proto.module(
    package="google.cloud.documentai.v1",
    manifest={
        "ProcessorVersion",
        "Processor",
    },
)


class ProcessorVersion(proto.Message):
    r"""A processor version is an implementation of a processor. Each
    processor can have multiple versions, pre-trained by Google
    internally or up-trained by the customer. At a time, a processor
    can only have one default version version. So the processor's
    behavior (when processing documents) is defined by a default
    version

    Attributes:
        name (str):
            The resource name of the processor version. Format:
            ``projects/{project}/locations/{location}/processors/{processor}/processorVersions/{processor_version}``
        display_name (str):
            The display name of the processor version.
        document_schema (google.cloud.documentai_v1.types.DocumentSchema):
            The schema of the processor version.
            Describes the output.
        state (google.cloud.documentai_v1.types.ProcessorVersion.State):
            The state of the processor version.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the processor version was created.
        kms_key_name (str):
            The KMS key name used for encryption.
        kms_key_version_name (str):
            The KMS key version with which data is
            encrypted.
        google_managed (bool):
            Denotes that this ProcessorVersion is managed
            by google.
        deprecation_info (google.cloud.documentai_v1.types.ProcessorVersion.DeprecationInfo):
            If set, information about the eventual
            deprecation of this version.
    """

    class State(proto.Enum):
        r"""The possible states of the processor version.

        Values:
            STATE_UNSPECIFIED (0):
                The processor version is in an unspecified
                state.
            DEPLOYED (1):
                The processor version is deployed and can be
                used for processing.
            DEPLOYING (2):
                The processor version is being deployed.
            UNDEPLOYED (3):
                The processor version is not deployed and
                cannot be used for processing.
            UNDEPLOYING (4):
                The processor version is being undeployed.
            CREATING (5):
                The processor version is being created.
            DELETING (6):
                The processor version is being deleted.
            FAILED (7):
                The processor version failed and is in an
                indeterminate state.
        """
        STATE_UNSPECIFIED = 0
        DEPLOYED = 1
        DEPLOYING = 2
        UNDEPLOYED = 3
        UNDEPLOYING = 4
        CREATING = 5
        DELETING = 6
        FAILED = 7

    class DeprecationInfo(proto.Message):
        r"""Information about the upcoming deprecation of this processor
        version.

        Attributes:
            deprecation_time (google.protobuf.timestamp_pb2.Timestamp):
                The time at which this processor version will
                be deprecated.
            replacement_processor_version (str):
                If set, the processor version that will be
                used as a replacement.
        """

        deprecation_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=1,
            message=timestamp_pb2.Timestamp,
        )
        replacement_processor_version: str = proto.Field(
            proto.STRING,
            number=2,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    document_schema: gcd_document_schema.DocumentSchema = proto.Field(
        proto.MESSAGE,
        number=12,
        message=gcd_document_schema.DocumentSchema,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=6,
        enum=State,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    kms_key_name: str = proto.Field(
        proto.STRING,
        number=9,
    )
    kms_key_version_name: str = proto.Field(
        proto.STRING,
        number=10,
    )
    google_managed: bool = proto.Field(
        proto.BOOL,
        number=11,
    )
    deprecation_info: DeprecationInfo = proto.Field(
        proto.MESSAGE,
        number=13,
        message=DeprecationInfo,
    )


class Processor(proto.Message):
    r"""The first-class citizen for Document AI. Each processor
    defines how to extract structural information from a document.

    Attributes:
        name (str):
            Output only. Immutable. The resource name of the processor.
            Format:
            ``projects/{project}/locations/{location}/processors/{processor}``
        type_ (str):
            The processor type, e.g., ``OCR_PROCESSOR``,
            ``INVOICE_PROCESSOR``, etc. To get a list of processors
            types, see
            [FetchProcessorTypes][google.cloud.documentai.v1.DocumentProcessorService.FetchProcessorTypes].
        display_name (str):
            The display name of the processor.
        state (google.cloud.documentai_v1.types.Processor.State):
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
            https://cloud.google.com/security-key-management.
    """

    class State(proto.Enum):
        r"""The possible states of the processor.

        Values:
            STATE_UNSPECIFIED (0):
                The processor is in an unspecified state.
            ENABLED (1):
                The processor is enabled, i.e., has an
                enabled version which can currently serve
                processing requests and all the feature
                dependencies have been successfully initialized.
            DISABLED (2):
                The processor is disabled.
            ENABLING (3):
                The processor is being enabled, will become ``ENABLED`` if
                successful.
            DISABLING (4):
                The processor is being disabled, will become ``DISABLED`` if
                successful.
            CREATING (5):
                The processor is being created, will become either
                ``ENABLED`` (for successful creation) or ``FAILED`` (for
                failed ones). Once a processor is in this state, it can then
                be used for document processing, but the feature
                dependencies of the processor might not be fully created
                yet.
            FAILED (6):
                The processor failed during creation or
                initialization of feature dependencies. The user
                should delete the processor and recreate one as
                all the functionalities of the processor are
                disabled.
            DELETING (7):
                The processor is being deleted, will be
                removed if successful.
        """
        STATE_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2
        ENABLING = 3
        DISABLING = 4
        CREATING = 5
        FAILED = 6
        DELETING = 7

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    default_processor_version: str = proto.Field(
        proto.STRING,
        number=9,
    )
    process_endpoint: str = proto.Field(
        proto.STRING,
        number=6,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    kms_key_name: str = proto.Field(
        proto.STRING,
        number=8,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
