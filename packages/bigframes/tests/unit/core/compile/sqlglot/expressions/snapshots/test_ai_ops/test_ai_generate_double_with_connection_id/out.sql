SELECT
  AI.GENERATE_DOUBLE(
    prompt => STRUCT(`string_col` AS _field_1, ' is the same as ' AS _field_2, `string_col` AS _field_3),
    connection_id => 'bigframes-dev.us.bigframes-default-connection',
    endpoint => 'gemini-2.5-flash'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
