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

"""Provides a :class:`.Key` for Google Cloud Datastore.

.. testsetup:: *

    from google.cloud import ndb

A key encapsulates the following pieces of information, which together
uniquely designate a (possible) entity in Google Cloud Datastore:

* a Google Cloud Platform project (a string)
* a list of one or more ``(kind, id)`` pairs where ``kind`` is a string
  and ``id`` is either a string or an integer
* an optional namespace (a string)
"""


import base64
import os

from google.cloud.datastore import _app_engine_key_pb2
from google.cloud.datastore import key as _key_module
import google.cloud.datastore


__all__ = ["Key"]
_APP_ID_ENVIRONMENT = "APPLICATION_ID"
_APP_ID_DEFAULT = "_"
_WRONG_TYPE = "Cannot construct Key reference on non-Key class; received {!r}"
_REFERENCE_APP_MISMATCH = (
    "Key reference constructed uses a different app {!r} than "
    "the one specified {!r}"
)
_REFERENCE_NAMESPACE_MISMATCH = (
    "Key reference constructed uses a different namespace {!r} than "
    "the one specified {!r}"
)
_INVALID_ID_TYPE = "Key id must be a string or a number; received {!r}"


class _BadArgumentError(Exception):
    """Placeholder exception for ``datastore_errors.BadArgumentError``."""


class _BadValueError(Exception):
    """Placeholder exception for ``datastore_errors.BadValueError``."""


