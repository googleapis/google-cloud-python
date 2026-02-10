SELECT
  `rowindex`,
  `int64_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
ORDER BY
  `rowindex` ASC NULLS LAST
LIMIT 10