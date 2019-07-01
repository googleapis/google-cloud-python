# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigquery-storage/#history

## 0.5.0

05-20-2019 09:23 PDT

### Implementation Changes

- Increase default deadline on ReadRows. ([#8030](https://github.com/googleapis/google-cloud-python/pull/8030))
- Respect timeout on `client.read_rows`. Don't resume on `DEADLINE_EXCEEDED` errors. ([#8025](https://github.com/googleapis/google-cloud-python/pull/8025))

### Documentation

- Use alabaster theme everwhere. ([#8021](https://github.com/googleapis/google-cloud-python/pull/8021))

## 0.4.0

04-16-2019 13:46 PDT

### Implementation Changes

- Remove gRPC size limit in the transport options ([#7664](https://github.com/googleapis/google-cloud-python/pull/7664))
- Add retry params for create_read_session (via synth). ([#7658](https://github.com/googleapis/google-cloud-python/pull/7658))

### New Features

- Add page iterator to ReadRowsStream ([#7680](https://github.com/googleapis/google-cloud-python/pull/7680))

### Internal / Testing Changes

- Remove system test for split rows ([#7673](https://github.com/googleapis/google-cloud-python/pull/7673))

## 0.3.0

04-02-2019 15:22 PDT

### Dependencies

- Add dependency for resource proto. ([#7585](https://github.com/googleapis/google-cloud-python/pull/7585))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### Documentation

- Fix links to BigQuery Storage API docs ([#7647](https://github.com/googleapis/google-cloud-python/pull/7647))
- Update proto / docstrings (via synth). ([#7461](https://github.com/googleapis/google-cloud-python/pull/7461))
- googlecloudplatform --> googleapis in READMEs ([#7411](https://github.com/googleapis/google-cloud-python/pull/7411))
- Updated client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Blacken new quickstart snippet. ([#7242](https://github.com/googleapis/google-cloud-python/pull/7242))
- Add quickstart demonstrating most BQ Storage API read features ([#7223](https://github.com/googleapis/google-cloud-python/pull/7223))
- Add bigquery_storage to docs ([#7222](https://github.com/googleapis/google-cloud-python/pull/7222))

### Internal / Testing Changes

- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Copy lintified proto files (via synth). ([#7475](https://github.com/googleapis/google-cloud-python/pull/7475))
- Add annotations to protocol buffers indicating request parameters (via synth). ([#7550](https://github.com/googleapis/google-cloud-python/pull/7550))

## 0.2.0

01-25-2019 13:54 PST

### New Features

- Add option to choose dtypes by column in to_dataframe. ([#7126](https://github.com/googleapis/google-cloud-python/pull/7126))

### Internal / Testing Changes

- Update copyright headers
- Protoc-generated serialization update. ([#7076](https://github.com/googleapis/google-cloud-python/pull/7076))
- BigQuery Storage: run 'blacken' during synth ([#7047](https://github.com/googleapis/google-cloud-python/pull/7047))

## 0.1.1

12-17-2018 18:03 PST


### Implementation Changes
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up fixes in GAPIC generator. ([#6708](https://github.com/googleapis/google-cloud-python/pull/6708))

### Documentation
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

### Internal / Testing Changes
- Blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- Correct release_status for bigquery_storage ([#6767](https://github.com/googleapis/google-cloud-python/pull/6767))

## 0.1.0

11-29-2018 13:45 PST

- Initial release of BigQuery Storage API client.

