CREATE MODEL `my_model`
OPTIONS(hidden_units = [32, 16], dropout = 0.2)
AS SELECT * FROM t
