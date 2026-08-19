SELECT
  LAG(`int64_col`, 1) OVER (ORDER BY `int64_col` ASC) AS `lag`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`