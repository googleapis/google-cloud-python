WITH `bfcte_0` AS (
  SELECT
    `R_REGIONKEY` AS `bfcol_0`,
    `R_NAME` AS `bfcol_1`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`REGION` AS `bft_4`
), `bfcte_1` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_2`,
    `N_NAME` AS `bfcol_3`,
    `N_REGIONKEY` AS `bfcol_4`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_3`
), `bfcte_2` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_19`,
    `N_REGIONKEY` AS `bfcol_20`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_3`
), `bfcte_3` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_5`,
    `S_NAME` AS `bfcol_6`,
    `S_ADDRESS` AS `bfcol_7`,
    `S_NATIONKEY` AS `bfcol_8`,
    `S_PHONE` AS `bfcol_9`,
    `S_ACCTBAL` AS `bfcol_10`,
    `S_COMMENT` AS `bfcol_11`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_2`
), `bfcte_4` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_21`,
    `S_NATIONKEY` AS `bfcol_22`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_2`
), `bfcte_5` AS (
  SELECT
    `PS_PARTKEY` AS `bfcol_12`,
    `PS_SUPPKEY` AS `bfcol_13`,
    `PS_SUPPLYCOST` AS `bfcol_14`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PARTSUPP` AS `bft_1`
), `bfcte_6` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_15`,
    `P_MFGR` AS `bfcol_16`,
    `P_TYPE` AS `bfcol_17`,
    `P_SIZE` AS `bfcol_18`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_0`
), `bfcte_7` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_23`,
    `P_TYPE` AS `bfcol_24`,
    `P_SIZE` AS `bfcol_25`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_0`
), `bfcte_8` AS (
  SELECT
    `bfcol_15` AS `bfcol_26`,
    `bfcol_16` AS `bfcol_27`,
    `bfcol_17` AS `bfcol_28`,
    `bfcol_18` AS `bfcol_29`,
    `bfcol_13` AS `bfcol_30`,
    `bfcol_14` AS `bfcol_31`
  FROM `bfcte_6`
  INNER JOIN `bfcte_5`
    ON `bfcol_15` = `bfcol_12`
), `bfcte_9` AS (
  SELECT
    `bfcol_23` AS `bfcol_32`,
    `bfcol_24` AS `bfcol_33`,
    `bfcol_25` AS `bfcol_34`,
    `bfcol_13` AS `bfcol_35`,
    `bfcol_14` AS `bfcol_36`
  FROM `bfcte_7`
  INNER JOIN `bfcte_5`
    ON `bfcol_23` = `bfcol_12`
), `bfcte_10` AS (
  SELECT
    `bfcol_26` AS `bfcol_37`,
    `bfcol_27` AS `bfcol_38`,
    `bfcol_28` AS `bfcol_39`,
    `bfcol_29` AS `bfcol_40`,
    `bfcol_31` AS `bfcol_41`,
    `bfcol_6` AS `bfcol_42`,
    `bfcol_7` AS `bfcol_43`,
    `bfcol_8` AS `bfcol_44`,
    `bfcol_9` AS `bfcol_45`,
    `bfcol_10` AS `bfcol_46`,
    `bfcol_11` AS `bfcol_47`
  FROM `bfcte_8`
  INNER JOIN `bfcte_3`
    ON `bfcol_30` = `bfcol_5`
), `bfcte_11` AS (
  SELECT
    `bfcol_32` AS `bfcol_48`,
    `bfcol_33` AS `bfcol_49`,
    `bfcol_34` AS `bfcol_50`,
    `bfcol_36` AS `bfcol_51`,
    `bfcol_22` AS `bfcol_52`
  FROM `bfcte_9`
  INNER JOIN `bfcte_4`
    ON `bfcol_35` = `bfcol_21`
), `bfcte_12` AS (
  SELECT
    `bfcol_37` AS `bfcol_53`,
    `bfcol_38` AS `bfcol_54`,
    `bfcol_39` AS `bfcol_55`,
    `bfcol_40` AS `bfcol_56`,
    `bfcol_41` AS `bfcol_57`,
    `bfcol_42` AS `bfcol_58`,
    `bfcol_43` AS `bfcol_59`,
    `bfcol_45` AS `bfcol_60`,
    `bfcol_46` AS `bfcol_61`,
    `bfcol_47` AS `bfcol_62`,
    `bfcol_3` AS `bfcol_63`,
    `bfcol_4` AS `bfcol_64`
  FROM `bfcte_10`
  INNER JOIN `bfcte_1`
    ON `bfcol_44` = `bfcol_2`
), `bfcte_13` AS (
  SELECT
    `bfcol_48` AS `bfcol_65`,
    `bfcol_49` AS `bfcol_66`,
    `bfcol_50` AS `bfcol_67`,
    `bfcol_51` AS `bfcol_68`,
    `bfcol_20` AS `bfcol_69`
  FROM `bfcte_11`
  INNER JOIN `bfcte_2`
    ON `bfcol_52` = `bfcol_19`
), `bfcte_14` AS (
  SELECT
    `bfcol_53` AS `bfcol_205`,
    `bfcol_54` AS `bfcol_206`,
    `bfcol_57` AS `bfcol_207`,
    `bfcol_58` AS `bfcol_208`,
    `bfcol_59` AS `bfcol_209`,
    `bfcol_60` AS `bfcol_210`,
    `bfcol_61` AS `bfcol_211`,
    `bfcol_62` AS `bfcol_212`,
    `bfcol_63` AS `bfcol_213`
  FROM `bfcte_12`
  INNER JOIN `bfcte_0`
    ON `bfcol_64` = `bfcol_0`
  WHERE
    `bfcol_56` = 15 AND ENDS_WITH(`bfcol_55`, 'BRASS') AND `bfcol_1` = 'EUROPE'
), `bfcte_15` AS (
  SELECT
    `bfcol_65`,
    `bfcol_66`,
    `bfcol_67`,
    `bfcol_68`,
    `bfcol_69`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_65` AS `bfcol_99`,
    `bfcol_66` AS `bfcol_100`,
    `bfcol_68` AS `bfcol_101`,
    `bfcol_1` AS `bfcol_102`,
    `bfcol_67` = 15 AS `bfcol_103`,
    `bfcol_65` AS `bfcol_147`,
    `bfcol_68` AS `bfcol_148`,
    `bfcol_1` AS `bfcol_149`,
    ENDS_WITH(`bfcol_66`, 'BRASS') AS `bfcol_150`,
    `bfcol_65` AS `bfcol_189`,
    `bfcol_68` AS `bfcol_190`,
    `bfcol_1` = 'EUROPE' AS `bfcol_191`
  FROM `bfcte_13`
  INNER JOIN `bfcte_0`
    ON `bfcol_69` = `bfcol_0`
  WHERE
    `bfcol_67` = 15 AND ENDS_WITH(`bfcol_66`, 'BRASS') AND `bfcol_1` = 'EUROPE'
), `bfcte_16` AS (
  SELECT
    `bfcol_189`,
    MIN(`bfcol_190`) AS `bfcol_216`
  FROM `bfcte_15`
  GROUP BY
    `bfcol_189`
), `bfcte_17` AS (
  SELECT
    `bfcol_189` AS `bfcol_214`,
    `bfcol_216`
  FROM `bfcte_16`
)
SELECT
  `bfcol_211` AS `S_ACCTBAL`,
  `bfcol_208` AS `S_NAME`,
  `bfcol_213` AS `N_NAME`,
  `bfcol_214` AS `P_PARTKEY`,
  `bfcol_206` AS `P_MFGR`,
  `bfcol_209` AS `S_ADDRESS`,
  `bfcol_210` AS `S_PHONE`,
  `bfcol_212` AS `S_COMMENT`
FROM `bfcte_17`
INNER JOIN `bfcte_14`
  ON `bfcol_214` = `bfcol_205` AND `bfcol_216` = `bfcol_207`
ORDER BY
  `bfcol_211` DESC,
  `bfcol_213` ASC NULLS LAST,
  `bfcol_208` ASC NULLS LAST,
  `bfcol_214` ASC NULLS LAST
LIMIT 100