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
from __future__ import annotations

from typing import Mapping, Sequence, Tuple


class JoinNameRemapper:
    def __init__(self, namespace: str) -> None:
        self._namespace = namespace

    def __call__(
        self, left_column_ids: Sequence[str], right_column_ids: Sequence[str]
    ) -> Tuple[Mapping[str, str], Mapping[str, str]]:
        """
        When joining column ids from different namespaces, this function defines how names are remapped.

        Take care to map value column ids and hidden column ids in separate namespaces. This is important because value
        column ids must be deterministic as they are referenced by dependent operators. The generation of hidden ids is
        dependent on compilation context, and should be completely separated from value column id mappings.
        """
        # This naming strategy depends on the number of value columns in source tables.
        # This means column id mappings must be adjusted if pushing operations above or below join in transformation
        new_left_ids = {
            col: f"{self._namespace}_l_{i}" for i, col in enumerate(left_column_ids)
        }
        new_right_ids = {
            col: f"{self._namespace}_r_{i}" for i, col in enumerate(right_column_ids)
        }
        return new_left_ids, new_right_ids


# Defines how column ids are remapped, regardless of join strategy or ordering mode
# Use this remapper for all value column remappings.
JOIN_NAME_REMAPPER = JoinNameRemapper("bfjoin")
