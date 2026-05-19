import bigframes
import bigframes.pandas as bpd
import pandas as pd
import sys

# Initialize session
bpd.options.compute.backend = "substrait"

df = bpd.read_pandas(pd.DataFrame({
    "bytes_col": [b"a", b"b", b"c", b"d", b"e", b"f", b"g"],
    "numeric_col": [1, 2, 3, 4, 5, 6, 7],
    "val": [10, 20, 30, 40, 50, 60, 70]
}))

sub_df = df.iloc[[4, 1, 2]]
sub_df = sub_df.set_index(["bytes_col", "numeric_col"])
drop_index = sub_df.index

df = df.set_index(["bytes_col", "numeric_col"])

print("DF INDEX:")
print(df.index)
print("DROP INDEX:")
print(drop_index)

res = df.drop(index=drop_index)
print("RESULT:")
print(res.to_pandas())
