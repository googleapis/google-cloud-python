# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-recommender/#history

## [2.0.0](https://www.github.com/googleapis/python-recommender/compare/v1.1.1...v2.0.0) (2020-11-19)


### ⚠ BREAKING CHANGES

* use microgenerator (#54)

### Features

* use microgenerator ([#54](https://www.github.com/googleapis/python-recommender/issues/54)) ([63b8a43](https://www.github.com/googleapis/python-recommender/commit/63b8a43ce25a5305664424fa247ad82595c4342f)). See [Migration Guide](https://github.com/googleapis/python-recommender/blob/master/UPGRADING.md).

### [1.1.1](https://www.github.com/googleapis/python-recommender/compare/v1.1.0...v1.1.1) (2020-10-29)


### Bug Fixes

* tweak retry params for 'ListInsights'/'GetInsight'/'MarkInsightAccepted' API calls (via synth) ([#49](https://www.github.com/googleapis/python-recommender/issues/49)) ([0d2baaf](https://www.github.com/googleapis/python-recommender/commit/0d2baaf9e0d05897b4ea380510d3d899638cb45d))

## [1.1.0](https://www.github.com/googleapis/python-recommender/compare/v1.0.0...v1.1.0) (2020-07-13)


### Features

* add methods for interacting with insights ([#35](https://www.github.com/googleapis/python-recommender/issues/35)) ([940a3fb](https://www.github.com/googleapis/python-recommender/commit/940a3fb01013865c836bfb55397c25284004a7ad))


### Bug Fixes

* update retry config ([#31](https://www.github.com/googleapis/python-recommender/issues/31)) ([5c497e2](https://www.github.com/googleapis/python-recommender/commit/5c497e29d65d288a4b8b24a7b5aa487a5804e880))

## [1.0.0](https://www.github.com/googleapis/python-recommender/compare/v0.3.0...v1.0.0) (2020-05-21)


### Features

* release as production/stable ([#17](https://www.github.com/googleapis/python-recommender/issues/17)) ([b6f0a19](https://www.github.com/googleapis/python-recommender/commit/b6f0a1972df2d0eb49580e152f47b2d13ea1c53c))

## [0.3.0](https://www.github.com/googleapis/python-recommender/compare/v0.2.0...v0.3.0) (2020-03-14)


### Features

* add insight support; undeprecate resource name helper methods (via synth) ([#7](https://www.github.com/googleapis/python-recommender/issues/7)) ([876c383](https://www.github.com/googleapis/python-recommender/commit/876c383afed9a2384d9ef361b4054c381ab9a23b))

## 0.2.0

01-24-2020 14:03 PST

### Implementation Changes
- Deprecate resource name helper methods (via synth).  ([#9863](https://github.com/googleapis/google-cloud-python/pull/9863))

### New Features
- Add v1, set release level to beta. ([#10170](https://github.com/googleapis/google-cloud-python/pull/10170))

### Documentation
- Add Python 2 sunset banner to documentation. ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- Change requests intersphinx url (via synth). ([#9408](https://github.com/googleapis/google-cloud-python/pull/9408))
- Fix library reference doc link. ([#9338](https://github.com/googleapis/google-cloud-python/pull/9338))

### Internal / Testing Changes
- Correct config path in synth file for recommender. ([#10076](https://github.com/googleapis/google-cloud-python/pull/10076))

## 0.1.0

09-27-2019 12:20 PDT

### New Features
- initial release of v1beta1 ([#9257](https://github.com/googleapis/google-cloud-python/pull/9257))
