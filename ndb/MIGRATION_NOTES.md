# `ndb` Migration Notes

This is a collection of assumptions, API / implementation differences
and comments about the `ndb` rewrite process.

The primary differences come from:

- Absence of "legacy" APIs provided by Google App Engine (e.g.
  `google.appengine.api.datastore_types`) as well as other environment
  specific features (e.g. the `APPLICATION_ID` environment variable)
- Presence of new features in Python 3 like keyword only arguments and
  async support

## Assumptions

- In production, the `APPLICATION_ID` environment variable will be set to
  a useful value (since there is no `dev_appserver.py` for
  `runtime: python37`). This is used as a fallback for the `ndb.Key()`
  constructor much like `google.cloud.datastore.Client()` determines a default
  project via one of

  - `DATASTORE_DATASET` environment variable (for `gcd` / emulator testing)
  - `GOOGLE_CLOUD_PROJECT` environment variable
  - Google App Engine application ID (this is legacy / standard GAE)
  - Google Compute Engine project ID (from metadata server)

  The correct fallback is likely different than this and should probably cache
  the output of `google.cloud.datastore.client._determine_default_project()`
  on the `ndb.Key` class or `ndb.key` module (it should cache at import time)

## Differences (between old and new implementations)

- The "standard" exceptions from App Engine are no longer available. Instead,
  we'll create "shims" for them in `google.cloud.ndb.exceptions` to match the
  class names and emulate behavior.
- There is no replacement for `google.appengine.api.namespace_manager` which is
  used to determine the default namespace when not passed in to `Key()`
- The `Key()` constructor (and helpers) make a distinction between `unicode`
  and `str` types (in Python 2). These are now `unicode->str` and `str->bytes`.
  However, `google.cloud.datastore.Key()` (the actual type we use under the
  covers), only allows the `str` type in Python 3, so much of the "type-check
  and branch" from the original implementation is gone. This **may** cause
  some slight differences.
- `Key.from_old_key()` and `Key.to_old_key()` always raise
  `NotImplementedError`. Without the actual types from the legacy runtime,
  these methods are impossible to implement. Also, since this code won't
  run on legacy Google App Engine, these methods aren't needed.
- `Key.app()` may not preserve the prefix from the constructor (this is noted
  in the docstring)
- `Key.__eq__` previously claimed to be "performance-conscious" and directly
  used `self.__app == other.__app` and similar comparisons. We don't store the
  same data on our `Key` (we just make a wrapper around
  `google.cloud.datastore.Key`), so these are replaced by functions calls
  `self.app() == self.app()` which incur some overhead.
- The verification of kind / string ID fails when they exceed 1500 bytes. The
  original implementation didn't allow in excess of 500 bytes, but it seems
  the limit has been raised by the backend. (FWIW, Danny's opinion is that
  the backend should enforce these limits, not the library.)
