WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    AI.GENERATE_DOUBLE(
      prompt => (`bfcol_0`, ' is the same as ', `bfcol_0`),
      connection_id => 'bigframes-dev.us.bigframes-default-connection',
      request_type => 'SHARED',
      model_params => JSON '{}'
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `result`
FROM `bfcte_1`