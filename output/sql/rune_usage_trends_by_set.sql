select lrs.rune_set_name
, lrs.rune_set_effect
, lrs.pieces_required
, count(sxr.rune_id) as equipped_count
from swex_runes sxr 
join swex_unit_list as sxul on sxr.occupied_id = sxul.unit_id
left join lt_rune_set as lrs on sxr.set_id = lrs.rune_set_id
where sxul.class >= 5
and sxr.upgrade_curr >= 3
group by lrs.rune_set_name
, lrs.pieces_required
order by lrs.pieces_required desc
, lrs.rune_set_name;