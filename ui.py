# %%
import asyncio
from dataclasses import dataclass
import json
import os
import threading
from typing import Any, Awaitable, Callable, Coroutine, Union
import numpy as np
from matplotlib import pyplot as plt
from nicegui import ui, app

import prototype


def stop():
    app.shutdown()
    app.stop()
    exit(0)


# @dataclass
# class DATA:
#     filenames: list[str] = []
#     hi: int = 0


# DATA.filenames.append("aaaaa")
# DATA.hi = 22


from nicegui.functions.refreshable import _P, _T


def Idempotence(f: ui.refreshable[_P, _T]):
    flag = True

    def wrap(*args: _P.args, **kwargs: _P.kwargs):
        nonlocal flag
        if flag:
            flag = False
            return f(*args, **kwargs)
        return f.refresh(*args, **kwargs)

    w: Callable[_P, Union[_T, Coroutine[None, None, _T]]] = wrap  # type: ignore
    return w


@Idempotence
@ui.refreshable
def show_plot(filenames: list[str]):
    # await asyncio.sleep(2)
    with ui.row() as row:
        # row.classes("absolute-right")
        # row.classes("row reverse")
        row.classes("full-width row inline no-wrap justify-end items-end content-end")

        with ui.pyplot(dpi=0.5) as g:
            # g.style("overflow: auto;")
            g.style("zoom: 70%;")
            # g.style("max-width: 200px; max-height: 100px;")

            plot = prototype.moving_towards()

            plot.set(filenames)
            plot.create()
            plot.show()

            g.on("click", stop)


# pathf = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
pathf = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s4_v3_-_macbeth_opening_scene\Annotation_s4_v3_-_macbeth_opening_scene.json"


if isinstance(v := show_plot([pathf]), Coroutine):
    print(asyncio.run(v))
else:
    print(v)


# @(lambda f: lambda x: f(2 * x))
# def fun(x):
#     print(x)


# fun(2)

# mmm = lambda x: 2 * x


# def mmm(x):
#     return x * 2


# print(mmm(1))


class UIApp:
    def __init__(self):
        self.file_names = [
            r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
        ]
        self.select = None
        self.row = None
        self.plt = None

        self.flag = True

    async def choose_file(self):
        if app.native.main_window:
            if files := await app.native.main_window.create_file_dialog(
                allow_multiple=True
            ):
                self.file_names.clear()
                self.file_names += list(files)

                # print(show_plot.instance)

                show_plot(self.file_names)

                # if self.flag:
                #     self.flag = False
                #     show_plot(self.file_names)
                # else:
                #     show_plot.refresh(self.file_names)

                # self.update_selected_files()

                # for file in files:
                #     print(file)
                #     ui.label(file)
                #     ui.notify(file)
        # if self.select:
        #     self.select.set_options(self.file_names, value=self.file_names[0])

    # def update_selected_files(self):
    #     if self.select:
    #         self.select.clear()

    #     self.select = ui.select(self.file_names, value=1)
    #     self.select.classes("w-200")

    #     if self.row:
    #         self.row.clear()

    #     with ui.row() as row:
    #         self.row = row
    #         # row.classes("absolute-right")

    #         # row.tailwind.background_color("green-400")
    #         # row.tailwind.position("absolute")
    #         # row.tailwind.top_right_bottom_left()

    #         # with ui.pyplot(figsize=(6, 4)) as g:
    #         if self.plt:
    #             self.plt.clear()

    #         with ui.pyplot() as g:
    #             self.plt = g
    #             self.gz = prototype.gaze()

    #             self.gz.set(self.file_names)
    #             self.gz.create()
    #             self.gz.show()

    #             g.on("click", stop)

    def create_button(self, text, on_click_handler):
        with ui.button(text, on_click=on_click_handler) as button:
            button.style("background-color: green;")
        return button

    def create_selection(self, bind: str):
        with ui.select({1: "hii"}, value=1) as select:
            select.bind_value(
                self, bind, #forward=lambda x: x, backward=lambda x: enumerate(x)
            )
            select.classes("w-200")
            return select

    def run_app(self):
        # with ui.row() as row:
        #     row.classes("absolute-right")

        #     row.tailwind.background_color("green-400")
        #     # row.tailwind.position("absolute")
        #     # row.tailwind.top_right_bottom_left()

        #     with ui.pyplot(figsize=(3, 2)) as g:
        #         prototype.gaze(self.file_names[0]).show()

        #         g.on("click", lambda x: app.shutdown())

        # self.update_selected_files()

        ui.button("[exit]", on_click=stop).classes("absolute-bottom-right")

        # app.native.start_args["debug"] = True
        # if app.native.main_window:
        #     app.native.main_window.maximized = True

        app.native.start_args["maximized"] = True
        ui.run(
            title="test",
            native=True,
            fullscreen=False,
            window_size=(1000, 800),
            reload=False,
            on_air=None,
        )


if __name__ == "__main__":
    ui_app = UIApp()

    # Create UI components
    # choose_file_button = ui_app.create_button("Choose File", ui_app.choose_file)

    with ui.button("Choose File", on_click=ui_app.choose_file) as button:
        button.tailwind.background_color("green-100")
        # button.style("background-color: green;")

    ui_app.create_selection("file_names")
    # ui_app.create_selection("option")

    # select = ui.select(file_names, value=1)
    # select.classes("w-200")

    # ui_app.update_selected_files()

    # with ui.button("hiiiii") as but:
    #     but.on("click", lambda: )

    # Arrange components
    # with ui.header().classes(replace="row items-center") as header:
    #     ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
    #         "flat color=white"
    #     )
    #     with ui.tabs() as tabs:
    #         ui.tab("A")
    #         ui.tab("B")
    #         ui.tab("C").classes("bg-green-100")

    # with ui.left_drawer().classes("bg-blue-100") as left_drawer:
    #     ui.label("Side menu")

    # with ui.tab_panels(tabs, value="A").classes("w-full"):
    #     with ui.tab_panel("A"):
    #         ui.label("Content of A")
    #     with ui.tab_panel("B"):
    #         ui.label("Content of B")
    #     with ui.tab_panel("C"):
    #         ui.label("Content of C")

    # tree = ui.tree(
    #     [
    #         {"id": "numbers", "icon": "tag", "children": [{"id": "1"}, {"id": "2"}]},
    #         {
    #             "id": "letters",
    #             "icon": "text_fields",
    #             "children": [{"id": "A"}, {"id": "B"}],
    #         },
    #     ],
    #     label_key="id",
    #     on_select=lambda e: ui.notify(e.value),
    # )

    # Add other UI components

    # Run the app
    ui_app.run_app()
