WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE WHEN `bfcol_0` IS NULL THEN NULL ELSE ANY_VALUE(`bfcol_0`) OVER () END AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `agg_int64`
FROM `bfcte_1`