class Key:
    """An immutable datastore key.

    For flexibility and convenience, multiple constructor signatures are
    supported.

    The primary way to construct a key is using positional arguments:

    .. testsetup:: *

        kind1, id1 = "Parent", "C"
        kind2, id2 = "Child", 42

    .. doctest:: key-constructor-primary

        >>> ndb.Key(kind1, id1, kind2, id2)
        Key('Parent', 'C', 'Child', 42)

    This is shorthand for either of the following two longer forms:

    .. doctest:: key-constructor-flat-or-pairs

        >>> ndb.Key(pairs=[(kind1, id1), (kind2, id2)])
        Key('Parent', 'C', 'Child', 42)
        >>> ndb.Key(flat=[kind1, id1, kind2, id2])
        Key('Parent', 'C', 'Child', 42)

    Either of the above constructor forms can additionally pass in another
    key using ``parent=<key>``. The ``(kind, id)`` pairs of the parent key are
    inserted before the ``(kind, id)`` pairs passed explicitly.

    .. doctest:: key-constructor-parent

        >>> parent = ndb.Key(kind1, id1)
        >>> parent
        Key('Parent', 'C')
        >>> ndb.Key(kind2, id2, parent=parent)
        Key('Parent', 'C', 'Child', 42)

    You can also construct a Key from a "url-safe" encoded string:

    .. doctest:: key-constructor-urlsafe

        >>> ndb.Key(urlsafe=b"agdleGFtcGxlcgsLEgRLaW5kGLkKDA")
        Key('Kind', 1337, app='example')

    For rare use cases the following constructors exist:

    .. testsetup:: key-constructor-rare

        from google.cloud.datastore import _app_engine_key_pb2
        reference = _app_engine_key_pb2.Reference(
            app="example",
            path=_app_engine_key_pb2.Path(element=[
                _app_engine_key_pb2.Path.Element(type="Kind", id=1337),
            ]),
        )

    .. doctest:: key-constructor-rare

        >>> # Passing in a low-level Reference object
        >>> reference
        app: "example"
        path {
          Element {
            type: "Kind"
            id: 1337
          }
        }
        <BLANKLINE>
        >>> ndb.Key(reference=reference)
        Key('Kind', 1337, app='example')
        >>> # Passing in a serialized low-level Reference
        >>> serialized = reference.SerializeToString()
        >>> serialized
        b'j\\x07exampler\\x0b\\x0b\\x12\\x04Kind\\x18\\xb9\\n\\x0c'
        >>> ndb.Key(serialized=serialized)
        Key('Kind', 1337, app='example')
        >>> # For unpickling, the same as ndb.Key(**kwargs)
        >>> kwargs = {"pairs": [("Cheese", "Cheddar")], "namespace": "good"}
        >>> ndb.Key(kwargs)
        Key('Cheese', 'Cheddar', namespace='good')

    The "url-safe" string is really a websafe-base64-encoded serialized
    ``Reference``, but it's best to think of it as just an opaque unique
    string.

    If a ``Reference`` is passed (using one of the ``reference``,
    ``serialized`` or ``urlsafe`` keywords), the positional arguments and
    ``namespace`` must match what is already present in the ``Reference``
    (after decoding if necessary). The parent keyword cannot be combined with
    a ``Reference`` in any form.

    Keys are immutable, which means that a Key object cannot be modified
    once it has been created. This is enforced by the implementation as
    well as Python allows.

    For access to the contents of a key, the following methods and
    operations are supported:

    * ``key1 == key2``, ``key1 != key2``: comparison for equality between keys
    * ``hash(key)``: a hash value sufficient for storing keys in a dictionary
    * ``key.urlsafe()``: a websafe-base64-encoded serialized ``Reference``
    * ``key.serialized()``: a serialized ``Reference``
    * ``key.reference()``: a ``Reference`` object (the caller promises not to
      mutate it)

    Keys also support interaction with the datastore; these methods are
    the only ones that engage in any kind of I/O activity. For ``Future``
    objects, see the documentation for :mod:`google.cloud.ndb.tasklets`.

    * ``key.get()``: return the entity for the key
    * ``key.get_async()``: return a future whose eventual result is
      the entity for the key
    * ``key.delete()``: delete the entity for the key
    * ``key.delete_async()``: asynchronously delete the entity for the key

    Keys may be pickled.

    Subclassing Key is best avoided; it would be hard to get right.

    Args:
        path_args (Union[Tuple[str, ...], Tuple[Dict]]): Either a tuple of
            ``(kind, id)`` pairs or a single dictionary containing only keyword
            arguments.
        reference (Optional[\
            ~google.cloud.datastore._app_engine_key_pb2.Reference]): A
            reference protobuf representing a key.
        serialized (Optional[bytes]): A reference protobuf serialized to bytes.
        urlsafe (Optional[str]): A reference protobuf serialized to bytes. The
            raw bytes are then converted to a websafe base64-encoded string.
        pairs (Optional[Iterable[Tuple[str, Union[str, int]]]]): An iterable
            of ``(kind, id)`` pairs. If this argument is used, then
            ``path_args`` should be empty.
        flat (Optional[Iterable[Union[str, int]]]): An iterable of the
            ``(kind, id)`` pairs but flattened into a single value. For
            example, the pairs ``[("Parent", 1), ("Child", "a")]`` would be
            flattened to ``["Parent", 1, "Child", "a"]``.
        app (Optional[str]): The Google Cloud Platform project (previously
            on Google App Engine, this was called the Application ID).
        namespace (Optional[str]): The namespace for the key.
        parent (Optional[Key]): The parent of the key being
            constructed. If provided, the key path will be **relative** to the
            parent key's path.

    Raises:
        TypeError: If none of ``reference``, ``serialized``, ``urlsafe``,
            ``pairs`` or ``flat`` is provided as an argument and no positional
            arguments were given with the path.
    """

    __slots__ = ("_key", "_reference")

    def __init__(self, *path_args, **kwargs):
        _constructor_handle_positional(path_args, kwargs)
        if (
            "reference" in kwargs
            or "serialized" in kwargs
            or "urlsafe" in kwargs
        ):
            ds_key, reference = _parse_from_ref(type(self), **kwargs)
        elif "pairs" in kwargs or "flat" in kwargs:
            ds_key = _parse_from_args(**kwargs)
            reference = None
        else:
            raise TypeError(
                "Key() cannot create a Key instance without arguments."
            )

        self._key = ds_key
        self._reference = reference

    @classmethod
    def _from_ds_key(cls, ds_key):
        """Factory constructor for a :class:`~google.cloud.datastore.key.Key`.

        This bypasses the actual constructor and directly sets the ``_key``
        attribute to ``ds_key``.

        Args:
            ds_key (~google.cloud.datastore.key.Key): A key from
                ``google-cloud-datastore``.

        Returns:
            Key: The constructed :class:`Key`.
        """
        key = cls.__new__(cls)
        key._key = ds_key
        key._reference = None
        return key

    def __repr__(self):
        """String representation used by :class:`str() <str>` and :func:`repr`.

        We produce a short string that conveys all relevant information,
        suppressing app and namespace when they are equal to the default.
        In many cases, this string should be able to be used to invoke the
        constructor.

        For example:

        .. doctest:: key-repr

            >>> key = ndb.Key("hi", 100)
            >>> repr(key)
            "Key('hi', 100)"
            >>>
            >>> key = ndb.Key(
            ...     "bye", "hundred", app="specific", namespace="space"
            ... )
            >>> str(key)
            "Key('bye', 'hundred', app='specific', namespace='space')"
        """
        args = ["{!r}".format(item) for item in self.flat()]
        if self.app() != _project_from_app(None):
            args.append("app={!r}".format(self.app()))
        if self.namespace() is not None:
            args.append("namespace={!r}".format(self.namespace()))

        return "Key({})".format(", ".join(args))

    def __str__(self):
        """Alias for :meth:`__repr__`."""
        return self.__repr__()

    def parent(self):
        """Parent key constructed from all but the last ``(kind, id)`` pairs.

        If there is only one ``(kind, id)`` pair, return :data:`None`.

        .. doctest:: key-parent

            >>> key = ndb.Key(
            ...     pairs=[
            ...         ("Purchase", "Food"),
            ...         ("Type", "Drink"),
            ...         ("Coffee", 11),
            ...     ]
            ... )
            >>> parent = key.parent()
            >>> parent
            Key('Purchase', 'Food', 'Type', 'Drink')
            >>>
            >>> grandparent = parent.parent()
            >>> grandparent
            Key('Purchase', 'Food')
            >>>
            >>> grandparent.parent() is None
            True
        """
        if self._key.parent is None:
            return None
        return Key._from_ds_key(self._key.parent)

    def root(self):
        """The root key.

        This is either the current key or the highest parent.

        .. doctest:: key-root

            >>> key = ndb.Key("a", 1, "steak", "sauce")
            >>> root_key = key.root()
            >>> root_key
            Key('a', 1)
            >>> root_key.root() is root_key
            True
        """
        root_key = self._key
        while root_key.parent is not None:
            root_key = root_key.parent

        if root_key is self._key:
            return self

        return Key._from_ds_key(root_key)

    def namespace(self):
        """The namespace for the key, if set.

        .. doctest:: key-namespace

            >>> key = ndb.Key("A", "B")
            >>> key.namespace() is None
            True
            >>>
            >>> key = ndb.Key("A", "B", namespace="rock")
            >>> key.namespace()
            'rock'
        """
        return self._key.namespace

    def app(self):
        """The project ID for the key.

        .. warning::

            This **may** differ from the original ``app`` passed in to the
            constructor. This is because prefixed application IDs like
            ``s~example`` are "legacy" identifiers from Google App Engine.
            They have been replaced by equivalent project IDs, e.g. here it
            would be ``example``.

        .. doctest:: key-app

            >>> key = ndb.Key("A", "B", app="s~example")
            >>> key.app()
            'example'
            >>>
            >>> key = ndb.Key("A", "B", app="example")
            >>> key.app()
            'example'
        """
        return self._key.project

    def id(self):
        """The string or integer ID in the last ``(kind, id)`` pair, if any.

        .. doctest:: key-id

            >>> key_int = ndb.Key("A", 37)
            >>> key_int.id()
            37
            >>> key_str = ndb.Key("A", "B")
            >>> key_str.id()
            'B'
            >>> key_partial = ndb.Key("A", None)
            >>> key_partial.id() is None
            True
        """
        return self._key.id_or_name

    def string_id(self):
        """The string ID in the last ``(kind, id)`` pair, if any.

        .. doctest:: key-string-id

            >>> key_int = ndb.Key("A", 37)
            >>> key_int.string_id() is None
            True
            >>> key_str = ndb.Key("A", "B")
            >>> key_str.string_id()
            'B'
            >>> key_partial = ndb.Key("A", None)
            >>> key_partial.string_id() is None
            True
        """
        return self._key.name

    def integer_id(self):
        """The string ID in the last ``(kind, id)`` pair, if any.

        .. doctest:: key-integer-id

            >>> key_int = ndb.Key("A", 37)
            >>> key_int.integer_id()
            37
            >>> key_str = ndb.Key("A", "B")
            >>> key_str.integer_id() is None
            True
            >>> key_partial = ndb.Key("A", None)
            >>> key_partial.integer_id() is None
            True
        """
        return self._key.id

    def pairs(self):
        """The ``(kind, id)`` pairs for the key.

        .. doctest:: key-pairs

            >>> key = ndb.Key("Satellite", "Moon", "Space", "Dust")
            >>> key.pairs()
            [('Satellite', 'Moon'), ('Space', 'Dust')]
            >>>
            >>> partial_key = ndb.Key("Known", None)
            >>> partial_key.pairs()
            [('Known', None)]
        """
        flat = self.flat()
        pairs = []
        for i in range(0, len(flat), 2):
            pairs.append(flat[i : i + 2])
        return pairs

    def flat(self):
        """The flat path for the key.

        .. doctest:: key-flat

            >>> key = ndb.Key("Satellite", "Moon", "Space", "Dust")
            >>> key.flat()
            ('Satellite', 'Moon', 'Space', 'Dust')
            >>>
            >>> partial_key = ndb.Key("Known", None)
            >>> partial_key.flat()
            ('Known', None)
        """
        flat_path = self._key.flat_path
        if len(flat_path) % 2 == 1:
            flat_path += (None,)
        return flat_path

    def kind(self):
        """The kind of the entity referenced.

        This comes from the last ``(kind, id)`` pair.

        .. doctest:: key-kind

            >>> key = ndb.Key("Satellite", "Moon", "Space", "Dust")
            >>> key.kind()
            'Space'
            >>>
            >>> partial_key = ndb.Key("Known", None)
            >>> partial_key.kind()
            'Known'
        """
        return self._key.kind


