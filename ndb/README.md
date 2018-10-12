# Google Datastore `ndb` Client Library

## Introduction

`ndb` is a client library for use with [Google Cloud Datastore][0].
It was designed specifically to be used from within the
[Google App Engine][1] Python runtime.

## Overview

Learn how to use the `ndb` library by visiting the Google Cloud Platform
[documentation][2].

## Assumptions

This is a running list of "compatibility" assumptions made for
the rewrite.

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
  on the `ndb.Key` class or `ndb.key` module (at import time)
- The "standard" exceptions from App Engine are no longer available. Instead,
  we'll create "shims" for them in `google.cloud.ndb._exceptions` to match the
  class names and emulate behavior.
- There is no replacement for `google.appengine.api.namespace_manager` which is
  used to determine the default namespace when not passed in to `Key()`

## Differences (between old and new implementations)

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

## Comments

- The `Key.__getnewargs__()` method isn't needed. For pickle protocols 0 and 1,
  `__new__` is not invoked on a class during unpickling; the state "unpacking"
  is handled solely via `__setstate__`. However, for pickle protocols 2, 3
  and 4, during unpickling an instance will first be created via
  `Key.__new__()` and then `__setstate__` would be called on that instance.
  The addition of the `__getnewargs__` allows the (positional) arguments to be
  stored in the pickled bytes. The original `ndb` implementation did **all** of
  the work of the constructor in `__new__`, so the call to `__setstate__` was
  redundant. In our implementation `__setstate__` is succifient and `__new__`
  isn't implemented, hence `__getnewargs__` isn't needed.
- Since we no longer use `__new__` as the constructor / utilize the
  `__getnewargs__` value, the extra support for
  `Key({"flat": ("a", "b"), ...})` as an alternative to
  `Key(flat=("a", "b"), ...)` can be retired
- Key parts (i.e. kind, string ID and / or integer ID) are verified when a
  `Reference` is created. However, this won't occur when the corresponding
  protobuf for the underlying `google.cloud.datastore.Key` is created. This
  is because the `Reference` is a legacy protobuf message type from App
  Engine, while the latest (`google/datastore/v1`) RPC definition uses a `Key`.
- There is a `Property._CREATION_COUNTER` that gets incremented every time
  a new `Property()` instance is created. This increment is not threadsafe.
  However, `ndb` was designed for `Property()` instances to be created at
  import time, so this may not be an issue.

[0]: https://cloud.google.com/datastore
[1]: https://cloud.google.com/appengine
[2]: https://cloud.google.com/appengine/docs/python/ndb/
