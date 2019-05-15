# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-storage/#history

## 1.15.1

05-14-2019 12:33 PDT

### Implementation Changes
- Widen range for 'google-cloud-core'. ([#7978](https://github.com/googleapis/google-cloud-python/pull/7978))

## 1.15.0

04-17-2019 15:37 PDT

### New Features
- Add support for V4 signed URLs ([#7460](https://github.com/googleapis/google-cloud-python/pull/7460))
- Add generation arguments to bucket / blob methods. ([#7444](https://github.com/googleapis/google-cloud-python/pull/7444))

### Implementation Changes
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Ensure that 'Blob.reload' passes encryption headers. ([#7441](https://github.com/googleapis/google-cloud-python/pull/7441))

### Documentation
- Update client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))

### Internal / Testing Changes
- Fix failing system tests ([#7714](https://github.com/googleapis/google-cloud-python/pull/7714))
- Increase number of retries for 429 errors. ([#7484](https://github.com/googleapis/google-cloud-python/pull/7484))
- Un-flake KMS integration tests expecting empty bucket. ([#7479](https://github.com/googleapis/google-cloud-python/pull/7479))

## 1.14.0

02-06-2019 12:49 PST


### New Features
- Add 'Bucket.iam_configuration' property, enabling Bucket-Policy-Only. ([#7066](https://github.com/googleapis/google-cloud-python/pull/7066))

### Documentation
- Improve docs for 'generate_signed_url'. ([#7201](https://github.com/googleapis/google-cloud-python/pull/7201))

## 1.13.2

12-17-2018 17:02 PST


### Implementation Changes
- Update `Blob.update_storage_class` to support rewrite tokens. ([#6527](https://github.com/googleapis/google-cloud-python/pull/6527))

### Internal / Testing Changes
- Skip signing tests for insufficient credentials ([#6917](https://github.com/googleapis/google-cloud-python/pull/6917))
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))
- Normalize docs for `page_size` / `max_results` / `page_token`. ([#6842](https://github.com/googleapis/google-cloud-python/pull/6842))

## 1.13.1

12-10-2018 13:31 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Accomodate new back-end restriction on retention period. ([#6388](https://github.com/googleapis/google-cloud-python/pull/6388))
- Avoid deleting a blob renamed to itself ([#6365](https://github.com/googleapis/google-cloud-python/pull/6365))

### Dependencies
- Update dependency to google-cloud-core ([#6835](https://github.com/googleapis/google-cloud-python/pull/6835))
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))

### Internal / Testing Changes
- Blacken libraries ([#6794](https://github.com/googleapis/google-cloud-python/pull/6794))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))
- Harden teardown in system tests. ([#6444](https://github.com/googleapis/google-cloud-python/pull/6444))
- Harden `create_bucket` call in systests vs. 429 TooManyRequests. ([#6401](https://github.com/googleapis/google-cloud-python/pull/6401))
- Skip public bucket test in VPC Service Controls  ([#6230](https://github.com/googleapis/google-cloud-python/pull/6230))
- Fix lint failure. ([#6219](https://github.com/googleapis/google-cloud-python/pull/6219))
- Disable test running in VPC Service Controls  restricted environment ([#6215](https://github.com/googleapis/google-cloud-python/pull/6215))
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 1.13.0

### New Features
- Add support for bucket retention policies ([#5534](https://github.com/googleapis/google-cloud-python/pull/5534))
- Allow `destination.content_type` to be None in `Blob.compose`. ([#6031](https://github.com/googleapis/google-cloud-python/pull/6031))

### Implementation Changes
- Ensure that `method` for `Blob.generate_signed_url` is uppercase. ([#6110](https://github.com/googleapis/google-cloud-python/pull/6110))

### Documentation
- Clarify GCS URL signing limitations on GCE ([#6104](https://github.com/googleapis/google-cloud-python/pull/6104))
- Redirect renamed 'usage.html'/'client.html' -> 'index.html'. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))

## 1.12.0

### New Features
- Add support for Python 3.7, drop support for Python 3.4. ([#5942](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5942))
- Add lifecycle rules helpers to bucket. ([#5877](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5877))

### Implementation Changes
- Add 'stacklevel=2' to deprecation warnings. ([#5897](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5897))

### Documentation
- Storage docs: fix typos. ([#5933](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5933))
- Prep storage docs for repo split. ([#5923](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5923))

### Internal / Testing Changes
- Harden systest teardown further. ([#5900](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5900))
- Nox: use inplace installs ([#5865](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5865))

## 1.11.0

### Implementation Changes
- Preserve message / args from an `InvalidResponse`. (#5492)
- Fix generating signed urls for blobs with non-ascii names. (#5625)
- Move bucket location specification to `Bucket.create`; deprecate `Bucket.location` setter (#5808)

### New Features
- Add `Client.get_service_account_email`. (#5765)

### Documentation
- Clarify `None` values for resource-backed properties. (#5509)
- Elaborate docs for `{Bucket,Blob}.make_{public,private}`; note how to enable anonymous accesss to `Blob.public_url`. (#5767)

### Internal / Testing Changes
- Harden `create_bucket` systest against 429 responses. (#5535)
- Add system test: signed URLs w/ non-ASCII blob name. (#5626)
- Harden `tearDownModule` against 429 TooManyRequests. (#5701)
- Retry `notification.create()` on `503 ServiceUnavailable`. (#5741)
- Fix failing KMS system tests. (#5832, #5837, #5860)

## 1.10.0

### New Features
- Add support for KMS keys (#5259)
- Add `{Blob,Bucket}make_private` method (#5336)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)

## 1.9.0

### Implementation Changes
- Change GCS batch endpoint from `/batch` to `/batch/storage/v1` (#5040)

### New Features
- Allow uploading files larger than 2GB by using Resumable Media Requests (#5187)
- Add range downloads (#5081)

### Documentation
- Update docstring to reflect correct units (#5277)
- Replace link to 404 object IAM docs with a note on limited utility. (#5181)
- Update doc reference in GCS client documentation (#5084)
- Add see also for `Bucket.create` method call for `Client.create_bucket()` documentation. (#5073)
- Link out to requester pays docs. (#5065)

### Internal / Testing Changes
- Add testing support for Python 3.7; remove testing support for Python 3.4. (#5295)
- Fix bad trove classifier
- Remove unused var (flake8 warning) (#5280)
- Fix unit test moving batch to batch/storage/v1 (#5082)

## 1.8.0

### New features

- Implement predefined acl (#4757)
- Add support for resumable signed url generation (#4789)

### Implementation changes

- Do not quote embedded slashes for public / signed URLs (#4716)

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Missing word in docstring (#4763)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)

## 1.7.0

### Features

- Enable anonymous access to blobs in public buckets (#4315)
- Make project optional / overridable for storage client (#4381)
- Relax regex used to test for valid project IDs (#4543)
- Add support for `source_generation` parameter to `Bucket.copy_blob` (#4546)

## 1.6.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Requiring `google-resumable-media >= 0.3.1` (#4244)

PyPI: https://pypi.org/project/google-cloud-storage/1.6.0/
