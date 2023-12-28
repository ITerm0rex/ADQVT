# %%
import json
from os.path import sep
import os.path
from contextlib import redirect_stdout
import random

from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], f"{y[i]:.2f}", ha="center")


def obj_hash(obj: object):
    return hash(json.dumps(obj))


class query_time_total:
    def set(self, filenames: list[str] = [], set_class="Gaze", set_holds="looking_at"):
        self.filenames = filenames
        self.set_class = set_class
        self.set_holds = set_holds
        return self

    def create(self):
        filename = self.filenames[0]

        with open(filename) as file:
            json_data = json.load(file)
            annotations = json_data["annotations"]
            query_list = [
                [
                    i["holds"],
                    (i["end"] - i["start"]) / 1e3,
                    i["arguments"],
                    {"start": i["start"], "end": i["end"]},
                ]
                for x in annotations
                for i in x["instances"]
                if (x["class"] == self.set_class and i["holds"] == self.set_holds)
            ]

            query_hash = {obj_hash(tuple(x[2].values())): x[2] for x in query_list}

            query_total = {
                tuple(v.values()): sum(
                    [g[1] for g in query_list if obj_hash(tuple(g[2].values())) == h]
                )
                for (h, v) in query_hash.items()
            }

            self.query_list = query_list
            self.query_hash = query_hash
            self.query_total = query_total
            self.filename = filename
            return self

    def show(self):
        # fig = plt.figure()
        fig = plt.gcf()
        fig.set_size_inches(*(fig.get_size_inches() * 2))
        # plt.autoscale()
        plt.title(self.filename)
        plt.xlabel(f"{self.set_holds}(...)")
        # plt.subplots_adjust(wspace=9, left=9, right=10)
        # plt.margins(5)
        plt.ylabel(f"Number of seconds total {self.set_holds}(...)")
        bars = (
            list(f"({', '.join(x)})" for x in self.query_total.keys()),
            list(self.query_total.values()),
        )
        # bc = plt.bar(*bars, width=2)
        # plt.bar_label(bc, [f"{b:.2f}" for b in bars[1]])
        # addlabels(*bars)

        plt.barh(*bars)
        # plt.subplot_tool()
        # plt.subplots_adjust(left=0.1, right=3.0, top=0.9, bottom=0.1)
        # plt.show()
        return self



# p1->r:f
# a->r:f

# |.....|         |..............|
#     |..|                |.........|


class query_count_total:
    def set(self, filenames: list[str] = [], set_class="Gaze", set_holds="looking_at"):
        self.filenames = filenames
        self.set_class = set_class
        self.set_holds = set_holds
        return self

    def create(self):
        filename = self.filenames[0]

        with open(filename) as file:
            json_data = json.load(file)
            annotations = json_data["annotations"]
            query_list = [
                [
                    i["holds"],
                    (i["end"] - i["start"]) / 1e3,
                    i["arguments"],
                    {"start": i["start"], "end": i["end"]},
                ]
                for x in annotations
                for i in x["instances"]
                if (x["class"] == self.set_class and i["holds"] == self.set_holds)
            ]

            query_hash = {obj_hash(tuple(x[2].values())): x[2] for x in query_list}

            query_total = {
                tuple(v.values()): sum(
                    [g[1] for g in query_list if obj_hash(tuple(g[2].values())) == h]
                )
                for (h, v) in query_hash.items()
            }

            self.query_list = query_list
            self.query_hash = query_hash
            self.query_total = query_total
            self.filename = filename
            return self

    def show(self):
        # fig = plt.figure()
        fig = plt.gcf()
        fig.set_size_inches(*(fig.get_size_inches() * 2))
        # plt.autoscale()
        plt.title(self.filename)
        plt.xlabel(f"{self.set_holds}(...)")
        # plt.subplots_adjust(wspace=9, left=9, right=10)
        # plt.margins(5)
        plt.ylabel(f"Number of seconds total {self.set_holds}(...)")
        bars = (
            list(f"({', '.join(x)})" for x in self.query_total.keys()),
            list(self.query_total.values()),
        )
        # bc = plt.bar(*bars, width=2)
        # plt.bar_label(bc, [f"{b:.2f}" for b in bars[1]])
        # addlabels(*bars)

        plt.barh(*bars)
        # plt.subplot_tool()
        # plt.subplots_adjust(left=0.1, right=3.0, top=0.9, bottom=0.1)
        # plt.show()
        return self


