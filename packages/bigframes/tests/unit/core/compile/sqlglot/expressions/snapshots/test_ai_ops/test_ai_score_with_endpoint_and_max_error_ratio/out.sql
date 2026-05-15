SELECT
  AI.SCORE(
    prompt => STRUCT(`string_col` AS _field_1, ' is the same as ' AS _field_2, `string_col` AS _field_3),
    endpoint => 'gemini-2.5-flash',
    max_error_ratio => 0.5
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`