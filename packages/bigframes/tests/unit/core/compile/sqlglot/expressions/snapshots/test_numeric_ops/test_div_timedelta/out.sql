WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `rowindex`,
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `rowindex` AS `bfcol_6`,
    `timestamp_col` AS `bfcol_7`,
    `int64_col` AS `bfcol_8`,
    CAST(FLOOR(IEEE_DIVIDE(86400000000, `int64_col`)) AS INT64) AS `bfcol_9`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `rowindex`,
  `bfcol_7` AS `timestamp_col`,
  `bfcol_8` AS `int64_col`,
  `bfcol_9` AS `timedelta_div_numeric`
FROM `bfcte_1`