def _project_from_app(app, allow_empty=False):
    """Convert a legacy Google App Engine app string to a project.

    Args:
        app (str): The application value to be used. If the caller passes
            :data:`None` then this will use the ``APPLICATION_ID`` environment
            variable to determine the running application.
        allow_empty (bool): Flag determining if an empty (i.e. :data:`None`)
            project is allowed. Defaults to :data:`False`.

    Returns:
        str: The cleaned project.
    """
    if app is None:
        if allow_empty:
            return None
        app = os.environ.get(_APP_ID_ENVIRONMENT, _APP_ID_DEFAULT)

    # NOTE: This is the same behavior as in the helper
    #       ``google.cloud.datastore.key._clean_app()``.
    parts = app.split("~", 1)
    return parts[-1]


def _from_reference(reference, app, namespace):
    """Convert Reference protobuf to :class:`~google.cloud.datastore.key.Key`.

    This is intended to work with the "legacy" representation of a
    datastore "Key" used within Google App Engine (a so-called
    "Reference"). This assumes that ``serialized`` was created within an App
    Engine app via something like ``ndb.Key(...).reference()``.

    However, the actual type used here is different since this code will not
    run in the App Engine standard environment where the type was
    ``google.appengine.datastore.entity_pb.Reference``.

    Args:
        serialized (bytes): A reference protobuf serialized to bytes.
        app (Optional[str]): The application ID / project ID for the
            constructed key.
        namespace (Optional[str]): The namespace for the constructed key.

    Returns:
        google.cloud.datastore.key.Key: The key corresponding to
        ``serialized``.

    Raises:
        RuntimeError: If ``app`` is not :data:`None`, but not the same as
            ``reference.app``.
        RuntimeError: If ``namespace`` is not :data:`None`, but not the same as
            ``reference.name_space``.
    """
    project = _project_from_app(reference.app)
    if app is not None:
        if _project_from_app(app) != project:
            raise RuntimeError(
                _REFERENCE_APP_MISMATCH.format(reference.app, app)
            )

    parsed_namespace = _key_module._get_empty(reference.name_space, "")
    if namespace is not None:
        if namespace != parsed_namespace:
            raise RuntimeError(
                _REFERENCE_NAMESPACE_MISMATCH.format(
                    reference.name_space, namespace
                )
            )

    _key_module._check_database_id(reference.database_id)
    flat_path = _key_module._get_flat_path(reference.path)
    return google.cloud.datastore.Key(
        *flat_path, project=project, namespace=parsed_namespace
    )


