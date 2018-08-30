# -*- coding: utf-8 -*-

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
    """Test that floats in a dataframe are encoded with at most 15 significant
        figures.

    See: https://github.com/pydata/pandas-gbq/issues/192
    """
    input_csv = StringIO(u"01/01/17 23:00,1.05148,1.05153,1.05148,1.05153,4")
    df = pandas.read_csv(input_csv, header=None)
    csv_buffer = load.encode_chunk(df)
    csv_bytes = csv_buffer.read()
    csv_string = csv_bytes.decode("utf-8")
    assert "1.05153" in csv_string


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
