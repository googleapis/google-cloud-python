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

import proto  # type: ignore

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.binaryauthorization.v1beta1',
    manifest={
        'Policy',
        'AdmissionWhitelistPattern',
        'AdmissionRule',
        'Attestor',
        'UserOwnedDrydockNote',
        'PkixPublicKey',
        'AttestorPublicKey',
    },
)


class Policy(proto.Message):
    r"""A [policy][google.cloud.binaryauthorization.v1beta1.Policy] for
    Binary Authorization.

    Attributes:
        name (str):
            Output only. The resource name, in the format
            ``projects/*/policy``. There is at most one policy per
            project.
        description (str):
            Optional. A descriptive comment.
        global_policy_evaluation_mode (google.cloud.binaryauthorization_v1beta1.types.Policy.GlobalPolicyEvaluationMode):
            Optional. Controls the evaluation of a
            Google-maintained global admission policy for
            common system-level images. Images not covered
            by the global policy will be subject to the
            project admission policy. This setting has no
            effect when specified inside a global admission
            policy.
        admission_whitelist_patterns (MutableSequence[google.cloud.binaryauthorization_v1beta1.types.AdmissionWhitelistPattern]):
            Optional. Admission policy allowlisting. A
            matching admission request will always be
            permitted. This feature is typically used to
            exclude Google or third-party infrastructure
            images from Binary Authorization policies.
        cluster_admission_rules (MutableMapping[str, google.cloud.binaryauthorization_v1beta1.types.AdmissionRule]):
            Optional. Per-cluster admission rules. Cluster spec format:
            ``location.clusterId``. There can be at most one admission
            rule per cluster spec. A ``location`` is either a compute
            zone (e.g. us-central1-a) or a region (e.g. us-central1).
            For ``clusterId`` syntax restrictions see
            https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters.
        kubernetes_namespace_admission_rules (MutableMapping[str, google.cloud.binaryauthorization_v1beta1.types.AdmissionRule]):
            Optional. Per-kubernetes-namespace admission rules. K8s
            namespace spec format: ``[a-z.-]+``, e.g. ``some-namespace``
        kubernetes_service_account_admission_rules (MutableMapping[str, google.cloud.binaryauthorization_v1beta1.types.AdmissionRule]):
            Optional. Per-kubernetes-service-account admission rules.
            Service account spec format: ``namespace:serviceaccount``.
            e.g. ``test-ns:default``
        istio_service_identity_admission_rules (MutableMapping[str, google.cloud.binaryauthorization_v1beta1.types.AdmissionRule]):
            Optional. Per-istio-service-identity admission rules. Istio
            service identity spec format:
            ``spiffe://<domain>/ns/<namespace>/sa/<serviceaccount>`` or
            ``<domain>/ns/<namespace>/sa/<serviceaccount>`` e.g.
            ``spiffe://example.com/ns/test-ns/sa/default``
        default_admission_rule (google.cloud.binaryauthorization_v1beta1.types.AdmissionRule):
            Required. Default admission rule for a
            cluster without a per-cluster, per-
            kubernetes-service-account, or
            per-istio-service-identity admission rule.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the policy was last
            updated.
    """
    class GlobalPolicyEvaluationMode(proto.Enum):
        r"""

        Values:
            GLOBAL_POLICY_EVALUATION_MODE_UNSPECIFIED (0):
                Not specified: DISABLE is assumed.
            ENABLE (1):
                Enables system policy evaluation.
            DISABLE (2):
                Disables system policy evaluation.
        """
        GLOBAL_POLICY_EVALUATION_MODE_UNSPECIFIED = 0
        ENABLE = 1
        DISABLE = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=6,
    )
    global_policy_evaluation_mode: GlobalPolicyEvaluationMode = proto.Field(
        proto.ENUM,
        number=7,
        enum=GlobalPolicyEvaluationMode,
    )
    admission_whitelist_patterns: MutableSequence['AdmissionWhitelistPattern'] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message='AdmissionWhitelistPattern',
    )
    cluster_admission_rules: MutableMapping[str, 'AdmissionRule'] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=3,
        message='AdmissionRule',
    )
    kubernetes_namespace_admission_rules: MutableMapping[str, 'AdmissionRule'] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=10,
        message='AdmissionRule',
    )
    kubernetes_service_account_admission_rules: MutableMapping[str, 'AdmissionRule'] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=8,
        message='AdmissionRule',
    )
    istio_service_identity_admission_rules: MutableMapping[str, 'AdmissionRule'] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=9,
        message='AdmissionRule',
    )
    default_admission_rule: 'AdmissionRule' = proto.Field(
        proto.MESSAGE,
        number=4,
        message='AdmissionRule',
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


class AdmissionWhitelistPattern(proto.Message):
    r"""An [admission allowlist
    pattern][google.cloud.binaryauthorization.v1beta1.AdmissionWhitelistPattern]
    exempts images from checks by [admission
    rules][google.cloud.binaryauthorization.v1beta1.AdmissionRule].

    Attributes:
        name_pattern (str):
            An image name pattern to allowlist, in the form
            ``registry/path/to/image``. This supports a trailing ``*``
            as a wildcard, but this is allowed only in text after the
            ``registry/`` part. ``*`` wildcard does not match ``/``,
            i.e., ``gcr.io/nginx*`` matches ``gcr.io/nginx@latest``, but
            it does not match ``gcr.io/nginx/image``. This also supports
            a trailing ``**`` wildcard which matches subdirectories,
            i.e., ``gcr.io/nginx**`` matches ``gcr.io/nginx/image``.
    """

    name_pattern: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AdmissionRule(proto.Message):
    r"""An [admission
    rule][google.cloud.binaryauthorization.v1beta1.AdmissionRule]
    specifies either that all container images used in a pod creation
    request must be attested to by one or more
    [attestors][google.cloud.binaryauthorization.v1beta1.Attestor], that
    all pod creations will be allowed, or that all pod creations will be
    denied.

    Images matching an [admission allowlist
    pattern][google.cloud.binaryauthorization.v1beta1.AdmissionWhitelistPattern]
    are exempted from admission rules and will never block a pod
    creation.

    Attributes:
        evaluation_mode (google.cloud.binaryauthorization_v1beta1.types.AdmissionRule.EvaluationMode):
            Required. How this admission rule will be
            evaluated.
        require_attestations_by (MutableSequence[str]):
            Optional. The resource names of the attestors that must
            attest to a container image, in the format
            ``projects/*/attestors/*``. Each attestor must exist before
            a policy can reference it. To add an attestor to a policy
            the principal issuing the policy change request must be able
            to read the attestor resource.

            Note: this field must be non-empty when the evaluation_mode
            field specifies REQUIRE_ATTESTATION, otherwise it must be
            empty.
        enforcement_mode (google.cloud.binaryauthorization_v1beta1.types.AdmissionRule.EnforcementMode):
            Required. The action when a pod creation is
            denied by the admission rule.
    """
    class EvaluationMode(proto.Enum):
        r"""

        Values:
            EVALUATION_MODE_UNSPECIFIED (0):
                Do not use.
            ALWAYS_ALLOW (1):
                This rule allows all all pod creations.
            REQUIRE_ATTESTATION (2):
                This rule allows a pod creation if all the attestors listed
                in ``require_attestations_by`` have valid attestations for
                all of the images in the pod spec.
            ALWAYS_DENY (3):
                This rule denies all pod creations.
        """
        EVALUATION_MODE_UNSPECIFIED = 0
        ALWAYS_ALLOW = 1
        REQUIRE_ATTESTATION = 2
        ALWAYS_DENY = 3

    class EnforcementMode(proto.Enum):
        r"""Defines the possible actions when a pod creation is denied by
        an admission rule.

        Values:
            ENFORCEMENT_MODE_UNSPECIFIED (0):
                Do not use.
            ENFORCED_BLOCK_AND_AUDIT_LOG (1):
                Enforce the admission rule by blocking the
                pod creation.
            DRYRUN_AUDIT_LOG_ONLY (2):
                Dryrun mode: Audit logging only.  This will
                allow the pod creation as if the admission
                request had specified break-glass.
        """
        ENFORCEMENT_MODE_UNSPECIFIED = 0
        ENFORCED_BLOCK_AND_AUDIT_LOG = 1
        DRYRUN_AUDIT_LOG_ONLY = 2

    evaluation_mode: EvaluationMode = proto.Field(
        proto.ENUM,
        number=1,
        enum=EvaluationMode,
    )
    require_attestations_by: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    enforcement_mode: EnforcementMode = proto.Field(
        proto.ENUM,
        number=3,
        enum=EnforcementMode,
    )


class Attestor(proto.Message):
    r"""An [attestor][google.cloud.binaryauthorization.v1beta1.Attestor]
    that attests to container image artifacts. An existing attestor
    cannot be modified except where indicated.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. The resource name, in the format:
            ``projects/*/attestors/*``. This field may not be updated.
        description (str):
            Optional. A descriptive comment.  This field
            may be updated. The field may be displayed in
            chooser dialogs.
        user_owned_drydock_note (google.cloud.binaryauthorization_v1beta1.types.UserOwnedDrydockNote):
            A Drydock ATTESTATION_AUTHORITY Note, created by the user.

            This field is a member of `oneof`_ ``attestor_type``.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the attestor was last
            updated.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=6,
    )
    user_owned_drydock_note: 'UserOwnedDrydockNote' = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof='attestor_type',
        message='UserOwnedDrydockNote',
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


class UserOwnedDrydockNote(proto.Message):
    r"""An [user owned drydock
    note][google.cloud.binaryauthorization.v1beta1.UserOwnedDrydockNote]
    references a Drydock ATTESTATION_AUTHORITY Note created by the user.

    Attributes:
        note_reference (str):
            Required. The Drydock resource name of a
            ATTESTATION_AUTHORITY Note, created by the user, in the
            format: ``projects/*/notes/*`` (or the legacy
            ``providers/*/notes/*``). This field may not be updated.

            An attestation by this attestor is stored as a Drydock
            ATTESTATION_AUTHORITY Occurrence that names a container
            image and that links to this Note. Drydock is an external
            dependency.
        public_keys (MutableSequence[google.cloud.binaryauthorization_v1beta1.types.AttestorPublicKey]):
            Optional. Public keys that verify
            attestations signed by this attestor.  This
            field may be updated.

            If this field is non-empty, one of the specified
            public keys must verify that an attestation was
            signed by this attestor for the image specified
            in the admission request.

            If this field is empty, this attestor always
            returns that no valid attestations exist.
        delegation_service_account_email (str):
            Output only. This field will contain the service account
            email address that this Attestor will use as the principal
            when querying Container Analysis. Attestor administrators
            must grant this service account the IAM role needed to read
            attestations from the [note_reference][Note] in Container
            Analysis (``containeranalysis.notes.occurrences.viewer``).

            This email address is fixed for the lifetime of the
            Attestor, but callers should not make any other assumptions
            about the service account email; future versions may use an
            email based on a different naming pattern.
    """

    note_reference: str = proto.Field(
        proto.STRING,
        number=1,
    )
    public_keys: MutableSequence['AttestorPublicKey'] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message='AttestorPublicKey',
    )
    delegation_service_account_email: str = proto.Field(
        proto.STRING,
        number=3,
    )


class PkixPublicKey(proto.Message):
    r"""A public key in the PkixPublicKey format (see
    https://tools.ietf.org/html/rfc5280#section-4.1.2.7 for
    details). Public keys of this type are typically textually
    encoded using the PEM format.

    Attributes:
        public_key_pem (str):
            A PEM-encoded public key, as described in
            https://tools.ietf.org/html/rfc7468#section-13
        signature_algorithm (google.cloud.binaryauthorization_v1beta1.types.PkixPublicKey.SignatureAlgorithm):
            The signature algorithm used to verify a message against a
            signature using this key. These signature algorithm must
            match the structure and any object identifiers encoded in
            ``public_key_pem`` (i.e. this algorithm must match that of
            the public key).
    """
    class SignatureAlgorithm(proto.Enum):
        r"""Represents a signature algorithm and other information
        necessary to verify signatures with a given public key. This is
        based primarily on the public key types supported by Tink's
        PemKeyType, which is in turn based on KMS's supported signing
        algorithms. See https://cloud.google.com/kms/docs/algorithms. In
        the future, BinAuthz might support additional public key types
        independently of Tink and/or KMS.

        Values:
            SIGNATURE_ALGORITHM_UNSPECIFIED (0):
                Not specified.
            RSA_PSS_2048_SHA256 (1):
                RSASSA-PSS 2048 bit key with a SHA256 digest.
            RSA_PSS_3072_SHA256 (2):
                RSASSA-PSS 3072 bit key with a SHA256 digest.
            RSA_PSS_4096_SHA256 (3):
                RSASSA-PSS 4096 bit key with a SHA256 digest.
            RSA_PSS_4096_SHA512 (4):
                RSASSA-PSS 4096 bit key with a SHA512 digest.
            RSA_SIGN_PKCS1_2048_SHA256 (5):
                RSASSA-PKCS1-v1_5 with a 2048 bit key and a SHA256 digest.
            RSA_SIGN_PKCS1_3072_SHA256 (6):
                RSASSA-PKCS1-v1_5 with a 3072 bit key and a SHA256 digest.
            RSA_SIGN_PKCS1_4096_SHA256 (7):
                RSASSA-PKCS1-v1_5 with a 4096 bit key and a SHA256 digest.
            RSA_SIGN_PKCS1_4096_SHA512 (8):
                RSASSA-PKCS1-v1_5 with a 4096 bit key and a SHA512 digest.
            ECDSA_P256_SHA256 (9):
                ECDSA on the NIST P-256 curve with a SHA256
                digest.
            EC_SIGN_P256_SHA256 (9):
                ECDSA on the NIST P-256 curve with a SHA256
                digest.
            ECDSA_P384_SHA384 (10):
                ECDSA on the NIST P-384 curve with a SHA384
                digest.
            EC_SIGN_P384_SHA384 (10):
                ECDSA on the NIST P-384 curve with a SHA384
                digest.
            ECDSA_P521_SHA512 (11):
                ECDSA on the NIST P-521 curve with a SHA512
                digest.
            EC_SIGN_P521_SHA512 (11):
                ECDSA on the NIST P-521 curve with a SHA512
                digest.
        """
        _pb_options = {'allow_alias': True}
        SIGNATURE_ALGORITHM_UNSPECIFIED = 0
        RSA_PSS_2048_SHA256 = 1
        RSA_PSS_3072_SHA256 = 2
        RSA_PSS_4096_SHA256 = 3
        RSA_PSS_4096_SHA512 = 4
        RSA_SIGN_PKCS1_2048_SHA256 = 5
        RSA_SIGN_PKCS1_3072_SHA256 = 6
        RSA_SIGN_PKCS1_4096_SHA256 = 7
        RSA_SIGN_PKCS1_4096_SHA512 = 8
        ECDSA_P256_SHA256 = 9
        EC_SIGN_P256_SHA256 = 9
        ECDSA_P384_SHA384 = 10
        EC_SIGN_P384_SHA384 = 10
        ECDSA_P521_SHA512 = 11
        EC_SIGN_P521_SHA512 = 11

    public_key_pem: str = proto.Field(
        proto.STRING,
        number=1,
    )
    signature_algorithm: SignatureAlgorithm = proto.Field(
        proto.ENUM,
        number=2,
        enum=SignatureAlgorithm,
    )


class AttestorPublicKey(proto.Message):
    r"""An [attestor public
    key][google.cloud.binaryauthorization.v1beta1.AttestorPublicKey]
    that will be used to verify attestations signed by this attestor.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        comment (str):
            Optional. A descriptive comment. This field
            may be updated.
        id (str):
            The ID of this public key. Signatures verified by BinAuthz
            must include the ID of the public key that can be used to
            verify them, and that ID must match the contents of this
            field exactly. Additional restrictions on this field can be
            imposed based on which public key type is encapsulated. See
            the documentation on ``public_key`` cases below for details.
        ascii_armored_pgp_public_key (str):
            ASCII-armored representation of a PGP public key, as the
            entire output by the command
            ``gpg --export --armor foo@example.com`` (either LF or CRLF
            line endings). When using this field, ``id`` should be left
            blank. The BinAuthz API handlers will calculate the ID and
            fill it in automatically. BinAuthz computes this ID as the
            OpenPGP RFC4880 V4 fingerprint, represented as upper-case
            hex. If ``id`` is provided by the caller, it will be
            overwritten by the API-calculated ID.

            This field is a member of `oneof`_ ``public_key``.
        pkix_public_key (google.cloud.binaryauthorization_v1beta1.types.PkixPublicKey):
            A raw PKIX SubjectPublicKeyInfo format public key.

            NOTE: ``id`` may be explicitly provided by the caller when
            using this type of public key, but it MUST be a valid
            RFC3986 URI. If ``id`` is left blank, a default one will be
            computed based on the digest of the DER encoding of the
            public key.

            This field is a member of `oneof`_ ``public_key``.
    """

    comment: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    ascii_armored_pgp_public_key: str = proto.Field(
        proto.STRING,
        number=3,
        oneof='public_key',
    )
    pkix_public_key: 'PkixPublicKey' = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof='public_key',
        message='PkixPublicKey',
    )


__all__ = tuple(sorted(__protobuf__.manifest))
