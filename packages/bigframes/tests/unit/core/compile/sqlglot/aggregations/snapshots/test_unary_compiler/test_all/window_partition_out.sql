WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `string_col` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN `bfcol_0` IS NULL
      THEN NULL
      ELSE COALESCE(LOGICAL_AND(`bfcol_0`) OVER (PARTITION BY `bfcol_1`), TRUE)
    END AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `agg_bool`
FROM `bfcte_1`