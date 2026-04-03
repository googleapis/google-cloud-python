# Copyright 2023 Google LLC
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

"""
The primary entry point for the BigQuery DataFrames (BigFrames) pandas-compatible API.

**BigQuery DataFrames** provides a Pythonic DataFrame and machine learning (ML) API
powered by the BigQuery engine. The ``bigframes.pandas`` module implements a large
subset of the pandas API, allowing you to perform large-scale data analysis
using familiar pandas syntax while the computations are executed in the cloud.

**Key Features:**

* **Petabyte-Scale Scalability:** Handle datasets that exceed local memory by
  offloading computation to the BigQuery distributed engine.
* **Pandas Compatibility:** Use common pandas methods like
  :func:`~bigframes.pandas.DataFrame.groupby`,
  :func:`~bigframes.pandas.DataFrame.merge`,
  :func:`~bigframes.pandas.DataFrame.pivot_table`, and more on BigQuery-backed
  :class:`~bigframes.pandas.DataFrame` objects.
* **Direct BigQuery Integration:** Read from and write to BigQuery tables and
  queries with :func:`bigframes.pandas.read_gbq` and
  :func:`bigframes.pandas.DataFrame.to_gbq`.
* **User-defined Functions (UDFs):** Effortlessly deploy Python functions
  functions using the :func:`bigframes.pandas.remote_function` and
  :func:`bigframes.pandas.udf` decorators.
* **Data Ingestion:** Support for various formats including CSV, Parquet, JSON,
  and Arrow via :func:`bigframes.pandas.read_csv`,
  :func:`bigframes.pandas.read_parquet`, etc., which are automatically uploaded
  to BigQuery for processing. Convert any pandas DataFrame into a BigQuery
  DataFrame using :func:`bigframes.pandas.read_pandas`.

**Example usage:**

    >>> import bigframes.pandas as bpd

Initialize session and set options.

    >>> bpd.options.bigquery.project = "your-project-id"  # doctest: +SKIP

Load data from a BigQuery public dataset.

    >>> df = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")  # doctest: +SKIP

Perform familiar pandas operations that execute in the cloud.

    >>> top_names = (
    ...     df.groupby("name")
    ...     .agg({"number": "sum"})
    ...     .sort_values("number", ascending=False)
    ...     .head(10)
    ... )  # doctest: +SKIP

Bring the final, aggregated results back to local memory if needed.

    >>> local_df = top_names.to_pandas()  # doctest: +SKIP

BigQuery DataFrames is designed for data scientists and analysts who need the
power of BigQuery with the ease of use of pandas. It eliminates the "data
movement bottleneck" by keeping your data in BigQuery for processing.
"""

from __future__ import annotations

import collections
import datetime
import inspect
import sys
import typing
from typing import Literal, Optional, Sequence, Union

import bigframes_vendored.pandas.core.tools.datetimes as vendored_pandas_datetimes
import pandas

import bigframes._config as config
import bigframes.core.global_session as global_session
import bigframes.core.indexes
import bigframes.dataframe
import bigframes.functions._utils as bff_utils
import bigframes.series
import bigframes.session
import bigframes.session._io.bigquery
import bigframes.version
from bigframes.core.col import col
from bigframes.core.logging import log_adapter
from bigframes.core.reshape.api import concat, crosstab, cut, get_dummies, merge, qcut
from bigframes.pandas import api
from bigframes.pandas.core.api import to_timedelta
from bigframes.pandas.io.api import (
    _read_gbq_colab,
    from_glob_path,
    read_arrow,
    read_avro,
    read_csv,
    read_gbq,
    read_gbq_function,
    read_gbq_model,
    read_gbq_object_table,
    read_gbq_query,
    read_gbq_table,
    read_json,
    read_orc,
    read_pandas,
    read_parquet,
    read_pickle,
)

try:
    import resource
except ImportError:
    # resource is only available on Unix-like systems.
    # https://docs.python.org/3/library/resource.html
    resource = None  # type: ignore


