"""Private module for fetching Google BigQuery credentials."""

import json
import logging
import os
import os.path

import pandas.compat

import pandas_gbq.exceptions

logger = logging.getLogger(__name__)


CREDENTIALS_CACHE_DIRNAME = "pandas_gbq"
CREDENTIALS_CACHE_FILENAME = "bigquery_credentials.dat"
SCOPES = ["https://www.googleapis.com/auth/bigquery"]

# The following constants are used for end-user authentication.
# It identifies (via credentials from the pandas-gbq-auth GCP project) the
# application that is requesting permission to access the BigQuery API on
# behalf of a G Suite or Gmail user.
#
# In a web application, the client secret would be kept secret, but this is not
# possible for applications that are installed locally on an end-user's
# machine.
#
# See: https://cloud.google.com/docs/authentication/end-user for details.
CLIENT_ID = (
    "725825577420-unm2gnkiprugilg743tkbig250f4sfsj.apps.googleusercontent.com"
)
CLIENT_SECRET = "4hqze9yI8fxShls8eJWkeMdJ"


def get_credentials(
    private_key=None, project_id=None, reauth=False, auth_local_webserver=False
):
    import pydata_google_auth

    if private_key:
        return get_service_account_credentials(private_key)

    credentials, default_project_id = pydata_google_auth.default(
        SCOPES,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        credentials_cache=get_credentials_cache(reauth),
        auth_local_webserver=auth_local_webserver,
    )

    project_id = project_id or default_project_id
    return credentials, project_id


def get_service_account_credentials(private_key):
    """DEPRECATED: Load service account credentials from key data or key path."""

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


def get_credentials_cache(reauth,):
    import pydata_google_auth.cache

    if reauth:
        return pydata_google_auth.cache.WriteOnlyCredentialsCache(
            dirname=CREDENTIALS_CACHE_DIRNAME,
            filename=CREDENTIALS_CACHE_FILENAME,
        )
    return pydata_google_auth.cache.ReadWriteCredentialsCache(
        dirname=CREDENTIALS_CACHE_DIRNAME, filename=CREDENTIALS_CACHE_FILENAME
    )
