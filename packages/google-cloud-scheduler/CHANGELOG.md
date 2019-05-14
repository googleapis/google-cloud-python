# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-scheduler/#history

## 1.1.0

05-13-2019 13:15 PDT

### New Features
- Add authorization headers and deadline for job attempts (via synth). ([#7938](https://github.com/googleapis/google-cloud-python/pull/7938))

### Internal / Testing Changes
- Add nox session `docs`, reorder methods (via synth). ([#7779](https://github.com/googleapis/google-cloud-python/pull/7779))

## 1.0.0

05-03-2019 10:04 PDT

### Internal / Testing Changes
- Add smoke test for scheduler. ([#7854](https://github.com/googleapis/google-cloud-python/pull/7854))

## 0.3.0

04-15-2019 10:32 PDT


### New Features
- add auth and configurable timeouts to v1beta1 (via synth). ([#7665](https://github.com/googleapis/google-cloud-python/pull/7665))

## 0.2.0

04-01-2019 15:39 PDT


### Implementation Changes
- Add routing header to method metadata (via synth). ([#7599](https://github.com/googleapis/google-cloud-python/pull/7599))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Remove unused message exports. ([#7273](https://github.com/googleapis/google-cloud-python/pull/7273))
- Protoc-generated serialization update. ([#7093](https://github.com/googleapis/google-cloud-python/pull/7093))
- Protoc-generated serialization update. ([#7055](https://github.com/googleapis/google-cloud-python/pull/7055))
- Use moved iam.policy now at google.api_core.iam.policy. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))

### New Features
- Add v1. ([#7608](https://github.com/googleapis/google-cloud-python/pull/7608))
- Pick up fixes to GAPIC generator. ([#6505](https://github.com/googleapis/google-cloud-python/pull/6505))

### Documentation
- googlecloudplatform --> googleapis in READMEs. ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright year. ([#7155](https://github.com/googleapis/google-cloud-python/pull/7155))
- Correct a link in a documentation string. ([#7119](https://github.com/googleapis/google-cloud-python/pull/7119))
- Pick up stub docstring fix in GAPIC generator. ([#6980](https://github.com/googleapis/google-cloud-python/pull/6980))
- Document Python 2 deprecation. ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Update link for Scheduler Docs. ([#6925](https://github.com/googleapis/google-cloud-python/pull/6925))

### Internal / Testing Changes
- Copy lintified proto files (via synth). ([#7469](https://github.com/googleapis/google-cloud-python/pull/7469))
- Add clarifying comment to blacken nox target. ([#7401](https://github.com/googleapis/google-cloud-python/pull/7401))
- Add protos as an artifact to library. ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Add baseline for synth.metadata. ([#6792](https://github.com/googleapis/google-cloud-python/pull/6865))
- Update noxfile. ([#6814](https://github.com/googleapis/google-cloud-python/pull/6814))
- Blacken all gen'd libs. ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps. ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py. ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries. ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))

## 0.1.0

11-13-2018 11:03 PST


### New Features
- Initial release of Cloud Scheduler library. ([#6482](https://github.com/googleapis/google-cloud-python/pull/6482))

