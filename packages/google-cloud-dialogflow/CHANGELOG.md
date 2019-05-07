# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/dialogflow/#history

## 0.6.0

05-06-2019 1:34 PST

### Implementation Changes

- Add routing header to method metadata.([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Warn when deprecated client_config argument is used. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add https://www.googleapis.com/auth/dialogflow OAuth scope. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add channel to gRPC transport classes. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

### Features

- Add argument output_audio_config to detect_intent. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add update_knowledge_base method. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Add update_document and reload_document methods. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

### Documentation:
- Change copyright year to 2019. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

### Internal / Testing Changes
- Use mock to patch create_channel in unit tests. ([#123](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))

## 0.5.2

12-18-2018 10:50 PST

### Documentation
- Add notice of Python 2.7 deprecation ([#112](https://github.com/googleapis/dialogflow-python-client-v2/pull/112))
- Fix typo in samples ([#52](https://github.com/googleapis/dialogflow-python-client-v2/pull/52))
- Update README.rst ([#27](https://github.com/googleapis/dialogflow-python-client-v2/pull/27))
- Updating README per ask from Product ([#81](https://github.com/googleapis/dialogflow-python-client-v2/pull/81))
- Add v2beta1 samples for dialogflow and update v2 sample formatting. ([#72](https://github.com/googleapis/dialogflow-python-client-v2/pull/72))

### Internal / Testing Changes
- Update github issue templates ([#103](https://github.com/googleapis/dialogflow-python-client-v2/pull/103))
- Strip dynamic badges from README ([#99](https://github.com/googleapis/dialogflow-python-client-v2/pull/99))
- Correct the repository name in samples README. ([#83](https://github.com/googleapis/dialogflow-python-client-v2/pull/83))
- Fix [#76](https://github.com/googleapis/dialogflow-python-client-v2/pull/76) by adding replacement patterns to dialogflow ([#79](https://github.com/googleapis/dialogflow-python-client-v2/pull/79))

## 0.4.0
- Regenerate v2beta1 endpoint

## 0.3.0
- Regenerate v2 endpoint
- Update documentation comments

## 0.2.0

### New Features
- Add v2 Endpoint (#38)

### Documentation
- Add sample readme, and sample agent (#15)

### Internal / Testing Changes
- Fix typo (#16)

