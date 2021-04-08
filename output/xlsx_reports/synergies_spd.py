from bk_db_tools.xlsx_data_replace import XlsxDataReplace

class SynergiesSpd(XlsxDataReplace):
    dataSets = [
        {
            'sheetName':'spd_leader_skills',
            'firstColumn':1,
            'firstRow':2,
            'sql':"""
            select mn.full_name
            , mn.natural_stars
            , ul.unit_level
            , pu.use_for_gwo
            , pu.use_for_gwd
            , pu.use_for_rta
            , ls.amount
            , ls.area
            , ls.element
            from swarfarm_monster_names mn
            join swarfarm_leader_skills ls on mn.leader_skill_id = ls.id
              and ls.attribute = "Attack Speed"
            left join swex_unit_list ul on mn.com2us_id = ul.com2us_id
              and ul.unit_level >= 35
            left join s_player_unit pu on ul.unit_id = pu.unit_id
            where mn.awaken_level >= 1
              and mn.awakens_to is null
            order by ls.amount desc
            , mn.full_name;
            """
        },
        {
            'sheetName':'spd_buffers',
            'firstColumn':1,
            'firstRow':2,
            'sql':"""
                select mn.full_name
                , mn.natural_stars
                , ul.unit_level
                , pu.use_for_gwo
                , pu.use_for_gwd
                , pu.use_for_rta
                , other.effect_name
                from swarfarm_skills s
                join swarfarm_skills_skill_effects sse on s.com2us_id = sse.skill_com2us_id
                  and sse.aoe = 1
                join swarfarm_skill_effects se on sse.effect_id = se.id
                  and se.id = 5 -- spd
                join swarfarm_monster_names mn on (mn.skill_1_id = s.id
                    or mn.skill_2_id = s.id
                    or mn.skill_3_id = s.id
                    or mn.skill_4_id = s.id)
                  and mn.awaken_level >= 1
                  and mn.awakens_to is null
                left join swex_unit_list ul on mn.com2us_id = ul.com2us_id
                  and ul.unit_level >= 35
                left join s_player_unit pu on ul.unit_id = pu.unit_id
                left join (
                    select mn2.com2us_id
                    , se2.name as effect_name
                    from swarfarm_skills s2
                    join swarfarm_skills_skill_effects sse2 on s2.com2us_id = sse2.skill_com2us_id
                      and sse2.aoe = 1
                    join swarfarm_skill_effects se2 on sse2.effect_id = se2.id
                      and se2.id in (1,2,3) 
                    join swarfarm_monster_names mn2 on (mn2.skill_1_id = s2.id
                        or mn2.skill_2_id = s2.id
                        or mn2.skill_3_id = s2.id
                        or mn2.skill_4_id = s2.id)
                      and mn2.awaken_level >= 1
                      and mn2.awakens_to is null
                    ) as other on other.com2us_id = mn.com2us_id
                order by mn.natural_stars desc
                , mn.full_name;
            """
        },      
        {
            'sheetName':'spd_scaling_dmg',
            'firstColumn':1,
            'firstRow':2,
            'sql':"""
                select mn.full_name
                , mn.natural_stars
                , ul.unit_level
                , pu.use_for_gwo
                , pu.use_for_gwd
                , pu.use_for_rta
                , pu.spd_tune_dmg
                , case
                    when s1.multiplier_formula is not null  and s1.multiplier_formula <> '' then s1.multiplier_formula || char(10) || s1.description 
                    else s1.description
                  end as skill_1
                , case
                    when s2.multiplier_formula is not null and s2.multiplier_formula <> '' then s2.multiplier_formula || char(10) || s2.description 
                    else s2.description
                  end as skill_2
                , case
                    when s3.multiplier_formula is not null and s3.multiplier_formula <> ''  then s3.multiplier_formula || char(10) || s3.description 
                    else s3.description
                  end as skill_3
                , case
                    when s4.multiplier_formula is not null and s4.multiplier_formula <> '' then s4.multiplier_formula || char(10) || s4.description 
                    else s4.description
                  end as skill_4
                from swarfarm_monster_names mn
                left join swex_unit_list ul on mn.com2us_id = ul.com2us_id
                  and ul.unit_level >= 35
                left join s_player_unit pu on ul.unit_id = pu.unit_id
                left join swarfarm_skills s1 on mn.skill_1_id = s1.id
                left join swarfarm_skills s2 on mn.skill_2_id = s2.id
                left join swarfarm_skills s3 on mn.skill_3_id = s3.id
                left join swarfarm_skills s4 on mn.skill_4_id = s4.id
                where mn.awaken_level >= 1
                and mn.awakens_to is null
                and (s2.multiplier_formula like '%SPD%'
                  or s3.multiplier_formula like '%SPD%')
                order by mn.natural_stars desc
                , mn.full_name;
            """
        },           
    ]