SELECT * FROM ML.PREDICT(MODEL `my_model`, (SELECT * FROM new_data), STRUCT(TRUE AS `keep_original_columns`))
