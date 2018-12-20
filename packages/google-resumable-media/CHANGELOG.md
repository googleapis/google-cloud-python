# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-resumable-media/#history

## 0.3.2

12-17-2018 17:31 PST

### Implementation Changes
- Using `str` instead of `repr` for multipart boundary.

### Dependencies
- Making `requests` a strict dependency for the `requests` subpackage.

### Documentation
- Announce deprecation of Python 2.7 ([#51](https://github.com/googleapis/google-resumable-media-python/pull/51))
- Fix broken redirect after repository move
- Updating generated static content in docs.

### Internal / Testing Changes
- Modify file not found test to look for the correct error message
- Harden tests so they can run with debug logging statements
- Adding AppVeyor support.
- Marking the version in `master` as `.dev1`.