def main():
    anot_path = r"\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
    anot_path = "." + anot_path.replace(sep, "/")
    anot_name = os.path.basename(anot_path)

    c_path = r"\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\stimulus_info.jscsrc"
    c_path = "." + c_path.replace(sep, "/")
    c_name = os.path.basename(c_path)

    with (
        open(anot_path) as fp,
        open(c_path) as fc,
        open("test-out.txt", "w") as f,
        redirect_stdout(f),
    ):
        json_data = json.load(fp)
        characters = json.load(fc)

        shorts = list(c["short"] for c in characters["entities"])

        annotations = json_data["annotations"]

        # forAll a,b in p , gaze(a, b) and stationary(b) and speacing(a)
        # sum() for a,b in p , gaze(a, b) and stationary(b) and speacing(a)
        #   for cls in annotations , stationary(a)

        stationary_list = [
            [
                [i["holds"], (i["end"] - i["start"]) / 1e3, i["arguments"]]
                for x in annotations
                for i in x["instances"]
                if (
                    x["class"] == "Motion"
                    and i["holds"] == "stationary"
                    and name in i["arguments"].values()
                )
            ]
            for name in shorts
        ]

        stationary_total = [sum([y[1] for y in x]) for x in stationary_list]

        gaze_list = [
            [
                i["holds"],
                (i["end"] - i["start"]) / 1e3,
                i["arguments"],
                {"start": i["start"], "end": i["end"]},
            ]
            for x in annotations
            for i in x["instances"]
            if (x["class"] == "Gaze" and i["holds"] == "looking_at")
        ]

        gaze_hash = {obj_hash(tuple(x[2].values())): x[2] for x in gaze_list}

        gaze_total = {
            tuple(v.values()): sum(
                [g[1] for g in gaze_list if obj_hash(tuple(g[2].values())) == h]
            )
            for (h, v) in gaze_hash.items()
        }

        opti = {"sep": "\n", "end": "\n" * 2, "file": None, "flush": False}

        if False:
            # from datetime import timedelta
            # import datetime
            # import time

            # print(datetime.timedelta())
            # time.gmtime()
            # t0 = datetime.datetime.now()

            # time.sleep(1)

            # t1 = datetime.datetime.now().replace(year=2022)

            # print((t1-t0).total_seconds())

            # print(datetime.time())
            # print(datetime.date.timetuple())

            return

        print(*gaze_total.items(), **opti)

        print(*gaze_hash.items(), **opti)

        print(*gaze_list, **opti)

        print(*stationary_list, **opti)

        print(stationary_total, **opti)

        print(json.dumps(json_data, indent=1), **opti)

        fig = plt.figure()
        fig.set_size_inches(*(fig.get_size_inches() * 0.8))
        plt.title(anot_name)
        plt.xlabel("looking_at(a, b)")
        plt.ylabel("Number of seconds total looking_at(a, b)")
        bars = (
            list(f"({x[0]}, {x[1]})" for x in gaze_total.keys()),
            list(gaze_total.values()),
        )
        bc = plt.bar(*bars)
        # plt.bar_label(bc, [f"{b:.2f}" for b in bars[1]])
        addlabels(*bars)

        fig.tight_layout(pad=0.2)
        fig.savefig(os.path.join("mic", "looking_at.png"))
        plt.show()

        # fig, ax = plt.subplots()
        # bar = ax.bar(*bars)
        # ax.bar_label(bar)
        # # plt.bar_label(ax, bar)
        # fig.show()
        # # plt.show()
        # fig.waitforbuttonpress()

        # return
        # raise Exception("plt")

        fig = plt.figure()
        fig.set_size_inches(*(fig.get_size_inches() * 0.8))
        plt.title(anot_name + "\n" + c_name)
        plt.xlabel("Names")
        plt.ylabel("Number of seconds stationary")
        bars = (
            # list(f"{x[1]:.2f} : " + x[0] for x in zip(shorts, stationary_total)),
            shorts,
            stationary_total,
        )
        plt.bar(*bars)
        addlabels(*bars)

        fig.tight_layout(pad=0.2)
        fig.savefig(os.path.join("mic", "stationary.png"))
        plt.show()


if __name__ == "__main__":
    main()
