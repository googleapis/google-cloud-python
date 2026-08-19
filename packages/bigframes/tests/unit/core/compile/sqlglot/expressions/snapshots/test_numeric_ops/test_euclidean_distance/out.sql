SELECT
  ML.DISTANCE(`int_list_col`, `int_list_col`, 'EUCLIDEAN') AS `int_list_col`,
  ML.DISTANCE(`numeric_list_col`, `numeric_list_col`, 'EUCLIDEAN') AS `numeric_list_col`
FROM `bigframes-dev`.`sqlglot_test`.`repeated_types` AS `bft_0`