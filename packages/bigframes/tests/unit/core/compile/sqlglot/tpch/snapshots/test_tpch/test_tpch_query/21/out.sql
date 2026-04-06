WITH `bfcte_0` AS (
  SELECT
    `O_ORDERKEY` AS `bfcol_0`,
    `O_ORDERSTATUS` AS `bfcol_1`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`ORDERS` AS `bft_3`
), `bfcte_1` AS (
  SELECT
    `N_NATIONKEY` AS `bfcol_2`,
    `N_NAME` AS `bfcol_3`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`NATION` AS `bft_2`
), `bfcte_2` AS (
  SELECT
    `S_SUPPKEY` AS `bfcol_4`,
    `S_NAME` AS `bfcol_5`,
    `S_NATIONKEY` AS `bfcol_6`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_1`
), `bfcte_3` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_30`,
    `L_SUPPKEY` AS `bfcol_31`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_0`
  WHERE
    `L_RECEIPTDATE` > `L_COMMITDATE`
), `bfcte_4` AS (
  SELECT
    `L_ORDERKEY`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_0`
), `bfcte_5` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_32`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_0`
  WHERE
    `L_RECEIPTDATE` > `L_COMMITDATE`
), `bfcte_6` AS (
  SELECT
    `L_ORDERKEY`,
    COUNT(1) AS `bfcol_18`
  FROM `bfcte_4`
  GROUP BY
    `L_ORDERKEY`
), `bfcte_7` AS (
  SELECT
    `L_ORDERKEY` AS `bfcol_33`
  FROM `bfcte_6`
  WHERE
    `bfcol_18` > 1
), `bfcte_8` AS (
  SELECT
    `bfcol_33` AS `bfcol_34`,
    `bfcol_31` AS `bfcol_35`
  FROM `bfcte_7`
  INNER JOIN `bfcte_3`
    ON `bfcol_33` = `bfcol_30`
), `bfcte_9` AS (
  SELECT
    `bfcol_33`,
    COUNT(1) AS `bfcol_37`
  FROM `bfcte_7`
  INNER JOIN `bfcte_5`
    ON `bfcol_33` = `bfcol_32`
  GROUP BY
    `bfcol_33`
), `bfcte_10` AS (
  SELECT
    `bfcol_33` AS `bfcol_36`,
    `bfcol_37`
  FROM `bfcte_9`
), `bfcte_11` AS (
  SELECT
    `bfcol_36` AS `bfcol_38`,
    `bfcol_37` AS `bfcol_39`,
    `bfcol_35` AS `bfcol_40`
  FROM `bfcte_10`
  INNER JOIN `bfcte_8`
    ON `bfcol_36` = `bfcol_34`
), `bfcte_12` AS (
  SELECT
    `bfcol_38` AS `bfcol_41`,
    `bfcol_39` AS `bfcol_42`,
    `bfcol_5` AS `bfcol_43`,
    `bfcol_6` AS `bfcol_44`
  FROM `bfcte_11`
  INNER JOIN `bfcte_2`
    ON `bfcol_40` = `bfcol_4`
), `bfcte_13` AS (
  SELECT
    `bfcol_41` AS `bfcol_45`,
    `bfcol_42` AS `bfcol_46`,
    `bfcol_43` AS `bfcol_47`,
    `bfcol_3` AS `bfcol_48`
  FROM `bfcte_12`
  INNER JOIN `bfcte_1`
    ON `bfcol_44` = `bfcol_2`
), `bfcte_14` AS (
  SELECT
    `bfcol_45`,
    `bfcol_46`,
    `bfcol_47`,
    `bfcol_48`,
    `bfcol_0`,
    `bfcol_1`,
    `bfcol_47` AS `bfcol_53`,
    (
      (
        `bfcol_46` = 1
      ) AND (
        `bfcol_48` = 'SAUDI ARABIA'
      )
    )
    AND (
      `bfcol_1` = 'F'
    ) AS `bfcol_54`
  FROM `bfcte_13`
  INNER JOIN `bfcte_0`
    ON `bfcol_45` = `bfcol_0`
  WHERE
    (
      (
        `bfcol_46` = 1
      ) AND (
        `bfcol_48` = 'SAUDI ARABIA'
      )
    )
    AND (
      `bfcol_1` = 'F'
    )
), `bfcte_15` AS (
  SELECT
    `bfcol_53`,
    COUNT(1) AS `bfcol_58`
  FROM `bfcte_14`
  GROUP BY
    `bfcol_53`
)
SELECT
  `bfcol_53` AS `S_NAME`,
  `bfcol_58` AS `NUMWAIT`
FROM `bfcte_15`
ORDER BY
  `bfcol_58` DESC,
  `bfcol_53` ASC NULLS LAST
LIMIT 100