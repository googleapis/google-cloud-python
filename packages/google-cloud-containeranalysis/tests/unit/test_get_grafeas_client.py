from google.cloud.devtools.containeranalysis_v1.services.container_analysis import (
    ContainerAnalysisAsyncClient,
)
from google.cloud.devtools.containeranalysis_v1.services.container_analysis import (
    ContainerAnalysisClient,
)


def test_get_grafeas_client():
    client = ContainerAnalysisClient()
    client.get_grafeas_client()


def test_get_grafeas_client_async():
    async_client = ContainerAnalysisAsyncClient()
    async_client.get_grafeas_client()
