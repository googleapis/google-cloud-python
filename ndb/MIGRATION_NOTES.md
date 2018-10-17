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
- I renamed `Property.__creation_counter_global` to
  `Property._CREATION_COUNTER`.
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
