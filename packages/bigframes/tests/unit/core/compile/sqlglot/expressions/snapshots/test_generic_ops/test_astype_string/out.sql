SELECT
  CAST(`int64_col` AS STRING),
  INITCAP(CAST(`bool_col` AS STRING)) AS `bool_col`,
  INITCAP(SAFE_CAST(`bool_col` AS STRING)) AS `bool_w_safe`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`