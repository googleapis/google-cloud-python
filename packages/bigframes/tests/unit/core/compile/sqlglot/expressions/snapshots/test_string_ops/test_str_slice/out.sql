SELECT
  SUBSTRING(`string_col`, 2, 2) AS `1_3`,
  SUBSTRING(`string_col`, 1, 3) AS `none_3`,
  SUBSTRING(`string_col`, 2) AS `1_none`,
  SUBSTRING(`string_col`, -3) AS `m3_none`,
  SUBSTRING(`string_col`, 1, GREATEST(0, LENGTH(`string_col`) + -3)) AS `none_m3`,
  SUBSTRING(
    `string_col`,
    GREATEST(1, LENGTH(`string_col`) + -4),
    GREATEST(0, LENGTH(`string_col`) + -3) - GREATEST(0, LENGTH(`string_col`) + -5)
  ) AS `m5_m3`,
  SUBSTRING(`string_col`, 2, GREATEST(0, LENGTH(`string_col`) + -4)) AS `1_m3`,
  SUBSTRING(
    `string_col`,
    GREATEST(1, LENGTH(`string_col`) + -2),
    5 - GREATEST(0, LENGTH(`string_col`) + -3)
  ) AS `m3_5`
FROM `bigframes-dev`.`sqlglot_test`.`scalar_types` AS `bft_0`