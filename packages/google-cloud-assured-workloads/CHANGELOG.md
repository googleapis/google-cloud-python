# Changelog

## [0.6.0](https://www.github.com/googleapis/python-assured-workloads/compare/v0.5.0...v0.6.0) (2021-08-30)


### Features

* Add Canada regions and support compliance regime ([#73](https://www.github.com/googleapis/python-assured-workloads/issues/73)) ([b62f7c7](https://www.github.com/googleapis/python-assured-workloads/commit/b62f7c720d198741673cc93d452d0ac9067cd3c3))
* display_name is added to ResourceSettings ([b62f7c7](https://www.github.com/googleapis/python-assured-workloads/commit/b62f7c720d198741673cc93d452d0ac9067cd3c3))
* resource_settings is added to CreateWorkloadOperationMetadata ([b62f7c7](https://www.github.com/googleapis/python-assured-workloads/commit/b62f7c720d198741673cc93d452d0ac9067cd3c3))
* ResourceType CONSUMER_FOLDER and KEYRING are added ([b62f7c7](https://www.github.com/googleapis/python-assured-workloads/commit/b62f7c720d198741673cc93d452d0ac9067cd3c3))


### Bug Fixes

* billing_account is now optional in Workload ([b62f7c7](https://www.github.com/googleapis/python-assured-workloads/commit/b62f7c720d198741673cc93d452d0ac9067cd3c3))
* ResourceType CONSUMER_PROJECT is deprecated ([b62f7c7](https://www.github.com/googleapis/python-assured-workloads/commit/b62f7c720d198741673cc93d452d0ac9067cd3c3))

## [0.5.0](https://www.github.com/googleapis/python-assured-workloads/compare/v0.4.2...v0.5.0) (2021-07-28)


### Features

* Add EU Regions And Support compliance regime ([#67](https://www.github.com/googleapis/python-assured-workloads/issues/67)) ([a370ad5](https://www.github.com/googleapis/python-assured-workloads/commit/a370ad5c1c7525544f3e5a83e84e0c05ed1851e2))

### [0.4.2](https://www.github.com/googleapis/python-assured-workloads/compare/v0.4.1...v0.4.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#64](https://www.github.com/googleapis/python-assured-workloads/issues/64)) ([c7e4331](https://www.github.com/googleapis/python-assured-workloads/commit/c7e43317be9e68508449a0f9cb548d1bd5904f1e))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#60](https://www.github.com/googleapis/python-assured-workloads/issues/60)) ([b161d65](https://www.github.com/googleapis/python-assured-workloads/commit/b161d658c8cdf294f72181b368e9e8df3529c392))


### Miscellaneous Chores

* release as 0.4.2 ([#65](https://www.github.com/googleapis/python-assured-workloads/issues/65)) ([8f8f538](https://www.github.com/googleapis/python-assured-workloads/commit/8f8f53852fd2e3ae4a917cdd7c37125fb01043a4))

### [0.4.1](https://www.github.com/googleapis/python-assured-workloads/compare/v0.4.0...v0.4.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#59](https://www.github.com/googleapis/python-assured-workloads/issues/59)) ([5113968](https://www.github.com/googleapis/python-assured-workloads/commit/5113968fa3e779a1e1d69f3642d9cd2f7ebcbe91))

## [0.4.0](https://www.github.com/googleapis/python-assured-workloads/compare/v0.3.1...v0.4.0) (2021-06-30)


### Features

* add always_use_jwt_access ([#52](https://www.github.com/googleapis/python-assured-workloads/issues/52)) ([9533d55](https://www.github.com/googleapis/python-assured-workloads/commit/9533d55b45ca854800cd2a15c136dc0247465fea))


### Bug Fixes

* disable always_use_jwt_access ([efac3ed](https://www.github.com/googleapis/python-assured-workloads/commit/efac3eddda13b62f01a451e0314b544d0f97cac8))
* disable always_use_jwt_access ([#56](https://www.github.com/googleapis/python-assured-workloads/issues/56)) ([efac3ed](https://www.github.com/googleapis/python-assured-workloads/commit/efac3eddda13b62f01a451e0314b544d0f97cac8))


### Documentation

* fix typo in docs/index.rst ([#43](https://www.github.com/googleapis/python-assured-workloads/issues/43)) ([df2ea64](https://www.github.com/googleapis/python-assured-workloads/commit/df2ea6472b097b53ee7c278051ad4bd11e85ef7b))
* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-assured-workloads/issues/1127)) ([#47](https://www.github.com/googleapis/python-assured-workloads/issues/47)) ([0f28736](https://www.github.com/googleapis/python-assured-workloads/commit/0f28736ad7d1966f41410d5d571fb56b6fef91df))

### [0.3.1](https://www.github.com/googleapis/python-assured-workloads/compare/v0.3.0...v0.3.1) (2021-06-16)


### Bug Fixes

* exclude docs and tests from package ([#44](https://www.github.com/googleapis/python-assured-workloads/issues/44)) ([d3dda4c](https://www.github.com/googleapis/python-assured-workloads/commit/d3dda4c019cc5fa8877b59d8454273f841a73d88))

## [0.3.0](https://www.github.com/googleapis/python-assured-workloads/compare/v0.2.1...v0.3.0) (2021-05-28)


### Features

* Add 'resource_settings' field to provide custom properties (ids) for the provisioned projects ([6ff8af6](https://www.github.com/googleapis/python-assured-workloads/commit/6ff8af6abc18d74d624e71b547f921b444435310))
* add HIPAA and HITRUST compliance regimes ([#13](https://www.github.com/googleapis/python-assured-workloads/issues/13)) ([6ff8af6](https://www.github.com/googleapis/python-assured-workloads/commit/6ff8af6abc18d74d624e71b547f921b444435310))
* support self-signed JWT flow for service accounts ([a28c728](https://www.github.com/googleapis/python-assured-workloads/commit/a28c728c4f8f50a3e5300d1cbfa7ed7262db1f9c))


### Bug Fixes

* add async client to %name_%version/init.py ([a28c728](https://www.github.com/googleapis/python-assured-workloads/commit/a28c728c4f8f50a3e5300d1cbfa7ed7262db1f9c))
* **deps:** add packaging requirement ([#37](https://www.github.com/googleapis/python-assured-workloads/issues/37)) ([ae6197c](https://www.github.com/googleapis/python-assured-workloads/commit/ae6197cb4761e2c7d1cab80721d7f3b0c16375f1))
* fix retry deadlines ([6ff8af6](https://www.github.com/googleapis/python-assured-workloads/commit/6ff8af6abc18d74d624e71b547f921b444435310))

### [0.2.1](https://www.github.com/googleapis/python-assured-workloads/compare/v0.2.0...v0.2.1) (2021-02-11)


### Bug Fixes

* remove client recv msg limit fix: add enums to `types/__init__.py` ([#9](https://www.github.com/googleapis/python-assured-workloads/issues/9)) ([ebd9505](https://www.github.com/googleapis/python-assured-workloads/commit/ebd950596feaa2ebd90334a0ace89f70ce76b381))

## [0.2.0](https://www.github.com/googleapis/python-assured-workloads/compare/v0.1.0...v0.2.0) (2020-11-17)


### Features

* add ``provisioned_resources_parent`` and ``kms_settings``; add common resource path helper methods ([daaff1f](https://www.github.com/googleapis/python-assured-workloads/commit/daaff1f32d3a1a44f0ba27ab3ecf4f8f0fbb6d3f))

## 0.1.0 (2020-10-02)


### Features

* generate v1beta1 ([999fa05](https://www.github.com/googleapis/python-assured-workloads/commit/999fa05075110ef9f915d08427731482e2bfc373))
