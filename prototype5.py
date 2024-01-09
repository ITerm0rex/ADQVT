import json
import matplotlib.pyplot as plt

import numpy as np


class JSONAnalyzer:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.load_data()

    def load_data(self):
        with open(self.json_file, "r") as file:
            data = json.load(file)
        return data

    def get_unique_actors_in_interval(self, time_interval):
        unique_actors = set()
        for annotation in self.data["annotations"]:
            for instance in annotation["instances"]:
                start_time, end_time = instance["start"], instance["end"]
                if start_time <= time_interval[1] and end_time >= time_interval[0]:
                    act = instance.get("arguments", {}).get("argument1", "")
                    if act:
                        unique_actors.add(act)
        return list(unique_actors)

    def get_unique_actions_in_interval(self, time_interval):
        actions_intervals = {}
        for annotation in self.data["annotations"]:
            for instance in annotation["instances"]:
                holds_value = instance.get("holds", "")
                start_time, end_time = instance["start"], instance["end"]

                # Check if the instance overlaps with or is within the specified interval
                if start_time <= time_interval[1] and end_time >= time_interval[0]:
                    adjusted_start = max(start_time, time_interval[0])
                    adjusted_end = min(end_time, time_interval[1])

                    if holds_value not in actions_intervals:
                        actions_intervals[holds_value] = (adjusted_start, adjusted_end)
                    else:
                        actions_intervals[holds_value] = (
                            max(actions_intervals[holds_value][0], adjusted_start),
                            min(actions_intervals[holds_value][1], adjusted_end),
                        )

        return actions_intervals

    def generate_labeled_plot(self, actions_intervals):
        captions = list(actions_intervals.keys())
        time_intervals = list(actions_intervals.values())

        for i, caption in enumerate(captions):
            for x in [0]:
                plt.plot(np.array(time_intervals[i]) + x, [i, i], label=caption)

        plt.yticks(range(len(captions)), captions)
        plt.xlabel("Time")
        plt.ylabel("Actions")
        plt.title("Actions Overlapping with the Given Interval")
        # plt.legend()
        plt.grid()
        plt.show()


if __name__ == "__main__":
    json_file_name = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
    analyzer = JSONAnalyzer(json_file_name)

    # Example: Choose a time interval
    time_interval = (12000, 50000)
    time_interval = (0, 260000)
    # time_interval = (32000, 50000)
    # time_interval = (32000, 32020)

    # Get unique actors during the interval
    unique_actors = analyzer.get_unique_actors_in_interval(time_interval)
    print("Unique Actors in the Interval:", unique_actors)

    # Choose an actor (replace 'chosen_actor' with an actor from the above list)
    chosen_actor = unique_actors

    # Get unique actions for the chosen actor during the interval
    actions_intervals = analyzer.get_unique_actions_in_interval(time_interval)
    print(f"\nUnique Actions for {chosen_actor} in the Interval:")
    for action, interval in actions_intervals.items():
        print(f"{action}: {interval}")

    # Generate a labeled plot
    analyzer.generate_labeled_plot(actions_intervals)
