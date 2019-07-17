# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-translate/#history

## 1.6.0

07-09-2019 13:13 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8409](https://github.com/googleapis/google-cloud-python/pull/8409))
- Update service descriptions and add additional rpc bindings for Translate ([#8267](https://github.com/googleapis/google-cloud-python/pull/8267))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8527](https://github.com/googleapis/google-cloud-python/pull/8527))

### Internal / Testing Changes
- Pin black version (via synth). ([#8600](https://github.com/googleapis/google-cloud-python/pull/8600))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth).  ([#8369](https://github.com/googleapis/google-cloud-python/pull/8369))
- Add disclaimer to auto-generated template files (via synth).  ([#8333](https://github.com/googleapis/google-cloud-python/pull/8333))
- Blacken (via synth). ([#8282](https://github.com/googleapis/google-cloud-python/pull/8282))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8255](https://github.com/googleapis/google-cloud-python/pull/8255))
- Fix coverage in 'types.py' (via synth). ([#8168](https://github.com/googleapis/google-cloud-python/pull/8168))
- Blacken noxfile.py, setup.py (via synth). ([#8135](https://github.com/googleapis/google-cloud-python/pull/8135))
- Add empty lines (via synth). ([#8076](https://github.com/googleapis/google-cloud-python/pull/8076))

## 1.5.0

05-16-2019 13:05 PDT


### Implementation Changes
- Add routing header to method metadata, fix docstring (via synth). ([#7660](https://github.com/googleapis/google-cloud-python/pull/7660))

### New Features
- Add `client_info` support to client / connection. ([#7873](https://github.com/googleapis/google-cloud-python/pull/7873))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Add docs for v3beta1. ([#7681](https://github.com/googleapis/google-cloud-python/pull/7681))

### Internal / Testing Changes
- Harden system test against back-end changes. ([#7987](https://github.com/googleapis/google-cloud-python/pull/7987))
- Exclude `docs/conf.py` in synth. ([#7943](https://github.com/googleapis/google-cloud-python/pull/7943))
- Update `docs/conf.py` (via synth). ([#7837](https://github.com/googleapis/google-cloud-python/pull/7837))
- Add nox session `docs`, reorder methods (via synth). ([#7785](https://github.com/googleapis/google-cloud-python/pull/7785))

## 1.4.0

04-02-2019 14:24 PDT


### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add Translate v3 ([#7637](https://github.com/googleapis/google-cloud-python/pull/7637))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

## 1.3.3

12-17-2018 17:07 PST


### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

## 1.3.2

12-10-2018 13:33 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Fix rtype for `Client.detect_language` for single values ([#5397](https://github.com/googleapis/google-cloud-python/pull/5397))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Fix installation package in README.rst ([#6426](https://github.com/googleapis/google-cloud-python/pull/6426))
- Fix [#6321](https://github.com/googleapis/google-cloud-python/pull/6321) Update README service links in quickstart guides. ([#6322](https://github.com/googleapis/google-cloud-python/pull/6322))
- Docs: normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Restore detailed usage docs. ([#5999](https://github.com/googleapis/google-cloud-python/pull/5999))
- Redirect renamed 'usage.html'/'client.html' -> 'index.html'. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))
- Prep translate docs for repo split. ([#5941](https://github.com/googleapis/google-cloud-python/pull/5941))

### Internal / Testing Changes
- Add blacken to noxfile ([#6795](https://github.com/googleapis/google-cloud-python/pull/6795))
- Blackening Continued... ([#6667](https://github.com/googleapis/google-cloud-python/pull/6667))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Adapt system test to updated back-end translation. ([#6427](https://github.com/googleapis/google-cloud-python/pull/6427))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/googleapis/google-cloud-python/pull/5304))
- Add Test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix bad trove classifier

## 1.3.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 1.3.0

### Notable Implementation Changes

- Use POST (rather than GET) for API `translate` requests (#4095,
  h/t to @Maerig)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)
- Fix example in `Config.get_variable()` (#3910)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-translate/1.3.0/
