# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-phishing-protection/#history


## [1.1.0](https://www.github.com/googleapis/python-phishingprotection/compare/v1.0.0...v1.1.0) (2021-01-06)


### Features

* add from_service_account_info factory and fix sphinx identifiers  ([#46](https://www.github.com/googleapis/python-phishingprotection/issues/46)) ([8938b54](https://www.github.com/googleapis/python-phishingprotection/commit/8938b54d590753ae25213945be3764e90d4bb327))


### Bug Fixes

* remove client recv msg limit and add enums to `types/__init__.py` ([197a753](https://www.github.com/googleapis/python-phishingprotection/commit/197a75346252441e5a5cb5eee982e7cb64a20299))

## [1.0.0](https://www.github.com/googleapis/python-phishingprotection/compare/v0.4.0...v1.0.0) (2020-12-04)


### ⚠ BREAKING CHANGES

* Move to API to python microgenerator. See [Migration Guide](https://github.com/googleapis/python-phishingprotection/blob/master/UPGRADING.md). (#31)

### Features

* move to API to python microgenerator ([#31](https://www.github.com/googleapis/python-phishingprotection/issues/31)) ([826fabd](https://www.github.com/googleapis/python-phishingprotection/commit/826fabd0b6591a7cca7cfcdbcc16b853c067cd3d))


### Bug Fixes

* update retry config ([#27](https://www.github.com/googleapis/python-phishingprotection/issues/27)) ([c0418ae](https://www.github.com/googleapis/python-phishingprotection/commit/c0418ae2e4d13f32706d3ce6844c6260b27ca0b7))

## [0.4.0](https://www.github.com/googleapis/python-phishingprotection/compare/v0.3.0...v0.4.0) (2020-06-23)


### Features

* release as beta ([#22](https://www.github.com/googleapis/python-phishingprotection/issues/22)) ([5111f42](https://www.github.com/googleapis/python-phishingprotection/commit/5111f425eef6135a4eb4b958d0ed1c6865e6e9d7))

## [0.3.0](https://www.github.com/googleapis/python-phishingprotection/compare/v0.2.0...v0.3.0) (2020-02-05)


### Features

* **phishingprotection:** undeprecate resource name helper methods, add 2.7 deprecation warning (via synth) ([#10048](https://www.github.com/googleapis/python-phishingprotection/issues/10048)) ([f96c1ed](https://www.github.com/googleapis/python-phishingprotection/commit/f96c1edfa57269b3e1ccbf3d8035e42fecb78987))


### Bug Fixes

* **phishingprotection:** deprecate resource name helper methods (via synth)  ([#9862](https://www.github.com/googleapis/python-phishingprotection/issues/9862)) ([83a9356](https://www.github.com/googleapis/python-phishingprotection/commit/83a93561695e799c8ff4a7d511fb7b6fe76d0d60))

## 0.2.0

10-10-2019 15:30 PDT

### Implementation Changes
- Use correct release status. ([#9451](https://github.com/googleapis/google-cloud-python/pull/9451))
- Remove send / receive message size limit (via synth). ([#8963](https://github.com/googleapis/google-cloud-python/pull/8963))
- Add `client_options` support, re-template / blacken files. ([#8539](https://github.com/googleapis/google-cloud-python/pull/8539))
- Fix dist name used to compute `gapic_version`. ([#8100](https://github.com/googleapis/google-cloud-python/pull/8100))
- Remove retries for `DEADLINE_EXCEEDED` (via synth). ([#7889](https://github.com/googleapis/google-cloud-python/pull/7889))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Change requests intersphinx url (via synth). ([#9407](https://github.com/googleapis/google-cloud-python/pull/9407))
- Update docstrings (via synth). ([#9350](https://github.com/googleapis/google-cloud-python/pull/9350))
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Normalize docs. ([#8994](https://github.com/googleapis/google-cloud-python/pull/8994))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

### Internal / Testing Changes
- Pin black version (via synth). ([#8590](https://github.com/googleapis/google-cloud-python/pull/8590))

## 0.1.0

04-30-2019 15:03 PDT

### New Features
- Initial release of Phishing Protection. ([#7801](https://github.com/googleapis/google-cloud-python/pull/7801))
