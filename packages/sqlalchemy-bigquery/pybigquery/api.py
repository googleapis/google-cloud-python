# Copyright (c) 2017 The PyBigQuery Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Integration with BigQuery API."""

from __future__ import absolute_import
from __future__ import unicode_literals

from google.cloud.bigquery import QueryJobConfig

from pybigquery import _helpers


class ApiClient(object):
    def __init__(self, credentials_path=None, location=None):
        self.credentials_path = credentials_path
        self.location = location
        self.client = _helpers.create_bigquery_client(
            credentials_path=credentials_path, location=location
        )

    def dry_run_query(self, query):
        job_config = QueryJobConfig()
        job_config.dry_run = True
        job_config.use_query_cache = False
        return self.client.query(query=(query), job_config=job_config)
