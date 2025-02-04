select
    c_custkey,
    c_name,
    round(sum(l_extendedprice * (1 - l_discount)), 2) as revenue,
    c_acctbal,
    n_name,
    c_address,
    c_phone,
    c_comment
from
    {customer_ds},
    {orders_ds},
    {line_item_ds},
    {nation_ds}
where
    c_custkey = o_custkey
    and l_orderkey = o_orderkey
    and o_orderdate >= date '1993-10-01'
    and o_orderdate < date '1993-10-01' + interval '3' month
    and l_returnflag = 'R'
    and c_nationkey = n_nationkey
group by
    c_custkey,
    c_name,
    c_acctbal,
    c_phone,
    n_name,
    c_address,
    c_comment
order by
    revenue desc
limit 20
