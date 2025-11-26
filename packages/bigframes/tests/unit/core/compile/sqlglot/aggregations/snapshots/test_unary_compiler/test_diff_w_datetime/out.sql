WITH `bfcte_0` AS (
  SELECT
    `datetime_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    DATETIME_DIFF(
      `datetime_col`,
      LAG(`datetime_col`, 1) OVER (ORDER BY `datetime_col` ASC NULLS LAST),
      MICROSECOND
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `diff_datetime`
FROM `bfcte_1`