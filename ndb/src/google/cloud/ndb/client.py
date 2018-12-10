# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A client for NDB which manages credentials, project, namespace."""

import os

from google.cloud import environment_vars
from google.cloud.client import ClientWithProject
from google.cloud import _helpers

_DATASTORE_HOST = "datastore.googleapis.com"


def _get_gcd_project():
    """Gets the GCD application ID if it can be inferred."""
    return os.getenv(environment_vars.GCD_DATASET)


def _determine_default_project(project=None):
    """Determine default project explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * DATASTORE_DATASET environment variable (for ``gcd`` / emulator testing)
    * GOOGLE_CLOUD_PROJECT environment variable
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type project: str
    :param project: Optional. The project to use as default.

    :rtype: str or ``NoneType``
    :returns: Default project if it can be determined.
    """
    if project is None:
        project = _get_gcd_project()

    if project is None:
        project = _helpers._determine_default_project(project=project)

    return project


class Client(ClientWithProject):
    """An NDB client.

    Arguments:
        project (Optional[str]): The project to pass to proxied API methods. If
            not passed, falls back to the default inferred from the
            environment.
        namespace (Optional[str]): Namespace to pass to proxied API methods.
        credentials (Optional[:class:`~google.auth.credentials.Credentials`]):
            The OAuth2 Credentials to use for this client. If not passed, falls
            back to the default inferred from the environment.
    """

    SCOPE = ("https://www.googleapis.com/auth/datastore",)
    """The scopes required for authenticating as a Cloud Datastore consumer."""

    def __init__(self, project=None, namespace=None, credentials=None):
        super(Client, self).__init__(project=project, credentials=credentials)
        self.namespace = namespace
        self.host = os.environ.get(environment_vars.GCD_HOST, _DATASTORE_HOST)

    @property
    def _http(self):
        """Getter for object used for HTTP transport.

        Raises:
            NotImplementedError: Always, HTTP transport is not supported.
        """
        raise NotImplementedError("HTTP transport is not supported.")

    @staticmethod
    def _determine_default(project):
        """Helper:  override default project detection."""
        return _determine_default_project(project)
