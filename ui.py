# %%
import asyncio
from dataclasses import dataclass, field
import glob
import json
import os
import sys
import threading
from typing import Any, Awaitable, Callable, Coroutine, Union
import numpy as np
from matplotlib import pyplot as plt
from nicegui import ui, app
from nicegui import core
from nicegui.logging import log


import prototype


from nicegui.functions.refreshable import _P, _T


def Idempotence(f: ui.refreshable[_P, _T]):  # type: ignore
    flag = True

    def wrap(*args: _P.args, **kwargs: _P.kwargs):
        nonlocal flag
        if flag:
            flag = False
            return f(*args, **kwargs)
        return f.refresh(*args, **kwargs)

    w: Callable[_P, Union[_T, Coroutine[None, None, _T]]] = wrap  # type: ignore
    return w


def stop():
    app.stop()
    app.shutdown()
    exit(0)


@dataclass
class env_fact:
    file_names: set[str] = field(default_factory=set[str])
    Class: str = "Visibility"
    Hold: str = "Visibility"


env = env_fact()


@Idempotence
@ui.refreshable
def show_plot():
    with ui.row() as row:
        row.classes("absolute-right")
        # row.classes("row reverse")
        # row.classes("full-width row inline no-wrap justify-end items-end content-end")

        print(env.file_names)

        if env.file_names == set():
            return

        with ui.pyplot() as g:
            # g.style("overflow: auto;")
            g.style("zoom: 85%;")
            # g.style("max-width: 200px; max-height: 100px;")

            plot = prototype.query_time_total()

            plot.set(list(env.file_names), env.Class, env.Hold)
            plot.create()
            plot.show()

            g.on("click", stop)


class UIApp:
    # def __init__(self):
    #     # self.file_names = set()
    #     self.select = None
    #     self.row = None
    #     self.plt = None
    #     self.flag = True
    
    @Idempotence
    @ui.refreshable
    def test(self,opt):
        with ui.row() as r:
            ui.label("hiii")
            with ui.select([]) as fi:
                fi.set_options(opt)
                # fi.bind_value(env, "file_names", forward=list)
                fi.on("input", lambda: fi.set_options(list(env.file_names)))

    async def choose_file(self):
        if app.native.main_window:
            if files := await app.native.main_window.create_file_dialog(
                allow_multiple=True
            ):
                env.file_names.clear()
                env.file_names.update(files)

    def create_button(self, text, on_click_handler):
        with ui.button(text, on_click=on_click_handler) as button:
            button.style("background-color: green;")
        return button

    def create_selection(self, bind: str):
        with ui.select([]) as select:
            select.bind_value(env, bind)
            # select.classes("w-200")
            return select

    def run_app(self):
        # env.file_names = set()

        with ui.button("Choose File") as button:
            # button.tailwind.background_color("green-100")
            # button.style("background-color: green;")
            button.on("click", self.choose_file)

        with ui.button("maxxx") as button:
            # button.tailwind.background_color("green-100")
            # button.style("background-color: green;")


            def maxx():
                # print((app.native.main_window), sep="\n")
                if app.native.main_window:
                    # app.native.main_window.maximize()
                    app.native.main_window.toggle_fullscreen()
                    # app.native.main_window.maximized = True
                    getattr(app.native.main_window, "toggle_fullscreen")

            button.on("click", maxx)

        with ui.select([]) as fi:
            # fi.bind_value(env, "file_names", forward=list)
            fi.on("input", lambda: fi.set_options(list(env.file_names)))

        # with ui.row() as row:
        #     # row.classes("absolute-right orange-6")
        #     # with ui.select([1, 2, 3]) as fi:
        #     #     fi.classes("absolute-center")
        #     with ui.select([1, 2, 3]) as fi:
        #         # fi.classes("absolute-center")
        #         pass
        #     with ui.select([1, 2, 3]) as fi:
        #         # fi.classes("absolute-center")
        #         pass
        #     with ui.select([1, 2, 3]) as fi:
        #         # fi.classes("absolute-center")
        #         pass
        
        # ui.add_body_html("""
        #                  """)

        self.create_selection("Class").set_options(
            ["Visibility", "Gaze", "HumanAction", "Saccade", "Attention"]
        )

        self.create_selection("Hold").set_options(
            ["Visibility", "looking_at", "speaking", "markup", "face", "torso"]
        )

        show_plot()
        
        self.test([1,2,3])
        
        self.test([4,5,6])


        # ui.button("[exit]", on_click=stop).classes("absolute-top-right bg-red")
        
        with ui.button("[exit]", on_click=stop) as but:
            but.classes("absolute-top-right bg-red")

        with ui.button("Render") as button:
            # button.on("click", lambda:print(env.file_names))
            button.on("click", show_plot)

        try:
            ui.run(
                title="demo",
                native=True,
                fullscreen=False,
                window_size=(1300, 900),
                reload=False,
                on_air=None,
                # frameless=True
                # *opti
            )
        except asyncio.exceptions.CancelledError:
            pass


if __name__ in {"__main__"}:
# if __name__ in {"__main__", "__mp_main__"}:
    ui_app = UIApp()
    
    # events = glob.glob(
    #     r"./HCI-2023/Annotated_Data_JSON/V3/event_json_data/**/Annotation_*.json",
    #     recursive=True,
    # )
    events = glob.glob(
        r"./HCI-2023/Annotated_Data_JSON/V3/event_json_data/*",
        recursive=True,
    )
    
    print(events)
    
    ui_app.run_app()
