# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/groupby-pandas.py

import bigframes.pandas as bpd

print("Groupby benchmark 10: sum v3 count by id1:id6")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.G1_1e9_1e2_5_0")

ans = x.groupby(
    ["id1", "id2", "id3", "id4", "id5", "id6"], as_index=False, dropna=False
).agg({"v3": "sum", "v1": "size"})
print(ans.shape)
chk = [ans["v3"].sum(), ans["v1"].sum()]
print(chk)

bpd.reset_session()
