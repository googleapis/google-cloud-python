WITH `bfcte_0` AS (
  SELECT
    `date_col` AS `bfcol_0`,
    `datetime_col` AS `bfcol_1`,
    `timestamp_col` AS `bfcol_2`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(MOD(EXTRACT(DAYOFWEEK FROM `bfcol_1`) + 5, 7) AS INT64) AS `bfcol_6`,
    CAST(MOD(EXTRACT(DAYOFWEEK FROM `bfcol_2`) + 5, 7) AS INT64) AS `bfcol_7`,
    CAST(MOD(EXTRACT(DAYOFWEEK FROM `bfcol_0`) + 5, 7) AS INT64) AS `bfcol_8`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `datetime_col`,
  `bfcol_7` AS `timestamp_col`,
  `bfcol_8` AS `date_col`
FROM `bfcte_1`