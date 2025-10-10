WITH `bfcte_0` AS (
  SELECT
    `date_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    CAST(DATE_DIFF(
      `bfcol_0`,
      LAG(`bfcol_0`, 1) OVER (ORDER BY `bfcol_0` IS NULL ASC NULLS LAST, `bfcol_0` ASC NULLS LAST),
      DAY
    ) * 86400000000 AS INT64) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `diff_date`
FROM `bfcte_1`