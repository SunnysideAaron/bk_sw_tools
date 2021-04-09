import json
import urllib.request

class ImportSwarfarm:
    def __init__(self, settings, db):
        self.settings = settings
        self.db = db    
    
    def run_script(self, params):
        self.create_tables()
        self.create_views()

        monstersJSON = self.fetch_swarfarm_api('monsters/')
        self.load_monsters_table(monstersJSON)
        
        skillsJSON = self.fetch_swarfarm_api('skills/')
        self.load_skills_table(skillsJSON)
        self.load_skills_upgrades_table(skillsJSON)
        self.load_skills_skill_effects_table(skillsJSON)
        
        skillEffectsJSON = self.fetch_swarfarm_api('skill-effects/')
        self.load_skill_effects_table(skillEffectsJSON)
                
        leaderSkillsJSON = self.fetch_swarfarm_api('leader-skills/')
        self.load_leader_skills_table(leaderSkillsJSON)
        
    def create_tables(self):
        sql = """
        DROP TABLE IF EXISTS swarfarm_monsters;
        """
    
        self.db.execute(sql)
        
        sql = """
        CREATE TABLE swarfarm_monsters (
          id int
        , url text
        , bestiary_slug text
        , com2us_id int
        , family_id int
        , name text
        , image_filename text
        , full_image_url text
        , element text
        , archetype text
        , base_stars int
        , natural_stars int
        , obtainable int
        , can_awaken int
        , awaken_level int
        , awaken_bonus text
        , skill_1_id int
        , skill_2_id int
        , skill_3_id int
        , skill_4_id int
        , skill_ups_to_max int
        , leader_skill_id int
        -- , homunculus_skills
        , base_hp int
        , base_attack int
        , base_defense int
        , speed int
        , crit_rate int
        , crit_damage int
        , resistance int
        , accuracy int
        , raw_hp int
        , raw_attack int
        , raw_defense int
        , max_lvl_hp int
        , max_lvl_attack int
        , max_lvl_defense int
        , awakens_from int
        , awakens_to int
        -- , awaken_cost
        -- , source
        , fusion_food int
        , homunculus int
        , craft_cost int
        -- , craft_materials
        );
        """

        self.db.execute(sql)

        sql = """
        CREATE INDEX swarfarm_monsters_com2us_id ON swarfarm_monsters(com2us_id);
        """

        self.db.execute(sql)

        sql = """
        DROP TABLE IF EXISTS swarfarm_skills;
        """
    
        self.db.execute(sql)
        
        sql = """
        CREATE TABLE swarfarm_skills (
          id int
        , com2us_id int
        , name text
        , description text
        , slot int
        , cooltime int
        , hits int
        , passive int
        , aoe int
        , max_level int
        , multiplier_formula text
        -- , multiplier_formula_raw
        , scales_with text
        , icon_filename text
        , full_icon_url text
        -- , used_on
        -- , level_progress_description
        );
        """

        self.db.execute(sql)        

        sql = """
        CREATE INDEX swarfarm_skills_com2us_id ON swarfarm_skills(com2us_id);
        """

        self.db.execute(sql)
        
        sql = """
        DROP TABLE IF EXISTS swarfarm_skills_upgrades;
        """
    
        self.db.execute(sql)
        
        sql = """
        CREATE TABLE swarfarm_skills_upgrades (
          skill_com2us_id int
        , upgrade_order int
        , effect text
        , amount int
        );
        """

        self.db.execute(sql)

        sql = """
        DROP TABLE IF EXISTS swarfarm_skills_skill_effects;
        """
    
        self.db.execute(sql)
        
        sql = """
        CREATE TABLE swarfarm_skills_skill_effects (
          skill_com2us_id int
        , effect_id int
        , aoe int
        , single_target int
        , self_effect int
        , chance int
        , on_crit int
        , on_death int
        , random int
        , quantity int
        , 'all' int
        , self_hp int
        , target_hp int
        , damage int
        , note text
        );
        """

        self.db.execute(sql)        
        
        sql = """
        DROP TABLE IF EXISTS swarfarm_skill_effects;
        """
    
        self.db.execute(sql)
        
        sql = """
        CREATE TABLE swarfarm_skill_effects (
          id int
        , url text
        , name text
        , is_buff int
        , description text
        , icon_filename text
        , full_icon_url text
        );
        """

        self.db.execute(sql)
        
        sql = """
        DROP TABLE IF EXISTS swarfarm_leader_skills
        """
    
        self.db.execute(sql)
        
        sql = """
        CREATE TABLE swarfarm_leader_skills (
          id int
        , url text
        , attribute text
        , amount int
        , area text
        , element text
        );
        """

        self.db.execute(sql)
        
        self.db.commit()

    def create_views(self):
        sql = """
        DROP VIEW IF EXISTS swarfarm_monster_families;
        """
    
        self.db.execute(sql)

        sql = """
        create view swarfarm_monster_families as
        select sfm.family_id
        , sfm.name
        from swarfarm_monsters sfm
        where sfm.obtainable = 1
        and sfm.awaken_level = 0
        group by sfm.family_id
        , sfm.name;
        """
    
        self.db.execute(sql)

        sql = """
        DROP VIEW IF EXISTS swarfarm_monster_names;
        """
    
        self.db.execute(sql)

        sql = """
        create view swarfarm_monster_names as
        select sfmf.name
        , case
            when sfmf.name is null then sfm.name || ' (' || sfm.element || ')'
            when awaken_level = 0 then sfm.element || ' ' || sfmf.name
            when awaken_level = 1 then sfm.name || ' (' || sfm.element || ' ' || sfmf.name || ')'
            when awaken_level = 2 then sfm.name || ' 2a (' || sfm.element || ' ' || sfmf.name || ')'
          end as full_name
        , sfm.*  
        from swarfarm_monsters sfm
        left join swarfarm_monster_families sfmf on sfm.family_id = sfmf.family_id;
        """
    
        self.db.execute(sql)
        
        self.db.commit()
        
    def fetch_swarfarm_api(self, path):
        baseURL = 'https://swarfarm.com/api/v2/'
        url = baseURL + path + '?page='
        tempJson = '';
        allJson = [];
        next = 'placeholder';
        page = 1;

        while (next and page <= 50): # a safeguard against endless loops
            tempJson = self.fetch_api(url + str(page))
            #print(tempJson['results'])
            allJson += tempJson['results']
            next = tempJson['next']
            print ('fetched ' + path + ' page: ' + str(page))
            page = page + 1
            
        return allJson;
    
    def fetch_api(self, url):
        operUrl = urllib.request.urlopen(url)

        if(operUrl.getcode()==200):
           data = operUrl.read()
           jsonData = json.loads(data)
        else:
           print("Error receiving data", operUrl.getcode())

        return jsonData

    def load_monsters_table(self, monstersJSON):    
        imageUrl = 'https://swarfarm.com/static/herders/images/monsters/'
        
        sql = """
        INSERT INTO swarfarm_monsters (
          id
        , url
        , bestiary_slug
        , com2us_id
        , family_id
        , name
        , image_filename
        , full_image_url
        , element
        , archetype
        , base_stars
        , natural_stars
        , obtainable
        , can_awaken
        , awaken_level
        , awaken_bonus
        , skill_1_id
        , skill_2_id
        , skill_3_id
        , skill_4_id
        , skill_ups_to_max
        , leader_skill_id
        -- , homunculus_skills
        , base_hp
        , base_attack
        , base_defense
        , speed
        , crit_rate
        , crit_damage
        , resistance
        , accuracy
        , raw_hp
        , raw_attack
        , raw_defense
        , max_lvl_hp
        , max_lvl_attack
        , max_lvl_defense
        , awakens_from
        , awakens_to
        -- , awaken_cost
        -- , source
        , fusion_food
        , homunculus
        , craft_cost
        -- , craft_materials
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
        -- , ?
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
        -- , ?
        -- , ?
        , ?
        , ?
        , ?
        -- , ?
        );
        """
        
        totalcount = 0
        msgcount = 0
        
        for monster in monstersJSON:
            skill_1_id = 0
            skill_2_id = 0
            skill_3_id = 0
            skill_4_id = 0
            leader_skill_id = 0
            
            if len(monster['skills']) >= 1:
                skill_1_id = monster['skills'][0]
            if len(monster['skills']) >= 2:
                skill_2_id = monster['skills'][1]
            if len(monster['skills']) >= 3:
                skill_3_id = monster['skills'][2]
            if len(monster['skills']) >= 4:
                skill_4_id = monster['skills'][3]                

            if monster['leader_skill'] is not None:
                leader_skill_id = monster['leader_skill']['id']
            
            params = (
                monster['id'],
                monster['url'],
                monster['bestiary_slug'],
                monster['com2us_id'],
                monster['family_id'],
                monster['name'],
                monster['image_filename'],
                imageUrl + monster['image_filename'],
                monster['element'],
                monster['archetype'],
                monster['base_stars'],
                monster['natural_stars'],
                monster['obtainable'],
                monster['can_awaken'],
                monster['awaken_level'],
                monster['awaken_bonus'],
                skill_1_id,
                skill_2_id,
                skill_3_id,
                skill_4_id,
                monster['skill_ups_to_max'],
                leader_skill_id,
                # monster.homunculus_skills,
                monster['base_hp'],
                monster['base_attack'],
                monster['base_defense'],
                monster['speed'],
                monster['crit_rate'],
                monster['crit_damage'],
                monster['resistance'],
                monster['accuracy'],
                monster['raw_hp'],
                monster['raw_attack'],
                monster['raw_defense'],
                monster['max_lvl_hp'],
                monster['max_lvl_attack'],
                monster['max_lvl_defense'],
                monster['awakens_from'],
                monster['awakens_to'],
                # monster['awaken_cost'],
                # monster['source'],
                monster['fusion_food'],
                monster['homunculus'],
                monster['craft_cost']
                # monster['craft_materials
                )
                
            self.db.execute(sql, params)    
            self.db.commit()

            totalcount += 1
            msgcount += 1
            
            if msgcount > 100:
                print ('inserted ' + str(totalcount) + ' monsters')
                msgcount = 0
                
    def load_skills_table(self, skillsJSON):    
        imageUrl = 'https://swarfarm.com/static/herders/images/skills/'
        
        sql = """
        INSERT INTO swarfarm_skills (
          id
        , com2us_id
        , name
        , description
        , slot
        , cooltime
        , hits
        , passive
        , aoe
        , max_level
        , multiplier_formula
        -- , multiplier_formula_raw
        , scales_with
        , icon_filename
        , full_icon_url
        -- , used_on
        -- , level_progress_description
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
        -- , ?
        , ?
        , ?
        , ?
        -- , ?
        -- , ?
        );
        """
        
        totalcount = 0
        msgcount = 0
        
        for skill in skillsJSON:
            scales_with = 0

            if skill['scales_with'] is not None:
                scales_with = ", ".join(skill['scales_with'])
            
            params = (
                skill['id'],
                skill['com2us_id'],
                skill['name'],
                skill['description'],
                skill['slot'],
                skill['cooltime'],
                skill['hits'],
                skill['passive'],
                skill['aoe'],
                skill['max_level'],
                skill['multiplier_formula'],
                # "multiplier_formula_raw": "[]",
                scales_with,
                skill['icon_filename'],
                imageUrl + skill['icon_filename']
                # "used_on",
                # "level_progress_description"
                )
                
            self.db.execute(sql, params)
            self.db.commit()
            
            totalcount += 1
            msgcount += 1
            
            if msgcount > 100:
                print ('inserted ' + str(totalcount) + ' skills')
                msgcount = 0

    def load_skills_upgrades_table(self, skillsJSON):    
        sql = """
        INSERT INTO swarfarm_skills_upgrades (
          skill_com2us_id
        , upgrade_order
        , effect
        , amount
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        );
        """
        
        totalcount = 0
        msgcount = 0
        
        for skill in skillsJSON:
            upgradeOrder = 0
            for upgrade in skill['upgrades']:
                params = (
                    skill['com2us_id'],
                    upgradeOrder,
                    upgrade['effect'],
                    upgrade['amount'])
                    
                self.db.execute(sql, params)
                self.db.commit()
                
                upgradeOrder += 1

            totalcount += 1
            msgcount += 1
            
            if msgcount > 100:
                print ('inserted ' + str(totalcount) + ' skill upgrades')
                msgcount = 0

    def load_skills_skill_effects_table(self, skillsJSON):    
        sql = """
        INSERT INTO swarfarm_skills_skill_effects (
          skill_com2us_id
        , effect_id
        , aoe
        , single_target
        , self_effect
        , chance
        , on_crit
        , on_death
        , random
        , quantity
        , 'all'
        , self_hp
        , target_hp
        , damage
        , note
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
        );
        """
        
        totalcount = 0
        msgcount = 0
        
        for skill in skillsJSON:
            for effect in skill['effects']:
                params = (
                    skill['com2us_id'],
                    effect['effect']['id'],
                    effect['aoe'],
                    effect['single_target'],
                    effect['self_effect'],
                    effect['chance'],
                    effect['on_crit'],
                    effect['on_death'],
                    effect['random'],
                    effect['quantity'],
                    effect['all'],
                    effect['self_hp'],
                    effect['target_hp'],
                    effect['damage'],
                    effect['note'])
                    
                self.db.execute(sql, params)
                self.db.commit()

            totalcount += 1
            msgcount += 1
            
            if msgcount > 100:
                print ('inserted ' + str(totalcount) + ' skills skill effects')
                msgcount = 0

    def load_skill_effects_table(self, skillEffectsJSON):    
        imageUrl = 'https://swarfarm.com/static/herders/images/buffs/'
        
        sql = """
        INSERT INTO swarfarm_skill_effects (
          id
        , url
        , name
        , is_buff
        , description
        , icon_filename
        , full_icon_url
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
        
        totalcount = 0
        msgcount = 0
        
        for skillEffect in skillEffectsJSON:
            fullIconUrl = ''
            
            if (skillEffect['icon_filename'] is not None and
                skillEffect['icon_filename'] != ''):
                fullIconUrl = imageUrl + skillEffect['icon_filename']
            
            params = (
                skillEffect['id'],
                skillEffect['url'],
                skillEffect['name'],
                skillEffect['is_buff'],
                skillEffect['description'],
                skillEffect['icon_filename'],
                fullIconUrl)
                
            self.db.execute(sql, params)
            self.db.commit()

            totalcount += 1
            msgcount += 1
            
            if msgcount > 100:
                print ('inserted ' + str(totalcount) + ' skill effects')
                msgcount = 0

    def load_leader_skills_table(self, leaderSkillsJSON):    
        sql = """
        INSERT INTO swarfarm_leader_skills (
          id
        , url
        , attribute
        , amount
        , area
        , element
        ) VALUES (
          ?
        , ?
        , ?
        , ?
        , ?
        , ?
        );
        """
        
        totalcount = 0
        msgcount = 0
        
        for leaderSkill in leaderSkillsJSON:
            params = (
                leaderSkill['id'],
                leaderSkill['url'],
                leaderSkill['attribute'],
                leaderSkill['amount'],
                leaderSkill['area'],
                leaderSkill['element'])
                
            self.db.execute(sql, params)
            self.db.commit()

            totalcount += 1
            msgcount += 1
            
            if msgcount > 100:
                print ('inserted ' + str(totalcount) + ' leader skills')
                msgcount = 0
