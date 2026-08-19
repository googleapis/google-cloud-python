SELECT
  `bool_col` <> LAG(`bool_col`, 1) OVER (ORDER BY `bool_col` DESC) AS `diff_bool`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`