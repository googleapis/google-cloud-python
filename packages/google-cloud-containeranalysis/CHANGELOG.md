# Changelog

## [1.0.0](https://www.github.com/googleapis/python-containeranalysis/compare/v0.3.1...v1.0.0) (2020-06-16)


### Features

* release as production/stable ([#15](https://www.github.com/googleapis/python-containeranalysis/issues/15)) ([b81e207](https://www.github.com/googleapis/python-containeranalysis/commit/b81e2074eb86c015c781b79a68839cbaeb40e5b2))
* remove `note_path` and `occurence_path` (via synth) ([#7](https://www.github.com/googleapis/python-containeranalysis/issues/7)) ([656b11e](https://www.github.com/googleapis/python-containeranalysis/commit/656b11eee22f11d1109e288190fc63b6c8ff20b7))

## 0.3.1

11-07-2019 11:08 PST

**NOTE**: Please upgrade to this version if you will also be using `google-cloud-build`. 

### Implementation Changes
- Make google.cloud.devtools a namespace ([#9606](https://github.com/googleapis/google-cloud-python/pull/9606))

### Documentation
- Change requests intersphinx ref (via synth)
- Fix intersphinx reference to requests ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))

## 0.3.0

08-12-2019 13:53 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8948](https://github.com/googleapis/google-cloud-python/pull/8948))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Normalize docs. ([#8994](https://github.com/googleapis/google-cloud-python/pull/8994))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.2.0

07-12-2019 16:56 PDT

### New Features
- Add 'client_options' support (via synth). ([#8502](https://github.com/googleapis/google-cloud-python/pull/8502))
- Add 'options_' argument to clients' 'get_iam_policy'; pin black version (via synth). ([#8653](https://github.com/googleapis/google-cloud-python/pull/8653))

### Dependencies
- Update pin for 'grpc-google-iam-v1' to 0.12.3+. ([#8647](https://github.com/googleapis/google-cloud-python/pull/8647))

### Documentation
- Update READMEs. ([#8456](https://github.com/googleapis/google-cloud-python/pull/8456))

### Internal / Testing Changes
- Fix language in repo metadata. ([#8537](https://github.com/googleapis/google-cloud-python/pull/8537))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.1.0

06-19-2019 11:02 PDT

### New Features
- Initial release of Container Analysis client library. ([#8381](https://github.com/googleapis/google-cloud-python/pull/8381))
