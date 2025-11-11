WITH `bfcte_0` AS (
  SELECT
    `date_col`,
    `rowindex`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    43200000000 AS `bfcol_6`
  FROM `bfcte_0`
)
SELECT
  `rowindex`,
  `timestamp_col`,
  `date_col`,
  `bfcol_6` AS `timedelta_div_numeric`
FROM `bfcte_1`