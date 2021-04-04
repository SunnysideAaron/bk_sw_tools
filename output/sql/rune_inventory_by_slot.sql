select sxr.slot_no
, count(sxr.rune_id) as 'count'
from swex_runes sxr 
where sxr.occupied_id = 0
and sxr.upgrade_curr >= 3
group by sxr.slot_no
order by sxr.slot_no;