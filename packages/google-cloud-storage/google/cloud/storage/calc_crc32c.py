import google_crc32c
import base64
import sys

full_file_path = sys.argv[1]
# rolling_checksum = google_crc32c.Checksum()
# bytes_to_read = 100*1024 *1024
# chunk_size = 2*1024 *1024
# bytes_read = 0
# data_chunks = []
# with open(full_file_path, 'rb') as fp:
#     # data = fp.read(32*1024*1024)
#     while bytes_read < bytes_to_read:
#         # fp.seek(16*1024*1024)
#         chunk = fp.read(chunk_size)
#         rolling_checksum.update(chunk)
#         bytes_read += len(chunk)
#         if bytes_read %  (2*1024*1024) == 0:
#             print('At', bytes_read/1024/1024,'MiB', int.from_bytes(rolling_checksum.digest(), byteorder="big"))
#         data_chunks.append(chunk)
# data = b''.join(data_chunks)

with open(full_file_path, "rb") as fp:
    data = fp.read()


crc32c_int = google_crc32c.value(data)
crc32c_hex = f"{crc32c_int:08x}"
crc32c_bytes = crc32c_int.to_bytes(4, "big")
base64_encoded = base64.b64encode(crc32c_bytes)
crc32c_base64 = base64_encoded.decode("utf-8")

print(crc32c_hex)
print(crc32c_base64)
print(crc32c_int)
# print(crc32c_base64)
