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
    package="grafeas.v1",
    manifest={"NoteKind", "RelatedUrl", "Signature", "Envelope", "EnvelopeSignature",},
)


class NoteKind(proto.Enum):
    r"""Kind represents the kinds of notes supported."""
    NOTE_KIND_UNSPECIFIED = 0
    VULNERABILITY = 1
    BUILD = 2
    IMAGE = 3
    PACKAGE = 4
    DEPLOYMENT = 5
    DISCOVERY = 6
    ATTESTATION = 7
    UPGRADE = 8
    COMPLIANCE = 9
    DSSE_ATTESTATION = 10


class RelatedUrl(proto.Message):
    r"""Metadata for any related URL information.

    Attributes:
        url (str):
            Specific URL associated with the resource.
        label (str):
            Label to describe usage of the URL.
    """

    url = proto.Field(proto.STRING, number=1,)
    label = proto.Field(proto.STRING, number=2,)


class Signature(proto.Message):
    r"""Verifiers (e.g. Kritis implementations) MUST verify signatures with
    respect to the trust anchors defined in policy (e.g. a Kritis
    policy). Typically this means that the verifier has been configured
    with a map from ``public_key_id`` to public key material (and any
    required parameters, e.g. signing algorithm).

    In particular, verification implementations MUST NOT treat the
    signature ``public_key_id`` as anything more than a key lookup hint.
    The ``public_key_id`` DOES NOT validate or authenticate a public
    key; it only provides a mechanism for quickly selecting a public key
    ALREADY CONFIGURED on the verifier through a trusted channel.
    Verification implementations MUST reject signatures in any of the
    following circumstances:

    -  The ``public_key_id`` is not recognized by the verifier.
    -  The public key that ``public_key_id`` refers to does not verify
       the signature with respect to the payload.

    The ``signature`` contents SHOULD NOT be "attached" (where the
    payload is included with the serialized ``signature`` bytes).
    Verifiers MUST ignore any "attached" payload and only verify
    signatures with respect to explicitly provided payload (e.g. a
    ``payload`` field on the proto message that holds this Signature, or
    the canonical serialization of the proto message that holds this
    signature).

    Attributes:
        signature (bytes):
            The content of the signature, an opaque
            bytestring. The payload that this signature
            verifies MUST be unambiguously provided with the
            Signature during verification. A wrapper message
            might provide the payload explicitly.
            Alternatively, a message might have a canonical
            serialization that can always be unambiguously
            computed to derive the payload.
        public_key_id (str):
            The identifier for the public key that verifies this
            signature.

            -  The ``public_key_id`` is required.
            -  The ``public_key_id`` SHOULD be an RFC3986 conformant
               URI.
            -  When possible, the ``public_key_id`` SHOULD be an
               immutable reference, such as a cryptographic digest.

            Examples of valid ``public_key_id``\ s:

            OpenPGP V4 public key fingerprint:

            -  "openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA"
               See
               https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr
               for more details on this scheme.

            RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER
            serialization):

            -  "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU"
            -  "nih:///sha-256;703f68f42aba2c6de30f488a5ea122fef76324679c9bf89791ba95a1271589a5".
    """

    signature = proto.Field(proto.BYTES, number=1,)
    public_key_id = proto.Field(proto.STRING, number=2,)


class Envelope(proto.Message):
    r"""MUST match
    https://github.com/secure-systems-lab/dsse/blob/master/envelope.proto.
    An authenticated message of arbitrary type.

    Attributes:
        payload (bytes):

        payload_type (str):

        signatures (Sequence[grafeas.grafeas_v1.types.EnvelopeSignature]):

    """

    payload = proto.Field(proto.BYTES, number=1,)
    payload_type = proto.Field(proto.STRING, number=2,)
    signatures = proto.RepeatedField(
        proto.MESSAGE, number=3, message="EnvelopeSignature",
    )


class EnvelopeSignature(proto.Message):
    r"""

    Attributes:
        sig (bytes):

        keyid (str):

    """

    sig = proto.Field(proto.BYTES, number=1,)
    keyid = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
