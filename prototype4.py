import itertools
import json
import matplotlib.pyplot as plt
import os


def get_class_instances(data, class_name) -> list:
    annotations = data["annotations"]
    for annotation in annotations:
        if annotation["class"] == class_name:
            return annotation["instances"]
    return []


def fetch_actor_data(actor_directory):
    actor_data = {}
    for filename in os.listdir(actor_directory):
        if filename.endswith(".png"):
            short_name, long_name = filename.split(" - ", 1)
            short_name = short_name.strip()
            long_name = long_name[:-4].strip()  # Remove the ".png" extension
            actor_data[short_name] = long_name
    return actor_data


def get_unique_holds_by_class(data):
    unique_holds_by_class = {}
    for annotation in data["annotations"]:
        class_name = annotation["class"]
        holds_values = set()
        for instance in annotation["instances"]:
            holds_value = instance.get("holds")
            if holds_value is not None:
                holds_values.add(holds_value)
        unique_holds_by_class[class_name] = list(holds_values)
    return unique_holds_by_class


class Graph_Generator:
    def __init__(self, json_file, actors):
        self.json_file = json_file
        self.actors = actors
        self.data = self.load_data()

    def load_data(self):
        with open(self.json_file, "r") as file:
            data = json.load(file)
        return data


class Graph_Individual(Graph_Generator):
    def __init__(self, json_file, actors, actor_name, actions):
        super().__init__(json_file, actors)
        self.actor_name = actor_name
        self.actions = actions

    def calculate_action_durations(self):
        durations = []
        for action in self.actions:
            sum_action = 0
            for annotation in self.data["annotations"]:
                for instance in annotation["instances"]:
                    if self.actor_name in instance["arguments"].values() and instance["holds"] == action:
                        sum_action += instance["end"] - instance["start"]
            durations.append(sum_action / 1e3)
        return durations, "Seconds"

    def plot_actor_durations(self):
        data, unit = self.calculate_action_durations()
        plt.bar(self.actions, data, label=f"{self.actors[self.actor_name]}: Actor {unit}")
        plt.xlabel("Actions")
        plt.ylabel(f"{unit}")
        plt.title(f"{self.actors[self.actor_name]}: Actor {unit}")
        plt.legend()
        plt.show()


class Graph_Simultaneous(Graph_Generator):
    def __init__(self, json_file, actors, actor_names, actions):
        super().__init__(json_file, actors)
        self.actor_names = actor_names
        self.actions = actions

    def calculate_action_durations(self):
        durations = []
        for action in self.actions:
            total_overlap_duration = 0
            actor_times = {actor: [] for actor in self.actor_names}  # Dictionary to store start and end times for each actor

            for annotation in self.data["annotations"]:
                for instance in annotation["instances"]:
                    if instance["holds"] == action and instance["arguments"]["argument1"] in self.actor_names:
                        actor_name = instance["arguments"]["argument1"]
                        start_time = instance["start"]
                        end_time = instance["end"]
                        actor_times[actor_name].append({"start": start_time, "end": end_time})

            # Calculate the total overlap duration for each unique pair of actors
            # print(list(itertools.combinations(set(self.actor_names).union(["aaa"]), 2)))
            for actor1, actor2 in itertools.combinations(self.actor_names, 2):
                times1 = actor_times[actor1]
                times2 = actor_times[actor2]

                for time1 in times1:
                    for time2 in times2:
                        # Determine overlap by comparing start and end times
                        overlap_start = max(time1["start"], time2["start"])
                        overlap_end = min(time1["end"], time2["end"])

                        # Calculate and accumulate the duration if there is an overlap
                        overlap_duration = max(0, overlap_end - overlap_start)
                        total_overlap_duration += overlap_duration

            # Append the total overlap duration for the current action to the durations list
            durations.append(total_overlap_duration / 1e3)  # Convert milliseconds to seconds

        # Return a tuple containing the durations list and the string "Seconds"
        return durations, "Seconds"

    def plot_actor_durations(self):
        data, unit = self.calculate_action_durations()
        plt.bar(self.actions, data, label=f"{', '.join([self.actors[actor] for actor in self.actor_names])}: Actor {unit}")
        plt.xlabel("Actions")
        plt.ylabel(f"{unit}")
        plt.title(f"{', '.join([self.actors[actor] for actor in self.actor_names])}: Actor {unit}")
        plt.legend()
        plt.show()


