WITH `bfcte_0` AS (
  SELECT
    `id` AS `bfcol_0`,
    `people` AS `bfcol_1`
  FROM `bigframes-dev`.`sqlglot_test`.`nested_structs_types`
)
SELECT
  `bfcol_0` AS `id`,
  `bfcol_0` AS `id_1`,
  `bfcol_1` AS `people`
FROM `bfcte_0`