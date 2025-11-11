WITH `bfcte_0` AS (
  SELECT
    `people`
  FROM `bigframes-dev`.`sqlglot_test`.`nested_structs_types`
), `bfcte_1` AS (
  SELECT
    *,
    `people`.`name` AS `bfcol_1`,
    `people`.`name` AS `bfcol_2`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `string`,
  `bfcol_2` AS `int`
FROM `bfcte_1`