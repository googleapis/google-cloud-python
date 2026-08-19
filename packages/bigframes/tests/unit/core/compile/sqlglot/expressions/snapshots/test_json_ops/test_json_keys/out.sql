SELECT
  JSON_KEYS(`json_col`, NULL) AS `json_keys`,
  JSON_KEYS(`json_col`, 2) AS `json_keys_w_max_depth`
FROM `bigframes-dev`.`sqlglot_test`.`json_types` AS `bft_0`