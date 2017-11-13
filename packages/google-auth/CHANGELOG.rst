Changelog
=========

v1.2.1
------

- Excluded compiled Python files in source distributions. (#215)
- Updated docs for creating RSASigner from string. (#213)
- Use ``six.raise_from`` wherever possible. (#212)
- Fixed a typo in a comment ``seconds`` not ``sections``. (#210)

v1.2.0
------

- Added ``google.auth.credentials.AnonymousCredentials``. (#206)
- Updated the documentation to link to the Google Cloud Platform Python setup guide (#204)

v1.1.1
------

- ``google.oauth.credentials.Credentials`` now correctly inherits from ``ReadOnlyScoped`` instead of ``Scoped``. (#200)

v1.1.0
------

- Added ``service_account.Credentials.project_id``. (#187)
- Move read-only methods of ``credentials.Scoped`` into new interface ``credentials.ReadOnlyScoped``. (#195, #196)
- Make ``compute_engine.Credentials`` derive from ``ReadOnlyScoped`` instead of ``Scoped``. (#195)
- Fix App Engine's expiration calculation (#197)
- Split ``crypt`` module into a package to allow alternative implementations. (#189)
- Add error message to handle case of empty string or missing file for GOOGLE_APPLICATION_CREDENTIALS (#188)

v1.0.2
------

- Fixed a bug where the Cloud SDK executable could not be found on Windows, leading to project ID detection failing. (#179)
- Fixed a bug where the timeout argument wasn't being passed through the httplib transport correctly. (#175)
- Added documentation for using the library on Google App Engine standard. (#172)
- Testing style updates. (#168)
- Added documentation around the oauth2client deprecation. (#165)
- Fixed a few lint issues caught by newer versions of pylint. (#166)

v1.0.1
------

- Fixed a bug in the clock skew accommodation logic where expired credentials could be used for up to 5 minutes. (#158)

v1.0.0
------

Milestone release for v1.0.0.
No significant changes since v0.10.0

v0.10.0
-------

- Added ``jwt.OnDemandCredentials``. (#142)
- Added new public property ``id_token`` to ``oauth2.credentials.Credentials``. (#150)
- Added the ability to set the address used to communicate with the Compute Engine metadata server via the ``GCE_METADATA_ROOT`` and ``GCE_METADATA_IP`` environment variables. (#148)
- Changed the way cloud project IDs are ascertained from the Google Cloud SDK. (#147)
- Modified expiration logic to add a 5 minute clock skew accommodation. (#145)

v0.9.0
------

- Added ``service_account.Credentials.with_claims``. (#140)
- Moved ``google.auth.oauthlib`` and ``google.auth.flow`` to a new separate package ``google_auth_oauthlib``. (#137, #139, #135, #126)
- Added ``InstalledAppFlow`` to ``google_auth_oauthlib``. (#128)
- Fixed some packaging and documentation issues. (#131)
- Added a helpful error message when importing optional dependencies. (#125)
- Made all properties required to reconstruct ``google.oauth2.credentials.Credentials`` public. (#124)
- Added official Python 3.6 support. (#102)
- Added ``jwt.Credentials.from_signing_credentials`` and removed ``service_account.Credentials.to_jwt_credentials``. (#120)

v0.8.0
------

- Removed one-time token behavior from ``jwt.Credentials``, audience claim is now required and fixed. (#117)
- ``crypt.Signer`` and ``crypt.Verifier`` are now abstract base classes. The concrete implementations have been renamed to ``crypt.RSASigner`` and ``crypt.RSAVerifier``. ``app_engine.Signer`` and ``iam.Signer`` now inherit from ``crypt.Signer``. (#115)
- ``transport.grpc`` now correctly calls ``Credentials.before_request``. (#116)

v0.7.0
------

- Added ``google.auth.iam.Signer``. (#108)
- Fixed issue where ``google.auth.app_engine.Signer`` erroneously returns a tuple from ``sign()``. (#109)
- Added public property ``google.auth.credentials.Signing.signer``. (#110)

v0.6.0
------

- Added experimental integration with ``requests-oauthlib`` in ``google.oauth2.oauthlib`` and ``google.oauth2.flow``. (#100, #105, #106)
- Fixed typo in ``google_auth_httplib2``'s README. (#105)

v0.5.0
------

- Added ``app_engine.Signer``. (#97)
- Added ``crypt.Signer.from_service_account_file``. (#95)
- Fixed error handling in the oauth2 client. (#96)
- Fixed the App Engine system tests.

v0.4.0
------

- ``transports.grpc.secure_authorized_channel`` now passes ``kwargs`` to ``grpc.secure_channel``. (#90)
- Added new property ``credentials.Singing.signer_email`` which can be used to identify the signer of a message. (#89)
- (google_auth_httplib2) Added a proxy to ``httplib2.Http.connections``.

v0.3.2
------

- Fixed an issue where an ``ImportError`` would occur if ``google.oauth2`` was imported before ``google.auth``. (#88)

v0.3.1
------

- Fixed a bug where non-padded base64 encoded strings were not accepted. (#87)
- Fixed a bug where ID token verification did not correctly call the HTTP request function. (#87)

v0.3.0
------

- Added Google ID token verification helpers. (#82)
- Swapped the ``target`` and ``request`` argument order for ``grpc.secure_authorized_channel``. (#81)
- Added a user's guide. (#79)
- Made ``service_account_email`` a public property on several credential classes. (#76)
- Added a ``scope`` argument to ``google.auth.default``. (#75)
- Added support for the ``GCLOUD_PROJECT`` environment variable. (#73)

v0.2.0
------

- Added gRPC support. (#67)
- Added Requests support. (#66)
- Added ``google.auth.credentials.with_scopes_if_required`` helper. (#65)
- Added private helper for oauth2client migration. (#70)

v0.1.0
------

First release with core functionality available. This version is ready for
initial usage and testing.

- Added ``google.auth.credentials``, public interfaces for Credential types. (#8)
- Added ``google.oauth2.credentials``, credentials that use OAuth 2.0 access and refresh tokens (#24)
- Added ``google.oauth2.service_account``, credentials that use Service Account private keys to obtain OAuth 2.0 access tokens. (#25)
- Added ``google.auth.compute_engine``, credentials that use the Compute Engine metadata service to obtain OAuth 2.0 access tokens. (#22)
- Added ``google.auth.jwt.Credentials``, credentials that use a JWT as a bearer token.
- Added ``google.auth.app_engine``, credentials that use the Google App Engine App Identity service to obtain OAuth 2.0 access tokens. (#46)
- Added ``google.auth.default()``, an implementation of Google Application Default Credentials that supports automatic Project ID detection. (#32)
- Added system tests for all credential types. (#51, #54, #56, #58, #59, #60, #61, #62)
- Added ``google.auth.transports.urllib3.AuthorizedHttp``, an HTTP client that includes authentication provided by credentials. (#19)
- Documentation style and formatting updates.

v0.0.1
------

Initial release with foundational functionality for cryptography and JWTs.

- ``google.auth.crypt`` for creating and verifying cryptographic signatures.
- ``google.auth.jwt`` for creating (encoding) and verifying (decoding) JSON Web tokens.
