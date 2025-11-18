WITH `bfcte_0` AS (
  SELECT
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    AI.GENERATE(
      prompt => (`string_col`, ' is the same as ', `string_col`),
      request_type => 'SHARED',
      model_params => JSON '{}'
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `result`
FROM `bfcte_1`