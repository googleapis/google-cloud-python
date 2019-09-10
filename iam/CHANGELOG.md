# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-iam/#history

## 0.2.1

08-23-2019 10:10 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8936](https://github.com/googleapis/google-cloud-python/pull/8936))

### Documentation
- Fix documentation links for iam and error-reporting. ([#9073](https://github.com/googleapis/google-cloud-python/pull/9073))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.2.0

07-24-2019 16:22 PDT


### Implementation Changes
- Remove generate_identity_binding_access_token (via synth). ([#8486](https://github.com/googleapis/google-cloud-python/pull/8486))
- Allow kwargs to be passed to create_channel (via synth). ([#8392](https://github.com/googleapis/google-cloud-python/pull/8392))
- Add routing header to method metadata, format docstrings, update docs configuration (via synth). ([#7595](https://github.com/googleapis/google-cloud-python/pull/7595))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7268](https://github.com/googleapis/google-cloud-python/pull/7268))
- Protoc-generated serialization update. ([#7084](https://github.com/googleapis/google-cloud-python/pull/7084))
- Protoc-generated serialization update. ([#7052](https://github.com/googleapis/google-cloud-python/pull/7052))
- Pick up stub docstring fix in GAPIC generator. ([#6972](https://github.com/googleapis/google-cloud-python/pull/6972))

### New Features
- Add 'client_options' support (via synth).  ([#8511](https://github.com/googleapis/google-cloud-python/pull/8511))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix client lib docs link in README. ([#7813](https://github.com/googleapis/google-cloud-python/pull/7813))
- Update copyright: 2018 -> 2019. ([#7146](https://github.com/googleapis/google-cloud-python/pull/7146))

### Internal / Testing Changes
- Pin black version (via synth). ([#8584](https://github.com/googleapis/google-cloud-python/pull/8584))
- Add nox session 'docs' to remaining manual clients. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). [#8353](https://github.com/googleapis/google-cloud-python/pull/8353))
- Add disclaimer to auto-generated template files (via synth). ([#8315](https://github.com/googleapis/google-cloud-python/pull/8315))
- Suppress checking 'cov-fail-under' in nox default session (via synth).  ([#8242](https://github.com/googleapis/google-cloud-python/pull/8242))
- Fix coverage in 'types.py' (via synth). ([#8154](https://github.com/googleapis/google-cloud-python/pull/8154))
- Blacken noxfile.py, setup.py (via synth). ([#8124](https://github.com/googleapis/google-cloud-python/pull/8124))
- Add empty lines (via synth). ([#8059](https://github.com/googleapis/google-cloud-python/pull/8059))
- Add nox session `docs` (via synth). ([#7772](https://github.com/googleapis/google-cloud-python/pull/7772))
- Copy lintified proto files (via synth). ([#7467](https://github.com/googleapis/google-cloud-python/pull/7467))
- Add clarifying comment to blacken nox target. ([#7393](https://github.com/googleapis/google-cloud-python/pull/7393))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.1.0

12-13-2018 10:55 PST


### New Features
- Add Client Library for IAM ([#6905](https://github.com/googleapis/google-cloud-python/pull/6905))

### Documentation
- Fix docs build ([#6913](https://github.com/googleapis/google-cloud-python/pull/6913))

### Internal / Testing Changes
- trove classifier fix ([#6922](https://github.com/googleapis/google-cloud-python/pull/6922))
