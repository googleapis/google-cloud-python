SELECT * FROM ML.EXPLAIN_PREDICT(MODEL `my_model`, (SELECT * FROM new_data), STRUCT(5 AS top_k_features))
