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
"""
.. warning::
    **Preview API**: Firestore Pipelines is currently in preview and is
    subject to potential breaking changes in future releases.
"""

from __future__ import annotations
from typing import Optional, Sequence, TYPE_CHECKING
from abc import ABC
from abc import abstractmethod
from enum import Enum

from google.cloud.firestore_v1.types.document import Pipeline as Pipeline_pb
from google.cloud.firestore_v1.types.document import Value
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.pipeline_expressions import (
    AggregateFunction,
    Expression,
    AliasedExpression,
    Field,
    BooleanExpression,
    Selectable,
    Ordering,
)
from google.cloud.firestore_v1._helpers import encode_value

if TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud.firestore_v1.base_pipeline import _BasePipeline
    from google.cloud.firestore_v1.base_document import BaseDocumentReference


class FindNearestOptions:
    """Options for configuring the `FindNearest` pipeline stage.

    Attributes:
        limit (Optional[int]): The maximum number of nearest neighbors to return.
        distance_field (Optional[Field]): An optional field to store the calculated
            distance in the output documents.
    """

    def __init__(
        self,
        limit: Optional[int] = None,
        distance_field: Optional[Field] = None,
    ):
        self.limit = limit
        self.distance_field = distance_field

    def __repr__(self):
        args = []
        if self.limit is not None:
            args.append(f"limit={self.limit}")
        if self.distance_field is not None:
            args.append(f"distance_field={self.distance_field}")
        return f"{self.__class__.__name__}({', '.join(args)})"


class SampleOptions:
    """Options for the 'sample' pipeline stage."""

    class Mode(Enum):
        DOCUMENTS = "documents"
        PERCENT = "percent"

    def __init__(self, value: int | float, mode: Mode | str):
        self.value = value
        self.mode = SampleOptions.Mode[mode.upper()] if isinstance(mode, str) else mode

    def __repr__(self):
        if self.mode == SampleOptions.Mode.DOCUMENTS:
            mode_str = "doc_limit"
        else:
            mode_str = "percentage"
        return f"SampleOptions.{mode_str}({self.value})"

    @staticmethod
    def doc_limit(value: int):
        """
        Sample a set number of documents

        Args:
            value: number of documents to sample
        """
        return SampleOptions(value, mode=SampleOptions.Mode.DOCUMENTS)

    @staticmethod
    def percentage(value: float):
        """
        Sample a percentage of documents

        Args:
            value: percentage of documents to return
        """
        return SampleOptions(value, mode=SampleOptions.Mode.PERCENT)


