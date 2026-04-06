WITH `bfcte_0` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_0`,
    `N_NAME` AS `bfcol_1`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_5` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_1` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_2`,
    `O_ORDERDATE` AS `bfcol_3`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_4` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_2` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_4`,
    `S_NATIONKEY` AS `bfcol_5`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_3` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_3` AS (
  SELECT
    `PS_PARTKEY` AS `bfcol_6`,
    `PS_SUPPKEY` AS `bfcol_7`,
    `PS_SUPPLYCOST` AS `bfcol_8`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PARTSUPP` AS `bft_2` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_4` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_9`,
    `L_PARTKEY` AS `bfcol_10`,
    `L_SUPPKEY` AS `bfcol_11`,
    `L_QUANTITY` AS `bfcol_12`,
    `L_EXTENDEDPRICE` AS `bfcol_13`,
    `L_DISCOUNT` AS `bfcol_14`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_5` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_15`,
    `P_NAME` AS `bfcol_16`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_6` AS (
  SELECT
    `bfcol_16` AS `bfcol_17`,
    `bfcol_9` AS `bfcol_18`,
    `bfcol_10` AS `bfcol_19`,
    `bfcol_11` AS `bfcol_20`,
    `bfcol_12` AS `bfcol_21`,
    `bfcol_13` AS `bfcol_22`,
    `bfcol_14` AS `bfcol_23`
  FROM `bfcte_5`
  INNER JOIN `bfcte_4`
    ON `bfcol_15` = `bfcol_10`
), `bfcte_7` AS (
  SELECT
    `bfcol_17` AS `bfcol_24`,
    `bfcol_18` AS `bfcol_25`,
    `bfcol_20` AS `bfcol_26`,
    `bfcol_21` AS `bfcol_27`,
    `bfcol_22` AS `bfcol_28`,
    `bfcol_23` AS `bfcol_29`,
    `bfcol_8` AS `bfcol_30`
  FROM `bfcte_6`
  INNER JOIN `bfcte_3`
    ON `bfcol_20` = `bfcol_7` AND `bfcol_19` = `bfcol_6`
), `bfcte_8` AS (
  SELECT
    `bfcol_24` AS `bfcol_31`,
    `bfcol_25` AS `bfcol_32`,
    `bfcol_27` AS `bfcol_33`,
    `bfcol_28` AS `bfcol_34`,
    `bfcol_29` AS `bfcol_35`,
    `bfcol_30` AS `bfcol_36`,
    `bfcol_5` AS `bfcol_37`
  FROM `bfcte_7`
  INNER JOIN `bfcte_2`
    ON `bfcol_26` = `bfcol_4`
), `bfcte_9` AS (
  SELECT
    `bfcol_31` AS `bfcol_38`,
    `bfcol_33` AS `bfcol_39`,
    `bfcol_34` AS `bfcol_40`,
    `bfcol_35` AS `bfcol_41`,
    `bfcol_36` AS `bfcol_42`,
    `bfcol_37` AS `bfcol_43`,
    `bfcol_3` AS `bfcol_44`
  FROM `bfcte_8`
  INNER JOIN `bfcte_1`
    ON `bfcol_32` = `bfcol_2`
), `bfcte_10` AS (
  SELECT
    `bfcol_38`,
    `bfcol_39`,
    `bfcol_40`,
    `bfcol_41`,
    `bfcol_42`,
    `bfcol_43`,
    `bfcol_44`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_39` AS `bfcol_52`,
    `bfcol_40` AS `bfcol_53`,
    `bfcol_41` AS `bfcol_54`,
    `bfcol_42` AS `bfcol_55`,
    `bfcol_44` AS `bfcol_56`,
    `bfcol_1` AS `bfcol_57`,
    REGEXP_CONTAINS(`bfcol_38`, 'green') AS `bfcol_58`,
    `bfcol_39` AS `bfcol_72`,
    `bfcol_40` AS `bfcol_73`,
    `bfcol_41` AS `bfcol_74`,
    `bfcol_42` AS `bfcol_75`,
    `bfcol_1` AS `bfcol_76`,
    EXTRACT(YEAR FROM `bfcol_44`) AS `bfcol_77`,
    `bfcol_1` AS `bfcol_84`,
    EXTRACT(YEAR FROM `bfcol_44`) AS `bfcol_85`,
    (
      `bfcol_40` * (
        1 - `bfcol_41`
      )
    ) - (
      `bfcol_42` * `bfcol_39`
    ) AS `bfcol_86`
  FROM `bfcte_9`
  INNER JOIN `bfcte_0`
    ON `bfcol_43` = `bfcol_0`
  WHERE
    REGEXP_CONTAINS(`bfcol_38`, 'green')
), `bfcte_11` AS (
  SELECT
    `bfcol_84`,
    `bfcol_85`,
    COALESCE(SUM(`bfcol_86`), 0) AS `bfcol_90`
  FROM `bfcte_10`
  WHERE
    NOT `bfcol_85` IS NULL
  GROUP BY
    `bfcol_84`,
    `bfcol_85`
)
SELECT
  `bfcol_84` AS `NATION`,
  `bfcol_85` AS `O_YEAR`,
  ROUND(`bfcol_90`, 2) AS `SUM_PROFIT`
FROM `bfcte_11`
ORDER BY
  `bfcol_84` ASC NULLS LAST,
  `bfcol_85` DESC,
  `bfcol_84` ASC NULLS LAST,
  `bfcol_85` ASC NULLS LAST