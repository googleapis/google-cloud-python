# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/groupby-pandas.py

import bigframes.pandas as bpd

print("Groupby benchmark 1: sum v1 by id1")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.G1_1e9_1e2_5_0")

ans = x.groupby("id1", as_index=False, dropna=False).agg({"v1": "sum"})
print(ans.shape)
chk = [ans["v1"].sum()]
print(chk)

bpd.reset_session()