class UnnestOptions:
    """Options for configuring the `Unnest` pipeline stage.

    Attributes:
        index_field (str): The name of the field to add to each output document,
            storing the original 0-based index of the element within the array.
    """

    def __init__(self, index_field: Field | str):
        self.index_field = (
            index_field if isinstance(index_field, Field) else Field.of(index_field)
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(index_field={self.index_field.path!r})"


class Stage(ABC):
    """Base class for all pipeline stages.

    Each stage represents a specific operation (e.g., filtering, sorting,
    transforming) within a Firestore pipeline. Subclasses define the specific
    arguments and behavior for each operation.
    """

    def __init__(self, custom_name: Optional[str] = None):
        self.name = custom_name or type(self).__name__.lower()

    def _to_pb(self) -> Pipeline_pb.Stage:
        return Pipeline_pb.Stage(
            name=self.name, args=self._pb_args(), options=self._pb_options()
        )

    @abstractmethod
    def _pb_args(self) -> list[Value]:
        """Return Ordered list of arguments the given stage expects"""
        raise NotImplementedError

    def _pb_options(self) -> dict[str, Value]:
        """Return optional named arguments that certain functions may support."""
        return {}

    def __repr__(self):
        items = ("%s=%r" % (k, v) for k, v in self.__dict__.items() if k != "name")
        return f"{self.__class__.__name__}({', '.join(items)})"


class AddFields(Stage):
    """Adds new fields to outputs from previous stages."""

    def __init__(self, *fields: Selectable):
        super().__init__("add_fields")
        self.fields = list(fields)

    def _pb_args(self):
        return [Selectable._to_value(self.fields)]


class Aggregate(Stage):
    """Performs aggregation operations, optionally grouped."""

    def __init__(
        self,
        *args: AliasedExpression[AggregateFunction],
        accumulators: Sequence[AliasedExpression[AggregateFunction]] = (),
        groups: Sequence[str | Selectable] = (),
    ):
        super().__init__()
        self.groups: list[Selectable] = [
            Field(f) if isinstance(f, str) else f for f in groups
        ]
        if args and accumulators:
            raise ValueError(
                "Aggregate stage contains both positional and keyword accumulators"
            )
        self.accumulators = args or accumulators

    def _pb_args(self):
        return [
            Selectable._to_value(self.accumulators),
            Selectable._to_value(self.groups),
        ]

    def __repr__(self):
        accumulator_str = ", ".join(repr(v) for v in self.accumulators)
        group_str = ""
        if self.groups:
            if self.accumulators:
                group_str = ", "
            group_str += f"groups={self.groups}"
        return f"{self.__class__.__name__}({accumulator_str}{group_str})"


class Collection(Stage):
    """Specifies a collection as the initial data source."""

    def __init__(self, path: str):
        super().__init__()
        if not path.startswith("/"):
            path = f"/{path}"
        self.path = path

    def _pb_args(self):
        return [Value(reference_value=self.path)]


class CollectionGroup(Stage):
    """Specifies a collection group as the initial data source."""

    def __init__(self, collection_id: str):
        super().__init__("collection_group")
        self.collection_id = collection_id

    def _pb_args(self):
        return [Value(reference_value=""), Value(string_value=self.collection_id)]


class Database(Stage):
    """Specifies the default database as the initial data source."""

    def __init__(self):
        super().__init__()

    def _pb_args(self):
        return []


class Distinct(Stage):
    """Returns documents with distinct combinations of specified field values."""

    def __init__(self, *fields: str | Selectable):
        super().__init__()
        self.fields: list[Selectable] = [
            Field(f) if isinstance(f, str) else f for f in fields
        ]

    def _pb_args(self) -> list[Value]:
        return [Selectable._to_value(self.fields)]


class Documents(Stage):
    """Specifies specific documents as the initial data source."""

    def __init__(self, *paths: str):
        super().__init__()
        self.paths = paths

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([repr(p) for p in self.paths])})"

    @staticmethod
    def of(*documents: "BaseDocumentReference") -> "Documents":
        doc_paths = ["/" + doc.path for doc in documents]
        return Documents(*doc_paths)

    def _pb_args(self):
        return [Value(reference_value=path) for path in self.paths]


class FindNearest(Stage):
    """Performs vector distance (similarity) search."""

    def __init__(
        self,
        field: str | Expression,
        vector: Sequence[float] | Vector,
        distance_measure: "DistanceMeasure" | str,
        options: Optional["FindNearestOptions"] = None,
    ):
        super().__init__("find_nearest")
        self.field: Expression = Field(field) if isinstance(field, str) else field
        self.vector: Vector = vector if isinstance(vector, Vector) else Vector(vector)
        self.distance_measure = (
            distance_measure
            if isinstance(distance_measure, DistanceMeasure)
            else DistanceMeasure[distance_measure.upper()]
        )
        self.options = options or FindNearestOptions()

    def _pb_args(self):
        return [
            self.field._to_pb(),
            encode_value(self.vector),
            Value(string_value=self.distance_measure.name.lower()),
        ]

    def _pb_options(self) -> dict[str, Value]:
        options = {}
        if self.options and self.options.limit is not None:
            options["limit"] = Value(integer_value=self.options.limit)
        if self.options and self.options.distance_field is not None:
            options["distance_field"] = self.options.distance_field._to_pb()
        return options


