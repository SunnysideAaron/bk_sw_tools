select lrs.rune_set_name
, lrs.rune_set_effect
, lrs.pieces_required
, count(sxr.rune_id) as 'count'
from swex_runes sxr 
left join lt_rune_set as lrs on sxr.set_id = lrs.rune_set_id
where sxr.occupied_id = 0
and sxr.upgrade_curr >= 3
group by lrs.rune_set_name
, lrs.pieces_required
order by lrs.pieces_required desc
, lrs.rune_set_name;