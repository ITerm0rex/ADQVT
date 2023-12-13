# %%
import pympi.Elan as Elan


file = r".\HCI-2023\Annotated_Data_ELAN\V3\event_elan_data\s2_v3_-_matchmaker_scene\Template_s2_v3_-_matchmaker_scene.eaf"

data = Elan.Eaf(file)

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
