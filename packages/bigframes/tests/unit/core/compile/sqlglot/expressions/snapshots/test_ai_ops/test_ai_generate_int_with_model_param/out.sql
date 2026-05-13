SELECT
  AI.GENERATE_INT(
    prompt => STRUCT(`string_col` AS _field_1, ' is the same as ' AS _field_2, `string_col` AS _field_3),
    model_params => JSON '{}'
  ) AS `result`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`
