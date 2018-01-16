# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-storage/#history

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
