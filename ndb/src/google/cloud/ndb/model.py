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


import inspect

from google.cloud.ndb import exceptions
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
Rollback = exceptions.Rollback


class KindError(exceptions.BadValueError):
    """Raised when an implementation for a kind can't be found.

    May also be raised when the kind is not a byte string.
    """


class InvalidPropertyError(exceptions.Error):
    """Raised when a property is not applicable to a given use.

    For example, a property must exist and be indexed to be used in a query's
    projection or group by clause.
    """


BadProjectionError = InvalidPropertyError
"""This alias for :class:`InvalidPropertyError` is for legacy support."""


class UnprojectedPropertyError(exceptions.Error):
    """Raised when getting a property value that's not in the projection."""


class ReadonlyPropertyError(exceptions.Error):
    """Raised when attempting to set a property value that is read-only."""


class ComputedPropertyError(ReadonlyPropertyError):
    """Raised when attempting to set or delete a computed property."""


class IndexProperty:
    """Immutable object representing a single property in an index."""

    __slots__ = ("_name", "_direction")

    def __new__(cls, *, name, direction):
        instance = super(IndexProperty, cls).__new__(cls)
        instance._name = name
        instance._direction = direction
        return instance

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

    def __new__(cls, *, kind, properties, ancestor):
        instance = super(Index, cls).__new__(cls)
        instance._kind = kind
        instance._properties = properties
        instance._ancestor = ancestor
        return instance

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

    def __new__(cls, *, definition, state, id):
        instance = super(IndexState, cls).__new__(cls)
        instance._definition = definition
        instance._state = state
        instance._id = id
        return instance

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
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def make_connection(*args, **kwargs):
    raise NotImplementedError


class ModelAttribute:
    """Base for classes that implement a ``_fix_up()`` method."""

    __slots__ = ()

    def _fix_up(self, cls, code_name):
        """Fix-up property name. To be implemented by subclasses.

        Args:
            cls (type): The model class that owns the property.
            code_name (str): The name of the :class:`Property` being fixed up.
        """


class _BaseValue:
    """A marker object wrapping a "base type" value.

    This is used to be able to tell whether ``entity._values[name]`` is a
    user value (i.e. of a type that the Python code understands) or a
    base value (i.e of a type that serialization understands).
    User values are unwrapped; base values are wrapped in a
    :class:`_BaseValue` instance.

    Args:
        b_val (Any): The base value to be wrapped.

    Raises:
        TypeError: If ``b_val`` is :data:`None`.
        TypeError: If ``b_val`` is a list.
    """

    __slots__ = ("b_val",)

    def __init__(self, b_val):
        if b_val is None:
            raise TypeError("Cannot wrap None")
        if isinstance(b_val, list):
            raise TypeError("Lists cannot be wrapped. Received", b_val)
        self.b_val = b_val

    def __repr__(self):
        return "_BaseValue({!r})".format(self.b_val)

    def __eq__(self, other):
        """Compare two :class:`_BaseValue` instances."""
        if not isinstance(other, _BaseValue):
            return NotImplemented

        return self.b_val == other.b_val

    def __ne__(self, other):
        """Inequality comparison operation."""
        return not self == other

    def __hash__(self):
        raise TypeError("_BaseValue is not immutable")


