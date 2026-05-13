SELECT
  AI.GENERATE(
    prompt => STRUCT(`string_col` AS _field_1, ' is the same as ' AS _field_2, `string_col` AS _field_3),
    endpoint => 'gemini-2.5-flash',
    output_schema => 'x INT64, y FLOAT64'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
