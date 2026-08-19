# Contains code from https://github.com/ibis-project/ibis/blob/9.2.0/ibis/expr/types/typing.py

from __future__ import annotations

from collections.abc import Hashable
from typing import TypeVar

__all__ = ["K", "V"]

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
