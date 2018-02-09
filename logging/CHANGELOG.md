# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-logging/#history

## 1.5.0

### Implementation Changes
  - Pass `grace period` and `batch size` to `worker` in
    `background_thread` (#4369)
  - Implement `unique_writer_identity` (#4595)
  - Expose `writer_identity` returned in `Sink` resource. (#4704)
  - Move `unique_writer_identity` from `LogSink` ctor to `create` (#4706)
  - Accomodate back-end change making 'Sink.filter' optional in
    constructor(#4699)
  - `LogSink.create` Capture Server-generated writer_identity (#4707)
  - Support passing `unique_writer_identity` to `Sink.update` (#4708)
  - The underlying client library was re-generated to fix bugs and to use new
    GAPIC library (#4759)
  - Add `max_latency` to `BackgroundThreadTransport` (#4762)
  - Change `AppEngineHandler` to apply labels from `get_gae_labels()` to
    `emit()` (#4824)


### Dependencies
  - Pinning `Django` test dependency to < 2.0 in Python 2.7 (#4519)

PyPI: https://pypi.org/project/google-cloud-logging/1.4.1/


## 1.4.0

### Implementation Changes

- Remove `deepcopy` of `Client._http` in background transport (#3954)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)
- Deferring to `google-api-core` for `grpcio` and
  `googleapis-common-protos`dependencies (#4096, #4098)

PyPI: https://pypi.org/project/google-cloud-logging/1.4.0/
