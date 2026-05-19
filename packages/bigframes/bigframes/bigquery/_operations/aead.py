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

from typing import TypeVar, Union

import bigframes.bigquery._googlesql
import bigframes.core.col
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


def decrypt_bytes(
    keyset: Union[T, bigframes.core.col.Expression, Union[bytes, dict]],
    ciphertext: Union[T, bigframes.core.col.Expression, bytes],
    additional_data: Union[T, bigframes.core.col.Expression, bytes],
) -> T:
    """Uses the matching key from keyset to decrypt ciphertext and verifies the integrity of the data using additional_data. Returns an error if decryption or verification fails."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _DECRYPT_BYTES_OP,
        keyset,
        ciphertext,
        additional_data,
    )  # type: ignore


def decrypt_string(
    keyset: Union[T, bigframes.core.col.Expression, Union[bytes, dict]],
    ciphertext: Union[T, bigframes.core.col.Expression, bytes],
    additional_data: Union[T, bigframes.core.col.Expression, str],
) -> T:
    """Like AEAD.DECRYPT_BYTES, but where additional_data is of type STRING."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _DECRYPT_STRING_OP,
        keyset,
        ciphertext,
        additional_data,
    )  # type: ignore


def encrypt(
    keyset: Union[T, bigframes.core.col.Expression, Union[bytes, dict]],
    plaintext: Union[T, bigframes.core.col.Expression, Union[bytes, str]],
    additional_data: Union[T, bigframes.core.col.Expression, Union[bytes, str]],
) -> T:
    """Encrypts plaintext using the primary cryptographic key in keyset. The algorithm of the primary key must be AEAD_AES_GCM_256. Binds the ciphertext to the context defined by additional_data. Returns NULL if any input is NULL."""
    return bigframes.bigquery._googlesql.apply_googlesql_scalar_op(
        _ENCRYPT_OP,
        keyset,
        plaintext,
        additional_data,
    )  # type: ignore
