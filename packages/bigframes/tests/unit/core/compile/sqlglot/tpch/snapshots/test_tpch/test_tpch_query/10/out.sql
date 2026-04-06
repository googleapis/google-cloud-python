WITH `bfcte_0` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_0`,
    `N_NAME` AS `bfcol_1`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_3`
), `bfcte_1` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_2`,
    `L_EXTENDEDPRICE` AS `bfcol_3`,
    `L_DISCOUNT` AS `bfcol_4`,
    `L_RETURNFLAG` AS `bfcol_5`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_2`
), `bfcte_2` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_6`,
    `O_CUSTKEY` AS `bfcol_7`,
    `O_ORDERDATE` AS `bfcol_8`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_1`
), `bfcte_3` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_9`,
    `C_NAME` AS `bfcol_10`,
    `C_ADDRESS` AS `bfcol_11`,
    `C_NATIONKEY` AS `bfcol_12`,
    `C_PHONE` AS `bfcol_13`,
    `C_ACCTBAL` AS `bfcol_14`,
    `C_COMMENT` AS `bfcol_15`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_0`
), `bfcte_4` AS (
  SELECT
    `bfcol_9` AS `bfcol_16`,
    `bfcol_10` AS `bfcol_17`,
    `bfcol_11` AS `bfcol_18`,
    `bfcol_12` AS `bfcol_19`,
    `bfcol_13` AS `bfcol_20`,
    `bfcol_14` AS `bfcol_21`,
    `bfcol_15` AS `bfcol_22`,
    `bfcol_6` AS `bfcol_23`,
    `bfcol_8` AS `bfcol_24`
  FROM `bfcte_3`
  INNER JOIN `bfcte_2`
    ON `bfcol_9` = `bfcol_7`
), `bfcte_5` AS (
  SELECT
    `bfcol_16` AS `bfcol_25`,
    `bfcol_17` AS `bfcol_26`,
    `bfcol_18` AS `bfcol_27`,
    `bfcol_19` AS `bfcol_28`,
    `bfcol_20` AS `bfcol_29`,
    `bfcol_21` AS `bfcol_30`,
    `bfcol_22` AS `bfcol_31`,
    `bfcol_24` AS `bfcol_32`,
    `bfcol_3` AS `bfcol_33`,
    `bfcol_4` AS `bfcol_34`,
    `bfcol_5` AS `bfcol_35`
  FROM `bfcte_4`
  INNER JOIN `bfcte_1`
    ON `bfcol_23` = `bfcol_2`
), `bfcte_6` AS (
  SELECT
    `bfcol_25`,
    `bfcol_26`,
    `bfcol_27`,
    `bfcol_28`,
    `bfcol_29`,
    `bfcol_30`,
    `bfcol_31`,
    `bfcol_32`,
    `bfcol_33`,
    `bfcol_34`,
    `bfcol_35`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_25` AS `bfcol_47`,
    `bfcol_26` AS `bfcol_48`,
    `bfcol_27` AS `bfcol_49`,
    `bfcol_29` AS `bfcol_50`,
    `bfcol_30` AS `bfcol_51`,
    `bfcol_31` AS `bfcol_52`,
    `bfcol_33` AS `bfcol_53`,
    `bfcol_34` AS `bfcol_54`,
    `bfcol_1` AS `bfcol_55`,
    (
      (
        `bfcol_32` >= CAST('1993-10-01' AS DATE)
      )
      AND (
        `bfcol_32` < CAST('1994-01-01' AS DATE)
      )
    )
    AND (
      `bfcol_35` = 'R'
    ) AS `bfcol_56`,
    `bfcol_25` AS `bfcol_76`,
    `bfcol_26` AS `bfcol_77`,
    `bfcol_27` AS `bfcol_78`,
    `bfcol_29` AS `bfcol_79`,
    `bfcol_30` AS `bfcol_80`,
    `bfcol_31` AS `bfcol_81`,
    `bfcol_1` AS `bfcol_82`,
    ROUND((
      `bfcol_33` * (
        1 - `bfcol_34`
      )
    ), 2) AS `bfcol_83`
  FROM `bfcte_5`
  INNER JOIN `bfcte_0`
    ON `bfcol_28` = `bfcol_0`
  WHERE
    (
      (
        `bfcol_32` >= CAST('1993-10-01' AS DATE)
      )
      AND (
        `bfcol_32` < CAST('1994-01-01' AS DATE)
      )
    )
    AND (
      `bfcol_35` = 'R'
    )
), `bfcte_7` AS (
  SELECT
    `bfcol_76`,
    `bfcol_77`,
    `bfcol_80`,
    `bfcol_79`,
    `bfcol_82`,
    `bfcol_78`,
    `bfcol_81`,
    COALESCE(SUM(`bfcol_83`), 0) AS `bfcol_92`
  FROM `bfcte_6`
  WHERE
    NOT `bfcol_81` IS NULL
  GROUP BY
    `bfcol_76`,
    `bfcol_77`,
    `bfcol_80`,
    `bfcol_79`,
    `bfcol_82`,
    `bfcol_78`,
    `bfcol_81`
)
SELECT
  `bfcol_76` AS `C_CUSTKEY`,
  `bfcol_77` AS `C_NAME`,
  `bfcol_92` AS `REVENUE`,
  `bfcol_80` AS `C_ACCTBAL`,
  `bfcol_82` AS `N_NAME`,
  `bfcol_78` AS `C_ADDRESS`,
  `bfcol_79` AS `C_PHONE`,
  `bfcol_81` AS `C_COMMENT`
FROM `bfcte_7`
ORDER BY
  `bfcol_92` DESC,
  `bfcol_76` ASC NULLS LAST,
  `bfcol_77` ASC NULLS LAST,
  `bfcol_80` ASC NULLS LAST,
  `bfcol_79` ASC NULLS LAST,
  `bfcol_82` ASC NULLS LAST,
  `bfcol_78` ASC NULLS LAST,
  `bfcol_81` ASC NULLS LAST
LIMIT 20