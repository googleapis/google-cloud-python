WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    APPROX_TOP_COUNT(`int64_col`, 10) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `int64_col`
FROM `bfcte_1`