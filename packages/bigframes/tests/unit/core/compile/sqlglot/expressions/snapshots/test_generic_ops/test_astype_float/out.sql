WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(CAST(`bfcol_0` AS INT64) AS FLOAT64) AS `bfcol_1`,
    CAST('1.34235e4' AS FLOAT64) AS `bfcol_2`,
    SAFE_CAST(SAFE_CAST(`bfcol_0` AS INT64) AS FLOAT64) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `bool_col`,
  `bfcol_2` AS `str_const`,
  `bfcol_3` AS `bool_w_safe`
FROM `bfcte_1`