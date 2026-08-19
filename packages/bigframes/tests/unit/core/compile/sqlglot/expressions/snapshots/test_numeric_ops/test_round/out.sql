SELECT
  `rowindex`,
  `int64_col`,
  `float64_col`,
  CAST(ROUND(`int64_col`, 0) AS INT64) AS `int_round_0`,
  CAST(ROUND(`int64_col`, 1) AS INT64) AS `int_round_1`,
  CAST(ROUND(`int64_col`, -1) AS INT64) AS `int_round_m1`,
  ROUND(`float64_col`, 0) AS `float_round_0`,
  ROUND(`float64_col`, 1) AS `float_round_1`,
  ROUND(`float64_col`, -1) AS `float_round_m1`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`