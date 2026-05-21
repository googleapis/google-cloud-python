import multiprocessing
import sys
from google.cloud.storage import Client

# def worker_task(blob):
#     """A simple task that receives a GCS blob across process boundary."""
#     print(f"Worker received blob: {blob.name}")

# def main():
#     print("Starting GCS Blob multiprocessing pickling test...")
#     try:
#         # Initialize the GCS Client, Bucket, and Blob
#         client = Client(project="multiprocessing-test-project")
#         bucket = client.bucket("reproduction-test-bucket")
#         blob = bucket.blob("reproduction-test-blob")
#         print("GCS Blob initialized.")
        
#         # Start a process and pass the GCS Blob
#         process = multiprocessing.Process(target=worker_task, args=(blob,))
#         print("Starting background worker process...")
#         process.start()
#         process.join()
#         print("Worker process finished successfully.")
        
#     except Exception as e:
#         print("\n[CRITICAL] Multiprocessing start failed!")
#         print(f"Error Type: {type(e).__name__}")
#         print(f"Error Message: {e}", file=sys.stderr)
#         sys.exit(1)

# if __name__ == "__main__":
#     main()


import pickle
from google.cloud.storage import Client

try:
    # Initialize the GCS Client
    client = Client(project="reproduction-test-project")
    print("Successfully initialized GCS Client.")
    
    # Attempt to serialize (pickle) the GCS Client instance
    print("Attempting to pickle GCS Client...")
    pickled_client = pickle.dumps(client)
    
    print("Successfully pickled GCS Client!")
    
    # Verify unpickling (deserialization)
    unpickled_client = pickle.loads(pickled_client)
    print("Successfully unpickled GCS Client!")
    
except Exception as e:
    import traceback
    print("\n[CRITICAL] Pickling failed!")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
    traceback.print_exc()
