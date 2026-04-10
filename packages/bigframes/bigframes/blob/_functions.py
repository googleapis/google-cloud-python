# Copyright 2024 Google LLC
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

import inspect
import typing
from dataclasses import dataclass
from typing import Callable, Iterable, Union

import google.cloud.bigquery as bigquery

import bigframes.session
import bigframes.session._io.bigquery as bf_io_bigquery

_PYTHON_TO_BQ_TYPES = {
    int: "INT64",
    float: "FLOAT64",
    str: "STRING",
    bytes: "BYTES",
    bool: "BOOL",
}


@dataclass(frozen=True)
class FunctionDef:
    """Definition of a Python UDF."""

    func: Callable  # function body
    requirements: Iterable[str]  # required packages


# TODO(garrettwu): migrate to bigframes UDF when it is available
class TransformFunction:
    """Simple transform function class to deal with Python UDF."""

    def __init__(
        self,
        func_def: FunctionDef,
        session: bigframes.session.Session,
        connection: str,
        max_batching_rows: int,
        container_cpu: Union[float, int],
        container_memory: str,
    ):
        self._func = func_def.func
        self._requirements = func_def.requirements
        self._session = session
        self._connection = connection
        self._max_batching_rows = (
            int(max_batching_rows) if max_batching_rows > 1 else max_batching_rows
        )
        self._container_cpu = container_cpu
        self._container_memory = container_memory

    def _input_bq_signature(self):
        sig = inspect.signature(self._func)
        inputs = []
        for k, v in sig.parameters.items():
            inputs.append(f"{k} {_PYTHON_TO_BQ_TYPES[v.annotation]}")
        return ", ".join(inputs)

    def _output_bq_type(self):
        sig = inspect.signature(self._func)
        return_annotation = sig.return_annotation
        origin = typing.get_origin(return_annotation)
        if origin is Union:
            args = typing.get_args(return_annotation)
            if len(args) == 2 and args[1] is type(None):
                return _PYTHON_TO_BQ_TYPES[args[0]]
        return _PYTHON_TO_BQ_TYPES[sig.return_annotation]

    def _create_udf(self):
        """Create Python UDF in BQ. Return name of the UDF."""
        udf_name = str(
            self._session._anon_dataset_manager.generate_unique_resource_id()
        )

        func_body = "import typing\n" + inspect.getsource(self._func)
        func_name = self._func.__name__
        packages = str(list(self._requirements))

        sql = f"""
CREATE OR REPLACE FUNCTION `{udf_name}`({self._input_bq_signature()})
RETURNS {self._output_bq_type()} LANGUAGE python
WITH CONNECTION `{self._connection}`
OPTIONS (entry_point='{func_name}', runtime_version='python-3.11', packages={packages}, max_batching_rows={self._max_batching_rows}, container_cpu={self._container_cpu}, container_memory='{self._container_memory}')
AS r\"\"\"


{func_body}


\"\"\"
        """

        bf_io_bigquery.start_query_with_client(
            self._session.bqclient,
            sql,
            job_config=bigquery.QueryJobConfig(),
            metrics=self._session._metrics,
            location=None,
            project=None,
            timeout=None,
            query_with_job=True,
            publisher=self._session._publisher,
        )

        return udf_name

    def udf(self):
        """Create and return the UDF object."""
        udf_name = self._create_udf()

        # TODO(b/404605969): remove cleanups when UDF fixes dataset deletion.
        self._session._function_session._update_temp_artifacts(udf_name, "")
        return self._session.read_gbq_function(udf_name)
