SELECT
  LEAD(`int64_col`, 1) OVER (ORDER BY `int64_col` ASC) AS `lead`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`