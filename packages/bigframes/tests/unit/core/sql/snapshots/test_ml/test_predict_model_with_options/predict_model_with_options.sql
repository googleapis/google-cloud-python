SELECT * FROM ML.PREDICT(MODEL `my_model`, (SELECT * FROM new_data), STRUCT(True AS keep_original_columns))
