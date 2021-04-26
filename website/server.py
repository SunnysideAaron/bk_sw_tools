from bottle import (
    BaseTemplate,
    Bottle,
    error,
    request,
    route,
    run,
    template,
    TEMPLATE_PATH,
)
from pathlib import Path

class Server: 
    def __init__(self, settings, db):
        self.settings = settings
        self.db = db
    
    def run_script(self, params):
        self._app = Bottle()
        self._route()
        views_dir = str(Path(__file__).parent.absolute() / 'views')
        TEMPLATE_PATH.insert(0, views_dir)
        BaseTemplate.defaults['artifact_details'] = self._artifact_details
        BaseTemplate.defaults['sub_effects'] = self._sub_effects
        BaseTemplate.defaults['sub_effects_for_unit'] = self._sub_effects_for_unit
        BaseTemplate.defaults['rank_color'] = self._rank_color
        
        self._app.run(
            host=self.settings.host,
            port=self.settings.port,
            debug=True,
            reloader=True
        )
        
    def _route(self):
        self._app.route('/', callback=self._index)
        self._app.route('/artifact_filter', callback=self._artifact_filter)
        self._app.route('/artifact_list', method='GET', callback=self._artifact_list)
        self._app.route('/artifact_unit', method='GET', callback=self._artifact_unit)
        
    def _index(self):
        return template('home')
        
    def _artifact_filter(self):
        sql = """
        SELECT artifact_id
        , artifact_short
        FROM lt_artifact
        order by artifact_short;
        """
        
        artifact_kinds = self.db.query(sql)

        sql = """
        select a.attribute_id
        , a.attribute
        from lt_attribute a;
        """
        
        attributes = self.db.query(sql)

        sql = """
        select unit_style_id
        , us.unit_style
        from lt_unit_style us;
        """
        
        unit_styles = self.db.query(sql)
        
        sql = """
        select rr.rank
        , rr.rarity_name
        from lt_rune_rarity rr
        where rr.rank < 13;
        """
        
        rune_rarities = self.db.query(sql)        
        
        sql = """
        SELECT artifact_primary_effect_id
        , effect
        FROM lt_artifact_primary_effect
        order by effect;
        """
        
        primary_effects = self.db.query(sql)

        sql = """
        select s.artifact_sub_id
        , s.sub_property
        from s_artifact_sub s
        order by s.select_list_order;
        """
        
        secondary_effects = self.db.query(sql)  

        return template(
            'artifact_filter',
            artifact_kinds=artifact_kinds,
            attributes=attributes,
            unit_styles=unit_styles,
            rune_rarities=rune_rarities,
            primary_effects=primary_effects,
            secondary_effects=secondary_effects
        )

    def _artifact_list(self):
        artifact_kind = request.GET.ArtifactKind.strip()
        attribute = request.GET.Attribute.strip()
        unit_style = request.GET.UnitStyle.strip()
        natural_rank = request.GET.NaturalRank.strip()
        power_up_minimum = request.GET.PowerUpMinimum.strip()
        power_up_maximum = request.GET.PowerUpMaximum.strip()
        primary_effect = request.GET.PrimaryEffect.strip()
        secondary_effect = request.GET.SecondaryEffect.strip()
        equipped = request.GET.Equipped.strip()
        efficiency_minimum = request.GET.EfficiencyMinimum.strip()
        
        sql = """
        select a.rid as artifact_id
        , lt_artifact.artifact_short
        , case 
            when a.type = 1 then lt_attribute.attribute
            else us.unit_style
          end as attribute_unit_style
        , rr.rarity_name
        , a.level as power_up
        , ape.effect as primary_effect
        , a.occupied_id
        , mn.full_name
        , max(ae.efficiency)
        from swex_artifacts a
        left join lt_artifact on a.type = lt_artifact.artifact_id
        left join lt_attribute on a.attribute = lt_attribute.attribute_id
        left join lt_unit_style us on a.unit_style = us.unit_style_id
        left join lt_rune_rarity rr on a.natural_rank = rr.rank
        left join lt_artifact_primary_effect ape on a.pri_effect_id = ape.artifact_primary_effect_id
        left join swex_unit_list ul on a.occupied_id = ul.unit_id
        left join swarfarm_monster_names mn on ul.com2us_id = mn.com2us_id
        left join swex_artifact_efficiency ae on a.rid = ae.rid
        where a.level >= ?
        and a.level <= ?
        """
        
        if not power_up_minimum:
            power_up_minimum = 0
         
        if not power_up_maximum:
            power_up_maximum = 15
  
        params = [power_up_minimum, power_up_maximum]
        
        if artifact_kind and artifact_kind != "All":
            sql = sql + """
            and a.type = ?
            """
            params.append(artifact_kind)
        
        if attribute and attribute != "All":
            sql = sql + """
            and a.attribute = ?
            """
            params.append(attribute)

        if unit_style and unit_style != "All":
            sql = sql + """
            and a.unit_style = ?
            """
            params.append(unit_style)
            
        if natural_rank and natural_rank != "All":
            sql = sql + """
            and a.natural_rank = ?
            """
            params.append(natural_rank)

        if primary_effect and primary_effect != "All":
            sql = sql + """
            and a.pri_effect_id = ?
            """
            params.append(primary_effect)
        
        if equipped == "1":
            sql = sql + """
            and a.occupied_id > 0
            """

        if equipped == "0":
            sql = sql + """
            and a.occupied_id = 0
            """
        
        if secondary_effect and secondary_effect != "All":
            sql = sql + """
            and a.rid in (
                select ae.rid
                from swex_artifact_efficiency ae
                where ae.artifact_sub_id = ?
            )
            """
            params.append(secondary_effect)
        
        sql = sql + """
        group by a.rid
        , lt_artifact.artifact_short
        , rr.rarity_name
        , a.level
        , ape.effect
        , a.occupied_id
        , mn.full_name
        """
        
        if efficiency_minimum and int(efficiency_minimum) > 0:
            sql = sql + """
            having max(ae.efficiency) > ?
            """
            params.append(float(efficiency_minimum) / 100)        
        
        sql = sql + """
        order by max(ae.efficiency) desc;
        """
        
        params = tuple(params)
        
        master_list = self.db.query(sql, params)        

        return template('artifact_list', master_list=master_list)

    def _artifact_unit(self):
        artifact_id = request.GET.artifact_id.strip()
            
        artifact_type = self._artifact_details(artifact_id)        
        
        sql = """
        select up.priority
        , ul.unit_id
        , ul.com2us_id as com2us_id
        , mn.full_name
        , ul.unit_level
        , s1.description as s1_description
        , s1.multiplier_formula as s1_formula
        , s2.description as s2_description
        , s2.multiplier_formula as s2_formula
        , s3.description as s3_description
        , s3.multiplier_formula as s3_formula
        , s4.description as s4_description
        , s4.multiplier_formula as s4_formula        
        , ul.artifact_slot_1_rid
        , ul.artifact_slot_2_rid
        , apu.user_setting as pri_effect_tier
        from swex_unit_list ul
        join swarfarm_monster_names mn on ul.com2us_id = mn.com2us_id
        left join s_unit_priority up on ul.unit_id = up.unit_id
        left join swarfarm_skills s1 on ul.skills_1_id = s1.com2us_id
        left join swarfarm_skills s2 on ul.skills_2_id = s2.com2us_id
        left join swarfarm_skills s3 on ul.skills_3_id = s3.com2us_id
        left join swarfarm_skills s4 on ul.skills_4_id = s4.com2us_id
        left join s_artifact_pri_unit apu on ul.com2us_id = apu.com2us_id
            and apu.effect = ?
        where unit_level >= 35
        and (mn.element = ?
            or mn.archetype = ?
        )
        order by unit_level desc 
        , up.priority desc 
        , mn.full_name;
        """        
        
        params = (
            artifact_type[0]['primary_effect'],
            artifact_type[0]['attribute'],
            artifact_type[0]['unit_style'],
        )
            
        units = self.db.query(sql, params)        
        
        return template(
            'artifact_unit',
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            units=units
        )        
    
    def _artifact_details(self, artifact_id):
        sql = """
        select swex_artifacts.level as power_up
        , swex_artifacts.type
        , rr.rarity_name
        , lt_artifact.artifact_short
        , lt_attribute.attribute
        , us.unit_style
        , case 
            when swex_artifacts.type = 1 then lt_attribute.attribute
            else us.unit_style
          end as attribute_unit_style
        , ape.effect as primary_effect
        from swex_artifacts
        left join lt_artifact on swex_artifacts.type = lt_artifact.artifact_id
        left join lt_attribute on swex_artifacts.attribute = lt_attribute.attribute_id
        left join lt_unit_style us on swex_artifacts.unit_style = us.unit_style_id
        left join lt_rune_rarity rr on swex_artifacts.natural_rank = rr.rank
        left join lt_artifact_primary_effect ape on swex_artifacts.pri_effect_id = ape.artifact_primary_effect_id
        where swex_artifacts.rid = ?
        """        
        
        params = (artifact_id,)
            
        return self.db.query(sql, params) 
    
    def _sub_effects(self, artifact_id):
        sql = """
        select ae.sub_property_formated
        , ae.efficiency
        , sub.user_tier
        from swex_artifact_efficiency ae
        left join s_artifact_sub sub on ae.artifact_sub_id = sub.artifact_sub_id
        where ae.rid = ?
        order by ae.efficiency desc
        """        
        
        params = (artifact_id,)
            
        return self.db.query(sql, params)

    def _sub_effects_for_unit(self, artifact_id, com2us_id):
        sql = """
        select ae.sub_property_formated
        , ae.efficiency
        , sub.user_tier
        from swex_artifact_efficiency ae
        left join s_artifact_sub_unit sub on ae.artifact_sub_id = sub.artifact_sub_id
            and sub.com2us_id = ?
        where ae.rid = ?
        order by ae.efficiency desc
        """        
        
        params = (com2us_id, artifact_id)
            
        return self.db.query(sql, params)
        
    # TODO convert this to be stored in the db since we will reuse often.
    # to do it right actually need 4 colors:
    # * background color
    # * text color on background color
    # * text color on light background
    # * text color on dark background
    def _rank_color(self, rank):
        color = "lightgrey"
        if rank == "Magic":
            color = "green"

        if rank == "Rare":
            color = "blue"

        if rank == "Hero":
            color = "purple"

        if rank == "Legendary":
            color = "orange"
            
        return color