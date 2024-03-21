import google.cloud.storage_client_v2 as storage_v2


transport_cls = storage_v2.StorageClient.get_transport_class()
channel = transport_cls.create_channel(attempt_direct_path=True)
transport = transport_cls(channel=channel)

request = storage_v2.ListBucketsRequest(
    parent="projects/python-docs-samples-tests",
)
storage_client = storage_v2.StorageClient(transport=transport)

page_result = storage_client.list_buckets(request=request)

