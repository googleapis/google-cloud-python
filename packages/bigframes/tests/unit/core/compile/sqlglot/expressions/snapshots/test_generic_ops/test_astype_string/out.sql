WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(`int64_col` AS STRING) AS `bfcol_2`,
    INITCAP(CAST(`bool_col` AS STRING)) AS `bfcol_3`,
    INITCAP(SAFE_CAST(`bool_col` AS STRING)) AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `int64_col`,
  `bfcol_3` AS `bool_col`,
  `bfcol_4` AS `bool_w_safe`
FROM `bfcte_1`