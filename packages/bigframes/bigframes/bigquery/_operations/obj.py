# Copyright 2025 Google LLC
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


"""This module exposes BigQuery ObjectRef functions.

See bigframes.bigquery.obj for public docs.
"""


from __future__ import annotations

import datetime
from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd

from bigframes.core import convert
from bigframes.core.logging import log_adapter
import bigframes.core.utils as utils
import bigframes.operations as ops
import bigframes.series as series


@log_adapter.method_logger(custom_base_name="bigquery_obj")
def fetch_metadata(
    objectref: series.Series,
) -> series.Series:
    """[Preview] The OBJ.FETCH_METADATA function returns Cloud Storage metadata for a partially populated ObjectRef value.

    Args:
        objectref (bigframes.pandas.Series):
            A partially populated ObjectRef value, in which the uri and authorizer fields are populated and the details field isn't.

    Returns:
        bigframes.pandas.Series: A fully populated ObjectRef value. The metadata is provided in the details field of the returned ObjectRef value.
    """
    objectref = convert.to_bf_series(objectref, default_index=None)
    return objectref._apply_unary_op(ops.obj_fetch_metadata_op)


@log_adapter.method_logger(custom_base_name="bigquery_obj")
def get_access_url(
    objectref: series.Series,
    mode: str,
    duration: Optional[Union[datetime.timedelta, pd.Timedelta, np.timedelta64]] = None,
) -> series.Series:
    """[Preview] The OBJ.GET_ACCESS_URL function returns JSON that contains reference information for the input ObjectRef value, and also access URLs that you can use to read or modify the Cloud Storage object.

    Args:
        objectref (bigframes.pandas.Series):
            An ObjectRef value that represents a Cloud Storage object.
        mode (str):
            A STRING value that identifies the type of URL that you want to be returned. The following values are supported:
            'r': Returns a URL that lets you read the object.
            'rw': Returns two URLs, one that lets you read the object, and one that lets you modify the object.
        duration (Union[datetime.timedelta, pandas.Timedelta, numpy.timedelta64], optional):
            An optional INTERVAL value that specifies how long the generated access URLs remain valid. You can specify a value between 30 minutes and 6 hours. For example, you could specify INTERVAL 2 HOUR to generate URLs that expire after 2 hours. The default value is 6 hours.

    Returns:
        bigframes.pandas.Series: A JSON value that contains the Cloud Storage object reference information from the input ObjectRef value, and also one or more URLs that you can use to access the Cloud Storage object.
    """
    objectref = convert.to_bf_series(objectref, default_index=None)

    duration_micros = None
    if duration is not None:
        duration_micros = utils.timedelta_to_micros(duration)

    return objectref._apply_unary_op(
        ops.ObjGetAccessUrl(mode=mode, duration=duration_micros)
    )


@log_adapter.method_logger(custom_base_name="bigquery_obj")
def make_ref(
    uri_or_json: Union[series.Series, Sequence[str]],
    authorizer: Union[series.Series, str, None] = None,
) -> series.Series:
    """[Preview] Use the OBJ.MAKE_REF function to create an ObjectRef value that contains reference information for a Cloud Storage object.

    Args:
        uri_or_json (bigframes.pandas.Series or str):
            A series of STRING values that contains the URI for the Cloud Storage object, for example, gs://mybucket/flowers/12345.jpg.
            OR
            A series of JSON value that represents a Cloud Storage object.
        authorizer (bigframes.pandas.Series or str, optional):
            A STRING value that contains the Cloud Resource connection used to access the Cloud Storage object.
            Required if ``uri_or_json`` is a URI string.

    Returns:
        bigframes.pandas.Series: An ObjectRef value.
    """
    uri_or_json = convert.to_bf_series(uri_or_json, default_index=None)

    if authorizer is not None:
        # Avoid join problems encountered if we try to convert a literal into Series.
        if not isinstance(authorizer, str):
            authorizer = convert.to_bf_series(authorizer, default_index=None)

        return uri_or_json._apply_binary_op(authorizer, ops.obj_make_ref_op)

    # If authorizer is not provided, we assume uri_or_json is a JSON objectref
    return uri_or_json._apply_unary_op(ops.obj_make_ref_json_op)
