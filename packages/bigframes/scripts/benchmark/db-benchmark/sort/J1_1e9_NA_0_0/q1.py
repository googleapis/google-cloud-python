# Contains code from https://github.com/duckdblabs/db-benchmark/blob/master/pandas/sort-pandas.py

import bigframes.pandas as bpd

print("Sort benchmark 1: sort by int id2")

x = bpd.read_gbq("bigframes-dev-perf.dbbenchmark.J1_1e9_NA_0_0")

ans = x.sort_values("id2")
print(ans.shape)

chk = [ans["v1"].sum()]
print(chk)

bpd.reset_session()
