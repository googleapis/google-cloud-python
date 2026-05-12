SELECT
  AI.CLASSIFY(input => STRUCT(`string_col` AS _field_1), categories => ['greeting', 'rejection']) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`