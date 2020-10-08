# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-securitycenter/#history

## [1.0.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.7.1...v1.0.0) (2020-10-08)


### ⚠ BREAKING CHANGES

* generate with microgenerator. See [Migration Guide](https://github.com/googleapis/python-securitycenter/blob/master/UPGRADING.md)(#49)

### Features

* generate with microgenerator ([#49](https://www.github.com/googleapis/python-securitycenter/issues/49)) ([838dbc8](https://www.github.com/googleapis/python-securitycenter/commit/838dbc8445046b755b775f96f654944ecb707e35))

### [0.7.1](https://www.github.com/googleapis/python-securitycenter/compare/v0.7.0...v0.7.1) (2020-09-18)


### Bug Fixes

* **sample:** fix a broken test ([#63](https://www.github.com/googleapis/python-securitycenter/issues/63)) ([7062b1c](https://www.github.com/googleapis/python-securitycenter/commit/7062b1c18a6f787275b325d2a7713cf0b2627094)), closes [#59](https://www.github.com/googleapis/python-securitycenter/issues/59)

## [0.7.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.6.0...v0.7.0) (2020-09-10)


### Features

* add field severity to findings; update retry configs ([#53](https://www.github.com/googleapis/python-securitycenter/issues/53)) ([80494a9](https://www.github.com/googleapis/python-securitycenter/commit/80494a915ca33d260862694be889b817869ff01a))


### Documentation

* Update Security Command Center UpdateNotificationConfig sample, adding filter to mutable field ([#39](https://www.github.com/googleapis/python-securitycenter/issues/39)) ([c70d790](https://www.github.com/googleapis/python-securitycenter/commit/c70d7904425ae5ac252ffa7317ec6d08234a6c27))

## [0.6.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.5.0...v0.6.0) (2020-07-01)


### Features

* add `security_marks_path` method; fix docstring links (via synth) ([#24](https://www.github.com/googleapis/python-securitycenter/issues/24)) ([80ce6e6](https://www.github.com/googleapis/python-securitycenter/commit/80ce6e6128abf106ef7c3631a426f99440a406d9))
* add Resource to the v1 NotificationMessage ([#33](https://www.github.com/googleapis/python-securitycenter/issues/33)) ([c930e6a](https://www.github.com/googleapis/python-securitycenter/commit/c930e6afc6aa701761f9966e1391ca2d3ebb30f4))


### Documentation

* Update notification samples to v1 ([#19](https://www.github.com/googleapis/python-securitycenter/issues/19)) ([5eba984](https://www.github.com/googleapis/python-securitycenter/commit/5eba984eefefd3d689d84d14a8078c28914307c8))

## [0.5.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.4.0...v0.5.0) (2020-03-10)


### Features

* add support for notification configs to v1 ([#15](https://www.github.com/googleapis/python-securitycenter/issues/15)) ([9720fa4](https://www.github.com/googleapis/python-securitycenter/commit/9720fa44dc6e785c60ee9af555b5fea0564f34e0))

## [0.4.0](https://www.github.com/googleapis/python-securitycenter/compare/v0.3.0...v0.4.0) (2020-02-13)


### Features

* add v1p1beta1; add `resource_display_name, `resource_parent_display_name`, `resource_project_display_name` to `v1.Asset.SecurityCenterProperties`; add output only field `resource` to `v1.ListFindingsResponse.ListFindingsResult`; increase `initial_rpc_timeout_millis` in default config for v1; standardize use of 'required' and 'optional' in docstrings; add 2.7 deprecation warning; bump copyright year to 2020 ([#7](https://www.github.com/googleapis/python-securitycenter/issues/7)) ([03e172b](https://www.github.com/googleapis/python-securitycenter/commit/03e172b34c7cf9a92de10085f4f040cd0e5e85eb))

## 0.3.0

07-24-2019 17:29 PDT

### Implementation Changes
- Allow kwargs to be passed to create_channel, update templates (via synth). ([#8402](https://github.com/googleapis/google-cloud-python/pull/8402))
- Update return type of run_asset_discovery (via synth). ([#8032](https://github.com/googleapis/google-cloud-python/pull/8032))
- Security Center: Add routing header to method metadata (via synth). ([#7589](https://github.com/googleapis/google-cloud-python/pull/7589))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8658](https://github.com/googleapis/google-cloud-python/pull/8658))
- Add 'client_options' support, update list method docstrings (via synth). ([#8521](https://github.com/googleapis/google-cloud-python/pull/8521))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Update docstrings (via synth). ([#8711](https://github.com/googleapis/google-cloud-python/pull/8711))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Docstring changes (via synth). ([#7704](https://github.com/googleapis/google-cloud-python/pull/7704))
- Add Snippets for security center list_assets call ([#7538](https://github.com/googleapis/google-cloud-python/pull/7538))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8362](https://github.com/googleapis/google-cloud-python/pull/8362))
- Add disclaimer to auto-generated template files (via synth).([#8326](https://github.com/googleapis/google-cloud-python/pull/8326))
- Fix coverage in 'types.py' (via synth). ([#8163](https://github.com/googleapis/google-cloud-python/pull/8163))
- Add empty lines (via synth). ([#8070](https://github.com/googleapis/google-cloud-python/pull/8070))
- Add nox session `docs`, reorder methods (via synth). ([#7780](https://github.com/googleapis/google-cloud-python/pull/7780))
- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))
- Add Ruby package configuration in protos (via synth). ([#7741](https://github.com/googleapis/google-cloud-python/pull/7741))
- proto file housekeeping FBO PHP (via synth).

## 0.2.0

03-12-2019 17:09 PDT


### Implementation Changes
- Remove 'having' filter arguments from query methods (via synth). [#7511](https://github.com/googleapis/google-cloud-python/pull/7511))
- Remove unused message exports. ([#7274](https://github.com/googleapis/google-cloud-python/pull/7274))
- Trivial gapic-generator change. ([#7233](https://github.com/googleapis/google-cloud-python/pull/7233))
- Protoc-generated serialization update, docstring tweak. ([#7094](https://github.com/googleapis/google-cloud-python/pull/7094))

### New Features
- Add support for `v1` API. ([#7495](https://github.com/googleapis/google-cloud-python/pull/7495))

### Documentation
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Docstring update from .proto file. ([#7056](https://github.com/googleapis/google-cloud-python/pull/7056))
- Fix 404 for 'Client Library Documentation' link. ([#7041](https://github.com/googleapis/google-cloud-python/pull/7041))
- Pick up stub docstring fix in GAPIC generator. ([#6981](https://github.com/googleapis/google-cloud-python/pull/6981))

### Internal / Testing Changes
- Proto file housekeeping FBO C# (via synth). ([#7502](https://github.com/googleapis/google-cloud-python/pull/7502))
- Copy lintified proto files (via synth). ([#7470](https://github.com/googleapis/google-cloud-python/pull/7470))
- Add clarifying comment to blacken nox target. ([#7402](https://github.com/googleapis/google-cloud-python/pull/7402))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.1.1

12-18-2018 09:45 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up changes to GAPIC generator. ([#6506](https://github.com/googleapis/google-cloud-python/pull/6506))
- Assorted synth fixups / cleanups ([#6400](https://github.com/googleapis/google-cloud-python/pull/6400))
- Fix `client_info` bug, update docstrings via synth. ([#6438](https://github.com/googleapis/google-cloud-python/pull/6438))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Docstring changes via synth. ([#6473](https://github.com/googleapis/google-cloud-python/pull/6473))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Overlooked synth changes. ([#6439](https://github.com/googleapis/google-cloud-python/pull/6439))

## 0.1.0

11-01-2018 15:12 PDT

### New Features
- Generate Security Center Client Library ([#6356](https://github.com/googleapis/google-cloud-python/pull/6356))
