# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/groupby-pandas.py

import bigframes.pandas as bpd

print("Groupby benchmark 4: mean v1:v3 by id4")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.G1_1e9_1e2_5_0")

ans = x.groupby("id4", as_index=False, dropna=False).agg(
    {"v1": "mean", "v2": "mean", "v3": "mean"}
)
print(ans.shape)
chk = [ans["v1"].sum(), ans["v2"].sum(), ans["v3"].sum()]
print(chk)

bpd.reset_session()
