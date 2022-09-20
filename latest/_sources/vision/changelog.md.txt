# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-vision/#history

## 0.39.0

08-12-2019 13:57 PDT

### Implementation Changes
- Remove send/recv msg size limit (via synth). ([#8976](https://github.com/googleapis/google-cloud-python/pull/8976))

### New Features
- Add 'parent' argument to annotation requests; add 'ProductSearchClient.purge_products' method; add 'object_annotations' field to product search results (via synth). ([#8988](https://github.com/googleapis/google-cloud-python/pull/8988))

### Documentation
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 0.38.1

07-24-2019 17:54 PDT

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

## 0.38.0

07-09-2019 10:05 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8411](https://github.com/googleapis/google-cloud-python/pull/8411))

### New Features
- Add 'client_options' support, update list method docstrings (via synth). ([#8529](https://github.com/googleapis/google-cloud-python/pull/8529))

### Internal / Testing Changes
- Pin black version (via synth). ([#8602](https://github.com/googleapis/google-cloud-python/pull/8602))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- All of the negative vision vpc sc tests should use the same file. ([#8439](https://github.com/googleapis/google-cloud-python/pull/8439))
- In order to make sure access to the bucket is blocked by vpc sc, try to download any arbitrary file from the bucket. ([#8374](https://github.com/googleapis/google-cloud-python/pull/8374))
- Add disclaimer to auto-generated template files (via synth). ([#8335](https://github.com/googleapis/google-cloud-python/pull/8335))
- Add Vision API system tests to verify accessing a gcs bucket outside of a secure perimeter is blocked. ([#8276](https://github.com/googleapis/google-cloud-python/pull/8276))
- Add Vision API Product Search tests to verify ProductSearch is blocked by VPC SC when trying to access a resource outside of a secure perimeter when run from within a secure perimeter. ([#8269](https://github.com/googleapis/google-cloud-python/pull/8269))
- Add AsyncBatchAnnotateFiles system test ([#8260](https://github.com/googleapis/google-cloud-python/pull/8260))
- Add ImportProductSets system test ([#8259](https://github.com/googleapis/google-cloud-python/pull/8259))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8257](https://github.com/googleapis/google-cloud-python/pull/8257))
- Declare encoding as utf-8 in pb2 files (via synth).  ([#8371](https://github.com/googleapis/google-cloud-python/pull/8371))

## 0.37.0

05-30-2019 15:19 PDT

### Implementation Changes
- Add routing header to method metadata (via synth).  ([#7604](https://github.com/googleapis/google-cloud-python/pull/7604))

### New Features
- Add more categories to product search, update noxfile (via synth). ([#8170](https://github.com/googleapis/google-cloud-python/pull/8170))
- Add batch annotation for images and files, reorder methods (via synth).  ([#7845](https://github.com/googleapis/google-cloud-python/pull/7845))
- Vision: Add proto files for v1p4beta1

### Internal / Testing Changes
- Change docstrings (via synth). ([#7983](https://github.com/googleapis/google-cloud-python/pull/7983))
- Add system tests for Vision Product Search. Test product set resource… ([#7913](https://github.com/googleapis/google-cloud-python/pull/7913))
-  Update noxfile and docs configuration (via synth). ([#7839](https://github.com/googleapis/google-cloud-python/pull/7839))
- Vision: Add nox session `docs`, reorder methods, modify samples in docstrings (via synth). ([#7787](https://github.com/googleapis/google-cloud-python/pull/7787))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))
- Copy lintified proto files (via synth). ([#7473](https://github.com/googleapis/google-cloud-python/pull/7473))

## 0.36.0

02-25-2019 15:02 PST


### Implementation Changes
- Remove unused message exports. ([#7280](https://github.com/googleapis/google-cloud-python/pull/7280))
- Protoc-generated serialization update. ([#7100](https://github.com/googleapis/google-cloud-python/pull/7100))
- GAPIC generation fixes: ([#7058](https://github.com/googleapis/google-cloud-python/pull/7058))
- Pick up order-of-enum fix from GAPIC generator. ([#6881](https://github.com/googleapis/google-cloud-python/pull/6881))

### New Features
- Add vision v1p4beta1. ([#7438](https://github.com/googleapis/google-cloud-python/pull/7438))

### Documentation
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Update copyright headers.

### Internal / Testing Changes
- Add clarifying comment to blacken nox target. ([#7408](https://github.com/googleapis/google-cloud-python/pull/7408))
- Copy proto files alongside protoc versions
- Vision: get system logo tests healthy. ([#7245](https://github.com/googleapis/google-cloud-python/pull/7245))
- Add protos as an artifact to library. ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))

## 0.35.2

12-17-2018 17:10 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

### Internal / Testing Changes
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))

## 0.35.1

11-21-2018 11:25 PST

### Implementation Changes
- Add ProductSearchClient to vision.py ([#6635](https://github.com/googleapis/google-cloud-python/pull/6635))

### Internal / Testing Changes
- Merge fixes to GAPIC generator. ([#6632](https://github.com/googleapis/google-cloud-python/pull/6632))

## 0.35.0

11-13-2018 09:55 PST


### Implementation Changes
- Fix client_info bug, update docstrings via synth. ([#6437](https://github.com/googleapis/google-cloud-python/pull/6437))

### New Features
- Add 'product_search_client' to 'vision_v1'. ([#6361](https://github.com/googleapis/google-cloud-python/pull/6361))

### Dependencies
- Bump minimum 'api_core' version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))

### Documentation
- Fix GAX fossils. ([#6264](https://github.com/googleapis/google-cloud-python/pull/6264))
- Normalize use of support level badges. ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Harmonize / DRY 'README.rst' / 'docs/index.rst'. ([#6003](https://github.com/googleapis/google-cloud-python/pull/6003))

### Internal / Testing Changes
- Use new Nox. ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))

## 0.34.0

### Implementation Changes

- Clean up feature introspection. ([#5851](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5851))

### New Features

- Regenerate to pick up new features in the underlying API. ([#5854](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/5854))

## 0.33.0

### New Features
- Add v1p3beta1 endpoint to vision client library (#5638)

## 0.32.0

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Regenerate underlying client library (#5467)

### Internal / Testing Changes
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.31.1

### Packaging
- Update setuptools before packaging (#5265)

## 0.31.0

- Vision v1p2beta1: PDF/TIFF OCR (#5127)
- Use `install_requires` for platform dependencies instead of `extras_require` (#4991)
- Add vision v1p2beta1 (#4998)
- Fix bad trove classifier
- Add max results to feature (#4817)

## 0.30.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Fix coveragerc to correctly omit generated files (#4843)

## 0.29.0

### :warning: Breaking Changes

- The HTTP/JSON based client that was deprecated in 0.25.0 is completely
  removed.

### Release Candidate

- This is the (hopefully) final release candidate before declaring a stable
  release.

### Features

- The `v1p1beta1` endpoint has been added. (#4493)

  This is a superset of `v1` and includes features that are still in beta
  on the API side. You can opt in to this endpoint by importing it explicitly:

  ```python
  from google.cloud import vision_v1p1beta1
  client = vision_v1p1beta1.ImageAnnotatorClient()
  ```

PyPI: https://pypi.org/project/google-cloud-vision/0.29.0/


## 0.28.0

### Notable Implementation Changes

- Update and re-organize autogenerated code (#3952)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-vision/0.28.0/
