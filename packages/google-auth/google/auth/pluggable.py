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

"""Pluggable Credentials.
Pluggable Credentials are initialized using external_account arguments which
are typically loaded from third-party executables. Unlike other
credentials that can be initialized with a list of explicit arguments, secrets
or credentials, external account clients use the environment and hints/guidelines
provided by the external_account JSON file to retrieve credentials and exchange
them for Google access tokens.

Example credential_source for pluggable credential:
{
    "executable": {
        "command": "/path/to/get/credentials.sh --arg1=value1 --arg2=value2",
        "timeout_millis": 5000,
        "output_file": "/path/to/generated/cached/credentials"
    }
}
"""

try:
    from collections.abc import Mapping
# Python 2.7 compatibility
except ImportError:  # pragma: NO COVER
    from collections import Mapping
import io
import json
import os
import subprocess
import time

from google.auth import _helpers
from google.auth import exceptions
from google.auth import external_account

# The max supported executable spec version.
EXECUTABLE_SUPPORTED_MAX_VERSION = 1


class Credentials(external_account.Credentials):
    """External account credentials sourced from executables."""

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
        workforce_pool_user_project=None,
    ):
        """Instantiates an external account credentials object from a executables.

        Args:
            audience (str): The STS audience field.
            subject_token_type (str): The subject token type.
            token_url (str): The STS endpoint URL.
            credential_source (Mapping): The credential source dictionary used to
                provide instructions on how to retrieve external credential to be
                exchanged for Google access tokens.

                Example credential_source for pluggable credential:

                    {
                        "executable": {
                            "command": "/path/to/get/credentials.sh --arg1=value1 --arg2=value2",
                            "timeout_millis": 5000,
                            "output_file": "/path/to/generated/cached/credentials"
                        }
                    }

            service_account_impersonation_url (Optional[str]): The optional service account
                impersonation getAccessToken URL.
            client_id (Optional[str]): The optional client ID.
            client_secret (Optional[str]): The optional client secret.
            quota_project_id (Optional[str]): The optional quota project ID.
            scopes (Optional[Sequence[str]]): Optional scopes to request during the
                authorization grant.
            default_scopes (Optional[Sequence[str]]): Default scopes passed by a
                Google client library. Use 'scopes' for user-defined scopes.
            workforce_pool_user_project (Optona[str]): The optional workforce pool user
                project number when the credential corresponds to a workforce pool and not
                a workload Pluggable. The underlying principal must still have
                serviceusage.services.use IAM permission to use the project for
                billing/quota.

        Raises:
            google.auth.exceptions.RefreshError: If an error is encountered during
                access token retrieval logic.
            ValueError: For invalid parameters.

        .. note:: Typically one of the helper constructors
            :meth:`from_file` or
            :meth:`from_info` are used instead of calling the constructor directly.
        """

        super(Credentials, self).__init__(
            audience=audience,
            subject_token_type=subject_token_type,
            token_url=token_url,
            credential_source=credential_source,
            service_account_impersonation_url=service_account_impersonation_url,
            client_id=client_id,
            client_secret=client_secret,
            quota_project_id=quota_project_id,
            scopes=scopes,
            default_scopes=default_scopes,
            workforce_pool_user_project=workforce_pool_user_project,
        )
        if not isinstance(credential_source, Mapping):
            self._credential_source_executable = None
            raise ValueError(
                "Missing credential_source. The credential_source is not a dict."
            )
        self._credential_source_executable = credential_source.get("executable")
        if not self._credential_source_executable:
            raise ValueError(
                "Missing credential_source. An 'executable' must be provided."
            )
        self._credential_source_executable_command = self._credential_source_executable.get(
            "command"
        )
        self._credential_source_executable_timeout_millis = self._credential_source_executable.get(
            "timeout_millis"
        )
        self._credential_source_executable_output_file = self._credential_source_executable.get(
            "output_file"
        )

        if not self._credential_source_executable_command:
            raise ValueError(
                "Missing command field. Executable command must be provided."
            )
        if not self._credential_source_executable_timeout_millis:
            self._credential_source_executable_timeout_millis = 30 * 1000
        elif (
            self._credential_source_executable_timeout_millis < 5 * 1000
            or self._credential_source_executable_timeout_millis > 120 * 1000
        ):
            raise ValueError("Timeout must be between 5 and 120 seconds.")

    @_helpers.copy_docstring(external_account.Credentials)
    def retrieve_subject_token(self, request):
        env_allow_executables = os.environ.get(
            "GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES"
        )
        if env_allow_executables != "1":
            raise ValueError(
                "Executables need to be explicitly allowed (set GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES to '1') to run."
            )

        # Check output file.
        if self._credential_source_executable_output_file is not None:
            try:
                with open(
                    self._credential_source_executable_output_file
                ) as output_file:
                    response = json.load(output_file)
            except Exception:
                pass
            else:
                try:
                    # If the cached response is expired, _parse_subject_token will raise an error which will be ignored and we will call the executable again.
                    subject_token = self._parse_subject_token(response)
                except ValueError:
                    raise
                except exceptions.RefreshError:
                    pass
                else:
                    return subject_token

        if not _helpers.is_python_3():
            raise exceptions.RefreshError(
                "Pluggable auth is only supported for python 3.6+"
            )

        # Inject env vars.
        env = os.environ.copy()
        env["GOOGLE_EXTERNAL_ACCOUNT_AUDIENCE"] = self._audience
        env["GOOGLE_EXTERNAL_ACCOUNT_TOKEN_TYPE"] = self._subject_token_type
        env[
            "GOOGLE_EXTERNAL_ACCOUNT_INTERACTIVE"
        ] = "0"  # Always set to 0 until interactive mode is implemented.
        if self._service_account_impersonation_url is not None:
            env[
                "GOOGLE_EXTERNAL_ACCOUNT_IMPERSONATED_EMAIL"
            ] = self.service_account_email
        if self._credential_source_executable_output_file is not None:
            env[
                "GOOGLE_EXTERNAL_ACCOUNT_OUTPUT_FILE"
            ] = self._credential_source_executable_output_file

        try:
            result = subprocess.run(
                self._credential_source_executable_command.split(),
                timeout=self._credential_source_executable_timeout_millis / 1000,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
            )
            if result.returncode != 0:
                raise exceptions.RefreshError(
                    "Executable exited with non-zero return code {}. Error: {}".format(
                        result.returncode, result.stdout
                    )
                )
        except Exception:
            raise
        else:
            try:
                data = result.stdout.decode("utf-8")
                response = json.loads(data)
                subject_token = self._parse_subject_token(response)
            except Exception:
                raise

        return subject_token

    @classmethod
    def from_info(cls, info, **kwargs):
        """Creates a Pluggable Credentials instance from parsed external account info.

        Args:
            info (Mapping[str, str]): The Pluggable external account info in Google
                format.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.pluggable.Credentials: The constructed
                credentials.

        Raises:
            ValueError: For invalid parameters.
        """
        return cls(
            audience=info.get("audience"),
            subject_token_type=info.get("subject_token_type"),
            token_url=info.get("token_url"),
            service_account_impersonation_url=info.get(
                "service_account_impersonation_url"
            ),
            client_id=info.get("client_id"),
            client_secret=info.get("client_secret"),
            credential_source=info.get("credential_source"),
            quota_project_id=info.get("quota_project_id"),
            workforce_pool_user_project=info.get("workforce_pool_user_project"),
            **kwargs
        )

    @classmethod
    def from_file(cls, filename, **kwargs):
        """Creates an Pluggable Credentials instance from an external account json file.

        Args:
            filename (str): The path to the Pluggable external account json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.pluggable.Credentials: The constructed
                credentials.
        """
        with io.open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return cls.from_info(data, **kwargs)

    def _parse_subject_token(self, response):
        if "version" not in response:
            raise ValueError("The executable response is missing the version field.")
        if response["version"] > EXECUTABLE_SUPPORTED_MAX_VERSION:
            raise exceptions.RefreshError(
                "Executable returned unsupported version {}.".format(
                    response["version"]
                )
            )
        if "success" not in response:
            raise ValueError("The executable response is missing the success field.")
        if not response["success"]:
            if "code" not in response or "message" not in response:
                raise ValueError(
                    "Error code and message fields are required in the response."
                )
            raise exceptions.RefreshError(
                "Executable returned unsuccessful response: code: {}, message: {}.".format(
                    response["code"], response["message"]
                )
            )
        if "expiration_time" not in response:
            raise ValueError(
                "The executable response is missing the expiration_time field."
            )
        if response["expiration_time"] < time.time():
            raise exceptions.RefreshError(
                "The token returned by the executable is expired."
            )
        if "token_type" not in response:
            raise ValueError("The executable response is missing the token_type field.")
        if (
            response["token_type"] == "urn:ietf:params:oauth:token-type:jwt"
            or response["token_type"] == "urn:ietf:params:oauth:token-type:id_token"
        ):  # OIDC
            return response["id_token"]
        elif response["token_type"] == "urn:ietf:params:oauth:token-type:saml2":  # SAML
            return response["saml_response"]
        else:
            raise exceptions.RefreshError("Executable returned unsupported token type.")
