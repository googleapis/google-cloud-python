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

from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import Boolean, Float


class search(GenericFunction):
    """Spanner SEARCH(target, query) FTS function."""

    type = Boolean
    name = "SEARCH"


class search_substring(GenericFunction):
    """Spanner SEARCH_SUBSTRING(target, query) FTS function."""

    type = Boolean
    name = "SEARCH_SUBSTRING"


class score(GenericFunction):
    """Spanner SCORE(target, query) relevance score function."""

    type = Float
    name = "SCORE"


class score_ngrams(GenericFunction):
    """Spanner SCORE_NGRAMS(target, query) N-gram score function."""

    type = Float
    name = "SCORE_NGRAMS"


class tokenize_fulltext(GenericFunction):
    """Spanner TOKENIZE_FULLTEXT(text, ...) function."""

    name = "TOKENIZE_FULLTEXT"


class tokenize_substring(GenericFunction):
    """Spanner TOKENIZE_SUBSTRING(text, ...) function."""

    name = "TOKENIZE_SUBSTRING"


class tokenize_ngrams(GenericFunction):
    """Spanner TOKENIZE_NGRAMS(text, ...) function."""

    name = "TOKENIZE_NGRAMS"


class tokenize_bool(GenericFunction):
    """Spanner TOKENIZE_BOOL(bool_val) function."""

    name = "TOKENIZE_BOOL"


class tokenize_number(GenericFunction):
    """Spanner TOKENIZE_NUMBER(number_val) function."""

    name = "TOKENIZE_NUMBER"


class tokenize_array(GenericFunction):
    """Spanner TOKENIZE_ARRAY(array_val) function."""

    name = "TOKENIZE_ARRAY"
