SELECT
  `rowindex`,
  `bool_col`,
  `int64_col`,
  `int64_col` | `int64_col` AS `int_and_int`,
  `bool_col` OR `bool_col` AS `bool_and_bool`,
  IF(`bool_col` = TRUE, `bool_col`, NULL) AS `bool_and_null`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`