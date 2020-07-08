# Changelog

### [0.26.3](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.2...v0.26.3) (2020-07-08)


### Bug Fixes

* fix wrong unit test ([#502](https://www.github.com/googleapis/gapic-generator-python/issues/502)) ([c95bd45](https://www.github.com/googleapis/gapic-generator-python/commit/c95bd45506df7973758b9e1249586597d8214985))

### [0.26.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.1...v0.26.2) (2020-07-07)


### Bug Fixes

* add oneof fields to generated protoplus init ([#485](https://www.github.com/googleapis/gapic-generator-python/issues/485)) ([be5a847](https://www.github.com/googleapis/gapic-generator-python/commit/be5a847aeff6687679f7bca46308362d588f5c77)), closes [#484](https://www.github.com/googleapis/gapic-generator-python/issues/484)

### [0.26.1](https://www.github.com/googleapis/gapic-generator-python/compare/v0.26.0...v0.26.1) (2020-07-07)


### Bug Fixes

* pass metadata to pagers ([#470](https://www.github.com/googleapis/gapic-generator-python/issues/470)) ([c43c6d9](https://www.github.com/googleapis/gapic-generator-python/commit/c43c6d943fa99f202014bf4bba795df25d314a63)), closes [#469](https://www.github.com/googleapis/gapic-generator-python/issues/469)

## [0.26.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.25.2...v0.26.0) (2020-06-30)


### Features

* add `credentials_file` and `scopes` via `client_options` ([#461](https://www.github.com/googleapis/gapic-generator-python/issues/461)) ([b5e1b1e](https://www.github.com/googleapis/gapic-generator-python/commit/b5e1b1e8991159dc176da889e9bdf12e3eebdb1e))


### Bug Fixes

* add name and version info to fixup script name ([#490](https://www.github.com/googleapis/gapic-generator-python/issues/490)) ([16fe7e7](https://www.github.com/googleapis/gapic-generator-python/commit/16fe7e7885b7e17bf16b4f1f8f8844b9f5d0bdfe))
* Temporarily define a fixed testing event loop ([#493](https://www.github.com/googleapis/gapic-generator-python/issues/493)) ([2d22d91](https://www.github.com/googleapis/gapic-generator-python/commit/2d22d919bc8c08e03f501ff2f23152b761467c80))

### [0.25.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.25.1...v0.25.2) (2020-06-23)


### Bug Fixes

* always use dataclasses 0.6 ([#481](https://www.github.com/googleapis/gapic-generator-python/issues/481)) ([066d04e](https://www.github.com/googleapis/gapic-generator-python/commit/066d04e7d53301024106f244280502f16af46b79))

### [0.25.1](https://www.github.com/googleapis/gapic-generator-python/compare/0.25.0...v0.25.1) (2020-06-23)


### Bug Fixes

* only require dataclases if python<3.7 ([#475](https://www.github.com/googleapis/gapic-generator-python/issues/475)) ([9597695](https://www.github.com/googleapis/gapic-generator-python/commit/959769518ea47df383b23b6e48c5da148f69029e))

## [0.25.0](https://www.github.com/googleapis/gapic-generator-python/compare/v0.24.2...v0.25.0) (2020-06-17)


### Features

* provide AsyncIO support for generated code ([#365](https://www.github.com/googleapis/gapic-generator-python/issues/365)) ([305ed34](https://www.github.com/googleapis/gapic-generator-python/commit/305ed34cfc1607c990f2f88b27f53358da25c366))

### [0.24.2](https://www.github.com/googleapis/gapic-generator-python/compare/v0.24.1...v0.24.2) (2020-06-13)


### Bug Fixes

* generated unit tests live in the 'tests/gapic' subdir ([#456](https://www.github.com/googleapis/gapic-generator-python/issues/456)) ([1ed7c9d](https://www.github.com/googleapis/gapic-generator-python/commit/1ed7c9d6fe9595c390387d72113d741ebf28538d)), closes [#454](https://www.github.com/googleapis/gapic-generator-python/issues/454)

### [0.24.1](https://www.github.com/googleapis/gapic-generator-python/compare/0.24.0...v0.24.1) (2020-06-12)


### Bug Fixes

* update GOOGLE_API_USE_MTLS value ([#453](https://www.github.com/googleapis/gapic-generator-python/issues/453)) ([7449ad5](https://www.github.com/googleapis/gapic-generator-python/commit/7449ad5aad4a1fbbf9ca3796e097512fc80991e3))
