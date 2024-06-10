# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/groupby-pandas.py

import bigframes.pandas as bpd

print("Groupby benchmark 6: median v3 sd v3 by id4 id5")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.G1_1e9_1e2_5_0")

ans = x.groupby(["id4", "id5"], as_index=False, dropna=False).agg(
    {"v3": ["median", "std"]}
)
print(ans.shape)
chk = [ans["v3"]["median"].sum(), ans["v3"]["std"].sum()]
print(chk)

bpd.reset_session()
