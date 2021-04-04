select tl.name
, tlu.rank
, tlr.description
, tlu.com2us_id
, mn.full_name
, mn.natural_stars
, mu.max_unit_level
from s_tier_list tl
left join s_tier_list_units tlu on tlu.tier_list_id = tl.tier_list_id
left join s_tier_list_ranks tlr on tlr.rank = tlu.rank
left join swarfarm_monster_names mn on tlu.com2us_id = mn.com2us_id
left join (
     select m.com2us_id
    , m2.com2us_id as com2us_id_awakened
    , m3.com2us_id as com2us_id_2a
    , max(ul.unit_level) as max_unit_level
     from swarfarm_monsters m
     left join swarfarm_monsters m2 on m.awakens_to = m2.id
     left join swarfarm_monsters m3 on m2.awakens_to = m3.id
     left join swex_unit_list ul on ul.com2us_id = m.com2us_id
       or ul.com2us_id = m2.com2us_id
       or ul.com2us_id = m3.com2us_id
     where m.obtainable = 1
     and m.natural_stars > 1
     and m.awaken_level = 0
     and m.can_awaken = 1
     group by m.com2us_id
    , m2.com2us_id
    , m3.com2us_id
    ) as mu on tlu.com2us_id = mu.com2us_id
    or tlu.com2us_id = mu.com2us_id_awakened
    or tlu.com2us_id = mu.com2us_id_2a
group by tl.name
, tlu.rank
, tlr.description
, tlu.com2us_id
, mn.full_name
, mn.natural_stars
order by tl.name
, tlr.sort_order
, mn.full_name