SELECT
  `rowindex`,
  `rowindex` AS `rowindex_1`,
  `int64_col`,
  `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
WHERE
  (
    (
      `rowindex` = 1
    ) OR (
      `int64_col` = 2
    )
  )
  AND STARTS_WITH(`string_col`, 'H')