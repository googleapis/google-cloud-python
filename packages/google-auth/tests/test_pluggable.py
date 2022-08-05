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

# import datetime
import json
import os
import subprocess

import mock
import pytest  # type: ignore

# from six.moves import http_client
# from six.moves import urllib

# from google.auth import _helpers
from google.auth import exceptions
from google.auth import pluggable

# from google.auth import transport


CLIENT_ID = "username"
CLIENT_SECRET = "password"
# Base64 encoding of "username:password".
BASIC_AUTH_ENCODING = "dXNlcm5hbWU6cGFzc3dvcmQ="
SERVICE_ACCOUNT_EMAIL = "service-1234@service-name.iam.gserviceaccount.com"
SERVICE_ACCOUNT_IMPERSONATION_URL = (
    "https://us-east1-iamcredentials.googleapis.com/v1/projects/-"
    + "/serviceAccounts/{}:generateAccessToken".format(SERVICE_ACCOUNT_EMAIL)
)
QUOTA_PROJECT_ID = "QUOTA_PROJECT_ID"
SCOPES = ["scope1", "scope2"]
SUBJECT_TOKEN_FIELD_NAME = "access_token"

TOKEN_URL = "https://sts.googleapis.com/v1/token"
SERVICE_ACCOUNT_IMPERSONATION_URL = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/byoid-test@cicpclientproj.iam.gserviceaccount.com:generateAccessToken"
SUBJECT_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:jwt"
AUDIENCE = "//iam.googleapis.com/projects/123456/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID"


