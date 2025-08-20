WITH `bfcte_0` AS (
  SELECT
    `date_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`,
    `timestamp_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    43200000000 AS `bfcol_6`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `rowindex`,
  `bfcol_2` AS `timestamp_col`,
  `bfcol_0` AS `date_col`,
  `bfcol_6` AS `timedelta_div_numeric`
FROM `bfcte_1`