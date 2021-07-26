# Changelog

### [0.4.2](https://www.github.com/googleapis/python-area120-tables/compare/v0.4.1...v0.4.2) (2021-07-26)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#69](https://www.github.com/googleapis/python-area120-tables/issues/69)) ([954f6c7](https://www.github.com/googleapis/python-area120-tables/commit/954f6c7ef550d502cb75edb1f981de8eb67849b1))
* enable self signed jwt for grpc ([#75](https://www.github.com/googleapis/python-area120-tables/issues/75)) ([75f29fc](https://www.github.com/googleapis/python-area120-tables/commit/75f29fc84173a1c9497d261fc74d71cb068a41af))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#70](https://www.github.com/googleapis/python-area120-tables/issues/70)) ([15716f3](https://www.github.com/googleapis/python-area120-tables/commit/15716f32094df082a6536513699e68ab308aaf17))


### Miscellaneous Chores

* release as 0.4.2 ([#74](https://www.github.com/googleapis/python-area120-tables/issues/74)) ([682d5dd](https://www.github.com/googleapis/python-area120-tables/commit/682d5dd57c6f752595401bd2d5d232f875bc163b))

### [0.4.1](https://www.github.com/googleapis/python-area120-tables/compare/v0.4.0...v0.4.1) (2021-06-30)


### Bug Fixes

* disable always_use_jwt_access ([5c043fa](https://www.github.com/googleapis/python-area120-tables/commit/5c043fa62bd8e7cdb27a2392a72a74bb15d2e9f4))
* disable always_use_jwt_access ([#65](https://www.github.com/googleapis/python-area120-tables/issues/65)) ([5c043fa](https://www.github.com/googleapis/python-area120-tables/commit/5c043fa62bd8e7cdb27a2392a72a74bb15d2e9f4))

## [0.4.0](https://www.github.com/googleapis/python-area120-tables/compare/v0.3.1...v0.4.0) (2021-06-23)


### Features

* add always_use_jwt_access ([#61](https://www.github.com/googleapis/python-area120-tables/issues/61)) ([91c6f3a](https://www.github.com/googleapis/python-area120-tables/commit/91c6f3adf14a642aba2c0e18158536e9f3031f59))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-area120-tables/issues/1127)) ([#56](https://www.github.com/googleapis/python-area120-tables/issues/56)) ([4bf2bae](https://www.github.com/googleapis/python-area120-tables/commit/4bf2baea55b617393487c2ae6866f04ef073378d)), closes [#1126](https://www.github.com/googleapis/python-area120-tables/issues/1126)

### [0.3.1](https://www.github.com/googleapis/python-area120-tables/compare/v0.3.0...v0.3.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#52](https://www.github.com/googleapis/python-area120-tables/issues/52)) ([da319aa](https://www.github.com/googleapis/python-area120-tables/commit/da319aa3611e82602a4085a7b4472b2ad074b0a7))

## [0.3.0](https://www.github.com/googleapis/python-area120-tables/compare/v0.2.0...v0.3.0) (2021-05-28)


### Features

* Added ListWorkspaces, GetWorkspace, BatchDeleteRows APIs ([#25](https://www.github.com/googleapis/python-area120-tables/issues/25)) ([99c6918](https://www.github.com/googleapis/python-area120-tables/commit/99c691819824ab6cc1915ba23867a5051b94b8a2))
* support self-signed JWT flow for service accounts ([fe5836e](https://www.github.com/googleapis/python-area120-tables/commit/fe5836e050cc3f548c9a98af73d01466e23e8404))


### Bug Fixes

* add async client to %name_%version/init.py ([fe5836e](https://www.github.com/googleapis/python-area120-tables/commit/fe5836e050cc3f548c9a98af73d01466e23e8404))
* **deps:** add packaging requirement ([#47](https://www.github.com/googleapis/python-area120-tables/issues/47)) ([c7cee0b](https://www.github.com/googleapis/python-area120-tables/commit/c7cee0bd0252560e603f1456bdc577b26d477c87))

## [0.2.0](https://www.github.com/googleapis/python-area120-tables/compare/v0.1.0...v0.2.0) (2021-01-29)


### Features

* add common resource paths, expose client transport ([#4](https://www.github.com/googleapis/python-area120-tables/issues/4)) ([e2367d0](https://www.github.com/googleapis/python-area120-tables/commit/e2367d0be19e5e8e353ad9757a5b2ba730168b4c))


### Bug Fixes

* remove client recv msg limit and add enums to `types/__init__.py` ([#13](https://www.github.com/googleapis/python-area120-tables/issues/13)) ([302c071](https://www.github.com/googleapis/python-area120-tables/commit/302c071a8493f24b85938b48b66ff6eb83203eda))

## 0.1.0 (2020-09-14)


### Features

* add v1alpha1 ([fc837f9](https://www.github.com/googleapis/python-area120-tables/commit/fc837f99e01228db2cb844376e2f27be6bff3cd6))
* generate v1alpha1 ([7c9b3c5](https://www.github.com/googleapis/python-area120-tables/commit/7c9b3c552c3e99934c71bc64f6f6421343470875))
