# Copyright 2021 Google LLC
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

"""System tests for Arrow connector."""

from typing import Optional

import pyarrow
import pytest

from google.cloud import bigquery
from google.cloud.bigquery import enums


@pytest.mark.parametrize(
    ("max_results", "scalars_table_name"),
    (
        (None, "scalars_table"),  # Use BQ Storage API.
        (10, "scalars_table"),  # Use REST API.
        (None, "scalars_extreme_table"),  # Use BQ Storage API.
        (10, "scalars_extreme_table"),  # Use REST API.
    ),
)
def test_list_rows_nullable_scalars_dtypes(
    bigquery_client: bigquery.Client,
    scalars_table: str,
    scalars_extreme_table: str,
    max_results: Optional[int],
    scalars_table_name: str,
):
    table_id = scalars_table
    if scalars_table_name == "scalars_extreme_table":
        table_id = scalars_extreme_table

    # TODO(GH#836): Avoid INTERVAL columns until they are supported by the
    # BigQuery Storage API and pyarrow.
    schema = [
        bigquery.SchemaField("bool_col", enums.SqlTypeNames.BOOLEAN),
        bigquery.SchemaField("bignumeric_col", enums.SqlTypeNames.BIGNUMERIC),
        bigquery.SchemaField("bytes_col", enums.SqlTypeNames.BYTES),
        bigquery.SchemaField("date_col", enums.SqlTypeNames.DATE),
        bigquery.SchemaField("datetime_col", enums.SqlTypeNames.DATETIME),
        bigquery.SchemaField("float64_col", enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("geography_col", enums.SqlTypeNames.GEOGRAPHY),
        bigquery.SchemaField("int64_col", enums.SqlTypeNames.INT64),
        bigquery.SchemaField("numeric_col", enums.SqlTypeNames.NUMERIC),
        bigquery.SchemaField("string_col", enums.SqlTypeNames.STRING),
        bigquery.SchemaField("time_col", enums.SqlTypeNames.TIME),
        bigquery.SchemaField("timestamp_col", enums.SqlTypeNames.TIMESTAMP),
    ]

    arrow_table = bigquery_client.list_rows(
        table_id,
        max_results=max_results,
        selected_fields=schema,
    ).to_arrow()

    schema = arrow_table.schema
    bignumeric_type = schema.field("bignumeric_col").type
    # 77th digit is partial.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#decimal_types
    assert bignumeric_type.precision in {76, 77}
    assert bignumeric_type.scale == 38

    bool_type = schema.field("bool_col").type
    assert bool_type.equals(pyarrow.bool_())

    bytes_type = schema.field("bytes_col").type
    assert bytes_type.equals(pyarrow.binary())

    date_type = schema.field("date_col").type
    assert date_type.equals(pyarrow.date32())

    datetime_type = schema.field("datetime_col").type
    assert datetime_type.unit == "us"
    assert datetime_type.tz is None

    float64_type = schema.field("float64_col").type
    assert float64_type.equals(pyarrow.float64())

    geography_type = schema.field("geography_col").type
    assert geography_type.equals(pyarrow.string())

    int64_type = schema.field("int64_col").type
    assert int64_type.equals(pyarrow.int64())

    numeric_type = schema.field("numeric_col").type
    assert numeric_type.precision == 38
    assert numeric_type.scale == 9

    string_type = schema.field("string_col").type
    assert string_type.equals(pyarrow.string())

    time_type = schema.field("time_col").type
    assert time_type.equals(pyarrow.time64("us"))

    timestamp_type = schema.field("timestamp_col").type
    assert timestamp_type.unit == "us"
    assert timestamp_type.tz is not None


@pytest.mark.parametrize("do_insert", [True, False])
def test_arrow_extension_types_same_for_storage_and_REST_APIs_894(
    dataset_client, test_table_name, do_insert
):
    types = dict(
        astring=("STRING", "'x'"),
        astring9=("STRING(9)", "'x'"),
        abytes=("BYTES", "b'x'"),
        abytes9=("BYTES(9)", "b'x'"),
        anumeric=("NUMERIC", "42"),
        anumeric9=("NUMERIC(9)", "42"),
        anumeric92=("NUMERIC(9,2)", "42"),
        abignumeric=("BIGNUMERIC", "42e30"),
        abignumeric49=("BIGNUMERIC(37)", "42e30"),
        abignumeric492=("BIGNUMERIC(37,2)", "42e30"),
        abool=("BOOL", "true"),
        adate=("DATE", "'2021-09-06'"),
        adatetime=("DATETIME", "'2021-09-06T09:57:26'"),
        ageography=("GEOGRAPHY", "ST_GEOGFROMTEXT('point(0 0)')"),
        # Can't get arrow data for interval :(
        # ainterval=('INTERVAL', "make_interval(1, 2, 3, 4, 5, 6)"),
        aint64=("INT64", "42"),
        afloat64=("FLOAT64", "42.0"),
        astruct=("STRUCT<v int64>", "struct(42)"),
        atime=("TIME", "'1:2:3'"),
        atimestamp=("TIMESTAMP", "'2021-09-06T09:57:26'"),
    )
    columns = ", ".join(f"{k} {t[0]}" for k, t in types.items())
    dataset_client.query(f"create table {test_table_name} ({columns})").result()
    if do_insert:
        names = list(types)
        values = ", ".join(types[name][1] for name in names)
        names = ", ".join(names)
        dataset_client.query(
            f"insert into {test_table_name} ({names}) values ({values})"
        ).result()
    at = dataset_client.query(f"select * from {test_table_name}").result().to_arrow()
    storage_api_metadata = {
        at.field(i).name: at.field(i).metadata for i in range(at.num_columns)
    }
    at = (
        dataset_client.query(f"select * from {test_table_name}")
        .result()
        .to_arrow(create_bqstorage_client=False)
    )
    rest_api_metadata = {
        at.field(i).name: at.field(i).metadata for i in range(at.num_columns)
    }

    assert rest_api_metadata == storage_api_metadata
    assert rest_api_metadata["adatetime"] == {
        b"ARROW:extension:name": b"google:sqlType:datetime"
    }
    assert rest_api_metadata["ageography"] == {
        b"ARROW:extension:name": b"google:sqlType:geography",
        b"ARROW:extension:metadata": b'{"encoding": "WKT"}',
    }


def test_list_rows_range_csv(
    bigquery_client: bigquery.Client,
    scalars_table_csv: str,
):
    table_id = scalars_table_csv

    schema = [
        bigquery.SchemaField(
            "range_date", enums.SqlTypeNames.RANGE, range_element_type="DATE"
        ),
    ]

    arrow_table = bigquery_client.list_rows(
        table_id,
        selected_fields=schema,
    ).to_arrow()

    schema = arrow_table.schema

    expected_type = pyarrow.struct(
        [("start", pyarrow.date32()), ("end", pyarrow.date32())]
    )

    range_type = schema.field("range_date").type
    assert range_type == expected_type


def test_to_arrow_query_with_empty_results(bigquery_client):
    """
    JSON regression test for https://github.com/googleapis/python-bigquery/issues/1580.
    """
    job = bigquery_client.query(
        """
        select
        123 as int_col,
        '' as string_col,
        to_json('{}') as json_col,
        struct(to_json('[]') as json_field, -1 as int_field) as struct_col,
        [to_json('null')] as json_array_col,
        from unnest([])
        """
    )
    table = job.to_arrow()
    assert list(table.column_names) == [
        "int_col",
        "string_col",
        "json_col",
        "struct_col",
        "json_array_col",
    ]
    assert table.shape == (0, 5)
    struct_type = table.field("struct_col").type
    assert struct_type.get_field_index("json_field") == 0
    assert struct_type.get_field_index("int_field") == 1


def test_query_and_wait_arrow_format_with_compression_codec_to_arrow_iterable(
    bigquery_client,
):
    iterator = bigquery_client.query_and_wait(
        "SELECT 1 AS num, 'hello' AS msg",
        query_results_format="ARROW",
        compression_codec=enums.QueryResultsCompressionCodec.LZ4_FRAME,
    )
    batches = list(iterator.to_arrow_iterable())
    assert len(batches) >= 1
    table = pyarrow.Table.from_batches(batches)
    assert table.column_names == ["num", "msg"]
    assert table.to_pydict() == {"num": [1], "msg": ["hello"]}


def test_query_and_wait_arrow_format_to_arrow(bigquery_client):
    iterator = bigquery_client.query_and_wait(
        "SELECT 42 AS val",
        query_results_format=enums.QueryResultsFormat.ARROW,
    )
    table = iterator.to_arrow()
    assert isinstance(table, pyarrow.Table)
    assert table.column_names == ["val"]
    assert table.to_pydict() == {"val": [42]}


def test_query_and_wait_arrow_format_to_dataframe(bigquery_client):
    pandas = pytest.importorskip("pandas")
    iterator = bigquery_client.query_and_wait(
        "SELECT 100 AS num, 'world' AS text",
        query_results_format=enums.QueryResultsFormat.ARROW,
    )
    df = iterator.to_dataframe()
    assert isinstance(df, pandas.DataFrame)
    assert df.columns.tolist() == ["num", "text"]
    assert df.to_dict(orient="records") == [{"num": 100, "text": "world"}]


def test_query_and_wait_arrow_format_to_dataframe_iterable(bigquery_client):
    pandas = pytest.importorskip("pandas")
    iterator = bigquery_client.query_and_wait(
        "SELECT 200 AS num, 'python' AS text",
        query_results_format=enums.QueryResultsFormat.ARROW,
    )
    dfs = list(iterator.to_dataframe_iterable())
    assert len(dfs) >= 1
    concat_df = pandas.concat(dfs, ignore_index=True)
    assert concat_df.columns.tolist() == ["num", "text"]
    assert concat_df.to_dict(orient="records") == [{"num": 200, "text": "python"}]


def test_query_rest_arrow_format_config(bigquery_client):
    """System test for setting QueryResultsFormat.ARROW on QueryJobConfig via query_and_wait()."""
    job_config = bigquery.QueryJobConfig()
    job_config.query_results_format = enums.QueryResultsFormat.ARROW

    assert job_config.query_results_format == enums.QueryResultsFormat.ARROW

    results = bigquery_client.query_and_wait(
        "SELECT 42 AS val, 'hello' AS msg", job_config=job_config
    )

    assert results.total_rows == 1
    df = results.to_dataframe()
    assert df.to_dict(orient="records") == [{"val": 42, "msg": "hello"}]


def test_query_arrow_multi_page(bigquery_client):
    """System test for multi-page query results (Page 1 REST + Page 2+ BQStorage gRPC)."""
    # Generate 5,000 rows and cap initial REST jobs.query page at 1,000 rows
    # so Page 1 (1,000 rows) comes via REST and Page 2+ (4,000 rows) streams via gRPC.
    query_str = "SELECT num FROM UNNEST(GENERATE_ARRAY(1, 5000)) AS num"
    results = bigquery_client.query_and_wait(
        query_str,
        query_results_format=enums.QueryResultsFormat.ARROW,
        page_size=1000,
    )

    batches = list(results.to_arrow_iterable())
    assert len(batches) >= 2
    assert batches[0].num_rows == 1000
    table = pyarrow.Table.from_batches(batches)
    assert isinstance(table, pyarrow.Table)
    assert len(table) == 5000
    assert table.column_names == ["num"]


@pytest.mark.parametrize("force_job_insert", [False, True])
def test_query_arrow_zero_rows(bigquery_client, force_job_insert):
    """System test for 0-row query results preserving schema across Arrow/DataFrame methods."""
    job_config = (
        bigquery.QueryJobConfig(priority=bigquery.QueryPriority.INTERACTIVE)
        if force_job_insert
        else None
    )
    results = bigquery_client.query_and_wait(
        "SELECT 1 AS num, 'abc' AS label FROM UNNEST(GENERATE_ARRAY(1, 10)) AS x WHERE x > 100",
        job_config=job_config,
        query_results_format=enums.QueryResultsFormat.ARROW,
    )
    assert results.total_rows == 0
    assert list(results.to_arrow_iterable()) == []

    table = results.to_arrow()
    assert len(table) == 0
    assert table.column_names == ["num", "label"]
    assert table.schema.field("num").type == pyarrow.int64()
    assert table.schema.field("label").type == pyarrow.string()

    df = results.to_dataframe()
    assert df.shape == (0, 2)
    assert list(df.columns) == ["num", "label"]


@pytest.mark.parametrize(
    ("max_results", "page_size", "force_job_insert", "expected_rows"),
    [
        (100, None, False, 100),  # 1. Fits on Page 1 (no page_size)
        (1200, 500, False, 1200),  # 2. Spans Page 1 (REST) + Page 2+ (gRPC)
        (100, 500, False, 100),  # 3. max_results < page_size
        (10000, None, False, 5000),  # 4. max_results > total_rows (single-page)
        (10000, 500, False, 5000),  # 5. max_results > total_rows (multi-page)
        (0, None, False, 0),  # 6. max_results = 0 (schema only / 0 rows)
        (1200, 500, True, 1200),  # 7. jobs.insert fallback path + max_results
    ],
)
def test_query_arrow_max_results(
    bigquery_client, max_results, page_size, force_job_insert, expected_rows
):
    """System test verifying max_results across Page 1, Page 2+, edge bounds, and jobs.insert."""
    query_str = "SELECT num FROM UNNEST(GENERATE_ARRAY(1, 5000)) AS num ORDER BY num"
    job_config = (
        bigquery.QueryJobConfig(priority=bigquery.QueryPriority.INTERACTIVE)
        if force_job_insert
        else None
    )
    results = bigquery_client.query_and_wait(
        query_str,
        job_config=job_config,
        query_results_format=enums.QueryResultsFormat.ARROW,
        max_results=max_results,
        page_size=page_size,
    )

    if expected_rows == 0:
        table = results.to_arrow()
    else:
        batches = list(results.to_arrow_iterable())
        table = pyarrow.Table.from_batches(batches)

    assert len(table) == expected_rows
    assert table.column_names == ["num"]
    assert table.column("num").to_pylist() == list(range(1, expected_rows + 1))


@pytest.mark.parametrize(
    ("codec", "force_job_insert"),
    [
        (enums.QueryResultsCompressionCodec.LZ4_FRAME, False),
        (enums.QueryResultsCompressionCodec.ZSTD, False),
        (enums.QueryResultsCompressionCodec.LZ4_FRAME, True),
    ],
)
def test_query_arrow_multi_page_compression_codec(
    bigquery_client, codec, force_job_insert
):
    """System test verifying ReadRows compresses wire bytes with compression_codec on Page 2+ and jobs.insert."""
    from unittest import mock
    from google.cloud.bigquery_storage_v1.services.big_query_read import (
        BigQueryReadClient as GapicBigQueryReadClient,
    )

    query_str = "SELECT REPEAT('abc123_', 50) AS payload FROM UNNEST(GENERATE_ARRAY(1, 5000)) AS num"
    job_config = (
        bigquery.QueryJobConfig(
            priority=bigquery.QueryPriority.INTERACTIVE,
            use_query_cache=False,
        )
        if force_job_insert
        else bigquery.QueryJobConfig(use_query_cache=False)
    )

    def _measure_stream_wire_bytes(results):
        wire_bytes = 0
        orig_gapic_read_rows = GapicBigQueryReadClient.read_rows

        def spy_gapic_read_rows(self, *args, **kwargs):
            stream = orig_gapic_read_rows(self, *args, **kwargs)
            for resp in stream:
                if (
                    resp.arrow_record_batch
                    and resp.arrow_record_batch.serialized_record_batch
                ):
                    nonlocal wire_bytes
                    wire_bytes += len(resp.arrow_record_batch.serialized_record_batch)
                yield resp

        with mock.patch.object(
            GapicBigQueryReadClient, "read_rows", spy_gapic_read_rows
        ):
            table = results.to_arrow()
        return table, wire_bytes

    uncompressed_results = bigquery_client.query_and_wait(
        query_str,
        job_config=job_config,
        query_results_format=enums.QueryResultsFormat.ARROW,
        page_size=500,
    )
    uncompressed_table, uncompressed_wire_bytes = _measure_stream_wire_bytes(
        uncompressed_results
    )

    compressed_results = bigquery_client.query_and_wait(
        query_str,
        job_config=job_config,
        query_results_format=enums.QueryResultsFormat.ARROW,
        compression_codec=codec,
        page_size=500,
    )
    compressed_table, compressed_wire_bytes = _measure_stream_wire_bytes(
        compressed_results
    )

    assert uncompressed_wire_bytes > 0
    assert compressed_wire_bytes > 0
    assert compressed_wire_bytes < uncompressed_wire_bytes
    assert compressed_table.equals(uncompressed_table)
    assert len(compressed_table) == 5000


def test_query_arrow_cached_multi_page(bigquery_client):
    """System test verifying cached multi-page Arrow queries read full results."""
    query_str = "SELECT REPEAT('cached_', 20) AS payload FROM UNNEST(GENERATE_ARRAY(1, 5000)) AS num"

    first_table = bigquery_client.query_and_wait(
        query_str,
        query_results_format=enums.QueryResultsFormat.ARROW,
        page_size=500,
    ).to_arrow()
    cached_table = bigquery_client.query_and_wait(
        query_str,
        query_results_format=enums.QueryResultsFormat.ARROW,
        page_size=500,
    ).to_arrow()

    assert len(first_table) == 5000
    assert len(cached_table) == 5000
    assert cached_table.equals(first_table)


def test_query_arrow_explicit_destination_table(
    dataset_client, dataset_id, test_table_name
):
    """System test verifying explicit destination tables on QueryJobConfig read via CreateReadSession."""
    dest_table = dataset_client.dataset(dataset_id).table(test_table_name)
    job_config = bigquery.QueryJobConfig(
        destination=dest_table,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # 1. Full + max_results read with LZ4_FRAME compression on explicit destination table
    results = dataset_client.query_and_wait(
        "SELECT num, CONCAT('row_', CAST(num AS STRING)) AS label "
        "FROM UNNEST(GENERATE_ARRAY(1, 2000)) AS num ORDER BY num",
        job_config=job_config,
        query_results_format=enums.QueryResultsFormat.ARROW,
        compression_codec=enums.QueryResultsCompressionCodec.LZ4_FRAME,
        max_results=1200,
    )
    table = pyarrow.Table.from_batches(results.to_arrow_iterable())
    assert len(table) == 1200
    assert table.column_names == ["num", "label"]
    assert table.column("num").to_pylist() == list(range(1, 1201))

    # 2. Zero-row explicit destination table preserves pyarrow.Schema
    empty_dest_table = dataset_client.dataset(dataset_id).table(
        f"{test_table_name}_empty"
    )
    empty_results = dataset_client.query_and_wait(
        "SELECT 1 AS num, 'abc' AS label FROM UNNEST(GENERATE_ARRAY(1, 5)) AS x WHERE x > 100",
        job_config=bigquery.QueryJobConfig(destination=empty_dest_table),
        query_results_format=enums.QueryResultsFormat.ARROW,
    )
    assert empty_results.total_rows == 0
    empty_table = empty_results.to_arrow()
    assert len(empty_table) == 0
    assert empty_table.column_names == ["num", "label"]
    assert empty_table.schema.field("num").type == pyarrow.int64()
    assert empty_table.schema.field("label").type == pyarrow.string()
