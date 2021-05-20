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
    package="google.cloud.binaryauthorization.v1beta1",
    manifest={"ContinuousValidationEvent",},
)


class ContinuousValidationEvent(proto.Message):
    r"""Represents an auditing event from Continuous Validation.
    Attributes:
        pod_event (google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.ContinuousValidationPodEvent):
            Pod event.
        unsupported_policy_event (google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.UnsupportedPolicyEvent):
            Unsupported policy event.
    """

    class ContinuousValidationPodEvent(proto.Message):
        r"""An auditing event for one Pod.
        Attributes:
            pod (str):
                The name of the Pod.
            deploy_time (google.protobuf.timestamp_pb2.Timestamp):
                Deploy time of the Pod from k8s.
            end_time (google.protobuf.timestamp_pb2.Timestamp):
                Termination time of the Pod from k8s, or
                nothing if still running.
            verdict (google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.ContinuousValidationPodEvent.PolicyConformanceVerdict):
                Auditing verdict for this Pod.
            images (Sequence[google.cloud.binaryauthorization_v1beta1.types.ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails]):
                List of images with auditing details.
        """

        class PolicyConformanceVerdict(proto.Enum):
            r"""Audit time policy conformance verdict."""
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
                r"""Result of the audit."""
                AUDIT_RESULT_UNSPECIFIED = 0
                ALLOW = 1
                DENY = 2

            image = proto.Field(proto.STRING, number=1,)
            result = proto.Field(
                proto.ENUM,
                number=2,
                enum="ContinuousValidationEvent.ContinuousValidationPodEvent.ImageDetails.AuditResult",
            )
            description = proto.Field(proto.STRING, number=3,)

        pod = proto.Field(proto.STRING, number=1,)
        deploy_time = proto.Field(
            proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,
        )
        end_time = proto.Field(
            proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,
        )
        verdict = proto.Field(
            proto.ENUM,
            number=4,
            enum="ContinuousValidationEvent.ContinuousValidationPodEvent.PolicyConformanceVerdict",
        )
        images = proto.RepeatedField(
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

        description = proto.Field(proto.STRING, number=1,)

    pod_event = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="event_type",
        message=ContinuousValidationPodEvent,
    )
    unsupported_policy_event = proto.Field(
        proto.MESSAGE, number=2, oneof="event_type", message=UnsupportedPolicyEvent,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
