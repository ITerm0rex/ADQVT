# %%
import pympi.Elan as Elan


file = r".\HCI-2023\Annotated_Data_ELAN\V3\event_elan_data\s2_v3_-_matchmaker_scene\Template_s2_v3_-_matchmaker_scene.eaf"

data = Elan.Eaf(file)


print(data.get_linked_files())
print(data.get_controlled_vocabulary_names())
