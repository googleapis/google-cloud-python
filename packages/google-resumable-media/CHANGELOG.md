# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-resumable-media/#history

## 0.4.1

09-16-2019 17:59 PDT


### Implementation Changes
- Revert "Always use raw response data. ([#87](https://github.com/googleapis/google-resumable-media-python/pull/87))" ([#103](https://github.com/googleapis/google-resumable-media-python/pull/103))

### Internal / Testing Changes
- Add black. ([#94](https://github.com/googleapis/google-resumable-media-python/pull/94))

## 0.4.0

09-05-2019 11:59 PDT

### Backward-Compatibility Note

The change to use raw response data (PR
[#87](https://github.com/googleapis/google-resumable-media-python/pull/87))
might break the hypothetical usecase of downloading a blob marked with
`Content-Encoding: gzip` and expecting to get the expanded data.

### Implementation Changes
- Require 200 response for initial resumable upload request. ([#95](https://github.com/googleapis/google-resumable-media-python/pull/95))
- Use `response` as variable for object returned from `http_request`. ([#98](https://github.com/googleapis/google-resumable-media-python/pull/98))
- Further DRY request dependency pins. ([#96](https://github.com/googleapis/google-resumable-media-python/pull/96))
- Finish download on seeing 416 response with zero byte range. ([#86](https://github.com/googleapis/google-resumable-media-python/pull/86))
- Always use raw response data. ([#87](https://github.com/googleapis/google-resumable-media-python/pull/87))

### Dependencies
- Drop runtime dependency check on `requests`. ([#97](https://github.com/googleapis/google-resumable-media-python/pull/97))

### Documentation
- Update docs after release ([#93](https://github.com/googleapis/google-resumable-media-python/pull/93))

## 0.3.3

08-23-2019 14:15 PDT

### Implementation Changes
- Add a default timeout for the http_request method ([#88](https://github.com/googleapis/google-resumable-media-python/pull/88))
- DRY 'requests' pin; don't shadow exception. ([#83](https://github.com/googleapis/google-resumable-media-python/pull/83))
- Drop a hardcoded value in an error message. ([#48](https://github.com/googleapis/google-resumable-media-python/pull/48))

### Documentation
- Reconstruct 'CHANGELOG.md' from pre-releasetool era releases. ([#66](https://github.com/googleapis/google-resumable-media-python/pull/66))

### Internal / Testing Changes
- Use Kokoro for CI ([#90](https://github.com/googleapis/google-resumable-media-python/pull/90))
- Renovate: preserve semver ranges. ([#82](https://github.com/googleapis/google-resumable-media-python/pull/82))
- Add renovate.json ([#79](https://github.com/googleapis/google-resumable-media-python/pull/79))
- Fix systest bitrot. ([#77](https://github.com/googleapis/google-resumable-media-python/pull/77))
- Fix docs build redux. ([#75](https://github.com/googleapis/google-resumable-media-python/pull/75))
- Update to new nox ([#57](https://github.com/googleapis/google-resumable-media-python/pull/57))

## 0.3.2

2018-12-17 17:31 PST

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
- Add Appveyor support. ([#40](https://github.com/googleapis/google-resumable-media-python/pull/40))
- Mark the version in `master` as `.dev1`.


## 0.3.1

2017-10-20

### Implementation Changes

- Add requests/urllib3 work-around for intercepting gzipped bytes. ([#36](https://github.com/googleapis/google-resumable-media-python/pull/36))

### Internal / Testing Changes
- Re-factor `system/requests/test_download.py`. ([#35](https://github.com/googleapis/google-resumable-media-python/pull/35))


## 0.3.0

2017-10-13

### Implementation Changes

- Add checksum validation for non-chunked non-composite downloads. ([#32](https://github.com/googleapis/google-resumable-media-python/pull/32))

### Dependencies

- Add `requests` extra to `setup.py`. ([#30](https://github.com/googleapis/google-resumable-media-python/pull/30))

### Documentation

- Update generated docs, due to updated `objects.inf` from reequests.


## 0.2.3

2017-08-07

### Implementation Changes

- Allow empty files to be uploaded. ([#25](https://github.com/googleapis/google-resumable-media-python/pull/25))


## 0.2.2

2017-08-01

### Implementation Changes

- Swap the order of `_write_to_stream()` / `_process_response()` in `requests` download. ([#24](https://github.com/googleapis/google-resumable-media-python/pull/24))
- Use requests `iter_content()` to avoid storing response body in RAM. ([#21](https://github.com/googleapis/google-resumable-media-python/pull/21))
- Add optional stream argument to DownloadBase. ([#20](https://github.com/googleapis/google-resumable-media-python/pull/20))


## 0.2.1

2017-07-21

### Implementation Changes

- Drop usage of `size` to measure (resumable) bytes uploaded. ([#18](https://github.com/googleapis/google-resumable-media-python/pull/18))
- Use explicit u prefix on unicode strings. ([#16](https://github.com/googleapis/google-resumable-media-python/pull/16))

### Internal / Testing Changes

- Update `author_email1` to official mailing list.

## 0.2.0

2017-07-18

### Implementation Changes

- Ensure passing  unicode to `json.loads()` rather than `bytes`. ([#13](https://github.com/googleapis/google-resumable-media-python/pull/13))
- Add `MANIFEST.in` to repository. ([#9](https://github.com/googleapis/google-resumable-media-python/pull/9))
- Move contents of exceptions module into common.

### Documentation

- Update docs after latest version of Sphinx. ([#11](https://github.com/googleapis/google-resumable-media-python/pull/11))
- Update `custom_html_writer` after Sphinx update removed a class. ([#10](https://github.com/googleapis/google-resumable-media-python/pull/10))

### Internal / Testing Changes

- Use nox `session.skip` (instead of ValueError) for system tests. ([#14](https://github.com/googleapis/google-resumable-media-python/pull/14))


## 0.1.1

2017-05-05


### Implementation Changes

- Add `common.RetryStrategy` class; us it in `wait_and_retry`.
- Rename `constants` module -> `common`.


## 0.1.0

2017-05-03

### Implementation Changes

- Pass `total_bytes` in `requests.ResumableUpload.initiate`.


## 0.0.5

2017-05-02

### New Features

- Add support for resumable uploads of unknown size. ([#6](https://github.com/googleapis/google-resumable-media-python/pull/6))


## 0.0.4

2017-04-28

### Implementation Changes

- Refactor upload / download support into public, transport-agnostic classes and private, `requests`-specific implementations.


## 0.0.3

2017-04-24

### New Features

- Add automatic retries for 429, 500, 502, 503 and 504 error responses. ([#4](https://github.com/googleapis/google-resumable-media-python/pull/4))


## 0.0.2

2017-04-24

### New Features

- Add optional `headers` to upload / download classes.

### Documentation

- Automate documentation builds via CircleCI.


## 0.0.1

2017-04-21

- Initial public release.

