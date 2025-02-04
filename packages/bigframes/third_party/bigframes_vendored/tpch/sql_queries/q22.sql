select
    cntrycode,
    count(*) as numcust,
    sum(c_acctbal) as totacctbal
from (
    select
        SUBSTR(c_phone, 1, 2) AS cntrycode,
        c_acctbal
    from
        {customer_ds}
    where
        SUBSTR(c_phone, 1, 2) in
            ('13', '31', '23', '29', '30', '18', '17')
        and c_acctbal > (
            select
                avg(c_acctbal)
            from
                {customer_ds}
            where
                c_acctbal > 0.00
                and SUBSTR(c_phone, 1, 2) in
                    ('13', '31', '23', '29', '30', '18', '17')
        )
        and not exists (
            select
                *
            from
                {orders_ds}
            where
                o_custkey = c_custkey
        )
    ) as custsale
group by
    cntrycode
order by
    cntrycode
