# -*- coding: utf-8 -*-

import textwrap
from io import StringIO
from unittest import mock

import numpy
import pandas
import pytest

from pandas_gbq.features import FEATURES
from pandas_gbq import load


def load_method(bqclient):
    if FEATURES.bigquery_has_from_dataframe_with_csv:
        return bqclient.load_table_from_dataframe
    return bqclient.load_table_from_file


def test_encode_chunk_with_unicode():
    """Test that a dataframe containing unicode can be encoded as a file.

    See: https://github.com/pydata/pandas-gbq/issues/106
    """
    df = pandas.DataFrame(
        numpy.random.randn(6, 4), index=range(6), columns=list("ABCD")
    )
    df["s"] = u"信用卡"
    csv_buffer = load.encode_chunk(df)
    csv_bytes = csv_buffer.read()
    csv_string = csv_bytes.decode("utf-8")
    assert u"信用卡" in csv_string


def test_encode_chunk_with_floats():
    """Test that floats in a dataframe are encoded with at most 17 significant
        figures.

    See: https://github.com/pydata/pandas-gbq/issues/192 and
    https://github.com/pydata/pandas-gbq/issues/326
    """
    input_csv = textwrap.dedent(
        """01/01/17 23:00,0.14285714285714285,4
        01/02/17 22:00,1.05148,3
        01/03/17 21:00,1.05153,2
        01/04/17 20:00,3.141592653589793,1
        01/05/17 19:00,2.0988936657440586e+43,0
        """
    )
    input_df = pandas.read_csv(
        StringIO(input_csv), header=None, float_precision="round_trip"
    )
    csv_buffer = load.encode_chunk(input_df)
    round_trip = pandas.read_csv(
        csv_buffer, header=None, float_precision="round_trip"
    )
    pandas.testing.assert_frame_equal(
        round_trip,
        input_df,
        check_exact=True,
    )


def test_encode_chunk_with_newlines():
    """See: https://github.com/pydata/pandas-gbq/issues/180"""
    df = pandas.DataFrame({"s": ["abcd", "ef\ngh", "ij\r\nkl"]})
    csv_buffer = load.encode_chunk(df)
    csv_bytes = csv_buffer.read()
    csv_string = csv_bytes.decode("utf-8")
    assert "abcd" in csv_string
    assert '"ef\ngh"' in csv_string
    assert '"ij\r\nkl"' in csv_string


def test_split_dataframe():
    df = pandas.DataFrame(numpy.random.randn(6, 4), index=range(6))
    chunks = list(load.split_dataframe(df, chunksize=2))
    assert len(chunks) == 3
    remaining, chunk = chunks[0]
    assert remaining == 4
    assert len(chunk.index) == 2


def test_encode_chunks_with_chunksize_none():
    df = pandas.DataFrame(numpy.random.randn(6, 4), index=range(6))
    chunks = list(load.split_dataframe(df))
    assert len(chunks) == 1
    remaining, chunk = chunks[0]
    assert remaining == 0
    assert len(chunk.index) == 6


@pytest.mark.parametrize(
    ["bigquery_has_from_dataframe_with_csv"], [(True,), (False,)]
)
def test_load_chunks_omits_policy_tags(
    monkeypatch, mock_bigquery_client, bigquery_has_from_dataframe_with_csv
):
    """Ensure that policyTags are omitted.

    We don't want to change the policyTags via a load job, as this can cause
    403 error. See: https://github.com/googleapis/python-bigquery/pull/557
    """
    import google.cloud.bigquery

    monkeypatch.setattr(
        type(FEATURES),
        "bigquery_has_from_dataframe_with_csv",
        mock.PropertyMock(return_value=bigquery_has_from_dataframe_with_csv),
    )
    df = pandas.DataFrame({"col1": [1, 2, 3]})
    destination = google.cloud.bigquery.TableReference.from_string(
        "my-project.my_dataset.my_table"
    )
    schema = {
        "fields": [
            {"name": "col1", "type": "INT64", "policyTags": ["tag1", "tag2"]}
        ]
    }

    _ = list(
        load.load_chunks(mock_bigquery_client, df, destination, schema=schema)
    )

    mock_load = load_method(mock_bigquery_client)
    assert mock_load.called
    _, kwargs = mock_load.call_args
    assert "job_config" in kwargs
    sent_field = kwargs["job_config"].schema[0].to_api_repr()
    assert "policyTags" not in sent_field
