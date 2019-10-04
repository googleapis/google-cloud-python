# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-auth-oauthlib/#history

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
