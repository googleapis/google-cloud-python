WITH `bfcte_0` AS (
  SELECT
    `bool_col`,
    `int64_col`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
), `bfcte_1` AS (
  SELECT
    COALESCE(LOGICAL_AND(`bool_col`), TRUE) AS `bfcol_3`,
    COALESCE(LOGICAL_AND(`int64_col` <> 0), TRUE) AS `bfcol_4`,
    COALESCE(LOGICAL_AND(LENGTH(`string_col`) > 0), TRUE) AS `bfcol_5`
  FROM `bfcte_0`
)
SELECT
  `bfcol_3` AS `bool_col`,
  `bfcol_4` AS `int64_col`,
  `bfcol_5` AS `string_col`
FROM `bfcte_1`