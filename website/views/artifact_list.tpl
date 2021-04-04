<h2>artifact management: list</h2>

<a href="/">home</a> > <a href="/artifact_filter">filters</a>

<table border="0">
    <tr>
        <th>
            unit
        </th>
        <th  colspan="2">
            artifact
        </th>
        <th align="right">
            efficiency
        </th>
        <th>
            tier
        </th>
        <th>
        </th>
    </tr>
    %for artifact in master_list:
        <%
        #TODO refactor to use new function in server.py
        rank_color = "lightgrey"
        if artifact['rarity_name'] == "Magic":
            rank_color = "green"
        end
        if artifact['rarity_name'] == "Rare":
            rank_color = "blue"
        end
        if artifact['rarity_name'] == "Hero":
            rank_color = "purple"
        end
        if artifact['rarity_name'] == "Legendary":
            rank_color = "orange"
        end
        %>

        <tr style="background-color:lightgrey;">
            <td>
                {{artifact['full_name']}}
            </td>
            <td colspan="2" align="center">
                + {{artifact['power_up']}} {{artifact['attribute_unit_style']}} Artifact
            </td>            
            <td colspan="2">
            </td>
            <td>
                <a href="/artifact_unit?artifact_id={{artifact['artifact_id']}}">find units</a>
            </td>
        </tr>
        <tr>
            <td>
            </td>
            <td>
                {{artifact['primary_effect']}}
            </td>            
            <td  align="center" style="max-width:15px;background-color:{{rank_color}};color:white;">
                {{artifact['rarity_name']}}
            </td>          
            <td colspan="3">
            </td>
        </tr>        
        %s_effects = sub_effects(artifact['artifact_id'])
        %for effect in s_effects:
            <tr>
                <td>
                </td>
                <td colspan="2">
                    - {{effect['sub_property_formated']}}
                </td>
                <td align="right">
                    {{str(int(round(effect['efficiency'] * 100,0))) + "%"}}
                </td>
                <td>
                    {{effect['user_tier']}}
                </td>
                <td>
                </td>                
            </tr>
        %end
    %end    
</table>