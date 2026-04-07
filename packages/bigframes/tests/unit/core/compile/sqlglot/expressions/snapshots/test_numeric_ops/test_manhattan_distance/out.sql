SELECT
  ML.DISTANCE(`float_list_col`, `float_list_col`, 'MANHATTAN') AS `float_list_col`,
  ML.DISTANCE(`numeric_list_col`, `numeric_list_col`, 'MANHATTAN') AS `numeric_list_col`
FROM `bigframes-dev`.`sqlglot_test`.`repeated_types` AS `bft_0`