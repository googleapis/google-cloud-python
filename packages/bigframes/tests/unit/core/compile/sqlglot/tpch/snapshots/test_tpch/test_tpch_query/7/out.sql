WITH `bfcte_0` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_22`,
    `N_NAME` AS `bfcol_23`,
    COALESCE(COALESCE(`N_NAME` IN ('FRANCE', 'GERMANY'), FALSE), FALSE) AS `bfcol_24`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_4`
  WHERE
    COALESCE(COALESCE(`N_NAME` IN ('FRANCE', 'GERMANY'), FALSE), FALSE)
), `bfcte_1` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_2`,
    `S_NATIONKEY` AS `bfcol_3`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_3`
), `bfcte_2` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_31`,
    `L_SUPPKEY` AS `bfcol_32`,
    `L_EXTENDEDPRICE` AS `bfcol_33`,
    `L_DISCOUNT` AS `bfcol_34`,
    `L_SHIPDATE` AS `bfcol_35`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_2`
  WHERE
    (
      `L_SHIPDATE` >= CAST('1995-01-01' AS DATE)
    )
    AND (
      `L_SHIPDATE` <= CAST('1996-12-31' AS DATE)
    )
), `bfcte_3` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_9`,
    `O_CUSTKEY` AS `bfcol_10`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_1`
), `bfcte_4` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_11`,
    `C_NATIONKEY` AS `bfcol_12`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_0`
), `bfcte_5` AS (
  SELECT
    `bfcol_22` AS `bfcol_36`,
    `bfcol_23` AS `bfcol_37`
  FROM `bfcte_0`
), `bfcte_6` AS (
  SELECT
    `bfcol_22` AS `bfcol_38`,
    `bfcol_23` AS `bfcol_39`
  FROM `bfcte_0`
), `bfcte_7` AS (
  SELECT
    `bfcol_11` AS `bfcol_40`,
    `bfcol_39` AS `bfcol_41`
  FROM `bfcte_4`
  INNER JOIN `bfcte_6`
    ON `bfcol_12` = `bfcol_38`
), `bfcte_8` AS (
  SELECT
    `bfcol_41` AS `bfcol_42`,
    `bfcol_9` AS `bfcol_43`
  FROM `bfcte_7`
  INNER JOIN `bfcte_3`
    ON `bfcol_40` = `bfcol_10`
), `bfcte_9` AS (
  SELECT
    `bfcol_42` AS `bfcol_44`,
    `bfcol_32` AS `bfcol_45`,
    `bfcol_33` AS `bfcol_46`,
    `bfcol_34` AS `bfcol_47`,
    `bfcol_35` AS `bfcol_48`
  FROM `bfcte_8`
  INNER JOIN `bfcte_2`
    ON `bfcol_43` = `bfcol_31`
), `bfcte_10` AS (
  SELECT
    `bfcol_44` AS `bfcol_49`,
    `bfcol_46` AS `bfcol_50`,
    `bfcol_47` AS `bfcol_51`,
    `bfcol_48` AS `bfcol_52`,
    `bfcol_3` AS `bfcol_53`
  FROM `bfcte_9`
  INNER JOIN `bfcte_1`
    ON `bfcol_45` = `bfcol_2`
), `bfcte_11` AS (
  SELECT
    `bfcol_49`,
    `bfcol_50`,
    `bfcol_51`,
    `bfcol_52`,
    `bfcol_53`,
    `bfcol_36`,
    `bfcol_37`,
    `bfcol_49` AS `bfcol_59`,
    `bfcol_50` AS `bfcol_60`,
    `bfcol_51` AS `bfcol_61`,
    `bfcol_52` AS `bfcol_62`,
    `bfcol_37` AS `bfcol_63`,
    `bfcol_49` <> `bfcol_37` AS `bfcol_64`,
    `bfcol_49` AS `bfcol_76`,
    `bfcol_52` AS `bfcol_77`,
    `bfcol_37` AS `bfcol_78`,
    `bfcol_50` * (
      1.0 - `bfcol_51`
    ) AS `bfcol_79`,
    `bfcol_49` AS `bfcol_84`,
    `bfcol_37` AS `bfcol_85`,
    `bfcol_50` * (
      1.0 - `bfcol_51`
    ) AS `bfcol_86`,
    EXTRACT(YEAR FROM `bfcol_52`) AS `bfcol_87`
  FROM `bfcte_10`
  INNER JOIN `bfcte_5`
    ON `bfcol_53` = `bfcol_36`
  WHERE
    `bfcol_49` <> `bfcol_37`
), `bfcte_12` AS (
  SELECT
    `bfcol_85`,
    `bfcol_84`,
    `bfcol_87`,
    COALESCE(SUM(`bfcol_86`), 0) AS `bfcol_92`
  FROM `bfcte_11`
  WHERE
    NOT `bfcol_87` IS NULL
  GROUP BY
    `bfcol_85`,
    `bfcol_84`,
    `bfcol_87`
)
SELECT
  `bfcol_85` AS `SUPP_NATION`,
  `bfcol_84` AS `CUST_NATION`,
  `bfcol_87` AS `L_YEAR`,
  `bfcol_92` AS `REVENUE`
FROM `bfcte_12`
ORDER BY
  `bfcol_85` ASC NULLS LAST,
  `bfcol_84` ASC NULLS LAST,
  `bfcol_87` ASC NULLS LAST