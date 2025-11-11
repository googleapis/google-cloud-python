WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `bytes_col`,
    `int64_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    ~(
      `int64_col`
    ) AS `bfcol_6`,
    ~(
      `bytes_col`
    ) AS `bfcol_7`,
    NOT (
      `bool_col`
    ) AS `bfcol_8`
  FROM `bfcte_0`
)
SELECT
  `bfcol_6` AS `int64_col`,
  `bfcol_7` AS `bytes_col`,
  `bfcol_8` AS `bool_col`
FROM `bfcte_1`