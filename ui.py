# %%
import asyncio
from dataclasses import dataclass, field
import glob
import json
import os
import sys
import threading
from typing import Optional
import numpy as np
from matplotlib import pyplot as plt
from nicegui import ui, app
from nicegui import core
from nicegui.logging import log
import webview
import plotly.graph_objects as go
from nicegui import run


from utility import Idempotence

import prototype
# import prototype4
# from prototype import BaseModel

import models
from models import BaseModel



core.app.native.window_args["maximized"] = True
core.app.native.window_args["zoomable"] = True
core.app.native.window_args["text_select"] = True
core.app.native.start_args['debug'] = True


@dataclass
class env_fact:
    file_names: set[str] = field(default_factory=set[str])
    Class: str = "Visibility"
    Hold: str = "Visibility"


env = env_fact()



class UIApp:
    def __init__(self):
        self.file_names: list[str] = list()
        self.select = None
        self.row = None
        self.plt = None
        self.flag = True
        self.num = 0

        self.models: list[BaseModel] = list()

        self.avalible_models: list[BaseModel] = list()
        self.current_model: Optional[BaseModel] = None

    @staticmethod
    def stop():
        app.stop()
        app.shutdown()
        # run.tear_down()

    async def choose_file(self):
        if app.native.main_window:
            if files := await app.native.main_window.create_file_dialog(
                allow_multiple=True,
                # dialog_type=webview.FOLDER_DIALOG,
            ):
                print(files)
                env.file_names.clear()
                env.file_names.update(files)

    @Idempotence
    @ui.refreshable
    def show_plot(self):
        with ui.row() as row:
            row.classes("absolute-right")
            # print(env.file_names)

            if env.file_names == set():
                return

            plot = prototype.query_time_total()

            plot.set(list(env.file_names), env.Class, env.Hold)
            plot.create()
            plot.show2()

    def run_app(self):
        with ui.button("Choose File") as button:
            button.on("click", self.choose_file)

        with ui.select({"a": 1, "b": 2}, multiple=True, clearable=True) as fi:
            fi.on("update:model-value", lambda: print(self.file_names))
            fi.bind_value(self, "file_names")

        with ui.row() as row:
            with ui.select([]) as select:
                select.bind_value(env, "Class")
                select.set_options(
                    ["Visibility", "Gaze", "HumanAction", "Saccade", "Attention"]
                )
                select.set_value("Visibility")

            with ui.select([]) as select:
                select.bind_value(env, "Hold")
                select.set_options(
                    ["Visibility", "looking_at", "speaking", "markup", "face", "torso"]
                )
                select.set_value("Visibility")

        with ui.button("Render") as button:
            # button.on("click", lambda:print(env.file_names))
            button.on("click", self.show_plot)

        with ui.header().classes(replace="row items-center") as header:
            ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
                "flat color=white"
            )
            with ui.tabs() as tabs:
                ui.tab("A")
                ui.tab("B")

        with ui.left_drawer().classes("bg-blue-100") as left_drawer:
            ui.label("Side menu")

        with ui.tab_panels(tabs, value="A", animated=False).classes("w-full"):
            with ui.tab_panel("A"):
                ui.label("Content of A")
                self.show_plot()
            with ui.tab_panel("B"):
                ui.label("Content of B")
                # ui.button("aaaaa", on_click=swi)

        with ui.button("[exit]", on_click=self.stop) as but:
            but.classes("absolute-top-right bg-red")

        ui.run(
            title="A ELAN (Annotation Data) Query Visualisation Tool",
            native=True,
            # fullscreen=False,
            # window_size=(1300, 900),
            reload=False,
            on_air=None,
            # frameless=True
            # *opti
        )


if __name__ in {"__main__", "__mp_main__"}:
# if __name__ in {"__main__"}:
    ui_app = UIApp()

    # events = glob.glob(
    #     r"./HCI-2023/Annotated_Data_JSON/V3/event_json_data/**/Annotation_*.json",
    #     recursive=True,
    # )
    # events = glob.glob(
    #     r"./HCI-2023/Annotated_Data_JSON/V3/event_json_data/*",
    #     recursive=True,
    # )

    # print(events)

    # import random

    # @app.get("/random/{max}")
    # def generate_random_number(max: int):
    #     return {"min": 0, "max": max, "value": random.randint(0, max)}

    # max = ui.number("max", value=100)
    # ui.button(
    #     "generate random number", on_click=lambda: ui.open(f"/random/{max.value:.0f}")
    # )

    ui_app.run_app()