def _from_serialized(serialized, app, namespace):
    """Convert serialized protobuf to :class:`~google.cloud.datastore.key.Key`.

    This is intended to work with the "legacy" representation of a
    datastore "Key" used within Google App Engine (a so-called
    "Reference"). This assumes that ``serialized`` was created within an App
    Engine app via something like ``ndb.Key(...).serialized()``.

    Args:
        serialized (bytes): A reference protobuf serialized to bytes.
        app (Optional[str]): The application ID / project ID for the
            constructed key.
        namespace (Optional[str]): The namespace for the constructed key.

    Returns:
        Tuple[google.cloud.datastore.key.Key, .Reference]: The key
        corresponding to ``serialized`` and the Reference protobuf.
    """
    reference = _app_engine_key_pb2.Reference()
    reference.ParseFromString(serialized)
    return _from_reference(reference, app, namespace), reference


def _from_urlsafe(urlsafe, app, namespace):
    """Convert urlsafe string to :class:`~google.cloud.datastore.key.Key`.

    .. note::

       This is borrowed from
       :meth:`~google.cloud.datastore.key.Key.from_legacy_urlsafe`.
       It is provided here, rather than calling that method, since component
       parts need to be re-used.

    This is intended to work with the "legacy" representation of a
    datastore "Key" used within Google App Engine (a so-called
    "Reference"). This assumes that ``urlsafe`` was created within an App
    Engine app via something like ``ndb.Key(...).urlsafe()``.

    Args:
        urlsafe (Union[bytes, str]): The base64 encoded (ASCII) string
            corresponding to a datastore "Key" / "Reference".
        app (Optional[str]): The application ID / project ID for the
            constructed key.
        namespace (Optional[str]): The namespace for the constructed key.

    Returns:
        Tuple[google.cloud.datastore.key.Key, .Reference]: The key
        corresponding to ``urlsafe`` and the Reference protobuf.
    """
    if isinstance(urlsafe, str):
        urlsafe = urlsafe.encode("ascii")
    padding = b"=" * (-len(urlsafe) % 4)
    urlsafe += padding
    raw_bytes = base64.urlsafe_b64decode(urlsafe)
    return _from_serialized(raw_bytes, app, namespace)


