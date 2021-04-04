<h2>artifact management: units for an artifact</h2>

<a href="/">home</a> > <a href="/artifact_filter">filters</a> > <a href="/artifact_list">list</a>

<table border="0">
    <tr>
        <th>
            unit<br>priority
        </th>
        <th>
            unit
        </th>
        <th>
            lvl
        </th>
        <th>
            skill 1
        </th>
        <th>
            skill 2
        </th>        
        <th>
            skill 3
        </th>
        <th>
            skill 4
        </th>
       
    </tr>
    %for unit in units:
        <tr style="background-color:lightgrey;">
            <td>
                {{unit['priority']}}
            </td>
            <td>
                {{unit['full_name']}}
            </td>
            <td>
                {{unit['unit_level']}}
            </td>            
            <td>
                {{unit['s1_formula']}}<br>
                {{unit['s1_description']}}
            </td> 
            <td>
                {{unit['s2_formula']}}<br>
                {{unit['s2_description']}}
            </td> 
            <td>
                {{unit['s3_formula']}}<br>
                {{unit['s3_description']}}
            </td> 
            <td>
                {{unit['s4_formula']}}<br>
                {{unit['s4_description']}}
            </td>             

        </tr>    
        <tr>
            <td colspan="2">
            </td>
            <td colspan="5">
                <table border="0" >
                    <tr>
                        <td valign="top">
                            <table border="0">
                                <tr>
                                    <td colspan="2" align="center">
                                        + {{artifact_type[0]['power_up']}} {{artifact_type[0]['attribute_unit_style']}} Artifact
                                    </td>
                                    <td></td>
                                    <td></td>
                                </tr>
                                    <td>
                                        {{artifact_type[0]['primary_effect']}} ({{unit['pri_effect_tier']}})
                                    </td>
                                    <td align="center" style="background-color:{{rank_color(artifact_type[0]['rarity_name'])}};color:white;">
                                        {{artifact_type[0]['rarity_name']}}
                                    </td>
                                    <th>
                                    </th>                                      
                                    <th >
                                        efficiency
                                    </th>
                                    <th>
                                    </th>                                      
                                    <th align="left">
                                        tier
                                    </th>                                    
                                <tr>
                                %s_effects = sub_effects_for_unit(artifact_id, unit['com2us_id'])
                                %for effect in s_effects:
                                    <tr>
                                        <td colspan="2">
                                            - {{effect['sub_property_formated']}}
                                        </td>
                                            <td>
                                            </td>                                        
                                        <td align="right">
                                            {{str(int(round(effect['efficiency'] * 100,0))) + "%"}}
                                        </td>
                                        <td>
                                        </td>                                        
                                        <td>
                                            {{effect['user_tier']}}
                                        </td>                
                                    </tr>
                                %end

                            </table>
                        </td>
                        <td>
                            %# to anyone seeing this. yes i know this is bad. very very bad.
                            <span style="white-space: nowrap;color:white;">11</span>
                        </td>
                        <td valign="top">
                            %equipped_artifact_id = unit['artifact_slot_1_rid']
                            %if (artifact_type[0]['type'] == 2):
                                %equipped_artifact_id = unit['artifact_slot_2_rid']
                            %end
                            %if equipped_artifact_id > 0:
                                %equippped_artifact = artifact_details(equipped_artifact_id)
                                <table border="0">
                                    <tr>
                                        <td colspan="2" align="center">
                                            + {{equippped_artifact[0]['power_up']}} {{equippped_artifact[0]['attribute_unit_style']}} Artifact
                                        </td>
                                        <td></td>
                                        <td></td>
                                    </tr>
                                        <td>
                                            {{equippped_artifact[0]['primary_effect']}} ({{unit['pri_effect_tier']}})
                                        </td>
                                        <td align="center" style="background-color:{{rank_color(equippped_artifact[0]['rarity_name'])}};color:white;">
                                            {{equippped_artifact[0]['rarity_name']}}
                                        </td>
                                        <th>
                                        </th>                                         
                                        <th >
                                            efficiency
                                        </th>
                                        <th>
                                        </th>                                        
                                        <th align="left">
                                            tier
                                        </th>                                    
                                    <tr>
                                    %s_effects = sub_effects_for_unit(equipped_artifact_id, unit['com2us_id'])
                                    %for effect in s_effects:
                                        <tr>
                                            <td colspan="2">
                                                - {{effect['sub_property_formated']}}
                                            </td>
                                            <td>
                                            </td>
                                            <td align="right">
                                                {{str(int(round(effect['efficiency'] * 100,0))) + "%"}}
                                            </td>
                                            <td>
                                            </td>
                                            <td>
                                                {{effect['user_tier']}}
                                            </td>                
                                        </tr>
                                    %end

                                </table>
                            %end
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    %end
</table>