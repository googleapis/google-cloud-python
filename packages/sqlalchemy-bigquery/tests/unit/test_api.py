# Copyright (c) 2021 The PyBigQuery Authors
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

import mock


def test_dry_run():

    with mock.patch("pybigquery._helpers.create_bigquery_client") as create_client:
        import pybigquery.api

        client = pybigquery.api.ApiClient("/my/creds", "mars")
        create_client.assert_called_once_with(
            credentials_path="/my/creds", location="mars"
        )
        client.dry_run_query("select 42")
        [(name, args, kwargs)] = create_client.return_value.query.mock_calls
        job_config = kwargs.pop("job_config")
        assert (name, args, kwargs) == ("", (), {"query": "select 42"})
        assert job_config.dry_run
        assert not job_config.use_query_cache