def _constructor_handle_positional(path_args, kwargs):
    """Properly handle positional arguments to Key constructor.

    This will modify ``kwargs`` in a few cases:

    * The constructor was called with a dictionary as the only
      positional argument (and no keyword arguments were passed). In
      this case, the contents of the dictionary passed in will be copied
      into ``kwargs``.
    * The constructor was called with at least one (non-dictionary)
      positional argument. In this case all of the positional arguments
      will be added to ``kwargs`` for the key ``flat``.

    Args:
        path_args (Tuple): The positional arguments.
        kwargs (Dict[str, Any]): The keyword arguments.

    Raises:
        TypeError: If keyword arguments were used while the first and
            only positional argument was a dictionary.
        TypeError: If positional arguments were provided and the keyword
            ``flat`` was used.
    """
    if not path_args:
        return

    if len(path_args) == 1 and isinstance(path_args[0], dict):
        if kwargs:
            raise TypeError(
                "Key() takes no keyword arguments when a dict is the "
                "the first and only non-keyword argument (for "
                "unpickling)."
            )
        kwargs.update(path_args[0])
    else:
        if "flat" in kwargs:
            raise TypeError(
                "Key() with positional arguments "
                "cannot accept flat as a keyword argument."
            )
        kwargs["flat"] = path_args


