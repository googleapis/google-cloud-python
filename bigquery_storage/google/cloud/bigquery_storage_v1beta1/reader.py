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

from __future__ import absolute_import

import collections
import itertools
import json

try:
    import fastavro
except ImportError:  # pragma: NO COVER
    fastavro = None
import google.api_core.exceptions

try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None
import six

from google.cloud.bigquery_storage_v1beta1 import types


_STREAM_RESUMPTION_EXCEPTIONS = (
    google.api_core.exceptions.DeadlineExceeded,
    google.api_core.exceptions.ServiceUnavailable,
)
_FASTAVRO_REQUIRED = "fastavro is required to parse Avro blocks"


class ReadRowsStream(object):
    """A stream of results from a read rows request.

    This stream is an iterable of
    :class:`~google.cloud.bigquery_storage_v1beta1.types.ReadRowsResponse`.
    Iterate over it to fetch all row blocks.

    If the fastavro library is installed, use the
    :func:`~google.cloud.bigquery_storage_v1beta1.reader.ReadRowsStream.rows()`
    method to parse all blocks into a stream of row dictionaries.

    If the pandas and fastavro libraries are installed, use the
    :func:`~google.cloud.bigquery_storage_v1beta1.reader.ReadRowsStream.to_dataframe()`
    method to parse all blocks into a :class:`pandas.DataFrame`.
    """

    def __init__(self, wrapped, client, read_position, read_rows_kwargs):
        """Construct a ReadRowsStream.

        Args:
            wrapped (Iterable[ \
                ~google.cloud.bigquery_storage_v1beta1.types.ReadRowsResponse \
            ]):
                The ReadRows stream to read.
            client ( \
                ~google.cloud.bigquery_storage_v1beta1.gapic. \
                    big_query_storage_client.BigQueryStorageClient \
            ):
                A GAPIC client used to reconnect to a ReadRows stream. This
                must be the GAPIC client to avoid a circular dependency on
                this class.
            read_position (Union[ \
                dict, \
                ~google.cloud.bigquery_storage_v1beta1.types.StreamPosition \
            ]):
                Required. Identifier of the position in the stream to start
                reading from. The offset requested must be less than the last
                row read from ReadRows. Requesting a larger offset is
                undefined. If a dict is provided, it must be of the same form
                as the protobuf message
                :class:`~google.cloud.bigquery_storage_v1beta1.types.StreamPosition`
            read_rows_kwargs (dict):
                Keyword arguments to use when reconnecting to a ReadRows
                stream.

        Returns:
            Iterable[ \
                ~google.cloud.bigquery_storage_v1beta1.types.ReadRowsResponse \
            ]:
                A sequence of row blocks.
        """

        # Make a copy of the read position so that we can update it without
        # mutating the original input.
        self._position = _copy_stream_position(read_position)
        self._client = client
        self._wrapped = wrapped
        self._read_rows_kwargs = read_rows_kwargs

    def __iter__(self):
        """An iterable of blocks.

        Returns:
            Iterable[ \
                ~google.cloud.bigquery_storage_v1beta1.types.ReadRowsResponse \
            ]:
                A sequence of row blocks.
        """

        # Infinite loop to reconnect on reconnectable errors while processing
        # the row stream.
        while True:
            try:
                for block in self._wrapped:
                    rowcount = block.avro_rows.row_count
                    self._position.offset += rowcount
                    yield block

                return  # Made it through the whole stream.
            except _STREAM_RESUMPTION_EXCEPTIONS:
                # Transient error, so reconnect to the stream.
                pass

            self._reconnect()

    def _reconnect(self):
        """Reconnect to the ReadRows stream using the most recent offset."""
        self._wrapped = self._client.read_rows(
            _copy_stream_position(self._position), **self._read_rows_kwargs
        )

    def rows(self, read_session):
        """Iterate over all rows in the stream.

        This method requires the fastavro library in order to parse row
        blocks.

        .. warning::
            DATETIME columns are not supported. They are currently parsed as
            strings in the fastavro library.

        Args:
            read_session ( \
                ~google.cloud.bigquery_storage_v1beta1.types.ReadSession \
            ):
                The read session associated with this read rows stream. This
                contains the schema, which is required to parse the data
                blocks.

        Returns:
            Iterable[Mapping]:
                A sequence of rows, represented as dictionaries.
        """
        if fastavro is None:
            raise ImportError(_FASTAVRO_REQUIRED)

        avro_schema, _ = _avro_schema(read_session)
        blocks = (_avro_rows(block, avro_schema) for block in self)
        return itertools.chain.from_iterable(blocks)

    def to_dataframe(self, read_session, dtypes=None):
        """Create a :class:`pandas.DataFrame` of all rows in the stream.

        This method requires the pandas libary to create a data frame and the
        fastavro library to parse row blocks.

        .. warning::
            DATETIME columns are not supported. They are currently parsed as
            strings in the fastavro library.

        Args:
            read_session ( \
                ~google.cloud.bigquery_storage_v1beta1.types.ReadSession \
            ):
                The read session associated with this read rows stream. This
                contains the schema, which is required to parse the data
                blocks.
            dtypes ( \
                Map[str, Union[str, pandas.Series.dtype]] \
            ):
                Optional. A dictionary of column names pandas ``dtype``s. The
                provided ``dtype`` is used when constructing the series for
                the column specified. Otherwise, the default pandas behavior
                is used.

        Returns:
            pandas.DataFrame:
                A data frame of all rows in the stream.
        """
        if fastavro is None:
            raise ImportError(_FASTAVRO_REQUIRED)
        if pandas is None:
            raise ImportError("pandas is required to create a DataFrame")

        if dtypes is None:
            dtypes = {}

        avro_schema, column_names = _avro_schema(read_session)
        frames = []
        for block in self:
            dataframe = _to_dataframe_with_dtypes(
                _avro_rows(block, avro_schema), column_names, dtypes
            )
            frames.append(dataframe)
        return pandas.concat(frames)


