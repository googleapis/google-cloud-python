# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-storage/#history

## 1.19.0

08-28-2019 09:45 PDT

### Implementation Changes
- Expose 'HMACKeyMetadata.id' field. ([#9115](https://github.com/googleapis/google-cloud-python/pull/9115))
- Make 'Blob.bucket' a readonly property. ([#9113](https://github.com/googleapis/google-cloud-python/pull/9113))
- Clarify 'response_type' for signed_url methods. ([#8942](https://github.com/googleapis/google-cloud-python/pull/8942))

### New Features
- Add `client_options` to constructors for manual clients. ([#9054](https://github.com/googleapis/google-cloud-python/pull/9054))

### Documentation
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))

### Internal / Testing Changes
- Remove CI for gh-pages, use googleapis.dev for api_core refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Fix tests broken by yesterday's google-resumable-media release. ([#9119](https://github.com/googleapis/google-cloud-python/pull/9119))
- Harden 'test_access_to_public_bucket' systest against 429 / 503 errors. ([#8997](https://github.com/googleapis/google-cloud-python/pull/8997))

## 1.18.0

08-07-2019 00:37 PDT


### New Features
- Add HMAC key support. ([#8430](https://github.com/googleapis/google-cloud-python/pull/8430))

### Documentation
- Mark old storage classes as legacy, not deprecated. ([#8887](https://github.com/googleapis/google-cloud-python/pull/8887))

### Internal / Testing Changes
- Normalize 'lint' / 'blacken' support under nox. ([#8831](https://github.com/googleapis/google-cloud-python/pull/8831))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.17.0

07-24-2019 12:37 PDT


### New Features
- Add `Bucket.location_type` property. ([#8570](https://github.com/googleapis/google-cloud-python/pull/8570))
- Add `Client.list_blobs(bucket_or_name)`. ([#8375](https://github.com/googleapis/google-cloud-python/pull/8375))


### Implementation Changes
- Retry bucket creation in signing setup. ([#8620](https://github.com/googleapis/google-cloud-python/pull/8620))
- Fix URI -> blob name conversion in `Client download_blob_to_file`. ([#8440](https://github.com/googleapis/google-cloud-python/pull/8440))
- Avoid escaping tilde in blob public / signed URLs. ([#8434](https://github.com/googleapis/google-cloud-python/pull/8434))
- Add generation to 'Blob.__repr__'. ([#8423](https://github.com/googleapis/google-cloud-python/pull/8423))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))
- Fix example in `Client.download_blob_to_file` docstring. ([#8629](https://github.com/googleapis/google-cloud-python/pull/8629))
- Remove typing information for kwargs to not conflict with type checkers ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))

### Internal / Testing Changes
- Skip failing `test_bpo_set_unset_preserves_acls` systest. ([#8617](https://github.com/googleapis/google-cloud-python/pull/8617))
- Add nox session 'docs'. ([#8478](https://github.com/googleapis/google-cloud-python/pull/8478))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 1.16.1

06-04-2019 11:09 PDT


### Dependencies
- Don't pin `google-api-core` in libs using `google-cloud-core`. ([#8213](https://github.com/googleapis/google-cloud-python/pull/8213))

### Documentation
- Fix example in `download_blob_to_file` docstring. ([#8201](https://github.com/googleapis/google-cloud-python/pull/8201))
- Tweak `fields` docstring further. ([#8040](https://github.com/googleapis/google-cloud-python/pull/8040))
- Improve docs for `fields` argument to `Bucket.list_blobs`. ([#8023](https://github.com/googleapis/google-cloud-python/pull/8023))
- Fix docs typo. ([#8027](https://github.com/googleapis/google-cloud-python/pull/8027))

### Internal / Testing Changes
- Retry harder in face of 409/429 during module teardown. ([#8113](https://github.com/googleapis/google-cloud-python/pull/8113))
- Add more retries for 429s during teardown operations. ([#8112](https://github.com/googleapis/google-cloud-python/pull/8112))

## 1.16.0

05-16-2019 12:55 PDT


### New Features
- Update `Client.create_bucket` to take a Bucket object or string. ([#7820](https://github.com/googleapis/google-cloud-python/pull/7820))
- Update `Client.get_bucket` to take a `Bucket` object or string. ([#7856](https://github.com/googleapis/google-cloud-python/pull/7856))
- Add `Client.download_blob_to_file` method. ([#7949](https://github.com/googleapis/google-cloud-python/pull/7949))
- Add `client_info` support to client / connection. ([#7872](https://github.com/googleapis/google-cloud-python/pull/7872))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))
- Pin `google-auth >= 1.2.0`. ([#7798](https://github.com/googleapis/google-cloud-python/pull/7798))

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
