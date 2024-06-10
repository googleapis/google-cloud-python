# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/join-pandas.py

import bigframes.pandas as bpd

print("Join benchmark 1: small inner on int")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.J1_1e9_NA_0_0")
small = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.J1_1e9_1e3_0_0")

ans = x.merge(small, on="id1")
print(ans.shape)

chk = [ans["v1"].sum(), ans["v2"].sum()]
print(chk)

bpd.reset_session()
