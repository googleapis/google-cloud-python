WITH `bfcte_0` AS (
  SELECT
    `id`,
    `people`
  FROM `bigframes-dev`.`sqlglot_test`.`nested_structs_types`
)
SELECT
  `id`,
  `id` AS `id_1`,
  `people`
FROM `bfcte_0`