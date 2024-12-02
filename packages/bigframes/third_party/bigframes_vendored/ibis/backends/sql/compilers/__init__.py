# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/backends/sql/compilers/__init__.py

from __future__ import annotations

__all__ = [
    "BigQueryCompiler",
]

from bigframes_vendored.ibis.backends.sql.compilers.bigquery import BigQueryCompiler
