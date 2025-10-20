# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-apps-card/#history

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.2.0...google-apps-card-v0.3.0) (2025-10-20)


### Documentation

* change `Workspace Add-ons` to `Workspace add-ons`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* improve comments  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))


### Features

* Add `NestedWidget`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add `Validation` and the field `TextInput.validation`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add the field `TextParagraph.TextSyntax`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add `ChipList`,`Chip` and field `Widgets.chip_list`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add `Button.Type` and field `Button.type`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add `Carousel` widget  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add the field `TextParagraph.max_lines`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add the field `DecoratedText.start_icon_vertical_alignment`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Add `OverflowMenu` widget  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))


### Bug Fixes

* An existing field `start_icon_uri` is moved in to oneof in message `.google.apps.card.v1.SelectionInput`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))
* Changed proto3 optional flag of an existing field `multi_select_max_selected_items` in message `.google.apps.card.v1.SelectionInput`  ([84be9032eb7ba04bb305870160699d2bc12e0dac](https://github.com/googleapis/google-cloud-python/commit/84be9032eb7ba04bb305870160699d2bc12e0dac))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.8...google-apps-card-v0.2.0) (2025-10-16)


### Features

* Add support for Python 3.14  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))


### Bug Fixes

* Deprecate credentials_file argument  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.7...google-apps-card-v0.1.8) (2025-06-11)


### Documentation

* Update import statement example in README ([1562bb7](https://github.com/googleapis/google-cloud-python/commit/1562bb740c7cd56179e52185dde3c32af861de5e))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.6...google-apps-card-v0.1.7) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([a1b9294](https://github.com/googleapis/google-cloud-python/commit/a1b9294d0bf6e27c2a951d6df7faf7807dc5420b))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.5...google-apps-card-v0.1.6) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))
* Add support for reading selective GAPIC generation methods from service YAML ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.4...google-apps-card-v0.1.5) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.3...google-apps-card-v0.1.4) (2024-07-30)


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.2...google-apps-card-v0.1.3) (2024-07-08)


### Bug Fixes

* Allow protobuf 5.x ([04ec204](https://github.com/googleapis/google-cloud-python/commit/04ec2046ed11c690273912e1bb6220823c7dd7c0))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.1...google-apps-card-v0.1.2) (2024-04-16)


### Features

* material icon in card ([fef36ac](https://github.com/googleapis/google-cloud-python/commit/fef36ac0532b145665c4e53c18d04058c4295d74))


### Documentation

* card proto update ([fef36ac](https://github.com/googleapis/google-cloud-python/commit/fef36ac0532b145665c4e53c18d04058c4295d74))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-apps-card-v0.1.0...google-apps-card-v0.1.1) (2024-03-05)


### Bug Fixes

* **deps:** Exclude google-auth 2.24.0 and 2.25.0 ([#12381](https://github.com/googleapis/google-cloud-python/issues/12381)) ([48ae8ab](https://github.com/googleapis/google-cloud-python/commit/48ae8aba7ec71a382e001b3a659022f942c3b436))

## 0.1.0 (2024-03-04)


### Features

* add initial files for google.apps.card.v1 ([#12370](https://github.com/googleapis/google-cloud-python/issues/12370)) ([394a05f](https://github.com/googleapis/google-cloud-python/commit/394a05fe2b3d2582c4f161efc574fe8e1625c913))

## Changelog
