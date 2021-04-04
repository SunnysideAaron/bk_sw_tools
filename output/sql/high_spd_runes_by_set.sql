select *
from 
(select rs.rune_set_name
, rs.pieces_required
, sxr.slot_no
, case
	when sxr.sec_eff_1_id = 8 then sxr.sec_eff_1_value
	when sxr.sec_eff_2_id = 8 then sxr.sec_eff_2_value
	when sxr.sec_eff_3_id = 8 then sxr.sec_eff_3_value
	when sxr.sec_eff_4_id = 8 then sxr.sec_eff_4_value
	else 0
  end as spd
, case
	when sxr.sec_eff_1_id = 8 then sec_eff_1_grind
	when sxr.sec_eff_2_id = 8 then sec_eff_2_grind
	when sxr.sec_eff_3_id = 8 then sec_eff_3_grind
	when sxr.sec_eff_4_id = 8 then sec_eff_4_grind
	else 0
  end as spd_grind 
, mn.full_name  
from swex_runes sxr
left join lt_rune_set rs on sxr.set_id = rs.rune_set_id
left join swex_unit_list ul on sxr.occupied_id = ul.unit_id
left join swarfarm_monster_names mn on ul.com2us_id = mn.com2us_id
) as r
where spd >= 15
order by r.pieces_required desc
, r.rune_set_name
, r.spd desc;