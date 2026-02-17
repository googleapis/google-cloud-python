SELECT
  JSON_SET(`json_col`, '$.a', 100) AS `json_col`
FROM `bigframes-dev`.`sqlglot_test`.`json_types` AS `bft_0`