def _exactly_one_specified(*values):
    """Make sure exactly one of ``values`` is truthy.

    Args:
        values (Tuple[Any, ...]): Some values to be checked.

    Returns:
        bool: Indicating if exactly one of ``values`` was truthy.
    """
    count = sum(1 for value in values if value)
    return count == 1


def _parse_from_ref(
    klass,
    reference=None,
    serialized=None,
    urlsafe=None,
    app=None,
    namespace=None,
    **kwargs
):
    """Construct a key from a Reference.

    This makes sure that **exactly** one of ``reference``, ``serialized`` and
    ``urlsafe`` is specified (all three are different representations of a
    ``Reference`` protobuf).

    Args:
        klass (type): The class of the instance being constructed. It must
            be :class:`.Key`; we do not allow constructing :class:`.Key`
            subclasses from a serialized Reference protobuf.
        reference (Optional[\
            ~google.cloud.datastore._app_engine_key_pb2.Reference]): A
            reference protobuf representing a key.
        serialized (Optional[bytes]): A reference protobuf serialized to bytes.
        urlsafe (Optional[str]): A reference protobuf serialized to bytes. The
            raw bytes are then converted to a websafe base64-encoded string.
        app (Optional[str]): The Google Cloud Platform project (previously
            on Google App Engine, this was called the Application ID).
        namespace (Optional[str]): The namespace for the key.
        kwargs (Dict[str, Any]): Any extra keyword arguments not covered by
            the explicitly provided ones. These are passed through to indicate
            to the user that the wrong combination of arguments was used, e.g.
            if ``parent`` and ``urlsafe`` were used together.

    Returns:
        Tuple[~.datastore.Key, \
            ~google.cloud.datastore._app_engine_key_pb2.Reference]:
        A pair of the constructed key and the reference that was serialized
        in one of the arguments.

    Raises:
        TypeError: If ``klass`` is not :class:`.Key`.
        TypeError: If ``kwargs`` isn't empty.
        TypeError: If any number other than exactly one of ``reference``,
            ``serialized`` or ``urlsafe`` is provided.
    """
    if klass is not Key:
        raise TypeError(_WRONG_TYPE.format(klass))

    if kwargs or not _exactly_one_specified(reference, serialized, urlsafe):
        raise TypeError(
            "Cannot construct Key reference from incompatible "
            "keyword arguments."
        )

    if reference:
        ds_key = _from_reference(reference, app, namespace)
    elif serialized:
        ds_key, reference = _from_serialized(serialized, app, namespace)
    else:
        # NOTE: We know here that ``urlsafe`` is truth-y;
        #       ``_exactly_one_specified()`` guarantees this.
        ds_key, reference = _from_urlsafe(urlsafe, app, namespace)

    return ds_key, reference


