WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    COALESCE(CAST(`bfcol_1` AS STRING), '$NULL_SENTINEL$') = COALESCE(CAST(CAST(`bfcol_0` AS INT64) AS STRING), '$NULL_SENTINEL$') AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `int64_col`
FROM `bfcte_1`