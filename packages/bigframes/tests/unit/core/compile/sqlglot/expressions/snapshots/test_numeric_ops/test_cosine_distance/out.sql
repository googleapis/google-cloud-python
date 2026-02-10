SELECT
  ML.DISTANCE(`int_list_col`, `int_list_col`, 'COSINE') AS `int_list_col`,
  ML.DISTANCE(`float_list_col`, `float_list_col`, 'COSINE') AS `float_list_col`
FROM `bigframes-dev`.`sqlglot_test`.`repeated_types`