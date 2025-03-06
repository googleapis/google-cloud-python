# Copyright 2023 Google LLC
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

import typing
import warnings

from google.cloud import bigquery
import pytest

import bigframes
import bigframes.constants
import bigframes.session.clients


def _assert_bq_execution_location(
    session: bigframes.Session, expected_location: typing.Optional[str] = None
):
    df = session.read_gbq(
        """
        SELECT "aaa" as name, 111 as number
        UNION ALL
        SELECT "bbb" as name, 222 as number
        UNION ALL
        SELECT "aaa" as name, 333 as number
    """
    )

    if expected_location is None:
        expected_location = session._location

    assert typing.cast(bigquery.QueryJob, df.query_job).location == expected_location

    result = (
        df[["name", "number"]]
        .groupby("name")
        .sum(numeric_only=True)
        .sort_values("number", ascending=False)
        .head()
    )

    assert (
        typing.cast(bigquery.QueryJob, result.query_job).location == expected_location
    )


def test_bq_location_default():
    session = bigframes.Session()

    assert session.bqclient.location == "US"

    # by default global endpoint is used
    assert (
        session.bqclient._connection.API_BASE_URL == "https://bigquery.googleapis.com"
    )

    # assert that bigframes session honors the location
    _assert_bq_execution_location(session)


@pytest.mark.parametrize(
    "bigquery_location",
    # Sort the set to avoid nondeterminism.
    sorted(bigframes.constants.ALL_BIGQUERY_LOCATIONS),
)
def test_bq_location(bigquery_location):
    session = bigframes.Session(
        context=bigframes.BigQueryOptions(location=bigquery_location)
    )

    assert session.bqclient.location == bigquery_location

    # by default global endpoint is used
    assert (
        session.bqclient._connection.API_BASE_URL == "https://bigquery.googleapis.com"
    )

    # assert that bigframes session honors the location
    _assert_bq_execution_location(session)


@pytest.mark.parametrize(
    ("set_location", "resolved_location"),
    # Sort the set to avoid nondeterminism.
    [
        (loc.capitalize(), loc)
        for loc in sorted(bigframes.constants.ALL_BIGQUERY_LOCATIONS)
    ],
)
def test_bq_location_non_canonical(set_location, resolved_location):
    session = bigframes.Session(
        context=bigframes.BigQueryOptions(location=set_location)
    )

    assert session.bqclient.location == resolved_location

    # by default global endpoint is used
    assert (
        session.bqclient._connection.API_BASE_URL == "https://bigquery.googleapis.com"
    )

    # assert that bigframes session honors the location
    _assert_bq_execution_location(session, resolved_location)


@pytest.mark.parametrize(
    "bigquery_location",
    # Sort the set to avoid nondeterminism.
    sorted(bigframes.constants.REP_ENABLED_BIGQUERY_LOCATIONS),
)
def test_bq_rep_endpoints(bigquery_location):
    with warnings.catch_warnings(record=True) as record:
        warnings.simplefilter("always")
        session = bigframes.Session(
            context=bigframes.BigQueryOptions(
                location=bigquery_location, use_regional_endpoints=True
            )
        )
        assert (
            len([warn for warn in record if isinstance(warn.message, FutureWarning)])
            == 0
        )

    # Verify that location and endpoints are correctly set for the BigQuery API
    # client
    # TODO(shobs): Figure out if the same can be verified for the other API
    # clients.
    assert session.bqclient.location == bigquery_location
    assert (
        session.bqclient._connection.API_BASE_URL
        == "https://bigquery.{location}.rep.googleapis.com".format(
            location=bigquery_location
        )
    )

    # assert that bigframes session honors the location
    _assert_bq_execution_location(session)


@pytest.mark.parametrize(
    "bigquery_location",
    # Sort the set to avoid nondeterminism.
    sorted(bigframes.constants.LEP_ENABLED_BIGQUERY_LOCATIONS),
)
def test_bq_lep_endpoints(bigquery_location):
    # We are not testing BigFrames Session for LEP endpoints because it involves
    # query execution using the endpoint, which requires the project to be
    # allowlisted for LEP access. We could hardcode one project which is
    # allowlisted but then not every open source developer will have access to
    # that. Let's rely on just creating the clients for LEP.
    with pytest.warns(FutureWarning) as record:
        clients_provider = bigframes.session.clients.ClientsProvider(
            location=bigquery_location, use_regional_endpoints=True
        )
        assert len(record) == 1
        assert bigquery_location in typing.cast(Warning, record[0].message).args[0]

    # Verify that location and endpoints are correctly set for the BigQuery API
    # client
    # TODO(shobs): Figure out if the same can be verified for the other API
    # clients.
    assert clients_provider.bqclient.location == bigquery_location
    assert (
        clients_provider.bqclient._connection.API_BASE_URL
        == "https://{location}-bigquery.googleapis.com".format(
            location=bigquery_location
        )
    )
