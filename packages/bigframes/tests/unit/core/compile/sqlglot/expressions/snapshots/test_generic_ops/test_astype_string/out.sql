WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(`bfcol_1` AS STRING) AS `bfcol_2`,
    INITCAP(CAST(`bfcol_0` AS STRING)) AS `bfcol_3`,
    INITCAP(SAFE_CAST(`bfcol_0` AS STRING)) AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int64_col`,
  `bfcol_3` AS `bool_col`,
  `bfcol_4` AS `bool_w_safe`
FROM `bfcte_1`