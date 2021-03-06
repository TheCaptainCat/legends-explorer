from legends_explorer.legends import Collection
from legends_explorer.legends.types import (
    Int, Str, Rectangle, Coordinates, List, GroupBy, Bool, SplitStr,
    LinkToPreviousGroupBy, Entity, Population, Path, GroupTree, Wrap
)

definitions = {
    'regions': Collection('regions', Entity('id', {
        'id': Int(), 'name': Str(), 'type': Str(), 'coords': Path(), 'evilness': Str(), 'force_id': Int()
    })),
    'underground_regions': Collection('underground_regions', Entity('id', {
        'id': Int(), 'type': Str(), 'depth': Int(), 'coords': Path()
    })),
    'landmasses': Collection('landmasses', Entity('id', {
        'id': Int(), 'name': Str(), 'coord_1': Coordinates(), 'coord_2': Coordinates()
    })),
    'mountain_peaks': Collection('mountain_peaks', Entity('id', {
        'id': Int(), 'name': Str(), 'coords': Coordinates(), 'height': Int(), 'is_volcano': Bool()
    })),
    'rivers': Collection('rivers', Entity('name', {
        'name': Str(), 'path': Path(points=5), 'end_pos': Coordinates()
    })),
    'sites': Collection('sites', Entity('id', {
        'id': Int(), 'type': Str(), 'name': Str(), 'coords': Coordinates(), 'rectangle': Rectangle(),
        'civ_id': Int(), 'cur_owner_id': Int(),
        'structures': List(Entity('id', {
            'id': Int(), 'type': Str(), 'name': Str(), 'name2': Str(), 'entity_id': Int(), 'deity': Int(),
            'subtype': Str(), 'owner_hfid': Int(), 'worship_hfid': Int(), 'deity_type': Int(),
            'inhabitant': GroupBy('inhabitants', Int()), 'religion': Int(), 'dungeon_type': Int(),
            'copied_artifact_id': GroupBy('copied_artifact_ids', Int())
        }, transforms={'local_id': 'id'})),
        'site_properties': List(Entity('id', {
            'id': Int(), 'structure_id': Int(), 'type': Str(), 'owner_hfid': Int()
        }))
    })),
    'world_constructions': Collection('world_constructions', Entity('id', {
        'id': Int(), 'name': Str(), 'type': Str(), 'coords': Path()
    })),
    'artifacts': Collection('artifacts', Entity('id', {
        'id': Int(), 'name': Str(), 'site_id': Int(), 'holder_hfid': Int(), 'mat': Str(), 'item_type': Str(),
        'structure_local_id': Int(), 'subregion_id': Int(), 'item_description': Str(), 'page_count': Int(),
        'abs_tile_x': Str(), 'abs_tile_y': Str(), 'abs_tile_z': Str(), 'writing': Int(), 'item_subtype': Str(),
        'item': Entity('name_string', {
            'name_string': Str(), 'page_number': Int(), 'page_written_content_id': Int(),
            'writing_written_content_id': Int()
        })
    })),
    "historical_figures": Collection('historical_figures', Entity('id', {
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
    })),
    'entity_populations': Collection('entity_populations', Entity('id', {
        'id': Int(), 'race': Population(), 'civ_id': Int()
    })),
    'entities': Collection('entities', Entity('id', {
        'id': Int(), 'name': Str(), 'race': Str(), 'type': Str(), 'worship_id': Int(), 'profession': Str(),
        'histfig_id': GroupBy('histfig_ids', Int()), 'weapon': GroupBy('weapons', Str()),
        'child': GroupBy('children', Int()), 'claims': Path(),
        'honor': GroupBy('honors', Entity('id', {
            'id': Int(), 'name': Str(), 'gives_precedence': Int(), 'requires_any_melee_or_ranged_skill': Bool(),
            'required_skill_ip_total': Int(), 'required_battles': Int(), 'exempt_epid': Int(),
            'exempt_former_epid': Int(), 'required_skill': Str(), 'required_kills': Int(),
            'granted_to_everybody': Bool(), 'required_years': Int()
        })),
        'entity_position_assignment': GroupBy('entity_position_assignments', Entity('id', {
            'id': Int(), 'histfig': Int(), 'position_id': Int(), 'squad_id': Int()
        })),
        'entity_position': GroupBy('entity_positions', Entity('id', {
            'id': Int(), 'name': Str(), 'name_male': Str(), 'name_female': Str(), 'spouse': Str(),
            'spouse_male': Str(), 'spouse_female': Str()
        })),
        'entity_link': GroupBy('entity_links', Entity('target', {
            'type': Str(), 'target': Int(), 'strength': Int()
        })),
        'occasion': GroupBy('occasions', Entity('id', {
            'id': Int(), 'name': Str(), 'event': Int(),
            'schedule': GroupBy('schedules', Entity('id', {
                'id': Int(), 'type': Str(), 'reference': Int(), 'reference2': Int(),
                'item_type': Str(), 'item_subtype': Str(),
                'feature': GroupBy('features', Entity('type', {
                    'type': Str(), 'reference': Int()
                }))
            }))
        }))
    })),
    'creature_raw': Collection('creature_raw', Entity('creature_id', {
        'creature_id': Str(), 'name_singular': Str(), 'name_plural': Str(), 'mundane': Bool(), 'mates_to_breed': Bool(),
        'vermin_': GroupTree('vermin_', 1, Bool()), 'two_genders': Bool(), 'has_male': Bool(), 'has_female': Bool(),
        'small_race': Bool(), 'biomes_': GroupTree('biome_', 3, Bool()), 'has_any_': GroupTree('has_any_', 1, Bool()),
        'all_castes_alive': Bool(), 'large_roaming': Bool(), 'savage': Bool(), 'ubiquitous': Bool(), 'good': Bool(),
        'loose_clusters': Bool(), 'equipment': Bool(), 'equipment_wagon': Bool(), 'fanciful': Bool(), 'evil': Bool(),
        'does_not_exist': Bool(), 'artificial_hiveable': Bool(), 'occurs_as_entity_race': Bool(), 'generated': Bool()
    })),
    'identities': Collection('identities', Entity('id', {
        'id': Int(), 'name': Str(), 'histfig_id': Int(), 'birth_year': Int(), 'birth_second': Int(), 'entity_id': Int(),
        'profession': Str(), 'caste': Str(), 'race': Str(), 'nemesis_id': Int()
    })),
    'historical_events': Collection('historical_events', Entity('id', {
        'id': Int(), 'year': Int(), 'seconds72': Int(), 'type': Str(), 'hfid': GroupBy('hfids', Int()), 'state': Str(),
        'subregion_id': Int(), 'feature_layer_id': Int(), 'coords': Coordinates(), 'position_id': Int(), 'link': Str(),
        'civ_id': Int(), 'artifact_id': Int(), 'dest_entity_id': Int(), 'source_site_id': Int(), 'unit_id': Int(),
        'source_structure_id': Int(), 'source_entity_id': Int(), 'from_original': Bool(), 'identity_id': Int(),
        'trickster_hfid': Int(), 'hist_figure_id': Int(), 'reason': Str(), 'reason_id': Int(), 'slayer_hfid': Int(),
        'slayer_item_id': Int(), 'slayer_shooter_item_id': Int(), 'cause': Str(), 'slayer_race': Str(), 'action': Str(),
        'slayer_caste': Str(), 'agreement_id': Int(), 'successful': Bool(), 'failed_judgment_test': Bool(),
        'method': Str(), 'top_facet': Str(), 'top_facet_rating': Int(), 'top_facet_modifier': Int(), 'site_id': Int(),
        'ally_defense_bonus': Int(), 'top_value': Str(), 'top_value_rating': Int(), 'top_value_modifier': Int(),
        'student_hfid': Int(), 'teacher_hfid': Int(), 'interaction': Str(), 'hfid_target': Int(), 'wc_id': Int(),
        'honor_id': Int(), 'target_enid': Int(), 'entity_id': Int(), 'target_hfid': Int(), 'corruptor_hfid': Int(),
        'target_seen_as': Str(), 'corruptor_seen_as': Str(), 'unit_type': Str(), 'hf_rep_1_of_2': Str(),
        'hf_rep_2_of_1': Str(), 'identity_id1': Int(), 'identity_id2': Int(), 'hfid1': Int(), 'hfid2': Int(),
        'winner_hfid': Int(), 'competitor_hfid': GroupBy('competitor_hfids', Int()), 'occasion_id': Int(),
        'schedule_id': Int(), 'gambler_hfid': Int(), 'structure_id': Int(), 'old_account': Int(),
        'new_account': Int(), 'claim': Str(), 'knowledge': SplitStr(':'), 'delegated': Bool(), 'inherited': Bool(),
        'giver_hist_figure_id': Int(), 'giver_entity_id': Int(), 'receiver_hist_figure_id': Int(), 'return': Bool(),
        'receiver_entity_id': Int(), 'building_profile_id': Int(), 'acquirer_hfid': Int(), 'purchased_unowned': Bool(),
        'rebuilt_ruined': Bool(), 'secret_goal': Str(), 'form_id': Int(), 'position_profile_id': Int(),
        'circumstance_id': Int(), 'seeker_hfid': Int(), 'relationship': Str(), 'entity_1': Int(), 'entity_2': Int(),
        'speaker_hfid': Int(), 'site_hfid': Int(), 'joiner_entity_id': GroupBy('joiner_entity_ids', Int()),
        'surveiled_convicted': Bool(), 'implicated_hfid': GroupBy('implicated_hfids', Int()), 'trader_hfid': Int(),
        'dest_site_id': Int(), 'production_zone_id': Int(), 'allotment': Int(), 'allotment_index': Int(),
        'account_shift': Int(), 'hist_fig_id': Int(), 'convicted_hfid': Int(), 'convicter_enid': Int(),
        'crime': Str(), 'prison_months': Int(), 'fooled_hfid': Int(), 'framer_hfid': Int(), 'death_penalty': Bool(),
        'wrongful_conviction': Bool(), 'subtype': Str(), 'group_1_hfid': Int(), 'joined_entity_id': Int(),
        'group_2_hfid': GroupBy('group_2_hfids', Int()), 'topic': Str(), 'relevant_position_profile_id': Int(),
        'group_hfid': GroupBy('group_hfids', Int()), 'target_identity': Int(), 'leader_hfid': Int(),
        'site_civ_id': Int(), 'confessed_after_apb_arrest_enid': Int(), 'interrogator_hfid': Int(),
        'top_relationship_rating': Int(), 'top_relationship_modifier': Int(), 'name_only': Bool(),
        'partial_incorporation': Bool(), 'situation': Str(), 'shrine_amount_destroyed': Int(), 'detected': Bool(),
        'dest_structure_id': Int(), 'wounder_hfid': Int(), 'woundee_hfid': Int(), 'attacker_civ_id': Int(),
        'defender_civ_id': Int(), 'attacker_general_hfid': Int(), 'defender_general_hfid': Int(), 'wcid': Int(),
        'attacker_merc_enid': Int(), 'first': Bool(), 'quality': Int(), 'snatcher_hfid': Int(), 'ransomed_hfid': Int(),
        'ransomer_hfid': Int(), 'payer_hfid': Int(), 'moved_to_site_id': Int(), 'body_state': Str(),
        'builder_hfid': Int(), 'resident_civ_id': Int(), 'mood': Str(), 'persecutor_hfid': Int(), 'master_wcid': Int(),
        'persecutor_enid': Int(), 'site_id1': Int(), 'site_id2': Int(), 'relevant_entity_id': Int(),
        'last_owner_hfid': Int(), 'actor_hfid': Int(), 'doer_hfid': Int(), 'attacker_hfid': Int(),
        'expelled_hfid': GroupBy('expelled_hfids', Int()), 'instigator_hfid': Int(), 'pos_taker_hfid': Int(),
        'property_confiscated_from_hfid': GroupBy('property_confiscated_from_hfids', Int()),
        'expelled_creature': GroupBy('expelled_creatures', Wrap('creature', Int())), 'changee_hfid': Int(),
        'expelled_pop_id': LinkToPreviousGroupBy('expelled_creatures', 'pop_id', Int()), 'join_entity_id': Int(),
        'expelled_number': LinkToPreviousGroupBy('expelled_creatures', 'number', Int()), 'changer_hfid': Int(),
        'dispute': Str(), 'entity_id_1': Int(), 'entity_id_2': Int(), 'site_id_1': Int(), 'site_id_2': Int(),
        'pop_': GroupTree('pop_', 1, Int()), 'old_race': Str(), 'old_caste': Str(), 'new_race': Str(),
        'new_caste': Str(), 'top_relationship_factor': Str(), 'corrupt_convicter_hfid': Int(), 'plotter_hfid': Int(),
        'initiating_enid': Int(), 'joining_enid': GroupBy('joining_enids', Int()), 'arresting_enid': Int(),
        'wanted_and_recognized': Bool(), 'held_firm_in_interrogation': Bool(), 'lure_hfid': Int(),
        'coconspirator_bonus': Int(), 'site_entity_id': Int(), 'civ_entity_id': Int(), 'new_site_civ_id': Int(),
        'relevant_id_for_method': Int(), 'acquirer_enid': Int(), 'defender_merc_enid': Int(), 'creator_hfid': Int(),
        'coconspirator_hfid': Int(), 'surveiled_coconspirator': Bool(), 'convict_is_contact': Bool(),
        'new_leader_hfid': Int(), 'exiled': Bool(), 'contact_hfid': Int(), 'surveiled_contact': Bool(),
        'trader_entity_id': Int(), 'religion_id': Int(), 'corruptor_identity': Int(), 'overthrown_hfid': Int(),
        'new_equipment_level': Int(), 'conspirator_hfid': GroupBy('conspirator_hfids', Int()),
        'did_not_reveal_all_in_interrogation': Bool(), 'destroyed_structure_id': Int(), 'd_support_merc_enid': Int(),
        'modifier_hfid': Int(), 'modification': Str(), 'a_support_merc_enid': Int(), 'rebuilt': Bool(),
        'law_add': Str(), 'law_remove': Str(), 'disturbance': Bool(), 'surveiled_target': Bool(), 'position': Str(),
        'site_property_id': Int(), 'destroyer_enid': Int(), 'saboteur_hfid': Int(), 'site': Int(), 'structure': Int(),
        'histfig': Int(), 'civ': Int(), 'link_type': Str(), 'new_job': Str(), 'old_job': Str(), 'appointer_hfid': Int(),
        'promise_to_hfid': Int(), 'trickster': Int(), 'identity_histfig_id': Int(), 'identity_name': Str(),
        'target': Int(), 'slayer_hf': Int(), 'death_cause': Str(), 'victim_hf': Int(), 'item_type': Str(), 'mat': Str(),
        'entity': Int(), 'item': Int(), 'stash_site': Int(), 'theft_method': Str(), 'item_subtype': Str(),
        'creator_unit_id': Int(), 'hf': Int(), 'hf_target': Int(), 'victim': Int(), 'race': Str(), 'caste': Str(),
        'part_lost': Bool(), 'eater': Int(), 'wounder': Int(), 'woundee': Int(), 'woundee_race': Int(),
        'woundee_caste': Int(), 'body_part': Int(), 'injury_type': Str(), 'site_civ': Int(), 'builder_hf': Int(),
        'rebuild': Bool(), 'changee': Int(), 'changer': Int(), 'pets': Str(), 'group': Int(),
        'identity_nemesis_id': Int(), 'identity_race': Str(), 'identity_caste': Str(), 'mattype': Int(),
        'victim_entity': Int(), 'abuse_type': Str(), 'pile_type': Str(), 'bodies': GroupBy('bodies_list', Int()),
        'source': Int(), 'destination': Int(), 'matindex': Int(), 'student': Int(), 'teacher': Int(),
        'artifact': Int(), 'secret_text': Str(), 'tree': Int(), 'item_mat': Str(), 'interaction_action': Str(),
        'doer': Int(), 'sanctify_hf': Int(), 'region': Int(),
        'circumstance': Entity('type', {'type': Str(), 'hist_event_collection': Int()})
    }))
}