- `Property.__creation_counter_global` has been removed as it seems to have
  been included for a feature that was never implemented. See
  [Issue #175][1] for original rationale for including it and [Issue #6317][2]
  for discussion of its removal.
- `ndb` uses "private" instance attributes in many places, e.g. `Key.__app`.
  The current implementation (for now) just uses "protected" attribute names,
  e.g. `Key._key` (the implementation has changed in the rewrite). We may want
  to keep the old "private" names around for compatibility. However, in some
  cases, the underlying representation of the class has changed (such as `Key`)
  due to newly available helper libraries or due to missing behavior from
  the legacy runtime.
- `query.PostFilterNode.__eq__` compares `self.predicate` to `other.predicate`
  rather than using `self.__dict__ == other.__dict__`
- `__slots__` have been added to most non-exception types for a number of
  reasons. The first is the naive "performance" win and the second is that
  this will make it transparent whenever `ndb` users refer to non-existent
  "private" or "protected" instance attributes
- I dropped `Property._positional` since keyword-only arguments are native
  Python 3 syntax and dropped `Property._attributes`  in favor of an
  approach using `inspect.signature()`
- A bug in `Property._find_methods` was fixed where `reverse=True` was applied
  **before** caching and then not respected when pulling from the cache
- The `Property._find_methods_cache` has been changed. Previously it would be
  set on each `Property` subclass and populated dynamically on first use.
  Now `Property._FIND_METHODS_CACHE` is set to `{}` when the `Property` class
  is created and there is another level of keys (based on fully-qualified
  class name) in the cache.
- `eventloop` has been renamed to `_eventloop`. It is believed that `eventloop`
  was previously a *de facto* private module, so we've just made that
  explicit.
- `BlobProperty._datastore_type` has not been implemented; the base class
  implementation is sufficient. The original implementation wrapped a byte
  string in a `google.appengine.api.datastore_types.ByteString` instance, but
  that type was mostly an alias for `str` in Python 2
- `BlobProperty._validate` used to special case for "too long when indexed"
  if `isinstance(self, TextProperty)`. We have removed this check since
  the implementation does the same check in `TextProperty._validate`.
- The `BlobProperty` constructor only sets `_compressed` if explicitly
  passed. The original set `_compressed` always (and used `False` as default).
  In the exact same fashion the `JsonProperty` constructor only sets
  `_json_type` if explicitly passed. Similarly, the `DateTimeProperty`
  constructor only sets `_auto_now` and `_auto_now_add` if explicitly passed.
- `TextProperty(indexed=True)` and `StringProperty(indexed=False)` are no
  longer supported (see docstrings for more info)
- `model.GeoPt` is an alias for `google.cloud.datastore.helpers.GeoPoint`
  rather than an alias for `google.appengine.api.datastore_types.GeoPt`. These
  classes have slightly different characteristics.
- The `Property()` constructor (and subclasses) originally accepted both
  `unicode` and `str` (the Python 2 versions) for `name` (and `kind`) but we
  only accept `str`.
- The `Parameter()` constructor (and subclasses) originally accepted `int`,
  `unicode` and `str` (the Python 2 versions) for `key` but we only accept
  `int` and `str`.
- When a `Key` is used to create a query "node", e.g. via
  `MyModel.my_value == some_key`, the underlying behavior has changed.
  Previously a `FilterNode` would be created with the actual value set to
  `some_key.to_old_key()`. Now, we set it to `some_key._key`.
- The `google.appengine.api.users.User` class is missing, so there is a
  replacement in `google.cloud.ndb.model.User` that is also available as
  `google.cloud.ndb.User`. This does not support federated identity and
  has new support for adding such a user to a `google.cloud.datastore.Entity`
  and for reading one from a new-style `Entity`
- The `UserProperty` class no longer supports `auto_current_user(_add)`
- `Model.__repr__` will use `_key` to describe the entity's key when there
  is also a user-defined property named `key`. For an example, see the
  class docstring for `Model`.

## Comments

- There is rampant use (and abuse) of `__new__` rather than `__init__` as
  a constructor as the original implementation. By using `__new__`, sometimes
  a **different** type is used from the constructor. It seems that feature,
  along with the fact that `pickle` only calls `__new__` (and never `__init__`)
  is why `__init__` is almost never used.
- The `Key.__getnewargs__()` method isn't needed. For pickle protocols 0 and 1,
  `__new__` is not invoked on a class during unpickling; the state "unpacking"
  is handled solely via `__setstate__`. However, for pickle protocols 2, 3
  and 4, during unpickling an instance will first be created via
  `Key.__new__()` and then `__setstate__` would be called on that instance.
  The addition of the `__getnewargs__` allows the (positional) arguments to be
  stored in the pickled bytes. **All** of the work of the constructor happens
  in `__new__`, so the call to `__setstate__` is redundant. In our
  implementation `__setstate__` is sufficient, hence `__getnewargs__` isn't
  needed.
- Key parts (i.e. kind, string ID and / or integer ID) are verified when a
  `Reference` is created. However, this won't occur when the corresponding
  protobuf for the underlying `google.cloud.datastore.Key` is created. This
  is because the `Reference` is a legacy protobuf message type from App
  Engine, while the latest (`google/datastore/v1`) RPC definition uses a `Key`.
- There is a `Property._CREATION_COUNTER` that gets incremented every time
  a new `Property()` instance is created. This increment is not threadsafe.
  However, `ndb` was designed for `Property()` instances to be created at
  import time, so this may not be an issue.
- `ndb.model._BaseValue` for "wrapping" non-user values should probably
  be dropped or redesigned if possible.
- Since we want "compatibility", suggestions in `TODO` comments have not been
  implemented. However, that policy can be changed if desired.
- It seems that `query.ConjunctionNode.__new__` had an unreachable line
  that returned a `FalseNode`. This return has been changed to a
  `RuntimeError` just it case it **is** actually reached.
- For ``AND`` and ``OR`` to compare equal, the nodes must come in the
  same order. So ``AND(a > 7, b > 6)`` is not equal to ``AND(b > 6, a > 7)``.
- It seems that `query.ConjunctionNode.__new__` had an unreachable line
  that returned a `FalseNode`. This return has been changed to a
  `RuntimeError` just it case it **is** actually reached.
- For ``AND`` and ``OR`` to compare equal, the nodes must come in the
  same order. So ``AND(a > 7, b > 6)`` is not equal to ``AND(b > 6, a > 7)``.
- The whole `bytes` vs. `str` issue needs to be considered package-wide.
  For example, the `Property()` constructor always encoded Python 2 `unicode`
  to a Python 2 `str` (i.e. `bytes`) with the `utf-8` encoding. This fits
  in some sense: the property name in the [protobuf definition][3] is a
  `string` (i.e. UTF-8 encoded text). However, there is a bit of a disconnect
  with other types that use property names, e.g. `FilterNode`.
- There is a giant web of module interdependency, so runtime imports (to avoid
  import cycles) are very common. For example `model.Property` depends on
  `query` but `query` depends on `model`.
- Will need to sort out dependencies on old RPC implementations and port to
  modern gRPC. ([Issue #6363][4])

[1]: https://github.com/GoogleCloudPlatform/datastore-ndb-python/issues/175
[2]: https://github.com/googleapis/google-cloud-python/issues/6317
[3]: https://github.com/googleapis/googleapis/blob/3afba2fd062df0c89ecd62d97f912192b8e0e0ae/google/datastore/v1/entity.proto#L203
[4]: https://github.com/googleapis/google-cloud-python/issues/6363
