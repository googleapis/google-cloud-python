# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/grafeas/#history

### [0.4.1](https://www.github.com/googleapis/python-grafeas/compare/v0.4.0...v0.4.1) (2020-06-25)


### Bug Fixes

* update retry config ([#24](https://www.github.com/googleapis/python-grafeas/issues/24)) ([122ec6a](https://www.github.com/googleapis/python-grafeas/commit/122ec6a2fdf93ad745b6c275defa0bb809f1d005))

## [0.4.0](https://www.github.com/googleapis/python-grafeas/compare/v0.3.0...v0.4.0) (2020-02-07)


### Features

* **grafeas:** add support for upgrade notes; add `cpe` and `last_scan_time` to `DiscoveryOccurrence`; add `source_update_time` to `VulnerabilityNote` (via synth) ([#10084](https://www.github.com/googleapis/python-grafeas/issues/10084)) ([2ee967b](https://www.github.com/googleapis/python-grafeas/commit/2ee967b916e663bacbda8c391528cdca3a1117fd))


### Bug Fixes

* **grafeas:** deprecate resource name helper methods (via synth) ([#9835](https://www.github.com/googleapis/python-grafeas/issues/9835)) ([a2c26d9](https://www.github.com/googleapis/python-grafeas/commit/a2c26d9b60194d305f8cb2b8ec4a4a33d7bf3686))

## 0.3.0

10-10-2019 11:28 PDT


### Implementation Changes
- Remove send / receive message size limit (via synth). ([#8981](https://github.com/googleapis/google-cloud-python/pull/8981))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))

## 0.2.0

07-12-2019 17:04 PDT


### Implementation Changes
- replace `min_affected_version` w/ `affected_version_{start,end}` (via synth).  ([#8465](https://github.com/googleapis/google-cloud-python/pull/8465))
- Allow kwargs to be passed to create_channel, update templates (via synth). ([#8391](https://github.com/googleapis/google-cloud-python/pull/8391))

### New Features
- Update list method docstrings (via synth). ([#8510](https://github.com/googleapis/google-cloud-python/pull/8510))

### Documentation
- Update READMEs. ([#8456](https://github.com/googleapis/google-cloud-python/pull/8456))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.1.0

06-17-2019 10:44 PDT

### New Features
- Initial release of the Grafeas client library. ([#8186](https://github.com/googleapis/google-cloud-python/pull/8186))
