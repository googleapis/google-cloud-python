# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-ndb/#history

## 0.1.0

09-10-2019 13:43 PDT


### Deprecations
- Deprecate `max_memcache_items`, memcache options, `force_rewrites`, `Query.map()`, `Query.mapi_async()`, `blobstore`. ([#168](https://github.com/googleapis/python-ndb/pull/168))

### Implementation Changes
- Fix error retrieving values for properties with different stored name ([#187](https://github.com/googleapis/python-ndb/pull/187))
- Use correct class when deserializing a PolyModel entity. ([#186](https://github.com/googleapis/python-ndb/pull/186))
- Support legacy compressed properties back and forth ([#183](https://github.com/googleapis/python-ndb/pull/183))
- Store Structured Properties in backwards compatible way ([#184](https://github.com/googleapis/python-ndb/pull/184))
- Allow put and get to work with compressed blob properties ([#175](https://github.com/googleapis/python-ndb/pull/175))
- Raise an exception when storing entity with partial key without Datastore. ([#171](https://github.com/googleapis/python-ndb/pull/171))
- Normalize to prefer ``project`` over ``app``. ([#170](https://github.com/googleapis/python-ndb/pull/170))
- Enforce naive datetimes for ``DateTimeProperty``. ([#167](https://github.com/googleapis/python-ndb/pull/167))
- Handle projections with structured properties. ([#166](https://github.com/googleapis/python-ndb/pull/166))
- Fix polymodel put and get ([#151](https://github.com/googleapis/python-ndb/pull/151))
- `_prepare_for_put` was not being called at entity level ([#138](https://github.com/googleapis/python-ndb/pull/138))
- Fix key property. ([#136](https://github.com/googleapis/python-ndb/pull/136))
- Fix thread local context. ([#131](https://github.com/googleapis/python-ndb/pull/131))
- Bugfix: Respect ``_indexed`` flag of properties. ([#127](https://github.com/googleapis/python-ndb/pull/127))
- Backwards compatibility with older style structured properties. ([#126](https://github.com/googleapis/python-ndb/pull/126))

### New Features
- Read legacy data with Repeated Structured Expando properties. ([#176](https://github.com/googleapis/python-ndb/pull/176))
- Implement ``Context.call_on_commit``. ([#159](https://github.com/googleapis/python-ndb/pull/159))
- Implement ``Context.flush`` ([#158](https://github.com/googleapis/python-ndb/pull/158))
- Implement ``use_datastore`` flag. ([#155](https://github.com/googleapis/python-ndb/pull/155))
- Implement ``tasklets.toplevel``. ([#157](https://github.com/googleapis/python-ndb/pull/157))
- RedisCache ([#150](https://github.com/googleapis/python-ndb/pull/150))
- Implement Global Cache (memcache) ([#148](https://github.com/googleapis/python-ndb/pull/148))
- ndb.Expando properties load and save ([#117](https://github.com/googleapis/python-ndb/pull/117))
- Implement cache policy. ([#116](https://github.com/googleapis/python-ndb/pull/116))

### Documentation
- Fix Kokoro publish-docs job ([#153](https://github.com/googleapis/python-ndb/pull/153))
- Update Migration Notes. ([#152](https://github.com/googleapis/python-ndb/pull/152))
- Add `project_urls` for pypi page ([#144](https://github.com/googleapis/python-ndb/pull/144))
- Fix `TRAMPOLINE_BUILD_FILE` in docs/common.cfg. ([#143](https://github.com/googleapis/python-ndb/pull/143))
- Add kokoro docs job to publish to googleapis.dev. ([#142](https://github.com/googleapis/python-ndb/pull/142))
- Initial version of migration guide ([#121](https://github.com/googleapis/python-ndb/pull/121))
- Add spellcheck sphinx extension to docs build process ([#123](https://github.com/googleapis/python-ndb/pull/123))

### Internal / Testing Changes
- Clean up usage of object.__new__ and mocks for `Model` in unit tests ([#177](https://github.com/googleapis/python-ndb/pull/177))
- Prove tasklets can be Python 2.7 and 3.7 compatible. ([#174](https://github.com/googleapis/python-ndb/pull/174))
- Discard src directory and fix flake8 failures ([#173](https://github.com/googleapis/python-ndb/pull/173))
- Some additional tests for `Model.__eq__()` ([#169](https://github.com/googleapis/python-ndb/pull/169))
- Remove skip flag accidentally left over ([#154](https://github.com/googleapis/python-ndb/pull/154))
- Try to get kokoro to add indexes for system tests ([#145](https://github.com/googleapis/python-ndb/pull/145))
- Add system test for PolyModel ([#133](https://github.com/googleapis/python-ndb/pull/133))
- Ask for feature development coordination via issues
- Fix system test under Datastore Emulator. (Fixes [#118](https://github.com/googleapis/python-ndb/pull/118)) ([#119](https://github.com/googleapis/python-ndb/pull/119))
- Add unit tests for `_entity_from_ds_entity` expando support ([#120](https://github.com/googleapis/python-ndb/pull/120))

## 0.0.1

06-11-2019 16:30 PDT

### Implementation Changes
- Query repeated structured properties. ([#103](https://github.com/googleapis/python-ndb/pull/103))
- Fix Structured Properties ([#102](https://github.com/googleapis/python-ndb/pull/102))

### New Features
- Implement expando model ([#99](https://github.com/googleapis/python-ndb/pull/99))
- Model properties ([#96](https://github.com/googleapis/python-ndb/pull/96))
- Implemented tasklets.synctasklet ([#58](https://github.com/googleapis/python-ndb/pull/58))
- Implement LocalStructuredProperty ([#93](https://github.com/googleapis/python-ndb/pull/93))
- Implement hooks. ([#95](https://github.com/googleapis/python-ndb/pull/95))
- Three easy Model methods. ([#94](https://github.com/googleapis/python-ndb/pull/94))
- Model.get or insert ([#92](https://github.com/googleapis/python-ndb/pull/92))
- Implement ``Model.get_by_id`` and ``Model.get_by_id_async``.
- Implement ``Model.allocate_ids`` and ``Model.allocate_ids_async``.
- Implement ``Query.fetch_page`` and ``Query.fetch_page_async``.
- Implement ``Query.count`` and ``Query.count_async``
- Implement ``Query.get`` and ``Query.get_async``.

### Documentation
- update sphinx version and eliminate all warnings ([#105](https://github.com/googleapis/python-ndb/pull/105))

## 0.0.1dev1

Initial development release of NDB client library.
