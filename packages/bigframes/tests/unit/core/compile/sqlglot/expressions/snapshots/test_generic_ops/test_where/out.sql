SELECT
  IF(`bool_col`, `int64_col`, `float64_col`) AS `result_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`