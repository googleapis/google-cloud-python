Changelog
=========

v1.6.1
------

11-12-2018 10:10 PST

Implementation Changes
++++++++++++++++++++++

- Automatically refresh impersonated credentials (`#304 <https://github.com/googleapis/google-auth-library-python/pull/304>`_)

v1.6.0
------

11-09-2018 11:07 PST

New Features
++++++++++++

- Add google.auth.impersonated_credentials (`#299 <https://github.com/googleapis/google-auth-library-python/pull/299>`_)

Documentation
+++++++++++++

- Update link to documentation for default credentials (`#296 <https://github.com/googleapis/google-auth-library-python/pull/296>`_)
- Update github issue templates (`#300 <https://github.com/googleapis/google-auth-library-python/pull/300>`_)
- Remove punctuation which becomes part of the url (`#284 <https://github.com/googleapis/google-auth-library-python/pull/284>`_)

Internal / Testing Changes
++++++++++++++++++++++++++

- Update trampoline.sh (`#302 <https://github.com/googleapis/google-auth-library-python/pull/302>`_)
- Enable static type checking with pytype (`#298 <https://github.com/googleapis/google-auth-library-python/pull/298>`_)
- Make classifiers in setup.py an array. (`#280 <https://github.com/googleapis/google-auth-library-python/pull/280>`_)


v1.5.1
------

- Fix check for error text on Python 3.7. (`#278 <https://github.com/googleapis/google-auth-library-python/pull/#278>`_)
- Use new Auth URIs. (`#281 <https://github.com/googleapis/google-auth-library-python/pull/#281>`_)
- Add code-of-conduct document. (`#270 <https://github.com/googleapis/google-auth-library-python/pull/#270>`_)
- Fix some typos in test_urllib3.py (`#268 <https://github.com/googleapis/google-auth-library-python/pull/#268>`_)

v1.5.0
------

- Warn when using user credentials from the Cloud SDK (`#266 <https://github.com/googleapis/google-auth-library-python/pull/266>`_)
- Add compute engine-based IDTokenCredentials (`#236 <https://github.com/googleapis/google-auth-library-python/pull/236>`_)
- Corrected some typos (`#265 <https://github.com/googleapis/google-auth-library-python/pull/265>`_)

v1.4.2
------

- Raise a helpful exception when trying to refresh credentials without a refresh token. (`#262 <https://github.com/googleapis/google-auth-library-python/pull/262>`_)
- Fix links to README and CONTRIBUTING in docs/index.rst. (`#260 <https://github.com/googleapis/google-auth-library-python/pull/260>`_)
- Fix a typo in credentials.py. (`#256 <https://github.com/googleapis/google-auth-library-python/pull/256>`_)
- Use pytest instead of py.test per upstream recommendation, #dropthedot. (`#255 <https://github.com/googleapis/google-auth-library-python/pull/255>`_)
- Fix typo on exemple of jwt usage (`#245 <https://github.com/googleapis/google-auth-library-python/pull/245>`_)

v1.4.1
------

- Added a check for the cryptography version before attempting to use it. (`#243 <https://github.com/googleapis/google-auth-library-python/pull/243>`_)

v1.4.0
------

- Added `cryptography`-based RSA signer and verifier. (`#185 <https://github.com/googleapis/google-auth-library-python/pull/185>`_)
- Added `google.oauth2.service_account.IDTokenCredentials`. (`#234 <https://github.com/googleapis/google-auth-library-python/pull/234>`_)
- Improved documentation around ID Tokens (`#224 <https://github.com/googleapis/google-auth-library-python/pull/224>`_)

v1.3.0
------

- Added ``google.oauth2.credentials.Credentials.from_authorized_user_file`` (`#226 <https://github.com/googleapis/google-auth-library-python/pull/#226>`_)
- Dropped direct pyasn1 dependency in favor of letting ``pyasn1-modules`` specify the right version. (`#230 <https://github.com/googleapis/google-auth-library-python/pull/#230>`_)
- ``default()`` now checks for the project ID environment var before warning about missing project ID. (`#227 <https://github.com/googleapis/google-auth-library-python/pull/#227>`_)
- Fixed the docstrings for ``has_scopes()`` and ``with_scopes()``. (`#228 <https://github.com/googleapis/google-auth-library-python/pull/#228>`_)
- Fixed example in docstring for ``ReadOnlyScoped``. (`#219 <https://github.com/googleapis/google-auth-library-python/pull/#219>`_)
- Made ``transport.requests`` use timeouts and retries to improve reliability. (`#220 <https://github.com/googleapis/google-auth-library-python/pull/#220>`_)

