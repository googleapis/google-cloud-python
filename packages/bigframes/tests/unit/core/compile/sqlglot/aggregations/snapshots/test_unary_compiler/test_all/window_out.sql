WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN `bfcol_0` IS NULL
      THEN NULL
      ELSE COALESCE(LOGICAL_AND(`bfcol_0`) OVER (), TRUE)
    END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `agg_bool`
FROM `bfcte_1`