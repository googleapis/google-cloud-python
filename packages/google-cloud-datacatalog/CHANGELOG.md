# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-datacatalog/#history

## [3.5.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.3...v3.5.0) (2021-10-28)


### Features

* add context manager support in client ([#240](https://www.github.com/googleapis/python-datacatalog/issues/240)) ([c403d1d](https://www.github.com/googleapis/python-datacatalog/commit/c403d1d5a637b23343b23e74debed5f8b4c5c12a))

### [3.4.3](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.2...v3.4.3) (2021-10-05)


### Bug Fixes

* improper types in pagers generation ([322cf9e](https://www.github.com/googleapis/python-datacatalog/commit/322cf9e543147b0b40e3b044e5822acf12e2d216))

### [3.4.2](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.1...v3.4.2) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([27fcefa](https://www.github.com/googleapis/python-datacatalog/commit/27fcefa6df0d9a3a1c0954dd908b9aa3ad1bf548))


### Documentation

* **samples:** add entry group greation to custom entry sample ([#215](https://www.github.com/googleapis/python-datacatalog/issues/215)) ([24d78cf](https://www.github.com/googleapis/python-datacatalog/commit/24d78cf44dd0a4e29aa66daec137e8a618b60f29))

### [3.4.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.4.0...v3.4.1) (2021-09-01)


### Bug Fixes

* make datacatalog == datacatalog_v1 ([#206](https://www.github.com/googleapis/python-datacatalog/issues/206)) ([aefe892](https://www.github.com/googleapis/python-datacatalog/commit/aefe892ab2cdb37b5f58faecd45758ea685c74ec))


### Documentation

* **samples:** add samples from docs & reorganize all samples for testing ([#78](https://www.github.com/googleapis/python-datacatalog/issues/78)) ([d34aca0](https://www.github.com/googleapis/python-datacatalog/commit/d34aca05a87aa75ad982612f57fe987a005f7896))

## [3.4.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.3.2...v3.4.0) (2021-07-28)


### Features

* Added ReplaceTaxonomy in Policy Tag Manager Serialization API ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for BigQuery connections entries ([#196](https://www.github.com/googleapis/python-datacatalog/issues/196)) ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for BigQuery routines entries ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for public tag templates ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added support for rich text tags ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))
* Added usage_signal field ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))


### Documentation

* Documentation improvements ([6abe29d](https://www.github.com/googleapis/python-datacatalog/commit/6abe29d21c7481aa836a103d99722adcfbf6a6d3))

### [3.3.2](https://www.github.com/googleapis/python-datacatalog/compare/v3.3.1...v3.3.2) (2021-07-27)


### Bug Fixes

* enable self signed jwt for grpc ([#192](https://www.github.com/googleapis/python-datacatalog/issues/192)) ([90a0be2](https://www.github.com/googleapis/python-datacatalog/commit/90a0be276e38e889a5086f8fd233d5b25e19965e))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#187](https://www.github.com/googleapis/python-datacatalog/issues/187)) ([317b207](https://www.github.com/googleapis/python-datacatalog/commit/317b207ef03ecedb84bd4619da71859b9ec1d6db))


### Miscellaneous Chores

* release as 3.3.2 ([#193](https://www.github.com/googleapis/python-datacatalog/issues/193)) ([7f38774](https://www.github.com/googleapis/python-datacatalog/commit/7f38774e4831122f5b645b911eed0f673e0f182f))

### [3.3.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.3.0...v3.3.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#186](https://www.github.com/googleapis/python-datacatalog/issues/186)) ([915f387](https://www.github.com/googleapis/python-datacatalog/commit/915f3875bf8496203aa6bc4ee6ce11fde33f65e9))

## [3.3.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.2.1...v3.3.0) (2021-07-01)


### Features

* add always_use_jwt_access ([#178](https://www.github.com/googleapis/python-datacatalog/issues/178)) ([2cb3cc2](https://www.github.com/googleapis/python-datacatalog/commit/2cb3cc2e062045b4b1f602c6e2ed79b3dc6f0014))


### Bug Fixes

* disable always_use_jwt_access ([#182](https://www.github.com/googleapis/python-datacatalog/issues/182)) ([1bef446](https://www.github.com/googleapis/python-datacatalog/commit/1bef4465d7c0f7f4e84afb664ca5d9f55e92ea14))


### Documentation

* omit mention of Python 2.7 in 'CONTRIBUTING.rst' ([#1127](https://www.github.com/googleapis/python-datacatalog/issues/1127)) ([#173](https://www.github.com/googleapis/python-datacatalog/issues/173)) ([a3d17d4](https://www.github.com/googleapis/python-datacatalog/commit/a3d17d4b485e757480040783259da234abec69a0)), closes [#1126](https://www.github.com/googleapis/python-datacatalog/issues/1126)

### [3.2.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.2.0...v3.2.1) (2021-06-09)


### Bug Fixes

* **deps:** add packaging requirement ([#163](https://www.github.com/googleapis/python-datacatalog/issues/163)) ([1cfdb5a](https://www.github.com/googleapis/python-datacatalog/commit/1cfdb5a444cd6c845546b060da2e0a0f7d533a0c))

## [3.2.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.1.1...v3.2.0) (2021-05-18)


### Features

* support self-signed JWT flow for service accounts ([85e46e1](https://www.github.com/googleapis/python-datacatalog/commit/85e46e144d32a0d66bc2d7c056453951eb77d592))


### Bug Fixes

* add async client to %name_%version/init.py ([85e46e1](https://www.github.com/googleapis/python-datacatalog/commit/85e46e144d32a0d66bc2d7c056453951eb77d592))

### [3.1.1](https://www.github.com/googleapis/python-datacatalog/compare/v3.1.0...v3.1.1) (2021-03-29)


### Bug Fixes

* use correct retry deadline ([#124](https://www.github.com/googleapis/python-datacatalog/issues/124)) ([0c69bc2](https://www.github.com/googleapis/python-datacatalog/commit/0c69bc2fbae593f62c543c5a15dbe810467b7510))

## [3.1.0](https://www.github.com/googleapis/python-datacatalog/compare/v3.0.0...v3.1.0) (2021-03-22)


### Features

* add `client_cert_source_for_mtls` argument to transports ([#107](https://www.github.com/googleapis/python-datacatalog/issues/107)) ([59a44bc](https://www.github.com/googleapis/python-datacatalog/commit/59a44bc744a6322a2a23313c851eb77204110e79))


### Bug Fixes

* remove gRPC send/recv limit; add enums to `types/__init__.py` ([#87](https://www.github.com/googleapis/python-datacatalog/issues/87)) ([e0c40c7](https://www.github.com/googleapis/python-datacatalog/commit/e0c40c765242868570532b5074fd239aa2c259e9))


### Documentation

* document enum values with `undoc-members` option ([#93](https://www.github.com/googleapis/python-datacatalog/issues/93)) ([2dbb3ef](https://www.github.com/googleapis/python-datacatalog/commit/2dbb3ef062b52925ad421c5c469ed6e67671e878))
* fix `type_` attribute name in the migration guide ([#113](https://www.github.com/googleapis/python-datacatalog/issues/113)) ([2f98f22](https://www.github.com/googleapis/python-datacatalog/commit/2f98f2244271d92f79fdb26103478166958b8c8a))
* fix upgrade guide ([#114](https://www.github.com/googleapis/python-datacatalog/issues/114)) ([4bfa587](https://www.github.com/googleapis/python-datacatalog/commit/4bfa587903105cb3de2272618374df0b04156017))
* update the upgrade guide to be from 1.0 to 3.0 ([#77](https://www.github.com/googleapis/python-datacatalog/issues/77)) ([eed034a](https://www.github.com/googleapis/python-datacatalog/commit/eed034a3969913e40554300ae97c5e00e4fcc79a))

## [3.0.0](https://www.github.com/googleapis/python-datacatalog/compare/v2.0.0...v3.0.0) (2020-11-17)


### ⚠ BREAKING CHANGES

* add common resource paths; expose client transport; rename ``type`` attributes to ``type_`` to avoid name collisions. (#64)

  Renamed attributes:
    * `TagTemplateField.type` -> `TagTemplatedField.type_`
    * `ColumnSchema.type` -> `ColumnSchema.type_`
    * `Entry.type` -> `Entry.type_`


### Features

* add common resource paths; expose client transport; rename ``type`` attributes to ``type_`` to avoid name collisions ([#64](https://www.github.com/googleapis/python-datacatalog/issues/64)) ([f8f797a](https://www.github.com/googleapis/python-datacatalog/commit/f8f797af757f643c4414e3c7a58b3423b3d80d6f))

## [2.0.0](https://www.github.com/googleapis/python-datacatalog/compare/v1.0.0...v2.0.0) (2020-08-20)


### ⚠ BREAKING CHANGES

* This release has breaking changes. See the [2.0.0 Migration Guide](https://github.com/googleapis/python-datacatalog/blob/main/UPGRADING.md) for details.

### Features

* Migrate API client to Microgenerator ([#54](https://www.github.com/googleapis/python-datacatalog/issues/54)) ([14fbdb8](https://www.github.com/googleapis/python-datacatalog/commit/14fbdb811688296e3978b4dfe7d4c240b5b1da5d))


### Bug Fixes

* update retry config ([#47](https://www.github.com/googleapis/python-datacatalog/issues/47)) ([1c56be7](https://www.github.com/googleapis/python-datacatalog/commit/1c56be78f1aae8dd5cd93e81188135d72cc80fdc))


### Documentation

* fix readme link ([#58](https://www.github.com/googleapis/python-datacatalog/issues/58)) ([55da34c](https://www.github.com/googleapis/python-datacatalog/commit/55da34caac42dd5959c046a50ba79375f7a41788))

## [1.0.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.8.0...v1.0.0) (2020-06-17)


### Features

* release as production/stable ([#25](https://www.github.com/googleapis/python-datacatalog/issues/25)) ([6d4c3df](https://www.github.com/googleapis/python-datacatalog/commit/6d4c3df232ba933e16780231b92c830453206170)), closes [#24](https://www.github.com/googleapis/python-datacatalog/issues/24)

## [0.8.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.7.0...v0.8.0) (2020-05-20)


### Features

* add `restricted_locations` to v1; add `order` to `TagField` and `TagTemplateField` in v1beta1; rename `field_path` to `tag_template_field_path` in v1beta1; add pagination support to `list_taxonomies` in v1beta1 ([#20](https://www.github.com/googleapis/python-datacatalog/issues/20)) ([7a890c2](https://www.github.com/googleapis/python-datacatalog/commit/7a890c2f87ff37f610c7246bcbf369314d87b93d))

## [0.7.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.6.0...v0.7.0) (2020-04-09)


### Features

* add v1 ([#13](https://www.github.com/googleapis/python-datacatalog/issues/13)) ([21629fe](https://www.github.com/googleapis/python-datacatalog/commit/21629fed1f86bb1a2800b5213f59acc5d862e2f5))

## [0.6.0](https://www.github.com/googleapis/python-datacatalog/compare/v0.5.0...v0.6.0) (2020-02-24)


### Features

* **datacatalog:** add sample for create a fileset entry quickstart ([#9977](https://www.github.com/googleapis/python-datacatalog/issues/9977)) ([16eaf4b](https://www.github.com/googleapis/python-datacatalog/commit/16eaf4b16cdc0ce7361afb1d8dac666cea2a9db0))
* **datacatalog:** undeprecate resource name helper methods, bump copyright year to 2020, tweak docstring formatting (via synth) ([#10228](https://www.github.com/googleapis/python-datacatalog/issues/10228)) ([84e5e7c](https://www.github.com/googleapis/python-datacatalog/commit/84e5e7c340fa189ce4cffca4fdee82cc7ded9f70))
* add `list_entry_groups`, `list_entries`, `update_entry_group` methods to v1beta1 (via synth) ([#6](https://www.github.com/googleapis/python-datacatalog/issues/6)) ([b51902e](https://www.github.com/googleapis/python-datacatalog/commit/b51902e26d590f52c9412756a178265850b7d516))


### Bug Fixes

* **datacatalog:** deprecate resource name helper methods (via synth) ([#9831](https://www.github.com/googleapis/python-datacatalog/issues/9831)) ([22db3f0](https://www.github.com/googleapis/python-datacatalog/commit/22db3f0683b8aca544cd96c0063dcc8157ad7335))

## 0.5.0

11-14-2019 12:54 PST

### New Features

- add policy tag manager clients ([#9804](https://github.com/googleapis/google-cloud-python/pull/9804))

### Documentation

- add python 2 sunset banner to documentation ([#9036](https://github.com/googleapis/google-cloud-python/pull/9036))
- add sample to create a fileset entry ([#9590](https://github.com/googleapis/google-cloud-python/pull/9590))
- add sample to create an entry group ([#9584](https://github.com/googleapis/google-cloud-python/pull/9584))

### Internal / Testing Changes

- change spacing in docs templates (via synth) ([#9743](https://github.com/googleapis/google-cloud-python/pull/9743))

## 0.4.0

10-23-2019 08:54 PDT

### Implementation Changes

- remove send/recv msg size limit (via synth) ([#8949](https://github.com/googleapis/google-cloud-python/pull/8949))

### New Features

- add entry group operations ([#9520](https://github.com/googleapis/google-cloud-python/pull/9520))

### Documentation

- fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- remove unused import from samples (via synth). ([#9110](https://github.com/googleapis/google-cloud-python/pull/9110))
- remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- add 'search' sample (via synth). ([#8793](https://github.com/googleapis/google-cloud-python/pull/8793))

## 0.3.0

07-24-2019 15:58 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8425](https://github.com/googleapis/google-cloud-python/pull/8425))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8654](https://github.com/googleapis/google-cloud-python/pull/8654))
- Add 'client_options' support, update list method docstrings (via synth). ([#8503](https://github.com/googleapis/google-cloud-python/pull/8503))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Add get_entry sample (via synth). ([#8725](https://github.com/googleapis/google-cloud-python/pull/8725))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add generated samples (via synth). ([#8710](https://github.com/googleapis/google-cloud-python/pull/8710))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Update docstrings (via synth). ([#8299](https://github.com/googleapis/google-cloud-python/pull/8299))

### Internal / Testing Changes
- Enable Sample Generator Tool for Data Catalog ([#8708](https://github.com/googleapis/google-cloud-python/pull/8708))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.2.0

06-12-2019 12:46 PDT

### New Features

- Add search capability, tags that match a query, and IAM policies ([#8266](https://github.com/googleapis/google-cloud-python/pull/8266))
- Add protos as an artifact to library (via synth). ([#8018](https://github.com/googleapis/google-cloud-python/pull/8018))

### Documentation

- Add nox session `docs`, reorder methods (via synth). ([#7766](https://github.com/googleapis/google-cloud-python/pull/7766))
- Fix broken link to client library docs in README ([#7713](https://github.com/googleapis/google-cloud-python/pull/7713))

### Internal / Testing Changes

- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8235](https://github.com/googleapis/google-cloud-python/pull/8235))
- Fix coverage in 'types.py' (via synth). ([#8150](https://github.com/googleapis/google-cloud-python/pull/8150))
- Blacken noxfile.py, setup.py (via synth). ([#8117](https://github.com/googleapis/google-cloud-python/pull/8117))
- Add empty lines (via synth). ([#8052](https://github.com/googleapis/google-cloud-python/pull/8052))

## 0.1.0

04-15-2019 15:46 PDT

### New Features

- Initial release of Cloud Data Catalog client. ([#7708](https://github.com/googleapis/google-cloud-python/pull/7708))
