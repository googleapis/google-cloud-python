WITH `bfcte_0` AS (
  SELECT
    `int64_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    FIRST_VALUE(`bfcol_0` IGNORE NULLS) OVER (
      ORDER BY `bfcol_0` IS NULL ASC NULLS LAST, `bfcol_0` ASC NULLS LAST
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `agg_int64`
FROM `bfcte_1`