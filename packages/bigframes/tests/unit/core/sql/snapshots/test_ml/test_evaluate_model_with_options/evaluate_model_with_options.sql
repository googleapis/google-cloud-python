SELECT * FROM ML.EVALUATE(MODEL `my_model`, STRUCT(False AS perform_aggregation, 10 AS horizon, 0.95 AS confidence_level))
