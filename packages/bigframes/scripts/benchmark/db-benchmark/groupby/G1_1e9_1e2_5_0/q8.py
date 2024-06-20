# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/groupby-pandas.py

import bigframes.pandas as bpd

print("Groupby benchmark 8: largest two v3 by id6")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.G1_1e9_1e2_5_0")

ans = (
    x[~x["v3"].isna()][["id6", "v3"]]
    .sort_values("v3", ascending=False)
    .groupby("id6", as_index=False, dropna=False)
    .head(2)
)
print(ans.shape)
chk = [ans["v3"].sum()]
print(chk)

bpd.reset_session()
