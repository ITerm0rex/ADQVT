# %%
import pympi.Elan as Elan


file = r".\HCI-2023\Annotated_Data_ELAN\V3\event_elan_data\s2_v3_-_matchmaker_scene\Template_s2_v3_-_matchmaker_scene.eaf"
# file = r".\HCI-2023\Annotated_Data_ELAN\V3\eyetracking_elan_data\s2_v3_-_matchmaker_scene\Template_s2_v3_-_matchmaker_scene_Group_C_participant_1_playlist_3.eaf"


data = Elan.Eaf(file)

tiers = data.get_tier_names()


tier = list(tiers)[0]
# tier2 = list(tiers)[4]

print(data.get_child_tiers_for(tier))


print(data.get_tier_names())
print()

# print(tier2)

# for x in data.get_gaps_and_overlaps2(tier, tier2):
#     print(x)
#     print(data.get_tier_ids_for_linguistic_type(x[2]))

# print(data.get_annotation_data_after_time(tier, 0))


print(file)

print(data.get_linked_files())
print()

print(data.get_controlled_vocabulary_names())
print()

print(data.get_external_ref_names())
print()

print(data.get_languages())
print()

print(data.get_properties())
print()

print(data.get_tier_ids_for_linguistic_type("HandAction"))
print()


print(data.get_linguistic_type_names())
