# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-dlp/#history

## 0.7.0

### New Features
- Add StoredInfoTypes (#5809)

## 0.6.0

### New Features
- Regenerate DLP v2 endpoint (redact image, delta presence) (#5666)

### Internal / Testing Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Modify system tests to use prerelease versions of grpcio (#5304)

## 0.5.0

### New Features
- Add PublishSummaryToCscc (#5246)
- Add configurable row limit (#5246)
- Add EntityID added to risk stats (#5246)
- Add dictionaries via GCS (#5246)

## 0.4.0

### Implementation Changes

- Remove DLP client version V2Beta1 (#5155)

## 0.3.0

### Implementation changes

- The library has been regenerated to pick up changes from the API's proto definition. (#5131)

## 0.2.0

### Interface additions

- Add DLP v2 (#5059)

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Testing and internal changes

- Normalize all setup.py files (#4909)

## 0.1.0

Initial release of the DLP (Data Loss Prevention) client library. (#4879)


