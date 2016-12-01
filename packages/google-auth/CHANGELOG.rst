Changelog
=========

v0.3.2
------

- Fixed an issue where an `ImportError` would occur if `google.oauth2` was imported before `google.auth`. (#88)

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
