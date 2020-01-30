# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-ndb/#history

## [1.0.0](https://www.github.com/googleapis/python-ndb/compare/v0.2.2...v1.0.0) (2020-01-30)


### Bug Fixes

* add user agent prefix google-cloud-ndb + version ([#299](https://www.github.com/googleapis/python-ndb/issues/299)) ([9fa136b](https://www.github.com/googleapis/python-ndb/commit/9fa136b9c163b24aefde6ccbc227a1035fa24bcd))
* Finish implementation of UserProperty. ([#301](https://www.github.com/googleapis/python-ndb/issues/301)) ([fd2e0ed](https://www.github.com/googleapis/python-ndb/commit/fd2e0ed9bb6cec8b5651c58eaee2b3ca8a96aebb)), closes [#280](https://www.github.com/googleapis/python-ndb/issues/280)
* Fix bug when wrapping base values. ([#303](https://www.github.com/googleapis/python-ndb/issues/303)) ([91ca8d9](https://www.github.com/googleapis/python-ndb/commit/91ca8d9044671361b731323317cef720dd19be82)), closes [#300](https://www.github.com/googleapis/python-ndb/issues/300)
* Fix bug with the _GlobalCacheGetBatch. ([#305](https://www.github.com/googleapis/python-ndb/issues/305)) ([f213165](https://www.github.com/googleapis/python-ndb/commit/f2131654c6e5f67895fb0e3c09a507e8dc25c4bb)), closes [#294](https://www.github.com/googleapis/python-ndb/issues/294)
* Preserve `QueryIterator.cursor_after`. ([#296](https://www.github.com/googleapis/python-ndb/issues/296)) ([4ffedc7](https://www.github.com/googleapis/python-ndb/commit/4ffedc7b5a2366be15dcd299052d8a46a748addd)), closes [#292](https://www.github.com/googleapis/python-ndb/issues/292)

### [0.2.2](https://www.github.com/googleapis/python-ndb/compare/v0.2.1...v0.2.2) (2020-01-15)


### Bug Fixes

* Convert NDB keys to Datastore keys for serialization. ([#287](https://www.github.com/googleapis/python-ndb/issues/287)) ([779411b](https://www.github.com/googleapis/python-ndb/commit/779411b562575bd2d6f0627ce1903c2996f3c529)), closes [#284](https://www.github.com/googleapis/python-ndb/issues/284)
* fix missing __ne__ methods ([#279](https://www.github.com/googleapis/python-ndb/issues/279)) ([03dd5e1](https://www.github.com/googleapis/python-ndb/commit/03dd5e1c78b8e8354379d743e2f810ef1bece4d2))
* Fix repr() for ComputedProperty ([#291](https://www.github.com/googleapis/python-ndb/issues/291)) ([2d8857b](https://www.github.com/googleapis/python-ndb/commit/2d8857b8e9a7119a47fd72ae76401af4e42bb5b5)), closes [#256](https://www.github.com/googleapis/python-ndb/issues/256)
* Handle `int` for DateTimeProperty ([#285](https://www.github.com/googleapis/python-ndb/issues/285)) ([2fe5be3](https://www.github.com/googleapis/python-ndb/commit/2fe5be31784a036062180f9c0f2c7b5eda978123)), closes [#261](https://www.github.com/googleapis/python-ndb/issues/261)
* More friendly error message when using `fetch_page` with post-filters. ([#269](https://www.github.com/googleapis/python-ndb/issues/269)) ([a40ae74](https://www.github.com/googleapis/python-ndb/commit/a40ae74d74fa83119349de4b3a91f90df40d7ea5)), closes [#254](https://www.github.com/googleapis/python-ndb/issues/254)

### [0.2.1](https://www.github.com/googleapis/python-ndb/compare/v0.2.0...v0.2.1) (2019-12-10)


### Bug Fixes

* Correctly handle `limit` and `offset` when batching query results. ([#237](https://www.github.com/googleapis/python-ndb/issues/237)) ([8d3ce5c](https://www.github.com/googleapis/python-ndb/commit/8d3ce5c6cce9055d21400aa9feebc99e66393667)), closes [#236](https://www.github.com/googleapis/python-ndb/issues/236)
* Improve test cleanup. ([#234](https://www.github.com/googleapis/python-ndb/issues/234)) ([21f3d8b](https://www.github.com/googleapis/python-ndb/commit/21f3d8b12a3e2fefe488a951fb5186c7620cb864))
* IntegerProperty now accepts `long` type for Python 2.7. ([#262](https://www.github.com/googleapis/python-ndb/issues/262)) ([9591e56](https://www.github.com/googleapis/python-ndb/commit/9591e569db32769c449d60dd3d9bdd6772dbc8f6)), closes [#250](https://www.github.com/googleapis/python-ndb/issues/250)
* Unstable order bug in unit test. ([#251](https://www.github.com/googleapis/python-ndb/issues/251)) ([7ff1df5](https://www.github.com/googleapis/python-ndb/commit/7ff1df51056f8498dc4320fc4b2684ead34a9116)), closes [#244](https://www.github.com/googleapis/python-ndb/issues/244)

## 0.2.0

11-06-2019 10:39 PST


### Implementation Changes
- `query.map()` and `query.map_async()` hanging with empty result set. ([#230](https://github.com/googleapis/python-ndb/pull/230))
- remove dunder version ([#202](https://github.com/googleapis/python-ndb/pull/202))
- Check context ([#211](https://github.com/googleapis/python-ndb/pull/211))
- Fix `Model._gql`. ([#223](https://github.com/googleapis/python-ndb/pull/223))
- Update intersphinx mapping ([#206](https://github.com/googleapis/python-ndb/pull/206))
- do not set meanings for compressed property when it has no value ([#200](https://github.com/googleapis/python-ndb/pull/200))

### New Features
- Python 2.7 compatibility ([#203](https://github.com/googleapis/python-ndb/pull/203))
- Add `tzinfo` to DateTimeProperty. ([#226](https://github.com/googleapis/python-ndb/pull/226))
- Implement `_prepare_for_put` for `StructuredProperty` and `LocalStructuredProperty`. ([#221](https://github.com/googleapis/python-ndb/pull/221))
- Implement ``Query.map`` and ``Query.map_async``. ([#218](https://github.com/googleapis/python-ndb/pull/218))
- Allow class member values in projection and distinct queries  ([#214](https://github.com/googleapis/python-ndb/pull/214))
- Implement ``Future.cancel()`` ([#204](https://github.com/googleapis/python-ndb/pull/204))

### Documentation
- Update README to include Python 2 support. ([#231](https://github.com/googleapis/python-ndb/pull/231))
- Fix typo in MIGRATION_NOTES.md ([#208](https://github.com/googleapis/python-ndb/pull/208))
- Spelling fixes. ([#209](https://github.com/googleapis/python-ndb/pull/209))
- Add spell checking dependencies for documentation build. ([#196](https://github.com/googleapis/python-ndb/pull/196))

### Internal / Testing Changes
- Enable release-please ([#228](https://github.com/googleapis/python-ndb/pull/228))
- Introduce local redis for tests ([#191](https://github.com/googleapis/python-ndb/pull/191))
- Use .kokoro configs from templates. ([#194](https://github.com/googleapis/python-ndb/pull/194))

## 0.1.0

09-10-2019 13:43 PDT

### Deprecations
- Deprecate `max_memcache_items`, memcache options, `force_rewrites`, `Query.map()`, `Query.map_async()`, `blobstore`. ([#168](https://github.com/googleapis/python-ndb/pull/168))

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
- Add RedisCache implementation of global cache ([#150](https://github.com/googleapis/python-ndb/pull/150))
- Implement Global Cache ([#148](https://github.com/googleapis/python-ndb/pull/148))
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
- Clean up usage of `object.__new__` and mocks for `Model` in unit tests ([#177](https://github.com/googleapis/python-ndb/pull/177))
- Prove tasklets can be Python 2.7 and 3.7 compatible. ([#174](https://github.com/googleapis/python-ndb/pull/174))
- Discard src directory and fix flake8 failures ([#173](https://github.com/googleapis/python-ndb/pull/173))
- Add tests for `Model.__eq__()` ([#169](https://github.com/googleapis/python-ndb/pull/169))
- Remove skip flag accidentally left over ([#154](https://github.com/googleapis/python-ndb/pull/154))
- Try to get kokoro to add indexes for system tests ([#145](https://github.com/googleapis/python-ndb/pull/145))
- Add system test for PolyModel ([#133](https://github.com/googleapis/python-ndb/pull/133))
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
