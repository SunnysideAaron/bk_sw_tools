from bk_db_tools.xlsx_data_replace import XlsxDataReplace

class STierList(XlsxDataReplace):
    dataSets = [
        {
            'sheetName':'s_tier_list_units',
            'firstColumn':1,
            'firstRow':2,
            'sql':
            """
            select *
            from (
                select tlu.tier_list_id
                , tl.name
                , tlu.com2us_id
                , mn.full_name
                , mn.natural_stars
                , tlu.rank
                from s_tier_list_units tlu
                left join s_tier_list tl on tlu.tier_list_id = tl.tier_list_id
                left join swarfarm_monster_names mn on tlu.com2us_id = mn.com2us_id
                union all 
                select tl2.tier_list_id
                , tl2.name
                , mn2.com2us_id
                , mn2.full_name
                , mn2.natural_stars
                , null as rank
                from s_tier_list tl2
                join swarfarm_monster_names mn2
                where tl2.load_units = 1
                and mn2.com2us_id not in (
                    select tlu2.com2us_id
                    from  s_tier_list_units tlu2 
                    where tlu2.tier_list_id = tl2.tier_list_id
                    and tlu2.com2us_id is not null)
                and mn2.awaken_level >= 1
                and mn2.obtainable = 1
                and mn2.natural_stars > 1
            ) as r 
            order by r.tier_list_id
            , r.full_name;
            """
        },       
    ]