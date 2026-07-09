import base64
import struct
import google_crc32c

# 1. Obtain the GCS checksum as an integer
gcs_b64_checksum = "R4ccNA=="  # Checksum for b"Hello, "
decoded_bytes = base64.b64decode(gcs_b64_checksum)
rolling_crc = struct.unpack(">I", decoded_bytes)[0]
print("rollin crc", rolling_crc)

# 2. Update it with new chunks using the public extend() function
chunk1 = b"World!"
rolling_crc = google_crc32c.extend(rolling_crc, chunk1)

chunk2 = b" More data."
rolling_crc = google_crc32c.extend(rolling_crc, chunk2)

# 3. Convert back to base64 for GCS comparison
# updated_b64 = base64.b64encode(struct.pack(">I", rolling_crc)).decode("utf-8")
print(f"Final rolling checksum: {rolling_crc}")
