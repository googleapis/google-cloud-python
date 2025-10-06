WITH `bfcte_0` AS (
  SELECT
    `string_col` AS `bfcol_0`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    AI.CLASSIFY(
      input => (`bfcol_0`),
      categories => ['greeting', 'rejection'],
      connection_id => 'bigframes-dev.us.bigframes-default-connection'
    ) AS `bfcol_1`
  FROM `bfcte_0`
)
SELECT
  `bfcol_1` AS `result`
FROM `bfcte_1`