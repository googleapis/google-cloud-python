# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Module for checking dependency versions and supported features."""

# https://github.com/googleapis/python-bigquery/blob/master/CHANGELOG.md
BIGQUERY_MINIMUM_VERSION = "1.11.1"
BIGQUERY_CLIENT_INFO_VERSION = "1.12.0"
BIGQUERY_BQSTORAGE_VERSION = "1.24.0"
BIGQUERY_FROM_DATAFRAME_CSV_VERSION = "2.6.0"
PANDAS_VERBOSITY_DEPRECATION_VERSION = "0.23.0"
PANDAS_PARQUET_LOSSLESS_TIMESTAMP_VERSION = "1.1.0"


class Features:
    def __init__(self):
        self._bigquery_installed_version = None
        self._pandas_installed_version = None

    @property
    def bigquery_installed_version(self):
        import google.cloud.bigquery
        import pkg_resources

        if self._bigquery_installed_version is not None:
            return self._bigquery_installed_version

        self._bigquery_installed_version = pkg_resources.parse_version(
            google.cloud.bigquery.__version__
        )
        bigquery_minimum_version = pkg_resources.parse_version(BIGQUERY_MINIMUM_VERSION)

        if self._bigquery_installed_version < bigquery_minimum_version:
            raise ImportError(
                "pandas-gbq requires google-cloud-bigquery >= {0}, "
                "current version {1}".format(
                    bigquery_minimum_version, self._bigquery_installed_version
                )
            )

        return self._bigquery_installed_version

    @property
    def bigquery_has_client_info(self):
        import pkg_resources

        bigquery_client_info_version = pkg_resources.parse_version(
            BIGQUERY_CLIENT_INFO_VERSION
        )
        return self.bigquery_installed_version >= bigquery_client_info_version

    @property
    def bigquery_has_bqstorage(self):
        import pkg_resources

        bigquery_bqstorage_version = pkg_resources.parse_version(
            BIGQUERY_BQSTORAGE_VERSION
        )
        return self.bigquery_installed_version >= bigquery_bqstorage_version

    @property
    def bigquery_has_from_dataframe_with_csv(self):
        import pkg_resources

        bigquery_from_dataframe_version = pkg_resources.parse_version(
            BIGQUERY_FROM_DATAFRAME_CSV_VERSION
        )
        return self.bigquery_installed_version >= bigquery_from_dataframe_version

    @property
    def pandas_installed_version(self):
        import pandas
        import pkg_resources

        if self._pandas_installed_version is not None:
            return self._pandas_installed_version

        self._pandas_installed_version = pkg_resources.parse_version(pandas.__version__)
        return self._pandas_installed_version

    @property
    def pandas_has_deprecated_verbose(self):
        import pkg_resources

        # Add check for Pandas version before showing deprecation warning.
        # https://github.com/pydata/pandas-gbq/issues/157
        pandas_verbosity_deprecation = pkg_resources.parse_version(
            PANDAS_VERBOSITY_DEPRECATION_VERSION
        )
        return self.pandas_installed_version >= pandas_verbosity_deprecation

    @property
    def pandas_has_parquet_with_lossless_timestamp(self):
        import pkg_resources

        desired_version = pkg_resources.parse_version(
            PANDAS_PARQUET_LOSSLESS_TIMESTAMP_VERSION
        )
        return self.pandas_installed_version >= desired_version


FEATURES = Features()
