# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.confidentialcomputing.v1",
    manifest={
        "SigningAlgorithm",
        "TokenType",
        "Challenge",
        "CreateChallengeRequest",
        "VerifyAttestationRequest",
        "TdxCcelAttestation",
        "SevSnpAttestation",
        "VerifyAttestationResponse",
        "GcpCredentials",
        "TokenOptions",
        "TpmAttestation",
        "ConfidentialSpaceInfo",
        "SignedEntity",
        "ContainerImageSignature",
    },
)


class SigningAlgorithm(proto.Enum):
    r"""SigningAlgorithm enumerates all the supported signing
    algorithms.

    Values:
        SIGNING_ALGORITHM_UNSPECIFIED (0):
            Unspecified signing algorithm.
        RSASSA_PSS_SHA256 (1):
            RSASSA-PSS with a SHA256 digest.
        RSASSA_PKCS1V15_SHA256 (2):
            RSASSA-PKCS1 v1.5 with a SHA256 digest.
        ECDSA_P256_SHA256 (3):
            ECDSA on the P-256 Curve with a SHA256
            digest.
    """
    SIGNING_ALGORITHM_UNSPECIFIED = 0
    RSASSA_PSS_SHA256 = 1
    RSASSA_PKCS1V15_SHA256 = 2
    ECDSA_P256_SHA256 = 3