def _to_dataframe_with_dtypes(rows, column_names, dtypes):
    columns = collections.defaultdict(list)
    for row in rows:
        for column in row:
            columns[column].append(row[column])
    for column in dtypes:
        columns[column] = pandas.Series(columns[column], dtype=dtypes[column])
    return pandas.DataFrame(columns, columns=column_names)


def _avro_schema(read_session):
    """Extract and parse Avro schema from a read session.

    Args:
        read_session ( \
            ~google.cloud.bigquery_storage_v1beta1.types.ReadSession \
        ):
            The read session associated with this read rows stream. This
            contains the schema, which is required to parse the data
            blocks.

    Returns:
        Tuple[fastavro.schema, Tuple[str]]:
            A parsed Avro schema, using :func:`fastavro.schema.parse_schema`
            and the column names for a read session.
    """
    json_schema = json.loads(read_session.avro_schema.schema)
    column_names = tuple((field["name"] for field in json_schema["fields"]))
    return fastavro.parse_schema(json_schema), column_names


def _avro_rows(block, avro_schema):
    """Parse all rows in a stream block.

    Args:
        read_session ( \
            ~google.cloud.bigquery_storage_v1beta1.types.ReadSession \
        ):
            The read session associated with this read rows stream. This
            contains the schema, which is required to parse the data
            blocks.

    Returns:
        Iterable[Mapping]:
            A sequence of rows, represented as dictionaries.
    """
    blockio = six.BytesIO(block.avro_rows.serialized_binary_rows)
    while True:
        # Loop in a while loop because schemaless_reader can only read
        # a single record.
        try:
            # TODO: Parse DATETIME into datetime.datetime (no timezone),
            #       instead of as a string.
            yield fastavro.schemaless_reader(blockio, avro_schema)
        except StopIteration:
            break  # Finished with block


def _copy_stream_position(position):
    """Copy a StreamPosition.

    Args:
        position (Union[ \
            dict, \
            ~google.cloud.bigquery_storage_v1beta1.types.StreamPosition \
        ]):
            StreamPostion (or dictionary in StreamPosition format) to copy.

    Returns:
        ~google.cloud.bigquery_storage_v1beta1.types.StreamPosition:
            A copy of the input StreamPostion.
    """
    if isinstance(position, types.StreamPosition):
        output = types.StreamPosition()
        output.CopyFrom(position)
        return output

    return types.StreamPosition(**position)
