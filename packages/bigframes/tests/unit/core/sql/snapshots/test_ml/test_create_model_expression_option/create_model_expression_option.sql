CREATE MODEL `my_model`
OPTIONS(l2_reg = 0.1, booster_type = 'gbtree')
AS SELECT * FROM t
