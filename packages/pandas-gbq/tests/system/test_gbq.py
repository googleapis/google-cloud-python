# -*- coding: utf-8 -*-

import sys
import uuid
from datetime import datetime

import google.oauth2.service_account
import numpy as np
import pandas.util.testing as tm
import pytest
import pytz
from pandas import DataFrame, NaT, compat
from pandas.compat import range, u

from pandas_gbq import gbq


TABLE_ID = "new_test"


def test_imports():
    try:
        import pkg_resources  # noqa
    except ImportError:
        raise ImportError("Could not import pkg_resources (setuptools).")

    gbq._test_google_api_imports()


@pytest.fixture(params=["env"])
def project(request, project_id):
    if request.param == "env":
        return project_id
    elif request.param == "none":
        return None


@pytest.fixture()
def credentials(private_key_path):
    return google.oauth2.service_account.Credentials.from_service_account_file(
        private_key_path
    )


@pytest.fixture()
def gbq_connector(project, credentials):
    return gbq.GbqConnector(project, credentials=credentials)


@pytest.fixture(scope="module")
def bigquery_client(project_id, private_key_path):
    from google.cloud import bigquery

    return bigquery.Client.from_service_account_json(
        private_key_path, project=project_id
    )


@pytest.fixture()
def random_dataset_id(bigquery_client):
    import google.api_core.exceptions

    dataset_id = "".join(["pandas_gbq_", str(uuid.uuid4()).replace("-", "_")])
    dataset_ref = bigquery_client.dataset(dataset_id)
    yield dataset_id
    try:
        bigquery_client.delete_dataset(dataset_ref, delete_contents=True)
    except google.api_core.exceptions.NotFound:
        pass  # Not all tests actually create a dataset


