from bk_db_tools.xlsx_data_replace import XlsxDataReplace

class UnitCombatSpeeds(XlsxDataReplace):
    dataSets = [
        {
            'sheetName':'combat_speeds',
            'firstColumn':1,
            'firstRow':5,
            'sql':"""
            select ul.unit_id
            , mn.full_name
            , ul.unit_level
            , mn.natural_stars
            , pu.use_for_gwo
            , pu.use_for_gwd
            , pu.use_for_rta
            , pu.spd_tune_max
            , pu.spd_tune_atk_bar
            , pu.spd_tune_buffer
            , pu.buffs
            , pu.spd_tune_strip
            , pu.spd_tune_debuff
            , pu.debuffs
            , pu.spd_tune_dmg
            , ul.spd as base_spd
            , sum(
                case 
                    when rf.pri_eff_id = 8 then rf.pri_eff_value
                    else rf.total_spd
                end) as rune_spd
            from swex_unit_list ul
            left join swarfarm_monster_names mn on ul.com2us_id = mn.com2us_id
            left join swex_runes_flattened rf on ul.unit_id = rf.occupied_id
            left join s_player_unit pu on ul.unit_id = pu.unit_id
            where ul.unit_level >= 35
            group by ul.unit_id
            , mn.full_name
            , ul.unit_level
            , pu.use_for_gwo
            , pu.use_for_gwd
            , pu.use_for_rta
            , pu.spd_tune_max
            , pu.spd_tune_atk_bar
            , pu.spd_tune_buffer
            , pu.buffs
            , pu.spd_tune_strip
            , pu.spd_tune_debuff
            , pu.debuffs
            , pu.spd_tune_dmg
            , ul.spd
            order by base_spd + rune_spd desc;
            """
        },
    ]