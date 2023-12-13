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
from nicegui import core


import prototype


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


def stop():
    app.shutdown()
    app.stop()
    exit(0)


@dataclass
class env:
    file_names: set[str]
    Class: str = "Visibility"
    Hold: str = "Visibility"


# class Ide:#(ui.refreshable[_P, _T]):
#     flag = True
#     f: ui.refreshable[_P, _T]

#     # Union[_T, Coroutine[None, None, _T]]:
#     def __init__(self, f: ui.refreshable[_P, _T]):
#         self.f = f

#     def __call__(
#         self, *args: _P.args, **kwargs: _P.kwargs
#     ) -> _T | Awaitable[_T] | None:
#         if self.flag:
#             self.flag = False
#             return self.f(*args, **kwargs)
#         return self.f.refresh(*args, **kwargs)
#         # return self.run(*args, **kwargs)

#     # def run(self, *args: _P.args, **kwargs: _P.kwargs):
#     #     if self.flag:
#     #         self.flag = False
#     #         return self.f(*args, **kwargs)
#     #     return self.f.refresh(*args, **kwargs)


@Idempotence
@ui.refreshable
def show_plot():
    # await asyncio.sleep(2)
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

            plot = prototype.query()

            # plot.set(filenames, "Visibility", "Visibility")
            plot.set(list(env.file_names), env.Class, env.Hold)
            # plot.set([r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"], env.Class, env.Hold)
            plot.create()
            plot.show()

            g.on("click", stop)


class UIApp:
    def __init__(self):
        # self.file_names = set()
        self.select = None
        self.row = None
        self.plt = None
        self.flag = True

    async def choose_file(self):
        if app.native.main_window:
            if files := await app.native.main_window.create_file_dialog(
                allow_multiple=True
            ):
                env.file_names.clear()
                env.file_names.update(files)
                # self.file_names.update(files)

                # self.file_names.clear()
                # self.file_names += list(files)

                # print(show_plot.instance)

                # show_plot()

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
        # with ui.row() as row:
        #     row.classes("absolute-right")

        #     row.tailwind.background_color("green-400")
        #     # row.tailwind.position("absolute")
        #     # row.tailwind.top_right_bottom_left()

        #     with ui.pyplot(figsize=(3, 2)) as g:
        #         prototype.gaze(self.file_names[0]).show()

        #         g.on("click", lambda x: app.shutdown())

        # self.update_selected_files()

        # .tailwind.background_color("red-100")

        # app.native.start_args["debug"] = True
        # if app.native.main_window:
        #     app.native.main_window.maximized = True

        # core.app.native.start_args["maximized"] = True

        # opti = {
        #     "maximized": True
        # }

        # app.native.window_args["maximized"] = True

        # pathf = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
        # # pathf = r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s4_v3_-_macbeth_opening_scene\Annotation_s4_v3_-_macbeth_opening_scene.json"

        # if isinstance(v := show_plot([pathf]), Coroutine):
        #     print(asyncio.run(v))
        # else:
        #     print(v)

        ui.run(
            title="test",
            native=True,
            fullscreen=False,
            window_size=(1300, 900),
            reload=False,
            on_air=None,
            # frameless=True
            # *opti
        )


if __name__ == "__main__":
    ui_app = UIApp()
    env.file_names = set()

    # choose_file_button = ui_app.create_button("Choose File", ui_app.choose_file)

    with ui.button("Choose File") as button:
        # button.tailwind.background_color("green-100")
        # button.style("background-color: green;")
        button.on("click", ui_app.choose_file)

    # with ui_app.create_selection("file_names") as fi:
    #     fi.on("click", lambda: fi.set_options(list(env.file_names)))

    with ui.select([]) as fi:
        # fi.bind_value(env, "file_names", forward=list)
        fi.on("input", lambda: fi.set_options(list(env.file_names)))

    ui_app.create_selection("Class").set_options(
        ["Visibility", "Gaze", "HumanAction", "Saccade", "Attention"]
    )
    ui_app.create_selection("Hold").set_options(
        ["Visibility", "looking_at", "speaking", "markup", "face", "torso"]
    )

    show_plot()

    ui.button("[exit]", on_click=stop).classes("absolute-top-right bg-red")

    with ui.button("Render") as button:
        # button.on("click", lambda:print(env.file_names))
        button.on("click", show_plot)

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

    # [
    #     r".\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
    # ]

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


    ui_app.run_app()
