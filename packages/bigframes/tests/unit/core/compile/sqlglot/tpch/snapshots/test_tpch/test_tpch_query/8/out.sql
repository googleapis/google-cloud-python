WITH `bfcte_0` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_0`,
    `N_NAME` AS `bfcol_1`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_6` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_1` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_4`,
    `N_REGIONKEY` AS `bfcol_5`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_6` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_2` AS (
  SELECT
    `R_REGIONKEY` AS `bfcol_2`,
    `R_NAME` AS `bfcol_3`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`REGION` AS `bft_5` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_3` AS (
  SELECT
    `C_CUSTKEY` AS `bfcol_6`,
    `C_NATIONKEY` AS `bfcol_7`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`CUSTOMER` AS `bft_4` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_4` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_8`,
    `O_CUSTKEY` AS `bfcol_9`,
    `O_ORDERDATE` AS `bfcol_10`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_3` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_5` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_11`,
    `S_NATIONKEY` AS `bfcol_12`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_2` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_6` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_13`,
    `L_PARTKEY` AS `bfcol_14`,
    `L_SUPPKEY` AS `bfcol_15`,
    `L_EXTENDEDPRICE` AS `bfcol_16`,
    `L_DISCOUNT` AS `bfcol_17`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_1` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_7` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_18`,
    `P_TYPE` AS `bfcol_19`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_0` FOR SYSTEM_TIME AS OF '2026-04-05T18:00:00'
), `bfcte_8` AS (
  SELECT
    `bfcol_19` AS `bfcol_20`,
    `bfcol_13` AS `bfcol_21`,
    `bfcol_15` AS `bfcol_22`,
    `bfcol_16` AS `bfcol_23`,
    `bfcol_17` AS `bfcol_24`
  FROM `bfcte_7`
  INNER JOIN `bfcte_6`
    ON `bfcol_18` = `bfcol_14`
), `bfcte_9` AS (
  SELECT
    `bfcol_20` AS `bfcol_25`,
    `bfcol_21` AS `bfcol_26`,
    `bfcol_23` AS `bfcol_27`,
    `bfcol_24` AS `bfcol_28`,
    `bfcol_12` AS `bfcol_29`
  FROM `bfcte_8`
  INNER JOIN `bfcte_5`
    ON `bfcol_22` = `bfcol_11`
), `bfcte_10` AS (
  SELECT
    `bfcol_25` AS `bfcol_30`,
    `bfcol_27` AS `bfcol_31`,
    `bfcol_28` AS `bfcol_32`,
    `bfcol_29` AS `bfcol_33`,
    `bfcol_9` AS `bfcol_34`,
    `bfcol_10` AS `bfcol_35`
  FROM `bfcte_9`
  INNER JOIN `bfcte_4`
    ON `bfcol_26` = `bfcol_8`
), `bfcte_11` AS (
  SELECT
    `bfcol_30` AS `bfcol_36`,
    `bfcol_31` AS `bfcol_37`,
    `bfcol_32` AS `bfcol_38`,
    `bfcol_33` AS `bfcol_39`,
    `bfcol_35` AS `bfcol_40`,
    `bfcol_7` AS `bfcol_41`
  FROM `bfcte_10`
  INNER JOIN `bfcte_3`
    ON `bfcol_34` = `bfcol_6`
), `bfcte_12` AS (
  SELECT
    `bfcol_36` AS `bfcol_42`,
    `bfcol_37` AS `bfcol_43`,
    `bfcol_38` AS `bfcol_44`,
    `bfcol_39` AS `bfcol_45`,
    `bfcol_40` AS `bfcol_46`,
    `bfcol_5` AS `bfcol_47`
  FROM `bfcte_11`
  INNER JOIN `bfcte_1`
    ON `bfcol_41` = `bfcol_4`
), `bfcte_13` AS (
  SELECT
    `bfcol_42` AS `bfcol_66`,
    `bfcol_43` AS `bfcol_67`,
    `bfcol_44` AS `bfcol_68`,
    `bfcol_45` AS `bfcol_69`,
    `bfcol_46` AS `bfcol_70`
  FROM `bfcte_12`
  INNER JOIN `bfcte_2`
    ON `bfcol_47` = `bfcol_2`
  WHERE
    `bfcol_3` = 'AMERICA'
), `bfcte_14` AS (
  SELECT
    `bfcol_66`,
    `bfcol_67`,
    `bfcol_68`,
    `bfcol_69`,
    `bfcol_70`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_66` AS `bfcol_76`,
    `bfcol_67` AS `bfcol_77`,
    `bfcol_68` AS `bfcol_78`,
    `bfcol_70` AS `bfcol_79`,
    `bfcol_1` AS `bfcol_80`,
    (
      `bfcol_70` >= CAST('1995-01-01' AS DATE)
    )
    AND (
      `bfcol_70` <= CAST('1996-12-31' AS DATE)
    ) AS `bfcol_81`,
    `bfcol_67` AS `bfcol_93`,
    `bfcol_68` AS `bfcol_94`,
    `bfcol_70` AS `bfcol_95`,
    `bfcol_1` AS `bfcol_96`,
    `bfcol_66` = 'ECONOMY ANODIZED STEEL' AS `bfcol_97`,
    `bfcol_67` AS `bfcol_107`,
    `bfcol_68` AS `bfcol_108`,
    `bfcol_1` AS `bfcol_109`,
    EXTRACT(YEAR FROM `bfcol_70`) AS `bfcol_110`,
    `bfcol_1` AS `bfcol_115`,
    EXTRACT(YEAR FROM `bfcol_70`) AS `bfcol_116`,
    `bfcol_67` * (
      1.0 - `bfcol_68`
    ) AS `bfcol_117`,
    EXTRACT(YEAR FROM `bfcol_70`) AS `bfcol_121`,
    `bfcol_67` * (
      1.0 - `bfcol_68`
    ) AS `bfcol_122`,
    IF(`bfcol_1` = 'BRAZIL', `bfcol_67` * (
      1.0 - `bfcol_68`
    ), 0) AS `bfcol_123`,
    EXTRACT(YEAR FROM `bfcol_70`) AS `bfcol_127`,
    IF(`bfcol_1` = 'BRAZIL', `bfcol_67` * (
      1.0 - `bfcol_68`
    ), 0) AS `bfcol_128`,
    `bfcol_67` * (
      1.0 - `bfcol_68`
    ) AS `bfcol_129`
  FROM `bfcte_13`
  INNER JOIN `bfcte_0`
    ON `bfcol_69` = `bfcol_0`
  WHERE
    (
      `bfcol_70` >= CAST('1995-01-01' AS DATE)
    )
    AND (
      `bfcol_70` <= CAST('1996-12-31' AS DATE)
    )
    AND `bfcol_66` = 'ECONOMY ANODIZED STEEL'
), `bfcte_15` AS (
  SELECT
    `bfcol_127`,
    COALESCE(SUM(`bfcol_128`), 0) AS `bfcol_133`,
    COALESCE(SUM(`bfcol_129`), 0) AS `bfcol_134`
  FROM `bfcte_14`
  WHERE
    NOT `bfcol_127` IS NULL
  GROUP BY
    `bfcol_127`
)
SELECT
  `bfcol_127` AS `O_YEAR`,
  ROUND(IEEE_DIVIDE(`bfcol_133`, `bfcol_134`), 2) AS `MKT_SHARE`
FROM `bfcte_15`
ORDER BY
  `bfcol_127` ASC NULLS LAST,
  `bfcol_127` ASC NULLS LAST