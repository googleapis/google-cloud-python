SELECT
  `int64_col` - LAG(`int64_col`, 1) OVER (ORDER BY `int64_col` ASC NULLS LAST) AS `diff_int`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`