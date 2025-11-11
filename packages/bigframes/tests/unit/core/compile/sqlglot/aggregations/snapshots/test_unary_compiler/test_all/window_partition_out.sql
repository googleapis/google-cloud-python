WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN `bool_col` IS NULL
      THEN NULL
      ELSE COALESCE(LOGICAL_AND(`bool_col`) OVER (PARTITION BY `string_col`), TRUE)
    END AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `agg_bool`
FROM `bfcte_1`