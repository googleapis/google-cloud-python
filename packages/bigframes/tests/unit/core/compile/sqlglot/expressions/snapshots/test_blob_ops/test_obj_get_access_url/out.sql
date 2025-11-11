WITH `bfcte_0` AS (
  SELECT
    `rowindex`,
    `string_col`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    OBJ.MAKE_REF(`string_col`, 'bigframes-dev.test-region.bigframes-default-connection') AS `bfcol_4`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    OBJ.GET_ACCESS_URL(`bfcol_4`) AS `bfcol_7`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    JSON_VALUE(`bfcol_7`, '$.access_urls.read_url') AS `bfcol_10`
  FROM `bfcte_2`
)
SELECT
  `rowindex`,
  `bfcol_10` AS `string_col`
FROM `bfcte_3`