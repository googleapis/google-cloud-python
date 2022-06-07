# Changelog

## [1.0.2](https://github.com/googleapis/python-datastream/compare/v1.0.1...v1.0.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#100](https://github.com/googleapis/python-datastream/issues/100)) ([251b6b4](https://github.com/googleapis/python-datastream/commit/251b6b4bd215cd68b5aa72b529a15f0f94704471))


### Documentation

* fix changelog header to consistent size ([#101](https://github.com/googleapis/python-datastream/issues/101)) ([f3dc083](https://github.com/googleapis/python-datastream/commit/f3dc0837538cbd77869b49afb8b750314c068ddf))

## [1.0.1](https://github.com/googleapis/python-datastream/compare/v1.0.0...v1.0.1) (2022-05-06)


### Documentation

* fix type in docstring for map fields ([cb7249d](https://github.com/googleapis/python-datastream/commit/cb7249d165c28d6c4005313759282ce4f78966c8))

## [1.0.0](https://github.com/googleapis/python-datastream/compare/v0.4.2...v1.0.0) (2022-03-15)


### Features

* bump release level to production/stable ([05b5c87](https://github.com/googleapis/python-datastream/commit/05b5c875df8b6be6d5e9c6a89ffca017e0b5a160))

## [0.4.2](https://github.com/googleapis/python-datastream/compare/v0.4.1...v0.4.2) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#76](https://github.com/googleapis/python-datastream/issues/76)) ([f29eba0](https://github.com/googleapis/python-datastream/commit/f29eba05290746af2cb84463ad505eb427e36d98))

## [0.4.1](https://github.com/googleapis/python-datastream/compare/v0.4.0...v0.4.1) (2022-02-26)


### Documentation

* add generated snippets ([#66](https://github.com/googleapis/python-datastream/issues/66)) ([75656c1](https://github.com/googleapis/python-datastream/commit/75656c11c8e9ff8e0ffc509476477db268aca08d))

## [0.4.0](https://github.com/googleapis/python-datastream/compare/v0.3.1...v0.4.0) (2022-02-03)


### Features

* add api key support ([#58](https://github.com/googleapis/python-datastream/issues/58)) ([88cf10a](https://github.com/googleapis/python-datastream/commit/88cf10a130116cbc199d6279b00959ad40946671))
* add datastream v1 ([#61](https://github.com/googleapis/python-datastream/issues/61)) ([28dab85](https://github.com/googleapis/python-datastream/commit/28dab85bf3b4ad937760d5219623793936e39731))


### Bug Fixes

* remove `FetchErrorsRequest` and `FetchErrorsResponse` ([28dab85](https://github.com/googleapis/python-datastream/commit/28dab85bf3b4ad937760d5219623793936e39731))
* remove `GcsFileFormat` and `SchemaFileFormat` ([28dab85](https://github.com/googleapis/python-datastream/commit/28dab85bf3b4ad937760d5219623793936e39731))
* remove `NoConnectivitySettings` ([28dab85](https://github.com/googleapis/python-datastream/commit/28dab85bf3b4ad937760d5219623793936e39731))

## [0.3.1](https://www.github.com/googleapis/python-datastream/compare/v0.3.0...v0.3.1) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([1ea0cb4](https://www.github.com/googleapis/python-datastream/commit/1ea0cb4ea38123cc737c5c82b28e093ec9943d8b))
* **deps:** require google-api-core >= 1.28.0 ([1ea0cb4](https://www.github.com/googleapis/python-datastream/commit/1ea0cb4ea38123cc737c5c82b28e093ec9943d8b))


### Documentation

* list oneofs in docstring ([1ea0cb4](https://www.github.com/googleapis/python-datastream/commit/1ea0cb4ea38123cc737c5c82b28e093ec9943d8b))

## [0.3.0](https://www.github.com/googleapis/python-datastream/compare/v0.2.0...v0.3.0) (2021-10-15)


### Features

* add support for python 3.10 ([#38](https://www.github.com/googleapis/python-datastream/issues/38)) ([52d43b4](https://www.github.com/googleapis/python-datastream/commit/52d43b486ff7af6b2ad8956b29a59f2b5e3605c8))

## [0.2.0](https://www.github.com/googleapis/python-datastream/compare/v0.1.3...v0.2.0) (2021-10-08)


### Features

* add context manager support in client ([#35](https://www.github.com/googleapis/python-datastream/issues/35)) ([fa36978](https://www.github.com/googleapis/python-datastream/commit/fa369789687993fff0359f22110951393c849e70))


### Bug Fixes

* add 'dict' annotation type to 'request' ([973c851](https://www.github.com/googleapis/python-datastream/commit/973c851b750768b8405c97d33ed4cfdd66d39d9a))
* improper types in pagers generation ([09eaafd](https://www.github.com/googleapis/python-datastream/commit/09eaafd1b695b10bfc2bb212974eff11da76782c))

## [0.1.3](https://www.github.com/googleapis/python-datastream/compare/v0.1.2...v0.1.3) (2021-08-30)


### Bug Fixes

* **datastream:** Change a few resource pattern variables from camelCase to snake_case ([#20](https://www.github.com/googleapis/python-datastream/issues/20)) ([296962a](https://www.github.com/googleapis/python-datastream/commit/296962abf8d0b8cda4f3e1e978262c8628f4b31e))

## [0.1.2](https://www.github.com/googleapis/python-datastream/compare/v0.1.1...v0.1.2) (2021-07-29)


### Bug Fixes

* enable self signed jwt for grpc ([#11](https://www.github.com/googleapis/python-datastream/issues/11)) ([a292c8d](https://www.github.com/googleapis/python-datastream/commit/a292c8d97ad80d30108731b32575e12e324c48b5))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#7](https://www.github.com/googleapis/python-datastream/issues/7)) ([2159aa8](https://www.github.com/googleapis/python-datastream/commit/2159aa82a0f17398540e65c6167f728fd0b2981c))


### Miscellaneous Chores

* release as 0.1.2 ([#12](https://www.github.com/googleapis/python-datastream/issues/12)) ([15998c2](https://www.github.com/googleapis/python-datastream/commit/15998c223864ac8d6b2442f66ed42f19e1dc62ea))

## [0.1.1](https://www.github.com/googleapis/python-datastream/compare/v0.1.0...v0.1.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#6](https://www.github.com/googleapis/python-datastream/issues/6)) ([641dbc7](https://www.github.com/googleapis/python-datastream/commit/641dbc792fa23b720fd29ccc8363ac90a260d76f))

## 0.1.0 (2021-06-30)


### Features

* generate v1alpha1 ([00ea8f3](https://www.github.com/googleapis/python-datastream/commit/00ea8f336ac805b73fadb8d48a2a8e2883b4a3e3))
