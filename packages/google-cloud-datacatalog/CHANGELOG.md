# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-datacatalog/#history

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

