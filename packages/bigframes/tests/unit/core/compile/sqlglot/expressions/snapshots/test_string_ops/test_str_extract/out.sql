WITH `bfcte_0` AS (
  SELECT
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    IF(
      REGEXP_CONTAINS(`string_col`, '([a-z]*)'),
      REGEXP_REPLACE(`string_col`, CONCAT('.*?', '([a-z]*)', '.*'), '\\1'),
      NULL
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string_col`
FROM `bfcte_1`