# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""External Account Credentials.

This module provides credentials that exchange workload identity pool external
credentials for Google access tokens. This facilitates accessing Google Cloud
Platform resources from on-prem and non-Google Cloud platforms (e.g. AWS,
Microsoft Azure, OIDC identity providers), using native credentials retrieved
from the current environment without the need to copy, save and manage
long-lived service account credentials.

Specifically, this is intended to use access tokens acquired using the GCP STS
token exchange endpoint following the `OAuth 2.0 Token Exchange`_ spec.

.. _OAuth 2.0 Token Exchange: https://tools.ietf.org/html/rfc8693
"""

import abc
import datetime
import json

import six

from google.auth import _helpers
from google.auth import credentials
from google.auth import exceptions
from google.auth import impersonated_credentials
from google.oauth2 import sts
from google.oauth2 import utils

# The token exchange grant_type used for exchanging credentials.
_STS_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"
# The token exchange requested_token_type. This is always an access_token.
_STS_REQUESTED_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:access_token"
# Cloud resource manager URL used to retrieve project information.
_CLOUD_RESOURCE_MANAGER = "https://cloudresourcemanager.googleapis.com/v1/projects/"


@six.add_metaclass(abc.ABCMeta)
class Credentials(credentials.Scoped, credentials.CredentialsWithQuotaProject):
    """Base class for all external account credentials.

    This is used to instantiate Credentials for exchanging external account
    credentials for Google access token and authorizing requests to Google APIs.
    The base class implements the common logic for exchanging external account
    credentials for Google access tokens.
    """

    def __init__(
        self,
        audience,
        subject_token_type,
        token_url,
        credential_source,
        service_account_impersonation_url=None,
        client_id=None,
        client_secret=None,
        quota_project_id=None,
        scopes=None,
        default_scopes=None,
    ):
        """Instantiates an external account credentials object.

        Args:
            audience (str): The STS audience field.
            subject_token_type (str): The subject token type.
            token_url (str): The STS endpoint URL.
            credential_source (Mapping): The credential source dictionary.
            service_account_impersonation_url (Optional[str]): The optional service account
                impersonation generateAccessToken URL.
            client_id (Optional[str]): The optional client ID.
            client_secret (Optional[str]): The optional client secret.
            quota_project_id (Optional[str]): The optional quota project ID.
            scopes (Optional[Sequence[str]]): Optional scopes to request during the
                authorization grant.
            default_scopes (Optional[Sequence[str]]): Default scopes passed by a
                Google client library. Use 'scopes' for user-defined scopes.
        Raises:
            google.auth.exceptions.RefreshError: If the generateAccessToken
                endpoint returned an error.
        """
        super(Credentials, self).__init__()
        self._audience = audience
        self._subject_token_type = subject_token_type
        self._token_url = token_url
        self._credential_source = credential_source
        self._service_account_impersonation_url = service_account_impersonation_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._quota_project_id = quota_project_id
        self._scopes = scopes
        self._default_scopes = default_scopes

        if self._client_id:
            self._client_auth = utils.ClientAuthentication(
                utils.ClientAuthType.basic, self._client_id, self._client_secret
            )
        else:
            self._client_auth = None
        self._sts_client = sts.Client(self._token_url, self._client_auth)

        if self._service_account_impersonation_url:
            self._impersonated_credentials = self._initialize_impersonated_credentials()
        else:
            self._impersonated_credentials = None
        self._project_id = None

    @property
    def requires_scopes(self):
        """Checks if the credentials requires scopes.

        Returns:
            bool: True if there are no scopes set otherwise False.
        """
        return not self._scopes and not self._default_scopes

    @property
    def project_number(self):
        """Optional[str]: The project number corresponding to the workload identity pool."""

        # STS audience pattern:
        # //iam.googleapis.com/projects/$PROJECT_NUMBER/locations/...
        components = self._audience.split("/")
        try:
            project_index = components.index("projects")
            if project_index + 1 < len(components):
                return components[project_index + 1] or None
        except ValueError:
            return None

    @_helpers.copy_docstring(credentials.Scoped)
    def with_scopes(self, scopes, default_scopes=None):
        return self.__class__(
            audience=self._audience,
            subject_token_type=self._subject_token_type,
            token_url=self._token_url,
            credential_source=self._credential_source,
            service_account_impersonation_url=self._service_account_impersonation_url,
            client_id=self._client_id,
            client_secret=self._client_secret,
            quota_project_id=self._quota_project_id,
            scopes=scopes,
            default_scopes=default_scopes,
        )

    @abc.abstractmethod
    def retrieve_subject_token(self, request):
        """Retrieves the subject token using the credential_source object.

        Args:
            request (google.auth.transport.Request): A callable used to make
                HTTP requests.
        Returns:
            str: The retrieved subject token.
        """
        # pylint: disable=missing-raises-doc
        # (pylint doesn't recognize that this is abstract)
        raise NotImplementedError("retrieve_subject_token must be implemented")

    def get_project_id(self, request):
        """Retrieves the project ID corresponding to the workload identity pool.

        When not determinable, None is returned.

        This is introduced to support the current pattern of using the Auth library:

            credentials, project_id = google.auth.default()

        The resource may not have permission (resourcemanager.projects.get) to
        call this API or the required scopes may not be selected:
        https://cloud.google.com/resource-manager/reference/rest/v1/projects/get#authorization-scopes

        Args:
            request (google.auth.transport.Request): A callable used to make
                HTTP requests.
        Returns:
            Optional[str]: The project ID corresponding to the workload identity pool
                if determinable.
        """
        if self._project_id:
            # If already retrieved, return the cached project ID value.
            return self._project_id
        scopes = self._scopes if self._scopes is not None else self._default_scopes
        # Scopes are required in order to retrieve a valid access token.
        if self.project_number and scopes:
            headers = {}
            url = _CLOUD_RESOURCE_MANAGER + self.project_number
            self.before_request(request, "GET", url, headers)
            response = request(url=url, method="GET", headers=headers)

            response_body = (
                response.data.decode("utf-8")
                if hasattr(response.data, "decode")
                else response.data
            )
            response_data = json.loads(response_body)

            if response.status == 200:
                # Cache result as this field is immutable.
                self._project_id = response_data.get("projectId")
                return self._project_id

        return None

    @_helpers.copy_docstring(credentials.Credentials)
    def refresh(self, request):
        scopes = self._scopes if self._scopes is not None else self._default_scopes
        if self._impersonated_credentials:
            self._impersonated_credentials.refresh(request)
            self.token = self._impersonated_credentials.token
            self.expiry = self._impersonated_credentials.expiry
        else:
            now = _helpers.utcnow()
            response_data = self._sts_client.exchange_token(
                request=request,
                grant_type=_STS_GRANT_TYPE,
                subject_token=self.retrieve_subject_token(request),
                subject_token_type=self._subject_token_type,
                audience=self._audience,
                scopes=scopes,
                requested_token_type=_STS_REQUESTED_TOKEN_TYPE,
            )
            self.token = response_data.get("access_token")
            lifetime = datetime.timedelta(seconds=response_data.get("expires_in"))
            self.expiry = now + lifetime

    @_helpers.copy_docstring(credentials.CredentialsWithQuotaProject)
    def with_quota_project(self, quota_project_id):
        # Return copy of instance with the provided quota project ID.
        return self.__class__(
            audience=self._audience,
            subject_token_type=self._subject_token_type,
            token_url=self._token_url,
            credential_source=self._credential_source,
            service_account_impersonation_url=self._service_account_impersonation_url,
            client_id=self._client_id,
            client_secret=self._client_secret,
            quota_project_id=quota_project_id,
            scopes=self._scopes,
            default_scopes=self._default_scopes,
        )

    def _initialize_impersonated_credentials(self):
        """Generates an impersonated credentials.

        For more details, see `projects.serviceAccounts.generateAccessToken`_.

        .. _projects.serviceAccounts.generateAccessToken: https://cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/generateAccessToken

        Returns:
            impersonated_credentials.Credential: The impersonated credentials
                object.

        Raises:
            google.auth.exceptions.RefreshError: If the generateAccessToken
                endpoint returned an error.
        """
        # Return copy of instance with no service account impersonation.
        source_credentials = self.__class__(
            audience=self._audience,
            subject_token_type=self._subject_token_type,
            token_url=self._token_url,
            credential_source=self._credential_source,
            service_account_impersonation_url=None,
            client_id=self._client_id,
            client_secret=self._client_secret,
            quota_project_id=self._quota_project_id,
            scopes=self._scopes,
            default_scopes=self._default_scopes,
        )

        # Determine target_principal.
        start_index = self._service_account_impersonation_url.rfind("/")
        end_index = self._service_account_impersonation_url.find(":generateAccessToken")
        if start_index != -1 and end_index != -1 and start_index < end_index:
            start_index = start_index + 1
            target_principal = self._service_account_impersonation_url[
                start_index:end_index
            ]
        else:
            raise exceptions.RefreshError(
                "Unable to determine target principal from service account impersonation URL."
            )

        scopes = self._scopes if self._scopes is not None else self._default_scopes
        # Initialize and return impersonated credentials.
        return impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=target_principal,
            target_scopes=scopes,
            quota_project_id=self._quota_project_id,
            iam_endpoint_override=self._service_account_impersonation_url,
        )
