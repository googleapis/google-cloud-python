# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigquery-datatransfer/#history

## 0.2.0

### Implementation Changes
- Regenerate bigquery-datatransfer (#5793)

### Internal / Testing Changes
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Modify system tests to use prerelease versions of grpcio (#5304)
- Add Test runs for Python 3.7 and remove 3.4 (#5295)
- Fix bad trove classifier
- Rename releases to changelog and include from CHANGELOG.md (#5191)

## 0.1.1

### Dependencies

- Update dependency range for api-core to include v1.0.0 releases (#4944)

### Documentation

- Fix package name in readme (#4670)
- BigQueryDataTransfer: update 404 link for API documentation (#4672)
- Replacing references to `stable/` docs with `latest/`. (#4638)

### Testing and internal changes

- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Update index.rst (#4816)
- nox unittest updates (#4646)

## 0.1.0

[![release level](https://img.shields.io/badge/release%20level-alpha-orange.svg?style&#x3D;flat)](https://cloud.google.com/terms/launch-stages)

The BigQuery Data Transfer Service automates data movement from SaaS
applications to Google BigQuery on a scheduled, managed basis. Your analytics
team can lay the foundation for a data warehouse without writing a single line
of code. BigQuery Data Transfer Service initially supports Google application
sources like Adwords, DoubleClick Campaign Manager, DoubleClick for Publishers
and YouTube.

PyPI: https://pypi.org/project/google-cloud-bigquery-datatransfer/0.1.0/
