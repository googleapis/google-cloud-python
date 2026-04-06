SELECT
  `rowindex`,
  `int64_col`,
  `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
WHERE
  `rowindex` > 0 AND `string_col` IN ('Hello, World!')