v1.2.1
------

- Excluded compiled Python files in source distributions. (`#215 <https://github.com/googleapis/google-auth-library-python/pull/#215>`_)
- Updated docs for creating RSASigner from string. (`#213 <https://github.com/googleapis/google-auth-library-python/pull/#213>`_)
- Use ``six.raise_from`` wherever possible. (`#212 <https://github.com/googleapis/google-auth-library-python/pull/#212>`_)
- Fixed a typo in a comment ``seconds`` not ``sections``. (`#210 <https://github.com/googleapis/google-auth-library-python/pull/#210>`_)

v1.2.0
------

- Added ``google.auth.credentials.AnonymousCredentials``. (`#206 <https://github.com/googleapis/google-auth-library-python/pull/#206>`_)
- Updated the documentation to link to the Google Cloud Platform Python setup guide (`#204 <https://github.com/googleapis/google-auth-library-python/pull/#204>`_)

v1.1.1
------

- ``google.oauth.credentials.Credentials`` now correctly inherits from ``ReadOnlyScoped`` instead of ``Scoped``. (`#200 <https://github.com/googleapis/google-auth-library-python/pull/#200>`_)

v1.1.0
------

- Added ``service_account.Credentials.project_id``. (`#187 <https://github.com/googleapis/google-auth-library-python/pull/#187>`_)
- Move read-only methods of ``credentials.Scoped`` into new interface ``credentials.ReadOnlyScoped``. (`#195 <https://github.com/googleapis/google-auth-library-python/pull/#195>`_, `#196 <https://github.com/googleapis/google-auth-library-python/pull/#196>`_)
- Make ``compute_engine.Credentials`` derive from ``ReadOnlyScoped`` instead of ``Scoped``. (`#195 <https://github.com/googleapis/google-auth-library-python/pull/#195>`_)
- Fix App Engine's expiration calculation (`#197 <https://github.com/googleapis/google-auth-library-python/pull/#197>`_)
- Split ``crypt`` module into a package to allow alternative implementations. (`#189 <https://github.com/googleapis/google-auth-library-python/pull/#189>`_)
- Add error message to handle case of empty string or missing file for GOOGLE_APPLICATION_CREDENTIALS (`#188 <https://github.com/googleapis/google-auth-library-python/pull/#188>`_)

v1.0.2
------

- Fixed a bug where the Cloud SDK executable could not be found on Windows, leading to project ID detection failing. (`#179 <https://github.com/googleapis/google-auth-library-python/pull/#179>`_)
- Fixed a bug where the timeout argument wasn't being passed through the httplib transport correctly. (`#175 <https://github.com/googleapis/google-auth-library-python/pull/#175>`_)
- Added documentation for using the library on Google App Engine standard. (`#172 <https://github.com/googleapis/google-auth-library-python/pull/#172>`_)
- Testing style updates. (`#168 <https://github.com/googleapis/google-auth-library-python/pull/#168>`_)
- Added documentation around the oauth2client deprecation. (`#165 <https://github.com/googleapis/google-auth-library-python/pull/#165>`_)
- Fixed a few lint issues caught by newer versions of pylint. (`#166 <https://github.com/googleapis/google-auth-library-python/pull/#166>`_)

v1.0.1
------

- Fixed a bug in the clock skew accommodation logic where expired credentials could be used for up to 5 minutes. (`#158 <https://github.com/googleapis/google-auth-library-python/pull/158>`_)

v1.0.0
------

Milestone release for v1.0.0.
No significant changes since v0.10.0

v0.10.0
-------

- Added ``jwt.OnDemandCredentials``. (`#142 <https://github.com/googleapis/google-auth-library-python/pull/142>`_)
- Added new public property ``id_token`` to ``oauth2.credentials.Credentials``. (`#150 <https://github.com/googleapis/google-auth-library-python/pull/150>`_)
- Added the ability to set the address used to communicate with the Compute Engine metadata server via the ``GCE_METADATA_ROOT`` and ``GCE_METADATA_IP`` environment variables. (`#148 <https://github.com/googleapis/google-auth-library-python/pull/148>`_)
- Changed the way cloud project IDs are ascertained from the Google Cloud SDK. (`#147 <https://github.com/googleapis/google-auth-library-python/pull/147>`_)
- Modified expiration logic to add a 5 minute clock skew accommodation. (`#145 <https://github.com/googleapis/google-auth-library-python/pull/145>`_)