class TestCredentials(object):
    CREDENTIAL_SOURCE_EXECUTABLE_COMMAND = (
        "/fake/external/excutable --arg1=value1 --arg2=value2"
    )
    CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE = "fake_output_file"
    CREDENTIAL_SOURCE_EXECUTABLE = {
        "command": CREDENTIAL_SOURCE_EXECUTABLE_COMMAND,
        "timeout_millis": 30000,
        "output_file": CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
    }
    CREDENTIAL_SOURCE = {"executable": CREDENTIAL_SOURCE_EXECUTABLE}
    EXECUTABLE_OIDC_TOKEN = "FAKE_ID_TOKEN"
    EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_ID_TOKEN = {
        "version": 1,
        "success": True,
        "token_type": "urn:ietf:params:oauth:token-type:id_token",
        "id_token": EXECUTABLE_OIDC_TOKEN,
        "expiration_time": 9999999999,
    }
    EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_JWT = {
        "version": 1,
        "success": True,
        "token_type": "urn:ietf:params:oauth:token-type:jwt",
        "id_token": EXECUTABLE_OIDC_TOKEN,
        "expiration_time": 9999999999,
    }
    EXECUTABLE_SAML_TOKEN = "FAKE_SAML_RESPONSE"
    EXECUTABLE_SUCCESSFUL_SAML_RESPONSE = {
        "version": 1,
        "success": True,
        "token_type": "urn:ietf:params:oauth:token-type:saml2",
        "saml_response": EXECUTABLE_SAML_TOKEN,
        "expiration_time": 9999999999,
    }
    EXECUTABLE_FAILED_RESPONSE = {
        "version": 1,
        "success": False,
        "code": "401",
        "message": "Permission denied. Caller not authorized",
    }
    CREDENTIAL_URL = "http://fakeurl.com"

    @classmethod
    def make_pluggable(
        cls,
        audience=AUDIENCE,
        subject_token_type=SUBJECT_TOKEN_TYPE,
        client_id=None,
        client_secret=None,
        quota_project_id=None,
        scopes=None,
        default_scopes=None,
        service_account_impersonation_url=None,
        credential_source=None,
        workforce_pool_user_project=None,
    ):
        return pluggable.Credentials(
            audience=audience,
            subject_token_type=subject_token_type,
            token_url=TOKEN_URL,
            service_account_impersonation_url=service_account_impersonation_url,
            credential_source=credential_source,
            client_id=client_id,
            client_secret=client_secret,
            quota_project_id=quota_project_id,
            scopes=scopes,
            default_scopes=default_scopes,
            workforce_pool_user_project=workforce_pool_user_project,
        )

    @mock.patch.object(pluggable.Credentials, "__init__", return_value=None)
    def test_from_info_full_options(self, mock_init):
        credentials = pluggable.Credentials.from_info(
            {
                "audience": AUDIENCE,
                "subject_token_type": SUBJECT_TOKEN_TYPE,
                "token_url": TOKEN_URL,
                "service_account_impersonation_url": SERVICE_ACCOUNT_IMPERSONATION_URL,
                "service_account_impersonation": {"token_lifetime_seconds": 2800},
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "quota_project_id": QUOTA_PROJECT_ID,
                "credential_source": self.CREDENTIAL_SOURCE,
            }
        )

        # Confirm pluggable.Credentials instantiated with expected attributes.
        assert isinstance(credentials, pluggable.Credentials)
        mock_init.assert_called_once_with(
            audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE,
            token_url=TOKEN_URL,
            service_account_impersonation_url=SERVICE_ACCOUNT_IMPERSONATION_URL,
            service_account_impersonation_options={"token_lifetime_seconds": 2800},
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            credential_source=self.CREDENTIAL_SOURCE,
            quota_project_id=QUOTA_PROJECT_ID,
            workforce_pool_user_project=None,
        )

    @mock.patch.object(pluggable.Credentials, "__init__", return_value=None)
    def test_from_info_required_options_only(self, mock_init):
        credentials = pluggable.Credentials.from_info(
            {
                "audience": AUDIENCE,
                "subject_token_type": SUBJECT_TOKEN_TYPE,
                "token_url": TOKEN_URL,
                "credential_source": self.CREDENTIAL_SOURCE,
            }
        )

        # Confirm pluggable.Credentials instantiated with expected attributes.
        assert isinstance(credentials, pluggable.Credentials)
        mock_init.assert_called_once_with(
            audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE,
            token_url=TOKEN_URL,
            service_account_impersonation_url=None,
            service_account_impersonation_options={},
            client_id=None,
            client_secret=None,
            credential_source=self.CREDENTIAL_SOURCE,
            quota_project_id=None,
            workforce_pool_user_project=None,
        )

    @mock.patch.object(pluggable.Credentials, "__init__", return_value=None)
    def test_from_file_full_options(self, mock_init, tmpdir):
        info = {
            "audience": AUDIENCE,
            "subject_token_type": SUBJECT_TOKEN_TYPE,
            "token_url": TOKEN_URL,
            "service_account_impersonation_url": SERVICE_ACCOUNT_IMPERSONATION_URL,
            "service_account_impersonation": {"token_lifetime_seconds": 2800},
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "quota_project_id": QUOTA_PROJECT_ID,
            "credential_source": self.CREDENTIAL_SOURCE,
        }
        config_file = tmpdir.join("config.json")
        config_file.write(json.dumps(info))
        credentials = pluggable.Credentials.from_file(str(config_file))

        # Confirm pluggable.Credentials instantiated with expected attributes.
        assert isinstance(credentials, pluggable.Credentials)
        mock_init.assert_called_once_with(
            audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE,
            token_url=TOKEN_URL,
            service_account_impersonation_url=SERVICE_ACCOUNT_IMPERSONATION_URL,
            service_account_impersonation_options={"token_lifetime_seconds": 2800},
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            credential_source=self.CREDENTIAL_SOURCE,
            quota_project_id=QUOTA_PROJECT_ID,
            workforce_pool_user_project=None,
        )

    @mock.patch.object(pluggable.Credentials, "__init__", return_value=None)
    def test_from_file_required_options_only(self, mock_init, tmpdir):
        info = {
            "audience": AUDIENCE,
            "subject_token_type": SUBJECT_TOKEN_TYPE,
            "token_url": TOKEN_URL,
            "credential_source": self.CREDENTIAL_SOURCE,
        }
        config_file = tmpdir.join("config.json")
        config_file.write(json.dumps(info))
        credentials = pluggable.Credentials.from_file(str(config_file))

        # Confirm pluggable.Credentials instantiated with expected attributes.
        assert isinstance(credentials, pluggable.Credentials)
        mock_init.assert_called_once_with(
            audience=AUDIENCE,
            subject_token_type=SUBJECT_TOKEN_TYPE,
            token_url=TOKEN_URL,
            service_account_impersonation_url=None,
            service_account_impersonation_options={},
            client_id=None,
            client_secret=None,
            credential_source=self.CREDENTIAL_SOURCE,
            quota_project_id=None,
            workforce_pool_user_project=None,
        )

    def test_constructor_invalid_options(self):
        credential_source = {"unsupported": "value"}

        with pytest.raises(ValueError) as excinfo:
            self.make_pluggable(credential_source=credential_source)

        assert excinfo.match(r"Missing credential_source")

    def test_constructor_invalid_credential_source(self):
        with pytest.raises(ValueError) as excinfo:
            self.make_pluggable(credential_source="non-dict")

        assert excinfo.match(r"Missing credential_source")

    def test_info_with_credential_source(self):
        credentials = self.make_pluggable(
            credential_source=self.CREDENTIAL_SOURCE.copy()
        )

        assert credentials.info == {
            "type": "external_account",
            "audience": AUDIENCE,
            "subject_token_type": SUBJECT_TOKEN_TYPE,
            "token_url": TOKEN_URL,
            "credential_source": self.CREDENTIAL_SOURCE,
        }

    @mock.patch.dict(
        os.environ,
        {
            "GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1",
            "GOOGLE_EXTERNAL_ACCOUNT_AUDIENCE": "original_audience",
            "GOOGLE_EXTERNAL_ACCOUNT_TOKEN_TYPE": "original_token_type",
            "GOOGLE_EXTERNAL_ACCOUNT_INTERACTIVE": "0",
            "GOOGLE_EXTERNAL_ACCOUNT_IMPERSONATED_EMAIL": "original_impersonated_email",
            "GOOGLE_EXTERNAL_ACCOUNT_OUTPUT_FILE": "original_output_file",
        },
    )
    def test_retrieve_subject_token_oidc_id_token(self):
        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(
                    self.EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_ID_TOKEN
                ).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(
                audience=AUDIENCE,
                service_account_impersonation_url=SERVICE_ACCOUNT_IMPERSONATION_URL,
                credential_source=self.CREDENTIAL_SOURCE,
            )

            subject_token = credentials.retrieve_subject_token(None)

            assert subject_token == self.EXECUTABLE_OIDC_TOKEN

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_oidc_jwt(self):
        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(self.EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_JWT).encode(
                    "UTF-8"
                ),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(
                audience=AUDIENCE,
                service_account_impersonation_url=SERVICE_ACCOUNT_IMPERSONATION_URL,
                credential_source=self.CREDENTIAL_SOURCE,
            )

            subject_token = credentials.retrieve_subject_token(None)

            assert subject_token == self.EXECUTABLE_OIDC_TOKEN

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_saml(self):
        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(self.EXECUTABLE_SUCCESSFUL_SAML_RESPONSE).encode(
                    "UTF-8"
                ),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            subject_token = credentials.retrieve_subject_token(None)

            assert subject_token == self.EXECUTABLE_SAML_TOKEN

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_failed(self):
        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(self.EXECUTABLE_FAILED_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(exceptions.RefreshError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(
                r"Executable returned unsuccessful response: code: 401, message: Permission denied. Caller not authorized."
            )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "0"})
    def test_retrieve_subject_token_not_allowd(self):
        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(
                    self.EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_ID_TOKEN
                ).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(ValueError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(r"Executables need to be explicitly allowed")

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_invalid_version(self):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_VERSION_2 = {
            "version": 2,
            "success": True,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 9999999999,
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_VERSION_2).encode(
                    "UTF-8"
                ),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(exceptions.RefreshError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(r"Executable returned unsupported version.")

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_expired_token(self):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_EXPIRED = {
            "version": 1,
            "success": True,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 0,
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_EXPIRED).encode(
                    "UTF-8"
                ),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(exceptions.RefreshError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(r"The token returned by the executable is expired.")

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_file_cache(self):
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE = "actual_output_file"
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE = {
            "command": "command",
            "timeout_millis": 30000,
            "output_file": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
        }
        ACTUAL_CREDENTIAL_SOURCE = {"executable": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE}
        with open(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE, "w") as output_file:
            json.dump(self.EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_ID_TOKEN, output_file)

        credentials = self.make_pluggable(credential_source=ACTUAL_CREDENTIAL_SOURCE)

        subject_token = credentials.retrieve_subject_token(None)
        assert subject_token == self.EXECUTABLE_OIDC_TOKEN

        os.remove(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE)

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_no_file_cache(self):
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE = {
            "command": "command",
            "timeout_millis": 30000,
        }
        ACTUAL_CREDENTIAL_SOURCE = {"executable": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE}

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(
                    self.EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_ID_TOKEN
                ).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(
                credential_source=ACTUAL_CREDENTIAL_SOURCE
            )

            subject_token = credentials.retrieve_subject_token(None)

            assert subject_token == self.EXECUTABLE_OIDC_TOKEN

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_file_cache_value_error_report(self):
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE = "actual_output_file"
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE = {
            "command": "command",
            "timeout_millis": 30000,
            "output_file": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
        }
        ACTUAL_CREDENTIAL_SOURCE = {"executable": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE}
        ACTUAL_EXECUTABLE_RESPONSE = {
            "success": True,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 9999999999,
        }
        with open(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE, "w") as output_file:
            json.dump(ACTUAL_EXECUTABLE_RESPONSE, output_file)

        credentials = self.make_pluggable(credential_source=ACTUAL_CREDENTIAL_SOURCE)

        with pytest.raises(ValueError) as excinfo:
            _ = credentials.retrieve_subject_token(None)

        assert excinfo.match(r"The executable response is missing the version field.")

        os.remove(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE)

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_file_cache_refresh_error_retry(self):
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE = "actual_output_file"
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE = {
            "command": "command",
            "timeout_millis": 30000,
            "output_file": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
        }
        ACTUAL_CREDENTIAL_SOURCE = {"executable": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE}
        ACTUAL_EXECUTABLE_RESPONSE = {
            "version": 2,
            "success": True,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 9999999999,
        }
        with open(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE, "w") as output_file:
            json.dump(ACTUAL_EXECUTABLE_RESPONSE, output_file)

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(
                    self.EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_ID_TOKEN
                ).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(
                credential_source=ACTUAL_CREDENTIAL_SOURCE
            )

            subject_token = credentials.retrieve_subject_token(None)

            assert subject_token == self.EXECUTABLE_OIDC_TOKEN

        os.remove(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE)

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_unsupported_token_type(self):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE = {
            "version": 1,
            "success": True,
            "token_type": "unsupported_token_type",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 9999999999,
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(exceptions.RefreshError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(r"Executable returned unsupported token type.")

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_missing_version(self):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE = {
            "success": True,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 9999999999,
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(ValueError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(
                r"The executable response is missing the version field."
            )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_missing_success(self):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE = {
            "version": 1,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 9999999999,
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(ValueError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(
                r"The executable response is missing the success field."
            )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_missing_error_code_message(self):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE = {"version": 1, "success": False}

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(ValueError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(
                r"Error code and message fields are required in the response."
            )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_without_expiration_time_should_fail_when_output_file_specified(
        self
    ):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE = {
            "version": 1,
            "success": True,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(ValueError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(
                r"The executable response must contain an expiration_time for successful responses when an output_file has been specified in the configuration."
            )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_without_expiration_time_should_fail_when_retrieving_from_output_file(
        self
    ):
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE = "actual_output_file"
        ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE = {
            "command": "command",
            "timeout_millis": 30000,
            "output_file": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
        }
        ACTUAL_CREDENTIAL_SOURCE = {"executable": ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE}
        data = self.EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE_ID_TOKEN.copy()
        data.pop("expiration_time")

        with open(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE, "w") as output_file:
            json.dump(data, output_file)

        credentials = self.make_pluggable(credential_source=ACTUAL_CREDENTIAL_SOURCE)

        with pytest.raises(ValueError) as excinfo:
            _ = credentials.retrieve_subject_token(None)

        assert excinfo.match(
            r"The executable response must contain an expiration_time for successful responses when an output_file has been specified in the configuration."
        )
        os.remove(ACTUAL_CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE)

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_without_expiration_time_should_pass_when_output_file_not_specified(
        self
    ):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE = {
            "version": 1,
            "success": True,
            "token_type": "urn:ietf:params:oauth:token-type:id_token",
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
        }

        CREDENTIAL_SOURCE = {
            "executable": {"command": "command", "timeout_millis": 30000}
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=CREDENTIAL_SOURCE)
            subject_token = credentials.retrieve_subject_token(None)

            assert subject_token == self.EXECUTABLE_OIDC_TOKEN

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_missing_token_type(self):
        EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE = {
            "version": 1,
            "success": True,
            "id_token": self.EXECUTABLE_OIDC_TOKEN,
            "expiration_time": 9999999999,
        }

        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[],
                stdout=json.dumps(EXECUTABLE_SUCCESSFUL_OIDC_RESPONSE).encode("UTF-8"),
                returncode=0,
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(ValueError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(
                r"The executable response is missing the token_type field."
            )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_credential_source_missing_command(self):
        with pytest.raises(ValueError) as excinfo:
            CREDENTIAL_SOURCE = {
                "executable": {
                    "timeout_millis": 30000,
                    "output_file": self.CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
                }
            }
            _ = self.make_pluggable(credential_source=CREDENTIAL_SOURCE)

        assert excinfo.match(
            r"Missing command field. Executable command must be provided."
        )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_credential_source_timeout_small(self):
        with pytest.raises(ValueError) as excinfo:
            CREDENTIAL_SOURCE = {
                "executable": {
                    "command": self.CREDENTIAL_SOURCE_EXECUTABLE_COMMAND,
                    "timeout_millis": 5000 - 1,
                    "output_file": self.CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
                }
            }
            _ = self.make_pluggable(credential_source=CREDENTIAL_SOURCE)

        assert excinfo.match(r"Timeout must be between 5 and 120 seconds.")

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_credential_source_timeout_large(self):
        with pytest.raises(ValueError) as excinfo:
            CREDENTIAL_SOURCE = {
                "executable": {
                    "command": self.CREDENTIAL_SOURCE_EXECUTABLE_COMMAND,
                    "timeout_millis": 120000 + 1,
                    "output_file": self.CREDENTIAL_SOURCE_EXECUTABLE_OUTPUT_FILE,
                }
            }
            _ = self.make_pluggable(credential_source=CREDENTIAL_SOURCE)

        assert excinfo.match(r"Timeout must be between 5 and 120 seconds.")

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_executable_fail(self):
        with mock.patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=[], stdout=None, returncode=1
            ),
        ):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(exceptions.RefreshError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(
                r"Executable exited with non-zero return code 1. Error: None"
            )

    @mock.patch.dict(os.environ, {"GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES": "1"})
    def test_retrieve_subject_token_python_2(self):
        with mock.patch("sys.version_info", (2, 7)):
            credentials = self.make_pluggable(credential_source=self.CREDENTIAL_SOURCE)

            with pytest.raises(exceptions.RefreshError) as excinfo:
                _ = credentials.retrieve_subject_token(None)

            assert excinfo.match(r"Pluggable auth is only supported for python 3.6+")
