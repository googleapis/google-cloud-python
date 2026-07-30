from unittest import mock

import pyarrow as pa

import pandas_gbq.arrow


def test_from_read_rows_response_valid_message_returns_record_batch():
    schema = pa.schema([("id", pa.int64()), ("name", pa.string())])
    batch = pa.RecordBatch.from_arrays(
        [pa.array([1, 2]), pa.array(["alice", "bob"])], schema=schema
    )
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, schema) as writer:
        writer.write_batch(batch)
    serialized_bytes = sink.getvalue().to_pybytes()

    mock_message = mock.MagicMock()
    mock_message.arrow_record_batch.serialized_record_batch = serialized_bytes

    result_batch = pandas_gbq.arrow.from_read_rows_response(
        mock_message, arrow_schema=schema
    )

    assert result_batch.num_rows == 2
    assert result_batch.schema.names == ["id", "name"]
    assert result_batch.column(0).to_pylist() == [1, 2]
    assert result_batch.column(1).to_pylist() == ["alice", "bob"]


def test_from_read_rows_response_empty_message_returns_empty_batch():
    schema = pa.schema([("val", pa.float64())])
    mock_message = mock.MagicMock()
    mock_message.arrow_record_batch.serialized_record_batch = b""

    result_batch = pandas_gbq.arrow.from_read_rows_response(
        mock_message, arrow_schema=schema
    )

    assert result_batch.num_rows == 0
    assert result_batch.schema == schema


def test_from_read_rows_response_uninstalled_pyarrow_raises_import_error():
    mock_message = mock.MagicMock()

    with mock.patch.object(pandas_gbq.arrow, "pa", None):
        import pytest

        with pytest.raises(ImportError, match="pyarrow is required"):
            pandas_gbq.arrow.from_read_rows_response(mock_message)
