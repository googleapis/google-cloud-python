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

from google.cloud.kms_v1.types import resources
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.kms.v1",
    manifest={
        "ListKeyRingsRequest",
        "ListCryptoKeysRequest",
        "ListCryptoKeyVersionsRequest",
        "ListImportJobsRequest",
        "ListKeyRingsResponse",
        "ListCryptoKeysResponse",
        "ListCryptoKeyVersionsResponse",
        "ListImportJobsResponse",
        "GetKeyRingRequest",
        "GetCryptoKeyRequest",
        "GetCryptoKeyVersionRequest",
        "GetPublicKeyRequest",
        "GetImportJobRequest",
        "CreateKeyRingRequest",
        "CreateCryptoKeyRequest",
        "CreateCryptoKeyVersionRequest",
        "ImportCryptoKeyVersionRequest",
        "CreateImportJobRequest",
        "UpdateCryptoKeyRequest",
        "UpdateCryptoKeyVersionRequest",
        "EncryptRequest",
        "DecryptRequest",
        "AsymmetricSignRequest",
        "AsymmetricDecryptRequest",
        "DecryptResponse",
        "EncryptResponse",
        "AsymmetricSignResponse",
        "AsymmetricDecryptResponse",
        "UpdateCryptoKeyPrimaryVersionRequest",
        "DestroyCryptoKeyVersionRequest",
        "RestoreCryptoKeyVersionRequest",
        "Digest",
        "LocationMetadata",
    },
)


class ListKeyRingsRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.ListKeyRings][google.cloud.kms.v1.KeyManagementService.ListKeyRings].

    Attributes:
        parent (str):
            Required. The resource name of the location associated with
            the [KeyRings][google.cloud.kms.v1.KeyRing], in the format
            ``projects/*/locations/*``.
        page_size (int):
            Optional. Optional limit on the number of
            [KeyRings][google.cloud.kms.v1.KeyRing] to include in the
            response. Further [KeyRings][google.cloud.kms.v1.KeyRing]
            can subsequently be obtained by including the
            [ListKeyRingsResponse.next_page_token][google.cloud.kms.v1.ListKeyRingsResponse.next_page_token]
            in a subsequent request. If unspecified, the server will
            pick an appropriate default.
        page_token (str):
            Optional. Optional pagination token, returned earlier via
            [ListKeyRingsResponse.next_page_token][google.cloud.kms.v1.ListKeyRingsResponse.next_page_token].
        filter (str):
            Optional. Only include resources that match the filter in
            the response. For more information, see `Sorting and
            filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
        order_by (str):
            Optional. Specify how the results should be sorted. If not
            specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListCryptoKeysRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.ListCryptoKeys][google.cloud.kms.v1.KeyManagementService.ListCryptoKeys].

    Attributes:
        parent (str):
            Required. The resource name of the
            [KeyRing][google.cloud.kms.v1.KeyRing] to list, in the
            format ``projects/*/locations/*/keyRings/*``.
        page_size (int):
            Optional. Optional limit on the number of
            [CryptoKeys][google.cloud.kms.v1.CryptoKey] to include in
            the response. Further
            [CryptoKeys][google.cloud.kms.v1.CryptoKey] can subsequently
            be obtained by including the
            [ListCryptoKeysResponse.next_page_token][google.cloud.kms.v1.ListCryptoKeysResponse.next_page_token]
            in a subsequent request. If unspecified, the server will
            pick an appropriate default.
        page_token (str):
            Optional. Optional pagination token, returned earlier via
            [ListCryptoKeysResponse.next_page_token][google.cloud.kms.v1.ListCryptoKeysResponse.next_page_token].
        version_view (google.cloud.kms_v1.types.CryptoKeyVersion.CryptoKeyVersionView):
            The fields of the primary version to include
            in the response.
        filter (str):
            Optional. Only include resources that match the filter in
            the response. For more information, see `Sorting and
            filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
        order_by (str):
            Optional. Specify how the results should be sorted. If not
            specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    version_view = proto.Field(
        proto.ENUM, number=4, enum=resources.CryptoKeyVersion.CryptoKeyVersionView,
    )
    filter = proto.Field(proto.STRING, number=5,)
    order_by = proto.Field(proto.STRING, number=6,)


class ListCryptoKeyVersionsRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.ListCryptoKeyVersions][google.cloud.kms.v1.KeyManagementService.ListCryptoKeyVersions].

    Attributes:
        parent (str):
            Required. The resource name of the
            [CryptoKey][google.cloud.kms.v1.CryptoKey] to list, in the
            format ``projects/*/locations/*/keyRings/*/cryptoKeys/*``.
        page_size (int):
            Optional. Optional limit on the number of
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion] to
            include in the response. Further
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
            can subsequently be obtained by including the
            [ListCryptoKeyVersionsResponse.next_page_token][google.cloud.kms.v1.ListCryptoKeyVersionsResponse.next_page_token]
            in a subsequent request. If unspecified, the server will
            pick an appropriate default.
        page_token (str):
            Optional. Optional pagination token, returned earlier via
            [ListCryptoKeyVersionsResponse.next_page_token][google.cloud.kms.v1.ListCryptoKeyVersionsResponse.next_page_token].
        view (google.cloud.kms_v1.types.CryptoKeyVersion.CryptoKeyVersionView):
            The fields to include in the response.
        filter (str):
            Optional. Only include resources that match the filter in
            the response. For more information, see `Sorting and
            filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
        order_by (str):
            Optional. Specify how the results should be sorted. If not
            specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    view = proto.Field(
        proto.ENUM, number=4, enum=resources.CryptoKeyVersion.CryptoKeyVersionView,
    )
    filter = proto.Field(proto.STRING, number=5,)
    order_by = proto.Field(proto.STRING, number=6,)


class ListImportJobsRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.ListImportJobs][google.cloud.kms.v1.KeyManagementService.ListImportJobs].

    Attributes:
        parent (str):
            Required. The resource name of the
            [KeyRing][google.cloud.kms.v1.KeyRing] to list, in the
            format ``projects/*/locations/*/keyRings/*``.
        page_size (int):
            Optional. Optional limit on the number of
            [ImportJobs][google.cloud.kms.v1.ImportJob] to include in
            the response. Further
            [ImportJobs][google.cloud.kms.v1.ImportJob] can subsequently
            be obtained by including the
            [ListImportJobsResponse.next_page_token][google.cloud.kms.v1.ListImportJobsResponse.next_page_token]
            in a subsequent request. If unspecified, the server will
            pick an appropriate default.
        page_token (str):
            Optional. Optional pagination token, returned earlier via
            [ListImportJobsResponse.next_page_token][google.cloud.kms.v1.ListImportJobsResponse.next_page_token].
        filter (str):
            Optional. Only include resources that match the filter in
            the response. For more information, see `Sorting and
            filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
        order_by (str):
            Optional. Specify how the results should be sorted. If not
            specified, the results will be sorted in the default order.
            For more information, see `Sorting and filtering list
            results <https://cloud.google.com/kms/docs/sorting-and-filtering>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListKeyRingsResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.ListKeyRings][google.cloud.kms.v1.KeyManagementService.ListKeyRings].

    Attributes:
        key_rings (Sequence[google.cloud.kms_v1.types.KeyRing]):
            The list of [KeyRings][google.cloud.kms.v1.KeyRing].
        next_page_token (str):
            A token to retrieve next page of results. Pass this value in
            [ListKeyRingsRequest.page_token][google.cloud.kms.v1.ListKeyRingsRequest.page_token]
            to retrieve the next page of results.
        total_size (int):
            The total number of [KeyRings][google.cloud.kms.v1.KeyRing]
            that matched the query.
    """

    @property
    def raw_page(self):
        return self

    key_rings = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.KeyRing,)
    next_page_token = proto.Field(proto.STRING, number=2,)
    total_size = proto.Field(proto.INT32, number=3,)


class ListCryptoKeysResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.ListCryptoKeys][google.cloud.kms.v1.KeyManagementService.ListCryptoKeys].

    Attributes:
        crypto_keys (Sequence[google.cloud.kms_v1.types.CryptoKey]):
            The list of [CryptoKeys][google.cloud.kms.v1.CryptoKey].
        next_page_token (str):
            A token to retrieve next page of results. Pass this value in
            [ListCryptoKeysRequest.page_token][google.cloud.kms.v1.ListCryptoKeysRequest.page_token]
            to retrieve the next page of results.
        total_size (int):
            The total number of
            [CryptoKeys][google.cloud.kms.v1.CryptoKey] that matched the
            query.
    """

    @property
    def raw_page(self):
        return self

    crypto_keys = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.CryptoKey,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    total_size = proto.Field(proto.INT32, number=3,)


class ListCryptoKeyVersionsResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.ListCryptoKeyVersions][google.cloud.kms.v1.KeyManagementService.ListCryptoKeyVersions].

    Attributes:
        crypto_key_versions (Sequence[google.cloud.kms_v1.types.CryptoKeyVersion]):
            The list of
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion].
        next_page_token (str):
            A token to retrieve next page of results. Pass this value in
            [ListCryptoKeyVersionsRequest.page_token][google.cloud.kms.v1.ListCryptoKeyVersionsRequest.page_token]
            to retrieve the next page of results.
        total_size (int):
            The total number of
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion]
            that matched the query.
    """

    @property
    def raw_page(self):
        return self

    crypto_key_versions = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.CryptoKeyVersion,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    total_size = proto.Field(proto.INT32, number=3,)


class ListImportJobsResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.ListImportJobs][google.cloud.kms.v1.KeyManagementService.ListImportJobs].

    Attributes:
        import_jobs (Sequence[google.cloud.kms_v1.types.ImportJob]):
            The list of [ImportJobs][google.cloud.kms.v1.ImportJob].
        next_page_token (str):
            A token to retrieve next page of results. Pass this value in
            [ListImportJobsRequest.page_token][google.cloud.kms.v1.ListImportJobsRequest.page_token]
            to retrieve the next page of results.
        total_size (int):
            The total number of
            [ImportJobs][google.cloud.kms.v1.ImportJob] that matched the
            query.
    """

    @property
    def raw_page(self):
        return self

    import_jobs = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.ImportJob,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    total_size = proto.Field(proto.INT32, number=3,)


class GetKeyRingRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.GetKeyRing][google.cloud.kms.v1.KeyManagementService.GetKeyRing].

    Attributes:
        name (str):
            Required. The [name][google.cloud.kms.v1.KeyRing.name] of
            the [KeyRing][google.cloud.kms.v1.KeyRing] to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetCryptoKeyRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.GetCryptoKey][google.cloud.kms.v1.KeyManagementService.GetCryptoKey].

    Attributes:
        name (str):
            Required. The [name][google.cloud.kms.v1.CryptoKey.name] of
            the [CryptoKey][google.cloud.kms.v1.CryptoKey] to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetCryptoKeyVersionRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.GetCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.GetCryptoKeyVersion].

    Attributes:
        name (str):
            Required. The
            [name][google.cloud.kms.v1.CryptoKeyVersion.name] of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] to
            get.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetPublicKeyRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.GetPublicKey][google.cloud.kms.v1.KeyManagementService.GetPublicKey].

    Attributes:
        name (str):
            Required. The
            [name][google.cloud.kms.v1.CryptoKeyVersion.name] of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            public key to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class GetImportJobRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.GetImportJob][google.cloud.kms.v1.KeyManagementService.GetImportJob].

    Attributes:
        name (str):
            Required. The [name][google.cloud.kms.v1.ImportJob.name] of
            the [ImportJob][google.cloud.kms.v1.ImportJob] to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateKeyRingRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.CreateKeyRing][google.cloud.kms.v1.KeyManagementService.CreateKeyRing].

    Attributes:
        parent (str):
            Required. The resource name of the location associated with
            the [KeyRings][google.cloud.kms.v1.KeyRing], in the format
            ``projects/*/locations/*``.
        key_ring_id (str):
            Required. It must be unique within a location and match the
            regular expression ``[a-zA-Z0-9_-]{1,63}``
        key_ring (google.cloud.kms_v1.types.KeyRing):
            Required. A [KeyRing][google.cloud.kms.v1.KeyRing] with
            initial field values.
    """

    parent = proto.Field(proto.STRING, number=1,)
    key_ring_id = proto.Field(proto.STRING, number=2,)
    key_ring = proto.Field(proto.MESSAGE, number=3, message=resources.KeyRing,)


class CreateCryptoKeyRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.CreateCryptoKey][google.cloud.kms.v1.KeyManagementService.CreateCryptoKey].

    Attributes:
        parent (str):
            Required. The [name][google.cloud.kms.v1.KeyRing.name] of
            the KeyRing associated with the
            [CryptoKeys][google.cloud.kms.v1.CryptoKey].
        crypto_key_id (str):
            Required. It must be unique within a KeyRing and match the
            regular expression ``[a-zA-Z0-9_-]{1,63}``
        crypto_key (google.cloud.kms_v1.types.CryptoKey):
            Required. A [CryptoKey][google.cloud.kms.v1.CryptoKey] with
            initial field values.
        skip_initial_version_creation (bool):
            If set to true, the request will create a
            [CryptoKey][google.cloud.kms.v1.CryptoKey] without any
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion].
            You must manually call
            [CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion]
            or
            [ImportCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion]
            before you can use this
            [CryptoKey][google.cloud.kms.v1.CryptoKey].
    """

    parent = proto.Field(proto.STRING, number=1,)
    crypto_key_id = proto.Field(proto.STRING, number=2,)
    crypto_key = proto.Field(proto.MESSAGE, number=3, message=resources.CryptoKey,)
    skip_initial_version_creation = proto.Field(proto.BOOL, number=5,)


class CreateCryptoKeyVersionRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.CreateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.CreateCryptoKeyVersion].

    Attributes:
        parent (str):
            Required. The [name][google.cloud.kms.v1.CryptoKey.name] of
            the [CryptoKey][google.cloud.kms.v1.CryptoKey] associated
            with the
            [CryptoKeyVersions][google.cloud.kms.v1.CryptoKeyVersion].
        crypto_key_version (google.cloud.kms_v1.types.CryptoKeyVersion):
            Required. A
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            with initial field values.
    """

    parent = proto.Field(proto.STRING, number=1,)
    crypto_key_version = proto.Field(
        proto.MESSAGE, number=2, message=resources.CryptoKeyVersion,
    )


class ImportCryptoKeyVersionRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.ImportCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.ImportCryptoKeyVersion].

    Attributes:
        parent (str):
            Required. The [name][google.cloud.kms.v1.CryptoKey.name] of
            the [CryptoKey][google.cloud.kms.v1.CryptoKey] to be
            imported into.
        algorithm (google.cloud.kms_v1.types.CryptoKeyVersion.CryptoKeyVersionAlgorithm):
            Required. The
            [algorithm][google.cloud.kms.v1.CryptoKeyVersion.CryptoKeyVersionAlgorithm]
            of the key being imported. This does not need to match the
            [version_template][google.cloud.kms.v1.CryptoKey.version_template]
            of the [CryptoKey][google.cloud.kms.v1.CryptoKey] this
            version imports into.
        import_job (str):
            Required. The [name][google.cloud.kms.v1.ImportJob.name] of
            the [ImportJob][google.cloud.kms.v1.ImportJob] that was used
            to wrap this key material.
        rsa_aes_wrapped_key (bytes):
            Wrapped key material produced with
            [RSA_OAEP_3072_SHA1_AES_256][google.cloud.kms.v1.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256]
            or
            [RSA_OAEP_4096_SHA1_AES_256][google.cloud.kms.v1.ImportJob.ImportMethod.RSA_OAEP_4096_SHA1_AES_256].

            This field contains the concatenation of two wrapped keys:

            .. raw:: html

                <ol>
                  <li>An ephemeral AES-256 wrapping key wrapped with the
                      [public_key][google.cloud.kms.v1.ImportJob.public_key] using RSAES-OAEP with SHA-1,
                      MGF1 with SHA-1, and an empty label.
                  </li>
                  <li>The key to be imported, wrapped with the ephemeral AES-256 key
                      using AES-KWP (RFC 5649).
                  </li>
                </ol>

            If importing symmetric key material, it is expected that the
            unwrapped key contains plain bytes. If importing asymmetric
            key material, it is expected that the unwrapped key is in
            PKCS#8-encoded DER format (the PrivateKeyInfo structure from
            RFC 5208).

            This format is the same as the format produced by PKCS#11
            mechanism CKM_RSA_AES_KEY_WRAP.
    """

    parent = proto.Field(proto.STRING, number=1,)
    algorithm = proto.Field(
        proto.ENUM, number=2, enum=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm,
    )
    import_job = proto.Field(proto.STRING, number=4,)
    rsa_aes_wrapped_key = proto.Field(
        proto.BYTES, number=5, oneof="wrapped_key_material",
    )


class CreateImportJobRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.CreateImportJob][google.cloud.kms.v1.KeyManagementService.CreateImportJob].

    Attributes:
        parent (str):
            Required. The [name][google.cloud.kms.v1.KeyRing.name] of
            the [KeyRing][google.cloud.kms.v1.KeyRing] associated with
            the [ImportJobs][google.cloud.kms.v1.ImportJob].
        import_job_id (str):
            Required. It must be unique within a KeyRing and match the
            regular expression ``[a-zA-Z0-9_-]{1,63}``
        import_job (google.cloud.kms_v1.types.ImportJob):
            Required. An [ImportJob][google.cloud.kms.v1.ImportJob] with
            initial field values.
    """

    parent = proto.Field(proto.STRING, number=1,)
    import_job_id = proto.Field(proto.STRING, number=2,)
    import_job = proto.Field(proto.MESSAGE, number=3, message=resources.ImportJob,)


class UpdateCryptoKeyRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.UpdateCryptoKey][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKey].

    Attributes:
        crypto_key (google.cloud.kms_v1.types.CryptoKey):
            Required. [CryptoKey][google.cloud.kms.v1.CryptoKey] with
            updated values.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. List of fields to be updated in
            this request.
    """

    crypto_key = proto.Field(proto.MESSAGE, number=1, message=resources.CryptoKey,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class UpdateCryptoKeyVersionRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.UpdateCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKeyVersion].

    Attributes:
        crypto_key_version (google.cloud.kms_v1.types.CryptoKeyVersion):
            Required.
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            with updated values.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. List of fields to be updated in
            this request.
    """

    crypto_key_version = proto.Field(
        proto.MESSAGE, number=1, message=resources.CryptoKeyVersion,
    )
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class EncryptRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKey][google.cloud.kms.v1.CryptoKey] or
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] to
            use for encryption.

            If a [CryptoKey][google.cloud.kms.v1.CryptoKey] is
            specified, the server will use its [primary
            version][google.cloud.kms.v1.CryptoKey.primary].
        plaintext (bytes):
            Required. The data to encrypt. Must be no larger than 64KiB.

            The maximum size depends on the key version's
            [protection_level][google.cloud.kms.v1.CryptoKeyVersionTemplate.protection_level].
            For [SOFTWARE][google.cloud.kms.v1.ProtectionLevel.SOFTWARE]
            keys, the plaintext must be no larger than 64KiB. For
            [HSM][google.cloud.kms.v1.ProtectionLevel.HSM] keys, the
            combined length of the plaintext and
            additional_authenticated_data fields must be no larger than
            8KiB.
        additional_authenticated_data (bytes):
            Optional. Optional data that, if specified, must also be
            provided during decryption through
            [DecryptRequest.additional_authenticated_data][google.cloud.kms.v1.DecryptRequest.additional_authenticated_data].

            The maximum size depends on the key version's
            [protection_level][google.cloud.kms.v1.CryptoKeyVersionTemplate.protection_level].
            For [SOFTWARE][google.cloud.kms.v1.ProtectionLevel.SOFTWARE]
            keys, the AAD must be no larger than 64KiB. For
            [HSM][google.cloud.kms.v1.ProtectionLevel.HSM] keys, the
            combined length of the plaintext and
            additional_authenticated_data fields must be no larger than
            8KiB.
        plaintext_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Optional. An optional CRC32C checksum of the
            [EncryptRequest.plaintext][google.cloud.kms.v1.EncryptRequest.plaintext].
            If specified,
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will verify the integrity of the received
            [EncryptRequest.plaintext][google.cloud.kms.v1.EncryptRequest.plaintext]
            using this checksum.
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will report an error if the checksum verification fails. If
            you receive a checksum error, your client should verify that
            CRC32C([EncryptRequest.plaintext][google.cloud.kms.v1.EncryptRequest.plaintext])
            is equal to
            [EncryptRequest.plaintext_crc32c][google.cloud.kms.v1.EncryptRequest.plaintext_crc32c],
            and if so, perform a limited number of retries. A persistent
            mismatch may indicate an issue in your computation of the
            CRC32C checksum. Note: This field is defined as int64 for
            reasons of compatibility across different languages.
            However, it is a non-negative integer, which will never
            exceed 2^32-1, and can be safely downconverted to uint32 in
            languages that support this type.

            NOTE: This field is in Beta.
        additional_authenticated_data_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Optional. An optional CRC32C checksum of the
            [EncryptRequest.additional_authenticated_data][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data].
            If specified,
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will verify the integrity of the received
            [EncryptRequest.additional_authenticated_data][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data]
            using this checksum.
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will report an error if the checksum verification fails. If
            you receive a checksum error, your client should verify that
            CRC32C([EncryptRequest.additional_authenticated_data][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data])
            is equal to
            [EncryptRequest.additional_authenticated_data_crc32c][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data_crc32c],
            and if so, perform a limited number of retries. A persistent
            mismatch may indicate an issue in your computation of the
            CRC32C checksum. Note: This field is defined as int64 for
            reasons of compatibility across different languages.
            However, it is a non-negative integer, which will never
            exceed 2^32-1, and can be safely downconverted to uint32 in
            languages that support this type.

            NOTE: This field is in Beta.
    """

    name = proto.Field(proto.STRING, number=1,)
    plaintext = proto.Field(proto.BYTES, number=2,)
    additional_authenticated_data = proto.Field(proto.BYTES, number=3,)
    plaintext_crc32c = proto.Field(
        proto.MESSAGE, number=7, message=wrappers_pb2.Int64Value,
    )
    additional_authenticated_data_crc32c = proto.Field(
        proto.MESSAGE, number=8, message=wrappers_pb2.Int64Value,
    )


class DecryptRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.Decrypt][google.cloud.kms.v1.KeyManagementService.Decrypt].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKey][google.cloud.kms.v1.CryptoKey] to use for
            decryption. The server will choose the appropriate version.
        ciphertext (bytes):
            Required. The encrypted data originally returned in
            [EncryptResponse.ciphertext][google.cloud.kms.v1.EncryptResponse.ciphertext].
        additional_authenticated_data (bytes):
            Optional. Optional data that must match the data originally
            supplied in
            [EncryptRequest.additional_authenticated_data][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data].
        ciphertext_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Optional. An optional CRC32C checksum of the
            [DecryptRequest.ciphertext][google.cloud.kms.v1.DecryptRequest.ciphertext].
            If specified,
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will verify the integrity of the received
            [DecryptRequest.ciphertext][google.cloud.kms.v1.DecryptRequest.ciphertext]
            using this checksum.
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will report an error if the checksum verification fails. If
            you receive a checksum error, your client should verify that
            CRC32C([DecryptRequest.ciphertext][google.cloud.kms.v1.DecryptRequest.ciphertext])
            is equal to
            [DecryptRequest.ciphertext_crc32c][google.cloud.kms.v1.DecryptRequest.ciphertext_crc32c],
            and if so, perform a limited number of retries. A persistent
            mismatch may indicate an issue in your computation of the
            CRC32C checksum. Note: This field is defined as int64 for
            reasons of compatibility across different languages.
            However, it is a non-negative integer, which will never
            exceed 2^32-1, and can be safely downconverted to uint32 in
            languages that support this type.

            NOTE: This field is in Beta.
        additional_authenticated_data_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Optional. An optional CRC32C checksum of the
            [DecryptRequest.additional_authenticated_data][google.cloud.kms.v1.DecryptRequest.additional_authenticated_data].
            If specified,
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will verify the integrity of the received
            [DecryptRequest.additional_authenticated_data][google.cloud.kms.v1.DecryptRequest.additional_authenticated_data]
            using this checksum.
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will report an error if the checksum verification fails. If
            you receive a checksum error, your client should verify that
            CRC32C([DecryptRequest.additional_authenticated_data][google.cloud.kms.v1.DecryptRequest.additional_authenticated_data])
            is equal to
            [DecryptRequest.additional_authenticated_data_crc32c][google.cloud.kms.v1.DecryptRequest.additional_authenticated_data_crc32c],
            and if so, perform a limited number of retries. A persistent
            mismatch may indicate an issue in your computation of the
            CRC32C checksum. Note: This field is defined as int64 for
            reasons of compatibility across different languages.
            However, it is a non-negative integer, which will never
            exceed 2^32-1, and can be safely downconverted to uint32 in
            languages that support this type.

            NOTE: This field is in Beta.
    """

    name = proto.Field(proto.STRING, number=1,)
    ciphertext = proto.Field(proto.BYTES, number=2,)
    additional_authenticated_data = proto.Field(proto.BYTES, number=3,)
    ciphertext_crc32c = proto.Field(
        proto.MESSAGE, number=5, message=wrappers_pb2.Int64Value,
    )
    additional_authenticated_data_crc32c = proto.Field(
        proto.MESSAGE, number=6, message=wrappers_pb2.Int64Value,
    )


class AsymmetricSignRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.AsymmetricSign][google.cloud.kms.v1.KeyManagementService.AsymmetricSign].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] to
            use for signing.
        digest (google.cloud.kms_v1.types.Digest):
            Required. The digest of the data to sign. The digest must be
            produced with the same digest algorithm as specified by the
            key version's
            [algorithm][google.cloud.kms.v1.CryptoKeyVersion.algorithm].
        digest_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Optional. An optional CRC32C checksum of the
            [AsymmetricSignRequest.digest][google.cloud.kms.v1.AsymmetricSignRequest.digest].
            If specified,
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will verify the integrity of the received
            [AsymmetricSignRequest.digest][google.cloud.kms.v1.AsymmetricSignRequest.digest]
            using this checksum.
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will report an error if the checksum verification fails. If
            you receive a checksum error, your client should verify that
            CRC32C([AsymmetricSignRequest.digest][google.cloud.kms.v1.AsymmetricSignRequest.digest])
            is equal to
            [AsymmetricSignRequest.digest_crc32c][google.cloud.kms.v1.AsymmetricSignRequest.digest_crc32c],
            and if so, perform a limited number of retries. A persistent
            mismatch may indicate an issue in your computation of the
            CRC32C checksum. Note: This field is defined as int64 for
            reasons of compatibility across different languages.
            However, it is a non-negative integer, which will never
            exceed 2^32-1, and can be safely downconverted to uint32 in
            languages that support this type.

            NOTE: This field is in Beta.
    """

    name = proto.Field(proto.STRING, number=1,)
    digest = proto.Field(proto.MESSAGE, number=3, message="Digest",)
    digest_crc32c = proto.Field(
        proto.MESSAGE, number=4, message=wrappers_pb2.Int64Value,
    )


class AsymmetricDecryptRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.AsymmetricDecrypt][google.cloud.kms.v1.KeyManagementService.AsymmetricDecrypt].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] to
            use for decryption.
        ciphertext (bytes):
            Required. The data encrypted with the named
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]'s
            public key using OAEP.
        ciphertext_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Optional. An optional CRC32C checksum of the
            [AsymmetricDecryptRequest.ciphertext][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext].
            If specified,
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will verify the integrity of the received
            [AsymmetricDecryptRequest.ciphertext][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext]
            using this checksum.
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            will report an error if the checksum verification fails. If
            you receive a checksum error, your client should verify that
            CRC32C([AsymmetricDecryptRequest.ciphertext][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext])
            is equal to
            [AsymmetricDecryptRequest.ciphertext_crc32c][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext_crc32c],
            and if so, perform a limited number of retries. A persistent
            mismatch may indicate an issue in your computation of the
            CRC32C checksum. Note: This field is defined as int64 for
            reasons of compatibility across different languages.
            However, it is a non-negative integer, which will never
            exceed 2^32-1, and can be safely downconverted to uint32 in
            languages that support this type.

            NOTE: This field is in Beta.
    """

    name = proto.Field(proto.STRING, number=1,)
    ciphertext = proto.Field(proto.BYTES, number=3,)
    ciphertext_crc32c = proto.Field(
        proto.MESSAGE, number=4, message=wrappers_pb2.Int64Value,
    )


class DecryptResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.Decrypt][google.cloud.kms.v1.KeyManagementService.Decrypt].

    Attributes:
        plaintext (bytes):
            The decrypted data originally supplied in
            [EncryptRequest.plaintext][google.cloud.kms.v1.EncryptRequest.plaintext].
        plaintext_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Integrity verification field. A CRC32C checksum of the
            returned
            [DecryptResponse.plaintext][google.cloud.kms.v1.DecryptResponse.plaintext].
            An integrity check of
            [DecryptResponse.plaintext][google.cloud.kms.v1.DecryptResponse.plaintext]
            can be performed by computing the CRC32C checksum of
            [DecryptResponse.plaintext][google.cloud.kms.v1.DecryptResponse.plaintext]
            and comparing your results to this field. Discard the
            response in case of non-matching checksum values, and
            perform a limited number of retries. A persistent mismatch
            may indicate an issue in your computation of the CRC32C
            checksum. Note: receiving this response message indicates
            that
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            is able to successfully decrypt the
            [ciphertext][google.cloud.kms.v1.DecryptRequest.ciphertext].
            Note: This field is defined as int64 for reasons of
            compatibility across different languages. However, it is a
            non-negative integer, which will never exceed 2^32-1, and
            can be safely downconverted to uint32 in languages that
            support this type.

            NOTE: This field is in Beta.
    """

    plaintext = proto.Field(proto.BYTES, number=1,)
    plaintext_crc32c = proto.Field(
        proto.MESSAGE, number=2, message=wrappers_pb2.Int64Value,
    )


class EncryptResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.Encrypt][google.cloud.kms.v1.KeyManagementService.Encrypt].

    Attributes:
        name (str):
            The resource name of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            used in encryption. Check this field to verify that the
            intended resource was used for encryption.
        ciphertext (bytes):
            The encrypted data.
        ciphertext_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Integrity verification field. A CRC32C checksum of the
            returned
            [EncryptResponse.ciphertext][google.cloud.kms.v1.EncryptResponse.ciphertext].
            An integrity check of
            [EncryptResponse.ciphertext][google.cloud.kms.v1.EncryptResponse.ciphertext]
            can be performed by computing the CRC32C checksum of
            [EncryptResponse.ciphertext][google.cloud.kms.v1.EncryptResponse.ciphertext]
            and comparing your results to this field. Discard the
            response in case of non-matching checksum values, and
            perform a limited number of retries. A persistent mismatch
            may indicate an issue in your computation of the CRC32C
            checksum. Note: This field is defined as int64 for reasons
            of compatibility across different languages. However, it is
            a non-negative integer, which will never exceed 2^32-1, and
            can be safely downconverted to uint32 in languages that
            support this type.

            NOTE: This field is in Beta.
        verified_plaintext_crc32c (bool):
            Integrity verification field. A flag indicating whether
            [EncryptRequest.plaintext_crc32c][google.cloud.kms.v1.EncryptRequest.plaintext_crc32c]
            was received by
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            and used for the integrity verification of the
            [plaintext][google.cloud.kms.v1.EncryptRequest.plaintext]. A
            false value of this field indicates either that
            [EncryptRequest.plaintext_crc32c][google.cloud.kms.v1.EncryptRequest.plaintext_crc32c]
            was left unset or that it was not delivered to
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService].
            If you've set
            [EncryptRequest.plaintext_crc32c][google.cloud.kms.v1.EncryptRequest.plaintext_crc32c]
            but this field is still false, discard the response and
            perform a limited number of retries.

            NOTE: This field is in Beta.
        verified_additional_authenticated_data_crc32c (bool):
            Integrity verification field. A flag indicating whether
            [EncryptRequest.additional_authenticated_data_crc32c][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data_crc32c]
            was received by
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            and used for the integrity verification of the
            [AAD][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data].
            A false value of this field indicates either that
            [EncryptRequest.additional_authenticated_data_crc32c][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data_crc32c]
            was left unset or that it was not delivered to
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService].
            If you've set
            [EncryptRequest.additional_authenticated_data_crc32c][google.cloud.kms.v1.EncryptRequest.additional_authenticated_data_crc32c]
            but this field is still false, discard the response and
            perform a limited number of retries.

            NOTE: This field is in Beta.
    """

    name = proto.Field(proto.STRING, number=1,)
    ciphertext = proto.Field(proto.BYTES, number=2,)
    ciphertext_crc32c = proto.Field(
        proto.MESSAGE, number=4, message=wrappers_pb2.Int64Value,
    )
    verified_plaintext_crc32c = proto.Field(proto.BOOL, number=5,)
    verified_additional_authenticated_data_crc32c = proto.Field(proto.BOOL, number=6,)


class AsymmetricSignResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.AsymmetricSign][google.cloud.kms.v1.KeyManagementService.AsymmetricSign].

    Attributes:
        signature (bytes):
            The created signature.
        signature_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Integrity verification field. A CRC32C checksum of the
            returned
            [AsymmetricSignResponse.signature][google.cloud.kms.v1.AsymmetricSignResponse.signature].
            An integrity check of
            [AsymmetricSignResponse.signature][google.cloud.kms.v1.AsymmetricSignResponse.signature]
            can be performed by computing the CRC32C checksum of
            [AsymmetricSignResponse.signature][google.cloud.kms.v1.AsymmetricSignResponse.signature]
            and comparing your results to this field. Discard the
            response in case of non-matching checksum values, and
            perform a limited number of retries. A persistent mismatch
            may indicate an issue in your computation of the CRC32C
            checksum. Note: This field is defined as int64 for reasons
            of compatibility across different languages. However, it is
            a non-negative integer, which will never exceed 2^32-1, and
            can be safely downconverted to uint32 in languages that
            support this type.

            NOTE: This field is in Beta.
        verified_digest_crc32c (bool):
            Integrity verification field. A flag indicating whether
            [AsymmetricSignRequest.digest_crc32c][google.cloud.kms.v1.AsymmetricSignRequest.digest_crc32c]
            was received by
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            and used for the integrity verification of the
            [digest][google.cloud.kms.v1.AsymmetricSignRequest.digest].
            A false value of this field indicates either that
            [AsymmetricSignRequest.digest_crc32c][google.cloud.kms.v1.AsymmetricSignRequest.digest_crc32c]
            was left unset or that it was not delivered to
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService].
            If you've set
            [AsymmetricSignRequest.digest_crc32c][google.cloud.kms.v1.AsymmetricSignRequest.digest_crc32c]
            but this field is still false, discard the response and
            perform a limited number of retries.

            NOTE: This field is in Beta.
        name (str):
            The resource name of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion]
            used for signing. Check this field to verify that the
            intended resource was used for signing.

            NOTE: This field is in Beta.
    """

    signature = proto.Field(proto.BYTES, number=1,)
    signature_crc32c = proto.Field(
        proto.MESSAGE, number=2, message=wrappers_pb2.Int64Value,
    )
    verified_digest_crc32c = proto.Field(proto.BOOL, number=3,)
    name = proto.Field(proto.STRING, number=4,)


class AsymmetricDecryptResponse(proto.Message):
    r"""Response message for
    [KeyManagementService.AsymmetricDecrypt][google.cloud.kms.v1.KeyManagementService.AsymmetricDecrypt].

    Attributes:
        plaintext (bytes):
            The decrypted data originally encrypted with
            the matching public key.
        plaintext_crc32c (google.protobuf.wrappers_pb2.Int64Value):
            Integrity verification field. A CRC32C checksum of the
            returned
            [AsymmetricDecryptResponse.plaintext][google.cloud.kms.v1.AsymmetricDecryptResponse.plaintext].
            An integrity check of
            [AsymmetricDecryptResponse.plaintext][google.cloud.kms.v1.AsymmetricDecryptResponse.plaintext]
            can be performed by computing the CRC32C checksum of
            [AsymmetricDecryptResponse.plaintext][google.cloud.kms.v1.AsymmetricDecryptResponse.plaintext]
            and comparing your results to this field. Discard the
            response in case of non-matching checksum values, and
            perform a limited number of retries. A persistent mismatch
            may indicate an issue in your computation of the CRC32C
            checksum. Note: This field is defined as int64 for reasons
            of compatibility across different languages. However, it is
            a non-negative integer, which will never exceed 2^32-1, and
            can be safely downconverted to uint32 in languages that
            support this type.

            NOTE: This field is in Beta.
        verified_ciphertext_crc32c (bool):
            Integrity verification field. A flag indicating whether
            [AsymmetricDecryptRequest.ciphertext_crc32c][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext_crc32c]
            was received by
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService]
            and used for the integrity verification of the
            [ciphertext][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext].
            A false value of this field indicates either that
            [AsymmetricDecryptRequest.ciphertext_crc32c][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext_crc32c]
            was left unset or that it was not delivered to
            [KeyManagementService][google.cloud.kms.v1.KeyManagementService].
            If you've set
            [AsymmetricDecryptRequest.ciphertext_crc32c][google.cloud.kms.v1.AsymmetricDecryptRequest.ciphertext_crc32c]
            but this field is still false, discard the response and
            perform a limited number of retries.

            NOTE: This field is in Beta.
    """

    plaintext = proto.Field(proto.BYTES, number=1,)
    plaintext_crc32c = proto.Field(
        proto.MESSAGE, number=2, message=wrappers_pb2.Int64Value,
    )
    verified_ciphertext_crc32c = proto.Field(proto.BOOL, number=3,)


class UpdateCryptoKeyPrimaryVersionRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.UpdateCryptoKeyPrimaryVersion][google.cloud.kms.v1.KeyManagementService.UpdateCryptoKeyPrimaryVersion].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKey][google.cloud.kms.v1.CryptoKey] to update.
        crypto_key_version_id (str):
            Required. The id of the child
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] to
            use as primary.
    """

    name = proto.Field(proto.STRING, number=1,)
    crypto_key_version_id = proto.Field(proto.STRING, number=2,)


class DestroyCryptoKeyVersionRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.DestroyCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.DestroyCryptoKeyVersion].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] to
            destroy.
    """

    name = proto.Field(proto.STRING, number=1,)


class RestoreCryptoKeyVersionRequest(proto.Message):
    r"""Request message for
    [KeyManagementService.RestoreCryptoKeyVersion][google.cloud.kms.v1.KeyManagementService.RestoreCryptoKeyVersion].

    Attributes:
        name (str):
            Required. The resource name of the
            [CryptoKeyVersion][google.cloud.kms.v1.CryptoKeyVersion] to
            restore.
    """

    name = proto.Field(proto.STRING, number=1,)


class Digest(proto.Message):
    r"""A [Digest][google.cloud.kms.v1.Digest] holds a cryptographic message
    digest.

    Attributes:
        sha256 (bytes):
            A message digest produced with the SHA-256
            algorithm.
        sha384 (bytes):
            A message digest produced with the SHA-384
            algorithm.
        sha512 (bytes):
            A message digest produced with the SHA-512
            algorithm.
    """

    sha256 = proto.Field(proto.BYTES, number=1, oneof="digest",)
    sha384 = proto.Field(proto.BYTES, number=2, oneof="digest",)
    sha512 = proto.Field(proto.BYTES, number=3, oneof="digest",)


class LocationMetadata(proto.Message):
    r"""Cloud KMS metadata for the given
    [google.cloud.location.Location][google.cloud.location.Location].

    Attributes:
        hsm_available (bool):
            Indicates whether
            [CryptoKeys][google.cloud.kms.v1.CryptoKey] with
            [protection_level][google.cloud.kms.v1.CryptoKeyVersionTemplate.protection_level]
            [HSM][google.cloud.kms.v1.ProtectionLevel.HSM] can be
            created in this location.
        ekm_available (bool):
            Indicates whether
            [CryptoKeys][google.cloud.kms.v1.CryptoKey] with
            [protection_level][google.cloud.kms.v1.CryptoKeyVersionTemplate.protection_level]
            [EXTERNAL][google.cloud.kms.v1.ProtectionLevel.EXTERNAL] can
            be created in this location.
    """

    hsm_available = proto.Field(proto.BOOL, number=1,)
    ekm_available = proto.Field(proto.BOOL, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
