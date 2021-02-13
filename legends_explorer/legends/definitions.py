from legends_explorer.legends import Collection
from legends_explorer.legends.types import (
    Int, Str, Rectangle, Coordinates, List, GroupBy, Bool, LinkToPreviousGroupBy, Entity
)

definitions = {
    'regions': Collection('regions', 'id', Entity('id', {
        'id': Int(), 'name': Str(), 'type': Str(), 'coords': Coordinates(), 'evilness': Str(), 'force_id': Int()
    })),
    'underground_regions': Collection('underground_regions', 'id', Entity('id', {
        'id': Int(), 'type': Str(), 'depth': Int(), 'coords': Coordinates()
    })),
    'sites': Collection('sites', 'id', Entity('id', {
        'id': Int(), 'type': Str(), 'name': Str(), 'coords': Coordinates(), 'rectangle': Rectangle(),
        'civ_id': Int(), 'cur_owner_id': Int(),
        'structures': List('id', Entity('id', {
            'id': Int(), 'type': Str(), 'name': Str(), 'name2': Str(), 'entity_id': Int(), 'deity': Int(),
            'subtype': Str(), 'owner_hfid': Int(), 'worship_hfid': Int(), 'deity_type': Int(),
            'inhabitant': GroupBy('inhabitants', Int()), 'religion': Int(), 'dungeon_type': Int(),
            'copied_artifact_id': GroupBy('copied_artifact_ids', Int())
        }, transforms={'local_id': 'id'})),
        'site_properties': List('id', Entity('id', {
            'id': Int(), 'structure_id': Int(), 'type': Str(), 'owner_hfid': Int()
        }))
    })),
    'artifacts': Collection('artifacts', 'id', Entity('id', {
        'id': Int(), 'name': Str(), 'site_id': Int(), 'holder_hfid': Int(), 'mat': Str(), 'item_type': Str(),
        'structure_local_id': Int(), 'subregion_id': Int(), 'item_description': Str(), 'page_count': Int(),
        'abs_tile_x': Str(), 'abs_tile_y': Str(), 'abs_tile_z': Str(), 'writing': Int(), 'item_subtype': Str(),
        'item': Entity('name_string', {
            'name_string': Str(), 'page_number': Int(), 'page_written_content_id': Int(),
            'writing_written_content_id': Int()
        })
    })),
    "historical_figures": Collection('historical_figures', 'id', Entity('id', {
        'id': Int(), 'name': Str(), 'race': Str(), 'caste': Str(), 'appeared': Int(), 'sex': Int(),
        'birth_year': Int(), 'birth_seconds72': Int(), 'death_year': Int(), 'death_seconds72': Int(),
        'associated_type': Str(), 'goal': GroupBy('goals', Str()), 'ent_pop_id': Int(), 'animated': Bool(),
        'current_identity_id': Int(), 'deity': Bool(), 'force': Bool(), 'animated_string': Str(),
        'sphere': GroupBy('spheres', Str()), 'interaction_knowledge': GroupBy('spheres', Str()),
        'journey_pet': GroupBy('journey_pets', Str()), 'holds_artifact': GroupBy('holds_artifacts', Int()),
        'active_interaction': GroupBy('active_interactions', Str()),
        'site_link': GroupBy('site_links', Entity('site_id', {
            'link_type': Str(), 'site_id': Int(), 'sub_id': Int(), 'entity_id': Int(), 'occupation_id': Int()
        })),
        'hf_link': GroupBy('hf_links', Entity('hfid', {
            'link_type': Str(), 'hfid': Int(), 'link_strength': Int()
        })),
        'vague_relationship': GroupBy('vague_relationships', Entity('hfid', {
            'childhood_friend': Bool(), 'hfid': Int(), 'war_buddy': Bool(), 'athlete_buddy': Bool(),
            'artistic_buddy': Bool(), 'religious_persecution_grudge': Bool(), 'scholar_buddy': Bool(),
            'jealous_obsession': Bool(), 'grudge': Bool(), 'persecution_grudge': Bool(),
            'atheletic_rival': Bool(), 'business_rival': Bool(), 'jealous_relationship_grudge': Bool()
        })),
        'entity_link': GroupBy('entity_links', Entity('entity_id', {
            'link_type': Str(), 'entity_id': Int(), 'link_strength': Int()
        })),
        'entity_position_link': LinkToPreviousGroupBy(
            'entity_links', 'entity_position_link', Entity('entity_id', {
                'position_profile_id': Int(), 'entity_id': Int(), 'start_year': Int()
            })
        ),
        'entity_former_position_link': LinkToPreviousGroupBy(
            'entity_links', 'entity_former_position_link', Entity('entity_id', {
                'position_profile_id': Int(), 'entity_id': Int(), 'start_year': Int(), 'end_year': Int()
            })
        ),
        'entity_squad_link': GroupBy('entity_squad_links', Entity('entity_id', {
            'squad_id': Int(), 'squad_position': Int(), 'entity_id': Int(), 'start_year': Int()
        })),
        'hf_skill': GroupBy('hf_skills', Entity('skill', {
            'skill': Str(), 'total_ip': Int()
        })),
        'relationship_profile_hf_visual': GroupBy('relationship_profile_hf_visuals', Entity('hfid', {
            'hfid': Int(), 'meet_count': Int(), 'last_meet_year': Int(), 'last_meet_seconds72': Int(),
            'known_identity_id': Int(), 'rep_friendly': Int(), 'love': Int(), 'trust': Int(),
            'loyalty': Int(), 'fear': Int(), 'respect': Int(), 'hf_id': Int(), 'rep_information_source': Int()
        })),
        'intrigue_actor': GroupBy('intrigue_actors', Entity('hfid', {
            'local_id': Int(), 'hfid': Int(), 'role': Str(), 'strategy': Str(), 'entity_id': Int(),
            'promised_me_immortality': Bool(), 'promised_actor_immortality': Bool(), 'handle_actor_id': Int(),
            'strategy_enid': Int(), 'strategy_eppid': Int()
        })),
        'intrigue_plot': GroupBy('intrigue_plots', Entity('local_id', {
            'local_id': Int(), 'type': Str(), 'on_hold': Bool(), 'entity_id': Int(), 'actor_id': Int(),
            'artifact_id': Int(), 'plot_actor': GroupBy('plot_actors', Entity('actor_id', {
                'actor_id': Int(), 'plot_role': Str(), 'agreement_id': Int(), 'agreement_has_messenger': Bool()
            })),
            'delegated_plot_id': Int(), 'delegated_plot_hfid': Int(),
            'parent_plot_id': Int(), 'parent_plot_hfid': Int()
        })),
        'entity_reputation': GroupBy('entity_reputations', Entity('entity_id', {
            'entity_id': Int(), 'first_ageless_year': Int(), 'first_ageless_season_count': Int(),
            'unsolved_murders': Int()
        })),
        'used_identity_id': GroupBy('used_identity_ids', Entity('entity_id', {
            'entity_id': Int(), 'first_ageless_year': Int(), 'first_ageless_season_count': Int()
        })),
        'relationship_profile_hf_historical': GroupBy('relationship_profiles_hf_historical', Entity('hf_id', {
            'hf_id': Int(), 'love': Int(), 'respect': Int(), 'trust': Int(), 'loyalty': Int(), 'fear': Int()
        })),
        'honor_entity': GroupBy('honor_entities', Entity('entity', {
            'entity': Int(), 'battles': Int(), 'kills': Int(), 'honor_id': GroupBy('honor_ids', Int())
        })),
        'site_property': GroupBy('site_properties', Entity('site_id', {
            'site_id': Int(), 'property_id': Int()
        }))
    }))
}
