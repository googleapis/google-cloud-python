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

import abc
import typing
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.kms_v1.types import resources
from google.cloud.kms_v1.types import service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-kms",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class KeyManagementServiceTransport(abc.ABC):
    """Abstract transport class for KeyManagementService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloudkms",
    )

    def __init__(
        self,
        *,
        host: str = "cloudkms.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.list_key_rings: gapic_v1.method.wrap_method(
                self.list_key_rings,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_crypto_keys: gapic_v1.method.wrap_method(
                self.list_crypto_keys,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_crypto_key_versions: gapic_v1.method.wrap_method(
                self.list_crypto_key_versions,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_import_jobs: gapic_v1.method.wrap_method(
                self.list_import_jobs,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_key_ring: gapic_v1.method.wrap_method(
                self.get_key_ring,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_crypto_key: gapic_v1.method.wrap_method(
                self.get_crypto_key,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_crypto_key_version: gapic_v1.method.wrap_method(
                self.get_crypto_key_version,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_public_key: gapic_v1.method.wrap_method(
                self.get_public_key,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_import_job: gapic_v1.method.wrap_method(
                self.get_import_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_key_ring: gapic_v1.method.wrap_method(
                self.create_key_ring,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_crypto_key: gapic_v1.method.wrap_method(
                self.create_crypto_key,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_crypto_key_version: gapic_v1.method.wrap_method(
                self.create_crypto_key_version,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.import_crypto_key_version: gapic_v1.method.wrap_method(
                self.import_crypto_key_version,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_import_job: gapic_v1.method.wrap_method(
                self.create_import_job,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_crypto_key: gapic_v1.method.wrap_method(
                self.update_crypto_key,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_crypto_key_version: gapic_v1.method.wrap_method(
                self.update_crypto_key_version,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.encrypt: gapic_v1.method.wrap_method(
                self.encrypt,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.decrypt: gapic_v1.method.wrap_method(
                self.decrypt,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.asymmetric_sign: gapic_v1.method.wrap_method(
                self.asymmetric_sign,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.asymmetric_decrypt: gapic_v1.method.wrap_method(
                self.asymmetric_decrypt,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_crypto_key_primary_version: gapic_v1.method.wrap_method(
                self.update_crypto_key_primary_version,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.destroy_crypto_key_version: gapic_v1.method.wrap_method(
                self.destroy_crypto_key_version,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.restore_crypto_key_version: gapic_v1.method.wrap_method(
                self.restore_crypto_key_version,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded,
                        exceptions.InternalServerError,
                        exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    @property
    def list_key_rings(
        self,
    ) -> typing.Callable[
        [service.ListKeyRingsRequest],
        typing.Union[
            service.ListKeyRingsResponse, typing.Awaitable[service.ListKeyRingsResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_crypto_keys(
        self,
    ) -> typing.Callable[
        [service.ListCryptoKeysRequest],
        typing.Union[
            service.ListCryptoKeysResponse,
            typing.Awaitable[service.ListCryptoKeysResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_crypto_key_versions(
        self,
    ) -> typing.Callable[
        [service.ListCryptoKeyVersionsRequest],
        typing.Union[
            service.ListCryptoKeyVersionsResponse,
            typing.Awaitable[service.ListCryptoKeyVersionsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_import_jobs(
        self,
    ) -> typing.Callable[
        [service.ListImportJobsRequest],
        typing.Union[
            service.ListImportJobsResponse,
            typing.Awaitable[service.ListImportJobsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_key_ring(
        self,
    ) -> typing.Callable[
        [service.GetKeyRingRequest],
        typing.Union[resources.KeyRing, typing.Awaitable[resources.KeyRing]],
    ]:
        raise NotImplementedError()

    @property
    def get_crypto_key(
        self,
    ) -> typing.Callable[
        [service.GetCryptoKeyRequest],
        typing.Union[resources.CryptoKey, typing.Awaitable[resources.CryptoKey]],
    ]:
        raise NotImplementedError()

    @property
    def get_crypto_key_version(
        self,
    ) -> typing.Callable[
        [service.GetCryptoKeyVersionRequest],
        typing.Union[
            resources.CryptoKeyVersion, typing.Awaitable[resources.CryptoKeyVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_public_key(
        self,
    ) -> typing.Callable[
        [service.GetPublicKeyRequest],
        typing.Union[resources.PublicKey, typing.Awaitable[resources.PublicKey]],
    ]:
        raise NotImplementedError()

    @property
    def get_import_job(
        self,
    ) -> typing.Callable[
        [service.GetImportJobRequest],
        typing.Union[resources.ImportJob, typing.Awaitable[resources.ImportJob]],
    ]:
        raise NotImplementedError()

    @property
    def create_key_ring(
        self,
    ) -> typing.Callable[
        [service.CreateKeyRingRequest],
        typing.Union[resources.KeyRing, typing.Awaitable[resources.KeyRing]],
    ]:
        raise NotImplementedError()

    @property
    def create_crypto_key(
        self,
    ) -> typing.Callable[
        [service.CreateCryptoKeyRequest],
        typing.Union[resources.CryptoKey, typing.Awaitable[resources.CryptoKey]],
    ]:
        raise NotImplementedError()

    @property
    def create_crypto_key_version(
        self,
    ) -> typing.Callable[
        [service.CreateCryptoKeyVersionRequest],
        typing.Union[
            resources.CryptoKeyVersion, typing.Awaitable[resources.CryptoKeyVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def import_crypto_key_version(
        self,
    ) -> typing.Callable[
        [service.ImportCryptoKeyVersionRequest],
        typing.Union[
            resources.CryptoKeyVersion, typing.Awaitable[resources.CryptoKeyVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_import_job(
        self,
    ) -> typing.Callable[
        [service.CreateImportJobRequest],
        typing.Union[resources.ImportJob, typing.Awaitable[resources.ImportJob]],
    ]:
        raise NotImplementedError()

    @property
    def update_crypto_key(
        self,
    ) -> typing.Callable[
        [service.UpdateCryptoKeyRequest],
        typing.Union[resources.CryptoKey, typing.Awaitable[resources.CryptoKey]],
    ]:
        raise NotImplementedError()

    @property
    def update_crypto_key_version(
        self,
    ) -> typing.Callable[
        [service.UpdateCryptoKeyVersionRequest],
        typing.Union[
            resources.CryptoKeyVersion, typing.Awaitable[resources.CryptoKeyVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def encrypt(
        self,
    ) -> typing.Callable[
        [service.EncryptRequest],
        typing.Union[
            service.EncryptResponse, typing.Awaitable[service.EncryptResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def decrypt(
        self,
    ) -> typing.Callable[
        [service.DecryptRequest],
        typing.Union[
            service.DecryptResponse, typing.Awaitable[service.DecryptResponse]
        ],
    ]:
        raise NotImplementedError()

    @property
    def asymmetric_sign(
        self,
    ) -> typing.Callable[
        [service.AsymmetricSignRequest],
        typing.Union[
            service.AsymmetricSignResponse,
            typing.Awaitable[service.AsymmetricSignResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def asymmetric_decrypt(
        self,
    ) -> typing.Callable[
        [service.AsymmetricDecryptRequest],
        typing.Union[
            service.AsymmetricDecryptResponse,
            typing.Awaitable[service.AsymmetricDecryptResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_crypto_key_primary_version(
        self,
    ) -> typing.Callable[
        [service.UpdateCryptoKeyPrimaryVersionRequest],
        typing.Union[resources.CryptoKey, typing.Awaitable[resources.CryptoKey]],
    ]:
        raise NotImplementedError()

    @property
    def destroy_crypto_key_version(
        self,
    ) -> typing.Callable[
        [service.DestroyCryptoKeyVersionRequest],
        typing.Union[
            resources.CryptoKeyVersion, typing.Awaitable[resources.CryptoKeyVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def restore_crypto_key_version(
        self,
    ) -> typing.Callable[
        [service.RestoreCryptoKeyVersionRequest],
        typing.Union[
            resources.CryptoKeyVersion, typing.Awaitable[resources.CryptoKeyVersion]
        ],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.SetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self,
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self,
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest],
        typing.Union[
            iam_policy.TestIamPermissionsResponse,
            typing.Awaitable[iam_policy.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("KeyManagementServiceTransport",)
