# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-apps-chat/#history

## [0.6.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.5.0...google-apps-chat-v0.6.0) (2026-02-05)


### Features

* Addition of QuoteType enum, QuotedMessageSnapshot &amp; ForwardMetadata in the QuotedMessageMetadata proto ([fe0a0b4638a8f5301c30be43fd2f2898ddc6db37](https://github.com/googleapis/google-cloud-python/commit/fe0a0b4638a8f5301c30be43fd2f2898ddc6db37))

## [0.5.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.4.0...google-apps-chat-v0.5.0) (2026-01-08)


### Documentation

* Improve documentation of attachment.proto, event_payload.proto and space.proto ([17cc12897e6afdf3f3131531c50a8226a3f57c0f](https://github.com/googleapis/google-cloud-python/commit/17cc12897e6afdf3f3131531c50a8226a3f57c0f))


### Features

* Add accessory widget support for private messages ([17cc12897e6afdf3f3131531c50a8226a3f57c0f](https://github.com/googleapis/google-cloud-python/commit/17cc12897e6afdf3f3131531c50a8226a3f57c0f))
* Add app authorization support to space APIs ([17cc12897e6afdf3f3131531c50a8226a3f57c0f](https://github.com/googleapis/google-cloud-python/commit/17cc12897e6afdf3f3131531c50a8226a3f57c0f))
* Addition of GMAIL_MESSAGE value for RichLinkType enum in the RichLinkMetadata proto ([17cc12897e6afdf3f3131531c50a8226a3f57c0f](https://github.com/googleapis/google-cloud-python/commit/17cc12897e6afdf3f3131531c50a8226a3f57c0f))
* auto-enable mTLS when supported certificates are detected ([c353aa5bcc937ef9399c8efc90492dadbcf01aa2](https://github.com/googleapis/google-cloud-python/commit/c353aa5bcc937ef9399c8efc90492dadbcf01aa2))
* check Python and dependency versions in generated GAPICs ([c353aa5bcc937ef9399c8efc90492dadbcf01aa2](https://github.com/googleapis/google-cloud-python/commit/c353aa5bcc937ef9399c8efc90492dadbcf01aa2))

## [0.4.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.3.0...google-apps-chat-v0.4.0) (2025-10-28)


### Documentation

* Update field documentations for space.proto and membership.proto  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))


### Features

* add ROLE_ASSISTANT_MANAGER to the MembershipRole enum in the Membership proto and assistant_managers_allowed to the PermissionSetting  ([c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb](https://github.com/googleapis/google-cloud-python/commit/c3c2fbbacf03dcaf015bbfb949f95d46d9e669cb))

## [0.3.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.9...google-apps-chat-v0.3.0) (2025-10-16)


### Features

* Add support for Python 3.14  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))


### Bug Fixes

* Deprecate credentials_file argument  ([98ee71abc0f97c88239b50bf0e0827df19630def](https://github.com/googleapis/google-cloud-python/commit/98ee71abc0f97c88239b50bf0e0827df19630def))

## [0.2.9](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.8...google-apps-chat-v0.2.9) (2025-08-29)


### Bug Fixes

* Changed field behavior for an existing field `last_update_time` in message `.google.chat.v1.QuotedMessageMetadata` ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))
* Changed field behavior for an existing field name in message .google.chat.v1.QuotedMessageMetadata ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))


### Documentation

* A comment for field `customer` in message `.google.chat.v1.Space` is changed ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))
* A comment for field `last_update_time` in message `.google.chat.v1.QuotedMessageMetadata` is changed ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))
* A comment for field `name` in message `.google.chat.v1.QuotedMessageMetadata` is changed ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))
* A comment for field `quoted_message_metadata` in message `.google.chat.v1.Message` is changed ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))
* A comment for field `update_mask` in message `.google.chat.v1.UpdateMessageRequest` is changed ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))
* A comment for message `QuotedMessageMetadata` is changed ([08076ef](https://github.com/googleapis/google-cloud-python/commit/08076ef884baddfe523d0be8cdfafe5637ee073b))

## [0.2.8](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.7...google-apps-chat-v0.2.8) (2025-08-06)


### Features

* Addition of app auth support for chat api ([e9795e3](https://github.com/googleapis/google-cloud-python/commit/e9795e356339141f7087a982c08fe962b3f559da))


### Documentation

* Update reference documentation for createSpace,updateSpace,deleteSpace,createMembership,updateMembership,deleteMembership and the newly added field -customer- in space.proto ([e9795e3](https://github.com/googleapis/google-cloud-python/commit/e9795e356339141f7087a982c08fe962b3f559da))

## [0.2.7](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.6...google-apps-chat-v0.2.7) (2025-07-23)


### Features

* Exposing 1p integration message content (drive, calendar, huddle, meet chips) ([b74ec0e](https://github.com/googleapis/google-cloud-python/commit/b74ec0ef9d46f96219dbdd9ff4937597a7486f28))


### Documentation

* Update reference documentation for annotations. Introduce new richlink metadata types ([b74ec0e](https://github.com/googleapis/google-cloud-python/commit/b74ec0ef9d46f96219dbdd9ff4937597a7486f28))

## [0.2.6](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.5...google-apps-chat-v0.2.6) (2025-05-08)


### Features

* A new method `customEmojis.create` is added ([1781daa](https://github.com/googleapis/google-cloud-python/commit/1781daa266a787f8e51575c121f247b1451806a9))
* A new method `customEmojis.delete` is added ([1781daa](https://github.com/googleapis/google-cloud-python/commit/1781daa266a787f8e51575c121f247b1451806a9))
* A new method `customEmojis.get` is added ([1781daa](https://github.com/googleapis/google-cloud-python/commit/1781daa266a787f8e51575c121f247b1451806a9))
* A new method `customEmojis.list` is added ([1781daa](https://github.com/googleapis/google-cloud-python/commit/1781daa266a787f8e51575c121f247b1451806a9))


### Documentation

* A comment for field `filter` in message `.google.chat.v1.ListReactionsRequest` is changed ([1781daa](https://github.com/googleapis/google-cloud-python/commit/1781daa266a787f8e51575c121f247b1451806a9))
* A comment for message `CustomEmoji` is changed ([1781daa](https://github.com/googleapis/google-cloud-python/commit/1781daa266a787f8e51575c121f247b1451806a9))

## [0.2.5](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.4...google-apps-chat-v0.2.5) (2025-03-15)


### Bug Fixes

* [Many APIs] Allow Protobuf 6.x ([a1b9294](https://github.com/googleapis/google-cloud-python/commit/a1b9294d0bf6e27c2a951d6df7faf7807dc5420b))

## [0.2.4](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.3...google-apps-chat-v0.2.4) (2025-03-09)


### Features

* Addition of space notification setting Chat API ([4c3dbf2](https://github.com/googleapis/google-cloud-python/commit/4c3dbf253f5113a5565110dd33a0749fb40c8fb2))

## [0.2.3](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.2...google-apps-chat-v0.2.3) (2025-02-24)


### Features

* [google-apps-chat] Add DeletionType.SPACE_MEMBER. This is returned when a message sent by an app is deleted by a human in a space ([#13539](https://github.com/googleapis/google-cloud-python/issues/13539)) ([8366123](https://github.com/googleapis/google-cloud-python/commit/8366123ecefb47efa33b3f7ead81dfd64225ae25))

## [0.2.2](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.1...google-apps-chat-v0.2.2) (2025-02-12)


### Features

* Add REST Interceptors which support reading metadata ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))
* Add support for reading selective GAPIC generation methods from service YAML ([a961bc0](https://github.com/googleapis/google-cloud-python/commit/a961bc029201b72fc4923490aeb3d82781853e6a))


### Documentation

* Update Google chat app command documentation ([50d43b1](https://github.com/googleapis/google-cloud-python/commit/50d43b1574812be8eb9bfffd241660ee1bddef15))

## [0.2.1](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.2.0...google-apps-chat-v0.2.1) (2025-01-29)


### Features

* A new field custom_emoji_metadata is added to message `.google.chat.v1.Annotation` ([b165f92](https://github.com/googleapis/google-cloud-python/commit/b165f923cdf47fbb23757531145eace0e3f088cb))
* A new message `CustomEmojiMetadata` is added ([b165f92](https://github.com/googleapis/google-cloud-python/commit/b165f923cdf47fbb23757531145eace0e3f088cb))
* A new value `CUSTOM_EMOJI` is added to enum `AnnotationType` ([b165f92](https://github.com/googleapis/google-cloud-python/commit/b165f923cdf47fbb23757531145eace0e3f088cb))


### Documentation

* A comment for field `custom_emoji` in message `.google.chat.v1.Emoji` is changed ([b165f92](https://github.com/googleapis/google-cloud-python/commit/b165f923cdf47fbb23757531145eace0e3f088cb))
* A comment for method `CreateReaction` in service `ChatService` is changed ([b165f92](https://github.com/googleapis/google-cloud-python/commit/b165f923cdf47fbb23757531145eace0e3f088cb))
* A comment for method `DeleteReaction` in service `ChatService` is changed ([b165f92](https://github.com/googleapis/google-cloud-python/commit/b165f923cdf47fbb23757531145eace0e3f088cb))

## [0.2.0](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.14...google-apps-chat-v0.2.0) (2024-12-12)


### ⚠ BREAKING CHANGES

* Changed field behavior for an existing field `update_mask` and `emoji`

### Features

* Add support for opt-in debug logging ([06e3ecc](https://github.com/googleapis/google-cloud-python/commit/06e3ecc2631cd5bf18873cb90c4b5026caf7d9d5))
* Chat Apps can now retrieve the import mode expire time information to know when to complete the import mode properly ([06e3ecc](https://github.com/googleapis/google-cloud-python/commit/06e3ecc2631cd5bf18873cb90c4b5026caf7d9d5))


### Bug Fixes

* Changed field behavior for an existing field `update_mask` and `emoji` ([06e3ecc](https://github.com/googleapis/google-cloud-python/commit/06e3ecc2631cd5bf18873cb90c4b5026caf7d9d5))


### Documentation

* Update reference documentation to include import_mode_expire_time field ([06e3ecc](https://github.com/googleapis/google-cloud-python/commit/06e3ecc2631cd5bf18873cb90c4b5026caf7d9d5))

## [0.1.14](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.13...google-apps-chat-v0.1.14) (2024-10-31)


### Bug Fixes

* disable universe-domain validation ([85c7512](https://github.com/googleapis/google-cloud-python/commit/85c7512bbdde2b9cc60b4ad42b8c36c4558a07a5))

## [0.1.13](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.12...google-apps-chat-v0.1.13) (2024-10-24)


### Features

* Add support for Python 3.13 ([#13199](https://github.com/googleapis/google-cloud-python/issues/13199)) ([2fc3726](https://github.com/googleapis/google-cloud-python/commit/2fc372685731141ca1ed2a917dd18bacd79db88e))

## [0.1.12](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.11...google-apps-chat-v0.1.12) (2024-10-08)


### Features

* Add doc for import mode external users support ([3881914](https://github.com/googleapis/google-cloud-python/commit/3881914b43b47bf2ee187f62447ef9eccc851749))
* Add doc for permission settings & announcement space support ([3881914](https://github.com/googleapis/google-cloud-python/commit/3881914b43b47bf2ee187f62447ef9eccc851749))


### Documentation

* Discoverable space docs improvement ([3881914](https://github.com/googleapis/google-cloud-python/commit/3881914b43b47bf2ee187f62447ef9eccc851749))
* Memberships API dev docs improvement ([3881914](https://github.com/googleapis/google-cloud-python/commit/3881914b43b47bf2ee187f62447ef9eccc851749))
* Messages API dev docs improvement ([3881914](https://github.com/googleapis/google-cloud-python/commit/3881914b43b47bf2ee187f62447ef9eccc851749))

## [0.1.11](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.10...google-apps-chat-v0.1.11) (2024-09-16)


### Features

* If you're a domain administrator or a delegated administrator, you can now include the `useAdminAccess` parameter when you call the Chat API with your administrator privileges with the following methods to manage Chat spaces and memberships in your Workspace organization: ([a20b1e5](https://github.com/googleapis/google-cloud-python/commit/a20b1e508068845c36b1701836ba17a699cb10ac))


### Documentation

* A comment for field `filter` in message `.google.chat.v1.ListMembershipsRequest` is updated to support `!=` operator ([a20b1e5](https://github.com/googleapis/google-cloud-python/commit/a20b1e508068845c36b1701836ba17a699cb10ac))

## [0.1.10](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.9...google-apps-chat-v0.1.10) (2024-09-05)


### Features

* [google-apps-chat] Add CHAT_SPACE link type support for GA launch ([#13064](https://github.com/googleapis/google-cloud-python/issues/13064)) ([0ee300a](https://github.com/googleapis/google-cloud-python/commit/0ee300a0497968aa2c85969924b37f95f67675f0))

## [0.1.9](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.8...google-apps-chat-v0.1.9) (2024-07-30)


### Features

* [google-apps-chat] add GetSpaceEvent and ListSpaceEvents APIs ([#12904](https://github.com/googleapis/google-cloud-python/issues/12904)) ([c6f70a6](https://github.com/googleapis/google-cloud-python/commit/c6f70a609e2f94161fb8ead8fcbfb49b3734d4d4))


### Bug Fixes

* Retry and timeout values do not propagate in requests during pagination ([c6eeae0](https://github.com/googleapis/google-cloud-python/commit/c6eeae00de802d98badd3de879ce5e870ba60a3a))

## [0.1.8](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.7...google-apps-chat-v0.1.8) (2024-07-08)


### Features

* Add doc for Discoverable Space support for GA launch ([09391b2](https://github.com/googleapis/google-cloud-python/commit/09391b22528550c29f33901d6b327fae8a4c058c))


### Bug Fixes

* Allow Protobuf 5.x ([#12863](https://github.com/googleapis/google-cloud-python/issues/12863)) ([3e6e423](https://github.com/googleapis/google-cloud-python/commit/3e6e423b86cdace8538f610941aa84c7a6217934))


### Documentation

* Update resource naming formats ([09391b2](https://github.com/googleapis/google-cloud-python/commit/09391b22528550c29f33901d6b327fae8a4c058c))

## [0.1.7](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.6...google-apps-chat-v0.1.7) (2024-06-27)


### Documentation

* Update doc for `CreateMembership` in service `ChatService` to support group members ([5c8eaae](https://github.com/googleapis/google-cloud-python/commit/5c8eaae2289427f56c730bbf3e7e78b15a35580a))
* Update doc for field `group_member` in message `google.chat.v1.Membership` ([5c8eaae](https://github.com/googleapis/google-cloud-python/commit/5c8eaae2289427f56c730bbf3e7e78b15a35580a))
* Update doc for SetUpSpace in service ChatService to support group members ([5c8eaae](https://github.com/googleapis/google-cloud-python/commit/5c8eaae2289427f56c730bbf3e7e78b15a35580a))

## [0.1.6](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.5...google-apps-chat-v0.1.6) (2024-05-16)


### Documentation

* [google-apps-chat] update Chat API comments ([#12694](https://github.com/googleapis/google-cloud-python/issues/12694)) ([f66440d](https://github.com/googleapis/google-cloud-python/commit/f66440dec8cab0a11e53dd9e3e165b85f9651f38))

## [0.1.5](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.4...google-apps-chat-v0.1.5) (2024-04-22)


### Features

* [google-apps-chat] Add Chat read state APIs ([#12597](https://github.com/googleapis/google-cloud-python/issues/12597)) ([741695a](https://github.com/googleapis/google-cloud-python/commit/741695ae4df223c4f6794adbc7ed437da2cdbedd))

## [0.1.4](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.3...google-apps-chat-v0.1.4) (2024-04-18)


### Features

* [google-apps-chat] add UpdateMembership API ([#12589](https://github.com/googleapis/google-cloud-python/issues/12589)) ([187a036](https://github.com/googleapis/google-cloud-python/commit/187a03605cd5d5d314c47a44dbf5227fb0af204a))

## [0.1.3](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.2...google-apps-chat-v0.1.3) (2024-04-16)


### Bug Fixes

* **deps:** Require google-apps-card &gt;= 0.1.2 ([66162a7](https://github.com/googleapis/google-cloud-python/commit/66162a79254774329b38ff81e82193fda2eefe02))


### Documentation

* Chat API documentation update ([66162a7](https://github.com/googleapis/google-cloud-python/commit/66162a79254774329b38ff81e82193fda2eefe02))

## [0.1.2](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.1...google-apps-chat-v0.1.2) (2024-03-27)


### Features

* [google-apps-chat] Launch AccessoryAction for GA ([#12517](https://github.com/googleapis/google-cloud-python/issues/12517)) ([a2113a8](https://github.com/googleapis/google-cloud-python/commit/a2113a80f398dcc94b55827330ec7ebbadc6fbf8))

## [0.1.1](https://github.com/googleapis/google-cloud-python/compare/google-apps-chat-v0.1.0...google-apps-chat-v0.1.1) (2024-03-22)


### Features

* add rich link annotation type ([a33e4b0](https://github.com/googleapis/google-cloud-python/commit/a33e4b00af086b31833c212c6fb92ab0d70d68f3))

## 0.1.0 (2024-03-05)


### Features

* add initial files for google.apps.chat.v1 ([#12379](https://github.com/googleapis/google-cloud-python/issues/12379)) ([cd56a46](https://github.com/googleapis/google-cloud-python/commit/cd56a4683d04eff015e23ee5fc9a319cfc1f3405))

## Changelog
