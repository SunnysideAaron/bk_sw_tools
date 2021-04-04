DROP VIEW IF EXISTS bdt_unit_priority2;

create view bdt_unit_priority2 as
select mn.com2us_id
, ul.unit_id
, mn.full_name
, ul.unit_level
, sum(c.user_unit_priority) as total_priority
from s_team as t
left join s_content c on c.content_id = t.content_id
left join swex_unit_list ul on ul.unit_id = t.unit_id
left join swarfarm_monster_names as mn on ul.com2us_id = mn.com2us_id
group by mn.com2us_id
, ul.unit_id
, mn.full_name
, ul.unit_level
order by total_priority desc;
