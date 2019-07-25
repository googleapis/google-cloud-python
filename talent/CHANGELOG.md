# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-talent/#history

## 0.3.0

07-24-2019 17:36 PDT


### Implementation Changes
- search_profiles returns iterable of SummarizedProfile instead of HistogramQueryResult (via synth). ([#7962](https://github.com/googleapis/google-cloud-python/pull/7962))

### New Features
- Add strict keywords search, increase timeout (via synth). ([#8712](https://github.com/googleapis/google-cloud-python/pull/8712))
- Add path-construction helpers to GAPIC clients (via synth). ([#8632](https://github.com/googleapis/google-cloud-python/pull/8632))
- Add 'result_set_id' param to 'ProfileSearchClient.search_profiles'; add 'ProfileQuery.candidate_availability_filter'; pin 'black' version; dostring tweaks (via synth). ([#8597](https://github.com/googleapis/google-cloud-python/pull/8597))
- Add 'client_options' support, update list method docstrings (via synth). ([#8523](https://github.com/googleapis/google-cloud-python/pull/8523))
- Add 'batch_create_jobs' and 'batch_update_jobs' (via synth). ([#8189](https://github.com/googleapis/google-cloud-python/pull/8189))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Allow kwargs to be passed to create_channel (via synth). ([#8405](https://github.com/googleapis/google-cloud-python/pull/8405))
- Declare encoding as utf-8 in pb2 files (via synth).([#8365](https://github.com/googleapis/google-cloud-python/pull/8365))
- Add disclaimer to auto-generated template files (via synth). ([#8329](https://github.com/googleapis/google-cloud-python/pull/8329))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8253](https://github.com/googleapis/google-cloud-python/pull/8253))
- Fix coverage in 'types.py' (via synth). ([#8165](https://github.com/googleapis/google-cloud-python/pull/8165))
- Blacken noxfile.py, setup.py (via synth).([#8133](https://github.com/googleapis/google-cloud-python/pull/8133))
- Add empty lines (via synth). ([#8073](https://github.com/googleapis/google-cloud-python/pull/8073))

## 0.2.0

05-09-2019 12:25 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Regenerate talent (via synth). ([#7861](https://github.com/googleapis/google-cloud-python/pull/7861))

### Documentation
- Fixed broken talent client library documentation link ([#7546](https://github.com/googleapis/google-cloud-python/pull/7546))
- Fix link in docstring.([#7508](https://github.com/googleapis/google-cloud-python/pull/7508))
- Documentation and formatting changes. ([#7489](https://github.com/googleapis/google-cloud-python/pull/7489))

## 0.1.0

03-05-2019 12:50 PST

- Initial release of google-cloud-talent

