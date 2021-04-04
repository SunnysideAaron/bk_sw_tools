select sxr.slot_no
, lre.rune_effect
, count(sxr.rune_id) as equiped_count
from swex_runes sxr 
join swex_unit_list as sxul on sxr.occupied_id = sxul.unit_id
join lt_rune_effect as lre on sxr.pri_eff_id = lre.rune_effect_id
where sxr.slot_no in (2,4,6)
group by sxr.slot_no
, lre.rune_effect
order by sxr.slot_no
, lre.rune_effect;