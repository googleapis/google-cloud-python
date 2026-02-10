SELECT
  REGEXP_CONTAINS(
    `string_col`,
    '^[\\p{Nd}\\x{00B9}\\x{00B2}\\x{00B3}\\x{2070}\\x{2074}-\\x{2079}\\x{2080}-\\x{2089}]+$'
  ) AS `string_col`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`