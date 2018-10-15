# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-firestore/#history

## 0.30.0

10-15-2018 09:04 PDT


### New Features
- Add `Document.collections` method. ([#5613](https://github.com/googleapis/google-cloud-python/pull/5613))
- Add `merge` as an option to `DocumentReference.set()` ([#4851](https://github.com/googleapis/google-cloud-python/pull/4851))
- Return emtpy snapshot instead of raising NotFound exception ([#5007](https://github.com/googleapis/google-cloud-python/pull/5007))
- Add Field path class ([#4392](https://github.com/googleapis/google-cloud-python/pull/4392))

### Implementation Changes
- Avoid overwriting `__module__` of messages from shared modules. ([#5364](https://github.com/googleapis/google-cloud-python/pull/5364))
- Don't omit originally-empty map values when processing timestamps. ([#6050](https://github.com/googleapis/google-cloud-python/pull/6050))

### Documentation
- Prep docs for repo split. ([#6000](https://github.com/googleapis/google-cloud-python/pull/6000))
- Docs: Replace links to `/stable/` with `/latest/`. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))
- Document `FieldPath.from_string` ([#5121](https://github.com/googleapis/google-cloud-python/pull/5121))

### Internal / Testing Changes
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add new conformance tests. ([#6124](https://github.com/googleapis/google-cloud-python/pull/6124))
- Add `synth.py`. ([#6079](https://github.com/googleapis/google-cloud-python/pull/6079))
- Test document update w/ integer ids ([#5895](https://github.com/googleapis/google-cloud-python/pull/5895))
- Nox: use inplace installs ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))
- Re-sync with .proto / .textproto files from google-cloud-common. ([#5351](https://github.com/googleapis/google-cloud-python/pull/5351))
- Modify system tests to use prerelease versions of grpcio ([#5304](https://github.com/googleapis/google-cloud-python/pull/5304))
- Add test runs for Python 3.7 and remove 3.4 ([#5295](https://github.com/googleapis/google-cloud-python/pull/5295))
- Fix over-long line. ([#5129](https://github.com/googleapis/google-cloud-python/pull/5129))
- Distinguish `FieldPath` classes from field path strings ([#4466](https://github.com/googleapis/google-cloud-python/pull/4466))
- Fix bad trove classifier
- Cleanup `FieldPath` ([#4996](https://github.com/googleapis/google-cloud-python/pull/4996))
- Fix typo in `Document.collections` docstring. ([#5669](https://github.com/googleapis/google-cloud-python/pull/5669))
- Implement `FieldPath.__add__` ([#5149](https://github.com/googleapis/google-cloud-python/pull/5149))

## 0.29.0

### New features

- All non-simple field names are converted into unicode (#4859)

### Implementation changes

- The underlying generated code has been re-generated to pick up new features and bugfixes. (#4916)
- The `Admin` API interface has been temporarily removed.

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)
- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Documentation

- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- System test fix, changed ALREADY_EXISTS and MISSING_ENTITY to DOCUMENT_EXISTS and MISSING_DOCUMENT and updated wording (#4803)
- Cross-language tests (#4359)
- Fix import column lengths pass 79 (#4464)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-firestore/0.28.0/
