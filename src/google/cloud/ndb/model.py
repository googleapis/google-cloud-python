# Copyright 2018 Google LLC
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

"""Model classes for datastore objects and properties for models."""


from google.cloud.ndb import _exceptions
from google.cloud.ndb import key as key_module


__all__ = [
    "Key",
    "BlobKey",
    "GeoPt",
    "Rollback",
    "KindError",
    "InvalidPropertyError",
    "BadProjectionError",
    "UnprojectedPropertyError",
    "ReadonlyPropertyError",
    "ComputedPropertyError",
    "IndexProperty",
    "Index",
    "IndexState",
    "ModelAdapter",
    "make_connection",
    "ModelAttribute",
    "Property",
    "ModelKey",
    "BooleanProperty",
    "IntegerProperty",
    "FloatProperty",
    "BlobProperty",
    "TextProperty",
    "StringProperty",
    "GeoPtProperty",
    "PickleProperty",
    "JsonProperty",
    "UserProperty",
    "KeyProperty",
    "BlobKeyProperty",
    "DateTimeProperty",
    "DateProperty",
    "TimeProperty",
    "StructuredProperty",
    "LocalStructuredProperty",
    "GenericProperty",
    "ComputedProperty",
    "MetaModel",
    "Model",
    "Expando",
    "transaction",
    "transaction_async",
    "in_transaction",
    "transactional",
    "transactional_async",
    "transactional_tasklet",
    "non_transactional",
    "get_multi_async",
    "get_multi",
    "put_multi_async",
    "put_multi",
    "delete_multi_async",
    "delete_multi",
    "get_indexes_async",
    "get_indexes",
]


Key = key_module.Key
BlobKey = NotImplemented  # From `google.appengine.api.datastore_types`
GeoPt = NotImplemented  # From `google.appengine.api.datastore_types`
Rollback = _exceptions.Rollback


class KindError(_exceptions.BadValueError):
    """Raised when an implementation for a kind can't be found.

    May also be raised when the kind is not a byte string.
    """


class InvalidPropertyError(_exceptions.Error):
    """Raised when a property is not applicable to a given use.

    For example, a property must exist and be indexed to be used in a query's
    projection or group by clause.
    """


BadProjectionError = InvalidPropertyError
"""This alias for :class:`InvalidPropertyError` is for legacy support."""


class UnprojectedPropertyError(_exceptions.Error):
    """Raised when getting a property value that's not in the projection."""


class ReadonlyPropertyError(_exceptions.Error):
    """Raised when attempting to set a property value that is read-only."""


class ComputedPropertyError(ReadonlyPropertyError):
    """Raised when attempting to set or delete a computed property."""


class IndexProperty:
    """Immutable object representing a single property in an index."""

    __slots__ = ("_name", "_direction")

    def __init__(self, *, name, direction):
        self._name = name
        self._direction = direction

    @property
    def name(self):
        """str: The property name being indexed."""
        return self._name

    @property
    def direction(self):
        """str: The direction in the index, ``asc`` or ``desc``."""
        return self._direction

    def __repr__(self):
        """Return a string representation."""
        return "{}(name={!r}, direction={!r})".format(
            self.__class__.__name__, self.name, self.direction
        )

    def __eq__(self, other):
        """Compare two index properties for equality."""
        if not isinstance(other, IndexProperty):
            return NotImplemented
        return self.name == other.name and self.direction == other.direction

    def __ne__(self, other):
        """Inequality comparison operation."""
        return not self == other

    def __hash__(self):
        return hash((self.name, self.direction))


