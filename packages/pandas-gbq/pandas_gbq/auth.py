# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Private module for fetching Google BigQuery credentials."""

import logging
import os
import stat

logger = logging.getLogger(__name__)


CREDENTIALS_CACHE_DIRNAME = "pandas_gbq"
CREDENTIALS_CACHE_FILENAME = "bigquery_credentials.dat"
SCOPES = ["https://www.googleapis.com/auth/bigquery"]


def get_credentials(
    private_key=None,
    project_id=None,
    reauth=False,
    auth_local_webserver=True,
    auth_redirect_uri=None,
    client_id=None,
    client_secret=None,
):
    # pydata-google-auth does not have type hints nor stubs that mypy uses for type checking.
    # Remove this comment and the ignore pragma upon completing:
    # https://github.com/googleapis/google-cloud-python/issues/17045
    import pydata_google_auth  # type: ignore[import-untyped]

    if private_key:
        raise NotImplementedError(
            """The private_key argument is deprecated. Construct a credentials
object, instead, by using the
google.oauth2.service_account.Credentials.from_service_account_file or
google.oauth2.service_account.Credentials.from_service_account_info class
method from the google-auth package."""
        )

    credentials, default_project_id = pydata_google_auth.default(
        SCOPES,
        client_id=client_id,
        client_secret=client_secret,
        credentials_cache=get_credentials_cache(reauth),
        auth_local_webserver=auth_local_webserver,
        redirect_uri=auth_redirect_uri,
    )

    project_id = project_id or default_project_id
    return credentials, project_id


def get_credentials_cache(reauth):
    # pydata-google-auth does not have type hints nor stubs that mypy uses for type checking.
    # Remove this comment and the ignore pragma upon completing:
    # https://github.com/googleapis/google-cloud-python/issues/17045
    import pydata_google_auth.cache  # type: ignore[import-untyped]

    # pydata-google-auth (through at least 1.9.1) creates the cache file with
    # the default mode, so make the file private before each load and save.
    class _ReadWriteCredentialsCache(
        pydata_google_auth.cache.ReadWriteCredentialsCache
    ):
        def load(self):
            _make_cache_file_private(self, create=False)
            return super().load()

        def save(self, credentials):
            _make_cache_file_private(self, create=True)
            super().save(credentials)

    class _WriteOnlyCredentialsCache(
        pydata_google_auth.cache.WriteOnlyCredentialsCache
    ):
        def save(self, credentials):
            _make_cache_file_private(self, create=True)
            super().save(credentials)

    if reauth:
        return _WriteOnlyCredentialsCache(
            dirname=CREDENTIALS_CACHE_DIRNAME,
            filename=CREDENTIALS_CACHE_FILENAME,
        )
    return _ReadWriteCredentialsCache(
        dirname=CREDENTIALS_CACHE_DIRNAME, filename=CREDENTIALS_CACHE_FILENAME
    )


def _make_cache_file_private(cache, create):
    """Makes the credentials cache file readable and writable by its owner only.

    Failures are logged, never raised, so that authentication carries on.

    Args:
        cache: A pydata-google-auth credentials cache.
        create: Whether to create the cache file, and its directory, if they
            don't exist.
    """
    # _path is private to pydata-google-auth. If a later version drops it, skip
    # this rather than failing authentication.
    path = getattr(cache, "_path", None)
    # Skip Windows too, where os.chmod can only set the read-only flag.
    if path is None or os.name == "nt":
        return

    if create:
        try:
            os.makedirs(os.path.dirname(path) or os.curdir, mode=0o700, exist_ok=True)
            fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o600)
            os.close(fd)
        except OSError as exc:
            # Debug only: pydata-google-auth warns when the same write fails.
            logger.debug("Unable to create credentials cache file %s: %s", path, exc)

    try:
        file_stat = os.stat(path)
        # Remove other users' access from a file saved by an earlier version.
        if stat.S_ISREG(file_stat.st_mode) and file_stat.st_mode & 0o077:
            os.chmod(path, stat.S_IMODE(file_stat.st_mode) & 0o700)
    except (FileNotFoundError, NotADirectoryError):
        # No cache file yet, so there is nothing to restrict.
        pass
    except OSError as exc:
        logger.warning(
            "Unable to restrict access to credentials cache file %s: %s", path, exc
        )
