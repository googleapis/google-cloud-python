# Changelog

## [1.6.0](https://github.com/googleapis/python-vm-migration/compare/v1.5.1...v1.6.0) (2023-02-09)


### Features

* Enable "rest" transport in Python for services supporting numeric enums ([#113](https://github.com/googleapis/python-vm-migration/issues/113)) ([f6d145d](https://github.com/googleapis/python-vm-migration/commit/f6d145d8ae1b287f55a381436273ffaa717381b7))

## [1.5.1](https://github.com/googleapis/python-vm-migration/compare/v1.5.0...v1.5.1) (2023-01-23)


### Bug Fixes

* Add context manager return types ([a25c621](https://github.com/googleapis/python-vm-migration/commit/a25c621955f2b293a7020b9413f393959d69b344))


### Documentation

* Add documentation for enums ([a25c621](https://github.com/googleapis/python-vm-migration/commit/a25c621955f2b293a7020b9413f393959d69b344))

## [1.5.0](https://github.com/googleapis/python-vm-migration/compare/v1.4.0...v1.5.0) (2023-01-10)


### Features

* Add support for python 3.11 ([#106](https://github.com/googleapis/python-vm-migration/issues/106)) ([d0192a1](https://github.com/googleapis/python-vm-migration/commit/d0192a19b22a517c5ab49964d9b38e7eaf34f30a))
* AWS as a source  ([6430190](https://github.com/googleapis/python-vm-migration/commit/6430190d31af9f24747e9d1395c84ff32ea32898))
* Cycle\Clone\Cutover steps ([6430190](https://github.com/googleapis/python-vm-migration/commit/6430190d31af9f24747e9d1395c84ff32ea32898))
* Cycles history ([6430190](https://github.com/googleapis/python-vm-migration/commit/6430190d31af9f24747e9d1395c84ff32ea32898))

## [1.4.0](https://github.com/googleapis/python-vm-migration/compare/v1.3.3...v1.4.0) (2022-12-15)


### Features

* Add support for `google.cloud.vmmigration.__version__` ([10abf02](https://github.com/googleapis/python-vm-migration/commit/10abf02cfd5aa474d4a78de135e34836d3e4fd03))
* Add typing to proto.Message based class attributes ([10abf02](https://github.com/googleapis/python-vm-migration/commit/10abf02cfd5aa474d4a78de135e34836d3e4fd03))


### Bug Fixes

* Add dict typing for client_options ([10abf02](https://github.com/googleapis/python-vm-migration/commit/10abf02cfd5aa474d4a78de135e34836d3e4fd03))
* **deps:** Require google-api-core &gt;=1.34.0, >=2.11.0  ([fbef486](https://github.com/googleapis/python-vm-migration/commit/fbef486e187c595a1eb74837166c190787837a92))
* Drop usage of pkg_resources ([fbef486](https://github.com/googleapis/python-vm-migration/commit/fbef486e187c595a1eb74837166c190787837a92))
* Fix timeout default values ([fbef486](https://github.com/googleapis/python-vm-migration/commit/fbef486e187c595a1eb74837166c190787837a92))


### Documentation

* **samples:** Snippetgen handling of repeated enum field ([10abf02](https://github.com/googleapis/python-vm-migration/commit/10abf02cfd5aa474d4a78de135e34836d3e4fd03))
* **samples:** Snippetgen should call await on the operation coroutine before calling result ([fbef486](https://github.com/googleapis/python-vm-migration/commit/fbef486e187c595a1eb74837166c190787837a92))

## [1.3.3](https://github.com/googleapis/python-vm-migration/compare/v1.3.2...v1.3.3) (2022-10-07)


### Bug Fixes

* **deps:** Allow protobuf 3.19.5 ([#94](https://github.com/googleapis/python-vm-migration/issues/94)) ([f1fdfb0](https://github.com/googleapis/python-vm-migration/commit/f1fdfb079272c277ac9061c16f679f364f0ca646))

## [1.3.2](https://github.com/googleapis/python-vm-migration/compare/v1.3.1...v1.3.2) (2022-09-29)


### Bug Fixes

* **deps:** Require protobuf >= 3.20.2 ([#92](https://github.com/googleapis/python-vm-migration/issues/92)) ([d962e5a](https://github.com/googleapis/python-vm-migration/commit/d962e5a7f9db2397c26cac2ebea0271e10b9341b))

## [1.3.1](https://github.com/googleapis/python-vm-migration/compare/v1.3.0...v1.3.1) (2022-08-11)


### Bug Fixes

* **deps:** allow protobuf < 5.0.0 ([#69](https://github.com/googleapis/python-vm-migration/issues/69)) ([d4d1ba8](https://github.com/googleapis/python-vm-migration/commit/d4d1ba873f490e30a85efb8a2df8c0ca3edf8daa))
* **deps:** require proto-plus >= 1.22.0 ([d4d1ba8](https://github.com/googleapis/python-vm-migration/commit/d4d1ba873f490e30a85efb8a2df8c0ca3edf8daa))

## [1.3.0](https://github.com/googleapis/python-vm-migration/compare/v1.2.0...v1.3.0) (2022-07-19)


### Features

* add ApplianceVersion, AvailableUpdates, MigratingVmView, UpgradeApplianceRequest, UpgradeApplianceResponse, UpgradeStatus ([#64](https://github.com/googleapis/python-vm-migration/issues/64)) ([839fac4](https://github.com/googleapis/python-vm-migration/commit/839fac47189552905a80d8443df90cd8f97829fe))

## [1.2.0](https://github.com/googleapis/python-vm-migration/compare/v1.1.2...v1.2.0) (2022-07-16)


### Features

* add audience parameter ([61827e2](https://github.com/googleapis/python-vm-migration/commit/61827e246c7aae16537d00095737a47ccf537f90))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([#61](https://github.com/googleapis/python-vm-migration/issues/61)) ([2e7fb1e](https://github.com/googleapis/python-vm-migration/commit/2e7fb1ef0d7069cd22f64de464148940c8330ac2))
* require python 3.7+ ([#59](https://github.com/googleapis/python-vm-migration/issues/59)) ([af250ac](https://github.com/googleapis/python-vm-migration/commit/af250ac6e3307ce002b5c2cedd3878342e580c7e))

## [1.1.2](https://github.com/googleapis/python-vm-migration/compare/v1.1.1...v1.1.2) (2022-06-03)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#48](https://github.com/googleapis/python-vm-migration/issues/48)) ([c5c3155](https://github.com/googleapis/python-vm-migration/commit/c5c3155f62d5f46ac4f5071d68af0c448edcd93d))


### Documentation

* fix changelog header to consistent size ([#49](https://github.com/googleapis/python-vm-migration/issues/49)) ([1f5f92a](https://github.com/googleapis/python-vm-migration/commit/1f5f92ab6422e9b737a9f8e597501eb0cf17b798))

## [1.1.1](https://github.com/googleapis/python-vm-migration/compare/v1.1.0...v1.1.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#24](https://github.com/googleapis/python-vm-migration/issues/24)) ([0ee06fd](https://github.com/googleapis/python-vm-migration/commit/0ee06fda92a66981f21b0fe546335362f4fc8d80))

## [1.1.0](https://github.com/googleapis/python-vm-migration/compare/v1.0.0...v1.1.0) (2022-02-11)


### Features

* add api key support ([#14](https://github.com/googleapis/python-vm-migration/issues/14)) ([bf6760c](https://github.com/googleapis/python-vm-migration/commit/bf6760ce5ead26b352a5a89e079fa2ca20c0c3c6))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([c53543e](https://github.com/googleapis/python-vm-migration/commit/c53543e159c2513089223fdc956860a051244c29))

## [1.0.0](https://github.com/googleapis/python-vm-migration/compare/v0.1.0...v1.0.0) (2022-01-24)


### Features

* bump release level to production/stable ([#4](https://github.com/googleapis/python-vm-migration/issues/4)) ([23b4a5e](https://github.com/googleapis/python-vm-migration/commit/23b4a5ef93452580a4587e3d95163fcf664ed39f))

## 0.1.0 (2021-11-18)


### Features

* generate v1 ([4041de0](https://www.github.com/googleapis/python-vm-migration/commit/4041de00804957fddba57f6e972c7ed1415354f9))
