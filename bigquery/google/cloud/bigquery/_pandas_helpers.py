# Copyright 2019 Google LLC
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

"""Shared helper functions for connecting BigQuery and pandas."""

try:
    import pyarrow
    import pyarrow.parquet
except ImportError:  # pragma: NO COVER
    pyarrow = None
import six.moves


def pyarrow_datetime():
    return pyarrow.timestamp("us", tz=None)


def pyarrow_numeric():
    return pyarrow.decimal128(38, 9)


def pyarrow_time():
    return pyarrow.time64("us")


def pyarrow_timestamp():
    return pyarrow.timestamp("us", tz="UTC")


BQ_TO_ARROW_SCALARS = {}
if pyarrow is not None:
    BQ_TO_ARROW_SCALARS = {
        "BOOL": pyarrow.bool_,
        "BOOLEAN": pyarrow.bool_,
        "BYTES": pyarrow.binary,
        "DATE": pyarrow.date32,
        "DATETIME": pyarrow_datetime,
        "FLOAT": pyarrow.float64,
        "FLOAT64": pyarrow.float64,
        "GEOGRAPHY": pyarrow.string,
        "INT64": pyarrow.int64,
        "INTEGER": pyarrow.int64,
        "NUMERIC": pyarrow_numeric,
        "STRING": pyarrow.string,
        "TIME": pyarrow_time,
        "TIMESTAMP": pyarrow_timestamp,
    }


def bq_to_arrow_data_type(field):
    """Return the Arrow data type, corresponding to a given BigQuery column.

    Returns None if default Arrow type inspection should be used.
    """
    # TODO: Use pyarrow.list_(item_type) for repeated (array) fields.
    if field.mode is not None and field.mode.upper() == "REPEATED":
        return None
    # TODO: Use pyarrow.struct(fields) for record (struct) fields.
    if field.field_type.upper() in ("RECORD", "STRUCT"):
        return None

    data_type_constructor = BQ_TO_ARROW_SCALARS.get(field.field_type.upper())
    if data_type_constructor is None:
        return None
    return data_type_constructor()


def to_parquet(dataframe, bq_schema, filepath):
    """Write dataframe as a Parquet file, according to the desired BQ schema.

    This function requires the :mod:`pyarrow` package. Arrow is used as an
    intermediate format.

    Args:
        dataframe (pandas.DataFrame):
            DataFrame to convert to convert to Parquet file.
        bq_schema (Sequence[google.cloud.bigquery.schema.SchemaField]):
            Desired BigQuery schema. Number of columns must match number of
            columns in the DataFrame.
        filepath (str):
            Path to write Parquet file to.
    """
    if pyarrow is None:
        raise ValueError("pyarrow is required for BigQuery schema conversion")

    if len(bq_schema) != len(dataframe.columns):
        # TODO: match names, too.
        raise ValueError(
            "Number of columns in schema must match number of columns in dataframe"
        )

    arrow_arrays = []
    column_names = []
    for bq_field in bq_schema:
        column_names.append(bq_field.name)
        arrow_arrays.append(
            pyarrow.array(
                dataframe[bq_field.name], type=bq_to_arrow_data_type(bq_field)
            )
        )

    # TODO: make pyarrow table and write to parquet.
    arrow_table = pyarrow.Table.from_arrays(arrow_arrays, names=column_names)
    pyarrow.parquet.write_table(arrow_table, filepath)
