# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-vision/#history

## [2.8.0](https://github.com/googleapis/python-vision/compare/v2.7.3...v2.8.0) (2022-07-14)


### Features

* add audience parameter ([#455](https://github.com/googleapis/python-vision/issues/455)) ([1d8fe5f](https://github.com/googleapis/python-vision/commit/1d8fe5f5bf4d61b759766e5bf11a50937710e9a5))


### Bug Fixes

* **deps:** require google-api-core>=1.32.0,>=2.8.0 ([1d8fe5f](https://github.com/googleapis/python-vision/commit/1d8fe5f5bf4d61b759766e5bf11a50937710e9a5))
* require python 3.7+ ([#452](https://github.com/googleapis/python-vision/issues/452)) ([401bd73](https://github.com/googleapis/python-vision/commit/401bd73afd6c2e5e2c776249fe647858384c0433))

## [2.7.3](https://github.com/googleapis/python-vision/compare/v2.7.2...v2.7.3) (2022-06-06)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#438](https://github.com/googleapis/python-vision/issues/438)) ([927e833](https://github.com/googleapis/python-vision/commit/927e8331c0825fbabb382942b3e0c1efd8bd7c11))


### Documentation

* fix changelog header to consistent size ([#439](https://github.com/googleapis/python-vision/issues/439)) ([e3bd56d](https://github.com/googleapis/python-vision/commit/e3bd56de3138830a931413d065ccc850b2e90a06))

## [2.7.2](https://github.com/googleapis/python-vision/compare/v2.7.1...v2.7.2) (2022-03-25)


### Documentation

* fixed 'annotate an image' ([#330](https://github.com/googleapis/python-vision/issues/330)) ([1019f29](https://github.com/googleapis/python-vision/commit/1019f2920b065359306f654cf864d9f27a90cf9d))

## [2.7.1](https://github.com/googleapis/python-vision/compare/v2.7.0...v2.7.1) (2022-03-05)


### Bug Fixes

* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#319](https://github.com/googleapis/python-vision/issues/319)) ([249bff7](https://github.com/googleapis/python-vision/commit/249bff765c746103e68851f4d381a526af704e81))

## [2.7.0](https://github.com/googleapis/python-vision/compare/v2.6.3...v2.7.0) (2022-02-28)


### Features

* add api key support ([#300](https://github.com/googleapis/python-vision/issues/300)) ([25fc254](https://github.com/googleapis/python-vision/commit/25fc254a117f025bd0c7bddbc7b246b3c5a2b760))


### Bug Fixes

* resolve DuplicateCredentialArgs error when using credentials_file ([#304](https://github.com/googleapis/python-vision/issues/304)) ([6cca548](https://github.com/googleapis/python-vision/commit/6cca5487296127d7690734fdc610672b983607f2))


### Documentation

* add auto-generated samples ([#309](https://github.com/googleapis/python-vision/issues/309)) ([efc022d](https://github.com/googleapis/python-vision/commit/efc022d6b850dffbb621c066aa8fd1ff69cb0519))

## [2.6.3](https://www.github.com/googleapis/python-vision/compare/v2.6.2...v2.6.3) (2021-12-12)


### Documentation

* Add example of how to use max_results ([#277](https://www.github.com/googleapis/python-vision/issues/277)) ([cf4dafe](https://www.github.com/googleapis/python-vision/commit/cf4dafe7c716c8091efd3bcc5a6fa5729c72fed3))
* Update doctext sample to include method signature ([#275](https://www.github.com/googleapis/python-vision/issues/275)) ([b059f3a](https://www.github.com/googleapis/python-vision/commit/b059f3a7b39a6f17c0086e18fc69776265de18d7))

## [2.6.2](https://www.github.com/googleapis/python-vision/compare/v2.6.1...v2.6.2) (2021-11-01)


### Bug Fixes

* **deps:** drop packaging dependency ([b6bf6ab](https://www.github.com/googleapis/python-vision/commit/b6bf6abb9114ffbf426ad3aca49d76190a421e3e))
* **deps:** require google-api-core >= 1.28.0 ([b6bf6ab](https://www.github.com/googleapis/python-vision/commit/b6bf6abb9114ffbf426ad3aca49d76190a421e3e))


### Documentation

* list oneofs in docstring ([b6bf6ab](https://www.github.com/googleapis/python-vision/commit/b6bf6abb9114ffbf426ad3aca49d76190a421e3e))

## [2.6.1](https://www.github.com/googleapis/python-vision/compare/v2.6.0...v2.6.1) (2021-10-26)


### Documentation

* update async_detect_document() sample ([#260](https://www.github.com/googleapis/python-vision/issues/260)) ([b044537](https://www.github.com/googleapis/python-vision/commit/b044537fb49794ba988ffd8324b50d5cdbac6678))

## [2.6.0](https://www.github.com/googleapis/python-vision/compare/v2.5.0...v2.6.0) (2021-10-20)


### Features

* add support for python 3.10 ([#253](https://www.github.com/googleapis/python-vision/issues/253)) ([7d5e27a](https://www.github.com/googleapis/python-vision/commit/7d5e27af26b13e1854c50f2ff7a7bdd7feea7b0a))


### Documentation

* **readme:** add pylint limitations ([#246](https://www.github.com/googleapis/python-vision/issues/246)) ([e4fb61f](https://www.github.com/googleapis/python-vision/commit/e4fb61f276f4540149884e8098fc4575f30ec9a6))

## [2.5.0](https://www.github.com/googleapis/python-vision/compare/v2.4.4...v2.5.0) (2021-10-08)


### Features

* add context manager support in client ([#247](https://www.github.com/googleapis/python-vision/issues/247)) ([629365f](https://www.github.com/googleapis/python-vision/commit/629365f32d67bf3a6863615832e5443e185b8e3b))

## [2.4.4](https://www.github.com/googleapis/python-vision/compare/v2.4.3...v2.4.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([29b57f6](https://www.github.com/googleapis/python-vision/commit/29b57f6ef6506ba36c66e18d46781e6a15e872b2))

## [2.4.3](https://www.github.com/googleapis/python-vision/compare/v2.4.2...v2.4.3) (2021-09-27)


### Bug Fixes

* add 'dict' annotation type to 'request' ([87ad0ea](https://www.github.com/googleapis/python-vision/commit/87ad0eabbba08754320fd836c5e76fba48222b5c))

## [2.4.2](https://www.github.com/googleapis/python-vision/compare/v2.4.1...v2.4.2) (2021-07-29)


### Bug Fixes

* enable self signed jwt for grpc ([#207](https://www.github.com/googleapis/python-vision/issues/207)) ([f5b5ca5](https://www.github.com/googleapis/python-vision/commit/f5b5ca52aaa04dbe91dcf32097309e00593b5ce9))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#201](https://www.github.com/googleapis/python-vision/issues/201)) ([f6eaa1c](https://www.github.com/googleapis/python-vision/commit/f6eaa1c0a89258f9378672b8713990fc10cea0c9))


### Miscellaneous Chores

* release as 2.4.2 ([#209](https://www.github.com/googleapis/python-vision/issues/209)) ([8d48b1b](https://www.github.com/googleapis/python-vision/commit/8d48b1b2284da8eff95190478292f5422d59a2f1))

## [2.4.1](https://www.github.com/googleapis/python-vision/compare/v2.4.0...v2.4.1) (2021-07-21)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#200](https://www.github.com/googleapis/python-vision/issues/200)) ([1409d36](https://www.github.com/googleapis/python-vision/commit/1409d366835f3e12bc5b26c09123b2e70f9dcb70))

## [2.4.0](https://www.github.com/googleapis/python-vision/compare/v2.3.2...v2.4.0) (2021-07-12)


### Features

* add always_use_jwt_access ([#166](https://www.github.com/googleapis/python-vision/issues/166)) ([bff7763](https://www.github.com/googleapis/python-vision/commit/bff7763c586284eab96b3f43573006273e2e71ee))


### Bug Fixes

* disable always_use_jwt_access ([8cc57cc](https://www.github.com/googleapis/python-vision/commit/8cc57cc21809596737e7a42102510942426ee3e6))
* disable always_use_jwt_access ([#171](https://www.github.com/googleapis/python-vision/issues/171)) ([8cc57cc](https://www.github.com/googleapis/python-vision/commit/8cc57cc21809596737e7a42102510942426ee3e6))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-vision/issues/1127)) ([#161](https://www.github.com/googleapis/python-vision/issues/161)) ([78740ad](https://www.github.com/googleapis/python-vision/commit/78740ade95bf3eb7a2c613383e6ed602dfd1f1db)), closes [#1126](https://www.github.com/googleapis/python-vision/issues/1126)

## [2.3.2](https://www.github.com/googleapis/python-vision/compare/v2.3.1...v2.3.2) (2021-06-02)


### Bug Fixes

* **deps:** add packaging requirement ([#147](https://www.github.com/googleapis/python-vision/issues/147)) ([41b88bd](https://www.github.com/googleapis/python-vision/commit/41b88bd482d4d6ec76fc6efc99aa9343496faf72))

## [2.3.1](https://www.github.com/googleapis/python-vision/compare/v2.3.0...v2.3.1) (2021-04-13)


### Documentation

* insert spaces between classes and methods in docs ([#133](https://www.github.com/googleapis/python-vision/issues/133)) ([1495241](https://www.github.com/googleapis/python-vision/commit/1495241f7f19098ba33412e5c6f98c76b0bedfb2))

## [2.3.0](https://www.github.com/googleapis/python-vision/compare/v2.2.0...v2.3.0) (2021-03-31)


### Features

* add `from_service_account_info` ([ace6046](https://www.github.com/googleapis/python-vision/commit/ace604680ff0f2d1b0d458aa5c3eb1e98b4e81b0))


### Bug Fixes

* fix retry deadlines ([#119](https://www.github.com/googleapis/python-vision/issues/119)) ([ace6046](https://www.github.com/googleapis/python-vision/commit/ace604680ff0f2d1b0d458aa5c3eb1e98b4e81b0))

## [2.2.0](https://www.github.com/googleapis/python-vision/compare/v2.1.0...v2.2.0) (2021-02-11)


### Features

* add from_service_account_info factory ([7c3035a](https://www.github.com/googleapis/python-vision/commit/7c3035a5fa58d7218ba4ee60fbd0b37fd5fb21ab))
* **v1:** add `LEFT_CHEEK_CENTER` and `RIGHT_CHEEK_CENTER` to `FaceAnnotation` ([#103](https://www.github.com/googleapis/python-vision/issues/103)) ([7c3035a](https://www.github.com/googleapis/python-vision/commit/7c3035a5fa58d7218ba4ee60fbd0b37fd5fb21ab))


### Bug Fixes

* **v1:** deprecate confidence fields in safe search annotation ([7c3035a](https://www.github.com/googleapis/python-vision/commit/7c3035a5fa58d7218ba4ee60fbd0b37fd5fb21ab))


### Documentation

* use absolute references for types in docstrings ([7c3035a](https://www.github.com/googleapis/python-vision/commit/7c3035a5fa58d7218ba4ee60fbd0b37fd5fb21ab))

## [2.1.0](https://www.github.com/googleapis/python-vision/compare/v2.0.0...v2.1.0) (2021-01-26)


### Features

* **v1:** add text detection params; fix: remove client side recv limits ([#82](https://www.github.com/googleapis/python-vision/issues/82)) ([eaf1621](https://www.github.com/googleapis/python-vision/commit/eaf1621dc5a76e970e58d6366a80c1272be83ed2))


### Bug Fixes

* Fixes VPCSC Tests that did not conform to V2.0.0 client API ([#61](https://www.github.com/googleapis/python-vision/issues/61)) ([efed79a](https://www.github.com/googleapis/python-vision/commit/efed79a18c2c66bccb42aa214610fa5e7f9898dc))


### Documentation

* update example usage ([#68](https://www.github.com/googleapis/python-vision/issues/68)) ([ea22e98](https://www.github.com/googleapis/python-vision/commit/ea22e981ff1dfc87a18b026c5e775d5f08a29821))

## [2.0.0](https://www.github.com/googleapis/python-vision/compare/v1.0.0...v2.0.0) (2020-09-29)


### ⚠ BREAKING CHANGES

* migrate to use microgen (#52)

### Features

* migrate to use microgen ([#52](https://www.github.com/googleapis/python-vision/issues/52)) ([cf3d353](https://www.github.com/googleapis/python-vision/commit/cf3d35306c3a8f6d32cc7ce1eb436c965acc30fe))


### Bug Fixes

* update retry configs ([#29](https://www.github.com/googleapis/python-vision/issues/29)) ([39c1652](https://www.github.com/googleapis/python-vision/commit/39c16522f7bc97544c361f8e14dbc9a2a5d4c0e4))


### Documentation

* added note about not supported device ([#24](https://www.github.com/googleapis/python-vision/issues/24)) ([b33fa88](https://www.github.com/googleapis/python-vision/commit/b33fa88e4f1e9cb2f6e029e6a34364fb6cdc1a96))

## [1.0.0](https://www.github.com/googleapis/python-vision/compare/v0.42.0...v1.0.0) (2020-02-28)


### Features

* bump release status to GA ([#11](https://www.github.com/googleapis/python-vision/issues/11)) ([2129bde](https://www.github.com/googleapis/python-vision/commit/2129bdedfa0dca85c5adc5350bff10d4a485df77))

## [0.42.0](https://www.github.com/googleapis/python-vision/compare/v0.41.0...v0.42.0) (2020-02-03)


### Features

* **vision:** undeprecate resource name helpers, add 2.7 sunset warning (via synth) ([#10052](https://www.github.com/googleapis/python-vision/issues/10052)) ([2c86705](https://www.github.com/googleapis/python-vision/commit/2c86705154ce219f8fb6bbbcc80832ec2b63baeb))

## 0.41.0

12-05-2019 14:49 PST


### New Features
- Add deprecation warning to resource name helper functions. ([#9866](https://github.com/googleapis/google-cloud-python/pull/9866))

### Documentation
- Add deprecation information to resource name helper function documentation. ([#9866](https://github.com/googleapis/google-cloud-python/pull/9866))

## 0.40.0

11-08-2019 09:30 PST


### Implementation Changes
- Add proto annotations (via synth). ([#9441](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9441))
- Add RPC annotations, update docstrings (via synth). ([#9230](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9230))

### New Features
- Add celebrity recognition support to v1p4beta1 (via synth). ([#9613](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9613))
- Add object annotation support to v1p4beta1 (via synth). ([#9613](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9613))
- Add `purge_products` method to v1p4beta1 (via synth). ([#9613](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9613))
- Add more product categories (via synth). ([#9224](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9224))

### Documentation
- Update docstring for `product_category`, change requests intersphinx url (via synth). ([#9413](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9413))
- Fix intersphinx reference to requests. ([#9294](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9294))
- Remove compatability badges from READMEs. ([#9035](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9035))
- Update docstring to say at most 5 frames can be batch annotated (via synth). ([#9041](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9041))

### Internal / Testing Changes
- Flatten case of logo text in systest. ([#9159](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9159))
- Docs: Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/9085))

## 0.39.0

08-12-2019 13:57 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8976](https://github.com/googleapis/google-cloud-python/pull/8976))

### New Features
- Add 'parent' argument to annotation requests; add 'ProductSearchClient.purge_products' method; add 'object_annotations' field to product search results (via synth). ([#8988](https://github.com/googleapis/google-cloud-python/pull/8988))

### Documentation
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.38.1

07-24-2019 17:54 PDT

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

## 0.38.0

07-09-2019 10:05 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8411](https://github.com/googleapis/google-cloud-python/pull/8411))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8529](https://github.com/googleapis/google-cloud-python/pull/8529))

### Internal / Testing Changes
- Pin black version (via synth). ([#8602](https://github.com/googleapis/google-cloud-python/pull/8602))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- All of the negative vision vpc sc tests should use the same file. ([#8439](https://github.com/googleapis/google-cloud-python/pull/8439))
- In order to make sure access to the bucket is blocked by vpc sc, try to download any arbitrary file from the bucket. ([#8374](https://github.com/googleapis/google-cloud-python/pull/8374))
- Add disclaimer to auto-generated template files (via synth). ([#8335](https://github.com/googleapis/google-cloud-python/pull/8335))
- Add Vision API system tests to verify accessing a gcs bucket outside of a secure perimeter is blocked. ([#8276](https://github.com/googleapis/google-cloud-python/pull/8276))
- Add Vision API Product Search tests to verify ProductSearch is blocked by VPC SC when trying to access a resource outside of a secure perimeter when run from within a secure perimeter. ([#8269](https://github.com/googleapis/google-cloud-python/pull/8269))
- Add AsyncBatchAnnotateFiles system test ([#8260](https://github.com/googleapis/google-cloud-python/pull/8260))
- Add ImportProductSets system test ([#8259](https://github.com/googleapis/google-cloud-python/pull/8259))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8257](https://github.com/googleapis/google-cloud-python/pull/8257))
- Declare encoding as utf-8 in pb2 files (via synth).  ([#8371](https://github.com/googleapis/google-cloud-python/pull/8371))

## 0.37.0

05-30-2019 15:19 PDT

### Implementation Changes
- Add routing header to method metadata (via synth).  ([#7604](https://github.com/googleapis/google-cloud-python/pull/7604))

### New Features
- Add more categories to product search, update noxfile (via synth). ([#8170](https://github.com/googleapis/google-cloud-python/pull/8170))
- Add batch annotation for images and files, reorder methods (via synth).  ([#7845](https://github.com/googleapis/google-cloud-python/pull/7845))
- Vision: Add proto files for v1p4beta1

### Internal / Testing Changes
- Change docstrings (via synth). ([#7983](https://github.com/googleapis/google-cloud-python/pull/7983))
- Add system tests for Vision Product Search. Test product set resource… ([#7913](https://github.com/googleapis/google-cloud-python/pull/7913))
-  Update noxfile and docs configuration (via synth). ([#7839](https://github.com/googleapis/google-cloud-python/pull/7839))
- Vision: Add nox session `docs`, reorder methods, modify samples in docstrings (via synth). ([#7787](https://github.com/googleapis/google-cloud-python/pull/7787))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Copy lintified proto files (via synth). ([#7473](https://github.com/googleapis/google-cloud-python/pull/7473))

## 0.36.0

02-25-2019 15:02 PST


### Implementation Changes
- Remove unused message exports. ([#7280](https://github.com/googleapis/google-cloud-python/pull/7280))
- Protoc-generated serialization update. ([#7100](https://github.com/googleapis/google-cloud-python/pull/7100))
- GAPIC generation fixes: ([#7058](https://github.com/googleapis/google-cloud-python/pull/7058))
- Pick up order-of-enum fix from GAPIC generator. ([#6881](https://github.com/googleapis/google-cloud-python/pull/6881))

### New Features
- Add vision v1p4beta1. ([#7438](https://github.com/googleapis/google-cloud-python/pull/7438))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers.

### Internal / Testing Changes
- Add clarifying comment to blacken nox target. ([#7408](https://github.com/googleapis/google-cloud-python/pull/7408))
- Copy proto files alongside protoc versions
- Vision: get system logo tests healthy. ([#7245](https://github.com/googleapis/google-cloud-python/pull/7245))
- Add protos as an artifact to library. ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.35.2

12-17-2018 17:10 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

### Internal / Testing Changes
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))

## 0.35.1

11-21-2018 11:25 PST

### Implementation Changes
- Add ProductSearchClient to vision.py ([#6635](https://github.com/googleapis/google-cloud-python/pull/6635))

### Internal / Testing Changes
- Merge fixes to GAPIC generator. ([#6632](https://github.com/googleapis/google-cloud-python/pull/6632))

## 0.35.0

11-13-2018 09:55 PST


### Implementation Changes
- Fix client_info bug, update docstrings via synth. ([#6437](https://github.com/googleapis/google-cloud-python/pull/6437))

### New Features
- Add 'product_search_client' to 'vision_v1'. ([#6361](https://github.com/googleapis/google-cloud-python/pull/6361))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Fix GAX fossils. ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Normalize use of support level badges. ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6003](https://github.com/googleapis/google-cloud-python/pull/6003))

### Internal / Testing Changes
- Use new Nox. ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.34.0

### Implementation Changes

- Clean up feature introspection. ([#5851](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5851))

### New Features

- Regenerate to pick up new features in the underlying API. ([#5854](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5854))

## 0.33.0

### New Features
- Add v1p3beta1 endpoint to vision client library (#5638)

## 0.32.0

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Regenerate underlying client library (#5467)

### Internal / Testing Changes
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.31.1

### Packaging
- Update setuptools before packaging (#5265)

## 0.31.0

- Vision v1p2beta1: PDF/TIFF OCR (#5127)
- Use `install_requires` for platform dependencies instead of `extras_require` (#4991)
- Add vision v1p2beta1 (#4998)
- Fix bad trove classifier
- Add max results to feature (#4817)

## 0.30.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Fix coveragerc to correctly omit generated files (#4843)

## 0.29.0

### :warning: Breaking Changes

- The HTTP/JSON based client that was deprecated in 0.25.0 is completely
  removed.

### Release Candidate

- This is the (hopefully) final release candidate before declaring a stable
  release.

### Features

- The `v1p1beta1` endpoint has been added. (#4493)

  This is a superset of `v1` and includes features that are still in beta
  on the API side. You can opt in to this endpoint by importing it explicitly:

  ```python
  from google.cloud import vision_v1p1beta1
  client = vision_v1p1beta1.ImageAnnotatorClient()
  ```

PyPI: https://pypi.org/project/google-cloud-vision/0.29.0/


## 0.28.0

### Notable Implementation Changes

- Update and re-organize autogenerated code (#3952)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-vision/0.28.0/
