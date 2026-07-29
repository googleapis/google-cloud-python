SELECT * FROM ML.GENERATE_TEXT(MODEL `my_project.my_dataset.my_model`, (SELECT * FROM new_data), STRUCT(
  0.5 AS `temperature`,
  128 AS `max_output_tokens`,
  20 AS `top_k`,
  0.9 AS `top_p`,
  TRUE AS `flatten_json_output`,
  ['a', 'b'] AS `stop_sequences`,
  TRUE AS `ground_with_google_search`,
  'TYPE' AS `request_type`
))
