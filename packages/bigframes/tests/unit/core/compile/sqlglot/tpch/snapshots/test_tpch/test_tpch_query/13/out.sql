WITH `bfcte_0` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_10`,
    `O_CUSTKEY` AS `bfcol_11`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_1`
  WHERE
    NOT (
      REGEXP_CONTAINS(`O_COMMENT`, 'special.*requests')
    )
), `bfcte_1` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_3`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_0`
), `bfcte_2` AS (
  SELECT
    `bfcol_3`,
    COUNT(`bfcol_10`) AS `bfcol_14`
  FROM `bfcte_1`
  LEFT JOIN `bfcte_0`
    ON `bfcol_3` = `bfcol_11`
  GROUP BY
    `bfcol_3`
), `bfcte_3` AS (
  SELECT
    `bfcol_14`,
    COUNT(1) AS `bfcol_16`
  FROM `bfcte_2`
  WHERE
    NOT `bfcol_14` IS NULL
  GROUP BY
    `bfcol_14`
)
SELECT
  `bfcol_14` AS `C_COUNT`,
  `bfcol_16` AS `CUSTDIST`
FROM `bfcte_3`
ORDER BY
  `bfcol_16` DESC,
  `bfcol_14` DESC