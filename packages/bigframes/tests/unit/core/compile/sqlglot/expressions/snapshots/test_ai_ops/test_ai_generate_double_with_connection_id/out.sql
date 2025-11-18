WITH `bfcte_0` AS (
  SELECT
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    AI.GENERATE_DOUBLE(
      prompt => (`string_col`, ' is the same as ', `string_col`),
      connection_id => 'bigframes-dev.us.bigframes-default-connection',
      endpoint => 'gemini-2.5-flash',
      request_type => 'SHARED'
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `result`
FROM `bfcte_1`