v0.9.0
------

- Added ``service_account.Credentials.with_claims``. (`#140 <https://github.com/googleapis/google-auth-library-python/pull/140>`_)
- Moved ``google.auth.oauthlib`` and ``google.auth.flow`` to a new separate package ``google_auth_oauthlib``. (`#137 <https://github.com/googleapis/google-auth-library-python/pull/137>`_, `#139 <https://github.com/googleapis/google-auth-library-python/pull/139>`_, `#135 <https://github.com/googleapis/google-auth-library-python/pull/135>`_, `#126 <https://github.com/googleapis/google-auth-library-python/pull/126>`_)
- Added ``InstalledAppFlow`` to ``google_auth_oauthlib``. (`#128 <https://github.com/googleapis/google-auth-library-python/pull/128>`_)
- Fixed some packaging and documentation issues. (`#131 <https://github.com/googleapis/google-auth-library-python/pull/131>`_)
- Added a helpful error message when importing optional dependencies. (`#125 <https://github.com/googleapis/google-auth-library-python/pull/125>`_)
- Made all properties required to reconstruct ``google.oauth2.credentials.Credentials`` public. (`#124 <https://github.com/googleapis/google-auth-library-python/pull/124>`_)
- Added official Python 3.6 support. (`#102 <https://github.com/googleapis/google-auth-library-python/pull/102>`_)
- Added ``jwt.Credentials.from_signing_credentials`` and removed ``service_account.Credentials.to_jwt_credentials``. (`#120 <https://github.com/googleapis/google-auth-library-python/pull/120>`_)

v0.8.0
------

- Removed one-time token behavior from ``jwt.Credentials``, audience claim is now required and fixed. (`#117 <https://github.com/googleapis/google-auth-library-python/pull/117>`_)
- ``crypt.Signer`` and ``crypt.Verifier`` are now abstract base classes. The concrete implementations have been renamed to ``crypt.RSASigner`` and ``crypt.RSAVerifier``. ``app_engine.Signer`` and ``iam.Signer`` now inherit from ``crypt.Signer``. (`#115 <https://github.com/googleapis/google-auth-library-python/pull/115>`_)
- ``transport.grpc`` now correctly calls ``Credentials.before_request``. (`#116 <https://github.com/googleapis/google-auth-library-python/pull/116>`_)

v0.7.0
------

- Added ``google.auth.iam.Signer``. (`#108 <https://github.com/googleapis/google-auth-library-python/pull/108>`_)
- Fixed issue where ``google.auth.app_engine.Signer`` erroneously returns a tuple from ``sign()``. (`#109 <https://github.com/googleapis/google-auth-library-python/pull/109>`_)
- Added public property ``google.auth.credentials.Signing.signer``. (`#110 <https://github.com/googleapis/google-auth-library-python/pull/110>`_)

v0.6.0
------

- Added experimental integration with ``requests-oauthlib`` in ``google.oauth2.oauthlib`` and ``google.oauth2.flow``. (`#100 <https://github.com/googleapis/google-auth-library-python/pull/100>`_, `#105 <https://github.com/googleapis/google-auth-library-python/pull/105>`_, `#106 <https://github.com/googleapis/google-auth-library-python/pull/106>`_)
- Fixed typo in ``google_auth_httplib2``'s README. (`#105 <https://github.com/googleapis/google-auth-library-python/pull/105>`_)

v0.5.0
------

- Added ``app_engine.Signer``. (`#97 <https://github.com/googleapis/google-auth-library-python/pull/97>`_)
- Added ``crypt.Signer.from_service_account_file``. (`#95 <https://github.com/googleapis/google-auth-library-python/pull/95>`_)
- Fixed error handling in the oauth2 client. (`#96 <https://github.com/googleapis/google-auth-library-python/pull/96>`_)
- Fixed the App Engine system tests.

v0.4.0
------

- ``transports.grpc.secure_authorized_channel`` now passes ``kwargs`` to ``grpc.secure_channel``. (`#90 <https://github.com/googleapis/google-auth-library-python/pull/90>`_)
- Added new property ``credentials.Singing.signer_email`` which can be used to identify the signer of a message. (`#89 <https://github.com/googleapis/google-auth-library-python/pull/89>`_)
- (google_auth_httplib2) Added a proxy to ``httplib2.Http.connections``.

v0.3.2
------

