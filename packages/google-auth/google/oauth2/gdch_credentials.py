# Copyright 2022 Google LLC
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

"""Experimental GDCH credentials support.
"""

import six
from six.moves import http_client

from google.auth import _helpers
from google.auth import credentials
from google.auth import exceptions
from google.oauth2 import _client


TOKEN_EXCHANGE_TYPE = "urn:ietf:params:oauth:token-type:token-exchange"
ACCESS_TOKEN_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:access_token"
JWT_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:jwt"
SERVICE_ACCOUNT_TOKEN_TYPE = "urn:k8s:params:oauth:token-type:serviceaccount"


class ServiceAccountCredentials(credentials.Credentials):
    """Credentials for GDCH (`Google Distributed Cloud Hosted`_) for service
    account users.

    .. _Google Distributed Cloud Hosted:
        https://cloud.google.com/blog/topics/hybrid-cloud/\
            announcing-google-distributed-cloud-edge-and-hosted

    Besides the constructor, a GDCH credential can be created via application
    default credentials.

    To do so, user first creates a JSON file of the
    following format::

        {
            "type":"gdch_service_account",
            "format_version":"v1",
            "k8s_ca_cert_path":"<k8s ca cert pem file path>",
            "k8s_cert_path":"<k8s cert pem file path>",
            "k8s_key_path":"<k8s key pem file path>",
            "k8s_token_endpoint":"<k8s token endpoint>",
            "ais_ca_cert_path":"<AIS ca cert pem file path>",
            "ais_token_endpoint":"<AIS token endpoint>"
        }

    Here "k8s_*" files are used to request a k8s token from k8s token endpoint
    using mutual TLS connection. The k8s token is then sent to AIS token endpoint
    to exchange for an AIS token. The AIS token will be used to talk to Google
    API services.

    "k8s_ca_cert_path" field is not needed if the k8s server uses well known CA.
    "ais_ca_cert_path" field is not needed if the AIS server uses well known CA.
    These two fields can be used for testing environments.

    The "format_version" field stands for the format of the JSON file. For now
    it is always "v1".

    After the JSON file is created, set `GOOGLE_APPLICATION_CREDENTIALS` environment
    variable to the JSON file path, then use the following code to create the
    credential::

        import google.auth

        credential, _ = google.auth.default()
        credential = credential.with_audience("<the audience>")

    The audience denotes the scope the AIS token is requested, for example, it
    could be either a k8s cluster or API service.
    """

    def __init__(
        self,
        k8s_ca_cert_path,
        k8s_cert_path,
        k8s_key_path,
        k8s_token_endpoint,
        ais_ca_cert_path,
        ais_token_endpoint,
        audience,
    ):
        """
        Args:
            k8s_ca_cert_path (str): CA cert path for k8s calls. This field is
                useful if the specific k8s server doesn't use well known CA,
                for instance, a testing k8s server. If the CA is well known,
                you can pass `None` for this parameter.
            k8s_cert_path (str): Certificate path for k8s calls
            k8s_key_path (str): Key path for k8s calls
            k8s_token_endpoint (str): k8s token endpoint url
            ais_ca_cert_path (str): CA cert path for AIS token endpoint calls.
                This field is useful if the specific AIS token server doesn't
                uses well known CA, for instance, a testing AIS server. If the
                CA is well known, you can pass `None` for this parameter.
            ais_token_endpoint (str): AIS token endpoint url
            audience (str): The audience for the requested AIS token. For
                example, it could be a k8s cluster or API service.
        """
        super(ServiceAccountCredentials, self).__init__()
        self._k8s_ca_cert_path = k8s_ca_cert_path
        self._k8s_cert_path = k8s_cert_path
        self._k8s_key_path = k8s_key_path
        self._k8s_token_endpoint = k8s_token_endpoint
        self._ais_ca_cert_path = ais_ca_cert_path
        self._ais_token_endpoint = ais_token_endpoint
        self._audience = audience

    def _make_k8s_token_request(self, request):
        k8s_request_body = {
            "kind": "TokenRequest",
            "apiVersion": "authentication.k8s.io/v1",
            "spec": {"audiences": [self._ais_token_endpoint]},
        }
        # mTLS connection to k8s token endpoint to get a k8s token.
        k8s_response_data = _client._token_endpoint_request(
            request,
            self._k8s_token_endpoint,
            k8s_request_body,
            access_token=None,
            use_json=True,
            expected_status_code=http_client.CREATED,
            cert=(self._k8s_cert_path, self._k8s_key_path),
            verify=self._k8s_ca_cert_path,
        )

        try:
            k8s_token = k8s_response_data["status"]["token"]
            return k8s_token
        except KeyError as caught_exc:
            new_exc = exceptions.RefreshError(
                "No access token in k8s token response.", k8s_response_data
            )
            six.raise_from(new_exc, caught_exc)

    def _make_ais_token_request(self, k8s_token, request):
        # send a request to AIS token point with the k8s token
        ais_request_body = {
            "grant_type": TOKEN_EXCHANGE_TYPE,
            "audience": self._audience,
            "requested_token_type": ACCESS_TOKEN_TOKEN_TYPE,
            "subject_token": k8s_token,
            "subject_token_type": SERVICE_ACCOUNT_TOKEN_TYPE,
        }
        ais_response_data = _client._token_endpoint_request(
            request,
            self._ais_token_endpoint,
            ais_request_body,
            access_token=None,
            use_json=True,
            verify=self._ais_ca_cert_path,
        )
        ais_token, _, ais_expiry, _ = _client._handle_refresh_grant_response(
            ais_response_data, None
        )
        return ais_token, ais_expiry

    @_helpers.copy_docstring(credentials.Credentials)
    def refresh(self, request):
        import google.auth.transport.requests

        if not isinstance(request, google.auth.transport.requests.Request):
            raise exceptions.RefreshError(
                "For GDCH service account credentials, request must be a google.auth.transport.requests.Request object"
            )

        k8s_token = self._make_k8s_token_request(request)
        self.token, self.expiry = self._make_ais_token_request(k8s_token, request)

    def with_audience(self, audience):
        """Create a copy of GDCH credentials with the specified audience.

        Args:
            audience (str): The intended audience for GDCH credentials.
        """
        return self.__class__(
            self._k8s_ca_cert_path,
            self._k8s_cert_path,
            self._k8s_key_path,
            self._k8s_token_endpoint,
            self._ais_ca_cert_path,
            self._ais_token_endpoint,
            audience,
        )
