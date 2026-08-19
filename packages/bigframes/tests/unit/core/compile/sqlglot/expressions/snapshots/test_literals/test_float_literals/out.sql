SELECT
  CAST('Infinity' AS FLOAT64) AS `inf`,
  CAST('-Infinity' AS FLOAT64) AS `ninf`,
  NULL AS `nan`,
  -0.0 AS `neg_zero`,
  1e-05 AS `0.00001`,
  1e-10 AS `1E-10`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`