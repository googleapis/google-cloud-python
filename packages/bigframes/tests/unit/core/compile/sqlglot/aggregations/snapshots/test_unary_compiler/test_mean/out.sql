WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `duration_col`,
    `int64_col`,
    `int64_col` AS `bfcol_6`,
    `bool_col` AS `bfcol_7`,
    `duration_col` AS `bfcol_8`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    AVG(`bfcol_6`) AS `bfcol_12`,
    AVG(CAST(`bfcol_7` AS INT64)) AS `bfcol_13`,
    CAST(FLOOR(AVG(`bfcol_8`)) AS INT64) AS `bfcol_14`,
    CAST(FLOOR(AVG(`bfcol_6`)) AS INT64) AS `bfcol_15`
  FROM `bfcte_0`
)
SELECT
  `bfcol_12` AS `int64_col`,
  `bfcol_13` AS `bool_col`,
  `bfcol_14` AS `duration_col`,
  `bfcol_15` AS `int64_col_w_floor`
FROM `bfcte_1`