class Index:
    """Immutable object representing an index."""

    __slots__ = ("_kind", "_properties", "_ancestor")

    def __init__(self, *, kind, properties, ancestor):
        self._kind = kind
        self._properties = properties
        self._ancestor = ancestor

    @property
    def kind(self):
        """str: The kind being indexed."""
        return self._kind

    @property
    def properties(self):
        """List[IndexProperty]: The properties being indexed."""
        return self._properties

    @property
    def ancestor(self):
        """bool: Indicates if this is an ancestor index."""
        return self._ancestor

    def __repr__(self):
        """Return a string representation."""
        return "{}(kind={!r}, properties={!r}, ancestor={})".format(
            self.__class__.__name__, self.kind, self.properties, self.ancestor
        )

    def __eq__(self, other):
        """Compare two indexes."""
        if not isinstance(other, Index):
            return NotImplemented

        return (
            self.kind == other.kind
            and self.properties == other.properties
            and self.ancestor == other.ancestor
        )

    def __ne__(self, other):
        """Inequality comparison operation."""
        return not self == other

    def __hash__(self):
        return hash((self.kind, self.properties, self.ancestor))


class IndexState:
    """Immutable object representing an index and its state."""

    __slots__ = ("_definition", "_state", "_id")

    def __init__(self, *, definition, state, id):
        self._definition = definition
        self._state = state
        self._id = id

    @property
    def definition(self):
        """Index: The index corresponding to the tracked state."""
        return self._definition

    @property
    def state(self):
        """str: The index state.

        Possible values are ``error``, ``deleting``, ``serving`` or
        ``building``.
        """
        return self._state

    @property
    def id(self):
        """int: The index ID."""
        return self._id

    def __repr__(self):
        """Return a string representation."""
        return "{}(definition={!r}, state={!r}, id={:d})".format(
            self.__class__.__name__, self.definition, self.state, self.id
        )

    def __eq__(self, other):
        """Compare two indexes."""
        if not isinstance(other, IndexState):
            return NotImplemented

        return (
            self.definition == other.definition
            and self.state == other.state
            and self.id == other.id
        )

    def __ne__(self, other):
        """Inequality comparison operation."""
        return not self == other

    def __hash__(self):
        return hash((self.definition, self.state, self.id))


class ModelAdapter:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def make_connection(*args, **kwargs):
    raise NotImplementedError


class ModelAttribute:
    """Base for :meth:`_fix_up` implementing classes."""

    def _fix_up(self, cls, code_name):
        """Fix-up property name. To be implemented by subclasses.

        Args:
            cls (type): The model class that owns the property.
            code_name (str): The name of the :class:`Property` being fixed up.
        """


