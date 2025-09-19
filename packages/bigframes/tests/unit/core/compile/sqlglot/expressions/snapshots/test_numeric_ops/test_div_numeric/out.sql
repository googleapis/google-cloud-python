WITH `bfcte_0` AS (
  SELECT
    `bool_col` AS `bfcol_0`,
    `int64_col` AS `bfcol_1`,
    `float64_col` AS `bfcol_2`,
    `rowindex` AS `bfcol_3`
  FROM `bigframes-dev`.`sqlglot_test`.`scalar_types`
), `bfcte_1` AS (
  SELECT
    *,
    `bfcol_3` AS `bfcol_8`,
    `bfcol_1` AS `bfcol_9`,
    `bfcol_0` AS `bfcol_10`,
    `bfcol_2` AS `bfcol_11`,
    IEEE_DIVIDE(`bfcol_1`, `bfcol_1`) AS `bfcol_12`
  FROM `bfcte_0`
), `bfcte_2` AS (
  SELECT
    *,
    `bfcol_8` AS `bfcol_18`,
    `bfcol_9` AS `bfcol_19`,
    `bfcol_10` AS `bfcol_20`,
    `bfcol_11` AS `bfcol_21`,
    `bfcol_12` AS `bfcol_22`,
    IEEE_DIVIDE(`bfcol_9`, 1) AS `bfcol_23`
  FROM `bfcte_1`
), `bfcte_3` AS (
  SELECT
    *,
    `bfcol_18` AS `bfcol_30`,
    `bfcol_19` AS `bfcol_31`,
    `bfcol_20` AS `bfcol_32`,
    `bfcol_21` AS `bfcol_33`,
    `bfcol_22` AS `bfcol_34`,
    `bfcol_23` AS `bfcol_35`,
    IEEE_DIVIDE(`bfcol_19`, 0.0) AS `bfcol_36`
  FROM `bfcte_2`
), `bfcte_4` AS (
  SELECT
    *,
    `bfcol_30` AS `bfcol_44`,
    `bfcol_31` AS `bfcol_45`,
    `bfcol_32` AS `bfcol_46`,
    `bfcol_33` AS `bfcol_47`,
    `bfcol_34` AS `bfcol_48`,
    `bfcol_35` AS `bfcol_49`,
    `bfcol_36` AS `bfcol_50`,
    IEEE_DIVIDE(`bfcol_31`, `bfcol_33`) AS `bfcol_51`
  FROM `bfcte_3`
), `bfcte_5` AS (
  SELECT
    *,
    `bfcol_44` AS `bfcol_60`,
    `bfcol_45` AS `bfcol_61`,
    `bfcol_46` AS `bfcol_62`,
    `bfcol_47` AS `bfcol_63`,
    `bfcol_48` AS `bfcol_64`,
    `bfcol_49` AS `bfcol_65`,
    `bfcol_50` AS `bfcol_66`,
    `bfcol_51` AS `bfcol_67`,
    IEEE_DIVIDE(`bfcol_47`, `bfcol_45`) AS `bfcol_68`
  FROM `bfcte_4`
), `bfcte_6` AS (
  SELECT
    *,
    `bfcol_60` AS `bfcol_78`,
    `bfcol_61` AS `bfcol_79`,
    `bfcol_62` AS `bfcol_80`,
    `bfcol_63` AS `bfcol_81`,
    `bfcol_64` AS `bfcol_82`,
    `bfcol_65` AS `bfcol_83`,
    `bfcol_66` AS `bfcol_84`,
    `bfcol_67` AS `bfcol_85`,
    `bfcol_68` AS `bfcol_86`,
    IEEE_DIVIDE(`bfcol_63`, 0.0) AS `bfcol_87`
  FROM `bfcte_5`
), `bfcte_7` AS (
  SELECT
    *,
    `bfcol_78` AS `bfcol_98`,
    `bfcol_79` AS `bfcol_99`,
    `bfcol_80` AS `bfcol_100`,
    `bfcol_81` AS `bfcol_101`,
    `bfcol_82` AS `bfcol_102`,
    `bfcol_83` AS `bfcol_103`,
    `bfcol_84` AS `bfcol_104`,
    `bfcol_85` AS `bfcol_105`,
    `bfcol_86` AS `bfcol_106`,
    `bfcol_87` AS `bfcol_107`,
    IEEE_DIVIDE(`bfcol_79`, CAST(`bfcol_80` AS INT64)) AS `bfcol_108`
  FROM `bfcte_6`
), `bfcte_8` AS (
  SELECT
    *,
    `bfcol_98` AS `bfcol_120`,
    `bfcol_99` AS `bfcol_121`,
    `bfcol_100` AS `bfcol_122`,
    `bfcol_101` AS `bfcol_123`,
    `bfcol_102` AS `bfcol_124`,
    `bfcol_103` AS `bfcol_125`,
    `bfcol_104` AS `bfcol_126`,
    `bfcol_105` AS `bfcol_127`,
    `bfcol_106` AS `bfcol_128`,
    `bfcol_107` AS `bfcol_129`,
    `bfcol_108` AS `bfcol_130`,
    IEEE_DIVIDE(CAST(`bfcol_100` AS INT64), `bfcol_99`) AS `bfcol_131`
  FROM `bfcte_7`
)
SELECT
  `bfcol_120` AS `rowindex`,
  `bfcol_121` AS `int64_col`,
  `bfcol_122` AS `bool_col`,
  `bfcol_123` AS `float64_col`,
  `bfcol_124` AS `int_div_int`,
  `bfcol_125` AS `int_div_1`,
  `bfcol_126` AS `int_div_0`,
  `bfcol_127` AS `int_div_float`,
  `bfcol_128` AS `float_div_int`,
  `bfcol_129` AS `float_div_0`,
  `bfcol_130` AS `int_div_bool`,
  `bfcol_131` AS `bool_div_int`
FROM `bfcte_8`