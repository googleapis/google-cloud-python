# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
    package="google.cloud.confidentialcomputing.v1",
    manifest={
        "Challenge",
        "CreateChallengeRequest",
        "VerifyAttestationRequest",
        "VerifyAttestationResponse",
        "GcpCredentials",
        "TpmAttestation",
    },
)


class Challenge(proto.Message):
    r"""A Challenge from the server used to guarantee freshness of
    attestations

    Attributes:
        name (str):
            Output only. The resource name for this Challenge in the
            format ``projects/*/locations/*/challenges/*``
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this Challenge
            was created
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which this Challenge
            will no longer be usable. It is also the
            expiration time for any tokens generated from
            this Challenge.
        used (bool):
            Output only. Indicates if this challenge has
            been used to generate a token.
        tpm_nonce (str):
            Output only. Identical to nonce, but as a
            string.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    expire_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    used: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    tpm_nonce: str = proto.Field(
        proto.STRING,
        number=6,
    )


class CreateChallengeRequest(proto.Message):
    r"""Message for creating a Challenge

    Attributes:
        parent (str):
            Required. The resource name of the location where the
            Challenge will be used, in the format
            ``projects/*/locations/*``.
        challenge (google.cloud.confidentialcomputing_v1.types.Challenge):
            Required. The Challenge to be created.
            Currently this field can be empty as all the
            Challenge fields are set by the server.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    challenge: "Challenge" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Challenge",
    )


class VerifyAttestationRequest(proto.Message):
    r"""A request for an OIDC token, providing all the necessary
    information needed for this service to verify the plaform state
    of the requestor.

    Attributes:
        challenge (str):
            Required. The name of the Challenge whose nonce was used to
            generate the attestation, in the format
            ``projects/*/locations/*/challenges/*``. The provided
            Challenge will be consumed, and cannot be used again.
        gcp_credentials (google.cloud.confidentialcomputing_v1.types.GcpCredentials):
            Optional. Credentials used to populate the "emails" claim in
            the claims_token.
        tpm_attestation (google.cloud.confidentialcomputing_v1.types.TpmAttestation):
            Required. The TPM-specific data provided by
            the attesting platform, used to populate any of
            the claims regarding platform state.
    """

    challenge: str = proto.Field(
        proto.STRING,
        number=1,
    )
    gcp_credentials: "GcpCredentials" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="GcpCredentials",
    )
    tpm_attestation: "TpmAttestation" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="TpmAttestation",
    )


class VerifyAttestationResponse(proto.Message):
    r"""A response once an attestation has been successfully
    verified, containing a signed OIDC token.

    Attributes:
        oidc_claims_token (str):
            Output only. Same as claims_token, but as a string.
    """

    oidc_claims_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GcpCredentials(proto.Message):
    r"""Credentials issued by GCP which are linked to the platform
    attestation. These will be verified server-side as part of
    attestaion verification.

    Attributes:
        service_account_id_tokens (MutableSequence[str]):
            Same as id_tokens, but as a string.
    """

    service_account_id_tokens: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class TpmAttestation(proto.Message):
    r"""TPM2 data containing everything necessary to validate any
    platform state measured into the TPM.

    Attributes:
        quotes (MutableSequence[google.cloud.confidentialcomputing_v1.types.TpmAttestation.Quote]):
            TPM2 PCR Quotes generated by calling TPM2_Quote on each PCR
            bank.
        tcg_event_log (bytes):
            The binary TCG Event Log containing events
            measured into the TPM by the platform firmware
            and operating system. Formatted as described in
            the "TCG PC Client Platform Firmware Profile
            Specification".
        canonical_event_log (bytes):
            An Event Log containing additional events measured into the
            TPM that are not already present in the tcg_event_log.
            Formatted as described in the "Canonical Event Log Format"
            TCG Specification.
        ak_cert (bytes):
            DER-encoded X.509 certificate of the
            Attestation Key (otherwise known as an AK or a
            TPM restricted signing key) used to generate the
            quotes.
        cert_chain (MutableSequence[bytes]):
            List of DER-encoded X.509 certificates which, together with
            the ak_cert, chain back to a trusted Root Certificate.
    """

    class Quote(proto.Message):
        r"""Information about Platform Control Registers (PCRs) including
        a signature over their values, which can be used for remote
        validation.

        Attributes:
            hash_algo (int):
                The hash algorithm of the PCR bank being quoted, encoded as
                a TPM_ALG_ID
            pcr_values (MutableMapping[int, bytes]):
                Raw binary values of each PCRs being quoted.
            raw_quote (bytes):
                TPM2 quote, encoded as a TPMS_ATTEST
            raw_signature (bytes):
                TPM2 signature, encoded as a TPMT_SIGNATURE
        """

        hash_algo: int = proto.Field(
            proto.INT32,
            number=1,
        )
        pcr_values: MutableMapping[int, bytes] = proto.MapField(
            proto.INT32,
            proto.BYTES,
            number=2,
        )
        raw_quote: bytes = proto.Field(
            proto.BYTES,
            number=3,
        )
        raw_signature: bytes = proto.Field(
            proto.BYTES,
            number=4,
        )

    quotes: MutableSequence[Quote] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Quote,
    )
    tcg_event_log: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )
    canonical_event_log: bytes = proto.Field(
        proto.BYTES,
        number=3,
    )
    ak_cert: bytes = proto.Field(
        proto.BYTES,
        number=4,
    )
    cert_chain: MutableSequence[bytes] = proto.RepeatedField(
        proto.BYTES,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
