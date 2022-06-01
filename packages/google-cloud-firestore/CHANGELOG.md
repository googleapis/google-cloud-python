# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-firestore/#history


## [2.5.2](https://github.com/googleapis/python-firestore/compare/v2.5.1...v2.5.2) (2022-06-01)


### Bug Fixes

* **deps:** require protobuf <4.0.0dev ([#598](https://github.com/googleapis/python-firestore/issues/598)) ([1796592](https://github.com/googleapis/python-firestore/commit/1796592ffdedcace571452fe30b37bac914f7225))

## [2.5.1](https://github.com/googleapis/python-firestore/compare/v2.5.0...v2.5.1) (2022-05-30)


### Bug Fixes

* bulk_writer default assignment ([#565](https://github.com/googleapis/python-firestore/issues/565)) ([843c278](https://github.com/googleapis/python-firestore/commit/843c27816e97f38de2d37277f65b4428362ef661))
* **deps:** Require proto-plus >=1.20.5 ([#593](https://github.com/googleapis/python-firestore/issues/593)) ([2281290](https://github.com/googleapis/python-firestore/commit/2281290b153bc6eadfe6e539ac5638a57f073990)), closes [#592](https://github.com/googleapis/python-firestore/issues/592)

## [2.5.0](https://github.com/googleapis/python-firestore/compare/v2.4.0...v2.5.0) (2022-05-05)


### Features

* Enable RunQueryResponse.done ([#572](https://github.com/googleapis/python-firestore/issues/572)) ([3ec13da](https://github.com/googleapis/python-firestore/commit/3ec13dac8eb72dd5d5314528956a5aa8218fd5ba))


### Documentation

* clarifications for filters ([4d054b0](https://github.com/googleapis/python-firestore/commit/4d054b0f1323e1564eaa9f11326129707b1b1872))
* fix type in docstring for map fields ([4d054b0](https://github.com/googleapis/python-firestore/commit/4d054b0f1323e1564eaa9f11326129707b1b1872))

## [2.4.0](https://github.com/googleapis/python-firestore/compare/v2.3.4...v2.4.0) (2022-03-08)


### Features

* add api key support ([#523](https://github.com/googleapis/python-firestore/issues/523)) ([31c943e](https://github.com/googleapis/python-firestore/commit/31c943ee3c12f3dc65d56f00c7e3bf859dde16dd))
* add context manager support in client ([#470](https://github.com/googleapis/python-firestore/issues/470)) ([1e1de20](https://github.com/googleapis/python-firestore/commit/1e1de20000c4441c4c015709d5c3512a53c74d6b))
* add support for Python 3.10 ([#469](https://github.com/googleapis/python-firestore/issues/469)) ([ddcb099](https://github.com/googleapis/python-firestore/commit/ddcb0990e092416eb9a334fac5d8d9251bc43496))
* allow 'Collection.where(__name__, in, [hello, world])' ([#501](https://github.com/googleapis/python-firestore/issues/501)) ([7d71244](https://github.com/googleapis/python-firestore/commit/7d71244c3dab0052452d93f52e1f71bdae88459c))
* update client libraries to support Database operations ([#513](https://github.com/googleapis/python-firestore/issues/513)) ([74d8171](https://github.com/googleapis/python-firestore/commit/74d81716c9168b0e3e2fdd203a47292ebb28eb6f))


### Bug Fixes

* **deps:** drop packaging dependency ([6b5a779](https://github.com/googleapis/python-firestore/commit/6b5a7795bb2827b65f8015fcef6663880a29a65d))
* **deps:** require google-api-core >= 1.28.0 ([6b5a779](https://github.com/googleapis/python-firestore/commit/6b5a7795bb2827b65f8015fcef6663880a29a65d))
* **deps:** require google-api-core>=1.31.5, >=2.3.2 ([#543](https://github.com/googleapis/python-firestore/issues/543)) ([c214732](https://github.com/googleapis/python-firestore/commit/c2147325ed34ff72ab423265d0082db55daaf993))
* fix license text in the unit test ([#535](https://github.com/googleapis/python-firestore/issues/535)) ([3f1fd36](https://github.com/googleapis/python-firestore/commit/3f1fd365688980c9f82a9fc69650129fa8c01dcf))
* handle empty last chunk correctly in 'Query._chunkify' ([#489](https://github.com/googleapis/python-firestore/issues/489)) ([3ddc718](https://github.com/googleapis/python-firestore/commit/3ddc718d50143e33b8af4ff1ba29e7cadf76a57c))
* hash snapshots using correct type for 'update_time' ([#467](https://github.com/googleapis/python-firestore/issues/467)) ([5e66a73](https://github.com/googleapis/python-firestore/commit/5e66a73f7e9d3131f483bf5961e8dc308f5e8dc3))
* resolve DuplicateCredentialArgs error when using credentials_file ([77b9082](https://github.com/googleapis/python-firestore/commit/77b9082ba0876fd0043aa2220f5a3278accad00b))
* stop / start stream after filter mismatch ([#502](https://github.com/googleapis/python-firestore/issues/502)) ([a256752](https://github.com/googleapis/python-firestore/commit/a256752d425a6d9ec1047c7e6f38226d34a0254e))


### Documentation

* add generated snippets ([#532](https://github.com/googleapis/python-firestore/issues/532)) ([aea2af9](https://github.com/googleapis/python-firestore/commit/aea2af959c8631c14f8a7ea880b344f6f015b214))
* clarify docstring in RunQueryRequest/RunQueryResponse ([#544](https://github.com/googleapis/python-firestore/issues/544)) ([d17febb](https://github.com/googleapis/python-firestore/commit/d17febb44fabc6b56c14cfd61238d157925c4a4a))
* list oneofs in docstring ([6b5a779](https://github.com/googleapis/python-firestore/commit/6b5a7795bb2827b65f8015fcef6663880a29a65d))

### [2.3.4](https://www.github.com/googleapis/python-firestore/compare/v2.3.3...v2.3.4) (2021-09-30)


### Bug Fixes

* improper types in pagers generation ([4434415](https://www.github.com/googleapis/python-firestore/commit/4434415ef5b4aef81fe2a8ec9469ebaaa2a19d1b))

### [2.3.3](https://www.github.com/googleapis/python-firestore/compare/v2.3.2...v2.3.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([32bc180](https://www.github.com/googleapis/python-firestore/commit/32bc18080346d21dc1e0a4a7142707f6888c5359))
* harden 'query.stream' against retriable exceptions ([#456](https://www.github.com/googleapis/python-firestore/issues/456)) ([0dca32f](https://www.github.com/googleapis/python-firestore/commit/0dca32f054e274c4d8cc2cc05f4c8b91aee9e183))
* unbreak query orders w/ non-orderable operators ([#453](https://www.github.com/googleapis/python-firestore/issues/453)) ([2dbbba0](https://www.github.com/googleapis/python-firestore/commit/2dbbba027659322e60be248726c96c06e7a9e441))


### Performance Improvements

* strip proto wrappers in '_helpers.decode_{value,dict}' ([#458](https://www.github.com/googleapis/python-firestore/issues/458)) ([335e2c4](https://www.github.com/googleapis/python-firestore/commit/335e2c432e3d5377c2e5fb504ff8d4a319dec63c))

### [2.3.2](https://www.github.com/googleapis/python-firestore/compare/v2.3.1...v2.3.2) (2021-09-09)


### Bug Fixes

* treat None cursors as a no-op. ([#440](https://www.github.com/googleapis/python-firestore/issues/440)) ([e7aed0f](https://www.github.com/googleapis/python-firestore/commit/e7aed0f585a59e877223a15a3c2fc7f0f49105ee))

### [2.3.1](https://www.github.com/googleapis/python-firestore/compare/v2.3.0...v2.3.1) (2021-08-30)


### Bug Fixes

* harden lookup of credentials id_token attribute ([#434](https://www.github.com/googleapis/python-firestore/issues/434)) ([e28272a](https://www.github.com/googleapis/python-firestore/commit/e28272a1a4e8f7a681f4506142f4d4cd6fa0b993))

## [2.3.0](https://www.github.com/googleapis/python-firestore/compare/v2.2.0...v2.3.0) (2021-08-18)


### Features

* add bulk writer ([#396](https://www.github.com/googleapis/python-firestore/issues/396)) ([98a7753](https://www.github.com/googleapis/python-firestore/commit/98a7753f05240a2a75b9ffd42b7a148c65a6e87f))
* add recursive delete ([#420](https://www.github.com/googleapis/python-firestore/issues/420)) ([813a57b](https://www.github.com/googleapis/python-firestore/commit/813a57b1070a1f6ac41d02897fab33f8039b83f9))
* add support for recursive queries ([#407](https://www.github.com/googleapis/python-firestore/issues/407)) ([eb45a36](https://www.github.com/googleapis/python-firestore/commit/eb45a36e6c06b642106e061a32bfc119eb7e5bf0))


### Bug Fixes

* enable self signed jwt for grpc ([#405](https://www.github.com/googleapis/python-firestore/issues/405)) ([8703b48](https://www.github.com/googleapis/python-firestore/commit/8703b48c45e7bb742a794cad9597740c44182f81))
* use insecure grpc channels with emulator ([#402](https://www.github.com/googleapis/python-firestore/issues/402)) ([4381ad5](https://www.github.com/googleapis/python-firestore/commit/4381ad503ca3e83510b876281fc768d00d40d499))
* remove unused requirement pytz ([#422](https://www.github.com/googleapis/python-firestore/issues/422)) ([539c1d7](https://www.github.com/googleapis/python-firestore/commit/539c1d719191eb0ae3a49290c26b628de7c27cd5))


### Documentation

* added generated docs for Bundles ([#416](https://www.github.com/googleapis/python-firestore/issues/416)) ([0176cc7](https://www.github.com/googleapis/python-firestore/commit/0176cc7fef8752433b5c2496046d3a56557eb824))
* fixed broken links to devsite ([#417](https://www.github.com/googleapis/python-firestore/issues/417)) ([1adfc81](https://www.github.com/googleapis/python-firestore/commit/1adfc81237c4ddee665e81f1beaef808cddb860e))

## [2.2.0](https://www.github.com/googleapis/python-firestore/compare/v2.1.3...v2.2.0) (2021-07-22)


### Features

* add `always_use_jwt_access` ([#380](https://www.github.com/googleapis/python-firestore/issues/380)) ([2ef4194](https://www.github.com/googleapis/python-firestore/commit/2ef41949390f9f9ab11c1472e037b3a72c1b7ff6))


### Bug Fixes

* disable `always_use_jwt_access` ([#385](https://www.github.com/googleapis/python-firestore/issues/385)) ([13753e2](https://www.github.com/googleapis/python-firestore/commit/13753e2d4a9207e0b010b2599c9728ac1df4f8bf))
* reseed RNG for each auto id on 3.6 to avoid collisions ([#388](https://www.github.com/googleapis/python-firestore/issues/388)) ([784e8ae](https://www.github.com/googleapis/python-firestore/commit/784e8ae27d42d8e25deacaf37c34d79369738b00))
* update type hint for `async_collection.document()` ([#370](https://www.github.com/googleapis/python-firestore/issues/370)) ([ee6a1c2](https://www.github.com/googleapis/python-firestore/commit/ee6a1c25ed9af729eb39860a8756be2e9c0ba5ae))


### Documentation

* omit mention of Python 2.7 in `CONTRIBUTING.rst`([#377](https://www.github.com/googleapis/python-firestore/issues/377)) ([23ec468](https://www.github.com/googleapis/python-firestore/commit/23ec468bfc615dc2967022dd0ea689a94bc66aa9))
* add "Samples" section to `CONTRIBUTING.rst` ([#401](https://www.github.com/googleapis/python-firestore/issues/401)) ([0f9184d](https://www.github.com/googleapis/python-firestore/commit/0f9184de72a39ba19e29e888ca6c44be5d21c043))

### [2.1.3](https://www.github.com/googleapis/python-firestore/compare/v2.1.2...v2.1.3) (2021-06-15)


### Bug Fixes

* add 'packaging' dependency ([#372](https://www.github.com/googleapis/python-firestore/issues/372)) ([9623a51](https://www.github.com/googleapis/python-firestore/commit/9623a51e099f4f01013a6074f2a1ecc4a47db9d6)), closes [#371](https://www.github.com/googleapis/python-firestore/issues/371)

### [2.1.2](https://www.github.com/googleapis/python-firestore/compare/v2.1.1...v2.1.2) (2021-06-14)


### Documentation

* fix broken links in multiprocessing.rst ([#360](https://www.github.com/googleapis/python-firestore/issues/360)) ([6e2c899](https://www.github.com/googleapis/python-firestore/commit/6e2c89989c73ece393c9d23c87f1fc67b500e079))

### [2.1.1](https://www.github.com/googleapis/python-firestore/compare/v2.1.0...v2.1.1) (2021-05-03)


### Bug Fixes

* Allow underspecifying a cursor ([#340](https://www.github.com/googleapis/python-firestore/issues/340)) ([abe9e8a](https://www.github.com/googleapis/python-firestore/commit/abe9e8ab66ba55e43ae7da9e7d9febd1e63a5183))
* bump minimum versions for google-api-core and proto-plus ([#334](https://www.github.com/googleapis/python-firestore/issues/334)) ([08554dc](https://www.github.com/googleapis/python-firestore/commit/08554dc803a59f7ecd2310ce6860ed4f8aacf78d))

## [2.1.0](https://www.github.com/googleapis/python-firestore/compare/v2.0.2...v2.1.0) (2021-03-30)


### Features

* add firestore bundles ([#319](https://www.github.com/googleapis/python-firestore/issues/319)) ([c54de50](https://www.github.com/googleapis/python-firestore/commit/c54de50922b810cac030a71526bf62b9e4785a2f))
* adds synthed bundle protos ([#325](https://www.github.com/googleapis/python-firestore/issues/325)) ([8fdf2a8](https://www.github.com/googleapis/python-firestore/commit/8fdf2a868c66f7ebec39b190deb5d3a8a38bbc96))
* support using client credentials with emulator ([#269](https://www.github.com/googleapis/python-firestore/issues/269)) ([dffc580](https://www.github.com/googleapis/python-firestore/commit/dffc580472193c7d3b0eecadc316d77afaa0d0bf))


### Bug Fixes

* limit data transferred as part of list_documents as we don't require field data ([#280](https://www.github.com/googleapis/python-firestore/issues/280)) ([0386bc4](https://www.github.com/googleapis/python-firestore/commit/0386bc4824bd082410112c495963f13fb2489dfa))
* patch emulator channel to be created accordingly ([#288](https://www.github.com/googleapis/python-firestore/issues/288)) ([1a973f3](https://www.github.com/googleapis/python-firestore/commit/1a973f37e86207925e705d3fccdc88875d5d3ad1))
* remove client recv msg limit fix: add enums to `types/__init__.py` ([#274](https://www.github.com/googleapis/python-firestore/issues/274)) ([2b47c00](https://www.github.com/googleapis/python-firestore/commit/2b47c0072769ee47073c68ccab73733416aa0cef))
* use correct retry deadline ([#331](https://www.github.com/googleapis/python-firestore/issues/331)) ([f9586d4](https://www.github.com/googleapis/python-firestore/commit/f9586d4d75390e0daccd1ef0902d11b4dcca6472))
* use correct type hint for '*path' args ([#300](https://www.github.com/googleapis/python-firestore/issues/300)) ([15b579f](https://www.github.com/googleapis/python-firestore/commit/15b579f0b94aa8de3310b8bbc14916e97ac0c060))


### Documentation

* add documentation for documentsnapshot class ([#263](https://www.github.com/googleapis/python-firestore/issues/263)) ([448c965](https://www.github.com/googleapis/python-firestore/commit/448c96580da9e6db039cc3c69d2ac0b87ae9a05e))
* clarify semantics of 'merge' argument to 'Document.set' ([#278](https://www.github.com/googleapis/python-firestore/issues/278)) ([29c6374](https://www.github.com/googleapis/python-firestore/commit/29c637490e43db59529edcd3b61ccfca383eb223)), closes [#277](https://www.github.com/googleapis/python-firestore/issues/277)
* trailing whitespace ([#310](https://www.github.com/googleapis/python-firestore/issues/310)) ([b8192f0](https://www.github.com/googleapis/python-firestore/commit/b8192f018ef53f93a75d3623045e3fd356fba17f))
* update intersphinx for grpc and auth ([#261](https://www.github.com/googleapis/python-firestore/issues/261)) ([1bbd3a0](https://www.github.com/googleapis/python-firestore/commit/1bbd3a0dca43714289f741e759d8aaa40e3ef600))

### [2.0.2](https://www.github.com/googleapis/python-firestore/compare/v2.0.1...v2.0.2) (2020-12-05)


### Bug Fixes

* request and flattened params are exclusive, surface transport in generated layer ([#256](https://www.github.com/googleapis/python-firestore/issues/256)) ([386e85e](https://www.github.com/googleapis/python-firestore/commit/386e85ecf704e1168b0deb4ee9e6c2105a9040a9)), closes [#251](https://www.github.com/googleapis/python-firestore/issues/251) [#252](https://www.github.com/googleapis/python-firestore/issues/252)

### [2.0.1](https://www.github.com/googleapis/python-firestore/compare/v2.0.0...v2.0.1) (2020-11-12)


### Bug Fixes

* use an insecure channel under emulation ([#254](https://www.github.com/googleapis/python-firestore/issues/254)) ([801f827](https://www.github.com/googleapis/python-firestore/commit/801f8275899ea53c34f725f8a7629699f8b8ecbb)), closes [#250](https://www.github.com/googleapis/python-firestore/issues/250)


### Documentation

* update code of conduct ([#253](https://www.github.com/googleapis/python-firestore/issues/253)) ([3702dc8](https://www.github.com/googleapis/python-firestore/commit/3702dc8eede408aa326ddca9173cde572671c785))

## [2.0.0](https://www.github.com/googleapis/python-firestore/compare/v1.9.0...v2.0.0) (2020-11-06)


### ⚠ BREAKING CHANGES

* remove support for Python 2.7
* remove v1beta1 surface for v2 (#96)
* Begin using new microgenerator for v2 firestore (#91)
* from `firestore-0.30.0`: revert to merge not being an option;

### Features

* add client_options to base client class ([#150](https://www.github.com/googleapis/python-firestore/issues/150)) ([f3bedc1](https://www.github.com/googleapis/python-firestore/commit/f3bedc1efae4430c6853581fafef06d613548314))
* add inline type hints and pytype ci ([#134](https://www.github.com/googleapis/python-firestore/issues/134)) ([afff842](https://www.github.com/googleapis/python-firestore/commit/afff842a3356cbe5b0342be57341c12b2d601fda))
* add retry/timeout to manual surface ([#222](https://www.github.com/googleapis/python-firestore/issues/222)) ([db5f286](https://www.github.com/googleapis/python-firestore/commit/db5f286772592460b2bf02df25a121994889585d)), closes [#221](https://www.github.com/googleapis/python-firestore/issues/221)
* add support for not-in and not-eq query operators ([#202](https://www.github.com/googleapis/python-firestore/issues/202)) ([1d09f21](https://www.github.com/googleapis/python-firestore/commit/1d09f21f6c8cb7f69f0e30a960418f0f6899aa01))
* add type hints for method params ([#182](https://www.github.com/googleapis/python-firestore/issues/182)) ([9b6c2f3](https://www.github.com/googleapis/python-firestore/commit/9b6c2f33351c65901ea648e4407b2817e5e70957))
* asyncio microgen batch ([#122](https://www.github.com/googleapis/python-firestore/issues/122)) ([a4e5b00](https://www.github.com/googleapis/python-firestore/commit/a4e5b00a4d59e3416061d5c1ed32a111097e88b3))
* asyncio microgen client ([#118](https://www.github.com/googleapis/python-firestore/issues/118)) ([de4cc44](https://www.github.com/googleapis/python-firestore/commit/de4cc445e34e4a186ccc17bf143e04b45fb35f0b))
* asyncio microgen collection ([#119](https://www.github.com/googleapis/python-firestore/issues/119)) ([6281a67](https://www.github.com/googleapis/python-firestore/commit/6281a67e0ead38e7b2e477b7f077da7e0457aa9b))
* asyncio microgen document ([#121](https://www.github.com/googleapis/python-firestore/issues/121)) ([31faecb](https://www.github.com/googleapis/python-firestore/commit/31faecb2ab2956bad64b0852f1fe54a05d8907f9))
* asyncio microgen query ([#127](https://www.github.com/googleapis/python-firestore/issues/127)) ([178fa2c](https://www.github.com/googleapis/python-firestore/commit/178fa2c2a51a6bd6ef7a3c41b8307e44b5eab062))
* asyncio microgen transaction ([#123](https://www.github.com/googleapis/python-firestore/issues/123)) ([35185a8](https://www.github.com/googleapis/python-firestore/commit/35185a849053877c9cc561e75cdb4cd7338cc508))
* asyncio system tests ([#132](https://www.github.com/googleapis/python-firestore/issues/132)) ([4256a85](https://www.github.com/googleapis/python-firestore/commit/4256a856e6f1531959ffc080dfc8c8b3a7263ea5))
* Begin using new microgenerator for v2 firestore ([#91](https://www.github.com/googleapis/python-firestore/issues/91)) ([e0add08](https://www.github.com/googleapis/python-firestore/commit/e0add0860ca958d139787cdbb7fceb570fbb80ab))
* create async interface ([#61](https://www.github.com/googleapis/python-firestore/issues/61)) ([eaba25e](https://www.github.com/googleapis/python-firestore/commit/eaba25e892fa33c20ecc7aeab1528a004cbf99f7))
* Create CODEOWNERS ([#40](https://www.github.com/googleapis/python-firestore/issues/40)) ([a0cbf40](https://www.github.com/googleapis/python-firestore/commit/a0cbf403fe88f07c83bec81f275ac168be573e93))
* improve type information ([#176](https://www.github.com/googleapis/python-firestore/issues/176)) ([30bb3fb](https://www.github.com/googleapis/python-firestore/commit/30bb3fb5c36648d3b8acf76349a5726d7a5f135d))
* integrate limit to last ([#145](https://www.github.com/googleapis/python-firestore/issues/145)) ([55da695](https://www.github.com/googleapis/python-firestore/commit/55da695710d0408fc314ffe5cc6d7a48cb71bc3b)), closes [#57](https://www.github.com/googleapis/python-firestore/issues/57)
* partition queries ([#210](https://www.github.com/googleapis/python-firestore/issues/210)) ([4f75a75](https://www.github.com/googleapis/python-firestore/commit/4f75a75170be1bbb310b9e4741f4862d694b5bf5))
* remove v1beta1 surface for v2 ([#96](https://www.github.com/googleapis/python-firestore/issues/96)) ([b4a8eb9](https://www.github.com/googleapis/python-firestore/commit/b4a8eb97a68b4c7d1bc9faf0b113dca4476d9f1f))
* use 'update_transforms' ([#219](https://www.github.com/googleapis/python-firestore/issues/219)) ([c122e41](https://www.github.com/googleapis/python-firestore/commit/c122e4186808468a2ff82e9cc54b501809519859)), closes [#217](https://www.github.com/googleapis/python-firestore/issues/217)
* use `DatetimeWithNanoseconds` throughout library ([#116](https://www.github.com/googleapis/python-firestore/issues/116)) ([1801ba2](https://www.github.com/googleapis/python-firestore/commit/1801ba2a0e990c533865fef200bbcc3818b3b486))
* **firestore:** add `IN`, `ARRAY_CONTAINS_ANY` operators; update docstrings (via synth) ([#9439](https://www.github.com/googleapis/python-firestore/issues/9439)) ([107e526](https://www.github.com/googleapis/python-firestore/commit/107e526cb1d887096e99ce86f7125760b325b2bb))
* **firestore:** add v1beta1 deprecation annotation ([#34](https://www.github.com/googleapis/python-firestore/issues/34)) ([b9e2ab5](https://www.github.com/googleapis/python-firestore/commit/b9e2ab58a41c7bbab28028cb88f84bd6013816ed))
* **firestore:** surface new 'IN' and 'ARRAY_CONTAINS_ANY' operators ([#9541](https://www.github.com/googleapis/python-firestore/issues/9541)) ([5e9fe4f](https://www.github.com/googleapis/python-firestore/commit/5e9fe4f9ba21b9c38ebd41eb7ed083b335472e0b))


### Bug Fixes

* add import message via synth ([#231](https://www.github.com/googleapis/python-firestore/issues/231)) ([5fb02e9](https://www.github.com/googleapis/python-firestore/commit/5fb02e9b9521938ec1040611cf7086077d07aac2)), closes [#227](https://www.github.com/googleapis/python-firestore/issues/227) [#228](https://www.github.com/googleapis/python-firestore/issues/228) [#229](https://www.github.com/googleapis/python-firestore/issues/229)
* add mocks to query get tests ([#109](https://www.github.com/googleapis/python-firestore/issues/109)) ([c4c5bfa](https://www.github.com/googleapis/python-firestore/commit/c4c5bfab0e5942706f2b55148e5e4f9fbd2e29f3))
* async_document docs to match expected usecase ([#129](https://www.github.com/googleapis/python-firestore/issues/129)) ([f26f222](https://www.github.com/googleapis/python-firestore/commit/f26f222a82028568c0974f379454c69a0fc549ca))
* asyncio microgen client get_all type ([#126](https://www.github.com/googleapis/python-firestore/issues/126)) ([9095368](https://www.github.com/googleapis/python-firestore/commit/9095368eaec4271b87ad792ff9bbd065364109f6))
* await on to_wrap in AsyncTransactional ([#147](https://www.github.com/googleapis/python-firestore/issues/147)) ([e640e66](https://www.github.com/googleapis/python-firestore/commit/e640e663f525233a8173767f6886537dfd97b121))
* constructor invalid path tests ([#114](https://www.github.com/googleapis/python-firestore/issues/114)) ([edf7bd1](https://www.github.com/googleapis/python-firestore/commit/edf7bd1879587c05b37910b0a870ba092c6f10ef))
* coverage to 99p ([8ddfe1d](https://www.github.com/googleapis/python-firestore/commit/8ddfe1df7df501524e4d406d9dd3b396fc2680eb))
* harden version data gathering against DistributionNotFound ([#212](https://www.github.com/googleapis/python-firestore/issues/212)) ([20b7260](https://www.github.com/googleapis/python-firestore/commit/20b72603eb0ae3164f68822c62378853be59d232))
* name parameter to indicate snapshot support ([#169](https://www.github.com/googleapis/python-firestore/issues/169)) ([be98897](https://www.github.com/googleapis/python-firestore/commit/be988971cc1bbbc3616a849037dafc8cc0bb5745)), closes [#56](https://www.github.com/googleapis/python-firestore/issues/56)
* pytype client errors ([#146](https://www.github.com/googleapis/python-firestore/issues/146)) ([eb19712](https://www.github.com/googleapis/python-firestore/commit/eb1971274038a079be664004a29a40d9b151d964))
* recover watch stream on more error types ([#9995](https://www.github.com/googleapis/python-firestore/issues/9995)) ([af5fd1d](https://www.github.com/googleapis/python-firestore/commit/af5fd1dabd411a67afa729d1954cb1b9edf4d619)), closes [#L817](https://www.github.com/googleapis/python-firestore/issues/L817)
* remove six dependency ([#110](https://www.github.com/googleapis/python-firestore/issues/110)) ([6e597f2](https://www.github.com/googleapis/python-firestore/commit/6e597f2886ff0cd3a9027c434006af0f0895257b))
* remove six dependency ([#120](https://www.github.com/googleapis/python-firestore/issues/120)) ([d82687d](https://www.github.com/googleapis/python-firestore/commit/d82687db3c55c478285d580547d263f1724a09b7))
* remove six dependency ([#98](https://www.github.com/googleapis/python-firestore/issues/98)) ([b264ccb](https://www.github.com/googleapis/python-firestore/commit/b264ccb9e2618fb7b40d5b4375777363fc26a9a9)), closes [#94](https://www.github.com/googleapis/python-firestore/issues/94)
* remove unnecessary dependency on libcst ([#220](https://www.github.com/googleapis/python-firestore/issues/220)) ([cd358db](https://www.github.com/googleapis/python-firestore/commit/cd358db784c4244271f197156662e38ed21d2f45))
* Support more Python sequence types when encoding to Protobuf ([#21](https://www.github.com/googleapis/python-firestore/issues/21)) ([b1c5987](https://www.github.com/googleapis/python-firestore/commit/b1c5987c606a14874b412e70f93015e161e278d6))
* type hint improvements ([#144](https://www.github.com/googleapis/python-firestore/issues/144)) ([d30fff8](https://www.github.com/googleapis/python-firestore/commit/d30fff8e42621d42d169e354948c26ee3e0d16f0))
* **firestore:** fix get and getall method of transaction ([#16](https://www.github.com/googleapis/python-firestore/issues/16)) ([de3aca0](https://www.github.com/googleapis/python-firestore/commit/de3aca0e78b68f66eb76bc679c6e95b0746ad590))
* **firestore:** fix lint ([#48](https://www.github.com/googleapis/python-firestore/issues/48)) ([7fa00c4](https://www.github.com/googleapis/python-firestore/commit/7fa00c49dc3fab1d687fff9246f3e5ff0682cac0))
* respect transform values passed into collection.add ([#7072](https://www.github.com/googleapis/python-firestore/issues/7072)) ([c643d91](https://www.github.com/googleapis/python-firestore/commit/c643d914075c1bfc2549a56ec419aff90af4d8e7)), closes [#6826](https://www.github.com/googleapis/python-firestore/issues/6826)
* update resume token for restarting BiDi streams ([#10282](https://www.github.com/googleapis/python-firestore/issues/10282)) ([61ec5a2](https://www.github.com/googleapis/python-firestore/commit/61ec5a2326aa101bbccbed229582570844e58bb7))
* Update team to be in correct org ([#43](https://www.github.com/googleapis/python-firestore/issues/43)) ([bef5a3a](https://www.github.com/googleapis/python-firestore/commit/bef5a3af4613b5f9d753bb6f45275e480e4bb301))
* **firestore:** simplify 'Collection.add', avoid spurious API call ([#9634](https://www.github.com/googleapis/python-firestore/issues/9634)) ([20f093e](https://www.github.com/googleapis/python-firestore/commit/20f093eb65014d307e402b774f14958a29043742)), closes [#9629](https://www.github.com/googleapis/python-firestore/issues/9629)


### Reverts

* Revert "Replace relative class refs with fully-qualifed names. (#8039)" (#8095) ([2441825](https://www.github.com/googleapis/python-firestore/commit/24418259483afab8bb9c1996d7bd5d28ab085773)), closes [#8039](https://www.github.com/googleapis/python-firestore/issues/8039) [#8095](https://www.github.com/googleapis/python-firestore/issues/8095)
* Revert "Do not use easily-misread glyphs in Firestore auto-IDs." (#4589) ([bbfd2ff](https://www.github.com/googleapis/python-firestore/commit/bbfd2ffa614c11e294753915d967278b9e0284f0)), closes [#4589](https://www.github.com/googleapis/python-firestore/issues/4589) [#4588](https://www.github.com/googleapis/python-firestore/issues/4588) [#4583](https://www.github.com/googleapis/python-firestore/issues/4583) [#4107](https://www.github.com/googleapis/python-firestore/issues/4107)


* Refactor conformance tests. (#6291) ([4d29c1f](https://www.github.com/googleapis/python-firestore/commit/4d29c1fa7f4a4f10fdafd7797b1f513aa24b7c3c)), closes [#6291](https://www.github.com/googleapis/python-firestore/issues/6291) [#6290](https://www.github.com/googleapis/python-firestore/issues/6290)


### Documentation

* add python 2 sunset banner to documentation ([#9036](https://www.github.com/googleapis/python-firestore/issues/9036)) ([819d154](https://www.github.com/googleapis/python-firestore/commit/819d1541bae21e4054124dd32ff38906d82caca9))
* add upgrading section to index of documentation ([#248](https://www.github.com/googleapis/python-firestore/issues/248)) ([55d1356](https://www.github.com/googleapis/python-firestore/commit/55d1356081c2d2226d7190dac2abdffbf8a0fb2f))
* adds UPGRADING.md, note to readme, to help inform users about migration to v2 ([#245](https://www.github.com/googleapis/python-firestore/issues/245)) ([6a8cbdd](https://www.github.com/googleapis/python-firestore/commit/6a8cbddd01771190c04a5fc065863e8def3eb44f))
* document admin client ([#174](https://www.github.com/googleapis/python-firestore/issues/174)) ([f099736](https://www.github.com/googleapis/python-firestore/commit/f09973638e627f741ea7d1f38294c4f8e9677e53)), closes [#30](https://www.github.com/googleapis/python-firestore/issues/30)
* fix intersphinx reference to requests ([#9294](https://www.github.com/googleapis/python-firestore/issues/9294)) ([e859f3c](https://www.github.com/googleapis/python-firestore/commit/e859f3cb40dae6d9828e01ef28fa2539b978c56f))
* fix typo in watch documentation ([#115](https://www.github.com/googleapis/python-firestore/issues/115)) ([367ac73](https://www.github.com/googleapis/python-firestore/commit/367ac732048e1e96cacb54238f88603ed47e2833))
* normalize use of support level badges ([#6159](https://www.github.com/googleapis/python-firestore/issues/6159)) ([6c9f1ac](https://www.github.com/googleapis/python-firestore/commit/6c9f1acd1394d86e5a632a6e2fe1452b5c5b6b87))
* re-add changelog entries lost in V2 switch ([#178](https://www.github.com/googleapis/python-firestore/issues/178)) ([d4a0f81](https://www.github.com/googleapis/python-firestore/commit/d4a0f8182930e5c74b08ca185c4d94f809b05797)), closes [#177](https://www.github.com/googleapis/python-firestore/issues/177)
* **firestore:** add documentation for Document,Collection .on_snapshot ([#9275](https://www.github.com/googleapis/python-firestore/issues/9275)) ([f250443](https://www.github.com/googleapis/python-firestore/commit/f250443aa292f0aad757d8fd813467159a333bbf))
* **firestore:** add new where operators to docstring ([#9789](https://www.github.com/googleapis/python-firestore/issues/9789)) ([c3864f7](https://www.github.com/googleapis/python-firestore/commit/c3864f743f6fdfbfd2a266712c1764ba23749f8f))
* **firestore:** clarify client threadsafety ([#9254](https://www.github.com/googleapis/python-firestore/issues/9254)) ([4963eee](https://www.github.com/googleapis/python-firestore/commit/4963eee999aa617163db089b6200bb875e5c03fb))
* **firestore:** remove duplicated word in README ([#9297](https://www.github.com/googleapis/python-firestore/issues/9297)) ([250024c](https://www.github.com/googleapis/python-firestore/commit/250024c4e4fdc0186f52a0e224e6f4b3b7e5694e))
* **firestore:** standardize use of 'required' and 'optional' in docstrings; add py2 deprecation warning; add 3.8 unit tests (via synth) ([#10068](https://www.github.com/googleapis/python-firestore/issues/10068)) ([0f72f2c](https://www.github.com/googleapis/python-firestore/commit/0f72f2c25bc6023155be49667cb917a1c217ecd3))
* Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://www.github.com/googleapis/python-firestore/issues/9085)) ([c7b3de8](https://www.github.com/googleapis/python-firestore/commit/c7b3de85ecd5b91b68d4df7a260e25b450e10664))
* Replace links to '/stable/' with '/latest/'. ([#5901](https://www.github.com/googleapis/python-firestore/issues/5901)) ([e2f606e](https://www.github.com/googleapis/python-firestore/commit/e2f606e472d29725247eeb329bd20524f2a68419)), closes [#5894](https://www.github.com/googleapis/python-firestore/issues/5894)

## [2.0.0-dev2](https://www.github.com/googleapis/python-firestore/compare/v1.9.0...v2.0.0-dev2) (2020-10-26)


### ⚠ BREAKING CHANGES

* remove v1beta1 surface for v2 (#96)
* Begin using new microgenerator for v2 firestore (#91)
* from `firestore-0.30.0`: revert to merge not being an option;

### Features

* add `retry`/`timeout` to manual surface ([#222](https://www.github.com/googleapis/python-firestore/issues/222)) ([db5f286](https://www.github.com/googleapis/python-firestore/commit/db5f286772592460b2bf02df25a121994889585d)), closes [#221](https://www.github.com/googleapis/python-firestore/issues/221)
* add support for `not-in` and `not-eq` query operators ([#202](https://www.github.com/googleapis/python-firestore/issues/202)) ([1d09f21](https://www.github.com/googleapis/python-firestore/commit/1d09f21f6c8cb7f69f0e30a960418f0f6899aa01))
* add type hints for method params ([#182](https://www.github.com/googleapis/python-firestore/issues/182)) ([9b6c2f3](https://www.github.com/googleapis/python-firestore/commit/9b6c2f33351c65901ea648e4407b2817e5e70957))
* improve type information ([#176](https://www.github.com/googleapis/python-firestore/issues/176)) ([30bb3fb](https://www.github.com/googleapis/python-firestore/commit/30bb3fb5c36648d3b8acf76349a5726d7a5f135d))
* add support for partition queries ([#210](https://www.github.com/googleapis/python-firestore/issues/210)) ([4f75a75](https://www.github.com/googleapis/python-firestore/commit/4f75a75170be1bbb310b9e4741f4862d694b5bf5))
* use `update_transforms` for mutations ([#219](https://www.github.com/googleapis/python-firestore/issues/219)) ([c122e41](https://www.github.com/googleapis/python-firestore/commit/c122e4186808468a2ff82e9cc54b501809519859)), closes [#217](https://www.github.com/googleapis/python-firestore/issues/217)


### Bug Fixes

* add import message via synth ([#231](https://www.github.com/googleapis/python-firestore/issues/231)) ([5fb02e9](https://www.github.com/googleapis/python-firestore/commit/5fb02e9b9521938ec1040611cf7086077d07aac2)), closes [#227](https://www.github.com/googleapis/python-firestore/issues/227) [#228](https://www.github.com/googleapis/python-firestore/issues/228) [#229](https://www.github.com/googleapis/python-firestore/issues/229)
* harden version data gathering against DistributionNotFound ([#212](https://www.github.com/googleapis/python-firestore/issues/212)) ([20b7260](https://www.github.com/googleapis/python-firestore/commit/20b72603eb0ae3164f68822c62378853be59d232))
* name parameter to indicate snapshot support ([#169](https://www.github.com/googleapis/python-firestore/issues/169)) ([be98897](https://www.github.com/googleapis/python-firestore/commit/be988971cc1bbbc3616a849037dafc8cc0bb5745)), closes [#56](https://www.github.com/googleapis/python-firestore/issues/56)
* remove unnecessary dependency on libcst ([#220](https://www.github.com/googleapis/python-firestore/issues/220)) ([cd358db](https://www.github.com/googleapis/python-firestore/commit/cd358db784c4244271f197156662e38ed21d2f45))


### Documentation

* document admin client ([#174](https://www.github.com/googleapis/python-firestore/issues/174)) ([f099736](https://www.github.com/googleapis/python-firestore/commit/f09973638e627f741ea7d1f38294c4f8e9677e53)), closes [#30](https://www.github.com/googleapis/python-firestore/issues/30)
* re-add changelog entries lost in V2 switch ([#178](https://www.github.com/googleapis/python-firestore/issues/178)) ([d4a0f81](https://www.github.com/googleapis/python-firestore/commit/d4a0f8182930e5c74b08ca185c4d94f809b05797)), closes [#177](https://www.github.com/googleapis/python-firestore/issues/177)

## [2.0.0-dev1](https://www.github.com/googleapis/python-firestore/compare/v1.9.0...v2.0.0-dev1) (2020-08-20)


### ⚠ BREAKING CHANGES

* remove v1beta1 surface for v2 (#96)
* Begin using new microgenerator for v2 firestore (#91)
* from `firestore-0.30.0`: revert to merge not being an option;

### Features

* asyncio microgen collection ([#119](https://www.github.com/googleapis/python-firestore/issues/119)) ([6281a67](https://www.github.com/googleapis/python-firestore/commit/6281a67e0ead38e7b2e477b7f077da7e0457aa9b))
* **firestore:** add `IN`, `ARRAY_CONTAINS_ANY` operators; update docstrings (via synth) ([#9439](https://www.github.com/googleapis/python-firestore/issues/9439)) ([107e526](https://www.github.com/googleapis/python-firestore/commit/107e526cb1d887096e99ce86f7125760b325b2bb))
* add client_options to base client class ([#150](https://www.github.com/googleapis/python-firestore/issues/150)) ([f3bedc1](https://www.github.com/googleapis/python-firestore/commit/f3bedc1efae4430c6853581fafef06d613548314))
* add inline type hints and pytype ci ([#134](https://www.github.com/googleapis/python-firestore/issues/134)) ([afff842](https://www.github.com/googleapis/python-firestore/commit/afff842a3356cbe5b0342be57341c12b2d601fda))
* asyncio microgen batch ([#122](https://www.github.com/googleapis/python-firestore/issues/122)) ([a4e5b00](https://www.github.com/googleapis/python-firestore/commit/a4e5b00a4d59e3416061d5c1ed32a111097e88b3))
* asyncio microgen client ([#118](https://www.github.com/googleapis/python-firestore/issues/118)) ([de4cc44](https://www.github.com/googleapis/python-firestore/commit/de4cc445e34e4a186ccc17bf143e04b45fb35f0b))
* asyncio microgen document ([#121](https://www.github.com/googleapis/python-firestore/issues/121)) ([31faecb](https://www.github.com/googleapis/python-firestore/commit/31faecb2ab2956bad64b0852f1fe54a05d8907f9))
* asyncio microgen query ([#127](https://www.github.com/googleapis/python-firestore/issues/127)) ([178fa2c](https://www.github.com/googleapis/python-firestore/commit/178fa2c2a51a6bd6ef7a3c41b8307e44b5eab062))
* asyncio microgen transaction ([#123](https://www.github.com/googleapis/python-firestore/issues/123)) ([35185a8](https://www.github.com/googleapis/python-firestore/commit/35185a849053877c9cc561e75cdb4cd7338cc508))
* **firestore:** add v1beta1 deprecation annotation ([#34](https://www.github.com/googleapis/python-firestore/issues/34)) ([b9e2ab5](https://www.github.com/googleapis/python-firestore/commit/b9e2ab58a41c7bbab28028cb88f84bd6013816ed))
* **firestore:** surface new 'IN' and 'ARRAY_CONTAINS_ANY' operators ([#9541](https://www.github.com/googleapis/python-firestore/issues/9541)) ([5e9fe4f](https://www.github.com/googleapis/python-firestore/commit/5e9fe4f9ba21b9c38ebd41eb7ed083b335472e0b))
* asyncio system tests ([#132](https://www.github.com/googleapis/python-firestore/issues/132)) ([4256a85](https://www.github.com/googleapis/python-firestore/commit/4256a856e6f1531959ffc080dfc8c8b3a7263ea5))
* Begin using new microgenerator for v2 firestore ([#91](https://www.github.com/googleapis/python-firestore/issues/91)) ([e0add08](https://www.github.com/googleapis/python-firestore/commit/e0add0860ca958d139787cdbb7fceb570fbb80ab))
* create async interface ([#61](https://www.github.com/googleapis/python-firestore/issues/61)) ([eaba25e](https://www.github.com/googleapis/python-firestore/commit/eaba25e892fa33c20ecc7aeab1528a004cbf99f7))
* Create CODEOWNERS ([#40](https://www.github.com/googleapis/python-firestore/issues/40)) ([a0cbf40](https://www.github.com/googleapis/python-firestore/commit/a0cbf403fe88f07c83bec81f275ac168be573e93))
* integrate limit to last ([#145](https://www.github.com/googleapis/python-firestore/issues/145)) ([55da695](https://www.github.com/googleapis/python-firestore/commit/55da695710d0408fc314ffe5cc6d7a48cb71bc3b)), closes [#57](https://www.github.com/googleapis/python-firestore/issues/57)
* remove v1beta1 surface for v2 ([#96](https://www.github.com/googleapis/python-firestore/issues/96)) ([b4a8eb9](https://www.github.com/googleapis/python-firestore/commit/b4a8eb97a68b4c7d1bc9faf0b113dca4476d9f1f))
* use `DatetimeWithNanoseconds` throughout library ([#116](https://www.github.com/googleapis/python-firestore/issues/116)) ([1801ba2](https://www.github.com/googleapis/python-firestore/commit/1801ba2a0e990c533865fef200bbcc3818b3b486))


### Bug Fixes

* add mocks to query get tests ([#109](https://www.github.com/googleapis/python-firestore/issues/109)) ([c4c5bfa](https://www.github.com/googleapis/python-firestore/commit/c4c5bfab0e5942706f2b55148e5e4f9fbd2e29f3))
* async_document docs to match expected usecase ([#129](https://www.github.com/googleapis/python-firestore/issues/129)) ([f26f222](https://www.github.com/googleapis/python-firestore/commit/f26f222a82028568c0974f379454c69a0fc549ca))
* asyncio microgen client get_all type ([#126](https://www.github.com/googleapis/python-firestore/issues/126)) ([9095368](https://www.github.com/googleapis/python-firestore/commit/9095368eaec4271b87ad792ff9bbd065364109f6))
* await on to_wrap in AsyncTransactional ([#147](https://www.github.com/googleapis/python-firestore/issues/147)) ([e640e66](https://www.github.com/googleapis/python-firestore/commit/e640e663f525233a8173767f6886537dfd97b121))
* constructor invalid path tests ([#114](https://www.github.com/googleapis/python-firestore/issues/114)) ([edf7bd1](https://www.github.com/googleapis/python-firestore/commit/edf7bd1879587c05b37910b0a870ba092c6f10ef))
* coverage to 99p ([8ddfe1d](https://www.github.com/googleapis/python-firestore/commit/8ddfe1df7df501524e4d406d9dd3b396fc2680eb))
* pytype client errors ([#146](https://www.github.com/googleapis/python-firestore/issues/146)) ([eb19712](https://www.github.com/googleapis/python-firestore/commit/eb1971274038a079be664004a29a40d9b151d964))
* recover watch stream on more error types ([#9995](https://www.github.com/googleapis/python-firestore/issues/9995)) ([af5fd1d](https://www.github.com/googleapis/python-firestore/commit/af5fd1dabd411a67afa729d1954cb1b9edf4d619)), closes [#L817](https://www.github.com/googleapis/python-firestore/issues/L817)
* remove six dependency ([#110](https://www.github.com/googleapis/python-firestore/issues/110)) ([6e597f2](https://www.github.com/googleapis/python-firestore/commit/6e597f2886ff0cd3a9027c434006af0f0895257b))
* remove six dependency ([#120](https://www.github.com/googleapis/python-firestore/issues/120)) ([d82687d](https://www.github.com/googleapis/python-firestore/commit/d82687db3c55c478285d580547d263f1724a09b7))
* remove six dependency ([#98](https://www.github.com/googleapis/python-firestore/issues/98)) ([b264ccb](https://www.github.com/googleapis/python-firestore/commit/b264ccb9e2618fb7b40d5b4375777363fc26a9a9)), closes [#94](https://www.github.com/googleapis/python-firestore/issues/94)
* respect transform values passed into collection.add ([#7072](https://www.github.com/googleapis/python-firestore/issues/7072)) ([c643d91](https://www.github.com/googleapis/python-firestore/commit/c643d914075c1bfc2549a56ec419aff90af4d8e7)), closes [#6826](https://www.github.com/googleapis/python-firestore/issues/6826)
* Support more Python sequence types when encoding to Protobuf ([#21](https://www.github.com/googleapis/python-firestore/issues/21)) ([b1c5987](https://www.github.com/googleapis/python-firestore/commit/b1c5987c606a14874b412e70f93015e161e278d6))
* type hint improvements ([#144](https://www.github.com/googleapis/python-firestore/issues/144)) ([d30fff8](https://www.github.com/googleapis/python-firestore/commit/d30fff8e42621d42d169e354948c26ee3e0d16f0))
* update resume token for restarting BiDi streams ([#10282](https://www.github.com/googleapis/python-firestore/issues/10282)) ([61ec5a2](https://www.github.com/googleapis/python-firestore/commit/61ec5a2326aa101bbccbed229582570844e58bb7))
* **firestore:** fix get and getall method of transaction ([#16](https://www.github.com/googleapis/python-firestore/issues/16)) ([de3aca0](https://www.github.com/googleapis/python-firestore/commit/de3aca0e78b68f66eb76bc679c6e95b0746ad590))
* **firestore:** fix lint ([#48](https://www.github.com/googleapis/python-firestore/issues/48)) ([7fa00c4](https://www.github.com/googleapis/python-firestore/commit/7fa00c49dc3fab1d687fff9246f3e5ff0682cac0))
* **firestore:** simplify 'Collection.add', avoid spurious API call ([#9634](https://www.github.com/googleapis/python-firestore/issues/9634)) ([20f093e](https://www.github.com/googleapis/python-firestore/commit/20f093eb65014d307e402b774f14958a29043742)), closes [#9629](https://www.github.com/googleapis/python-firestore/issues/9629)
* Update team to be in correct org ([#43](https://www.github.com/googleapis/python-firestore/issues/43)) ([bef5a3a](https://www.github.com/googleapis/python-firestore/commit/bef5a3af4613b5f9d753bb6f45275e480e4bb301))


### Documentation

* add python 2 sunset banner to documentation ([#9036](https://www.github.com/googleapis/python-firestore/issues/9036)) ([819d154](https://www.github.com/googleapis/python-firestore/commit/819d1541bae21e4054124dd32ff38906d82caca9))
* fix intersphinx reference to requests ([#9294](https://www.github.com/googleapis/python-firestore/issues/9294)) ([e859f3c](https://www.github.com/googleapis/python-firestore/commit/e859f3cb40dae6d9828e01ef28fa2539b978c56f))
* **firestore:** clarify client threadsafety ([#9254](https://www.github.com/googleapis/python-firestore/issues/9254)) ([4963eee](https://www.github.com/googleapis/python-firestore/commit/4963eee999aa617163db089b6200bb875e5c03fb))
* fix typo in watch documentation ([#115](https://www.github.com/googleapis/python-firestore/issues/115)) ([367ac73](https://www.github.com/googleapis/python-firestore/commit/367ac732048e1e96cacb54238f88603ed47e2833))
* normalize use of support level badges ([#6159](https://www.github.com/googleapis/python-firestore/issues/6159)) ([6c9f1ac](https://www.github.com/googleapis/python-firestore/commit/6c9f1acd1394d86e5a632a6e2fe1452b5c5b6b87))
* Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://www.github.com/googleapis/python-firestore/issues/9085)) ([c7b3de8](https://www.github.com/googleapis/python-firestore/commit/c7b3de85ecd5b91b68d4df7a260e25b450e10664))
* Replace links to '/stable/' with '/latest/'. ([#5901](https://www.github.com/googleapis/python-firestore/issues/5901)) ([e2f606e](https://www.github.com/googleapis/python-firestore/commit/e2f606e472d29725247eeb329bd20524f2a68419)), closes [#5894](https://www.github.com/googleapis/python-firestore/issues/5894)
* **firestore:** add documentation for Document,Collection .on_snapshot ([#9275](https://www.github.com/googleapis/python-firestore/issues/9275)) ([f250443](https://www.github.com/googleapis/python-firestore/commit/f250443aa292f0aad757d8fd813467159a333bbf))
* **firestore:** add new where operators to docstring ([#9789](https://www.github.com/googleapis/python-firestore/issues/9789)) ([c3864f7](https://www.github.com/googleapis/python-firestore/commit/c3864f743f6fdfbfd2a266712c1764ba23749f8f))
* **firestore:** remove duplicated word in README ([#9297](https://www.github.com/googleapis/python-firestore/issues/9297)) ([250024c](https://www.github.com/googleapis/python-firestore/commit/250024c4e4fdc0186f52a0e224e6f4b3b7e5694e))
* **firestore:** standardize use of 'required' and 'optional' in docstrings; add py2 deprecation warning; add 3.8 unit tests (via synth) ([#10068](https://www.github.com/googleapis/python-firestore/issues/10068)) ([0f72f2c](https://www.github.com/googleapis/python-firestore/commit/0f72f2c25bc6023155be49667cb917a1c217ecd3))

### Tests
* Refactor conformance tests. (#6291) ([4d29c1f](https://www.github.com/googleapis/python-firestore/commit/4d29c1fa7f4a4f10fdafd7797b1f513aa24b7c3c)), closes [#6291](https://www.github.com/googleapis/python-firestore/issues/6291) [#6290](https://www.github.com/googleapis/python-firestore/issues/6290)


## [1.9.0](https://www.github.com/googleapis/python-firestore/compare/v1.8.1...v1.9.0) (2020-08-13)


### Features

* **firestore:** add client_options to base class ([#148](https://www.github.com/googleapis/python-firestore/issues/148)) ([91d6580](https://www.github.com/googleapis/python-firestore/commit/91d6580e2903ab55798d66bc53541faa86ca76fe))


### [1.8.1](https://www.github.com/googleapis/python-firestore/compare/v1.8.0...v1.8.1) (2020-07-07)


### Bug Fixes

* **#82:** Add import back to generated client ([#83](https://www.github.com/googleapis/python-firestore/issues/83)) ([2d0ee60](https://www.github.com/googleapis/python-firestore/commit/2d0ee603926ffad484c9874e8745ea97d3c384eb)), closes [#82](https://www.github.com/googleapis/python-firestore/issues/82)


## [1.8.0](https://www.github.com/googleapis/python-firestore/compare/v1.7.0...v1.8.0) (2020-07-06)


### Features

* support limit to last feature ([#57](https://www.github.com/googleapis/python-firestore/issues/57)) ([8c75e21](https://www.github.com/googleapis/python-firestore/commit/8c75e218331fda25ea3a789e84ba8dc11af2db02))
* **firestore:** add support of emulator to run system tests on emulator ([#31](https://www.github.com/googleapis/python-firestore/issues/31)) ([891edc7](https://www.github.com/googleapis/python-firestore/commit/891edc7a9fd576cf0b61286502b0ba02223f89c6))
* **firestore:** add v1beta1 deprecation annotation ([#34](https://www.github.com/googleapis/python-firestore/issues/34)) ([b9e2ab5](https://www.github.com/googleapis/python-firestore/commit/b9e2ab58a41c7bbab28028cb88f84bd6013816ed))
* **v1:** add batch write ([#62](https://www.github.com/googleapis/python-firestore/issues/62)) ([1415bc4](https://www.github.com/googleapis/python-firestore/commit/1415bc47a7b9742c4a522ab2be67bbcb5ce39db4))


### Bug Fixes

* Support more Python sequence types when encoding to Protobuf ([#21](https://www.github.com/googleapis/python-firestore/issues/21)) ([b1c5987](https://www.github.com/googleapis/python-firestore/commit/b1c5987c606a14874b412e70f93015e161e278d6))
* **firestore:** use specific naming convention ([#58](https://www.github.com/googleapis/python-firestore/issues/58)) ([c97a168](https://www.github.com/googleapis/python-firestore/commit/c97a168d9b1e4f2cd8625b02f66d6978381652dd))


### Documentation

* **firestore:** on_snapshot document changes ([#79](https://www.github.com/googleapis/python-firestore/issues/79)) ([c556fc5](https://www.github.com/googleapis/python-firestore/commit/c556fc5c656ed313c2b1d3eb37435c694601ee11))


## [1.7.0](https://www.github.com/googleapis/python-firestore/compare/v1.6.2...v1.7.0) (2020-05-18)


### Features

* Create CODEOWNERS ([#40](https://www.github.com/googleapis/python-firestore/issues/40)) ([a0cbf40](https://www.github.com/googleapis/python-firestore/commit/a0cbf403fe88f07c83bec81f275ac168be573e93))


### Bug Fixes

* **firestore:** fix get and getall method of transaction ([#16](https://www.github.com/googleapis/python-firestore/issues/16)) ([de3aca0](https://www.github.com/googleapis/python-firestore/commit/de3aca0e78b68f66eb76bc679c6e95b0746ad590))
* Update team to be in correct org ([#43](https://www.github.com/googleapis/python-firestore/issues/43)) ([bef5a3a](https://www.github.com/googleapis/python-firestore/commit/bef5a3af4613b5f9d753bb6f45275e480e4bb301))
* **firestore:** fix lint ([#48](https://www.github.com/googleapis/python-firestore/issues/48)) ([7fa00c4](https://www.github.com/googleapis/python-firestore/commit/7fa00c49dc3fab1d687fff9246f3e5ff0682cac0))

### [1.6.2](https://www.github.com/googleapis/python-firestore/compare/v1.6.1...v1.6.2) (2020-01-31)


### Bug Fixes

* update resume token for restarting BiDi streams ([#10282](https://www.github.com/googleapis/python-firestore/issues/10282)) ([61ec5a2](https://www.github.com/googleapis/python-firestore/commit/61ec5a2326aa101bbccbed229582570844e58bb7))

## 1.6.1

01-02-2020 10:35 PST


### Implementation Changes
- Recover watch streams on more error types ([#9995](https://github.com/googleapis/google-cloud-python/pull/9995))
- Simplify 'Collection.add' and avoid a spurious API call ([#9634](https://github.com/googleapis/google-cloud-python/pull/9634))

### Documentation
- Add new where operators to docstring ([#9789](https://github.com/googleapis/google-cloud-python/pull/9789))
- Change spacing in docs templates (via synth) ([#9750](https://github.com/googleapis/google-cloud-python/pull/9750))
- Add python 2 sunset banner to documentation ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))

## 1.6.0

11-06-2019 13:49 PST

### New Features
- Surface new 'IN' and 'ARRAY_CONTAINS_ANY' query operators. ([#9541](https://github.com/googleapis/google-cloud-python/pull/9541))

## 1.5.0

10-15-2019 06:45 PDT


### Implementation Changes
- Expand dotted keys in mappings used as cursors. ([#8568](https://github.com/googleapis/google-cloud-python/pull/8568))
- Tweak GAPIC client configuration (via synth). ([#9173](https://github.com/googleapis/google-cloud-python/pull/9173))

### New Features
- Add `IN`, `ARRAY_CONTAINS_ANY` operators; update docstrings (via synth). ([#9439](https://github.com/googleapis/google-cloud-python/pull/9439))
- Add `COLLECTION_GROUP` to `Index.QueryScope` enum; update docstrings (via synth). ([#9253](https://github.com/googleapis/google-cloud-python/pull/9253))
- Add `client_options` to v1 client. ([#9048](https://github.com/googleapis/google-cloud-python/pull/9048))

### Dependencies
- Pin 'google-cloud-core >= 1.0.3, < 2.0.0dev'. ([#9445](https://github.com/googleapis/google-cloud-python/pull/9445))

### Documentation
- Update README example to use non-deprecated `query.get`. ([#9235](https://github.com/googleapis/google-cloud-python/pull/9235))
- Remove duplicated word in README. ([#9297](https://github.com/googleapis/google-cloud-python/pull/9297))
- Fix intersphinx reference to `requests`. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core refs`. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Add license file. ([#9109](https://github.com/googleapis/google-cloud-python/pull/9109))
- Fix reference to library name ([#9047](https://github.com/googleapis/google-cloud-python/pull/9047))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

## 1.4.0

08-06-2019 11:43 PDT

### New Features
- Support emulator in client. ([#8721](https://github.com/googleapis/google-cloud-python/pull/8721))
- Add GAPIC client for Admin V1. ([#8667](https://github.com/googleapis/google-cloud-python/pull/8667))
- Add `Transaction.get` / `Transaction.get_all`. ([#8628](https://github.com/googleapis/google-cloud-python/pull/8628))

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8955](https://github.com/googleapis/google-cloud-python/pull/8955))
- Deprecate `v1beta1` API / client. ([#8886](https://github.com/googleapis/google-cloud-python/pull/8886))
- Allow snapshot cursors from other collections for collection group queries. ([#8882](https://github.com/googleapis/google-cloud-python/pull/8882))
- Fix sorting `delete_changes` in `Watch._compute_snapshot`. ([#8809](https://github.com/googleapis/google-cloud-python/pull/8809))
- Treat `None` as EOF in `Watch.on_snapshot`. ([#8687](https://github.com/googleapis/google-cloud-python/pull/8687))
- Fix V1 `Client.collections` method. ([#8718](https://github.com/googleapis/google-cloud-python/pull/8718))
- Avoid adding `prefix` to update mask for transforms used in `update`. ([#8701](https://github.com/googleapis/google-cloud-python/pull/8701))
- Add `should_terminate` predicate for clean BiDi shutdown. ([#8650](https://github.com/googleapis/google-cloud-python/pull/8650))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Preserve manual change in noxfile (run systests verbosely). ([#8744](https://github.com/googleapis/google-cloud-python/pull/8744))
- Update V1 conformance tests to match new repo / format. ([#8689](https://github.com/googleapis/google-cloud-python/pull/8689))
- Improve cleanups for `watch` system tests. ([#8638](https://github.com/googleapis/google-cloud-python/pull/8638))
- Avoid sharing top-level collection across test cases / CI runs. ([#8637](https://github.com/googleapis/google-cloud-python/pull/8637))

## 1.3.0

07-09-2019 13:19 PDT


### Implementation Changes
- Add missing transforms to 'google.cloud.firestore' shim. ([#8481](https://github.com/googleapis/google-cloud-python/pull/8481))
- Preserve reference to missing documents in 'Client.get_all'. ([#8472](https://github.com/googleapis/google-cloud-python/pull/8472))
- Add gRPC keepalive to gapic client initialization. ([#8264](https://github.com/googleapis/google-cloud-python/pull/8264))
- Add disclaimer to auto-generated template files. ([#8314](https://github.com/googleapis/google-cloud-python/pull/8314))
- Use correct environment variable to guard the 'system' part. ([#7912](https://github.com/googleapis/google-cloud-python/pull/7912))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8509](https://github.com/googleapis/google-cloud-python/pull/8509))
- Allow kwargs to be passed to create_channel (via synth). ([#8390](https://github.com/googleapis/google-cloud-python/pull/8390))
- Add 'FieldPath.documentId()'. ([#8543](https://github.com/googleapis/google-cloud-python/pull/8543))

### Documentation
- Fix docstring example for 'Client.collection_group'. ([#8438](https://github.com/googleapis/google-cloud-python/pull/8438))
- Normalize docstring class refs. ([#8102](https://github.com/googleapis/google-cloud-python/pull/8102))

### Internal / Testing Changes
- Pin black version (via synth). ([#8583](https://github.com/googleapis/google-cloud-python/pull/8583))
- All: Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8352](https://github.com/googleapis/google-cloud-python/pull/8352))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8241](https://github.com/googleapis/google-cloud-python/pull/8241))
- Blacken noxfile.py, setup.py (via synth). ([#8123](https://github.com/googleapis/google-cloud-python/pull/8123))
- Add empty lines (via synth). ([#8058](https://github.com/googleapis/google-cloud-python/pull/8058))

## 1.2.0

05-16-2019 12:25 PDT


### New Features
- Add support for numeric transforms: `increment` / `maximum` / `minimum`. ([#7989](https://github.com/googleapis/google-cloud-python/pull/7989))
- Add `client_info` support to V1 client. ([#7877](https://github.com/googleapis/google-cloud-python/pull/7877)) and ([#7898](https://github.com/googleapis/google-cloud-python/pull/7898))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Internal / Testing Changes
- Add nox session `docs`,  add routing header to method metadata, reorder methods (via synth).. ([#7771](https://github.com/googleapis/google-cloud-python/pull/7771))

## 1.1.0

04-30-2019 12:29 PDT


### New Features
- Add support for CollectionGroup queries. ([#7758](https://github.com/googleapis/google-cloud-python/pull/7758))

## 1.0.0

04-30-2019 10:00 PDT

### Implementation Changes
- Use parent path for watch on queries. ([#7752](https://github.com/googleapis/google-cloud-python/pull/7752))
- Add routing header to method metadata (via synth). ([#7749](https://github.com/googleapis/google-cloud-python/pull/7749))

## 0.32.1

04-05-2019 10:51 PDT


### Dependencies
- Update google-api-core dependency

## 0.32.0

04-01-2019 11:44 PDT


### Implementation Changes
- Allow passing metadata as part of creating a bidi ([#7514](https://github.com/googleapis/google-cloud-python/pull/7514))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Rename 'Query.get' -> 'stream'. ([#7284](https://github.com/googleapis/google-cloud-python/pull/7284))
- Remove bogus error checking of query response stream. ([#7206](https://github.com/googleapis/google-cloud-python/pull/7206))
-'increment' / 'minimum' / 'maximum' field transform attributes. ([#7129](https://github.com/googleapis/google-cloud-python/pull/7129))
- Respect transform values passed into collection.add ([#7072](https://github.com/googleapis/google-cloud-python/pull/7072))
- Protoc-generated serialization update. ([#7083](https://github.com/googleapis/google-cloud-python/pull/7083))

### New Features
- Firestore: Add v1 API version. ([#7494](https://github.com/googleapis/google-cloud-python/pull/7494))
- Add 'Collection.list_documents' method. ([#7221](https://github.com/googleapis/google-cloud-python/pull/7221))
- Add 'DocumentReference.path' property. ([#7219](https://github.com/googleapis/google-cloud-python/pull/7219))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Fix the docstring example for 'Query.on_snapshot'.  ([#7281](https://github.com/googleapis/google-cloud-python/pull/7281))
- Update copyright headers

### Internal / Testing Changes
- Fix typo in proto comments (via synth).
- Prep firestore unit tests for generation from 'v1' protos. ([#7437](https://github.com/googleapis/google-cloud-python/pull/7437))
- Copy lintified proto files (via synth). ([#7466](https://github.com/googleapis/google-cloud-python/pull/7466))
- Add clarifying comment to blacken nox target. ([#7392](https://github.com/googleapis/google-cloud-python/pull/7392))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.31.0

12-18-2018 11:20 PST


### Implementation Changes
- Implement equality semantics for public types ([#6916](https://github.com/googleapis/google-cloud-python/pull/6916))
- Pick up stub docstring fix in GAPIC generator. ([#6988](https://github.com/googleapis/google-cloud-python/pull/6988))
- Use 'DatetimeWithNanos' for converting timestamp messages. ([#6920](https://github.com/googleapis/google-cloud-python/pull/6920))
- Enable use of 'WriteBatch' as a context manager. ([#6912](https://github.com/googleapis/google-cloud-python/pull/6912))
- Document timeouts for 'Query.get' / 'Collection.get'. ([#6853](https://github.com/googleapis/google-cloud-python/pull/6853))
- Normalize FieldPath parsing / escaping ([#6904](https://github.com/googleapis/google-cloud-python/pull/6904))
- For queries ordered on `__name__`, expand field values to full paths. ([#6829](https://github.com/googleapis/google-cloud-python/pull/6829))
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Prevent use of transforms as values passed to 'Query.where'. ([#6703](https://github.com/googleapis/google-cloud-python/pull/6703))
- 'Query.select([])' implies `__name__`. ([#6735](https://github.com/googleapis/google-cloud-python/pull/6735))
- Reject invalid paths passed to 'Query.{select,where,order_by}' ([#6770](https://github.com/googleapis/google-cloud-python/pull/6770))
- Prevent use of transforms as cursor values. ([#6706](https://github.com/googleapis/google-cloud-python/pull/6706))
- Refactor 'Document.get' to use the 'GetDocument' API. ([#6534](https://github.com/googleapis/google-cloud-python/pull/6534))
- Pick up enum fixes in the GAPIC generator. ([#6612](https://github.com/googleapis/google-cloud-python/pull/6612))
- Pick up changes to GAPIC client config. ([#6589](https://github.com/googleapis/google-cloud-python/pull/6589))
- Suppress deprecation warnings for 'assertRaisesRegexp'. ([#6543](https://github.com/googleapis/google-cloud-python/pull/6543))
- Firestore: pick up fixes to GAPIC generator. ([#6523](https://github.com/googleapis/google-cloud-python/pull/6523))
- Fix `client_info` bug, update docstrings. ([#6412](https://github.com/googleapis/google-cloud-python/pull/6412))
- Block calling 'DocumentRef.get()' with a single string. ([#6270](https://github.com/googleapis/google-cloud-python/pull/6270))

### New Features
- Impose required semantics for snapshots as cursors: ([#6837](https://github.com/googleapis/google-cloud-python/pull/6837))
- Make cursor-related 'Query' methods accept lists ([#6697](https://github.com/googleapis/google-cloud-python/pull/6697))
- Add 'Client.collections' method. ([#6650](https://github.com/googleapis/google-cloud-python/pull/6650))
- Add support for 'ArrayRemove' / 'ArrayUnion' transforms ([#6651](https://github.com/googleapis/google-cloud-python/pull/6651))
- Add support for `array_contains` query operator. ([#6481](https://github.com/googleapis/google-cloud-python/pull/6481))
- Add Watch Support ([#6191](https://github.com/googleapis/google-cloud-python/pull/6191))
- Remove use of deprecated 'channel' argument. ([#6271](https://github.com/googleapis/google-cloud-python/pull/6271))

### Dependencies
- Pin 'google-api_core >= 1.7.0'. ([#6937](https://github.com/googleapis/google-cloud-python/pull/6937))
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Nnormalize docs for `page_size` / `max_results` / `page_token`. ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))
- Port changelog from 30.1 branch to main ([#6903](https://github.com/googleapis/google-cloud-python/pull/6903))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Add driver for listen conformance tests. ([#6935](https://github.com/googleapis/google-cloud-python/pull/6935))
- Add driver for query conformance tests. ([#6839](https://github.com/googleapis/google-cloud-python/pull/6839))
- Update noxfile.
- Blacken libraries ([#6794](https://github.com/googleapis/google-cloud-python/pull/6794))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Fix delete conformance ([#6559](https://github.com/googleapis/google-cloud-python/pull/6559))
- Add synth metadata. ([#6567](https://github.com/googleapis/google-cloud-python/pull/6567))
- Refactor conformance tests. ([#6291](https://github.com/googleapis/google-cloud-python/pull/6291))
- Import stdlib ABCs from 'collections.abc' rather than 'collections'. ([#6451](https://github.com/googleapis/google-cloud-python/pull/6451))
- Fix path of tests-to-include in MANIFEST.in ([#6381](https://github.com/googleapis/google-cloud-python/pull/6381))
- Fix error from new flake8 version. ([#6320](https://github.com/googleapis/google-cloud-python/pull/6320))

## 0.30.1

12-11-2018 10:49 PDT
 

### Dependencies
- Update `core` and `api_core` dependencies to latest versions.

## 0.30.0

10-15-2018 09:04 PDT


### New Features
- Add `Document.collections` method. ([#5613](https://github.com/googleapis/google-cloud-python/pull/5613))
- Add `merge` as an option to `DocumentReference.set()` ([#4851](https://github.com/googleapis/google-cloud-python/pull/4851))
- Return emtpy snapshot instead of raising NotFound exception ([#5007](https://github.com/googleapis/google-cloud-python/pull/5007))
- Add Field path class ([#4392](https://github.com/googleapis/google-cloud-python/pull/4392))

### Implementation Changes
- Avoid overwriting `__module__` of messages from shared modules. ([#5364](https://github.com/googleapis/google-cloud-python/pull/5364))
- Don't omit originally-empty map values when processing timestamps. ([#6050](https://github.com/googleapis/google-cloud-python/pull/6050))

### Documentation
- Prep docs for repo split. ([#6000](https://github.com/googleapis/google-cloud-python/pull/6000))
- Docs: Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))
- Document `FieldPath.from_string` ([#5121](https://github.com/googleapis/google-cloud-python/pull/5121))

### Internal / Testing Changes
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add new conformance tests. ([#6124](https://github.com/googleapis/google-cloud-python/pull/6124))
- Add `synth.py`. ([#6079](https://github.com/googleapis/google-cloud-python/pull/6079))
- Test document update w/ integer ids ([#5895](https://github.com/googleapis/google-cloud-python/pull/5895))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Re-sync with .proto / .textproto files from google-cloud-common. ([#5351](https://github.com/googleapis/google-cloud-python/pull/5351))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/googleapis/google-cloud-python/pull/5304))
- Add test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix over-long line. ([#5129](https://github.com/googleapis/google-cloud-python/pull/5129))
- Distinguish `FieldPath` classes from field path strings ([#4466](https://github.com/googleapis/google-cloud-python/pull/4466))
- Fix bad trove classifier
- Cleanup `FieldPath` ([#4996](https://github.com/googleapis/google-cloud-python/pull/4996))
- Fix typo in `Document.collections` docstring. ([#5669](https://github.com/googleapis/google-cloud-python/pull/5669))
- Implement `FieldPath.__add__` ([#5149](https://github.com/googleapis/google-cloud-python/pull/5149))

## 0.29.0

### New features

- All non-simple field names are converted into unicode (#4859)

### Implementation changes

- The underlying generated code has been re-generated to pick up new features and bugfixes. (#4916)
- The `Admin` API interface has been temporarily removed.

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)
- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Documentation

- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- System test fix, changed ALREADY_EXISTS and MISSING_ENTITY to DOCUMENT_EXISTS and MISSING_DOCUMENT and updated wording (#4803)
- Cross-language tests (#4359)
- Fix import column lengths pass 79 (#4464)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-firestore/0.28.0/
