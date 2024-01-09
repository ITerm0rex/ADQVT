import json
import matplotlib.pyplot as plt
import os

def get_class_instances(data, class_name) -> list:
    annotations = data["annotations"]
    for annotation in annotations:
        if annotation["class"] == class_name:
            return annotation["instances"]
    return []

# ui <-> model -> output


class ActionAnalyzer:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.load_data()

    def load_data(self):
        with open(self.json_file, "r") as file:
            data = json.load(file)
        return data

    # def calculate_action_counts(self, actor, action):
    #     count = 0
    #     for annotation in self.data["annotations"]:
    #         for instance in annotation["instances"]:
    #             if actor in instance["arguments"].values():
    #                 if instance["holds"] == action:
    #                     count += 1
    #     return count, "Count"

    # def calculate_action_duration(self, actor, action):
    #     sum_action = 0
    #     for annotation in self.data["annotations"]:
    #         for instance in annotation["instances"]:
    #             if actor in instance["arguments"].values():
    #                 if instance["holds"] == action:
    #                     sum_action += instance["end"] - instance["start"]
    #     return sum_action / 1e3, "Seconds"
    
    def calculate_action_counts(self, actors, action):
        def calculate_action_count(actor):
            count = 0
            for annotation in self.data["annotations"]:
                for instance in annotation["instances"]:
                    if actor in instance["arguments"].values():
                        if instance["holds"] == action:
                            count += 1
            return count
        return [calculate_action_count(actor) for actor in actors], "Count"
    
    def calculate_action_durations(self, actors, action):
        def calculate_action_duration(actor):
            sum_action = 0
            for annotation in self.data["annotations"]:
                for instance in annotation["instances"]:
                    if actor in instance["arguments"].values():
                        if instance["holds"] == action:
                            sum_action += instance["end"] - instance["start"]
            return sum_action / 1e3
        return [calculate_action_duration(actor) for actor in actors], "Seconds"

    def plot_actor_counts_for_action(self, action, actors):
        
        # get_class_instances(self.data, )
        
        # data, unit = [self.calculate_action_duration(actor, action) for actor in actors]
        
        data1, unit1 = self.calculate_action_counts(actors, action)
        data2, unit2 = self.calculate_action_durations(actors, action)
        
        plt.scatter(data1, data2)
        
        # data, unit = self.calculate_action_durations(actors, action)
        # plt.bar(actors, data, color="blue")
        # plt.xlabel("Actors")
        # plt.ylabel(unit)
        # plt.title(f"Actor {unit} for {action}")
        plt.show()


if __name__ == "__main__":
    json_file_name = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
    
    # json_file_name = r".\HCI-2023\Annotated_Data_JSON\V3\eyetracking_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene_Group_C_participant_1_playlist_3.json"

    analyzer = ActionAnalyzer(json_file_name)
    # analyzer.set_actions(['moving', 'stationary', 'turning_away', 'turning_towards', 'turning'])

    # analyzer.set_action('moving')

    # analyzer.set_actors(['rya', 'dai', 'ann'])
    # analyzer.plot()

    # Example: Generate separate plots for each action
    actions = ["moving", "stationary", "turning_away", "turning_towards", "turning"]
    actors = ["rya", "dai", "ann"]
    
    for action in actions:
        analyzer.plot_actor_counts_for_action(action, actors)
