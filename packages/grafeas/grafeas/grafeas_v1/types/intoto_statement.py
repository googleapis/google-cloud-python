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

from grafeas.grafeas_v1.types import intoto_provenance
from grafeas.grafeas_v1.types import slsa_provenance as g_slsa_provenance


__protobuf__ = proto.module(
    package="grafeas.v1", manifest={"InTotoStatement", "Subject",},
)


class InTotoStatement(proto.Message):
    r"""Spec defined at
    https://github.com/in-toto/attestation/tree/main/spec#statement
    The serialized InTotoStatement will be stored as
    Envelope.payload. Envelope.payloadType is always
    "application/vnd.in-toto+json".

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        type_ (str):
            Always ``https://in-toto.io/Statement/v0.1``.
        subject (Sequence[grafeas.grafeas_v1.types.Subject]):

        predicate_type (str):
            ``https://slsa.dev/provenance/v0.1`` for SlsaProvenance.
        provenance (grafeas.grafeas_v1.types.InTotoProvenance):

            This field is a member of `oneof`_ ``predicate``.
        slsa_provenance (grafeas.grafeas_v1.types.SlsaProvenance):

            This field is a member of `oneof`_ ``predicate``.
    """

    type_ = proto.Field(proto.STRING, number=1,)
    subject = proto.RepeatedField(proto.MESSAGE, number=2, message="Subject",)
    predicate_type = proto.Field(proto.STRING, number=3,)
    provenance = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="predicate",
        message=intoto_provenance.InTotoProvenance,
    )
    slsa_provenance = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="predicate",
        message=g_slsa_provenance.SlsaProvenance,
    )


class Subject(proto.Message):
    r"""

    Attributes:
        name (str):

        digest (Sequence[grafeas.grafeas_v1.types.Subject.DigestEntry]):
            ``"<ALGORITHM>": "<HEX_VALUE>"`` Algorithms can be e.g.
            sha256, sha512 See
            https://github.com/in-toto/attestation/blob/main/spec/field_types.md#DigestSet
    """

    name = proto.Field(proto.STRING, number=1,)
    digest = proto.MapField(proto.STRING, proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
