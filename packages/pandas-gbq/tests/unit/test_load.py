# -*- coding: utf-8 -*-

import textwrap
from io import StringIO

import numpy
import pandas

from pandas_gbq import load


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


def test_encode_chunks_splits_dataframe():
    df = pandas.DataFrame(numpy.random.randn(6, 4), index=range(6))
    chunks = list(load.encode_chunks(df, chunksize=2))
    assert len(chunks) == 3
    remaining, buffer = chunks[0]
    assert remaining == 4
    assert len(buffer.readlines()) == 2


def test_encode_chunks_with_chunksize_none():
    df = pandas.DataFrame(numpy.random.randn(6, 4), index=range(6))
    chunks = list(load.encode_chunks(df))
    assert len(chunks) == 1
    remaining, buffer = chunks[0]
    assert remaining == 0
    assert len(buffer.readlines()) == 6
