from bk_db_tools.xlsx_data_replace import XlsxDataReplace

class SArtifact(XlsxDataReplace):
    dataSets = [
        {
            'sheetName':'s_artifact_pri_unit',
            'firstColumn':1,
            'firstRow':2,
            'lastColumn':5,
            'sql':
            """
            select *
            from (
                select apu.com2us_id
                , mn.full_name
                , apu.effect
                , apu.default_setting
                , apu.user_setting
                from s_artifact_pri_unit apu
                left join swarfarm_monster_names mn on apu.com2us_id = mn.com2us_id
                union all
                select mn2.com2us_id
                , mn2.full_name
                , ape.effect
                , '' as default_setting
                , '' as user_setting
                from swarfarm_monster_names mn2
                join lt_artifact_primary_effect ape
                left join s_artifact_pri_unit apu2 on  mn2.com2us_id = apu2.com2us_id
                where mn2.obtainable = 1
                and mn2.natural_stars > 1
                and mn2.can_awaken > 0
                and mn2.awakens_to is null
                and apu2.com2us_id is null
            ) as r 
            order by r.full_name
            , r.effect;
            """
        },
        {
            'sheetName':'s_artifact_sub_unit',
            'firstColumn':1,
            'firstRow':2,
            'lastColumn':7,
            'sql':
            """
            select *
            from (
                select asu.com2us_id
                , mn.full_name
                , asu.artifact_sub_id
                , asub.sub_property
                , asu.default_tier
                , asu.user_tier
                , asu.notes
                from s_artifact_sub_unit asu
                left join swarfarm_monster_names mn on asu.com2us_id = mn.com2us_id
                left join s_artifact_sub asub on asu.artifact_sub_id = asub.artifact_sub_id
                union all
                select mn2.com2us_id
                , mn2.full_name
                , asub.artifact_sub_id
                , asub.sub_property
                , '' as default_tier
                , '' as user_tier
                , '' as notes
                from swarfarm_monster_names mn2
                join s_artifact_sub asub
                left join s_artifact_sub_unit asu2 on  mn2.com2us_id = asu2.com2us_id
                where mn2.obtainable = 1
                and mn2.natural_stars > 1
                and mn2.can_awaken > 0
                and mn2.awakens_to is null
                and asu2.com2us_id is null
            ) as r 
            order by r.full_name
            , r.sub_property;
            """
        },        
    ]