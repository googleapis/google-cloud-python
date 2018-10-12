"""Private module for fetching Google BigQuery credentials."""

import json
import logging
import os
import os.path

import pandas.compat

import pandas_gbq.exceptions

logger = logging.getLogger(__name__)


SCOPES = ["https://www.googleapis.com/auth/bigquery"]


def get_credentials(
    private_key=None,
    project_id=None,
    reauth=False,
    auth_local_webserver=False,
    try_credentials=None,
):
    if try_credentials is None:
        try_credentials = _try_credentials

    if private_key:
        return get_service_account_credentials(private_key)

    # Try to retrieve Application Default Credentials
    credentials, default_project = get_application_default_credentials(
        try_credentials, project_id=project_id
    )

    if credentials:
        return credentials, default_project

    credentials = get_user_account_credentials(
        try_credentials,
        project_id=project_id,
        reauth=reauth,
        auth_local_webserver=auth_local_webserver,
    )
    return credentials, project_id


def get_service_account_credentials(private_key):
    import google.auth.transport.requests
    from google.oauth2.service_account import Credentials

    is_path = os.path.isfile(private_key)

    try:
        if is_path:
            with open(private_key) as f:
                json_key = json.loads(f.read())
        else:
            # ugly hack: 'private_key' field has new lines inside,
            # they break json parser, but we need to preserve them
            json_key = json.loads(private_key.replace("\n", "   "))
            json_key["private_key"] = json_key["private_key"].replace(
                "   ", "\n"
            )

        if pandas.compat.PY3:
            json_key["private_key"] = bytes(json_key["private_key"], "UTF-8")

        credentials = Credentials.from_service_account_info(json_key)
        credentials = credentials.with_scopes(SCOPES)

        # Refresh the token before trying to use it.
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)

        return credentials, json_key.get("project_id")
    except (KeyError, ValueError, TypeError, AttributeError):
        raise pandas_gbq.exceptions.InvalidPrivateKeyFormat(
            "Detected private_key as {}. ".format(
                "path" if is_path else "contents"
            )
            + "Private key is missing or invalid. It should be service "
            "account private key JSON (file path or string contents) "
            'with at least two keys: "client_email" and "private_key". '
            "Can be obtained from: https://console.developers.google."
            "com/permissions/serviceaccounts"
        )


def get_application_default_credentials(try_credentials, project_id=None):
    """
    This method tries to retrieve the "default application credentials".
    This could be useful for running code on Google Cloud Platform.

    Parameters
    ----------
    project_id (str, optional): Override the default project ID.

    Returns
    -------
    - GoogleCredentials,
        If the default application credentials can be retrieved
        from the environment. The retrieved credentials should also
        have access to the project (project_id) on BigQuery.
    - OR None,
        If default application credentials can not be retrieved
        from the environment. Or, the retrieved credentials do not
        have access to the project (project_id) on BigQuery.
    """
    import google.auth
    from google.auth.exceptions import DefaultCredentialsError

    try:
        credentials, default_project = google.auth.default(scopes=SCOPES)
    except (DefaultCredentialsError, IOError):
        return None, None

    # Even though we now have credentials, check that the credentials can be
    # used with BigQuery. For example, we could be running on a GCE instance
    # that does not allow the BigQuery scopes.
    billing_project = project_id or default_project
    return try_credentials(billing_project, credentials), billing_project


