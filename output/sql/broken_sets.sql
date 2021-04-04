select sfmn.full_name
, lrs.rune_set_name
, lrs.rune_set_effect
, lrs.pieces_required
, count(sxr.rune_id) as 'count'
from swex_runes sxr 
join swex_unit_list as sxul on sxr.occupied_id = sxul.unit_id
left join swarfarm_monster_names as sfmn on sxul.com2us_id = sfmn.com2us_id 
left join lt_rune_set as lrs on sxr.set_id = lrs.rune_set_id
where sxul.class >= 5
and sxr.upgrade_curr >= 3
group by sfmn.full_name
, lrs.rune_set_name
, lrs.rune_set_effect
, lrs.pieces_required
having count(sxr.rune_id) < lrs.pieces_required
order by sfmn.full_name
, lrs.rune_set_name;