def remote_function(
    # Make sure that the input/output types, and dataset can be used
    # positionally. This avoids the worst of the breaking change from 1.x to
    # 2.x while still preventing possible mixups between consecutive str
    # parameters.
    input_types: Union[None, type, Sequence[type]] = None,
    output_type: Optional[type] = None,
    dataset: Optional[str] = None,
    *,
    bigquery_connection: Optional[str] = None,
    reuse: bool = True,
    name: Optional[str] = None,
    packages: Optional[Sequence[str]] = None,
    cloud_function_service_account: str,
    cloud_function_kms_key_name: Optional[str] = None,
    cloud_function_docker_repository: Optional[str] = None,
    max_batching_rows: Optional[int] = 1000,
    cloud_function_timeout: Optional[int] = 600,
    cloud_function_max_instances: Optional[int] = None,
    cloud_function_vpc_connector: Optional[str] = None,
    cloud_function_vpc_connector_egress_settings: Optional[
        Literal["all", "private-ranges-only", "unspecified"]
    ] = None,
    cloud_function_memory_mib: Optional[int] = None,
    cloud_function_cpus: Optional[float] = None,
    cloud_function_ingress_settings: Literal[
        "all", "internal-only", "internal-and-gclb"
    ] = "internal-only",
    cloud_build_service_account: Optional[str] = None,
):
    return global_session.with_default_session(
        bigframes.session.Session.remote_function,
        input_types=input_types,
        output_type=output_type,
        dataset=dataset,
        bigquery_connection=bigquery_connection,
        reuse=reuse,
        name=name,
        packages=packages,
        cloud_function_service_account=cloud_function_service_account,
        cloud_function_kms_key_name=cloud_function_kms_key_name,
        cloud_function_docker_repository=cloud_function_docker_repository,
        max_batching_rows=max_batching_rows,
        cloud_function_timeout=cloud_function_timeout,
        cloud_function_max_instances=cloud_function_max_instances,
        cloud_function_vpc_connector=cloud_function_vpc_connector,
        cloud_function_vpc_connector_egress_settings=cloud_function_vpc_connector_egress_settings,
        cloud_function_memory_mib=cloud_function_memory_mib,
        cloud_function_cpus=cloud_function_cpus,
        cloud_function_ingress_settings=cloud_function_ingress_settings,
        cloud_build_service_account=cloud_build_service_account,
    )


remote_function.__doc__ = inspect.getdoc(bigframes.session.Session.remote_function)


def deploy_remote_function(
    func,
    **kwargs,
):
    return global_session.with_default_session(
        bigframes.session.Session.deploy_remote_function,
        func=func,
        **kwargs,
    )


deploy_remote_function.__doc__ = inspect.getdoc(
    bigframes.session.Session.deploy_remote_function
)


def udf(
    *,
    input_types: Union[None, type, Sequence[type]] = None,
    output_type: Optional[type] = None,
    dataset: str,
    bigquery_connection: Optional[str] = None,
    name: str,
    packages: Optional[Sequence[str]] = None,
    max_batching_rows: Optional[int] = None,
    container_cpu: Optional[float] = None,
    container_memory: Optional[str] = None,
):
    return global_session.with_default_session(
        bigframes.session.Session.udf,
        input_types=input_types,
        output_type=output_type,
        dataset=dataset,
        bigquery_connection=bigquery_connection,
        name=name,
        packages=packages,
        max_batching_rows=max_batching_rows,
        container_cpu=container_cpu,
        container_memory=container_memory,
    )


udf.__doc__ = inspect.getdoc(bigframes.session.Session.udf)


def deploy_udf(
    func,
    **kwargs,
):
    return global_session.with_default_session(
        bigframes.session.Session.deploy_udf,
        func=func,
        **kwargs,
    )


deploy_udf.__doc__ = inspect.getdoc(bigframes.session.Session.deploy_udf)


