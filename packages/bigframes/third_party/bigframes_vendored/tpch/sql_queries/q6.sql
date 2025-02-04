select
    sum(l_extendedprice * l_discount) as revenue
from
    {line_item_ds}
where
    l_shipdate >= date '1994-01-01'
    and l_shipdate < date '1994-01-01' + interval '1' year
    and l_discount between .05 and .07
    and l_quantity < 24
