WITH `bfcte_0` AS (
  SELECT
    `bool_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    COALESCE(LOGICAL_AND(`bool_col`) OVER (), TRUE) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `agg_bool`
FROM `bfcte_1`