@typing.overload
def to_datetime(
    arg: Union[
        vendored_pandas_datetimes.local_iterables,
        bigframes.series.Series,
        bigframes.dataframe.DataFrame,
    ],
    *,
    utc: bool = False,
    format: Optional[str] = None,
    unit: Optional[str] = None,
) -> bigframes.series.Series: ...


@typing.overload
def to_datetime(
    arg: Union[int, float, str, datetime.datetime, datetime.date],
    *,
    utc: bool = False,
    format: Optional[str] = None,
    unit: Optional[str] = None,
) -> Union[pandas.Timestamp, datetime.datetime]: ...


def to_datetime(
    arg: Union[
        Union[int, float, str, datetime.datetime, datetime.date],
        vendored_pandas_datetimes.local_iterables,
        bigframes.series.Series,
        bigframes.dataframe.DataFrame,
    ],
    *,
    utc: bool = False,
    format: Optional[str] = None,
    unit: Optional[str] = None,
) -> Union[pandas.Timestamp, datetime.datetime, bigframes.series.Series]:
    return global_session.with_default_session(
        bigframes.session.Session.to_datetime,
        arg,
        utc=utc,
        format=format,
        unit=unit,
    )


to_datetime.__doc__ = vendored_pandas_datetimes.to_datetime.__doc__


def get_default_session_id() -> str:
    """Gets the session id that is used whenever a custom session
    has not been provided.

    It is the session id of the default global session. It is prefixed to
    the table id of all temporary tables created in the global session.

    Returns:
        str:
            The default global session id, ex. 'sessiona1b2c'
    """
    return get_global_session().session_id


@log_adapter.method_logger
def clean_up_by_session_id(
    session_id: str,
    location: Optional[str] = None,
    project: Optional[str] = None,
) -> None:
    """Searches through BigQuery tables and routines and deletes the ones
    created during the session with the given session id. The match is
    determined by having the session id present in the resource name or
    metadata. The cloud functions serving the cleaned up routines are also
    cleaned up.

    This could be useful if the session object has been lost.
    Calling `session.close()` or `bigframes.pandas.close_session()`
    is preferred in most cases.

    Args:
        session_id (str):
            The session id to clean up. Can be found using
            session.session_id or get_default_session_id().

        location (str, default None):
            The location of the session to clean up. If given, used
            together with project kwarg to determine the dataset
            to search through for tables to clean up.

        project (str, default None):
            The project id associated with the session to clean up.
            If given, used together with location kwarg to determine
            the dataset to search through for tables to clean up.

    Returns:
        None
    """
    session = get_global_session()

    if (location is None) != (project is None):
        raise ValueError(
            "Only one of project or location was given. Must specify both or neither."
        )
    elif location is None and project is None:
        dataset = session._anonymous_dataset
    else:
        dataset = bigframes.session._io.bigquery.create_bq_dataset_reference(
            session.bqclient,
            location=location,
            project=project,
            publisher=session._publisher,
        )

    bigframes.session._io.bigquery.delete_tables_matching_session_id(
        session.bqclient, dataset, session_id
    )

    bff_utils.clean_up_by_session_id(
        session.bqclient, session.cloudfunctionsclient, dataset, session_id
    )


# pandas dtype attributes
NA = pandas.NA
"""Alias for :class:`pandas.NA`."""

BooleanDtype = pandas.BooleanDtype
"""Alias for :class:`pandas.BooleanDtype`."""

Float64Dtype = pandas.Float64Dtype
"""Alias for :class:`pandas.Float64Dtype`."""

Int64Dtype = pandas.Int64Dtype
"""Alias for :class:`pandas.Int64Dtype`."""

StringDtype = pandas.StringDtype
"""Alias for :class:`pandas.StringDtype`."""

ArrowDtype = pandas.ArrowDtype
"""Alias for :class:`pandas.ArrowDtype`."""

