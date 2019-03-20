# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-asset/#history

## 0.2.0

03-19-2019 12:17 PDT


### Implementation Changes
- Rename 'GcsDestination.uri' -> 'object_uri', docstring changes . ([#7202](https://github.com/googleapis/google-cloud-python/pull/7202))
- Protoc-generated serialization update.. ([#7073](https://github.com/googleapis/google-cloud-python/pull/7073))

### New Features
- Generate v1. ([#7513](https://github.com/googleapis/google-cloud-python/pull/7513))

### Documentation
- Fix broken links to Cloud Asset API ([#7524](https://github.com/googleapis/google-cloud-python/pull/7524))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers
- Pick up stub docstring fix in GAPIC generator.[#6963](https://github.com/googleapis/google-cloud-python/pull/6963))

### Internal / Testing Changes
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Add support for including protos in synth ([#7114](https://github.com/googleapis/google-cloud-python/pull/7114))

## 0.1.2

12-17-2018 16:15 PST


### Implementation Changes
- Use moved iam.policy now at google.api_core.iam.policy ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6607](https://github.com/googleapis/google-cloud-python/pull/6607))
- Pick up fixes in GAPIC generator. ([#6489](https://github.com/googleapis/google-cloud-python/pull/6489))
- Fix client_info bug, update docstrings. ([#6403](https://github.com/googleapis/google-cloud-python/pull/6403))
- Synth docstring changes generated from updated protos ([#6349](https://github.com/googleapis/google-cloud-python/pull/6349))
- Generated cloud asset client files are under asset-[version] ([#6341](https://github.com/googleapis/google-cloud-python/pull/6341))

### New Features

### Dependencies
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Fix docs build. ([#6351](https://github.com/googleapis/google-cloud-python/pull/6351))
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Add templating to asset synth.py ([#6606](https://github.com/googleapis/google-cloud-python/pull/6606))
- Add synth metadata. ([#6560](https://github.com/googleapis/google-cloud-python/pull/6560))
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Unblack gapic and protos.
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Add / fix badges for PyPI / versions. ([#6158](https://github.com/googleapis/google-cloud-python/pull/6158))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.1.1

### Packaging
- Release as `google-cloud-asset`, rather than `google-cloud-cloudasset`.
  (#5998)

## 0.1.0

Initial release.

