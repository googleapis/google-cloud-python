# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-auth-oauthlib/#history

### [0.4.3](https://www.github.com/googleapis/google-auth-library-python-oauthlib/compare/v0.4.2...v0.4.3) (2021-02-12)


### Bug Fixes

* add `charset-utf-8` to response header ([#104](https://www.github.com/googleapis/google-auth-library-python-oauthlib/issues/104)) ([53e31e2](https://www.github.com/googleapis/google-auth-library-python-oauthlib/commit/53e31e2d03b315c12670370f67bdca29b1cd5422))
* **deps:** add lower bounds to all dependencies ([#99](https://www.github.com/googleapis/google-auth-library-python-oauthlib/issues/99)) ([5587c6a](https://www.github.com/googleapis/google-auth-library-python-oauthlib/commit/5587c6a72547742986e363e1f5ef6bcabd93bb02))

### [0.4.2](https://www.github.com/googleapis/google-auth-library-python-oauthlib/compare/v0.4.1...v0.4.2) (2020-10-28)


### Bug Fixes

* don't open browser if port is occupied ([#92](https://www.github.com/googleapis/google-auth-library-python-oauthlib/issues/92)) ([0004057](https://www.github.com/googleapis/google-auth-library-python-oauthlib/commit/00040576ab096faec1f6eb54c886cb9c33be17ed)), closes [#75](https://www.github.com/googleapis/google-auth-library-python-oauthlib/issues/75)

## 0.4.1

08-26-2019 13:25 PDT

### Implementation Changes
- Don't auto-generate code_verifier by default. ([#48](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/48))

### Internal / Testing Changes
- Add renovate.json ([#56](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/56))

## 0.4.0
- Add `get_user_credentials` function to get your user credentials ([#40](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/40))
- Add noxfile ([#43](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/43))
- Implement code verifier (PKCE) ([#42](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/42))
- Use actual server port in redirect_uri to allow automatic assignment ([#33](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/33))
([#41](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/41))

## 0.3.0
- Use utc when parsing expiration timestamp ([#26](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/26))
- Allow saving credentials in current directory ([#25](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/25))

## 0.2.0
- Populate id_token into credentials from oauth2session ([#20](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/20))
- Carry token expiry from oauth2session into Credentials object ([#18](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/18)) ([#19](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/19))
- Accept redirect_uri as arg to flow creating classmethods. ([#17](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/17))

## 0.1.1
- Allow ``access_type`` parameter to be overriden in ``Flow`` ([#16](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/16))
- Use a test port that is less likely to be taken ([#12](https://github.com/googleapis/google-auth-library-python-oauthlib/pull/12))
- Documentation updates

## 0.1.0
Add command line tool.

## 0.0.1
Initial release. This package contains the functionality previously located in `google.oauth2.oauthlib` and `google.oauth2.flows`.
