CREATE MODEL `my_model`
OPTIONS(model_type = 'LINEAR_REG', learn_rate = HPARAM_RANGE(0.0001, 1.0), optimizer = HPARAM_CANDIDATES(['ADAGRAD', 'SGD']))
AS SELECT * FROM t
