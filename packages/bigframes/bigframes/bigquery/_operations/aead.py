# Copyright 2026 Google LLC
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

#
# DO NOT MODIFY THIS FILE DIRECTLY.
# This file was generated from: scripts/data/sql-functions/aead.yaml
# by the script: scripts/generate_bigframes_bigquery.py

from __future__ import annotations

import datetime
from typing import Any, Optional, TypeVar, Union

import bigframes.core.col
import bigframes.core.expression as ex
import bigframes.core.sentinels as sentinels
import bigframes.operations as ops
import bigframes.series as series
from bigframes import dtypes
from bigframes.operations import googlesql

T = TypeVar("T", series.Series, bigframes.core.col.Expression)

_DECRYPT_BYTES_OP = googlesql.GoogleSqlScalarOp(
    "AEAD.DECRYPT_BYTES",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.BYTES_DTYPE,
)
_DECRYPT_STRING_OP = googlesql.GoogleSqlScalarOp(
    "AEAD.DECRYPT_STRING",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.STRING_DTYPE,
)
_ENCRYPT_OP = googlesql.GoogleSqlScalarOp(
    "AEAD.ENCRYPT",
    args=(googlesql.ArgSpec(), googlesql.ArgSpec(), googlesql.ArgSpec()),
    signature=lambda *args: dtypes.BYTES_DTYPE,
)


def _apply_googlesql_op(
    op: googlesql.GoogleSqlScalarOp,
    *args: Any,
) -> Union[series.Series, bigframes.core.col.Expression]:
    """Applies a GoogleSQL scalar operator to the given arguments.

    Handles a mix of Series, Expression, and literal inputs.
    """
    # Find the first Series to use for alignment
    first_series = None
    for arg in args:
        if isinstance(arg, series.Series):
            first_series = arg
            break

    if first_series is not None:
        processed_args = []
        block = first_series._block
        for arg in args:
            if isinstance(arg, bigframes.core.col.Expression):
                # Project expression onto the block
                block, col_id = block.project_expr(arg._expr)
                processed_args.append(series.Series(block.select_column(col_id)))
            elif arg is sentinels.DEFAULT:
                # OmittedArg is handled by GoogleSqlScalarOp in compiler
                processed_args.append(bigframes.core.col.Expression(ex.OmittedArg()))
            else:
                processed_args.append(arg)

        # Apply the n-ary op. _apply_nary_op handles alignment of Series and literals.
        result = first_series._apply_nary_op(op, processed_args, ignore_self=True)
        result.name = None
        return result

    # No Series, return an Expression
    expr_args = []
    for arg in args:
        if isinstance(arg, bigframes.core.col.Expression):
            expr_args.append(arg._expr)
        elif arg is sentinels.DEFAULT:
            expr_args.append(ex.OmittedArg())
        else:
            expr_args.append(ex.const(arg))

    return bigframes.core.col.Expression(ex.OpExpression(op, tuple(expr_args)))


def decrypt_bytes(
    keyset: Union[T, Union[bytes, dict]],
    ciphertext: Union[T, bytes],
    additional_data: Union[T, bytes],
) -> T:
    """Uses the matching key from keyset to decrypt ciphertext and verifies the integrity of the data using additional_data. Returns an error if decryption or verification fails."""
    return _apply_googlesql_op(
        _DECRYPT_BYTES_OP,
        keyset,
        ciphertext,
        additional_data,
    )  # type: ignore


def decrypt_string(
    keyset: Union[T, Union[bytes, dict]],
    ciphertext: Union[T, bytes],
    additional_data: Union[T, str],
) -> T:
    """Like AEAD.DECRYPT_BYTES, but where additional_data is of type STRING."""
    return _apply_googlesql_op(
        _DECRYPT_STRING_OP,
        keyset,
        ciphertext,
        additional_data,
    )  # type: ignore


def encrypt(
    keyset: Union[T, Union[bytes, dict]],
    plaintext: Union[T, Union[bytes, str]],
    additional_data: Union[T, Union[bytes, str]],
) -> T:
    """Encrypts plaintext using the primary cryptographic key in keyset. The algorithm of the primary key must be AEAD_AES_GCM_256. Binds the ciphertext to the context defined by additional_data. Returns NULL if any input is NULL."""
    return _apply_googlesql_op(
        _ENCRYPT_OP,
        keyset,
        plaintext,
        additional_data,
    )  # type: ignore