class Property(ModelAttribute):
    # Instance default fallbacks provided by class.
    _code_name = None
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
    _FIND_METHODS_CACHE = {}

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

    def __repr__(self):
        """Return a compact unambiguous string representation of a property.

        This cycles through all stored attributes and displays the ones that
        differ from the default values.
        """
        args = []
        cls = self.__class__
        signature = inspect.signature(self.__init__)
        for name, parameter in signature.parameters.items():
            attr = "_{}".format(name)
            instance_val = getattr(self, attr)
            default_val = getattr(cls, attr)

            if instance_val is not default_val:
                if isinstance(instance_val, type):
                    as_str = instance_val.__qualname__
                else:
                    as_str = repr(instance_val)

                if parameter.kind == inspect.Parameter.KEYWORD_ONLY:
                    as_str = "{}={}".format(name, as_str)
                args.append(as_str)

        return "{}({})".format(self.__class__.__name__, ", ".join(args))

    def _datastore_type(self, value):
        """Internal hook used by property filters.

        Sometimes the low-level query interface needs a specific data type
        in order for the right filter to be constructed. See
        :meth:`_comparison`.

        Args:
            value (Any): The value to be converted to a low-level type.

        Returns:
            Any: The passed-in ``value``, always. Subclasses may alter this
            behavior.
        """
        return value

    def _comparison(self, op, value):
        """Internal helper for comparison operators.

        Args:
            op (str): The comparison operator. One of ``=``, ``!=``, ``<``,
                ``<=``, ``>``, ``>=`` or ``in``.

        Returns:
            FilterNode: A FilterNode instance representing the requested
            comparison.

        Raises:
            BadFilterError: If the current property is not indexed.
        """
        # Import late to avoid circular imports.
        from google.cloud.ndb import query

        if not self._indexed:
            raise exceptions.BadFilterError(
                "Cannot query for unindexed property {}".format(self._name)
            )

        if value is not None:
            value = self._do_validate(value)
            value = self._call_to_base_type(value)
            value = self._datastore_type(value)

        return query.FilterNode(self._name, op, value)

    # Comparison operators on Property instances don't compare the
    # properties; instead they return ``FilterNode``` instances that can be
    # used in queries.

    def __eq__(self, value):
        """FilterNode: Represents the ``=`` comparison."""
        return self._comparison("=", value)

    def __ne__(self, value):
        """FilterNode: Represents the ``!=`` comparison."""
        return self._comparison("!=", value)

    def __lt__(self, value):
        """FilterNode: Represents the ``<`` comparison."""
        return self._comparison("<", value)

    def __le__(self, value):
        """FilterNode: Represents the ``<=`` comparison."""
        return self._comparison("<=", value)

    def __gt__(self, value):
        """FilterNode: Represents the ``>`` comparison."""
        return self._comparison(">", value)

    def __ge__(self, value):
        """FilterNode: Represents the ``>=`` comparison."""
        return self._comparison(">=", value)

    def _IN(self, value):
        """For the ``in`` comparison operator.

        The ``in`` operator cannot be overloaded in the way we want
        to, so we define a method. For example:

        .. code-block:: python

            Employee.query(Employee.rank.IN([4, 5, 6]))

        Note that the method is called ``_IN()`` but may normally be invoked
        as ``IN()``; ``_IN()`` is provided for the case that a
        :class:`.StructuredProperty` refers to a model that has a property
        named ``IN``.

        Args:
            value (Iterable[Any]): The set of values that the property value
                must be contained in.

        Returns:
            Union[~google.cloud.ndb.query.DisjunctionNode, \
                ~google.cloud.ndb.query.FilterNode, \
                ~google.cloud.ndb.query.FalseNode]: A node corresponding
            to the desired in filter.

            * If ``value`` is empty, this will return a :class:`.FalseNode`
            * If ``len(value) == 1``, this will return a :class:`.FilterNode`
            * Otherwise, this will return a :class:`.DisjunctionNode`

        Raises:
            ~google.cloud.ndb.exceptions.BadFilterError: If the current
                property is not indexed.
            ~google.cloud.ndb.exceptions.BadArgumentError: If ``value`` is not
                a basic container (:class:`list`, :class:`tuple`, :class:`set`
                or :class:`frozenset`).
        """
        # Import late to avoid circular imports.
        from google.cloud.ndb import query

        if not self._indexed:
            raise exceptions.BadFilterError(
                "Cannot query for unindexed property {}".format(self._name)
            )

        if not isinstance(value, (list, tuple, set, frozenset)):
            raise exceptions.BadArgumentError(
                "Expected list, tuple or set, got {!r}".format(value)
            )

        values = []
        for sub_value in value:
            if sub_value is not None:
                sub_value = self._do_validate(sub_value)
                sub_value = self._call_to_base_type(sub_value)
                sub_value = self._datastore_type(sub_value)
            values.append(sub_value)

        return query.FilterNode(self._name, "in", values)

    IN = _IN
    """Used to check if a property value is contained in a set of values.

    For example:

    .. code-block:: python

        Employee.query(Employee.rank.IN([4, 5, 6]))
    """

    def __neg__(self):
        """Return a descending sort order on this property.

        For example:

        .. code-block:: python

            Employee.query().order(-Employee.rank)

        Raises:
            NotImplementedError: Always, the original implementation relied on
                a low-level datastore query module.
        """
        raise NotImplementedError("Missing datastore_query.PropertyOrder")

    def __pos__(self):
        """Return an ascending sort order on this property.

        Note that this is redundant but provided for consistency with
        :meth:`__neg__`. For example, the following two are equivalent:

        .. code-block:: python

            Employee.query().order(+Employee.rank)
            Employee.query().order(Employee.rank)

        Raises:
            NotImplementedError: Always, the original implementation relied on
                a low-level datastore query module.
        """
        raise NotImplementedError("Missing datastore_query.PropertyOrder")

    def _do_validate(self, value):
        """Call all validations on the value.

        This transforms the ``value`` via:

        * Calling the derived ``_validate()`` method(s) (on subclasses that
          don't define ``_to_base_type``),
        * Calling the custom validator function

        After transforming, it checks if the transformed value is in
        ``choices`` (if defined).

        It's possible that one of the ``_validate()`` methods will raise
        an exception.

        If ``value`` is a base-value, this will do nothing and return it.

        .. note::

            This does not call all composable ``_validate()`` methods.
            It only calls ``_validate()`` methods up to the
            first class in the hierarchy that defines a ``_to_base_type()``
            method, when the MRO is traversed looking for ``_validate()`` and
            ``_to_base_type()`` methods.

        .. note::

            For a repeated property this method should be called
            for each value in the list, not for the list as a whole.

        Args:
            value (Any): The value to be converted / validated.

        Returns:
            Any: The transformed ``value``, possibly modified in an idempotent
            way.
        """
        if isinstance(value, _BaseValue):
            return value

        value = self._call_shallow_validation(value)

        if self._validator is not None:
            new_value = self._validator(self, value)
            if new_value is not None:
                value = new_value

        if self._choices is not None:
            if value not in self._choices:
                raise exceptions.BadValueError(
                    "Value {!r} for property {} is not an allowed "
                    "choice".format(value, self._name)
                )

        return value

    def _fix_up(self, cls, code_name):
        """Internal helper called to tell the property its name.

        This is called by :meth:`_fix_up_properties`, which is called by
        :class:`MetaModel` when finishing the construction of a :class:`Model`
        subclass. The name passed in is the name of the class attribute to
        which the current property is assigned (a.k.a. the code name). Note
        that this means that each property instance must be assigned to (at
        most) one class attribute. E.g. to declare three strings, you must
        call create three :class`StringProperty` instances:

        .. code-block:: python

            class MyModel(ndb.Model):
                foo = ndb.StringProperty()
                bar = ndb.StringProperty()
                baz = ndb.StringProperty()

        you cannot write:

        .. code-block:: python

            class MyModel(ndb.Model):
                foo = bar = baz = ndb.StringProperty()

        Args:
            cls (type): The class that the property is stored on. This argument
                is unused by this method, but may be used by subclasses.
            code_name (str): The name (on the class) that refers to this
                property.
        """
        self._code_name = code_name
        if self._name is None:
            self._name = code_name

    def _store_value(self, entity, value):
        """Store a value in an entity for this property.

        This assumes validation has already taken place. For a repeated
        property the value should be a list.

        Args:
            entity (Model): An entity to set a value on.
            value (Any): The value to be stored for this property.
        """
        entity._values[self._name] = value

    def _set_value(self, entity, value):
        """Set a value in an entity for a property.

        This performs validation first. For a repeated property the value
        should be a list (or similar container).

        Args:
            entity (Model): An entity to set a value on.
            value (Any): The value to be stored for this property.

        Raises:
            ReadonlyPropertyError: If the ``entity`` is the result of a
                projection query.
            .BadValueError: If the current property is repeated but the
                ``value`` is not a basic container (:class:`list`,
                :class:`tuple`, :class:`set` or :class:`frozenset`).
        """
        if entity._projection:
            raise ReadonlyPropertyError(
                "You cannot set property values of a projection entity"
            )

        if self._repeated:
            if not isinstance(value, (list, tuple, set, frozenset)):
                raise exceptions.BadValueError(
                    "Expected list or tuple, got {!r}".format(value)
                )
            value = [self._do_validate(v) for v in value]
        else:
            if value is not None:
                value = self._do_validate(value)

        self._store_value(entity, value)

    def _has_value(self, entity, unused_rest=None):
        """Determine if the entity has a value for this property.

        Args:
            entity (Model): An entity to check if the current property has
                a value set.
            unused_rest (None): An always unused keyword.
        """
        return self._name in entity._values

    def _retrieve_value(self, entity, default=None):
        """Retrieve the value for this property from an entity.

        This returns :data:`None` if no value is set, or the ``default``
        argument if given. For a repeated property this returns a list if a
        value is set, otherwise :data:`None`. No additional transformations
        are applied.

        Args:
            entity (Model): An entity to get a value from.
            default (Optional[Any]): The default value to use as fallback.
        """
        return entity._values.get(self._name, default)

    def _get_user_value(self, entity):
        """Return the user value for this property of the given entity.

        This implies removing the :class:`_BaseValue` wrapper if present, and
        if it is, calling all ``_from_base_type()`` methods, in the reverse
        method resolution order of the property's class. It also handles
        default values and repeated properties.

        Args:
            entity (Model): An entity to get a value from.

        Returns:
            Any: The original value (if not :class:`_BaseValue`) or the wrapped
            value converted from the base type.
        """
        return self._apply_to_values(entity, self._opt_call_from_base_type)

    def _get_base_value(self, entity):
        """Return the base value for this property of the given entity.

        This implies calling all ``_to_base_type()`` methods, in the method
        resolution order of the property's class, and adding a
        :class:`_BaseValue` wrapper, if one is not already present. (If one
        is present, no work is done.)  It also handles default values and
        repeated properties.

        Args:
            entity (Model): An entity to get a value from.

        Returns:
            Union[_BaseValue, List[_BaseValue]]: The original value
            (if :class:`_BaseValue`) or the value converted to the base type
            and wrapped.
        """
        return self._apply_to_values(entity, self._opt_call_to_base_type)

    def _opt_call_from_base_type(self, value):
        """Call :meth:`_from_base_type` if necessary.

        If ``value`` is a :class:`_BaseValue`, unwrap it and call all
        :math:`_from_base_type` methods. Otherwise, return the value
        unchanged.

        Args:
            value (Any): The value to invoke :meth:`_call_from_base_type`
               for.

        Returns:
            Any: The original value (if not :class:`_BaseValue`) or the value
            converted from the base type.
        """
        if isinstance(value, _BaseValue):
            value = self._call_from_base_type(value.b_val)
        return value

    def _value_to_repr(self, value):
        """Turn a value (base or not) into its repr().

        This exists so that property classes can override it separately.

        This manually applies ``_from_base_type()`` so as not to have a side
        effect on what's contained in the entity. Printing a value should not
        change it.

        Args:
            value (Any): The value to convert to a pretty-print ``repr``.

        Returns:
            str: The ``repr`` of the "true" value.
        """
        val = self._opt_call_from_base_type(value)
        return repr(val)

    def _opt_call_to_base_type(self, value):
        """Call :meth:`_to_base_type` if necessary.

        If ``value`` is a :class:`_BaseValue`, return it unchanged.
        Otherwise, call all :meth:`_validate` and :meth:`_to_base_type` methods
        and wrap it in a :class:`_BaseValue`.

        Args:
            value (Any): The value to invoke :meth:`_call_to_base_type`
               for.

        Returns:
            _BaseValue: The original value (if :class:`_BaseValue`) or the
            value converted to the base type and wrapped.
        """
        if not isinstance(value, _BaseValue):
            value = _BaseValue(self._call_to_base_type(value))
        return value

    def _call_from_base_type(self, value):
        """Call all ``_from_base_type()`` methods on the value.

        This calls the methods in the reverse method resolution order of
        the property's class.

        Args:
            value (Any): The value to be converted.

        Returns:
            Any: The transformed ``value``.
        """
        methods = self._find_methods("_from_base_type", reverse=True)
        call = self._apply_list(methods)
        return call(value)

    def _call_to_base_type(self, value):
        """Call all ``_validate()`` and ``_to_base_type()`` methods on value.

        This calls the methods in the method resolution order of the
        property's class. For example, given the hierarchy

        .. code-block:: python

            class A(Property):
                def _validate(self, value):
                    ...
                def _to_base_type(self, value):
                    ...

            class B(A):
                def _validate(self, value):
                    ...
                def _to_base_type(self, value):
                    ...

            class C(B):
                def _validate(self, value):
                    ...

        the full list of methods (in order) is:

        * ``C._validate()``
        * ``B._validate()``
        * ``B._to_base_type()``
        * ``A._validate()``
        * ``A._to_base_type()``

        Args:
            value (Any): The value to be converted / validated.

        Returns:
            Any: The transformed ``value``.
        """
        methods = self._find_methods("_validate", "_to_base_type")
        call = self._apply_list(methods)
        return call(value)

    def _call_shallow_validation(self, value):
        """Call the "initial" set of ``_validate()`` methods.

        This is similar to :meth:`_call_to_base_type` except it only calls
        those ``_validate()`` methods that can be called without needing to
        call ``_to_base_type()``.

        An example: suppose the class hierarchy is

        .. code-block:: python

            class A(Property):
                def _validate(self, value):
                    ...
                def _to_base_type(self, value):
                    ...

            class B(A):
                def _validate(self, value):
                    ...
                def _to_base_type(self, value):
                    ...

            class C(B):
                def _validate(self, value):
                    ...

        The full list of methods (in order) called by
        :meth:`_call_to_base_type` is:

        * ``C._validate()``
        * ``B._validate()``
        * ``B._to_base_type()``
        * ``A._validate()``
        * ``A._to_base_type()``

        whereas the full list of methods (in order) called here stops once
        a ``_to_base_type`` method is encountered:

        * ``C._validate()``
        * ``B._validate()``

        Args:
            value (Any): The value to be converted / validated.

        Returns:
            Any: The transformed ``value``.
        """
        methods = []
        for method in self._find_methods("_validate", "_to_base_type"):
            # Stop if ``_to_base_type`` is encountered.
            if method.__name__ != "_validate":
                break
            methods.append(method)

        call = self._apply_list(methods)
        return call(value)

    @classmethod
    def _find_methods(cls, *names, reverse=False):
        """Compute a list of composable methods.

        Because this is a common operation and the class hierarchy is
        static, the outcome is cached (assuming that for a particular list
        of names the reversed flag is either always on, or always off).

        Args:
            names (Tuple[str, ...]): One or more method names to look up on
                the current class or base classes.
            reverse (bool): Optional flag, default False; if True, the list is
              reversed.

        Returns:
            List[Callable]: Class method objects.
        """
        # Get cache on current class / set cache if it doesn't exist.
        key = "{}.{}".format(cls.__module__, cls.__qualname__)
        cache = cls._FIND_METHODS_CACHE.setdefault(key, {})
        hit = cache.get(names)
        if hit is not None:
            if reverse:
                return list(reversed(hit))
            else:
                return hit

        methods = []
        for klass in cls.__mro__:
            for name in names:
                method = klass.__dict__.get(name)
                if method is not None:
                    methods.append(method)

        cache[names] = methods
        if reverse:
            return list(reversed(methods))
        else:
            return methods

    def _apply_list(self, methods):
        """Chain together a list of callables for transforming a value.

        .. note::

            Each callable in ``methods`` is an unbound instance method, e.g.
            accessed via ``Property.foo`` rather than ``instance.foo``.
            Therefore, calling these methods will require ``self`` as the
            first argument.

        If one of the method returns :data:`None`, the previous value is kept;
        otherwise the last value is replace.

        Exceptions thrown by a method in ``methods`` are not caught, so it
        is up to the caller to catch them.

        Args:
            methods (Iterable[Callable[[Any], Any]]): An iterable of methods
                to apply to a value.

        Returns:
            Callable[[Any], Any]: A callable that takes a single value and
            applies each method in ``methods`` to it.
        """

        def call(value):
            for method in methods:
                new_value = method(self, value)
                if new_value is not None:
                    value = new_value
            return value

        return call

    def _apply_to_values(self, entity, function):
        """Apply a function to the property value / values of a given entity.

        This retrieves the property value, applies the function, and then
        stores the value back. For a repeated property, the function is
        applied separately to each of the values in the list. The
        resulting value or list of values is both stored back in the
        entity and returned from this method.

        Args:
            entity (Model): An entity to get a value from.
            function (Callable[[Any], Any]): A transformation to apply to
                the value.

        Returns:
            Any: The transformed value store on the entity for this property.
        """
        value = self._retrieve_value(entity, self._default)
        if self._repeated:
            if value is None:
                value = []
                self._store_value(entity, value)
            else:
                # NOTE: This assumes, but does not check, that ``value`` is
                #       iterable. This relies on ``_set_value`` having checked
                #       and converted to a ``list`` for a repeated property.
                value[:] = map(function, value)
        else:
            if value is not None:
                new_value = function(value)
                if new_value is not None and new_value is not value:
                    self._store_value(entity, new_value)
                    value = new_value

        return value


class ModelKey(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BooleanProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class IntegerProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class FloatProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BlobProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TextProperty(BlobProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class StringProperty(TextProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GeoPtProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class PickleProperty(BlobProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class JsonProperty(BlobProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class UserProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KeyProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BlobKeyProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateTimeProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateProperty(DateTimeProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TimeProperty(DateTimeProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class StructuredProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class LocalStructuredProperty(BlobProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GenericProperty(Property):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ComputedProperty(GenericProperty):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class MetaModel(type):
    __slots__ = ()

    def __new__(self, *args, **kwargs):
        raise NotImplementedError


class Model:
    __slots__ = ()

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
    __slots__ = ()

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
