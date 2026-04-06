WITH `bfcte_0` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_0`,
    `S_NATIONKEY` AS `bfcol_1`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_5`
), `bfcte_1` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_2`,
    `C_NATIONKEY` AS `bfcol_3`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_4`
), `bfcte_2` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_4`,
    `N_NAME` AS `bfcol_5`,
    `N_REGIONKEY` AS `bfcol_6`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_3`
), `bfcte_3` AS (
  SELECT
    `R_REGIONKEY` AS `bfcol_32`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`REGION` AS `bft_2`
  WHERE
    `R_NAME` = 'ASIA'
), `bfcte_4` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_33`,
    `O_CUSTKEY` AS `bfcol_34`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_1`
  WHERE
    (
      `O_ORDERDATE` >= CAST('1994-01-01' AS DATE)
    )
    AND (
      `O_ORDERDATE` < CAST('1995-01-01' AS DATE)
    )
), `bfcte_5` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_29`,
    `L_SUPPKEY` AS `bfcol_30`,
    `L_EXTENDEDPRICE` * (
      1.0 - `L_DISCOUNT`
    ) AS `bfcol_31`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_0`
), `bfcte_6` AS (
  SELECT
    `bfcol_4` AS `bfcol_35`,
    `bfcol_5` AS `bfcol_36`
  FROM `bfcte_3`
  INNER JOIN `bfcte_2`
    ON `bfcol_32` = `bfcol_6`
), `bfcte_7` AS (
  SELECT
    `bfcol_35` AS `bfcol_37`,
    `bfcol_36` AS `bfcol_38`,
    `bfcol_2` AS `bfcol_39`
  FROM `bfcte_6`
  INNER JOIN `bfcte_1`
    ON `bfcol_35` = `bfcol_3`
), `bfcte_8` AS (
  SELECT
    `bfcol_33` AS `bfcol_40`,
    `bfcol_37` AS `bfcol_41`,
    `bfcol_38` AS `bfcol_42`
  FROM `bfcte_4`
  INNER JOIN `bfcte_7`
    ON `bfcol_34` = `bfcol_39`
), `bfcte_9` AS (
  SELECT
    `bfcol_30` AS `bfcol_43`,
    `bfcol_31` AS `bfcol_44`,
    `bfcol_41` AS `bfcol_45`,
    `bfcol_42` AS `bfcol_46`
  FROM `bfcte_5`
  INNER JOIN `bfcte_8`
    ON `bfcol_29` = `bfcol_40`
), `bfcte_10` AS (
  SELECT
    `bfcol_46`,
    COALESCE(SUM(`bfcol_44`), 0) AS `bfcol_49`
  FROM `bfcte_9`
  INNER JOIN `bfcte_0`
    ON `bfcol_43` = `bfcol_0` AND `bfcol_45` = `bfcol_1`
  GROUP BY
    `bfcol_46`
)
SELECT
  `bfcol_46` AS `N_NAME`,
  `bfcol_49` AS `REVENUE`
FROM `bfcte_10`
ORDER BY
  `bfcol_49` DESC,
  `bfcol_46` ASC NULLS LAST