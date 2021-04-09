from bk_db_tools.xlsx_data_replace import XlsxDataReplace

class RuneManagement(XlsxDataReplace):
    dataSets = [
        {
            'sheetName':'inventory',
            'firstColumn':1,
            'firstRow':10,
            'lastRow':15,
            'sql':"""
            select sxr.slot_no
            , count(sxr.rune_id) as 'count'
            from swex_runes sxr 
            where sxr.occupied_id = 0
            and sxr.upgrade_curr >= 3
            group by sxr.slot_no
            order by sxr.slot_no;
            """
        },
        {
            'sheetName':'inventory',
            'firstColumn':4,
            'firstRow':3,
            'lastRow':25,
            'sql':"""
            select lrs.rune_set_name
            , lrs.rune_set_effect
            , lrs.pieces_required
            , count(
              case 
                when sxr.occupied_id > 0 then 1
              end
            ) as 'equipped'
            , count(
              case 
                when sxr.occupied_id = 0 then 1
              end
            ) as 'inventory'
            , count(sxr.rune_id) as 'total'
            from swex_runes sxr 
            left join lt_rune_set as lrs on sxr.set_id = lrs.rune_set_id
            where sxr.upgrade_curr >= 3
            group by lrs.rune_set_name
            , lrs.pieces_required
            order by lrs.pieces_required desc
            , lrs.rune_set_name;
            """
        },
        {
            'sheetName':'inventory',
            'firstColumn':5,
            'firstRow':29,
            'sql':"""
            select sxr.slot_no
            , lre.rune_effect
            , count(
              case 
                when sxr.occupied_id > 0 then 1
              end
            ) as 'equipped'
            , count(
              case 
                when sxr.occupied_id = 0 then 1
              end
            ) as 'inventory'
            , count(sxr.rune_id) as 'total'
            from swex_runes sxr 
            join lt_rune_effect as lre on sxr.pri_eff_id = lre.rune_effect_id
            where sxr.slot_no in (2,4,6)
			and sxr.upgrade_curr >= 3
            group by sxr.slot_no
            , lre.rune_effect
            order by sxr.slot_no
            , lre.rune_effect;
            """
        },
        {
            'sheetName':'quality',
            'firstColumn':3,
            'firstRow':5,
            'sql':"""
            select sxrf.rune_id
            , lrs.rune_set_name
            , sxrf.slot_no
            , lre.rune_effect
            , lrr.rarity_name as default_rarity
            , sxrf.class as stars
            , sxrf.upgrade_curr as power_up_level
            , sxre.efficiency
            , sxrq.adjusted_cri_rate_qualifier
            , sxrq.adjusted_acc_qualifier
            , sxrq.adjusted_res_qualifier
            , sxrq.adjusted_atk_offensive_power_qualifier
            , sxrq.adjusted_hp_offensive_power_qualifier
            , sxrq.adjusted_def_offensive_power_qualifier
            , sxrq.adjusted_def_power_qualifier
            , sxrq.adjusted_support_power_qualifier
            , sxrf.total_spd
            , sxrf.total_hp_percent
            , sxrf.total_atk_percent
            , sxrf.total_def_percent  
            , sxrf.total_cri_rate_percent
            , sxrf.total_cri_dmg_percent
            , sxrf.total_acc_percent
            , sxrf.total_res_percent 
            , sfmn.full_name
            , sxul.unit_level
            from swex_runes_flattened sxrf
            left join swex_unit_list as sxul on sxrf.occupied_id = sxul.unit_id
            left join swarfarm_monster_names as sfmn on sxul.com2us_id = sfmn.com2us_id
            left join lt_rune_set as lrs on sxrf.set_id = lrs.rune_set_id
            left join lt_rune_effect as lre on sxrf.pri_eff_id = lre.rune_effect_id
            left join lt_rune_rarity as lrr on sxrf.extra = lrr.rank
            left join swex_rune_quality as sxrq on sxrf.rune_id = sxrq.rune_id
            left join swex_rune_efficiency as sxre on sxrf.rune_id = sxre.rune_id
            order by sxre.efficiency desc;
            """
        },
        {
            'sheetName':'gem_grind',
            'firstColumn':2,
            'firstRow':5,
            'sql':"""
            select r.rune_id
            , rs.rune_set_name
            , r.slot_no
            , re.rune_effect
            , rr.rarity_name as default_rarity
            , r.class as stars
            , r.upgrade_curr as power_up_level
            , re.efficiency
            , re1.rune_effect as sec_eff_1
            , r.sec_eff_1_value
            , r.sec_eff_1_gemmed
            , r.sec_eff_1_grind
            , re2.rune_effect as sec_eff_2
            , r.sec_eff_2_value
            , r.sec_eff_2_gemmed
            , r.sec_eff_2_grind
            , re3.rune_effect as sec_eff_3
            , r.sec_eff_3_value
            , r.sec_eff_3_gemmed
            , r.sec_eff_3_grind
            , re4.rune_effect as sec_eff_4
            , r.sec_eff_4_value
            , r.sec_eff_4_gemmed
            , r.sec_eff_4_grind
            , mn.full_name
            , ul.unit_level
            from swex_runes r 
            left join swex_unit_list as ul on r.occupied_id = ul.unit_id
            left join swarfarm_monster_names as mn on ul.com2us_id = mn.com2us_id
            left join lt_rune_set as rs on r.set_id = rs.rune_set_id
            left join lt_rune_effect as re on r.pri_eff_id = re.rune_effect_id
            left join lt_rune_effect as re1 on r.sec_eff_1_id = re1.rune_effect_id
            left join lt_rune_effect as re2 on r.sec_eff_2_id = re2.rune_effect_id
            left join lt_rune_effect as re3 on r.sec_eff_3_id = re3.rune_effect_id
            left join lt_rune_effect as re4 on r.sec_eff_4_id = re4.rune_effect_id
            left join lt_rune_rarity as rr on r.extra = rr.rank
            left join swex_rune_efficiency as re on r.rune_id = re.rune_id
            where r.upgrade_curr >= 12
            order by re.efficiency desc;
            """
        },        
    ]