import asyncio
import json
import os
import threading
import numpy as np
from matplotlib import pyplot as plt
from nicegui import ui, app, run


async def choose_file():
    if app.native.main_window:
        if files := await app.native.main_window.create_file_dialog(
            allow_multiple=True
        ):
            for file in files:
                ui.notify(file)


with ui.button("choose file", on_click=choose_file) as b:
    b.set_text("aaaaaaaaaaaaaaaaaaaaa")

    b.style(
        """
    background-color: green;
    """
    )

if __name__ == "__main__":
    with open(r".\web\styles.css", "r") as style:
        css = "".join(style.readlines())
        print(css)

    anot_path = r"\HCI-2023\Annotated_Data_JSON\V3\event_json_data\s2_v3_-_matchmaker_scene\Annotation_s2_v3_-_matchmaker_scene.json"
    anot_path = "." + anot_path.replace(os.sep, "/")
    anot_name = os.path.basename(anot_path)

    with open(anot_path) as fp:
        json_data = json.load(fp)

        ui.json_editor(json_data)


# <link rel="stylesheet" href="./web/styles.css">

ui.add_head_html(
    """
<style>
* {
// background-color: green;
}
</style>
"""
)

ui.add_body_html(
    """

"""
)


with ui.header().classes(replace="row items-center") as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
        "flat color=white"
    )
    with ui.tabs() as tabs:
        ui.tab("A")
        ui.tab("B")
        ui.tab("C").classes("bg-green-100")

with ui.footer(value=False) as footer:
    ui.label("Footer")

with ui.left_drawer().classes("bg-blue-100") as left_drawer:
    ui.label("Side menu")

with ui.page_sticky(position="bottom-right", x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon="contact_support").props("fab")

with ui.tab_panels(tabs, value="A").classes("w-full"):
    with ui.tab_panel("A"):
        ui.label("Content of A")
    with ui.tab_panel("B"):
        ui.label("Content of B")
    with ui.tab_panel("C"):
        ui.label("Content of C")


tree = ui.tree(
    [
        {"id": "numbers", "icon": "tag", "children": [{"id": "1"}, {"id": "2"}]},
        {
            "id": "letters",
            "icon": "text_fields",
            "children": [{"id": "A"}, {"id": "B"}],
        },
    ],
    label_key="id",
    on_select=lambda e: ui.notify(e.value),
)

tree.add_slot(
    "default-header",
    r"""
    <div class="row items-center">
        <q-icon :name="props.node.icon || 'share'" color="orange" size="28px" class="q-mr-sm" />
        <div class="text-weight-bold text-primary">{{ props.node.id }}</div>
    </div>
""",
)

with tree.add_slot("default-body"):
    ui.label("This is some default content.").classes(
        "ml-8 text-weight-light text-black"
    )


with ui.button("bbbbbbbbbbbbb") as b:
    # b.set_text("åååååååååååå")

    # b.style(
    #     """
    # background-color: green;
    # """
    # )

    def mmmm():
        print(123)

    b.on("click", mmmm)


class Demo:
    def __init__(self):
        self.actions = None
        self.names = None


demo = Demo()


with ui.toggle({1: "a", 2: "b", 3: "c"}) as t:
    t.bind_value(demo, "names")
    t.on("click", lambda x: ui.label(text=str(x)))


with ui.toggle({4: "stationary", 5: "gesturing", 6: "speaking"}) as t:
    t.bind_value(demo, "actions")
    t.on("click", lambda: print(vars(demo)))

with ui.row() as row:
    row.classes("absolute-right")
    # .classes("absolute-center shadow")\
    # .style(
    #     """
    #     position: absolute;
    #     right:0px;
    #     """
    # )\

    row.tailwind.background_color("green-400")

    with ui.pyplot(figsize=(3, 2)) as g:
        x = np.linspace(0.0, 5.0)
        y = np.cos(2 * np.pi * x) * np.exp(-x)
        plt.plot(x, y, "-")
        g.tailwind.background_color("green-100")
        g.on("click", lambda x: app.shutdown())


@ui.refreshable
def stuff():
    with ui.button("button", color="green") as b:
        b.on("click", lambda: b.set_text("!!!!!!!!!!!!!!!!!!"))
        # async def aaa():
        #     await b.clicked()
        #     b.set_text("!!!!!!!!!!!!!!!!!!")
        
        # if __name__ == "__main__":
        #     threading.Thread(target=lambda: asyncio.run(aaa())).run()


stuff()

ui.run(
    title="test",
    native=True,
    fullscreen=False,
    window_size=(1000, 800),
    reload=False,
    on_air=None,
    # prod_js=False,
    # tailwind=False,
)