class RawStage(Stage):
    """Represents a generic, named stage with parameters."""

    def __init__(
        self,
        name: str,
        *params: Expression | Value,
        options: dict[str, Expression | Value] = {},
    ):
        super().__init__(name)
        self.params: list[Value] = [
            p._to_pb() if isinstance(p, Expression) else p for p in params
        ]
        self.options: dict[str, Value] = {
            k: v._to_pb() if isinstance(v, Expression) else v
            for k, v in options.items()
        }

    def _pb_args(self):
        return self.params

    def _pb_options(self):
        return self.options

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"


class Limit(Stage):
    """Limits the maximum number of documents returned."""

    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit

    def _pb_args(self):
        return [Value(integer_value=self.limit)]


class Offset(Stage):
    """Skips a specified number of documents."""

    def __init__(self, offset: int):
        super().__init__()
        self.offset = offset

    def _pb_args(self):
        return [Value(integer_value=self.offset)]


class RemoveFields(Stage):
    """Removes specified fields from outputs."""

    def __init__(self, *fields: str | Field):
        super().__init__("remove_fields")
        self.fields = [Field(f) if isinstance(f, str) else f for f in fields]

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(repr(f) for f in self.fields)})"

    def _pb_args(self) -> list[Value]:
        return [f._to_pb() for f in self.fields]


class ReplaceWith(Stage):
    """Replaces the document content with the value of a specified field."""

    def __init__(self, field: Selectable):
        super().__init__("replace_with")
        self.field = Field(field) if isinstance(field, str) else field

    def _pb_args(self):
        return [self.field._to_pb(), Value(string_value="full_replace")]


class Sample(Stage):
    """Performs pseudo-random sampling of documents."""

    def __init__(self, limit_or_options: int | SampleOptions):
        super().__init__()
        if isinstance(limit_or_options, int):
            options = SampleOptions.doc_limit(limit_or_options)
        else:
            options = limit_or_options
        self.options: SampleOptions = options

    def _pb_args(self):
        if self.options.mode == SampleOptions.Mode.DOCUMENTS:
            return [
                Value(integer_value=self.options.value),
                Value(string_value="documents"),
            ]
        else:
            return [
                Value(double_value=self.options.value),
                Value(string_value="percent"),
            ]


class Select(Stage):
    """Selects or creates a set of fields."""

    def __init__(self, *selections: str | Selectable):
        super().__init__()
        self.projections = [Field(s) if isinstance(s, str) else s for s in selections]

    def _pb_args(self) -> list[Value]:
        return [Selectable._value_from_selectables(*self.projections)]


class Sort(Stage):
    """Sorts documents based on specified criteria."""

    def __init__(self, *orders: "Ordering"):
        super().__init__()
        self.orders = list(orders)

    def _pb_args(self):
        return [o._to_pb() for o in self.orders]


class Union(Stage):
    """Performs a union of documents from two pipelines."""

    def __init__(self, other: _BasePipeline):
        super().__init__()
        self.other = other

    def _pb_args(self):
        return [Value(pipeline_value=self.other._to_pb().pipeline)]


class Unnest(Stage):
    """Produces a document for each element in an array field."""

    def __init__(
        self,
        field: Selectable | str,
        alias: Field | str | None = None,
        options: UnnestOptions | None = None,
    ):
        super().__init__()
        self.field: Selectable = Field(field) if isinstance(field, str) else field
        if alias is None:
            self.alias = self.field
        elif isinstance(alias, str):
            self.alias = Field(alias)
        else:
            self.alias = alias
        self.options = options

    def _pb_args(self):
        return [self.field._to_pb(), self.alias._to_pb()]

    def _pb_options(self):
        options = {}
        if self.options is not None:
            options["index_field"] = self.options.index_field._to_pb()
        return options


class Where(Stage):
    """Filters documents based on a specified condition."""

    def __init__(self, condition: BooleanExpression):
        super().__init__()
        self.condition = condition

    def _pb_args(self):
        return [self.condition._to_pb()]
