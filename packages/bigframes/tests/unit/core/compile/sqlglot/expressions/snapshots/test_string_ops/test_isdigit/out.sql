WITH `bfcte_0` AS (
  SELECT
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    REGEXP_CONTAINS(
      `string_col`,
      '^[\\p{Nd}\\x{00B9}\\x{00B2}\\x{00B3}\\x{2070}\\x{2074}-\\x{2079}\\x{2080}-\\x{2089}]+$'
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string_col`
FROM `bfcte_1`