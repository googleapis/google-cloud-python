from google.cloud import storage
from google.oauth2 import service_account
import json

# Replace with your in-memory service account JSON key info
with open(
    "/usr/local/google/home/chandrasiri/chandrasiri-gcs-prober-pysdk-sa-key.json"
) as fp:
    service_account_info = json.load(fp)
# Create credentials from the in-memory dictionary
credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)

# Initialize the Storage client with the custom credentials
storage_client = storage.Client(
    project=service_account_info["project_id"], credentials=credentials
)

# Use the client to list buckets, for example
buckets = list(storage_client.list_buckets())
print(buckets)
