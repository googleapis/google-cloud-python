# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-monitoring/#history

## 0.30.1

### Implementation Changes
- Monitoring: Add Transports Layer to clients (#5594)
- Remove gRPC size restrictions (4MB default) (#5594)

### Documentation
- Monitoring. Update documentation links. (#5557)

## 0.30.0

### Implementation Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)

### New Features
- Add aliases for new V3 service clients. (#5424)

### Documentation
- Remove link to `usage` on index of monitoring (#5272)

### Internal / Testing Changes
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)

## 0.29.0

### Implementation Changes
- Update monitoring library to use new generated client (#5212)
- Move aligner and reducer links from timeSeries.list to alertPolicies (#5011)

### Internal / Testing Changes
- Fix bad trove classifier

## 0.28.1

### Implementation changes

- Convert label values to str in client.metric() (#4910)

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

## 0.28.0

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-monitoring/0.28.0/
