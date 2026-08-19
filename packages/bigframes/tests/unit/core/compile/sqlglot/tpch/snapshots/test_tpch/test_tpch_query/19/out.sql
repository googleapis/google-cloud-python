WITH `bfcte_0` AS (
  SELECT
    *
  FROM UNNEST(ARRAY<STRUCT<`bfcol_0` INT64>>[STRUCT(0)])
), `bfcte_1` AS (
  SELECT
    `L_PARTKEY` AS `bfcol_1`,
    `L_QUANTITY` AS `bfcol_2`,
    `L_EXTENDEDPRICE` AS `bfcol_3`,
    `L_DISCOUNT` AS `bfcol_4`,
    `L_SHIPINSTRUCT` AS `bfcol_5`,
    `L_SHIPMODE` AS `bfcol_6`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`LINEITEM` AS `bft_1`
), `bfcte_2` AS (
  SELECT
    `P_PARTKEY` AS `bfcol_7`,
    `P_BRAND` AS `bfcol_8`,
    `P_SIZE` AS `bfcol_9`,
    `P_CONTAINER` AS `bfcol_10`
  FROM `bigframes-dev-perf`.`tpch_0001t`.`PART` AS `bft_0`
), `bfcte_3` AS (
  SELECT
    `bfcol_7`,
    `bfcol_8`,
    `bfcol_9`,
    `bfcol_10`,
    `bfcol_1`,
    `bfcol_2`,
    `bfcol_3`,
    `bfcol_4`,
    `bfcol_5`,
    `bfcol_6`,
    `bfcol_3` AS `bfcol_19`,
    `bfcol_4` AS `bfcol_20`,
    (
      COALESCE(COALESCE(`bfcol_6` IN ('AIR', 'AIR REG'), FALSE), FALSE)
      AND (
        `bfcol_5` = 'DELIVER IN PERSON'
      )
    )
    AND (
      (
        (
          (
            (
              (
                `bfcol_8` = 'Brand#12'
              )
              AND COALESCE(COALESCE(`bfcol_10` IN ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG'), FALSE), FALSE)
            )
            AND (
              (
                `bfcol_2` >= 1
              ) AND (
                `bfcol_2` <= 11
              )
            )
          )
          AND (
            (
              `bfcol_9` >= 1
            ) AND (
              `bfcol_9` <= 5
            )
          )
        )
        OR (
          (
            (
              (
                `bfcol_8` = 'Brand#23'
              )
              AND COALESCE(
                COALESCE(`bfcol_10` IN ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK'), FALSE),
                FALSE
              )
            )
            AND (
              (
                `bfcol_2` >= 10
              ) AND (
                `bfcol_2` <= 20
              )
            )
          )
          AND (
            (
              `bfcol_9` >= 1
            ) AND (
              `bfcol_9` <= 10
            )
          )
        )
      )
      OR (
        (
          (
            (
              `bfcol_8` = 'Brand#34'
            )
            AND COALESCE(COALESCE(`bfcol_10` IN ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG'), FALSE), FALSE)
          )
          AND (
            (
              `bfcol_2` >= 20
            ) AND (
              `bfcol_2` <= 30
            )
          )
        )
        AND (
          (
            `bfcol_9` >= 1
          ) AND (
            `bfcol_9` <= 15
          )
        )
      )
    ) AS `bfcol_21`,
    `bfcol_3` AS `bfcol_27`,
    1 - `bfcol_4` AS `bfcol_28`,
    `bfcol_3` * (
      1 - `bfcol_4`
    ) AS `bfcol_31`
  FROM `bfcte_2`
  INNER JOIN `bfcte_1`
    ON `bfcol_7` = `bfcol_1`
  WHERE
    (
      COALESCE(COALESCE(`bfcol_6` IN ('AIR', 'AIR REG'), FALSE), FALSE)
      AND (
        `bfcol_5` = 'DELIVER IN PERSON'
      )
    )
    AND (
      (
        (
          (
            (
              (
                `bfcol_8` = 'Brand#12'
              )
              AND COALESCE(COALESCE(`bfcol_10` IN ('SM CASE', 'SM BOX', 'SM PACK', 'SM PKG'), FALSE), FALSE)
            )
            AND (
              (
                `bfcol_2` >= 1
              ) AND (
                `bfcol_2` <= 11
              )
            )
          )
          AND (
            (
              `bfcol_9` >= 1
            ) AND (
              `bfcol_9` <= 5
            )
          )
        )
        OR (
          (
            (
              (
                `bfcol_8` = 'Brand#23'
              )
              AND COALESCE(
                COALESCE(`bfcol_10` IN ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK'), FALSE),
                FALSE
              )
            )
            AND (
              (
                `bfcol_2` >= 10
              ) AND (
                `bfcol_2` <= 20
              )
            )
          )
          AND (
            (
              `bfcol_9` >= 1
            ) AND (
              `bfcol_9` <= 10
            )
          )
        )
      )
      OR (
        (
          (
            (
              `bfcol_8` = 'Brand#34'
            )
            AND COALESCE(COALESCE(`bfcol_10` IN ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG'), FALSE), FALSE)
          )
          AND (
            (
              `bfcol_2` >= 20
            ) AND (
              `bfcol_2` <= 30
            )
          )
        )
        AND (
          (
            `bfcol_9` >= 1
          ) AND (
            `bfcol_9` <= 15
          )
        )
      )
    )
), `bfcte_4` AS (
  SELECT
    COALESCE(SUM(`bfcol_31`), 0) AS `bfcol_33`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *
  FROM `bfcte_4`
)
SELECT
  CASE WHEN `bfcol_0` = 0 THEN `bfcol_33` END AS `REVENUE`
FROM `bfcte_5`
CROSS JOIN `bfcte_0`