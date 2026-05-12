SELECT
  AI.CLASSIFY(
    input => STRUCT(`string_col` AS _field_1),
    categories => ['greeting', 'rejection'],
    connection_id => 'bigframes-dev.us.bigframes-default-connection'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`