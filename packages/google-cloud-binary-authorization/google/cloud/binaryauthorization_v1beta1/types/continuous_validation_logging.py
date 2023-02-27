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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.binaryauthorization.v1beta1",
    manifest={
        "ContinuousValidationEvent",
    },
)


class ContinuousValidationEvent(proto.Message):
    r"""Represents an auditing event from Continuous Validation.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        pod_event (google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.ContinuousValidationPodEvent):
            Pod event.

            This field is a member of `oneof`_ ``event_type``.
        unsupported_policy_event (google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.UnsupportedPolicyEvent):
            Unsupported policy event.

            This field is a member of `oneof`_ ``event_type``.
    """

    class ContinuousValidationPodEvent(proto.Message):
        r"""An auditing event for one Pod.

        Attributes:
            pod_namespace (str):
                The k8s namespace of the Pod.
            pod (str):
                The name of the Pod.
            deploy_time (google.protobuf.timestamp_pb2.Timestamp):
                Deploy time of the Pod from k8s.
            end_time (google.protobuf.timestamp_pb2.Timestamp):
                Termination time of the Pod from k8s, or
                nothing if still running.
            verdict (google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.ContinuousValidationPodEvent.PolicyConformanceVerdict):
                Auditing verdict for this Pod.
            images (MutableSequence[google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails]):
                List of images with auditing details.
        """

        class PolicyConformanceVerdict(proto.Enum):
            r"""Audit time policy conformance verdict.

            Values:
                POLICY_CONFORMANCE_VERDICT_UNSPECIFIED (0):
                    We should always have a verdict. This is an
                    error.
                VIOLATES_POLICY (1):
                    The pod violates the policy.
            """
            POLICY_CONFORMANCE_VERDICT_UNSPECIFIED = 0
            VIOLATES_POLICY = 1

        class ImageDetails(proto.Message):
            r"""Container image with auditing details.

            Attributes:
                image (str):
                    The name of the image.
                result (google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails.AuditResult):
                    The result of the audit for this image.
                description (str):
                    Description of the above result.
            """

            class AuditResult(proto.Enum):
                r"""Result of the audit.

                Values:
                    AUDIT_RESULT_UNSPECIFIED (0):
                        Unspecified result. This is an error.
                    ALLOW (1):
                        Image is allowed.
                    DENY (2):
                        Image is denied.
                """
                AUDIT_RESULT_UNSPECIFIED = 0
                ALLOW = 1
                DENY = 2

            image: str = proto.Field(
                proto.STRING,
                number=1,
            )
            result: "ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails.AuditResult" = proto.Field(
                proto.ENUM,
                number=2,
                enum="ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails.AuditResult",
            )
            description: str = proto.Field(
                proto.STRING,
                number=3,
            )

        pod_namespace: str = proto.Field(
            proto.STRING,
            number=7,
        )
        pod: str = proto.Field(
            proto.STRING,
            number=1,
        )
        deploy_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=2,
            message=timestamp_pb2.Timestamp,
        )
        end_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=3,
            message=timestamp_pb2.Timestamp,
        )
        verdict: "ContinuousValidationEvent.ContinuousValidationPodEvent.PolicyConformanceVerdict" = proto.Field(
            proto.ENUM,
            number=4,
            enum="ContinuousValidationEvent.ContinuousValidationPodEvent.PolicyConformanceVerdict",
        )
        images: MutableSequence[
            "ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=5,
            message="ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails",
        )

    class UnsupportedPolicyEvent(proto.Message):
        r"""An event describing that the project policy is unsupported by
        CV.

        Attributes:
            description (str):
                A description of the unsupported policy.
        """

        description: str = proto.Field(
            proto.STRING,
            number=1,
        )

    pod_event: ContinuousValidationPodEvent = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="event_type",
        message=ContinuousValidationPodEvent,
    )
    unsupported_policy_event: UnsupportedPolicyEvent = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="event_type",
        message=UnsupportedPolicyEvent,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
