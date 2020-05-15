# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-ndb/#history

### [1.2.1](https://www.github.com/googleapis/python-ndb/compare/v1.2.0...v1.2.1) (2020-05-15)


### Features

* Improve custom validators ([#408](https://www.github.com/googleapis/python-ndb/issues/408)) ([5b6cdd6](https://www.github.com/googleapis/python-ndb/commit/5b6cdd627dfce3e5b987c2ecd945d39b5056aa37)), closes [#252](https://www.github.com/googleapis/python-ndb/issues/252)


### Bug Fixes

* clear context cache on rollback ([#410](https://www.github.com/googleapis/python-ndb/issues/410)) ([aa17986](https://www.github.com/googleapis/python-ndb/commit/aa17986759f32ea16c340961d70fbc8fc123b244)), closes [#398](https://www.github.com/googleapis/python-ndb/issues/398)
* do not allow empty key parts for key constructor in namespaced model ([#401](https://www.github.com/googleapis/python-ndb/issues/401)) ([f3528b3](https://www.github.com/googleapis/python-ndb/commit/f3528b3e51c93c762c4e31eed76a1b2f06be84e1)), closes [#384](https://www.github.com/googleapis/python-ndb/issues/384)
* don't rely on duck typing for `_retry.is_transient_error` ([#425](https://www.github.com/googleapis/python-ndb/issues/425)) ([4524542](https://www.github.com/googleapis/python-ndb/commit/4524542e5f6da1af047d86fee3d48cf65ea75508)), closes [#415](https://www.github.com/googleapis/python-ndb/issues/415)
* handle empty batches from Firestore ([#396](https://www.github.com/googleapis/python-ndb/issues/396)) ([1a054ca](https://www.github.com/googleapis/python-ndb/commit/1a054cadff07074de9395cb99ae2c40f987aed2e)), closes [#386](https://www.github.com/googleapis/python-ndb/issues/386)
* make sure reads happen in transaction if there is a transaction ([#395](https://www.github.com/googleapis/python-ndb/issues/395)) ([f32644f](https://www.github.com/googleapis/python-ndb/commit/f32644fcf8c16dc0fd74e14108d7955effff1771)), closes [#394](https://www.github.com/googleapis/python-ndb/issues/394)
* more should be boolean in fetch_page call ([#423](https://www.github.com/googleapis/python-ndb/issues/423)) ([a69ffd2](https://www.github.com/googleapis/python-ndb/commit/a69ffd21aaaa881f5e8e54339fd62a1b02d19c4b)), closes [#422](https://www.github.com/googleapis/python-ndb/issues/422)
* support same options in model.query as query ([#407](https://www.github.com/googleapis/python-ndb/issues/407)) ([d08019f](https://www.github.com/googleapis/python-ndb/commit/d08019fbecb0f018987267b01929a21e97b418e2))
* uniform handling of `projection` argument ([#428](https://www.github.com/googleapis/python-ndb/issues/428)) ([2b65c04](https://www.github.com/googleapis/python-ndb/commit/2b65c04e72a66062e2c792b5b1fb067fb935987f)), closes [#379](https://www.github.com/googleapis/python-ndb/issues/379)
* use `skipped_results` from query results to adjust offset ([#399](https://www.github.com/googleapis/python-ndb/issues/399)) ([6d1452d](https://www.github.com/googleapis/python-ndb/commit/6d1452d977f3f030ff65d5cbb3e593c0789e6c14)), closes [#392](https://www.github.com/googleapis/python-ndb/issues/392)
* use fresh context cache for each transaction ([#409](https://www.github.com/googleapis/python-ndb/issues/409)) ([5109b91](https://www.github.com/googleapis/python-ndb/commit/5109b91425e917727973079020dc51c2b8fddf53)), closes [#394](https://www.github.com/googleapis/python-ndb/issues/394)
* use true `keys_only` query for `Query.count()` ([#405](https://www.github.com/googleapis/python-ndb/issues/405)) ([88184c3](https://www.github.com/googleapis/python-ndb/commit/88184c312dd7bdc7bd36ec58fd53e3fd5001d7ac)), closes [#400](https://www.github.com/googleapis/python-ndb/issues/400) [#404](https://www.github.com/googleapis/python-ndb/issues/404)

## [1.2.0](https://www.github.com/googleapis/python-ndb/compare/v1.1.2...v1.2.0) (2020-04-20)


### Features

* add `namespace` property to `context.Context` ([#388](https://www.github.com/googleapis/python-ndb/issues/388)) ([34bac15](https://www.github.com/googleapis/python-ndb/commit/34bac153bcc191857715a8760671acaf4fd12706)), closes [#385](https://www.github.com/googleapis/python-ndb/issues/385)
* new `join` argument for `transaction` and related functions ([#381](https://www.github.com/googleapis/python-ndb/issues/381)) ([2c91685](https://www.github.com/googleapis/python-ndb/commit/2c916851d088b650a5d643dc322a4919f456fe05)), closes [#366](https://www.github.com/googleapis/python-ndb/issues/366)


### Bug Fixes

* accept `bytes` or `str` as base value for `JsonProperty` ([#380](https://www.github.com/googleapis/python-ndb/issues/380)) ([e7a0c7c](https://www.github.com/googleapis/python-ndb/commit/e7a0c7c8fb7d80f009442f759abadbd336c0c828)), closes [#378](https://www.github.com/googleapis/python-ndb/issues/378)
* add `ABORTED` to retryable status codes ([#391](https://www.github.com/googleapis/python-ndb/issues/391)) ([183c0c3](https://www.github.com/googleapis/python-ndb/commit/183c0c33a4429ad6bdaa9f141a8ac88ad4e3544d)), closes [#383](https://www.github.com/googleapis/python-ndb/issues/383)
* add missing _get_for_dict method ([#368](https://www.github.com/googleapis/python-ndb/issues/368)) ([55b80ff](https://www.github.com/googleapis/python-ndb/commit/55b80ffa086568e8f820f9ab304952bc39383bd8)), closes [#367](https://www.github.com/googleapis/python-ndb/issues/367)
* empty Entities for optional LocalStructuredProperty fields  ([#370](https://www.github.com/googleapis/python-ndb/issues/370)) ([27a0969](https://www.github.com/googleapis/python-ndb/commit/27a0969982013b37d3f6d8785c3ad127788661f9)), closes [#369](https://www.github.com/googleapis/python-ndb/issues/369)
* return type in DateTimeProperty._to_base_type docstring ([#371](https://www.github.com/googleapis/python-ndb/issues/371)) ([0c549c8](https://www.github.com/googleapis/python-ndb/commit/0c549c89ff78554c4a4dde40973b503aa741422f))

### [1.1.2](https://www.github.com/googleapis/python-ndb/compare/v1.1.1...v1.1.2) (2020-03-16)


### Bug Fixes

* check for legacy local structured property values ([#365](https://www.github.com/googleapis/python-ndb/issues/365)) ([f81f406](https://www.github.com/googleapis/python-ndb/commit/f81f406d8e1059121341828836fce2aae5782fca)), closes [#359](https://www.github.com/googleapis/python-ndb/issues/359)
* move stub (grpc communication channel) to client ([#362](https://www.github.com/googleapis/python-ndb/issues/362)) ([90e0625](https://www.github.com/googleapis/python-ndb/commit/90e06252df25fa2ce199543e7b01b17ec284aaf1)), closes [#343](https://www.github.com/googleapis/python-ndb/issues/343)

### [1.1.1](https://www.github.com/googleapis/python-ndb/compare/v1.1.0...v1.1.1) (2020-03-05)


### Bug Fixes

* fix bug with `yield` of empty list in tasklets ([#354](https://www.github.com/googleapis/python-ndb/issues/354)) ([2d60ebf](https://www.github.com/googleapis/python-ndb/commit/2d60ebfe656abd75f6b9303550b2e03c2cbd79b7)), closes [#353](https://www.github.com/googleapis/python-ndb/issues/353)
* LocalStructuredProperty keep_keys ([#355](https://www.github.com/googleapis/python-ndb/issues/355)) ([9ff1b3d](https://www.github.com/googleapis/python-ndb/commit/9ff1b3de817da50b58a6aed574d7e2f2dcf92310))
* support nested sequences in parallel `yield` for tasklets ([#358](https://www.github.com/googleapis/python-ndb/issues/358)) ([8c91e7a](https://www.github.com/googleapis/python-ndb/commit/8c91e7ae8262f355a9eafe9051b3c1ef19d4c7cd)), closes [#349](https://www.github.com/googleapis/python-ndb/issues/349)

## [1.1.0](https://www.github.com/googleapis/python-ndb/compare/v1.0.1...v1.1.0) (2020-03-02)


### Features

* `Key.to_legacy_urlsafe()` ([#348](https://www.github.com/googleapis/python-ndb/issues/348)) ([ab10e3c](https://www.github.com/googleapis/python-ndb/commit/ab10e3c4998b8995d5a057163ce8d9dc8992111a))


### Bug Fixes

* allow legacy ndb to read LocalStructuredProperty entities. ([#344](https://www.github.com/googleapis/python-ndb/issues/344)) ([7b07692](https://www.github.com/googleapis/python-ndb/commit/7b0769236841cea1e864ae1e928a7b7021d300dc))
* fix delete in transaction ([#333](https://www.github.com/googleapis/python-ndb/issues/333)) ([5c162f4](https://www.github.com/googleapis/python-ndb/commit/5c162f4337b837f7125b1fb03f8cff5fb1b4a356)), closes [#271](https://www.github.com/googleapis/python-ndb/issues/271)
* make sure ``key.Key`` uses namespace from client when not specified ([#339](https://www.github.com/googleapis/python-ndb/issues/339)) ([44f02e4](https://www.github.com/googleapis/python-ndb/commit/44f02e46deef245f4d1ae80f9d2e4edd46ecd265)), closes [#337](https://www.github.com/googleapis/python-ndb/issues/337)
* properly exclude from indexes non-indexed subproperties of structured properties ([#346](https://www.github.com/googleapis/python-ndb/issues/346)) ([dde6b85](https://www.github.com/googleapis/python-ndb/commit/dde6b85897457cef7a1080690df5cfae9cb6c31e)), closes [#341](https://www.github.com/googleapis/python-ndb/issues/341)
* resurrect support for compressed text property ([#342](https://www.github.com/googleapis/python-ndb/issues/342)) ([5a86456](https://www.github.com/googleapis/python-ndb/commit/5a864563dc6e155b73e2ac35af6519823c356e19)), closes [#277](https://www.github.com/googleapis/python-ndb/issues/277)
* use correct name when reading legacy structured properties with names ([#347](https://www.github.com/googleapis/python-ndb/issues/347)) ([01d1256](https://www.github.com/googleapis/python-ndb/commit/01d1256e9d41c20bb5836067455c4be4abe1c516)), closes [#345](https://www.github.com/googleapis/python-ndb/issues/345)

### [1.0.1](https://www.github.com/googleapis/python-ndb/compare/v1.0.0...v1.0.1) (2020-02-11)


### Bug Fixes

* attempt to have fewer transient errors in continuous integration ([#328](https://www.github.com/googleapis/python-ndb/issues/328)) ([0484c7a](https://www.github.com/googleapis/python-ndb/commit/0484c7abf5a1529db5fecf17ebdf0252eab8449e))
* correct migration doc ([#313](https://www.github.com/googleapis/python-ndb/issues/313)) ([#317](https://www.github.com/googleapis/python-ndb/issues/317)) ([efce24f](https://www.github.com/googleapis/python-ndb/commit/efce24f16a877aecf78264946c22a2c9e3e97f53))
* disuse `__slots__` in most places ([#330](https://www.github.com/googleapis/python-ndb/issues/330)) ([a8b723b](https://www.github.com/googleapis/python-ndb/commit/a8b723b992e7a91860f6a73c0ee0fd7071e574d3)), closes [#311](https://www.github.com/googleapis/python-ndb/issues/311)
* don't set key on structured property entities ([#312](https://www.github.com/googleapis/python-ndb/issues/312)) ([63f3d94](https://www.github.com/googleapis/python-ndb/commit/63f3d943001d77c1ea0eb9b719e71ecff4eb5dd6)), closes [#281](https://www.github.com/googleapis/python-ndb/issues/281)
* fix race condition in remote calls ([#329](https://www.github.com/googleapis/python-ndb/issues/329)) ([f550510](https://www.github.com/googleapis/python-ndb/commit/f5505100f065e71a14714369d8aef1f7b06ee838)), closes [#302](https://www.github.com/googleapis/python-ndb/issues/302)
* make query options convert projection properties to strings ([#325](https://www.github.com/googleapis/python-ndb/issues/325)) ([d1a4800](https://www.github.com/googleapis/python-ndb/commit/d1a4800c5f53490e6956c11797bd3472ea404b5b))
* use multiple batches of limited size for large operations ([#321](https://www.github.com/googleapis/python-ndb/issues/321)) ([8e69453](https://www.github.com/googleapis/python-ndb/commit/8e6945377a4635632d0c35b7a41daebe501d4f0f)), closes [#318](https://www.github.com/googleapis/python-ndb/issues/318)
* use six string_types and integer_types for all isinstance() checks ([#323](https://www.github.com/googleapis/python-ndb/issues/323)) ([133acf8](https://www.github.com/googleapis/python-ndb/commit/133acf87b2a2efbfeae23ac9f629132cfb368a55))

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
