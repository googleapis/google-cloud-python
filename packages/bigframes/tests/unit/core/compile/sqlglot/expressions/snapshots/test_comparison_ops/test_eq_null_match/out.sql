WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    COALESCE(CAST(`int64_col` AS STRING), '$NULL_SENTINEL$') = COALESCE(CAST(CAST(`bool_col` AS INT64) AS STRING), '$NULL_SENTINEL$') AS `bfcol_4`
  FROM `bfcte_0`
)
SELECT
  `bfcol_4` AS `int64_col`
FROM `bfcte_1`