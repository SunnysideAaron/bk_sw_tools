from src.xlsx_data_replace import XlsxDataReplace

class SOther(XlsxDataReplace):
    dataSets = [
        {
            'sheetName':'s_player_unit',
            'firstColumn':1,
            'firstRow':2,
            'sql':
            """
            select *
            from (
                select pu.unit_id
                , mn.full_name
                , ul.unit_level
                , pu.use_for_gb12
                , pu.use_for_db12
                , pu.use_for_nb12
                , pu.use_for_sf10
                , pu.use_for_pc10
                , pu.use_for_toa
                , pu.use_for_dhole_griffon
                , pu.use_for_dhole_inugami
                , pu.use_for_dhole_warbear
                , pu.use_for_dhole_fairy
                , pu.use_for_dhole_pixie
                , pu.use_for_dhole_werewolf
                , pu.use_for_dhole_cat
                , pu.use_for_dhole_howl
                , pu.use_for_dhole_grim
                , pu.use_for_dhole_karzhan
                , pu.use_for_dhole_ellunia
                , pu.use_for_dhole_lumel
                , pu.use_for_dhole_khalderun
                , pu.use_for_d_predator
                , pu.use_for_rift_beast_fire
                , pu.use_for_rift_beast_ice
                , pu.use_for_rift_beast_wind
                , pu.use_for_rift_beast_light
                , pu.use_for_rift_beast_dark
                , pu.use_for_r5
                , pu.use_for_lab
                , pu.use_for_arena
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
                , pu.cleanser
                , pu.reviver
                , pu.runed_as_healer
                , pu.runed_as_tank
                , pu.runed_as_bruiser                
                , mn.full_name || ' lvl ' || ul.unit_level || ' | ' || ul.unit_id as unit_select
                from s_player_unit pu
                join swex_unit_list ul on pu.unit_id = ul.unit_id
                left join swarfarm_monster_names mn on mn.com2us_id = ul.com2us_id
                union all
                select ul2.unit_id
                , mn2.full_name
                , ul2.unit_level
                , null as use_for_gb12
                , null as use_for_db12
                , null as use_for_nb12
                , null as use_for_sf10
                , null as use_for_pc10
                , null as use_for_toa
                , null as use_for_dhole_griffon
                , null as use_for_dhole_inugami
                , null as use_for_dhole_warbear
                , null as use_for_dhole_fairy
                , null as use_for_dhole_pixie
                , null as use_for_dhole_werewolf
                , null as use_for_dhole_cat
                , null as use_for_dhole_howl
                , null as use_for_dhole_grim
                , null as use_for_dhole_karzhan
                , null as use_for_dhole_ellunia
                , null as use_for_dhole_lumel
                , null as use_for_dhole_khalderun
                , null as use_for_d_predator
                , null as use_for_rift_beast_fire
                , null as use_for_rift_beast_ice
                , null as use_for_rift_beast_wind
                , null as use_for_rift_beast_light
                , null as use_for_rift_beast_dark
                , null as use_for_r5
                , null as use_for_lab
                , null as use_for_arena                
                , null as use_for_gwo
                , null as use_for_gwd
                , null as use_for_rta
                , null as spd_tune_max
                , null as spd_tune_atk_bar
                , null as spd_tune_buffer
                , null as buffs
                , null as spd_tune_strip
                , null as spd_tune_debuff
                , null as debuffs
                , null as spd_tune_dmg
                , null as cleanser
                , null as reviver
                , null as runed_as_healer
                , null as runed_as_tank
                , null as runed_as_bruiser
                , mn2.full_name || ' lvl ' || ul2.unit_level || ' | ' || ul2.unit_id as unit_select
                from swex_unit_list ul2 
                left join swarfarm_monster_names mn2 on mn2.com2us_id = ul2.com2us_id
                left join s_player_unit pu2 on ul2.unit_id = pu2.unit_id
                where pu2.unit_id is null
                and ul2.unit_level >= 35
            ) as r 
            order by r.unit_level desc
            , r.full_name;
            """
        }, 
    ]