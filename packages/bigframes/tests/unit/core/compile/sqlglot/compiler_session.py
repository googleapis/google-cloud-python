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

import dataclasses
import typing
import weakref

import bigframes.core
import bigframes.core.compile.sqlglot as sqlglot
import bigframes.dataframe
import bigframes.session.executor
import bigframes.session.metrics


@dataclasses.dataclass
class SQLCompilerExecutor(bigframes.session.executor.Executor):
    """Executor for SQL compilation using sqlglot."""

    compiler = sqlglot

    def to_sql(
        self,
        array_value: bigframes.core.ArrayValue,
        offset_column: typing.Optional[str] = None,
        ordered: bool = True,
        enable_cache: bool = False,
    ) -> str:
        if offset_column:
            array_value, _ = array_value.promote_offsets()

        # Compared with BigQueryCachingExecutor, SQLCompilerExecutor skips
        # caching the subtree.
        return self.compiler.SQLGlotCompiler().compile(
            array_value.node, ordered=ordered
        )


class SQLCompilerSession(bigframes.session.Session):
    """Session for SQL compilation using sqlglot."""

    def __init__(self):
        # TODO: remove unused attributes.
        self._location = None  # type: ignore
        self._bq_kms_key_name = None  # type: ignore
        self._clients_provider = None  # type: ignore
        self.ibis_client = None  # type: ignore
        self._bq_connection = None  # type: ignore
        self._skip_bq_connection_check = True
        self._objects: list[
            weakref.ReferenceType[
                typing.Union[
                    bigframes.core.indexes.Index,
                    bigframes.series.Series,
                    bigframes.dataframe.DataFrame,
                ]
            ]
        ] = []
        self._strictly_ordered: bool = True
        self._allow_ambiguity = False  # type: ignore
        self._default_index_type = bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64
        self._metrics = bigframes.session.metrics.ExecutionMetrics()
        self._remote_function_session = None  # type: ignore
        self._temp_storage_manager = None  # type: ignore
        self._loader = None  # type: ignore

        self._session_id: str = "sqlglot_unit_tests_session"
        self._executor = SQLCompilerExecutor()
