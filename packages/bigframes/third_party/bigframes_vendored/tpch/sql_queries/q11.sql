select
    ps_partkey,
    round(sum(ps_supplycost * ps_availqty), 2) as value
from
    {part_supp_ds},
    {supplier_ds},
    {nation_ds}
where
    ps_suppkey = s_suppkey
    and s_nationkey = n_nationkey
    and n_name = 'GERMANY'
group by
    ps_partkey having
            sum(ps_supplycost * ps_availqty) > (
        select
            sum(ps_supplycost * ps_availqty) * 0.0001
        from
            {part_supp_ds},
            {supplier_ds},
            {nation_ds}
        where
            ps_suppkey = s_suppkey
            and s_nationkey = n_nationkey
            and n_name = 'GERMANY'
        )
    order by
        value desc
