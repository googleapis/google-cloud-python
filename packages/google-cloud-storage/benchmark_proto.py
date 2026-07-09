import time
import os
import google_crc32c
from google.cloud._storage_v2.types import storage as storage_type


def custom_serialize(msg):
    if hasattr(msg, "_pb"):
        return msg._pb.SerializeToString()
    return msg.SerializeToString()


def benchmark():
    pb_BidiWriteObjectRequest = storage_type.BidiWriteObjectRequest._meta.pb
    pb_ChecksummedData = storage_type.ChecksummedData._meta.pb

    chunk_size = 2 * 1024 * 1024
    data = os.urandom(chunk_size)
    crc = google_crc32c.value(data)

    checksummed_data_pb = pb_ChecksummedData(content=data, crc32c=crc)
    pb_request = pb_BidiWriteObjectRequest(
        write_offset=0,
        checksummed_data=checksummed_data_pb,
    )

    checksummed_data_plus = storage_type.ChecksummedData(content=data)
    checksummed_data_plus.crc32c = crc
    proto_plus_request = storage_type.BidiWriteObjectRequest(
        write_offset=0,
        checksummed_data=checksummed_data_plus,
    )

    # 1. Custom serialize on raw pb
    t0 = time.perf_counter()
    for _ in range(1000):
        _ = custom_serialize(pb_request)
    t1 = time.perf_counter()
    print(f"custom_serialize(raw pb): {t1 - t0:.4f} seconds")

    # 2. Custom serialize on proto-plus
    t0 = time.perf_counter()
    for _ in range(1000):
        _ = custom_serialize(proto_plus_request)
    t1 = time.perf_counter()
    print(f"custom_serialize(proto-plus): {t1 - t0:.4f} seconds")


if __name__ == "__main__":
    benchmark()
