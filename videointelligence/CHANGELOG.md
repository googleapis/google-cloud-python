# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-videointelligence/#history

## 1.11.0

08-12-2019 14:00 PDT

### New Features
- Add segment / shot presence label annotations fields (via synth). ([#8987](https://github.com/googleapis/google-cloud-python/pull/8987))
- Add V1 video segment / feature fields; remove send/recv msg size limit (via synth). ([#8975](https://github.com/googleapis/google-cloud-python/pull/8975))

### Documentation
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.10.0

07-24-2019 17:52 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8410](https://github.com/googleapis/google-cloud-python/pull/8410))

### New Features
- Add 'client_options' support (via synth). ([#8528](https://github.com/googleapis/google-cloud-python/pull/8528))
- Add support for streaming classification / object tracking (via synth). ([#8427](https://github.com/googleapis/google-cloud-python/pull/8427))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Add VPC SC integration tests. ([#8607](https://github.com/googleapis/google-cloud-python/pull/8607))
- Pin black version (via synth). ([#8601](https://github.com/googleapis/google-cloud-python/pull/8601))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Change test video URI, add disclaimer to auto-generated template files (via synth). ([#8334](https://github.com/googleapis/google-cloud-python/pull/8334))
- Declare encoding as utf-8 in pb2 files (via synth).  ([#8370](https://github.com/googleapis/google-cloud-python/pull/8370))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8256](https://github.com/googleapis/google-cloud-python/pull/8256))

## 1.9.0

06-05-2019 10:42 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add v1 object tracking support, v1p3b1 speech transcription / logo recognition support (via synth). ([#8221](https://github.com/googleapis/google-cloud-python/pull/8221))

### Documentation
- Change input_uri for sample video (via synth). ([#7944](https://github.com/googleapis/google-cloud-python/pull/7944))
- Fix uri to video (via synth).  ([#7862](https://github.com/googleapis/google-cloud-python/pull/7862))

### Internal / Testing Changes
- Fix coverage in 'types.py' (via synth). ([#8169](https://github.com/googleapis/google-cloud-python/pull/8169))
- Blacken noxfile.py, setup.py (via synth). ([#8136](https://github.com/googleapis/google-cloud-python/pull/8136))
- Harden synth replacement against template changes. ([#8104](https://github.com/googleapis/google-cloud-python/pull/8104))
- Update noxfile (via synth). ([#7838](https://github.com/googleapis/google-cloud-python/pull/7838))
- Add nox session `docs` (via synth). ([#7786](https://github.com/googleapis/google-cloud-python/pull/7786))
- Update docs build configuration.  ([#7603](https://github.com/googleapis/google-cloud-python/pull/7603))

## 1.8.0

03-06-2019 12:20 PST

### New Features
- Add videointelligence v1p3beta1 (Streaming API Support). ([#7490](https://github.com/googleapis/google-cloud-python/pull/7490))

### Internal / Testing Changes
- Copy lintified proto files (via synth). ([#7472](https://github.com/googleapis/google-cloud-python/pull/7472))

## 1.7.0

02-25-2019 12:25 PST


### Implementation Changes
- Remove unused message exports. ([#7279](https://github.com/googleapis/google-cloud-python/pull/7279))
- Protoc-generated serialization update. ([#7099](https://github.com/googleapis/google-cloud-python/pull/7099))

### New Features
- Add text detection / object tracking feature support (via sync). ([#7415](https://github.com/googleapis/google-cloud-python/pull/7415))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers.
- Pick up stub docstring fix in GAPIC generator. ([#6986](https://github.com/googleapis/google-cloud-python/pull/6986))

### Internal / Testing Changes
- Add clarifying comment to blacken nox target. ([#7407](https://github.com/googleapis/google-cloud-python/pull/7407))
- Copy proto files alongside protoc versions.
- Add protos as an artifact to library. ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 1.6.1

12-17-2018 17:09 PST

### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Fixes to GAPIC generator. ([#6578](https://github.com/googleapis/google-cloud-python/pull/6578))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

### Internal / Testing Changes
- Add baseline for synth.metadata
- Update noxfile.
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))

## 1.6.0

11-09-2018 13:36 PST


### Implementation Changes
- Add support for speech transcription. ([#6313](https://github.com/googleapis/google-cloud-python/pull/6313))
- Fix client_info bug, update docstrings and timeouts. ([#6425](https://github.com/googleapis/google-cloud-python/pull/6425))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Avoid broken 'google-common-apis 1.5.4' release. ([#6355](https://github.com/googleapis/google-cloud-python/pull/6355))

### Documentation
- normalize use of support level badges.([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Add 'mock' to unit test dependencies for autogen libs. ([#6402](https://github.com/googleapis/google-cloud-python/pull/6402))

## 1.5.0

### New Features
- Regenerate v2p2beta1 to add Object Tracking and Text Detection Beta ([#6225](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6225))

### Documentation
- Harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6002](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6002))
- Correct text for the pip install command ([#6198](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6198))

### Internal / Testing Changes
- Use new Nox ([#6175](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6175))

## 1.4.0

### New Features
- Add support for 'v1p2beta1' API version ([#6004](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/6004))

### Implementation Changes
- Re-generate library using videointelligence/synth.py ([#5982](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5982))
- Re-generate library using videointelligence/synth.py ([#5954](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5954))

## 1.3.0

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### New Features
- Regenerate Video Intelligence v1p1beta1 endpoint to add new features (#5617)

### Internal / Testing Changes
- Add Test runs for Python 3.7 and remove 3.4 (#5295)

## 1.2.0

### New Features

- Add v1p1beta1 version of videointelligence (#5165)

### Internal / Testing Changes

- Fix v1p1beta1 unit tests (#5064)

## 1.1.0

### Interface additions

- Added video v1p1beta1 (#5048)

## 1.0.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Normalize all setup.py files (#4909)

## 1.0.0

[![release level](https://img.shields.io/badge/release%20level-general%20availability%20%28GA%29-brightgreen.svg?style&#x3D;flat)](https://cloud.google.com/terms/launch-stages)

### Features

#### General Availability

The `google-cloud-videointelligence` package is now supported at the
**general availability** quality level. This means it is stable; the code
and API surface will not change in backwards-incompatible ways unless
absolutely necessary (e.g. because of critical security issues) or with an
extensive deprecation period.

One exception to this: We will remove beta endpoints (as a semver-minor update)
at whatever point the underlying endpoints go away.

#### v1 endpoint

The underlying video intelligence API has also gone general availability, and
this library by default now uses the `v1` endpoint (rather than `v1beta2`)
unless you explicitly used something else. This is a backwards compatible
change as the `v1` and `v1beta2` endpoints are identical. If you pinned to
`v1beta2`, you are encouraged to move to `v1`.

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

### Packaging

- Change "Development Status" in package metadata from `3 - Alpha`
  to `4 - Beta` (eb43849569556c6e47f11b8310864c5a280507f2)

PyPI: https://pypi.org/project/google-cloud-videointelligence/0.28.0/
