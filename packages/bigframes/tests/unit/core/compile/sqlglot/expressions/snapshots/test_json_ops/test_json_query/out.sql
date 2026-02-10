SELECT
  JSON_QUERY(`json_col`, '$') AS `json_col`
FROM `bigframes-dev`.`sqlglot_test`.`json_types`