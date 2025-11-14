WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `float64_col`,
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    [COALESCE(`bool_col`, FALSE)] AS `bfcol_8`,
    [COALESCE(`int64_col`, 0)] AS `bfcol_9`,
    [COALESCE(`string_col`, ''), COALESCE(`string_col`, '')] AS `bfcol_10`,
    [
      COALESCE(`int64_col`, 0),
      CAST(COALESCE(`bool_col`, FALSE) AS INT64),
      COALESCE(`float64_col`, 0.0)
    ] AS `bfcol_11`
  FROM `bfcte_0`
)
SELECT
  `bfcol_8` AS `bool_col`,
  `bfcol_9` AS `int64_col`,
  `bfcol_10` AS `strs_col`,
  `bfcol_11` AS `numeric_col`
FROM `bfcte_1`