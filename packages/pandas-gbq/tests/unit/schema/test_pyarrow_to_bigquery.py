# Copyright (c) 2024 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import pyarrow

from pandas_gbq.schema import pyarrow_to_bigquery


def test_arrow_type_to_bigquery_field_unknown():
    # Default types should be picked at a higher layer.
    assert (
        pyarrow_to_bigquery.arrow_type_to_bigquery_field("test_name", pyarrow.null())
        is None
    )


def test_arrow_type_to_bigquery_field_list_of_unknown():
    # Default types should be picked at a higher layer.
    assert (
        pyarrow_to_bigquery.arrow_type_to_bigquery_field(
            "test_name", pyarrow.list_(pyarrow.null())
        )
        is None
    )
