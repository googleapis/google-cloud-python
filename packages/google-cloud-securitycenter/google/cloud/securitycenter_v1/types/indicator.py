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
        "Indicator",
    },
)


class Indicator(proto.Message):
    r"""Represents what's commonly known as an Indicator of compromise (IoC)
    in computer forensics. This is an artifact observed on a network or
    in an operating system that, with high confidence, indicates a
    computer intrusion. Reference:
    https://en.wikipedia.org/wiki/Indicator_of_compromise

    Attributes:
        ip_addresses (Sequence[str]):
            List of ip addresses associated to the
            Finding.
        domains (Sequence[str]):
            List of domains associated to the Finding.
        signatures (Sequence[google.cloud.securitycenter_v1.types.Indicator.ProcessSignature]):
            The list of matched signatures indicating
            that the given process is present in the
            environment.
        uris (Sequence[str]):
            The list of URIs associated to the Findings.
    """

    class ProcessSignature(proto.Message):
        r"""Indicates what signature matched this process.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            memory_hash_signature (google.cloud.securitycenter_v1.types.Indicator.ProcessSignature.MemoryHashSignature):
                Signature indicating that a binary family was
                matched.

                This field is a member of `oneof`_ ``signature``.
            yara_rule_signature (google.cloud.securitycenter_v1.types.Indicator.ProcessSignature.YaraRuleSignature):
                Signature indicating that a YARA rule was
                matched.

                This field is a member of `oneof`_ ``signature``.
        """

        class MemoryHashSignature(proto.Message):
            r"""A signature corresponding to memory page hashes.

            Attributes:
                binary_family (str):
                    The binary family.
                detections (Sequence[google.cloud.securitycenter_v1.types.Indicator.ProcessSignature.MemoryHashSignature.Detection]):
                    The list of memory hash detections
                    contributing to the binary family match.
            """

            class Detection(proto.Message):
                r"""Memory hash detection contributing to the binary family
                match.

                Attributes:
                    binary (str):
                        The name of the binary associated with the
                        memory hash signature detection.
                    percent_pages_matched (float):
                        The percentage of memory page hashes in the
                        signature that were matched.
                """

                binary = proto.Field(
                    proto.STRING,
                    number=2,
                )
                percent_pages_matched = proto.Field(
                    proto.DOUBLE,
                    number=3,
                )

            binary_family = proto.Field(
                proto.STRING,
                number=1,
            )
            detections = proto.RepeatedField(
                proto.MESSAGE,
                number=4,
                message="Indicator.ProcessSignature.MemoryHashSignature.Detection",
            )

        class YaraRuleSignature(proto.Message):
            r"""A signature corresponding to a YARA rule.

            Attributes:
                yara_rule (str):
                    The name of the YARA rule.
            """

            yara_rule = proto.Field(
                proto.STRING,
                number=5,
            )

        memory_hash_signature = proto.Field(
            proto.MESSAGE,
            number=6,
            oneof="signature",
            message="Indicator.ProcessSignature.MemoryHashSignature",
        )
        yara_rule_signature = proto.Field(
            proto.MESSAGE,
            number=7,
            oneof="signature",
            message="Indicator.ProcessSignature.YaraRuleSignature",
        )

    ip_addresses = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    domains = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    signatures = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=ProcessSignature,
    )
    uris = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
