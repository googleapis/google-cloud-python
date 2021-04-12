# Copyright 2021 The PyBigQuery Authors
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from google.api_core import client_info
import google.auth
from google.cloud import bigquery
from google.oauth2 import service_account
import sqlalchemy


USER_AGENT_TEMPLATE = "sqlalchemy/{}"
SCOPES = (
    "https://www.googleapis.com/auth/bigquery",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/drive",
)


def google_client_info():
    user_agent = USER_AGENT_TEMPLATE.format(sqlalchemy.__version__)
    return client_info.ClientInfo(user_agent=user_agent)


def create_bigquery_client(
    credentials_info=None,
    credentials_path=None,
    default_query_job_config=None,
    location=None,
    project_id=None,
):
    default_project = None

    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        credentials = credentials.with_scopes(SCOPES)
        default_project = credentials.project_id
    elif credentials_info:
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )
        credentials = credentials.with_scopes(SCOPES)
        default_project = credentials.project_id
    else:
        credentials, default_project = google.auth.default(scopes=SCOPES)

    if project_id is None:
        project_id = default_project

    return bigquery.Client(
        client_info=google_client_info(),
        project=project_id,
        credentials=credentials,
        location=location,
        default_query_job_config=default_query_job_config,
    )