class Graph_Action_Analyzer(Graph_Generator):
    def __init__(self, json_file, actors):
        super().__init__(json_file, actors)

    def calculate_action_durations(self, class_name, action):
        durations = []
        for actor in self.actors.keys():
            sum_action = 0
            for annotation in self.data["annotations"]:
                if annotation["class"] == class_name:
                    for instance in annotation["instances"]:
                        if actor in instance["arguments"].values() and instance["holds"] == action:
                            sum_action += instance["end"] - instance["start"]
            durations.append(sum_action / 1e3)
        return durations, "Seconds"

    def plot_actor_durations_for_action(self, class_name, action):
        data, unit = self.calculate_action_durations(class_name, action)

        actor_names_full = [self.actors[short_name] for short_name in self.actors.keys()]

        plt.bar(actor_names_full, data, label=f"{class_name}: {action} Durations")
        plt.xlabel("Actors")
        plt.ylabel(f"{unit}")
        plt.title(f"{class_name}: {action} Durations")
        plt.legend()
        plt.show()

# VIDEOSNIPPETS

class VideoSnippets:
    def __init__(self, json_file, actors_data):
        self.json_file = json_file
        self.actors_data = actors_data
        self.data = self.load_data()

    def load_data(self):
        with open(self.json_file, "r") as file:
            data = json.load(file)
        return data

    def get_class_instances(self, class_name) -> list:
        annotations = self.data["annotations"]
        for annotation in annotations:
            if annotation["class"] == class_name:
                return annotation["instances"]
        return []

    class VideoSnippetsIndividual:
        def __init__(self, data, actor_name, action):
            self.data = data
            self.actor_name = actor_name
            self.action = action

        def get_time_snippets(self):
            time_snippets = []
            for annotation in self.data["annotations"]:
                for instance in annotation["instances"]:
                    if self.actor_name in instance["arguments"].values() and instance["holds"] == self.action:
                        time_snippets.append({"start": instance["start"], "end": instance["end"]})
            return time_snippets

    class VideoSnippetsSimultaneous:
        def __init__(self, data, actor_names, action):
            self.data = data
            self.actor_names = actor_names
            self.action = action

        def get_time_snippets(self):
            time_snippets = []
            actor_times = {actor: [] for actor in self.actor_names}

            for annotation in self.data["annotations"]:
                for instance in annotation["instances"]:
                    if instance["holds"] == self.action and instance["arguments"]["argument1"] in self.actor_names:
                        actor_name = instance["arguments"]["argument1"]
                        start_time = instance["start"]
                        end_time = instance["end"]
                        actor_times[actor_name].append({"start": start_time, "end": end_time})

            for actor1, actor2 in itertools.combinations(self.actor_names, 2):
                times1 = actor_times[actor1]
                times2 = actor_times[actor2]

                for time1 in times1:
                    for time2 in times2:
                        overlap_start = max(time1["start"], time2["start"])
                        overlap_end = min(time1["end"], time2["end"])

                        if overlap_end > overlap_start:
                            time_snippets.append({"start": overlap_start, "end": overlap_end})

            return time_snippets

if __name__ == "__main__":
    json_file_name = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"

    actor_directory = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\characters_of_interest"

    with open(json_file_name, "r") as file:
        data = json.load(file)

    unique_holds_by_class = get_unique_holds_by_class(data)

    actors_data = fetch_actor_data(actor_directory)

    # Example usage for Graph_Individual
    actor_name_individual = "ann"
    actions_individual = ["moving", "stationary", "turning_away", "turning_towards", "turning"]

    graph_individual = Graph_Individual(json_file_name, actors_data, actor_name_individual, actions_individual)
    graph_individual.plot_actor_durations()

    # Example usage for Graph_Simultaneous
    actor_names_simultaneous = ["ann", "dai"]
    actions_simultaneous = ["moving", "stationary", "turning_away", "turning_towards", "turning", "Visibility"]

    graph_simultaneous = Graph_Simultaneous(json_file_name, actors_data, actor_names_simultaneous, actions_simultaneous)
    graph_simultaneous.plot_actor_durations()

    # Example usage for Graph_Action_Analyzer
    class_name_action_analyzer = "Visibility"
    action_action_analyzer = "Visibility"

    graph_action_analyzer = Graph_Action_Analyzer(json_file_name, actors_data)
    graph_action_analyzer.plot_actor_durations_for_action(class_name_action_analyzer, action_action_analyzer)

    video_snippets = VideoSnippets(json_file_name, actors_data)

    # Example usage for VideoSnippetsIndividual
    actor_name_individual = "ann"
    action_individual = "Visibility"
    snippets_individual = video_snippets.VideoSnippetsIndividual(data, actor_name_individual, action_individual).get_time_snippets()
    print(f"{actor_name_individual} doing {action_individual}: {snippets_individual}")

    # Example usage for VideoSnippetsSimultaneous
    actor_names_simultaneous = ["ann", "dai"]
    action_simultaneous = "Visibility"
    snippets_simultaneous = video_snippets.VideoSnippetsSimultaneous(data, actor_names_simultaneous, action_simultaneous).get_time_snippets()
    print(f"{', '.join(actor_names_simultaneous)} doing {action_simultaneous} simultaneously: {snippets_simultaneous}")