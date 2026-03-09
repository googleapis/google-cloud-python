SELECT * FROM ML.PREDICT(MODEL `my_model`, (SELECT * FROM new_data), STRUCT(true AS keep_original_columns))
