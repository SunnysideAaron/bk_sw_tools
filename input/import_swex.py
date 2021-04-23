import glob
import json
import os
from pathlib import Path

class ImportSwex: 
    def __init__(self, settings, db):
        self.settings = settings
        self.db = db 
    
    def run_script(self, params):
        self.create_tables()
        self.create_views()
        
        jsonData = self.load_file()

        self.insert_unit_list(jsonData['unit_list'])
        
        for deco in jsonData['deco_list']: 
            self.insert_deco(deco)
        
        for unit in jsonData['unit_list']: 
            for rune in unit['runes']:
                self.insert_rune(rune)
            for artifact in unit['artifacts']:
                self.insert_artifact(artifact)    
        
        for inventory in jsonData['inventory_info']: 
            self.insert_inventory(inventory)
        
        for rune in jsonData['runes']: 
            self.insert_rune(rune)

        for rune_craft_item in jsonData['rune_craft_item_list']: 
            self.insert_rune_craft_item(rune_craft_item)
            
        for artifact in jsonData['artifacts']: 
            self.insert_artifact(artifact)

        for rta_rune in jsonData['world_arena_rune_equip_list']: 
            self.insert_rta_rune(rta_rune)

        for rta_artifact in jsonData['world_arena_artifact_equip_list']: 
            self.insert_rta_artifact(rta_artifact)
  
    def create_tables(self):
        sql = """
        DROP TABLE IF EXISTS swex_deco_list
        """

        self.db.execute(sql)

        sql = """
        CREATE TABLE swex_deco_list (
          wizard_id int
        , deco_id int
        , decoration_id int
        , island_id int
        , pos_x int
        , pos_y int
        , level int
        );
        """

        self.db.execute(sql)

        sql = """
        DROP TABLE IF EXISTS swex_unit_list
        """
    
        self.db.execute(sql)
        
        sql = """
        CREATE TABLE swex_unit_list (
          unit_id int
        , wizard_id int
        , island_id int
        , pos_x int
        , pos_y int
        , building_id int
        , com2us_id int
        , unit_level int
        , class int
        , con int
        , atk int
        , def int
        , spd int
        , resist int
        , accuracy int
        , critical_rate int
        , critical_damage int
        , experience int
        , exp_gained int
        , exp_gain_rate int
        , skills_1_id int
        , skills_1_level int
        , skills_2_id int
        , skills_2_level int
        , skills_3_id int
        , skills_3_level int 
        , skills_4_id int
        , skills_4_level int
        , rune_slot_1_id int
        , rune_slot_2_id int
        , rune_slot_3_id int
        , rune_slot_4_id int
        , rune_slot_5_id int
        , rune_slot_6_id int
        , artifact_slot_1_rid int
        , artifact_slot_2_rid int
        , costume_master_id int
        , trans_items text
        , attribute int
        , create_time text
        , source int
        , homunculus int
        , homunculus_name text
        , awakening_info text
        );
        """

        self.db.execute(sql)
        
        sql = """
        DROP TABLE IF EXISTS swex_inventory_info
        """

        self.db.execute(sql)

        sql = """
        CREATE TABLE swex_inventory_info (
          wizard_id int
        , item_master_type int
        , item_master_id int
        , item_quantity int
        );
        """

        self.db.execute(sql)
        
        sql = """
        DROP TABLE IF EXISTS swex_runes
        """

        self.db.execute(sql)

        sql = """
        CREATE TABLE swex_runes (
          rune_id int
        , wizard_id int
        , occupied_type int
        , occupied_id int
        , slot_no int
        , rank int
        , class int
        , set_id int
        , upgrade_limit int
        , upgrade_curr int
        , base_value int
        , sell_value int
        , pri_eff_id int
        , pri_eff_value int
        , prefix_eff_id int
        , prefix_eff_value int
        , sec_eff_1_id int
        , sec_eff_1_value int
        , sec_eff_1_gemmed int
        , sec_eff_1_grind int
        , sec_eff_2_id int
        , sec_eff_2_value int
        , sec_eff_2_gemmed int
        , sec_eff_2_grind int
        , sec_eff_3_id int
        , sec_eff_3_value int
        , sec_eff_3_gemmed int
        , sec_eff_3_grind int
        , sec_eff_4_id int
        , sec_eff_4_value int
        , sec_eff_4_gemmed int
        , sec_eff_4_grind int
        , extra int
        );
        """

        self.db.execute(sql)

        sql = """
        DROP TABLE IF EXISTS swex_rune_craft_item_list
        """

        self.db.execute(sql)

        sql = """
        CREATE TABLE swex_rune_craft_item_list (
          craft_item_id int
        , wizard_id int
        , craft_type int
        , craft_type_id int
        , sell_value int
        , amount int
        );
        """

        self.db.execute(sql)

        sql = """
        DROP TABLE IF EXISTS swex_artifacts
        """

        self.db.execute(sql)

        sql = """
        CREATE TABLE swex_artifacts (
          rid int
        , wizard_id int
        , occupied_id int
        , slot int
        , type int
        , attribute int
        , unit_style int
        , natural_rank int
        , rank int
        , level int
        , pri_effect_id int
        , pri_effect_1 int
        , pri_effect_2 int
        , pri_effect_3 int
        , pri_effect_4 int
        , sec_effects_1_id int
        , sec_effects_1_1 int
        , sec_effects_1_2 int
        , sec_effects_1_3 int
        , sec_effects_1_4 int
        , sec_effects_2_id int
        , sec_effects_2_1 int
        , sec_effects_2_2 int
        , sec_effects_2_3 int
        , sec_effects_2_4 int
        , sec_effects_3_id int
        , sec_effects_3_1 int
        , sec_effects_3_2 int
        , sec_effects_3_3 int
        , sec_effects_3_4 int
        , sec_effects_4_id int
        , sec_effects_4_1 int
        , sec_effects_4_2 int
        , sec_effects_4_3 int
        , sec_effects_4_4 int
        , locked int
        , source int
        , extra text
        , date_add text
        , date_mod text
        );
        """

        self.db.execute(sql)

        sql = """
        DROP TABLE IF EXISTS swex_rta_runes
        """

        self.db.execute(sql)

        sql = """
        CREATE TABLE swex_rta_runes (
          rune_id int
        , occupied_id int
        );
        """

        self.db.execute(sql)

        sql = """
        DROP TABLE IF EXISTS swex_rta_artifacts
        """

        self.db.execute(sql)

        sql = """
        CREATE TABLE swex_rta_artifacts (
          rid int
        , artifact_id int  
        , occupied_id int
        );
        """

        self.db.execute(sql)

        self.db.commit()

    def create_views(self):
        sql = """
        DROP VIEW IF EXISTS swex_runes_flattened;
        """
    
        self.db.execute(sql)

        sql = """
        create view swex_runes_flattened as
        select sxr.rune_id
        , sxr.occupied_id
        , sxr.set_id
        , sxr.slot_no
        , sxr.rank
        , sxr.extra
        , sxr.class
        , sxr.upgrade_curr
        , sxr.pri_eff_id
        , sxr.pri_eff_value
        , case
            when sxr.prefix_eff_id = 1 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 1 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 1 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 1 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 1 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_hp_flat
        , case
            when sxr.prefix_eff_id = 2 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 2 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 2 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 2 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 2 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_hp_percent
        , case
            when sxr.prefix_eff_id = 3 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 3 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 3 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 3 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 3 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_atk_flat	  
        , case
            when sxr.prefix_eff_id = 4 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 4 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 4 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 4 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 4 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_atk_percent
        , case
            when sxr.prefix_eff_id = 5 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 5 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 5 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 5 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 5 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_def_flat	  
        , case
            when sxr.prefix_eff_id = 6 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 6 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 6 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 6 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 6 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_def_percent  
        , case
            when sxr.prefix_eff_id = 8 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 8 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 8 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 8 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 8 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_spd
        , case
            when sxr.prefix_eff_id = 9 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 9 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 9 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 9 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 9 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_cri_rate_percent
        , case
            when sxr.prefix_eff_id = 10 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 10 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 10 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 10 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 10 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_cri_dmg_percent
        , case
            when sxr.prefix_eff_id = 12 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 12 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 12 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 12 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 12 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_acc_percent
        , case
            when sxr.prefix_eff_id = 11 then sxr.prefix_eff_value
            when sxr.sec_eff_1_id = 11 then sxr.sec_eff_1_value + sec_eff_1_grind
            when sxr.sec_eff_2_id = 11 then sxr.sec_eff_2_value + sec_eff_2_grind
            when sxr.sec_eff_3_id = 11 then sxr.sec_eff_3_value + sec_eff_3_grind
            when sxr.sec_eff_4_id = 11 then sxr.sec_eff_4_value + sec_eff_4_grind
            else 0
          end as total_res_percent
        from swex_runes sxr;
        """
    
        self.db.execute(sql)

        sql = """
        DROP VIEW IF EXISTS swex_rune_efficiency;
        """
    
        self.db.execute(sql)

        sql = """
        create view swex_rune_efficiency as
        select sxrf.rune_id
        , round(((sxrf.total_hp_percent / cast(40 as float))
        + (sxrf.total_atk_percent / cast(40 as float))
        + (sxrf.total_def_percent / cast(40 as float))
        + (sxrf.total_spd / cast(30 as float))
        + (sxrf.total_cri_rate_percent / cast(30 as float))
        + (sxrf.total_cri_dmg_percent / cast(35 as float))
        + (sxrf.total_acc_percent / cast(40 as float))
        + (sxrf.total_res_percent / cast(40 as float))
        + 1) / 2.8 * 100) as efficiency
        from swex_runes_flattened sxrf;
        """
    
        self.db.execute(sql)
        
        sql = """
        DROP VIEW IF EXISTS swex_rune_quality;
        """
    
        self.db.execute(sql)

        sql = """
        create view swex_rune_quality as
        select sxrf2.rune_id
        , adjusted_cri_rate_qualifier
        , adjusted_acc_qualifier
        , adjusted_res_qualifier
        , case
            when atk_offensive_power_qualifier_4_set > atk_offensive_power_qualifier_4_pri_eff then atk_offensive_power_qualifier_4_set
            else atk_offensive_power_qualifier_4_pri_eff
          end as adjusted_atk_offensive_power_qualifier
        , case
            when hp_offensive_power_qualifier_4_set > hp_offensive_power_qualifier_4_pri_eff then hp_offensive_power_qualifier_4_set
            else hp_offensive_power_qualifier_4_pri_eff
          end as adjusted_hp_offensive_power_qualifier  
        , case
            when def_offensive_power_qualifier_4_set > def_offensive_power_qualifier_4_pri_eff then def_offensive_power_qualifier_4_set
            else def_offensive_power_qualifier_4_pri_eff
          end as adjusted_def_offensive_power_qualifier
        , case
            when def_power_qualifier_4_set > def_power_qualifier_4_pri_eff then def_power_qualifier_4_set
            else def_power_qualifier_4_pri_eff
          end as adjusted_def_power_qualifier
        , adjusted_support_power_qualifier  
        from (
            select sxrf.rune_id
            , case
                when lrs.cri_rate_synergy = 1 then sxrf.total_cri_rate_percent + sxrf.total_spd
                else sxrf.total_cri_rate_percent
              end as adjusted_cri_rate_qualifier
            , case
                when lrs.acc_synergy = 1 then sxrf.total_acc_percent + sxrf.total_spd
                else sxrf.total_acc_percent
              end as adjusted_acc_qualifier  
            , case
                when lrs.res_synergy = 1 then sxrf.total_res_percent + sxrf.total_spd
                else sxrf.total_res_percent
              end as adjusted_res_qualifier
            , case
                when lrs.atk_offensive_power_synergy = 1 then sxrf.total_atk_percent + total_cri_rate_percent + total_cri_dmg_percent + sxrf.total_spd
                else sxrf.total_atk_percent + total_cri_rate_percent + total_cri_dmg_percent
              end as atk_offensive_power_qualifier_4_set
            , case
                when sxrf.slot_no in (2,4,6)
                    and sxrf.pri_eff_id in (4,9,10)
                    then sxrf.total_atk_percent + total_cri_rate_percent + total_cri_dmg_percent + 5
                else sxrf.total_atk_percent + total_cri_rate_percent + total_cri_dmg_percent
              end as atk_offensive_power_qualifier_4_pri_eff
            , case
                when lrs.hp_offensive_power_synergy = 1 then sxrf.total_hp_percent + total_cri_rate_percent + total_cri_dmg_percent + sxrf.total_spd
                else sxrf.total_hp_percent + total_cri_rate_percent + total_cri_dmg_percent
              end as hp_offensive_power_qualifier_4_set
            , case
                when sxrf.slot_no in (2,4,6)
                    and sxrf.pri_eff_id in (2,9,10)
                    then sxrf.total_hp_percent + total_cri_rate_percent + total_cri_dmg_percent + 5
                else sxrf.total_hp_percent + total_cri_rate_percent + total_cri_dmg_percent
              end as hp_offensive_power_qualifier_4_pri_eff
            , case
                when lrs.def_offensive_power_synergy = 1 then sxrf.total_def_percent + total_cri_rate_percent + total_cri_dmg_percent + sxrf.total_spd
                else sxrf.total_def_percent + total_cri_rate_percent + total_cri_dmg_percent
              end as def_offensive_power_qualifier_4_set
            , case
                when sxrf.slot_no in (2,4,6)
                    and sxrf.pri_eff_id in (6,9,10)
                    then sxrf.total_def_percent + total_cri_rate_percent + total_cri_dmg_percent + 5
                else sxrf.total_def_percent + total_cri_rate_percent + total_cri_dmg_percent
              end as def_offensive_power_qualifier_4_pri_eff	  
            , case
                when lrs.def_power_synergy = 1 then sxrf.total_hp_percent + sxrf.total_def_percent + sxrf.total_res_percent + sxrf.total_spd
                else sxrf.total_hp_percent + sxrf.total_def_percent + sxrf.total_res_percent
              end as def_power_qualifier_4_set
            , case
                when sxrf.slot_no in (2,4,6)
                    and sxrf.pri_eff_id in (2,4,11)
                    then sxrf.total_hp_percent + sxrf.total_def_percent + sxrf.total_res_percent + 5
                else sxrf.total_hp_percent + sxrf.total_def_percent + sxrf.total_res_percent
              end as def_power_qualifier_4_pri_eff
            , case
                when sxrf.slot_no in (2,4,6)
                    and sxrf.pri_eff_id in (2,8,12)
                    then sxrf.total_hp_percent + sxrf.total_spd + sxrf.total_acc_percent + 5
                else sxrf.total_hp_percent + sxrf.total_spd + sxrf.total_acc_percent
              end as adjusted_support_power_qualifier
            from swex_runes_flattened sxrf
            left join lt_rune_set as lrs on sxrf.set_id = lrs.rune_set_id
        ) as sxrf2;
        """
    
        self.db.execute(sql)

        sql = """
        DROP VIEW IF EXISTS swex_artifact_efficiency;
        """
    
        self.db.execute(sql)

        sql = """
        create view swex_artifact_efficiency as
        select a1.rid
        , 1 as item_order
        , a1.sec_effects_1_id as artifact_sub_id
        , as1.sub_property
        , a1.sec_effects_1_1 as sub_value
        , case 
            when a1.sec_effects_1_id in (222,223) then replace(as1.sub_property, 'CRIT DMG+',  'CRIT DMG+' || a1.sec_effects_1_1)
            when a1.sec_effects_1_id = 224 then replace(as1.sub_property, 'CRIT DMG +',  'CRIT DMG +' || a1.sec_effects_1_1)
            else replace(as1.sub_property, 'N%',  a1.sec_effects_1_1 || '%')
          end as sub_property_formated
        , 1.0 * a1.sec_effects_1_1 / as1.max_power_up as efficiency
        from swex_artifacts a1 
        join s_artifact_sub as1 on a1.sec_effects_1_id = as1.artifact_sub_id
        union all
        select a2.rid
        , 2 as item_order
        , a2.sec_effects_2_id as artifact_sub_id
        , as2.sub_property
        , a2.sec_effects_2_1 as sub_value
        , case 
            when a2.sec_effects_2_id in (222,223) then replace(as2.sub_property, 'CRIT DMG+',  'CRIT DMG+' || a2.sec_effects_2_1)
            when a2.sec_effects_2_id = 224 then replace(as2.sub_property, 'CRIT DMG +',  'CRIT DMG +' || a2.sec_effects_2_1)
            else replace(as2.sub_property, 'N%',  a2.sec_effects_2_1 || '%')
          end as sub_property_formated
        , 1.0 * a2.sec_effects_2_1 / as2.max_power_up as efficiency
        from swex_artifacts a2 
        join s_artifact_sub as2 on a2.sec_effects_2_id = as2.artifact_sub_id
        union all
        select a3.rid
        , 3 as item_order
        , a3.sec_effects_3_id as artifact_sub_id
        , as3.sub_property
        , a3.sec_effects_3_1 as sub_value
        , case 
            when a3.sec_effects_3_id in (222,223) then replace(as3.sub_property, 'CRIT DMG+',  'CRIT DMG+' || a3.sec_effects_3_1)
            when a3.sec_effects_3_id = 224 then replace(as3.sub_property, 'CRIT DMG +',  'CRIT DMG +' || a3.sec_effects_3_1)
            else replace(as3.sub_property, 'N%',  a3.sec_effects_3_1 || '%')
          end as sub_property_formated
        , 1.0 * a3.sec_effects_3_1 / as3.max_power_up as efficiency
        from swex_artifacts a3
        join s_artifact_sub as3 on a3.sec_effects_3_id = as3.artifact_sub_id
        union all
        select a4.rid
        , 4 as item_order
        , a4.sec_effects_4_id as artifact_sub_id
        , as4.sub_property
        , a4.sec_effects_4_1 as sub_value
        , case 
            when a4.sec_effects_4_id in (222,223) then replace(as4.sub_property, 'CRIT DMG+',  'CRIT DMG+' || a4.sec_effects_4_1)
            when a4.sec_effects_4_id = 224 then replace(as4.sub_property, 'CRIT DMG +',  'CRIT DMG +' || a4.sec_effects_4_1)
            else replace(as4.sub_property, 'N%',  a4.sec_effects_4_1 || '%')
          end as sub_property_formated
        , 1.0 * a4.sec_effects_4_1 / as4.max_power_up as efficiency
        from swex_artifacts a4 
        join s_artifact_sub as4 on a4.sec_effects_4_id = as4.artifact_sub_id;
        """
    
        self.db.execute(sql)
        
        self.db.commit()

    def load_file(self):
        #20/80 rule, just hard code the path.
        search = str(Path(__file__).parent.absolute()) + '\*.json'
        
        list_of_files = glob.glob(search)

        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, encoding='utf-8') as jsonFile:
            jsonData = json.load(jsonFile)
        return jsonData

    def insert_deco(self, deco):
        sql = """
        INSERT INTO swex_deco_list (
          wizard_id
        , deco_id
        , decoration_id
        , island_id
        , pos_x
        , pos_y
        , level
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        );
        """   

        params = (
            deco['wizard_id'],
            deco['deco_id'],
            deco['master_id'],
            deco['island_id'],
            deco['pos_x'],
            deco['pos_y'],
            deco['level'])

        self.db.execute(sql, params)
        
        self.db.commit()

    def insert_unit_list(self, unitList):
        sql = """
        INSERT INTO swex_unit_list (
          unit_id
        , wizard_id
        , island_id
        , pos_x
        , pos_y
        , building_id
        , com2us_id
        , unit_level
        , class
        , con
        , atk
        , def
        , spd
        , resist
        , accuracy
        , critical_rate
        , critical_damage
        , experience
        , exp_gained
        , exp_gain_rate
        , skills_1_id
        , skills_1_level
        , skills_2_id
        , skills_2_level
        , skills_3_id
        , skills_3_level
        , skills_4_id
        , skills_4_level
        , rune_slot_1_id
        , rune_slot_2_id
        , rune_slot_3_id
        , rune_slot_4_id
        , rune_slot_5_id
        , rune_slot_6_id
        , artifact_slot_1_rid
        , artifact_slot_2_rid
        , costume_master_id
        , trans_items
        , attribute
        , create_time
        , source
        , homunculus
        , homunculus_name
        , awakening_info
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        );
        """
        
        for unit in unitList:
            skills_1_id = 0
            skills_1_level = 0
            skills_2_id = 0
            skills_2_level = 0
            skills_3_id = 0
            skills_3_level = 0
            skills_4_id = 0
            skills_4_level = 0
            rune_slot_1_id = 0
            rune_slot_2_id = 0
            rune_slot_3_id = 0
            rune_slot_4_id = 0
            rune_slot_5_id = 0
            rune_slot_6_id = 0
            artifact_slot_1_rid = 0
            artifact_slot_2_rid = 0
            trans_items = ''
            awakening_info = ''

            if len(unit['skills']) >= 1:
                skills_1_id = unit['skills'][0][0]
                skills_1_level = unit['skills'][0][1]

            if len(unit['skills']) >= 2:
                skills_2_id = unit['skills'][1][0]
                skills_2_level = unit['skills'][1][1]

            if len(unit['skills']) >= 3:
                skills_3_id = unit['skills'][2][0]
                skills_3_level = unit['skills'][2][1]

            if len(unit['skills']) >= 4:
                skills_4_id = unit['skills'][3][0]
                skills_4_level = unit['skills'][3][1]

            for rune in unit['runes']:
                if rune['slot_no'] == 1:
                    rune_slot_1_id = rune['rune_id']
                if rune['slot_no'] == 2:
                    rune_slot_2_id = rune['rune_id']
                if rune['slot_no'] == 3:
                    rune_slot_3_id = rune['rune_id']
                if rune['slot_no'] == 4:
                    rune_slot_4_id = rune['rune_id']
                if rune['slot_no'] == 5:
                    rune_slot_5_id = rune['rune_id']
                if rune['slot_no'] == 6:
                    rune_slot_6_id = rune['rune_id']

            for artifact in unit['artifacts']:
                if artifact['slot'] == 1:
                    artifact_slot_1_rid = artifact['rid']
                if artifact['slot'] == 2:
                    artifact_slot_2_rid = artifact['rid']

            if len(unit['trans_items']) > 0:
                trans_items = 'to do'

            if len(unit['awakening_info']) > 0:
                awakening_info = 'to do'
                
            params = (
                unit['unit_id'],
                unit['wizard_id'],
                unit['island_id'],
                unit['pos_x'],
                unit['pos_y'],
                unit['building_id'],
                #changing unit_master_id to com2us_id to be consistent with other data sources
                unit['unit_master_id'],
                unit['unit_level'],
                unit['class'],
                unit['con'],
                unit['atk'],
                unit['def'],
                unit['spd'],
                unit['resist'],
                unit['accuracy'],
                unit['critical_rate'],
                unit['critical_damage'],
                unit['experience'],
                unit['exp_gained'],
                unit['exp_gain_rate'],
                skills_1_id,
                skills_1_level,
                skills_2_id,
                skills_2_level,
                skills_3_id,
                skills_3_level,
                skills_4_id,
                skills_4_level,
                rune_slot_1_id,
                rune_slot_2_id,
                rune_slot_3_id,
                rune_slot_4_id,
                rune_slot_5_id,
                rune_slot_6_id,
                artifact_slot_1_rid,
                artifact_slot_2_rid,
                unit['costume_master_id'],
                trans_items,
                unit['attribute'],
                unit['create_time'],
                unit['source'],
                unit['homunculus'],
                unit['homunculus_name'],
                awakening_info)

            self.db.execute(sql, params)

            self.db.commit()
        
    def insert_inventory(self, inventory):
        sql = """
        INSERT INTO swex_inventory_info (
          wizard_id
        , item_master_type
        , item_master_id
        , item_quantity
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        );
        """   

        params = (
            inventory['wizard_id'],
            inventory['item_master_type'],
            inventory['item_master_id'],
            inventory['item_quantity'])

        self.db.execute(sql, params)
        
        self.db.commit()        
               
    def insert_rune(self, rune):
        sql = """
        INSERT INTO swex_runes (
          rune_id
        , wizard_id
        , occupied_type
        , occupied_id
        , slot_no
        , rank
        , class
        , set_id
        , upgrade_limit
        , upgrade_curr
        , base_value
        , sell_value
        , pri_eff_id
        , pri_eff_value
        , prefix_eff_id
        , prefix_eff_value
        , sec_eff_1_id
        , sec_eff_1_value
        , sec_eff_1_gemmed
        , sec_eff_1_grind
        , sec_eff_2_id
        , sec_eff_2_value
        , sec_eff_2_gemmed
        , sec_eff_2_grind
        , sec_eff_3_id
        , sec_eff_3_value
        , sec_eff_3_gemmed
        , sec_eff_3_grind
        , sec_eff_4_id
        , sec_eff_4_value
        , sec_eff_4_gemmed
        , sec_eff_4_grind  
        , extra
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        );
        """
        
        sec_eff_1_id = 0
        sec_eff_1_value = 0
        sec_eff_1_gemmed = 0
        sec_eff_1_grind = 0
        sec_eff_2_id = 0
        sec_eff_2_value = 0
        sec_eff_2_gemmed = 0
        sec_eff_2_grind = 0
        sec_eff_3_id = 0
        sec_eff_3_value = 0
        sec_eff_3_gemmed = 0
        sec_eff_3_grind = 0
        sec_eff_4_id = 0
        sec_eff_4_value = 0
        sec_eff_4_gemmed = 0
        sec_eff_4_grind = 0
        
        if len(rune['sec_eff']) >= 1:
            sec_eff_1_id = rune['sec_eff'][0][0]
            sec_eff_1_value = rune['sec_eff'][0][1]
            sec_eff_1_gemmed = rune['sec_eff'][0][2]
            sec_eff_1_grind = rune['sec_eff'][0][3]

        if len(rune['sec_eff']) >= 2:
            sec_eff_2_id = rune['sec_eff'][1][0]
            sec_eff_2_value = rune['sec_eff'][1][1]
            sec_eff_2_gemmed = rune['sec_eff'][1][2]
            sec_eff_2_grind = rune['sec_eff'][1][3]

        if len(rune['sec_eff']) >= 3:
            sec_eff_3_id = rune['sec_eff'][2][0]
            sec_eff_3_value = rune['sec_eff'][2][1]
            sec_eff_3_gemmed = rune['sec_eff'][2][2]
            sec_eff_3_grind = rune['sec_eff'][2][3]

        if len(rune['sec_eff']) >= 4:
            sec_eff_4_id = rune['sec_eff'][3][0]
            sec_eff_4_value = rune['sec_eff'][3][1]
            sec_eff_4_gemmed = rune['sec_eff'][3][2]
            sec_eff_4_grind = rune['sec_eff'][3][3]
            
        params = (
            rune['rune_id'],
            rune['wizard_id'],
            rune['occupied_type'],
            rune['occupied_id'],
            rune['slot_no'],
            rune['rank'],
            rune['class'],
            rune['set_id'],
            rune['upgrade_limit'],
            rune['upgrade_curr'],
            rune['base_value'],
            rune['sell_value'],
            rune['pri_eff'][0],
            rune['pri_eff'][1],
            rune['prefix_eff'][0],
            rune['prefix_eff'][1],
            sec_eff_1_id,
            sec_eff_1_value,
            sec_eff_1_gemmed,
            sec_eff_1_grind,
            sec_eff_2_id,
            sec_eff_2_value,
            sec_eff_2_gemmed,
            sec_eff_2_grind,
            sec_eff_3_id,
            sec_eff_3_value,
            sec_eff_3_gemmed,
            sec_eff_3_grind,
            sec_eff_4_id,
            sec_eff_4_value,
            sec_eff_4_gemmed,
            sec_eff_4_grind,
            rune['extra'])

        self.db.execute(sql, params)
        
        self.db.commit()

    def insert_rune_craft_item(self, rune_craft_item):
        sql = """
        INSERT INTO swex_rune_craft_item_list (
          craft_item_id
        , wizard_id
        , craft_type
        , craft_type_id
        , sell_value
        , amount        
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        , ?
        , ?
        );
        """   

        params = (
            rune_craft_item['craft_item_id'],
            rune_craft_item['wizard_id'],
            rune_craft_item['craft_type'],
            rune_craft_item['craft_type_id'],
            rune_craft_item['sell_value'],
            rune_craft_item['amount'])

        self.db.execute(sql, params)
        
        self.db.commit() 

    def insert_artifact(self, artifact):
        sql = """
        INSERT INTO swex_artifacts (
          rid
        , wizard_id
        , occupied_id
        , slot
        , type
        , attribute
        , unit_style
        , natural_rank
        , rank
        , level        
        , pri_effect_id
        , pri_effect_1
        , pri_effect_2
        , pri_effect_3
        , pri_effect_4
        , sec_effects_1_id
        , sec_effects_1_1
        , sec_effects_1_2
        , sec_effects_1_3
        , sec_effects_1_4
        , sec_effects_2_id
        , sec_effects_2_1
        , sec_effects_2_2
        , sec_effects_2_3
        , sec_effects_2_4
        , sec_effects_3_id
        , sec_effects_3_1
        , sec_effects_3_2
        , sec_effects_3_3
        , sec_effects_3_4
        , sec_effects_4_id
        , sec_effects_4_1
        , sec_effects_4_2
        , sec_effects_4_3
        , sec_effects_4_4
        , locked
        , source
        , extra
        , date_add
        , date_mod
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        );
        """
        
        sec_effects_1_id = 0
        sec_effects_1_1 = 0
        sec_effects_1_2 = 0
        sec_effects_1_3 = 0
        sec_effects_1_4 = 0
        sec_effects_2_id = 0
        sec_effects_2_1 = 0
        sec_effects_2_2 = 0
        sec_effects_2_3 = 0
        sec_effects_2_4 = 0
        sec_effects_3_id = 0
        sec_effects_3_1 = 0
        sec_effects_3_2 = 0
        sec_effects_3_3 = 0
        sec_effects_3_4 = 0
        sec_effects_4_id = 0
        sec_effects_4_1 = 0
        sec_effects_4_2 = 0
        sec_effects_4_3 = 0
        sec_effects_4_4 = 0
        extra = ''
        
        if len(artifact['sec_effects']) >= 1:
            sec_effects_1_id = artifact['sec_effects'][0][0]
            sec_effects_1_1 = artifact['sec_effects'][0][1]
            sec_effects_1_2 = artifact['sec_effects'][0][2]
            sec_effects_1_3 = artifact['sec_effects'][0][3]
            sec_effects_1_4 = artifact['sec_effects'][0][4]

        if len(artifact['sec_effects']) >= 2:
            sec_effects_2_id = artifact['sec_effects'][1][0]
            sec_effects_2_1 = artifact['sec_effects'][1][1]
            sec_effects_2_2 = artifact['sec_effects'][1][2]
            sec_effects_2_3 = artifact['sec_effects'][1][3]
            sec_effects_2_4 = artifact['sec_effects'][1][4]
            
        if len(artifact['sec_effects']) >= 3:
            sec_effects_3_id = artifact['sec_effects'][2][0]
            sec_effects_3_1 = artifact['sec_effects'][2][1]
            sec_effects_3_2 = artifact['sec_effects'][2][2]
            sec_effects_3_3 = artifact['sec_effects'][2][3]
            sec_effects_3_4 = artifact['sec_effects'][2][4]

        if len(artifact['sec_effects']) >= 4:
            sec_effects_4_id = artifact['sec_effects'][3][0]
            sec_effects_4_1 = artifact['sec_effects'][3][1]
            sec_effects_4_2 = artifact['sec_effects'][3][2]
            sec_effects_4_3 = artifact['sec_effects'][3][3]
            sec_effects_4_4 = artifact['sec_effects'][3][4]
        
        if len(artifact['extra']) > 0:
            extra = 'to do'
                
        params = (
            artifact['rid'],
            artifact['wizard_id'],
            artifact['occupied_id'],
            artifact['slot'],
            artifact['type'],
            artifact['attribute'],
            artifact['unit_style'],
            artifact['natural_rank'],
            artifact['rank'],
            artifact['level'],
            artifact['pri_effect'][0],
            artifact['pri_effect'][1],
            artifact['pri_effect'][2],
            artifact['pri_effect'][2],
            artifact['pri_effect'][4],
            sec_effects_1_id,
            sec_effects_1_1,
            sec_effects_1_2,
            sec_effects_1_3,
            sec_effects_1_4,
            sec_effects_2_id,
            sec_effects_2_1,
            sec_effects_2_2,
            sec_effects_2_3,
            sec_effects_2_4,
            sec_effects_3_id,
            sec_effects_3_1,
            sec_effects_3_2,
            sec_effects_3_3,
            sec_effects_3_4,
            sec_effects_4_id,
            sec_effects_4_1,
            sec_effects_4_2,
            sec_effects_4_3,
            sec_effects_4_4,
            artifact['locked'],
            artifact['source'],
            extra,
            artifact['date_add'],
            artifact['date_mod'])

        self.db.execute(sql, params)
        
        self.db.commit()

    def insert_rta_rune(self, rta_rune):
        sql = """
        INSERT INTO swex_rta_runes (
          rune_id
        , occupied_id
        ) VALUES (
          ?
        , ?
        );
        """
                        
        params = (
            rta_rune['rune_id'],
            rta_rune['occupied_id'])

        self.db.execute(sql, params)
        
        self.db.commit()

    def insert_rta_artifact(self, rta_artifact):
        sql = """
        INSERT INTO swex_rta_artifacts (
          rid
        , artifact_id 
        , occupied_id
        ) VALUES (
          ?
        , ?
        , ?
        );
        """
    
        params = (
            rta_artifact['rid'],
            rta_artifact['artifact_id'],
            rta_artifact['occupied_id'])

        self.db.execute(sql, params)
        
        self.db.commit()