WITH `bfcte_0` AS (
  SELECT
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    LEAD(`int64_col`, 1) OVER (ORDER BY `int64_col` ASC) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `lead`
FROM `bfcte_1`