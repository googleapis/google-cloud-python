# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-ads-datamanager/#history

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-datamanager-v0.3.0...google-ads-datamanager-v0.4.0) (2026-02-05)


### Documentation

* describe additional URI format for kek_uri in GcpEncryptionInfo and AwsKmsEncryptionInfo ([fe0a0b4638a8f5301c30be43fd2f2898ddc6db37](https://github.com/googleapis/google-cloud-python/commit/fe0a0b4638a8f5301c30be43fd2f2898ddc6db37))


### Bug Fixes

* update `go_package` packaging option from `google.golang.org/genproto/googleapis/ads/datamanager/v1;datamanager` to `cloud.google.com/go/datamanager/apiv1/datamanagerpb;datamanagerpb` ([fe0a0b4638a8f5301c30be43fd2f2898ddc6db37](https://github.com/googleapis/google-cloud-python/commit/fe0a0b4638a8f5301c30be43fd2f2898ddc6db37))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-datamanager-v0.2.0...google-ads-datamanager-v0.3.0) (2026-01-08)


### Features

* auto-enable mTLS when supported certificates are detected ([c353aa5bcc937ef9399c8efc90492dadbcf01aa2](https://github.com/googleapis/google-cloud-python/commit/c353aa5bcc937ef9399c8efc90492dadbcf01aa2))
* check Python and dependency versions in generated GAPICs ([c353aa5bcc937ef9399c8efc90492dadbcf01aa2](https://github.com/googleapis/google-cloud-python/commit/c353aa5bcc937ef9399c8efc90492dadbcf01aa2))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-datamanager-v0.1.0...google-ads-datamanager-v0.2.0) (2025-12-04)


### Features

* add `event_name` to `Event` for specifying the name of the Google Analytics event ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add new error codes `UNSUPPORTED_OPERATING_ACCOUNT_FOR_DATA_PARTNER`, `UNSUPPORTED_LINKED_ACCOUNT_FOR_DATA_PARTNER`, `INVALID_PROPERTY_TYPE`, `INVALID_STREAM_TYPE`, `LINKED_ACCOUNT_ONLY_ALLOWED_WITH_DATA_PARTNER_LOGIN_ACCOUNT`, `OPERATING_ACCOUNT_LOGIN_ACCOUNT_MISMATCH`, `EVENT_TIME_INVALID`, `RESERVED_NAME_USED`, `INVALID_EVENT_NAME`, `NOT_ALLOWLISTED`, `MULTIPLE_DESTINATIONS_FOR_GOOGLE_ANALYTICS_EVENT`, `FIELD_VALUE_TOO_LONG`, `TOO_MANY_ELEMENTS` to `ErrorReason` enum ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `PROCESSING_ERROR_REASON_AWS_AUTH_FAILED` to `ProcessingErrorReason` enum ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `additional_user_properties` to `UserProperties` for sending additional key-value pairs of user properties ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `AwsWrappedKeyInfo` to `EncryptionInfo` for supporting data encryption using AWS KMS keys ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `user_id` to `Event` for uniquely identifying a user as defined by the advertiser for Google Analytics events ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `client_id` to `Event` for uniquely identifying a user instance of a web client for a Google Analytics web stream ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `additional_event_parameters` to `Event` for sending additional key-value pairs of event parameters for Google Analytics events ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `GOOGLE_ANALYTICS_PROPERTY` to `AccountType` enum for supporting Google Analytics as a destination ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `additional_item_parameters` to `Item` for sending additional key-value pairs of item parameters ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `item_id` to `Item` for uniquely identifying an item ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))
* add `PROCESSING_WARNING_REASON_AWS_AUTH_FAILED` to `ProcessingWarningReason` enum ([03e69912a61695deefca6ffaae1add8119f026e4](https://github.com/googleapis/google-cloud-python/commit/03e69912a61695deefca6ffaae1add8119f026e4))

## [0.1.0](https://github.com/googleapis/google-cloud-python/compare/google-ads-datamanager-v0.0.0...google-ads-datamanager-v0.1.0) (2025-11-06)


### Features

* onboard a new library  ([8197d16dc5300cd153425dfb29e4dc510a2e7d05](https://github.com/googleapis/google-cloud-python/commit/8197d16dc5300cd153425dfb29e4dc510a2e7d05))
