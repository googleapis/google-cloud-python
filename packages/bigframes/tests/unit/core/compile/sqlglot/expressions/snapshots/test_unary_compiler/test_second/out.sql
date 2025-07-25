WITH `bfcte_0` AS (
  SELECT
    `timestamp_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    EXTRACT(SECOND FROM `bfcol_0`) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `timestamp_col`
FROM `bfcte_1`