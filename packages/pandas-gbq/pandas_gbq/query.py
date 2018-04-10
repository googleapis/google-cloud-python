
import pkg_resources
from google.cloud import bigquery


# Version with query config breaking change.
BIGQUERY_CONFIG_VERSION = pkg_resources.parse_version('0.32.0.dev1')


def query_config_old_version(resource):
    # Verify that we got a query resource. In newer versions of
    # google-cloud-bigquery enough of the configuration is passed on to the
    # backend that we can expect a backend validation error instead.
    if len(resource) != 1:
        raise ValueError("Only one job type must be specified, but "
                         "given {}".format(','.join(resource.keys())))
    if 'query' not in resource:
        raise ValueError("Only 'query' job type is supported")
    return bigquery.QueryJobConfig.from_api_repr(resource['query'])


def query_config(resource, installed_version):
    if installed_version < BIGQUERY_CONFIG_VERSION:
        return query_config_old_version(resource)
    return bigquery.QueryJobConfig.from_api_repr(resource)
