v0.3.0
------
* Use utc when parsing expiration timestamp (#26)
* Allow saving credentials in current directory (#25)


v0.2.0
------

* Populate id_token into credentials from oauth2session (#20)
* Carry token expiry from oauth2session into Credentials object (#18) (#19)
* Accept redirect_uri as arg to flow creating classmethods. (#17)

v0.1.1
------

* Allow ``access_type`` parameter to be overriden in ``Flow`` (#16)
* Use a test port that is less likely to be taken (#12)
* Documentation updates

v0.1.0
------

Add command line tool.

v0.0.1
------

Initial release. This package contains the functionality previously located in `google.oauth2.oauthlib` and `google.oauth2.flows`.
