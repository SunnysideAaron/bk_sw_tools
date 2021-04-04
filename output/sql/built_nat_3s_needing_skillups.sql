select ul.com2us_id
, mn.full_name
, ul.unit_level
, skills_1_level + skills_2_level + skills_3_level skill_levels_attained
, mn.skill_ups_to_max + 3 as total_skill_levels
from swex_unit_list ul
left join swarfarm_monster_names mn on ul.com2us_id = mn.com2us_id
where ul.unit_level >= 35
and mn.natural_stars <= 3
and mn.awaken_level < 2
and (skills_1_level + skills_2_level + skills_3_level) <> (mn.skill_ups_to_max + 3)
order by mn.full_name;