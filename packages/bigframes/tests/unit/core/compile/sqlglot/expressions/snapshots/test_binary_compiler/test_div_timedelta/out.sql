WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`,
    `rowindex` AS `bfcol_1`,
    `timestamp_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_1` AS `bfcol_6`,
    `bfcol_2` AS `bfcol_7`,
    `bfcol_0` AS `bfcol_8`,
    CAST(FLOOR(IEEE_DIVIDE(86400000000, `bfcol_0`)) AS INT64) AS `bfcol_9`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `rowindex`,
  `bfcol_7` AS `timestamp_col`,
  `bfcol_8` AS `int64_col`,
  `bfcol_9` AS `timedelta_div_numeric`
FROM `bfcte_1`