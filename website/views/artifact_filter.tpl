<h2>artifact management: list filter</h2>

<a href="/">home</a>
</br></br>
<form action="/artifact_list" method="GET">
    <table border="0">
        <tr>
            <td>
                <label for="ArtifactKind">artifact</label>
            </td>
            <td>
                <select name="ArtifactKind" id="ArtifactKind">
                    <option value="All">All</option>
                    %for artifact_kind in artifact_kinds:
                        <option value="{{artifact_kind['artifact_id']}}">{{artifact_kind['artifact_short']}}</option>
                    %end 
                </select>
            </td>
        </tr>
        <tr>
            <td>    
                <label for="Attribute">attribute</label><br>
            </td>
            <td>
                <select name="Attribute" id="Attribute">
                    <option value="All">All</option>
                    %for attribute in attributes:
                        <option value="{{attribute['attribute_id']}}">{{attribute['attribute']}}</option>
                    %end 
                </select>
            </td>
        </tr>
        <tr>
            <td>    
                <label for="UnitStyle">unit style</label><br>
            </td>
            <td>
                <select name="UnitStyle" id="UnitStyle">
                    <option value="All">All</option>
                    %for unit_style in unit_styles:
                        <option value="{{unit_style['unit_style_id']}}">{{unit_style['unit_style']}}</option>
                    %end 
                </select>
            </td>
        </tr>
        <tr>
            <td>
                <label for="NaturalRank">natural rank</label>
            </td>
            <td>
                <select name="NaturalRank" id="NaturalRank">
                    <option value="All">All</option>
                    %for rune_rarity in rune_rarities:
                        <option value="{{rune_rarity['rank']}}">{{rune_rarity['rarity_name']}}</option>
                    %end 
                </select>
            </td>
        </tr>
        <tr>
            <td>    
                <label for="PowerUpMinimum">power-up minimum</label><br>
            </td>
            <td>
                <input type="number" name="PowerUpMinimum" id="PowerUpMinimum" value=0>
            </td>
        </tr>
        <tr>
            <td>
                <label for="PowerUpMaximum">power-up maximum</label>
            </td>
            <td>
                <input type="number" name="PowerUpMaximum" id="PowerUpMaximum" value=15>
            </td>
        </tr>
        <tr>
            <td>    
                <label for="PrimaryEffect">primary effect</label><br>
            </td>
            <td>
                <select name="PrimaryEffect" id="PrimaryEffect">
                    <option value="All">All</option>
                    %for primary_effect in primary_effects:
                        <option value="{{primary_effect['artifact_primary_effect_id']}}">{{primary_effect['effect']}}</option>
                    %end                    
                </select>
            </td>
        </tr>
                <tr>
            <td>
                <label for="SecondaryEffect">secondary effect</label>
            </td>
            <td>
                <select name="SecondaryEffect" id="SecondaryEffect">
                    <option value="All">All</option>
                    %for secondary_effect in secondary_effects:
                        <option value="{{secondary_effect['artifact_sub_id']}}">{{secondary_effect['sub_property']}}</option>
                    %end 
                </select>
            </td>
        </tr>
        <tr>
            <td>    
                <label for="Equipped">equipped</label><br>
            </td>
            <td>
                <select name="Equipped" id="Equipped">
                    <option value="All">All</option>
                    <option value="1">Yes</option>
                    <option value="0">No</option>
                </select>
            </td>
        </tr>
        <tr>
            <td>
                <label for="EfficiencyMinimum">efficiency minimum</label>
            </td>
            <td>
                <input type="number" name="EfficiencyMinimum" id="EfficiencyMinimum" value=0>%
            </td>
        </tr>
        <tr>
            <td></td>
            <td>
                <input type="submit" name="list" value="list">
            </td>
        </tr>
    </table>
</form>