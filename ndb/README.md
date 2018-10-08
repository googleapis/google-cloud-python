# Google Datastore ``ndb`` Client Library

## Introduction

``ndb`` is a client library for use with [Google Cloud Datastore][0].
It was designed specifically to be used from within the
[Google App Engine][1] Python runtime.

## Overview

Learn how to use the ``ndb`` library by visiting the Google Cloud Platform
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
- The "standard" exception from App Engine are no longer available. Instead,
  we'll create "shims" for them to emulate behavior. For example, the `Key()`
  constructor used to raise the `BadArgumentError` exception from
  `google.appengine.api.datastore_errors` in some cases. Currently shims are
  - `ndb.key._BadArgumentError`
  - `ndb.key._BadValueError`
- There is no replacement for `google.appengine.api.namespace_manager` which is
  used to determine the default namespace when not passed in to `Key()`


[0]: https://cloud.google.com/datastore
[1]: https://cloud.google.com/appengine
[2]: https://cloud.google.com/appengine/docs/python/ndb/
