# Copyright 2019 Google LLC
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

"""Get user credentials from interactive code environments.

This module contains helpers for getting user credentials from interactive
code environments installed on a development machine, such as Jupyter
notebooks.
"""

from __future__ import absolute_import

import google_auth_oauthlib.flow


def get_user_credentials(scopes, client_id, client_secret):
    """Gets credentials associated with your Google user account.

    This function authenticates using your user credentials by going through
    the OAuth 2.0 flow. You'll open a browser window to authenticate to your
    Google account. The permissions it requests correspond to the scopes
    you've provided.

    To obtain the ``client_id`` and ``client_secret``, create an **OAuth
    client ID** with application type **Other** from the `Credentials page on
    the Google Developer's Console
    <https://console.developers.google.com/apis/credentials>`_. Learn more
    with the `Authenticating as an end user
    <https://cloud.google.com/docs/authentication/end-user>`_ guide.

    Args:
        scopes (Sequence[str]):
            A list of scopes to use when authenticating to Google APIs. See
            the `list of OAuth 2.0 scopes for Google APIs
            <https://developers.google.com/identity/protocols/googlescopes>`_.
        client_id (str):
            A string that identifies your application to Google APIs. Find
            this value in the `Credentials page on the Google Developer's
            Console
            <https://console.developers.google.com/apis/credentials>`_.
        client_secret (str):
            A string that verifies your application to Google APIs. Find this
            value in the `Credentials page on the Google Developer's Console
            <https://console.developers.google.com/apis/credentials>`_.

    Returns:
        google.oauth2.credentials.Credentials:
            The OAuth 2.0 credentials for the user.

    Examples:
        Get credentials for your user account and use them to run a query
        with BigQuery::

            import google_auth_oauthlib

            # TODO: Create a client ID for your project.
            client_id = "YOUR-CLIENT-ID.apps.googleusercontent.com"
            client_secret = "abc_ThIsIsAsEcReT"

            # TODO: Choose the needed scopes for your applications.
            scopes = ["https://www.googleapis.com/auth/cloud-platform"]

            credentials = google_auth_oauthlib.get_user_credentials(
                scopes, client_id, client_secret
            )

            # 1. Open the link.
            # 2. Authorize the application to have access to your account.
            # 3. Copy and paste the authorization code to the prompt.

            # Use the credentials to construct a client for Google APIs.
            from google.cloud import bigquery

            bigquery_client = bigquery.Client(
                credentials=credentials, project="your-project-id"
            )
            print(list(bigquery_client.query("SELECT 1").result()))
    """

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    app_flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
        client_config, scopes=scopes
    )

    return app_flow.run_console()