- Fixed an issue where an ``ImportError`` would occur if ``google.oauth2`` was imported before ``google.auth``. (`#88 <https://github.com/googleapis/google-auth-library-python/pull/88>`_)

v0.3.1
------

- Fixed a bug where non-padded base64 encoded strings were not accepted. (`#87 <https://github.com/googleapis/google-auth-library-python/pull/87>`_)
- Fixed a bug where ID token verification did not correctly call the HTTP request function. (`#87 <https://github.com/googleapis/google-auth-library-python/pull/87>`_)

v0.3.0
------

- Added Google ID token verification helpers. (`#82 <https://github.com/googleapis/google-auth-library-python/pull/82>`_)
- Swapped the ``target`` and ``request`` argument order for ``grpc.secure_authorized_channel``. (`#81 <https://github.com/googleapis/google-auth-library-python/pull/81>`_)
- Added a user's guide. (`#79 <https://github.com/googleapis/google-auth-library-python/pull/79>`_)
- Made ``service_account_email`` a public property on several credential classes. (`#76 <https://github.com/googleapis/google-auth-library-python/pull/76>`_)
- Added a ``scope`` argument to ``google.auth.default``. (`#75 <https://github.com/googleapis/google-auth-library-python/pull/75>`_)
- Added support for the ``GCLOUD_PROJECT`` environment variable. (`#73 <https://github.com/googleapis/google-auth-library-python/pull/73>`_)

v0.2.0
------

- Added gRPC support. (`#67 <https://github.com/googleapis/google-auth-library-python/pull/67>`_)
- Added Requests support. (`#66 <https://github.com/googleapis/google-auth-library-python/pull/66>`_)
- Added ``google.auth.credentials.with_scopes_if_required`` helper. (`#65 <https://github.com/googleapis/google-auth-library-python/pull/65>`_)
- Added private helper for oauth2client migration. (`#70 <https://github.com/googleapis/google-auth-library-python/pull/70>`_)

v0.1.0
------

First release with core functionality available. This version is ready for
initial usage and testing.

- Added ``google.auth.credentials``, public interfaces for Credential types. (`#8 <https://github.com/googleapis/google-auth-library-python/pull/8>`_)
- Added ``google.oauth2.credentials``, credentials that use OAuth 2.0 access and refresh tokens (`#24 <https://github.com/googleapis/google-auth-library-python/pull/24>`_)
- Added ``google.oauth2.service_account``, credentials that use Service Account private keys to obtain OAuth 2.0 access tokens. (`#25 <https://github.com/googleapis/google-auth-library-python/pull/25>`_)
- Added ``google.auth.compute_engine``, credentials that use the Compute Engine metadata service to obtain OAuth 2.0 access tokens. (`#22 <https://github.com/googleapis/google-auth-library-python/pull/22>`_)
- Added ``google.auth.jwt.Credentials``, credentials that use a JWT as a bearer token.
- Added ``google.auth.app_engine``, credentials that use the Google App Engine App Identity service to obtain OAuth 2.0 access tokens. (`#46 <https://github.com/googleapis/google-auth-library-python/pull/46>`_)
- Added ``google.auth.default()``, an implementation of Google Application Default Credentials that supports automatic Project ID detection. (`#32 <https://github.com/googleapis/google-auth-library-python/pull/32>`_)
- Added system tests for all credential types. (`#51 <https://github.com/googleapis/google-auth-library-python/pull/51>`_, `#54 <https://github.com/googleapis/google-auth-library-python/pull/54>`_, `#56 <https://github.com/googleapis/google-auth-library-python/pull/56>`_, `#58 <https://github.com/googleapis/google-auth-library-python/pull/58>`_, `#59 <https://github.com/googleapis/google-auth-library-python/pull/59>`_, `#60 <https://github.com/googleapis/google-auth-library-python/pull/60>`_, `#61 <https://github.com/googleapis/google-auth-library-python/pull/61>`_, `#62 <https://github.com/googleapis/google-auth-library-python/pull/62>`_)
- Added ``google.auth.transports.urllib3.AuthorizedHttp``, an HTTP client that includes authentication provided by credentials. (`#19 <https://github.com/googleapis/google-auth-library-python/pull/19>`_)
- Documentation style and formatting updates.

v0.0.1
------

Initial release with foundational functionality for cryptography and JWTs.

- ``google.auth.crypt`` for creating and verifying cryptographic signatures.
- ``google.auth.jwt`` for creating (encoding) and verifying (decoding) JSON Web tokens.
