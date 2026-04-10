SELECT
  `rowindex`,
  ROUND(`int64_col` + `int64_too`) AS `bigframes_unnamed_column`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`