class TokenType(proto.Enum):
    r"""Token type enum contains the different types of token
    responses Confidential Space supports

    Values:
        TOKEN_TYPE_UNSPECIFIED (0):
            Unspecified token type
        TOKEN_TYPE_OIDC (1):
            OpenID Connect (OIDC) token type
        TOKEN_TYPE_PKI (2):
            Public Key Infrastructure (PKI) token type
        TOKEN_TYPE_LIMITED_AWS (3):
            Limited claim token type for AWS integration
    """
    TOKEN_TYPE_UNSPECIFIED = 0
    TOKEN_TYPE_OIDC = 1
    TOKEN_TYPE_PKI = 2
    TOKEN_TYPE_LIMITED_AWS = 3


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

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        td_ccel (google.cloud.confidentialcomputing_v1.types.TdxCcelAttestation):
            Optional. A TDX with CCEL and RTMR
            Attestation Quote.

            This field is a member of `oneof`_ ``tee_attestation``.
        sev_snp_attestation (google.cloud.confidentialcomputing_v1.types.SevSnpAttestation):
            Optional. An SEV-SNP Attestation Report.

            This field is a member of `oneof`_ ``tee_attestation``.
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
        confidential_space_info (google.cloud.confidentialcomputing_v1.types.ConfidentialSpaceInfo):
            Optional. Optional information related to the
            Confidential Space TEE.
        token_options (google.cloud.confidentialcomputing_v1.types.TokenOptions):
            Optional. A collection of optional,
            workload-specified claims that modify the token
            output.
    """

    td_ccel: "TdxCcelAttestation" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="tee_attestation",
        message="TdxCcelAttestation",
    )
    sev_snp_attestation: "SevSnpAttestation" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="tee_attestation",
        message="SevSnpAttestation",
    )
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
    confidential_space_info: "ConfidentialSpaceInfo" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="ConfidentialSpaceInfo",
    )
    token_options: "TokenOptions" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="TokenOptions",
    )


class TdxCcelAttestation(proto.Message):
    r"""A TDX Attestation quote.

    Attributes:
        ccel_acpi_table (bytes):
            Optional. The Confidential Computing Event
            Log (CCEL) ACPI table. Formatted as described in
            the ACPI Specification 6.5.
        ccel_data (bytes):
            Optional. The CCEL event log. Formatted as
            described in the UEFI 2.10.
        canonical_event_log (bytes):
            Optional. An Event Log containing additional
            events measured into the RTMR that are not
            already present in the CCEL.
        td_quote (bytes):
            Optional. The TDX attestation quote from the
            guest. It contains the RTMR values.
    """

    ccel_acpi_table: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )
    ccel_data: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )
    canonical_event_log: bytes = proto.Field(
        proto.BYTES,
        number=3,
    )
    td_quote: bytes = proto.Field(
        proto.BYTES,
        number=4,
    )


class SevSnpAttestation(proto.Message):
    r"""An SEV-SNP Attestation Report.
    Contains the attestation report and the certificate bundle that
    the client collects.

    Attributes:
        report (bytes):
            Optional. The SEV-SNP Attestation Report Format is in
            revision 1.55, §7.3 Attestation, Table 22.
            ATTESTATION_REPORT Structure in this document:
            https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/specifications/56860.pdf
        aux_blob (bytes):
            Optional. Certificate bundle defined in the GHCB protocol
            definition Format is documented in GHCB revision 2.03,
            section 4.1.8.1 struct cert_table in this document:
            https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/specifications/56421.pdf
    """

    report: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )
    aux_blob: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class VerifyAttestationResponse(proto.Message):
    r"""A response once an attestation has been successfully
    verified, containing a signed OIDC token.

    Attributes:
        oidc_claims_token (str):
            Output only. Same as claims_token, but as a string.
        partial_errors (MutableSequence[google.rpc.status_pb2.Status]):
            Output only. A list of messages that carry
            the partial error details related to
            VerifyAttestation.
    """

    oidc_claims_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    partial_errors: MutableSequence[status_pb2.Status] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=status_pb2.Status,
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


class TokenOptions(proto.Message):
    r"""Options to modify claims in the token to generate
    custom-purpose tokens.

    Attributes:
        audience (str):
            Optional. Optional string to issue the token
            with a custom audience claim. Required if one or
            more nonces are specified.
        nonce (MutableSequence[str]):
            Optional. Optional parameter to place one or more nonces in
            the eat_nonce claim in the output token. The minimum size
            for JSON-encoded EATs is 10 bytes and the maximum size is 74
            bytes.
        token_type (google.cloud.confidentialcomputing_v1.types.TokenType):
            Optional. Optional token type to select what
            type of token to return.
    """

    audience: str = proto.Field(
        proto.STRING,
        number=1,
    )
    nonce: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    token_type: "TokenType" = proto.Field(
        proto.ENUM,
        number=3,
        enum="TokenType",
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


class ConfidentialSpaceInfo(proto.Message):
    r"""ConfidentialSpaceInfo contains information related to the
    Confidential Space TEE.

    Attributes:
        signed_entities (MutableSequence[google.cloud.confidentialcomputing_v1.types.SignedEntity]):
            Optional. A list of signed entities
            containing container image signatures that can
            be used for server-side signature verification.
    """

    signed_entities: MutableSequence["SignedEntity"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SignedEntity",
    )


class SignedEntity(proto.Message):
    r"""SignedEntity represents an OCI image object containing
    everything necessary to verify container image signatures.

    Attributes:
        container_image_signatures (MutableSequence[google.cloud.confidentialcomputing_v1.types.ContainerImageSignature]):
            Optional. A list of container image
            signatures attached to an OCI image object.
    """

    container_image_signatures: MutableSequence[
        "ContainerImageSignature"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ContainerImageSignature",
    )


class ContainerImageSignature(proto.Message):
    r"""ContainerImageSignature holds necessary metadata to verify a
    container image signature.

    Attributes:
        payload (bytes):
            Optional. The binary signature payload following the
            SimpleSigning format
            https://github.com/sigstore/cosign/blob/main/specs/SIGNATURE_SPEC.md#simple-signing.
            This payload includes the container image digest.
        signature (bytes):
            Optional. A signature over the payload. The container image
            digest is incorporated into the signature as follows:

            1. Generate a SimpleSigning format payload that includes the
               container image digest.
            2. Generate a signature over SHA256 digest of the payload.
               The signature generation process can be represented as
               follows:
               ``Sign(sha256(SimpleSigningPayload(sha256(Image Manifest))))``
        public_key (bytes):
            Optional. Reserved for future use.
        sig_alg (google.cloud.confidentialcomputing_v1.types.SigningAlgorithm):
            Optional. Reserved for future use.
    """

    payload: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )
    signature: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )
    public_key: bytes = proto.Field(
        proto.BYTES,
        number=3,
    )
    sig_alg: "SigningAlgorithm" = proto.Field(
        proto.ENUM,
        number=4,
        enum="SigningAlgorithm",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