@pytest.fixture()
def tokyo_dataset(bigquery_client, random_dataset_id):
    from google.cloud import bigquery

    dataset_ref = bigquery_client.dataset(random_dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "asia-northeast1"
    bigquery_client.create_dataset(dataset)
    return random_dataset_id


@pytest.fixture()
def tokyo_table(bigquery_client, tokyo_dataset):
    table_id = "tokyo_table"
    # Create a random table using DDL.
    # https://github.com/GoogleCloudPlatform/golang-samples/blob/2ab2c6b79a1ea3d71d8f91609b57a8fbde07ae5d/bigquery/snippets/snippet.go#L739
    bigquery_client.query(
        """CREATE TABLE {}.{}
        AS SELECT
          2000 + CAST(18 * RAND() as INT64) as year,
          IF(RAND() > 0.5,"foo","bar") as token
        FROM UNNEST(GENERATE_ARRAY(0,5,1)) as r
        """.format(
            tokyo_dataset, table_id
        ),
        location="asia-northeast1",
    ).result()
    return table_id


@pytest.fixture()
def gbq_dataset(project, credentials):
    return gbq._Dataset(project, credentials=credentials)


@pytest.fixture()
def gbq_table(project, credentials, random_dataset_id):
    return gbq._Table(project, random_dataset_id, credentials=credentials)


def make_mixed_dataframe_v2(test_size):
    # create df to test for all BQ datatypes except RECORD
    bools = np.random.randint(2, size=(1, test_size)).astype(bool)
    flts = np.random.randn(1, test_size)
    ints = np.random.randint(1, 10, size=(1, test_size))
    strs = np.random.randint(1, 10, size=(1, test_size)).astype(str)
    times = [
        datetime.now(pytz.timezone("US/Arizona")) for t in range(test_size)
    ]
    return DataFrame(
        {
            "bools": bools[0],
            "flts": flts[0],
            "ints": ints[0],
            "strs": strs[0],
            "times": times[0],
        },
        index=range(test_size),
    )


class TestGBQConnectorIntegration(object):
    def test_should_be_able_to_make_a_connector(self, gbq_connector):
        assert gbq_connector is not None, "Could not create a GbqConnector"

    def test_should_be_able_to_get_a_bigquery_client(self, gbq_connector):
        bigquery_client = gbq_connector.get_client()
        assert bigquery_client is not None

    def test_should_be_able_to_get_schema_from_query(self, gbq_connector):
        schema, pages = gbq_connector.run_query("SELECT 1")
        assert schema is not None

    def test_should_be_able_to_get_results_from_query(self, gbq_connector):
        schema, pages = gbq_connector.run_query("SELECT 1")
        assert pages is not None


def test_should_read(project, credentials):
    query = 'SELECT "PI" AS valid_string'
    df = gbq.read_gbq(
        query, project_id=project, credentials=credentials, dialect="legacy"
    )
    tm.assert_frame_equal(df, DataFrame({"valid_string": ["PI"]}))


class TestReadGBQIntegration(object):
    @pytest.fixture(autouse=True)
    def setup(self, project, credentials):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test is
        # executed.
        self.gbq_connector = gbq.GbqConnector(project, credentials=credentials)
        self.credentials = credentials

    def test_should_properly_handle_empty_strings(self, project_id):
        query = 'SELECT "" AS empty_string'
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"empty_string": [""]}))

    def test_should_properly_handle_null_strings(self, project_id):
        query = "SELECT STRING(NULL) AS null_string"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"null_string": [None]}))

    def test_should_properly_handle_valid_integers(self, project_id):
        query = "SELECT INTEGER(3) AS valid_integer"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"valid_integer": [3]}))

    def test_should_properly_handle_nullable_integers(self, project_id):
        query = """SELECT * FROM
                    (SELECT 1 AS nullable_integer),
                    (SELECT NULL AS nullable_integer)"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"nullable_integer": [1, None]}))

    def test_should_properly_handle_valid_longs(self, project_id):
        query = "SELECT 1 << 62 AS valid_long"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"valid_long": [1 << 62]}))

    def test_should_properly_handle_nullable_longs(self, project_id):
        query = """SELECT * FROM
                    (SELECT 1 << 62 AS nullable_long),
                    (SELECT NULL AS nullable_long)"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(
            df, DataFrame({"nullable_long": [1 << 62, None]})
        )

    def test_should_properly_handle_null_integers(self, project_id):
        query = "SELECT INTEGER(NULL) AS null_integer"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"null_integer": [None]}))

    def test_should_properly_handle_valid_floats(self, project_id):
        from math import pi

        query = "SELECT PI() AS valid_float"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"valid_float": [pi]}))

    def test_should_properly_handle_nullable_floats(self, project_id):
        from math import pi

        query = """SELECT * FROM
                    (SELECT PI() AS nullable_float),
                    (SELECT NULL AS nullable_float)"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"nullable_float": [pi, None]}))

    def test_should_properly_handle_valid_doubles(self, project_id):
        from math import pi

        query = "SELECT PI() * POW(10, 307) AS valid_double"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(
            df, DataFrame({"valid_double": [pi * 10 ** 307]})
        )

    def test_should_properly_handle_nullable_doubles(self, project_id):
        from math import pi

        query = """SELECT * FROM
                    (SELECT PI() * POW(10, 307) AS nullable_double),
                    (SELECT NULL AS nullable_double)"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(
            df, DataFrame({"nullable_double": [pi * 10 ** 307, None]})
        )

    def test_should_properly_handle_null_floats(self, project_id):
        query = "SELECT FLOAT(NULL) AS null_float"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"null_float": [np.nan]}))

    def test_should_properly_handle_timestamp_unix_epoch(self, project_id):
        query = 'SELECT TIMESTAMP("1970-01-01 00:00:00") AS unix_epoch'
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(
            df,
            DataFrame(
                {"unix_epoch": [np.datetime64("1970-01-01T00:00:00.000000Z")]}
            ),
        )

    def test_should_properly_handle_arbitrary_timestamp(self, project_id):
        query = 'SELECT TIMESTAMP("2004-09-15 05:00:00") AS valid_timestamp'
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(
            df,
            DataFrame(
                {
                    "valid_timestamp": [
                        np.datetime64("2004-09-15T05:00:00.000000Z")
                    ]
                }
            ),
        )

    @pytest.mark.parametrize(
        "expression, type_",
        [
            ("current_date()", "<M8[ns]"),
            ("current_timestamp()", "<M8[ns]"),
            ("current_datetime()", "<M8[ns]"),
            ("TRUE", bool),
            ("FALSE", bool),
        ],
    )
    def test_return_correct_types(self, project_id, expression, type_):
        """
        All type checks can be added to this function using additional
        parameters, rather than creating additional functions.
        We can consolidate the existing functions here in time

        TODO: time doesn't currently parse
        ("time(12,30,00)", "<M8[ns]"),
        """
        query = "SELECT {} AS _".format(expression)
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="standard",
        )
        assert df["_"].dtype == type_

    def test_should_properly_handle_null_timestamp(self, project_id):
        query = "SELECT TIMESTAMP(NULL) AS null_timestamp"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"null_timestamp": [NaT]}))

    def test_should_properly_handle_null_boolean(self, project_id):
        query = "SELECT BOOLEAN(NULL) AS null_boolean"
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"null_boolean": [None]}))

    def test_should_properly_handle_nullable_booleans(self, project_id):
        query = """SELECT * FROM
                    (SELECT BOOLEAN(TRUE) AS nullable_boolean),
                    (SELECT NULL AS nullable_boolean)"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(
            df, DataFrame({"nullable_boolean": [True, None]}).astype(object)
        )

    def test_unicode_string_conversion_and_normalization(self, project_id):
        correct_test_datatype = DataFrame({"unicode_string": [u("\xe9\xfc")]})

        unicode_string = "\xc3\xa9\xc3\xbc"

        if compat.PY3:
            unicode_string = unicode_string.encode("latin-1").decode("utf8")

        query = 'SELECT "{0}" AS unicode_string'.format(unicode_string)

        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, correct_test_datatype)

    def test_index_column(self, project_id):
        query = "SELECT 'a' AS string_1, 'b' AS string_2"
        result_frame = gbq.read_gbq(
            query,
            project_id=project_id,
            index_col="string_1",
            credentials=self.credentials,
            dialect="legacy",
        )
        correct_frame = DataFrame(
            {"string_1": ["a"], "string_2": ["b"]}
        ).set_index("string_1")
        assert result_frame.index.name == correct_frame.index.name

    def test_column_order(self, project_id):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ["string_3", "string_1", "string_2"]
        result_frame = gbq.read_gbq(
            query,
            project_id=project_id,
            col_order=col_order,
            credentials=self.credentials,
            dialect="legacy",
        )
        correct_frame = DataFrame(
            {"string_1": ["a"], "string_2": ["b"], "string_3": ["c"]}
        )[col_order]
        tm.assert_frame_equal(result_frame, correct_frame)

    def test_read_gbq_raises_invalid_column_order(self, project_id):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ["string_aaa", "string_1", "string_2"]

        # Column string_aaa does not exist. Should raise InvalidColumnOrder
        with pytest.raises(gbq.InvalidColumnOrder):
            gbq.read_gbq(
                query,
                project_id=project_id,
                col_order=col_order,
                credentials=self.credentials,
                dialect="legacy",
            )

    def test_column_order_plus_index(self, project_id):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ["string_3", "string_2"]
        result_frame = gbq.read_gbq(
            query,
            project_id=project_id,
            index_col="string_1",
            col_order=col_order,
            credentials=self.credentials,
            dialect="legacy",
        )
        correct_frame = DataFrame(
            {"string_1": ["a"], "string_2": ["b"], "string_3": ["c"]}
        )
        correct_frame.set_index("string_1", inplace=True)
        correct_frame = correct_frame[col_order]
        tm.assert_frame_equal(result_frame, correct_frame)

    def test_read_gbq_raises_invalid_index_column(self, project_id):
        query = "SELECT 'a' AS string_1, 'b' AS string_2, 'c' AS string_3"
        col_order = ["string_3", "string_2"]

        # Column string_bbb does not exist. Should raise InvalidIndexColumn
        with pytest.raises(gbq.InvalidIndexColumn):
            gbq.read_gbq(
                query,
                project_id=project_id,
                index_col="string_bbb",
                col_order=col_order,
                credentials=self.credentials,
                dialect="legacy",
            )

    def test_malformed_query(self, project_id):
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq(
                "SELCET * FORM [publicdata:samples.shakespeare]",
                project_id=project_id,
                credentials=self.credentials,
                dialect="legacy",
            )

    def test_bad_project_id(self):
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq(
                "SELCET * FROM [publicdata:samples.shakespeare]",
                project_id="not-my-project",
                credentials=self.credentials,
                dialect="legacy",
            )

    def test_bad_table_name(self, project_id):
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq(
                "SELECT * FROM [publicdata:samples.nope]",
                project_id=project_id,
                credentials=self.credentials,
                dialect="legacy",
            )

    def test_download_dataset_larger_than_200k_rows(self, project_id):
        test_size = 200005
        # Test for known BigQuery bug in datasets larger than 100k rows
        # http://stackoverflow.com/questions/19145587/bq-py-not-paging-results
        df = gbq.read_gbq(
            "SELECT id FROM [publicdata:samples.wikipedia] "
            "GROUP EACH BY id ORDER BY id ASC LIMIT {0}".format(test_size),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        assert len(df.drop_duplicates()) == test_size

    def test_zero_rows(self, project_id):
        # Bug fix for https://github.com/pandas-dev/pandas/issues/10273
        df = gbq.read_gbq(
            "SELECT title, id, is_bot, "
            "SEC_TO_TIMESTAMP(timestamp) ts "
            "FROM [publicdata:samples.wikipedia] "
            "WHERE timestamp=-9999999",
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        page_array = np.zeros(
            (0,),
            dtype=[
                ("title", object),
                ("id", np.dtype(int)),
                ("is_bot", np.dtype(bool)),
                ("ts", "M8[ns]"),
            ],
        )
        expected_result = DataFrame(
            page_array, columns=["title", "id", "is_bot", "ts"]
        )
        tm.assert_frame_equal(df, expected_result, check_index_type=False)

    def test_one_row_one_column(self, project_id):
        df = gbq.read_gbq(
            "SELECT 3 as v",
            project_id=project_id,
            credentials=self.credentials,
            dialect="standard",
        )
        expected_result = DataFrame(dict(v=[3]))
        tm.assert_frame_equal(df, expected_result)

    def test_legacy_sql(self, project_id):
        legacy_sql = "SELECT id FROM [publicdata.samples.wikipedia] LIMIT 10"

        # Test that a legacy sql statement fails when
        # setting dialect='standard'
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq(
                legacy_sql,
                project_id=project_id,
                dialect="standard",
                credentials=self.credentials,
            )

        # Test that a legacy sql statement succeeds when
        # setting dialect='legacy'
        df = gbq.read_gbq(
            legacy_sql,
            project_id=project_id,
            dialect="legacy",
            credentials=self.credentials,
        )
        assert len(df.drop_duplicates()) == 10

    def test_standard_sql(self, project_id):
        standard_sql = (
            "SELECT DISTINCT id FROM "
            "`publicdata.samples.wikipedia` LIMIT 10"
        )

        # Test that a standard sql statement fails when using
        # the legacy SQL dialect.
        with pytest.raises(gbq.GenericGBQException):
            gbq.read_gbq(
                standard_sql,
                project_id=project_id,
                credentials=self.credentials,
                dialect="legacy",
            )

        # Test that a standard sql statement succeeds when
        # setting dialect='standard'
        df = gbq.read_gbq(
            standard_sql,
            project_id=project_id,
            dialect="standard",
            credentials=self.credentials,
        )
        assert len(df.drop_duplicates()) == 10

    def test_query_with_parameters(self, project_id):
        sql_statement = "SELECT @param1 + @param2 AS valid_result"
        config = {
            "query": {
                "useLegacySql": False,
                "parameterMode": "named",
                "queryParameters": [
                    {
                        "name": "param1",
                        "parameterType": {"type": "INTEGER"},
                        "parameterValue": {"value": 1},
                    },
                    {
                        "name": "param2",
                        "parameterType": {"type": "INTEGER"},
                        "parameterValue": {"value": 2},
                    },
                ],
            }
        }
        # Test that a query that relies on parameters fails
        # when parameters are not supplied via configuration
        with pytest.raises(ValueError):
            gbq.read_gbq(
                sql_statement,
                project_id=project_id,
                credentials=self.credentials,
                dialect="legacy",
            )

        # Test that the query is successful because we have supplied
        # the correct query parameters via the 'config' option
        df = gbq.read_gbq(
            sql_statement,
            project_id=project_id,
            credentials=self.credentials,
            configuration=config,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"valid_result": [3]}))

    def test_query_inside_configuration(self, project_id):
        query_no_use = 'SELECT "PI_WRONG" AS valid_string'
        query = 'SELECT "PI" AS valid_string'
        config = {"query": {"query": query, "useQueryCache": False}}
        # Test that it can't pass query both
        # inside config and as parameter
        with pytest.raises(ValueError):
            gbq.read_gbq(
                query_no_use,
                project_id=project_id,
                credentials=self.credentials,
                configuration=config,
                dialect="legacy",
            )

        df = gbq.read_gbq(
            None,
            project_id=project_id,
            credentials=self.credentials,
            configuration=config,
            dialect="legacy",
        )
        tm.assert_frame_equal(df, DataFrame({"valid_string": ["PI"]}))

    def test_configuration_without_query(self, project_id):
        sql_statement = "SELECT 1"
        config = {
            "copy": {
                "sourceTable": {
                    "projectId": project_id,
                    "datasetId": "publicdata:samples",
                    "tableId": "wikipedia",
                },
                "destinationTable": {
                    "projectId": project_id,
                    "datasetId": "publicdata:samples",
                    "tableId": "wikipedia_copied",
                },
            }
        }
        # Test that only 'query' configurations are supported
        # nor 'copy','load','extract'
        with pytest.raises(ValueError):
            gbq.read_gbq(
                sql_statement,
                project_id=project_id,
                credentials=self.credentials,
                configuration=config,
                dialect="legacy",
            )

    def test_configuration_raises_value_error_with_multiple_config(
        self, project_id
    ):
        sql_statement = "SELECT 1"
        config = {
            "query": {"query": sql_statement, "useQueryCache": False},
            "load": {"query": sql_statement, "useQueryCache": False},
        }
        # Test that only ValueError is raised with multiple configurations
        with pytest.raises(ValueError):
            gbq.read_gbq(
                sql_statement,
                project_id=project_id,
                credentials=self.credentials,
                configuration=config,
                dialect="legacy",
            )

    def test_timeout_configuration(self, project_id):
        sql_statement = "SELECT 1"
        config = {"query": {"timeoutMs": 1}}
        # Test that QueryTimeout error raises
        with pytest.raises(gbq.QueryTimeout):
            gbq.read_gbq(
                sql_statement,
                project_id=project_id,
                credentials=self.credentials,
                configuration=config,
                dialect="legacy",
            )

    def test_query_response_bytes(self):
        assert self.gbq_connector.sizeof_fmt(999) == "999.0 B"
        assert self.gbq_connector.sizeof_fmt(1024) == "1.0 KB"
        assert self.gbq_connector.sizeof_fmt(1099) == "1.1 KB"
        assert self.gbq_connector.sizeof_fmt(1044480) == "1020.0 KB"
        assert self.gbq_connector.sizeof_fmt(1048576) == "1.0 MB"
        assert self.gbq_connector.sizeof_fmt(1048576000) == "1000.0 MB"
        assert self.gbq_connector.sizeof_fmt(1073741824) == "1.0 GB"
        assert self.gbq_connector.sizeof_fmt(1.099512e12) == "1.0 TB"
        assert self.gbq_connector.sizeof_fmt(1.125900e15) == "1.0 PB"
        assert self.gbq_connector.sizeof_fmt(1.152922e18) == "1.0 EB"
        assert self.gbq_connector.sizeof_fmt(1.180592e21) == "1.0 ZB"
        assert self.gbq_connector.sizeof_fmt(1.208926e24) == "1.0 YB"
        assert self.gbq_connector.sizeof_fmt(1.208926e28) == "10000.0 YB"

    def test_struct(self, project_id):
        query = """SELECT 1 int_field,
                   STRUCT("a" as letter, 1 as num) struct_field"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="standard",
        )
        expected = DataFrame(
            [[1, {"letter": "a", "num": 1}]],
            columns=["int_field", "struct_field"],
        )
        tm.assert_frame_equal(df, expected)

    def test_array(self, project_id):
        query = """select ["a","x","b","y","c","z"] as letters"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="standard",
        )
        tm.assert_frame_equal(
            df,
            DataFrame([[["a", "x", "b", "y", "c", "z"]]], columns=["letters"]),
        )

    def test_array_length_zero(self, project_id):
        query = """WITH t as (
                   SELECT "a" letter, [""] as array_field
                   UNION ALL
                   SELECT "b" letter, [] as array_field)

                   select letter, array_field, array_length(array_field) len
                   from t
                   order by letter ASC"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="standard",
        )
        expected = DataFrame(
            [["a", [""], 1], ["b", [], 0]],
            columns=["letter", "array_field", "len"],
        )
        tm.assert_frame_equal(df, expected)

    def test_array_agg(self, project_id):
        query = """WITH t as (
                SELECT "a" letter, 1 num
                UNION ALL
                SELECT "b" letter, 2 num
                UNION ALL
                SELECT "a" letter, 3 num)

                select letter, array_agg(num order by num ASC) numbers
                from t
                group by letter
                order by letter ASC"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            credentials=self.credentials,
            dialect="standard",
        )
        tm.assert_frame_equal(
            df,
            DataFrame(
                [["a", [1, 3]], ["b", [2]]], columns=["letter", "numbers"]
            ),
        )

    def test_array_of_floats(self, private_key_path, project_id):
        query = """select [1.1, 2.2, 3.3] as a, 4 as b"""
        df = gbq.read_gbq(
            query,
            project_id=project_id,
            private_key=private_key_path,
            dialect="standard",
        )
        tm.assert_frame_equal(
            df, DataFrame([[[1.1, 2.2, 3.3], 4]], columns=["a", "b"])
        )

    def test_tokyo(self, tokyo_dataset, tokyo_table, private_key_path):
        df = gbq.read_gbq(
            "SELECT MAX(year) AS max_year FROM {}.{}".format(
                tokyo_dataset, tokyo_table
            ),
            dialect="standard",
            location="asia-northeast1",
            private_key=private_key_path,
        )
        print(df)
        assert df["max_year"][0] >= 2000


class TestToGBQIntegration(object):
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, project, credentials, random_dataset_id):
        # - PER-TEST FIXTURES -
        # put here any instruction you want to be run *BEFORE* *EVERY* test is
        # executed.
        self.table = gbq._Table(
            project, random_dataset_id, credentials=credentials
        )
        self.destination_table = "{}.{}".format(random_dataset_id, TABLE_ID)
        self.credentials = credentials

    def test_upload_data(self, project_id):
        test_id = "1"
        test_size = 20001
        df = make_mixed_dataframe_v2(test_size)

        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id,
            chunksize=10000,
            credentials=self.credentials,
        )

        result = gbq.read_gbq(
            "SELECT COUNT(*) AS num_rows FROM {0}".format(
                self.destination_table + test_id
            ),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        assert result["num_rows"][0] == test_size

    def test_upload_data_if_table_exists_fail(self, project_id):
        test_id = "2"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        self.table.create(TABLE_ID + test_id, gbq._generate_bq_schema(df))

        # Test the default value of if_exists is 'fail'
        with pytest.raises(gbq.TableCreationError):
            gbq.to_gbq(
                df,
                self.destination_table + test_id,
                project_id,
                credentials=self.credentials,
            )

        # Test the if_exists parameter with value 'fail'
        with pytest.raises(gbq.TableCreationError):
            gbq.to_gbq(
                df,
                self.destination_table + test_id,
                project_id,
                if_exists="fail",
                credentials=self.credentials,
            )

    def test_upload_data_if_table_exists_append(self, project_id):
        test_id = "3"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        df_different_schema = tm.makeMixedDataFrame()

        # Initialize table with sample data
        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id,
            chunksize=10000,
            credentials=self.credentials,
        )

        # Test the if_exists parameter with value 'append'
        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id,
            if_exists="append",
            credentials=self.credentials,
        )

        result = gbq.read_gbq(
            "SELECT COUNT(*) AS num_rows FROM {0}".format(
                self.destination_table + test_id
            ),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        assert result["num_rows"][0] == test_size * 2

        # Try inserting with a different schema, confirm failure
        with pytest.raises(gbq.InvalidSchema):
            gbq.to_gbq(
                df_different_schema,
                self.destination_table + test_id,
                project_id,
                if_exists="append",
                credentials=self.credentials,
            )

    def test_upload_subset_columns_if_table_exists_append(self, project_id):
        # Issue 24: Upload is succesful if dataframe has columns
        # which are a subset of the current schema
        test_id = "16"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        df_subset_cols = df.iloc[:, :2]

        # Initialize table with sample data
        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id,
            chunksize=10000,
            credentials=self.credentials,
        )

        # Test the if_exists parameter with value 'append'
        gbq.to_gbq(
            df_subset_cols,
            self.destination_table + test_id,
            project_id,
            if_exists="append",
            credentials=self.credentials,
        )

        result = gbq.read_gbq(
            "SELECT COUNT(*) AS num_rows FROM {0}".format(
                self.destination_table + test_id
            ),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        assert result["num_rows"][0] == test_size * 2

    def test_upload_data_if_table_exists_replace(self, project_id):
        test_id = "4"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        df_different_schema = tm.makeMixedDataFrame()

        # Initialize table with sample data
        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id,
            chunksize=10000,
            credentials=self.credentials,
        )

        # Test the if_exists parameter with the value 'replace'.
        gbq.to_gbq(
            df_different_schema,
            self.destination_table + test_id,
            project_id,
            if_exists="replace",
            credentials=self.credentials,
        )

        result = gbq.read_gbq(
            "SELECT COUNT(*) AS num_rows FROM {0}".format(
                self.destination_table + test_id
            ),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )
        assert result["num_rows"][0] == 5

    def test_upload_data_if_table_exists_raises_value_error(self, project_id):
        test_id = "4"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)

        # Test invalid value for if_exists parameter raises value error
        with pytest.raises(ValueError):
            gbq.to_gbq(
                df,
                self.destination_table + test_id,
                project_id,
                if_exists="xxxxx",
                credentials=self.credentials,
            )

    def test_google_upload_errors_should_raise_exception(self, project_id):
        raise pytest.skip("buggy test")

        test_id = "5"
        test_timestamp = datetime.now(pytz.timezone("US/Arizona"))
        bad_df = DataFrame(
            {
                "bools": [False, False],
                "flts": [0.0, 1.0],
                "ints": [0, "1"],
                "strs": ["a", 1],
                "times": [test_timestamp, test_timestamp],
            },
            index=range(2),
        )

        with pytest.raises(gbq.StreamingInsertError):
            gbq.to_gbq(
                bad_df,
                self.destination_table + test_id,
                project_id,
                credentials=self.credentials,
            )

    def test_upload_chinese_unicode_data(self, project_id):
        test_id = "2"
        test_size = 6
        df = DataFrame(
            np.random.randn(6, 4), index=range(6), columns=list("ABCD")
        )
        df["s"] = u"信用卡"

        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id,
            credentials=self.credentials,
            chunksize=10000,
        )

        result_df = gbq.read_gbq(
            "SELECT * FROM {0}".format(self.destination_table + test_id),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )

        assert len(result_df) == test_size

        if sys.version_info.major < 3:
            pytest.skip(msg="Unicode comparison in Py2 not working")

        result = result_df["s"].sort_values()
        expected = df["s"].sort_values()

        tm.assert_numpy_array_equal(expected.values, result.values)

    def test_upload_other_unicode_data(self, project_id):
        test_id = "3"
        test_size = 3
        df = DataFrame(
            {
                "s": ["Skywalker™", "lego", "hülle"],
                "i": [200, 300, 400],
                "d": [
                    "2017-12-13 17:40:39",
                    "2017-12-13 17:40:39",
                    "2017-12-13 17:40:39",
                ],
            }
        )

        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id=project_id,
            credentials=self.credentials,
            chunksize=10000,
        )

        result_df = gbq.read_gbq(
            "SELECT * FROM {0}".format(self.destination_table + test_id),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )

        assert len(result_df) == test_size

        if sys.version_info.major < 3:
            pytest.skip(msg="Unicode comparison in Py2 not working")

        result = result_df["s"].sort_values()
        expected = df["s"].sort_values()

        tm.assert_numpy_array_equal(expected.values, result.values)

    def test_upload_mixed_float_and_int(self, project_id):
        """Test that we can upload a dataframe containing an int64 and float64 column.
        See: https://github.com/pydata/pandas-gbq/issues/116
        """
        test_id = "mixed_float_and_int"
        test_size = 2
        df = DataFrame(
            [[1, 1.1], [2, 2.2]],
            index=["row 1", "row 2"],
            columns=["intColumn", "floatColumn"],
        )

        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id=project_id,
            credentials=self.credentials,
        )

        result_df = gbq.read_gbq(
            "SELECT * FROM {0}".format(self.destination_table + test_id),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )

        assert len(result_df) == test_size

    def test_upload_data_with_newlines(self, project_id):
        test_id = "data_with_newlines"
        test_size = 2
        df = DataFrame({"s": ["abcd", "ef\ngh"]})

        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id=project_id,
            credentials=self.credentials,
        )

        result_df = gbq.read_gbq(
            "SELECT * FROM {0}".format(self.destination_table + test_id),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )

        assert len(result_df) == test_size

        if sys.version_info.major < 3:
            pytest.skip(msg="Unicode comparison in Py2 not working")

        result = result_df["s"].sort_values()
        expected = df["s"].sort_values()

        tm.assert_numpy_array_equal(expected.values, result.values)

    def test_upload_data_flexible_column_order(self, project_id):
        test_id = "13"
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)

        # Initialize table with sample data
        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id,
            chunksize=10000,
            credentials=self.credentials,
        )

        df_columns_reversed = df[df.columns[::-1]]

        gbq.to_gbq(
            df_columns_reversed,
            self.destination_table + test_id,
            project_id,
            if_exists="append",
            credentials=self.credentials,
        )

    def test_upload_data_with_valid_user_schema(self, project_id):
        # Issue #46; tests test scenarios with user-provided
        # schemas
        df = tm.makeMixedDataFrame()
        test_id = "18"
        test_schema = [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
        destination_table = self.destination_table + test_id
        gbq.to_gbq(
            df,
            destination_table,
            project_id,
            credentials=self.credentials,
            table_schema=test_schema,
        )
        dataset, table = destination_table.split(".")
        assert self.table.verify_schema(
            dataset, table, dict(fields=test_schema)
        )

    def test_upload_data_with_invalid_user_schema_raises_error(
        self, project_id
    ):
        df = tm.makeMixedDataFrame()
        test_id = "19"
        test_schema = [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "FLOAT"},
            {"name": "D", "type": "FLOAT"},
        ]
        destination_table = self.destination_table + test_id
        with pytest.raises(gbq.GenericGBQException):
            gbq.to_gbq(
                df,
                destination_table,
                project_id,
                credentials=self.credentials,
                table_schema=test_schema,
            )

    def test_upload_data_with_missing_schema_fields_raises_error(
        self, project_id
    ):
        df = tm.makeMixedDataFrame()
        test_id = "20"
        test_schema = [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "FLOAT"},
        ]
        destination_table = self.destination_table + test_id
        with pytest.raises(gbq.GenericGBQException):
            gbq.to_gbq(
                df,
                destination_table,
                project_id,
                credentials=self.credentials,
                table_schema=test_schema,
            )

    def test_upload_data_with_timestamp(self, project_id):
        test_id = "21"
        test_size = 6
        df = DataFrame(
            np.random.randn(test_size, 4),
            index=range(test_size),
            columns=list("ABCD"),
        )
        df["times"] = np.datetime64("2018-03-13T05:40:45.348318Z")

        gbq.to_gbq(
            df,
            self.destination_table + test_id,
            project_id=project_id,
            credentials=self.credentials,
        )

        result_df = gbq.read_gbq(
            "SELECT * FROM {0}".format(self.destination_table + test_id),
            project_id=project_id,
            credentials=self.credentials,
            dialect="legacy",
        )

        assert len(result_df) == test_size

        expected = df["times"].sort_values()
        result = result_df["times"].sort_values()
        tm.assert_numpy_array_equal(expected.values, result.values)

    def test_upload_data_with_different_df_and_user_schema(self, project_id):
        df = tm.makeMixedDataFrame()
        df["A"] = df["A"].astype(str)
        df["B"] = df["B"].astype(str)
        test_id = "22"
        test_schema = [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
        destination_table = self.destination_table + test_id
        gbq.to_gbq(
            df,
            destination_table,
            project_id,
            credentials=self.credentials,
            table_schema=test_schema,
        )
        dataset, table = destination_table.split(".")
        assert self.table.verify_schema(
            dataset, table, dict(fields=test_schema)
        )

    def test_upload_data_tokyo(
        self, project_id, tokyo_dataset, bigquery_client
    ):
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        tokyo_destination = "{}.to_gbq_test".format(tokyo_dataset)

        # Initialize table with sample data
        gbq.to_gbq(
            df,
            tokyo_destination,
            project_id,
            credentials=self.credentials,
            location="asia-northeast1",
        )

        table = bigquery_client.get_table(
            bigquery_client.dataset(tokyo_dataset).table("to_gbq_test")
        )
        assert table.num_rows > 0

    def test_upload_data_tokyo_non_existing_dataset(
        self, project_id, random_dataset_id, bigquery_client
    ):
        test_size = 10
        df = make_mixed_dataframe_v2(test_size)
        non_existing_tokyo_dataset = random_dataset_id
        non_existing_tokyo_destination = "{}.to_gbq_test".format(
            non_existing_tokyo_dataset
        )

        # Initialize table with sample data
        gbq.to_gbq(
            df,
            non_existing_tokyo_destination,
            project_id,
            credentials=self.credentials,
            location="asia-northeast1",
        )

        table = bigquery_client.get_table(
            bigquery_client.dataset(non_existing_tokyo_dataset).table(
                "to_gbq_test"
            )
        )
        assert table.num_rows > 0


# _Dataset tests


def test_create_dataset(bigquery_client, gbq_dataset, random_dataset_id):
    gbq_dataset.create(random_dataset_id)
    dataset_reference = bigquery_client.dataset(random_dataset_id)
    assert bigquery_client.get_dataset(dataset_reference) is not None


def test_create_dataset_already_exists(gbq_dataset, random_dataset_id):
    gbq_dataset.create(random_dataset_id)
    with pytest.raises(gbq.DatasetCreationError):
        gbq_dataset.create(random_dataset_id)


def test_dataset_exists(gbq_dataset, random_dataset_id):
    gbq_dataset.create(random_dataset_id)
    assert gbq_dataset.exists(random_dataset_id)


def test_dataset_does_not_exist(gbq_dataset, random_dataset_id):
    assert not gbq_dataset.exists(random_dataset_id)


# _Table tests


def test_create_table(gbq_table):
    schema = gbq._generate_bq_schema(tm.makeMixedDataFrame())
    gbq_table.create("test_create_table", schema)
    assert gbq_table.exists("test_create_table")


def test_create_table_already_exists(gbq_table):
    schema = gbq._generate_bq_schema(tm.makeMixedDataFrame())
    gbq_table.create("test_create_table_exists", schema)
    with pytest.raises(gbq.TableCreationError):
        gbq_table.create("test_create_table_exists", schema)


def test_table_does_not_exist(gbq_table):
    assert not gbq_table.exists("test_table_does_not_exist")


def test_delete_table(gbq_table):
    test_schema = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }
    gbq_table.create("test_delete_table", test_schema)
    gbq_table.delete("test_delete_table")
    assert not gbq_table.exists("test_delete_table")


def test_delete_table_not_found(gbq_table):
    with pytest.raises(gbq.NotFoundException):
        gbq_table.delete("test_delete_table_not_found")


def test_create_table_data_dataset_does_not_exist(
    project, credentials, gbq_dataset, random_dataset_id
):
    table_id = "test_create_table_data_dataset_does_not_exist"
    table_with_new_dataset = gbq._Table(
        project, random_dataset_id, credentials=credentials
    )
    df = make_mixed_dataframe_v2(10)
    table_with_new_dataset.create(table_id, gbq._generate_bq_schema(df))
    assert gbq_dataset.exists(random_dataset_id)
    assert table_with_new_dataset.exists(table_id)


def test_verify_schema_allows_flexible_column_order(gbq_table, gbq_connector):
    table_id = "test_verify_schema_allows_flexible_column_order"
    test_schema_1 = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }
    test_schema_2 = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "B", "type": "FLOAT"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }

    gbq_table.create(table_id, test_schema_1)
    assert gbq_connector.verify_schema(
        gbq_table.dataset_id, table_id, test_schema_2
    )


def test_verify_schema_fails_different_data_type(gbq_table, gbq_connector):
    table_id = "test_verify_schema_fails_different_data_type"
    test_schema_1 = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }
    test_schema_2 = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "STRING"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }

    gbq_table.create(table_id, test_schema_1)
    assert not gbq_connector.verify_schema(
        gbq_table.dataset_id, table_id, test_schema_2
    )


def test_verify_schema_fails_different_structure(gbq_table, gbq_connector):
    table_id = "test_verify_schema_fails_different_structure"
    test_schema_1 = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }
    test_schema_2 = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B2", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }

    gbq_table.create(table_id, test_schema_1)
    assert not gbq_connector.verify_schema(
        gbq_table.dataset_id, table_id, test_schema_2
    )


def test_verify_schema_ignores_field_mode(gbq_table, gbq_connector):
    table_id = "test_verify_schema_ignores_field_mode"
    test_schema_1 = {
        "fields": [
            {"name": "A", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "B", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "C", "type": "STRING", "mode": "NULLABLE"},
            {"name": "D", "type": "TIMESTAMP", "mode": "REQUIRED"},
        ]
    }
    test_schema_2 = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
            {"name": "D", "type": "TIMESTAMP"},
        ]
    }

    gbq_table.create(table_id, test_schema_1)
    assert gbq_connector.verify_schema(
        gbq_table.dataset_id, table_id, test_schema_2
    )


def test_retrieve_schema(gbq_table, gbq_connector):
    # Issue #24 schema function returns the schema in biquery
    table_id = "test_retrieve_schema"
    test_schema = {
        "fields": [
            {
                "name": "A",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": None,
            },
            {
                "name": "B",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": None,
            },
            {
                "name": "C",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": None,
            },
            {
                "name": "D",
                "type": "TIMESTAMP",
                "mode": "NULLABLE",
                "description": None,
            },
        ]
    }

    gbq_table.create(table_id, test_schema)
    actual = gbq_connector._clean_schema_fields(
        gbq_connector.schema(gbq_table.dataset_id, table_id)
    )
    expected = [
        {"name": "A", "type": "FLOAT"},
        {"name": "B", "type": "FLOAT"},
        {"name": "C", "type": "STRING"},
        {"name": "D", "type": "TIMESTAMP"},
    ]
    assert expected == actual, "Expected schema used to create table"


def test_schema_is_subset_passes_if_subset(gbq_table, gbq_connector):
    # Issue #24 schema_is_subset indicates whether the schema of the
    # dataframe is a subset of the schema of the bigquery table
    table_id = "test_schema_is_subset_passes_if_subset"
    table_schema = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
        ]
    }
    tested_schema = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
        ]
    }

    gbq_table.create(table_id, table_schema)
    assert gbq_connector.schema_is_subset(
        gbq_table.dataset_id, table_id, tested_schema
    )


def test_schema_is_subset_fails_if_not_subset(gbq_table, gbq_connector):
    # For pull request #24
    table_id = "test_schema_is_subset_fails_if_not_subset"
    table_schema = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "B", "type": "FLOAT"},
            {"name": "C", "type": "STRING"},
        ]
    }
    tested_schema = {
        "fields": [
            {"name": "A", "type": "FLOAT"},
            {"name": "C", "type": "FLOAT"},
        ]
    }

    gbq_table.create(table_id, table_schema)
    assert not gbq_connector.schema_is_subset(
        gbq_table.dataset_id, table_id, tested_schema
    )
