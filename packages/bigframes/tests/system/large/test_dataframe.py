import sys

import pandas as pd
import pytest


@pytest.mark.skipif(
    sys.version_info >= (3, 12),
    # See: https://github.com/python/cpython/issues/112282
    reason="setrecursionlimit has no effect on the Python C stack since Python 3.12.",
)
def test_corr_150_columns(scalars_df_numeric_150_columns_maybe_ordered):
    scalars_df, scalars_pandas_df = scalars_df_numeric_150_columns_maybe_ordered
    bf_result = scalars_df.corr(numeric_only=True).to_pandas()
    pd_result = scalars_pandas_df.corr(numeric_only=True)

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_dtype=False,
        check_index_type=False,
        check_column_type=False,
    )


@pytest.mark.skipif(
    sys.version_info >= (3, 12),
    # See: https://github.com/python/cpython/issues/112282
    reason="setrecursionlimit has no effect on the Python C stack since Python 3.12.",
)
def test_cov_150_columns(scalars_df_numeric_150_columns_maybe_ordered):
    scalars_df, scalars_pandas_df = scalars_df_numeric_150_columns_maybe_ordered
    bf_result = scalars_df.cov(numeric_only=True).to_pandas()
    pd_result = scalars_pandas_df.cov(numeric_only=True)

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_dtype=False,
        check_index_type=False,
        check_column_type=False,
    )