def _parse_from_args(
    pairs=None, flat=None, app=None, namespace=None, parent=None
):
    """Construct a key the path (and possibly a parent key).

    Args:
        pairs (Optional[Iterable[Tuple[str, Union[str, int]]]]): An iterable
            of (kind, ID) pairs.
        flat (Optional[Iterable[Union[str, int]]]): An iterable of the
            (kind, ID) pairs but flattened into a single value. For example,
            the pairs ``[("Parent", 1), ("Child", "a")]`` would be flattened to
            ``["Parent", 1, "Child", "a"]``.
        app (Optional[str]): The Google Cloud Platform project (previously
            on Google App Engine, this was called the Application ID).
        namespace (Optional[str]): The namespace for the key.
        parent (Optional[~.ndb.key.Key]): The parent of the key being
            constructed. If provided, the key path will be **relative** to the
            parent key's path.

    Returns:
        ~.datastore.Key: The constructed key.

    Raises:
        ._BadValueError: If ``parent`` is passed but is not a ``Key``.
    """
    flat = _get_path(flat, pairs)
    _clean_flat_path(flat)

    parent_ds_key = None
    if parent is None:
        project = _project_from_app(app)
    else:
        project = _project_from_app(app, allow_empty=True)
        if not isinstance(parent, Key):
            raise _BadValueError(
                "Expected Key instance, got {!r}".format(parent)
            )
        # Offload verification of parent to ``google.cloud.datastore.Key()``.
        parent_ds_key = parent._key

    return google.cloud.datastore.Key(
        *flat, parent=parent_ds_key, project=project, namespace=namespace
    )


def _get_path(flat, pairs):
    """Get a flat path of key arguments.

    Does this from exactly one of ``flat`` or ``pairs``.

    Args:
        pairs (Optional[Iterable[Tuple[str, Union[str, int]]]]): An iterable
            of (kind, ID) pairs.
        flat (Optional[Iterable[Union[str, int]]]): An iterable of the
            (kind, ID) pairs but flattened into a single value. For example,
            the pairs ``[("Parent", 1), ("Child", "a")]`` would be flattened to
            ``["Parent", 1, "Child", "a"]``.

    Returns:
        List[Union[str, int]]: The flattened path as a list.

    Raises:
        TypeError: If both ``flat`` and ``pairs`` are provided.
        ValueError: If the ``flat`` path does not have an even number of
            elements.
        TypeError: If the paths are both empty.
    """
    if flat:
        if pairs is not None:
            raise TypeError(
                "Key() cannot accept both flat and pairs arguments."
            )
        if len(flat) % 2:
            raise ValueError(
                "Key() must have an even number of positional arguments."
            )
        flat = list(flat)
    else:
        flat = []
        for kind, id_ in pairs:
            flat.extend((kind, id_))

    if not flat:
        raise TypeError("Key must consist of at least one pair.")

    return flat


def _clean_flat_path(flat):
    """Verify and convert the flat path for a key.

    This may modify ``flat`` in place. In particular, if the last element is
    :data:`None` (for a partial key), this will pop it off the end. Also
    if some of the kinds are instance of :class:`.Model`, they will be
    converted to strings in ``flat``.

    Args:
        flat (List[Union[str, int]]): The flattened path as a list.

    Raises:
        TypeError: If the kind in a pair is an invalid type.
        ._BadArgumentError: If a key ID is :data:`None` (indicating a partial
           key), but in a pair other than the last one.
        TypeError: If a key ID is not a string or integer.
    """
    # Verify the inputs in ``flat``.
    for i in range(0, len(flat), 2):
        # Make sure the ``kind`` is either a string or a Model.
        kind = flat[i]
        if isinstance(kind, type):
            kind = kind._get_kind()
            flat[i] = kind
        if not isinstance(kind, str):
            raise TypeError(
                "Key kind must be a string or Model class; "
                "received {!r}".format(kind)
            )
        # Make sure the ``id_`` is either a string or int. In the special case
        # of a partial key, ``id_`` can be ``None`` for the last pair.
        id_ = flat[i + 1]
        if id_ is None:
            if i + 2 < len(flat):
                raise _BadArgumentError("Incomplete Key entry must be last")
        elif not isinstance(id_, (str, int)):
            raise TypeError(_INVALID_ID_TYPE.format(id_))

    # Remove trailing ``None`` for a partial key.
    if flat[-1] is None:
        flat.pop()
