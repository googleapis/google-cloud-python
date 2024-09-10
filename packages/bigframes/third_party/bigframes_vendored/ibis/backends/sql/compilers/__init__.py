# Contains code from https://github.com/ibis-project/ibis/blob/main/ibis/backends/sql/compilers/__init__.py

import bigframes_vendored.ibis.backends.sql.compilers.bigquery as bigquery

__all__ = [
    "bigquery",
]
