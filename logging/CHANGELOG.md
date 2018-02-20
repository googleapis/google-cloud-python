# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-logging/#history

## 1.5.0

# New features

- Added `max_latency` to `BackgroundThreadTransport`. (#4762)
- Added support for unique writer identity in `Sink`. (#4595, #4708, #4704, #4706)

# Implementation changes

- The underlying auto-generated client library was re-generated to pick up new features and bugfixes. (#4759)
- Moved the code path of `get_gae_labels()` to `emit()`. (#4824)
- Removed a debug print statement. (#4838)
- `LogSink.create` captures the server-generated `writerIdentity`. (#4707)
- Accomodated a back-end change making `Sink.filter` optional. (#4699)

# Testing

- Fixed system tests (#4768)
- Hardened test for `retrieve_metadata_server` against transparent DNS proxies. (#4698)
- Added cleanup for Pub / Sub topic in logging system test. (#4532)
- Added another check for Python 2.7 in Logging `nox -s default`. (#4523)
- Pinned `django` test dependency to `< 2.0` in Python 2.7. (#4519)
- Maked a `nox -s default` session for all packages. (#4324)
- Shortened test names. (#4321)

# Documentation

- Added doc to highlight missing `uniqueWriterIdentity` field. (#4579)
- Fixing "Fore" -> "For" typo in README docs. (#4317)

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
