WITH `bfcte_0` AS (
  SELECT
    `S_SUPPKEY`,
    `S_COMMENT`,
    `S_SUPPKEY` AS `bfcol_8`,
    NOT (
      REGEXP_CONTAINS(`S_COMMENT`, 'Customer.*Complaints')
    ) AS `bfcol_9`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`SUPPLIER` AS `bft_2`
  WHERE
    NOT (
      REGEXP_CONTAINS(`S_COMMENT`, 'Customer.*Complaints')
    )
), `bfcte_1` AS (
  SELECT
    `PS_PARTKEY` AS `bfcol_2`,
    `PS_SUPPKEY` AS `bfcol_3`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PARTSUPP` AS `bft_1`
), `bfcte_2` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_4`,
    `P_BRAND` AS `bfcol_5`,
    `P_TYPE` AS `bfcol_6`,
    `P_SIZE` AS `bfcol_7`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_0`
), `bfcte_3` AS (
  SELECT
    `bfcol_8`
  FROM `bfcte_0`
  GROUP BY
    `bfcol_8`
), `bfcte_4` AS (
  SELECT
    `bfcol_5` AS `bfcol_55`,
    `bfcol_6` AS `bfcol_56`,
    `bfcol_7` AS `bfcol_57`,
    `bfcol_3` AS `bfcol_58`
  FROM `bfcte_2`
  INNER JOIN `bfcte_1`
    ON `bfcol_4` = `bfcol_2`
  WHERE
    `bfcol_5` <> 'Brand#45'
    AND NOT (
      REGEXP_CONTAINS(`bfcol_6`, 'MEDIUM POLISHED')
    )
    AND COALESCE(COALESCE(`bfcol_7` IN (49, 14, 23, 45, 19, 3, 36, 9), FALSE), FALSE)
), `bfcte_5` AS (
  SELECT
    `bfcol_8` AS `bfcol_21`
  FROM `bfcte_3`
), `bfcte_6` AS (
  SELECT
    *,
    `bfcol_58` IN ((
        SELECT
          *
        FROM `bfcte_5`
    )) AS `bfcol_59`
  FROM `bfcte_4`
), `bfcte_7` AS (
  SELECT
    *
  FROM `bfcte_6`
  WHERE
    `bfcol_59`
), `bfcte_8` AS (
  SELECT
    `bfcol_55`,
    `bfcol_56`,
    `bfcol_57`,
    COUNT(DISTINCT `bfcol_58`) AS `bfcol_69`
  FROM `bfcte_7`
  GROUP BY
    `bfcol_55`,
    `bfcol_56`,
    `bfcol_57`
)
SELECT
  `bfcol_55` AS `P_BRAND`,
  `bfcol_56` AS `P_TYPE`,
  `bfcol_57` AS `P_SIZE`,
  `bfcol_69` AS `SUPPLIER_CNT`
FROM `bfcte_8`
ORDER BY
  `bfcol_69` DESC,
  `bfcol_55` ASC NULLS LAST,
  `bfcol_56` ASC NULLS LAST,
  `bfcol_57` ASC NULLS LAST