class Property(ModelAttribute):
    # Instance default fallbacks provided by class.
    _name = None
    _indexed = True
    _repeated = False
    _required = False
    _default = None
    _choices = None
    _validator = None
    _verbose_name = None
    _write_empty_list = False
    # Non-public class attributes.
    _CREATION_COUNTER = 0

    def __init__(
        self,
        name=None,
        *,
        indexed=None,
        repeated=None,
        required=None,
        default=None,
        choices=None,
        validator=None,
        verbose_name=None,
        write_empty_list=None
    ):
        # NOTE: These explicitly avoid setting the values so that the
        #       instances will fall back to the class on lookup.
        if name is not None:
            self._name = self._verify_name(name)
        if indexed is not None:
            self._indexed = indexed
        if repeated is not None:
            self._repeated = repeated
        if required is not None:
            self._required = required
        if default is not None:
            self._default = default
        self._verify_repeated()
        if choices is not None:
            self._choices = self._verify_choices(choices)
        if validator is not None:
            self._validator = self._verify_validator(validator)
        if verbose_name is not None:
            self._verbose_name = verbose_name
        if write_empty_list is not None:
            self._write_empty_list = write_empty_list
        # Keep a unique creation counter. Note that this is not threadsafe.
        Property._CREATION_COUNTER += 1
        self._creation_counter = Property._CREATION_COUNTER

    @staticmethod
    def _verify_name(name):
        """Verify the name of the property.

        Args:
            name (Union[str, bytes]): The name of the property.

        Returns:
            bytes: The UTF-8 encoded version of the ``name``, if not already
            passed in as bytes.

        Raises:
            TypeError: If the ``name`` is not a string or bytes.
            ValueError: If the name contains a ``.``.
        """
        if isinstance(name, str):
            name = name.encode("utf-8")

        if not isinstance(name, bytes):
            raise TypeError(
                "Name {!r} is not a string or byte string".format(name)
            )

        if b"." in name:
            raise ValueError(
                "Name {!r} cannot contain period characters".format(name)
            )

        return name

    def _verify_repeated(self):
        """Checks if the repeated / required / default values are compatible.

        Raises:
            ValueError: If ``repeated`` is :data:`True` but one of
                ``required`` or ``default`` is set.
        """
        if self._repeated and (self._required or self._default is not None):
            raise ValueError(
                "repeated is incompatible with required or default"
            )

    @staticmethod
    def _verify_choices(choices):
        """Verify the choices for a property with a limited set of values.

        Args:
            choices (Union[list, tuple, set, frozenset]): An iterable of
                allowed values for the property.

        Returns:
            frozenset: The ``choices`` cast to a frozen set.

        Raises:
            TypeError: If ``choices`` is not one of the expected container
                types.
        """
        if not isinstance(choices, (list, tuple, set, frozenset)):
            raise TypeError(
                "choices must be a list, tuple or set; received {!r}".format(
                    choices
                )
            )
        return frozenset(choices)

    @staticmethod
    def _verify_validator(validator):
        """Verify the validator for a property.

        The validator will be called as follows:

        .. code-block:: python

            value = validator(prop, value)

        The ``validator`` should be idempotent, i.e. calling it a second time
        should not further modify the value. So a validator that returns e.g.
        ``value.lower()`` or ``value.strip()`` is fine, but one that returns
        ``value + "$"`` is not.

        Args:
            validator (Callable[[.Property, Any], bool]): A callable that can
                validate a property value.

        Returns:
            Callable[[.Property, Any], bool]: The ``validator``.

        Raises:
            TypeError: If ``validator`` is not callable. This is determined by
                checking is the attribute ``__call__`` is defined.
        """
        # NOTE: Checking for ``_call__`` is done to match the original
        #       implementation. It's not clear why ``callable()`` was not used.
        if getattr(validator, "__call__", None) is None:
            raise TypeError(
                "validator must be callable or None; received {!r}".format(
                    validator
                )
            )

        return validator


class ModelKey(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BooleanProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class IntegerProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class FloatProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BlobProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TextProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class StringProperty(TextProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GeoPtProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class PickleProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class JsonProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class UserProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KeyProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BlobKeyProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateTimeProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateProperty(DateTimeProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TimeProperty(DateTimeProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class StructuredProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class LocalStructuredProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GenericProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ComputedProperty(GenericProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class MetaModel(type):
    def __new__(self, *args, **kwargs):
        raise NotImplementedError


class Model:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def _get_kind(cls):
        """Return the kind name for this class.

        This defaults to ``cls.__name__``; users may override this to give a
        class a different name when stored in Google Cloud Datastore than the
        name of the class.
        """
        return cls.__name__


class Expando(Model):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def transaction(*args, **kwargs):
    raise NotImplementedError


def transaction_async(*args, **kwargs):
    raise NotImplementedError


def in_transaction(*args, **kwargs):
    raise NotImplementedError


def transactional(*args, **kwargs):
    raise NotImplementedError


def transactional_async(*args, **kwargs):
    raise NotImplementedError


def transactional_tasklet(*args, **kwargs):
    raise NotImplementedError


def non_transactional(*args, **kwargs):
    raise NotImplementedError


def get_multi_async(*args, **kwargs):
    raise NotImplementedError


def get_multi(*args, **kwargs):
    raise NotImplementedError


def put_multi_async(*args, **kwargs):
    raise NotImplementedError


def put_multi(*args, **kwargs):
    raise NotImplementedError


def delete_multi_async(*args, **kwargs):
    raise NotImplementedError


def delete_multi(*args, **kwargs):
    raise NotImplementedError


def get_indexes_async(*args, **kwargs):
    raise NotImplementedError


def get_indexes(*args, **kwargs):
    raise NotImplementedError
