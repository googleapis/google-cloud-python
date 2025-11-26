WITH `bfcte_0` AS (
  SELECT
    `timestamp_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    TIMESTAMP_DIFF(
      `timestamp_col`,
      LAG(`timestamp_col`, 1) OVER (ORDER BY `timestamp_col` DESC),
      MICROSECOND
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `diff_timestamp`
FROM `bfcte_1`