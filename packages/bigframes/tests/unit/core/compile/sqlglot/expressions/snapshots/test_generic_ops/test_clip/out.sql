WITH `bfcte_0` AS (
  SELECT
    `int64_col`,
    `int64_too`,
    `rowindex`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    GREATEST(LEAST(`rowindex`, `int64_too`), `int64_col`) AS `bfcol_3`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `result_col`
FROM `bfcte_1`