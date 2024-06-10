# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/groupby-pandas.py

import bigframes.pandas as bpd

print("Groupby benchmark 7: max v1 - min v2 by id3")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.G1_1e9_1e2_5_0")

ans = (
    x.groupby("id3", as_index=False, dropna=False)
    .agg({"v1": "max", "v2": "min"})
    .assign(range_v1_v2=lambda x: x["v1"] - x["v2"])[["id3", "range_v1_v2"]]
)
print(ans.shape)
chk = [ans["range_v1_v2"].sum()]
print(chk)

bpd.reset_session()
