WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CASE
      WHEN `int64_col` IS NULL
      THEN NULL
      ELSE AVG(`int64_col`) OVER (PARTITION BY `string_col`)
    END AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_2` AS `agg_int64`
FROM `bfcte_1`