# Class aliases
# TODO(swast): Make these real classes so we can refer to these in type
# checking and docstrings.
DataFrame = bigframes.dataframe.DataFrame
Index = bigframes.core.indexes.Index
MultiIndex = bigframes.core.indexes.MultiIndex
DatetimeIndex = bigframes.core.indexes.DatetimeIndex
Series = bigframes.series.Series
__version__ = bigframes.version.__version__

# Other public pandas attributes
NamedAgg = collections.namedtuple("NamedAgg", ["column", "aggfunc"])

options = config.options
"""Global :class:`~bigframes._config.Options` to configure BigQuery DataFrames."""

option_context = config.option_context
"""Global :class:`~bigframes._config.option_context` to configure BigQuery DataFrames."""


# Session management APIs
def get_global_session():
    return global_session.get_global_session()


get_global_session.__doc__ = global_session.get_global_session.__doc__


def close_session():
    return global_session.close_session()


close_session.__doc__ = global_session.close_session.__doc__


def reset_session():
    return global_session.close_session()


reset_session.__doc__ = global_session.close_session.__doc__


# SQL Compilation uses recursive algorithms on deep trees
# 10M tree depth should be sufficient to generate any sql that is under bigquery limit
# Note: This limit does not have the desired effect on Python 3.12 in
# which the applicable limit is now hard coded. See:
# https://github.com/python/cpython/issues/112282
sys.setrecursionlimit(max(10000000, sys.getrecursionlimit()))

if resource is not None:
    soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_STACK)
    if soft_limit < hard_limit or hard_limit == resource.RLIM_INFINITY:
        try:
            resource.setrlimit(resource.RLIMIT_STACK, (hard_limit, hard_limit))
        except Exception:
            pass

_functions = [
    clean_up_by_session_id,
    concat,
    crosstab,
    cut,
    deploy_remote_function,
    deploy_udf,
    get_default_session_id,
    get_dummies,
    merge,
    qcut,
    read_csv,
    read_arrow,
    read_gbq,
    _read_gbq_colab,
    read_gbq_function,
    read_gbq_model,
    read_gbq_object_table,
    read_gbq_query,
    read_gbq_table,
    read_json,
    read_pandas,
    read_parquet,
    read_pickle,
    read_orc,
    read_avro,
    remote_function,
    to_datetime,
    to_timedelta,
    from_glob_path,
]

# Use __all__ to let type checkers know what is part of the public API.
# Note that static analysis checkers like pylance depend on these being string
# literals, not derived at runtime.
__all__ = [
    # Function names
    "clean_up_by_session_id",
    "concat",
    "crosstab",
    "col",
    "cut",
    "deploy_remote_function",
    "deploy_udf",
    "get_default_session_id",
    "get_dummies",
    "merge",
    "qcut",
    "read_csv",
    "read_arrow",
    "read_gbq",
    "_read_gbq_colab",
    "read_gbq_function",
    "read_gbq_model",
    "read_gbq_object_table",
    "read_gbq_query",
    "read_gbq_table",
    "read_json",
    "read_pandas",
    "read_parquet",
    "read_pickle",
    "read_orc",
    "read_avro",
    "remote_function",
    "to_datetime",
    "to_timedelta",
    "from_glob_path",
    # Other names
    "api",
    # pandas dtype attributes
    "NA",
    "BooleanDtype",
    "Float64Dtype",
    "Int64Dtype",
    "StringDtype",
    "ArrowDtype",
    # Class aliases
    "DataFrame",
    "Index",
    "MultiIndex",
    "DatetimeIndex",
    "Series",
    "__version__",
    # Other public pandas attributes
    "NamedAgg",
    "options",
    "option_context",
    # Session management APIs
    "get_global_session",
    "close_session",
    "reset_session",
    "udf",
]

_module = sys.modules[__name__]

for _function in _functions:
    _decorated_object = log_adapter.method_logger(_function, custom_base_name="pandas")
    setattr(_module, _function.__name__, _decorated_object)
