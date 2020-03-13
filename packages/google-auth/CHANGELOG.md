# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-auth/#history

### [1.11.3](https://www.github.com/googleapis/google-auth-library-python/compare/v1.11.2...v1.11.3) (2020-03-13)


### Bug Fixes

* fix the scopes so test can pass for a local run ([#450](https://www.github.com/googleapis/google-auth-library-python/issues/450)) ([b2dd77f](https://www.github.com/googleapis/google-auth-library-python/commit/b2dd77fe4a538e1d165fc9d859c9a299f6832cda))
* only add IAM scope to credentials that can change scopes ([#451](https://www.github.com/googleapis/google-auth-library-python/issues/451)) ([82e224b](https://www.github.com/googleapis/google-auth-library-python/commit/82e224b0854950a5607cd028edbcbcdc3e9e6505))

### [1.11.2](https://www.github.com/googleapis/google-auth-library-python/compare/v1.11.1...v1.11.2) (2020-02-14)


### Reverts

* Revert "fix: update `_GOOGLE_OAUTH2_CERTS_URL` (#365)" (#444) ([901c259](https://www.github.com/googleapis/google-auth-library-python/commit/901c259b1764f5a305a542cbae14d926ba7a57db)), closes [#365](https://www.github.com/googleapis/google-auth-library-python/issues/365) [#444](https://www.github.com/googleapis/google-auth-library-python/issues/444)

### [1.11.1](https://www.github.com/googleapis/google-auth-library-python/compare/v1.11.0...v1.11.1) (2020-02-13)


### Bug Fixes

* compute engine id token credentials "with_target_audience" method ([#438](https://www.github.com/googleapis/google-auth-library-python/issues/438)) ([bc0ec93](https://www.github.com/googleapis/google-auth-library-python/commit/bc0ec93dc66fdcaa6a82222386623fa44f24ddfe))
* update `_GOOGLE_OAUTH2_CERTS_URL` ([#365](https://www.github.com/googleapis/google-auth-library-python/issues/365)) ([054db75](https://www.github.com/googleapis/google-auth-library-python/commit/054db75734756b0e82e7984ca07fa80025edc908))

## [1.11.0](https://www.github.com/googleapis/google-auth-library-python/compare/v1.10.2...v1.11.0) (2020-01-23)


### Features

* add non-None default timeout to AuthorizedSession.request() ([#435](https://www.github.com/googleapis/google-auth-library-python/issues/435)) ([d274a3a](https://www.github.com/googleapis/google-auth-library-python/commit/d274a3a2b3f913bc2cab4ca51f9c7fdef94b8f31)), closes [#434](https://www.github.com/googleapis/google-auth-library-python/issues/434) [googleapis/google-cloud-python#10182](https://www.github.com/googleapis/google-cloud-python/issues/10182)
* distinguish transport and execution time timeouts ([#424](https://www.github.com/googleapis/google-auth-library-python/issues/424)) ([52a733d](https://www.github.com/googleapis/google-auth-library-python/commit/52a733d604528fa86d05321bb74241a43aea4211)), closes [#423](https://github.com/googleapis/google-auth-library-python/issues/423)

### [1.10.2](https://www.github.com/googleapis/google-auth-library-python/compare/v1.10.1...v1.10.2) (2020-01-18)


### Bug Fixes

* make collections import compatible across Python versions ([#419](https://www.github.com/googleapis/google-auth-library-python/issues/419)) ([c5a3395](https://www.github.com/googleapis/google-auth-library-python/commit/c5a3395b8781e14c4566cf0e476b234d6a1c1224)), closes [#418](https://www.github.com/googleapis/google-auth-library-python/issues/418)

### [1.10.1](https://www.github.com/googleapis/google-auth-library-python/compare/v1.10.0...v1.10.1) (2020-01-10)


### Bug Fixes

* **google.auth.compute_engine.metadata:** add retry to google.auth.compute_engine._metadata.get() ([#398](https://www.github.com/googleapis/google-auth-library-python/issues/398)) ([af29c1a](https://www.github.com/googleapis/google-auth-library-python/commit/af29c1a9fd9282b38867961e4053f74f018a3815)), closes [#211](https://www.github.com/googleapis/google-auth-library-python/issues/211) [#323](https://www.github.com/googleapis/google-auth-library-python/issues/323) [#323](https://www.github.com/googleapis/google-auth-library-python/issues/323) [#211](https://www.github.com/googleapis/google-auth-library-python/issues/211)
* always pass body of type bytes to `google.auth.transport.Request` ([#421](https://www.github.com/googleapis/google-auth-library-python/issues/421)) ([a57a770](https://www.github.com/googleapis/google-auth-library-python/commit/a57a7708cfea635b5030f8c7ba10c967715f9a87)), closes [#318](https://www.github.com/googleapis/google-auth-library-python/issues/318)

## [1.10.0](https://www.github.com/googleapis/google-auth-library-python/compare/v1.9.0...v1.10.0) (2019-12-18)


### Features

* send quota project id in x-goog-user-project for OAuth2 credentials ([#412](https://www.github.com/googleapis/google-auth-library-python/issues/412)) ([32d71a5](https://www.github.com/googleapis/google-auth-library-python/commit/32d71a5858435af0818a705b754404882bb7bb9e)), closes [#400](https://www.github.com/googleapis/google-auth-library-python/issues/400)

## [1.9.0](https://www.github.com/googleapis/google-auth-library-python/compare/v1.8.2...v1.9.0) (2019-12-12)


### Features

* add timeout parameter to `AuthorizedSession.request()` ([#406](https://www.github.com/googleapis/google-auth-library-python/issues/406)) ([d86d7b8](https://www.github.com/googleapis/google-auth-library-python/commit/d86d7b8c43df152765c7fc59a54015361b46dcde))

### [1.8.2](https://www.github.com/googleapis/google-auth-library-python/compare/v1.8.1...v1.8.2) (2019-12-11)


### Bug Fixes

* revert "feat: send quota project id in x-goog-user-project header for OAuth2 credentials ([#400](https://www.github.com/googleapis/google-auth-library-python/issues/400))" ([#407](https://www.github.com/googleapis/google-auth-library-python/issues/407)) ([25ea942](https://www.github.com/googleapis/google-auth-library-python/commit/25ea942cef4378ff22adf235dd1baf1ca0d595f8))

### [1.8.1](https://www.github.com/googleapis/google-auth-library-python/compare/v1.8.0...v1.8.1) (2019-12-09)


### Bug Fixes

* revert "feat: add timeout to AuthorizedSession.request() ([#397](https://www.github.com/googleapis/google-auth-library-python/issues/397))" ([#401](https://www.github.com/googleapis/google-auth-library-python/issues/401)) ([451ecbd](https://www.github.com/googleapis/google-auth-library-python/commit/451ecbd48a910348bbf7a7b38162a044fad6e6e1))

## [1.8.0](https://www.github.com/googleapis/google-auth-library-python/compare/v1.7.2...v1.8.0) (2019-12-09)


### Features

* add `to_json` method to google.oauth2.credentials.Credentials ([#367](https://www.github.com/googleapis/google-auth-library-python/issues/367)) ([bfb1f8c](https://www.github.com/googleapis/google-auth-library-python/commit/bfb1f8cc8a706ce5ca2a14886c920ca2220ec349))
* add timeout to AuthorizedSession.request() ([#397](https://www.github.com/googleapis/google-auth-library-python/issues/397)) ([381dd40](https://www.github.com/googleapis/google-auth-library-python/commit/381dd400911d29926ffbf04e0f2ba53ef7bb997e))
* send quota project id in x-goog-user-project header for OAuth2 credentials ([#400](https://www.github.com/googleapis/google-auth-library-python/issues/400)) ([ab3dc1e](https://www.github.com/googleapis/google-auth-library-python/commit/ab3dc1e26f5240ea3456de364c7c5cb8f40f9583))

### [1.7.2](https://www.github.com/googleapis/google-auth-library-python/compare/v1.7.1...v1.7.2) (2019-12-02)


### Bug Fixes

* in token endpoint request, do not decode the response data if it is not encoded ([#393](https://www.github.com/googleapis/google-auth-library-python/issues/393)) ([3b5d3e2](https://www.github.com/googleapis/google-auth-library-python/commit/3b5d3e2192ce0cdc97854a1d70d5e382e454275c))
* make gRPC auth plugin non-blocking + add default timeout value for requests transport ([#390](https://www.github.com/googleapis/google-auth-library-python/issues/390)) ([0c33e9c](https://www.github.com/googleapis/google-auth-library-python/commit/0c33e9c0fe4f87fa46c8f1a5afe725a467ac5fcc)), closes [#351](https://www.github.com/googleapis/google-auth-library-python/issues/351)

### [1.7.1](https://www.github.com/googleapis/google-auth-library-python/compare/v1.7.0...v1.7.1) (2019-11-13)


### Bug Fixes

* change 'internal_failure' condition to also use `error' field ([#387](https://www.github.com/googleapis/google-auth-library-python/issues/387)) ([46bb58e](https://www.github.com/googleapis/google-auth-library-python/commit/46bb58e694716908a5ed00f05dbb794cdec667dd))

## 1.7.0

10-30-2019 17:11 PDT


### Implementation Changes
- Add retry loop  for fetching authentication token if any 'Internal Failure' occurs ([#368](https://github.com/googleapis/google-auth-library-python/pull/368))
- Use cls parameter instead of class ([#341](https://github.com/googleapis/google-auth-library-python/pull/341))

### New Features
- Add support for `impersonated_credentials.Sign`, `IDToken` ([#348](https://github.com/googleapis/google-auth-library-python/pull/348))
- Add downscoping to OAuth2 credentials ([#309](https://github.com/googleapis/google-auth-library-python/pull/309))

### Dependencies
- Update dependency cachetools to v3 ([#357](https://github.com/googleapis/google-auth-library-python/pull/357))
- Update dependency rsa to v4 ([#358](https://github.com/googleapis/google-auth-library-python/pull/358))
- Set an upper bound on dependencies version ([#352](https://github.com/googleapis/google-auth-library-python/pull/352))
- Require a minimum version of setuptools ([#322](https://github.com/googleapis/google-auth-library-python/pull/322))

### Documentation
- Add busunkim96 as maintainer ([#373](https://github.com/googleapis/google-auth-library-python/pull/373))
- Update user-guide.rst ([#337](https://github.com/googleapis/google-auth-library-python/pull/337))
- Fix typo in jwt docs ([#332](https://github.com/googleapis/google-auth-library-python/pull/332))
- Clarify which SA has Token Creator role ([#330](https://github.com/googleapis/google-auth-library-python/pull/330))

### Internal / Testing Changes
- Change 'name' to distribution name ([#379](https://github.com/googleapis/google-auth-library-python/pull/379))
- Fix system tests, move to Kokoro ([#372](https://github.com/googleapis/google-auth-library-python/pull/372))
- Blacken ([#375](https://github.com/googleapis/google-auth-library-python/pull/375))
- Rename nox.py -> noxfile.py ([#369](https://github.com/googleapis/google-auth-library-python/pull/369))
- Add initial renovate config ([#356](https://github.com/googleapis/google-auth-library-python/pull/356))
- Use new pytest api to keep building with pytest 5 ([#353](https://github.com/googleapis/google-auth-library-python/pull/353))


## 1.6.3

02-15-2019 9:31 PST

### Implementation Changes

- follow rfc 7515 : strip padding from JWS segments  ([#324](https://github.com/googleapis/google-auth-library-python/pull/324))
- Add retry to `_metadata.ping()` ([#323](https://github.com/googleapis/google-auth-library-python/pull/323))

## 1.6.2

12-17-2018 10:51 PST

### Documentation

- Announce deprecation of Python 2.7 ([#311](https://github.com/googleapis/google-auth-library-python/pull/311))
- Link all the PRs in CHANGELOG ([#307](https://github.com/googleapis/google-auth-library-python/pull/307))

## 1.6.1

11-12-2018 10:10 PST

### Implementation Changes

- Automatically refresh impersonated credentials ([#304](https://github.com/googleapis/google-auth-library-python/pull/304))

## 1.6.0

11-09-2018 11:07 PST

### New Features

- Add `google.auth.impersonated_credentials` ([#299](https://github.com/googleapis/google-auth-library-python/pull/299))

### Documentation

- Update link to documentation for default credentials ([#296](https://github.com/googleapis/google-auth-library-python/pull/296))
- Update github issue templates ([#300](https://github.com/googleapis/google-auth-library-python/pull/300))
- Remove punctuation which becomes part of the url ([#284](https://github.com/googleapis/google-auth-library-python/pull/284))

### Internal / Testing Changes

- Update trampoline.sh ([302](https://github.com/googleapis/google-auth-library-python/pull/302))
- Enable static type checking with pytype ([#298](https://github.com/googleapis/google-auth-library-python/pull/298))
- Make classifiers in setup.py an array. ([#280](https://github.com/googleapis/google-auth-library-python/pull/280))


## 1.5.1

- Fix check for error text on Python 3.7. ([#278](https://github.com/googleapis/google-auth-library-python/pull/#278))
- Use new Auth URIs. ([#281](https://github.com/googleapis/google-auth-library-python/pull/#281))
- Add code-of-conduct document. ([#270](https://github.com/googleapis/google-auth-library-python/pull/#270))
- Fix some typos in test_urllib3.py ([#268](https://github.com/googleapis/google-auth-library-python/pull/#268))

## 1.5.0

- Warn when using user credentials from the Cloud SDK ([#266](https://github.com/googleapis/google-auth-library-python/pull/266))
- Add compute engine-based IDTokenCredentials ([#236](https://github.com/googleapis/google-auth-library-python/pull/236))
- Corrected some typos ([#265](https://github.com/googleapis/google-auth-library-python/pull/265))

## 1.4.2

- Raise a helpful exception when trying to refresh credentials without a refresh token. ([#262](https://github.com/googleapis/google-auth-library-python/pull/262))
- Fix links to README and CONTRIBUTING in docs/index.rst. ([#260](https://github.com/googleapis/google-auth-library-python/pull/260))
- Fix a typo in credentials.py. ([#256](https://github.com/googleapis/google-auth-library-python/pull/256))
- Use pytest instead of py.test per upstream recommendation, #dropthedot. ([#255](https://github.com/googleapis/google-auth-library-python/pull/255))
- Fix typo on exemple of jwt usage ([#245](https://github.com/googleapis/google-auth-library-python/pull/245))

## 1.4.1

- Added a check for the cryptography version before attempting to use it. ([#243](https://github.com/googleapis/google-auth-library-python/pull/243))

## 1.4.0

- Added `cryptography`-based RSA signer and verifier. ([#185](https://github.com/googleapis/google-auth-library-python/pull/185))
- Added `google.oauth2.service_account.IDTokenCredentials`. ([#234](https://github.com/googleapis/google-auth-library-python/pull/234))
- Improved documentation around ID Tokens ([#224](https://github.com/googleapis/google-auth-library-python/pull/224))

## 1.3.0

- Added ``google.oauth2.credentials.Credentials.from_authorized_user_file`` ([#226](https://github.com/googleapis/google-auth-library-python/pull/#226))
- Dropped direct pyasn1 dependency in favor of letting ``pyasn1-modules`` specify the right version. ([#230](https://github.com/googleapis/google-auth-library-python/pull/#230))
- ``default()`` now checks for the project ID environment var before warning about missing project ID. ([#227](https://github.com/googleapis/google-auth-library-python/pull/#227))
- Fixed the docstrings for ``has_scopes()`` and ``with_scopes()``. ([#228](https://github.com/googleapis/google-auth-library-python/pull/#228))
- Fixed example in docstring for ``ReadOnlyScoped``. ([#219](https://github.com/googleapis/google-auth-library-python/pull/#219))
- Made ``transport.requests`` use timeouts and retries to improve reliability. ([#220](https://github.com/googleapis/google-auth-library-python/pull/#220))

## 1.2.1

- Excluded compiled Python files in source distributions. ([#215](https://github.com/googleapis/google-auth-library-python/pull/#215))
- Updated docs for creating RSASigner from string. ([#213](https://github.com/googleapis/google-auth-library-python/pull/#213))
- Use ``six.raise_from`` wherever possible. ([#212](https://github.com/googleapis/google-auth-library-python/pull/#212))
- Fixed a typo in a comment ``seconds`` not ``sections``. ([#210](https://github.com/googleapis/google-auth-library-python/pull/#210))

## 1.2.0

- Added ``google.auth.credentials.AnonymousCredentials``. ([#206](https://github.com/googleapis/google-auth-library-python/pull/#206))
- Updated the documentation to link to the Google Cloud Platform Python setup guide ([#204](https://github.com/googleapis/google-auth-library-python/pull/#204))

## 1.1.1

- ``google.oauth.credentials.Credentials`` now correctly inherits from ``ReadOnlyScoped`` instead of ``Scoped``. ([#200](https://github.com/googleapis/google-auth-library-python/pull/#200))

## 1.1.0

- Added ``service_account.Credentials.project_id``. ([#187](https://github.com/googleapis/google-auth-library-python/pull/#187))
- Move read-only methods of ``credentials.Scoped`` into new interface ``credentials.ReadOnlyScoped``. ([#195](https://github.com/googleapis/google-auth-library-python/pull/#195), [#196](https://github.com/googleapis/google-auth-library-python/pull/#196))
- Make ``compute_engine.Credentials`` derive from ``ReadOnlyScoped`` instead of ``Scoped``. ([#195](https://github.com/googleapis/google-auth-library-python/pull/#195))
- Fix App Engine's expiration calculation ([#197](https://github.com/googleapis/google-auth-library-python/pull/#197))
- Split ``crypt`` module into a package to allow alternative implementations. ([#189](https://github.com/googleapis/google-auth-library-python/pull/#189))
- Add error message to handle case of empty string or missing file for `GOOGLE_APPLICATION_CREDENTIALS` ([#188](https://github.com/googleapis/google-auth-library-python/pull/#188))

## 1.0.2

- Fixed a bug where the Cloud SDK executable could not be found on Windows, leading to project ID detection failing. ([#179](https://github.com/googleapis/google-auth-library-python/pull/#179))
- Fixed a bug where the timeout argument wasn't being passed through the httplib transport correctly. ([#175](https://github.com/googleapis/google-auth-library-python/pull/#175))
- Added documentation for using the library on Google App Engine standard. ([#172](https://github.com/googleapis/google-auth-library-python/pull/#172))
- Testing style updates. ([#168](https://github.com/googleapis/google-auth-library-python/pull/#168))
- Added documentation around the oauth2client deprecation. ([#165](https://github.com/googleapis/google-auth-library-python/pull/#165))
- Fixed a few lint issues caught by newer versions of pylint. ([#166](https://github.com/googleapis/google-auth-library-python/pull/#166))

## 1.0.1

- Fixed a bug in the clock skew accommodation logic where expired credentials could be used for up to 5 minutes. ([#158](https://github.com/googleapis/google-auth-library-python/pull/158))

## 1.0.0

Milestone release for v1.0.0.
No significant changes since v0.10.0

## 0.10.0

- Added ``jwt.OnDemandCredentials``. ([#142](https://github.com/googleapis/google-auth-library-python/pull/142))
- Added new public property ``id_token`` to ``oauth2.credentials.Credentials``. ([#150](https://github.com/googleapis/google-auth-library-python/pull/150))
- Added the ability to set the address used to communicate with the Compute Engine metadata server via the ``GCE_METADATA_ROOT`` and ``GCE_METADATA_IP`` environment variables. ([#148](https://github.com/googleapis/google-auth-library-python/pull/148))
- Changed the way cloud project IDs are ascertained from the Google Cloud SDK. ([#147](https://github.com/googleapis/google-auth-library-python/pull/147))
- Modified expiration logic to add a 5 minute clock skew accommodation. ([#145](https://github.com/googleapis/google-auth-library-python/pull/145))

## 0.9.0

- Added ``service_account.Credentials.with_claims``. ([#140](https://github.com/googleapis/google-auth-library-python/pull/140))
- Moved ``google.auth.oauthlib`` and ``google.auth.flow`` to a new separate package ``google_auth_oauthlib``. ([#137](https://github.com/googleapis/google-auth-library-python/pull/137), [#139](https://github.com/googleapis/google-auth-library-python/pull/139), [#135](https://github.com/googleapis/google-auth-library-python/pull/135), [#126](https://github.com/googleapis/google-auth-library-python/pull/126))
- Added ``InstalledAppFlow`` to ``google_auth_oauthlib``. ([#128](https://github.com/googleapis/google-auth-library-python/pull/128))
- Fixed some packaging and documentation issues. ([#131](https://github.com/googleapis/google-auth-library-python/pull/131))
- Added a helpful error message when importing optional dependencies. ([#125](https://github.com/googleapis/google-auth-library-python/pull/125))
- Made all properties required to reconstruct ``google.oauth2.credentials.Credentials`` public. ([#124](https://github.com/googleapis/google-auth-library-python/pull/124))
- Added official Python 3.6 support. ([#102](https://github.com/googleapis/google-auth-library-python/pull/102))
- Added ``jwt.Credentials.from_signing_credentials`` and removed ``service_account.Credentials.to_jwt_credentials``. ([#120](https://github.com/googleapis/google-auth-library-python/pull/120))

## 0.8.0

- Removed one-time token behavior from ``jwt.Credentials``, audience claim is now required and fixed. ([#117](https://github.com/googleapis/google-auth-library-python/pull/117))
- ``crypt.Signer`` and ``crypt.Verifier`` are now abstract base classes. The concrete implementations have been renamed to ``crypt.RSASigner`` and ``crypt.RSAVerifier``. ``app_engine.Signer`` and ``iam.Signer`` now inherit from ``crypt.Signer``. ([#115](https://github.com/googleapis/google-auth-library-python/pull/115))
- ``transport.grpc`` now correctly calls ``Credentials.before_request``. ([#116](https://github.com/googleapis/google-auth-library-python/pull/116))

## 0.7.0

- Added ``google.auth.iam.Signer``. ([#108](https://github.com/googleapis/google-auth-library-python/pull/108))
- Fixed issue where ``google.auth.app_engine.Signer`` erroneously returns a tuple from ``sign()``. ([#109](https://github.com/googleapis/google-auth-library-python/pull/109))
- Added public property ``google.auth.credentials.Signing.signer``. ([#110](https://github.com/googleapis/google-auth-library-python/pull/110))

## 0.6.0

- Added experimental integration with ``requests-oauthlib`` in ``google.oauth2.oauthlib`` and ``google.oauth2.flow``. ([#100](https://github.com/googleapis/google-auth-library-python/pull/100), [#105](https://github.com/googleapis/google-auth-library-python/pull/105), [#106](https://github.com/googleapis/google-auth-library-python/pull/106))
- Fixed typo in ``google_auth_httplib2``'s README. ([#105](https://github.com/googleapis/google-auth-library-python/pull/105))

## 0.5.0

- Added ``app_engine.Signer``. ([#97](https://github.com/googleapis/google-auth-library-python/pull/97))
- Added ``crypt.Signer.from_service_account_file``. ([#95](https://github.com/googleapis/google-auth-library-python/pull/95))
- Fixed error handling in the oauth2 client. ([#96](https://github.com/googleapis/google-auth-library-python/pull/96))
- Fixed the App Engine system tests.

## 0.4.0

- ``transports.grpc.secure_authorized_channel`` now passes ``kwargs`` to ``grpc.secure_channel``. ([#90](https://github.com/googleapis/google-auth-library-python/pull/90))
- Added new property ``credentials.Singing.signer_email`` which can be used to identify the signer of a message. ([#89](https://github.com/googleapis/google-auth-library-python/pull/89))
- (google_auth_httplib2) Added a proxy to ``httplib2.Http.connections``.

## 0.3.2

- Fixed an issue where an ``ImportError`` would occur if ``google.oauth2`` was imported before ``google.auth``. ([#88](https://github.com/googleapis/google-auth-library-python/pull/88))

## 0.3.1

- Fixed a bug where non-padded base64 encoded strings were not accepted. ([#87](https://github.com/googleapis/google-auth-library-python/pull/87))
- Fixed a bug where ID token verification did not correctly call the HTTP request function. ([#87](https://github.com/googleapis/google-auth-library-python/pull/87))

## 0.3.0

- Added Google ID token verification helpers. ([#82](https://github.com/googleapis/google-auth-library-python/pull/82))
- Swapped the ``target`` and ``request`` argument order for ``grpc.secure_authorized_channel``. ([#81](https://github.com/googleapis/google-auth-library-python/pull/81))
- Added a user's guide. ([#79](https://github.com/googleapis/google-auth-library-python/pull/79))
- Made ``service_account_email`` a public property on several credential classes. ([#76](https://github.com/googleapis/google-auth-library-python/pull/76))
- Added a ``scope`` argument to ``google.auth.default``. ([#75](https://github.com/googleapis/google-auth-library-python/pull/75))
- Added support for the ``GCLOUD_PROJECT`` environment variable. ([#73](https://github.com/googleapis/google-auth-library-python/pull/73))

## 0.2.0

- Added gRPC support. ([#67](https://github.com/googleapis/google-auth-library-python/pull/67))
- Added Requests support. ([#66](https://github.com/googleapis/google-auth-library-python/pull/66))
- Added ``google.auth.credentials.with_scopes_if_required`` helper. ([#65](https://github.com/googleapis/google-auth-library-python/pull/65))
- Added private helper for oauth2client migration. ([#70](https://github.com/googleapis/google-auth-library-python/pull/70))

## 0.1.0

First release with core functionality available. This version is ready for
initial usage and testing.

- Added ``google.auth.credentials``, public interfaces for Credential types. ([#8](https://github.com/googleapis/google-auth-library-python/pull/8))
- Added ``google.oauth2.credentials``, credentials that use OAuth 2.0 access and refresh tokens ([#24](https://github.com/googleapis/google-auth-library-python/pull/24))
- Added ``google.oauth2.service_account``, credentials that use Service Account private keys to obtain OAuth 2.0 access tokens. ([#25](https://github.com/googleapis/google-auth-library-python/pull/25))
- Added ``google.auth.compute_engine``, credentials that use the Compute Engine metadata service to obtain OAuth 2.0 access tokens. ([#22](https://github.com/googleapis/google-auth-library-python/pull/22))
- Added ``google.auth.jwt.Credentials``, credentials that use a JWT as a bearer token.
- Added ``google.auth.app_engine``, credentials that use the Google App Engine App Identity service to obtain OAuth 2.0 access tokens. ([#46](https://github.com/googleapis/google-auth-library-python/pull/46))
- Added ``google.auth.default()``, an implementation of Google Application Default Credentials that supports automatic Project ID detection. ([#32](https://github.com/googleapis/google-auth-library-python/pull/32))
- Added system tests for all credential types. ([#51](https://github.com/googleapis/google-auth-library-python/pull/51), [#54](https://github.com/googleapis/google-auth-library-python/pull/54), [#56](https://github.com/googleapis/google-auth-library-python/pull/56), [#58](https://github.com/googleapis/google-auth-library-python/pull/58), [#59](https://github.com/googleapis/google-auth-library-python/pull/59), [#60](https://github.com/googleapis/google-auth-library-python/pull/60), [#61](https://github.com/googleapis/google-auth-library-python/pull/61), [#62](https://github.com/googleapis/google-auth-library-python/pull/62))
- Added ``google.auth.transports.urllib3.AuthorizedHttp``, an HTTP client that includes authentication provided by credentials. ([#19](https://github.com/googleapis/google-auth-library-python/pull/19))
- Documentation style and formatting updates.

## 0.0.1

Initial release with foundational functionality for cryptography and JWTs.

- ``google.auth.crypt`` for creating and verifying cryptographic signatures.
- ``google.auth.jwt`` for creating (encoding) and verifying (decoding) JSON Web tokens.