def get_user_account_credentials(
    try_credentials,
    project_id=None,
    reauth=False,
    auth_local_webserver=False,
    credentials_path=None,
):
    """Gets user account credentials.

    This method authenticates using user credentials, either loading saved
    credentials from a file or by going through the OAuth flow.

    Parameters
    ----------
    None

    Returns
    -------
    GoogleCredentials : credentials
        Credentials for the user with BigQuery access.
    """
    from google_auth_oauthlib.flow import InstalledAppFlow
    from oauthlib.oauth2.rfc6749.errors import OAuth2Error

    # Use the default credentials location under ~/.config and the
    # equivalent directory on windows if the user has not specified a
    # credentials path.
    if not credentials_path:
        credentials_path = get_default_credentials_path()

        # Previously, pandas-gbq saved user account credentials in the
        # current working directory. If the bigquery_credentials.dat file
        # exists in the current working directory, move the credentials to
        # the new default location.
        if os.path.isfile("bigquery_credentials.dat"):
            os.rename("bigquery_credentials.dat", credentials_path)

    credentials = None
    if not reauth:
        credentials = load_user_account_credentials(
            try_credentials,
            project_id=project_id,
            credentials_path=credentials_path,
        )

    client_config = {
        "installed": {
            "client_id": (
                "495642085510-k0tmvj2m941jhre2nbqka17vqpjfddtd"
                ".apps.googleusercontent.com"
            ),
            "client_secret": "kOc9wMptUtxkcIFbtZCcrEAc",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
        }
    }

    if credentials is None:
        app_flow = InstalledAppFlow.from_client_config(
            client_config, scopes=SCOPES
        )

        try:
            if auth_local_webserver:
                credentials = app_flow.run_local_server()
            else:
                credentials = app_flow.run_console()
        except OAuth2Error as ex:
            raise pandas_gbq.exceptions.AccessDenied(
                "Unable to get valid credentials: {0}".format(ex)
            )

        save_user_account_credentials(credentials, credentials_path)

    return credentials


def load_user_account_credentials(
    try_credentials, project_id=None, credentials_path=None
):
    """
    Loads user account credentials from a local file.

    .. versionadded 0.2.0

    Parameters
    ----------
    None

    Returns
    -------
    - GoogleCredentials,
        If the credentials can loaded. The retrieved credentials should
        also have access to the project (project_id) on BigQuery.
    - OR None,
        If credentials can not be loaded from a file. Or, the retrieved
        credentials do not have access to the project (project_id)
        on BigQuery.
    """
    import google.auth.transport.requests
    from google.oauth2.credentials import Credentials

    try:
        with open(credentials_path) as credentials_file:
            credentials_json = json.load(credentials_file)
    except (IOError, ValueError):
        return None

    credentials = Credentials(
        token=credentials_json.get("access_token"),
        refresh_token=credentials_json.get("refresh_token"),
        id_token=credentials_json.get("id_token"),
        token_uri=credentials_json.get("token_uri"),
        client_id=credentials_json.get("client_id"),
        client_secret=credentials_json.get("client_secret"),
        scopes=credentials_json.get("scopes"),
    )

    # Refresh the token before trying to use it.
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)

    return try_credentials(project_id, credentials)


def get_default_credentials_path():
    """
    Gets the default path to the BigQuery credentials

    .. versionadded 0.3.0

    Returns
    -------
    Path to the BigQuery credentials
    """
    if os.name == "nt":
        config_path = os.environ["APPDATA"]
    else:
        config_path = os.path.join(os.path.expanduser("~"), ".config")

    config_path = os.path.join(config_path, "pandas_gbq")

    # Create a pandas_gbq directory in an application-specific hidden
    # user folder on the operating system.
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    return os.path.join(config_path, "bigquery_credentials.dat")


def save_user_account_credentials(credentials, credentials_path):
    """
    Saves user account credentials to a local file.

    .. versionadded 0.2.0
    """
    try:
        with open(credentials_path, "w") as credentials_file:
            credentials_json = {
                "refresh_token": credentials.refresh_token,
                "id_token": credentials.id_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": credentials.scopes,
            }
            json.dump(credentials_json, credentials_file)
    except IOError:
        logger.warning("Unable to save credentials.")


def _try_credentials(project_id, credentials):
    from google.cloud import bigquery
    import google.api_core.exceptions
    import google.auth.exceptions

    if not credentials:
        return None
    if not project_id:
        return credentials

    try:
        client = bigquery.Client(project=project_id, credentials=credentials)
        # Check if the application has rights to the BigQuery project
        client.query("SELECT 1").result()
        return credentials
    except google.api_core.exceptions.GoogleAPIError:
        return None
    except google.auth.exceptions.RefreshError:
        # Sometimes (such as on Travis) google-auth returns GCE credentials,
        # but fetching the token for those credentials doesn't actually work.
        # See:
        # https://github.com/googleapis/google-auth-library-python/issues/287
        return None
