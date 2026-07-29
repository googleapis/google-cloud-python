SELECT
  JSON_EXTRACT_STRING_ARRAY(`json_col`, '$') AS `json_col`
FROM `bigframes-dev`.`sqlglot_test`.`json_types` AS `bft_0`