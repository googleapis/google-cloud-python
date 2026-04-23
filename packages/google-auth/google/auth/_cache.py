# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict
from typing import TypeVar

_Key = TypeVar("_Key", bound=Hashable)
_Value = TypeVar("_Value")
_T = TypeVar("_T")


class LRUCache(dict):
    def __init__(self, maxsize: int) -> None:
        super().__init__()
        self._order = OrderedDict()
        self.maxsize = maxsize

    def clear(self) -> None:
        super().clear()
        self._order.clear()

    def get(self, key: _Key, default: _T=None) -> _Value | _T:
        try:
            value = super().__getitem__(key)
            self._update(key)
            return value
        except KeyError:
            return default

    def __getitem__(self, key: _Key) -> _Value:
        value = super().__getitem__(key)
        self._update(key)
        return value

    def __setitem__(self, key: _Key, value: _Value) -> None:
        maxsize = self.maxsize
        if maxsize <= 0:
            return
        if key not in self:
            while len(self) >= maxsize:
                self.popitem()
        super().__setitem__(key, value)
        self._update(key)

    def __delitem__(self, key: _Key) -> None:
        super().__delitem__(key)
        del self._order[key]

    def popitem(self) -> tuple[_Key, _Value]:
        """Remove and return the least recently used key-value pair."""
        key, _ = self._order.popitem(last=False)
        return key, super().pop(key)

    def _update(self, key: _Key) -> None:
        try:
            self._order.move_to_end(key)
        except KeyError:
            self._order[key] = None
