import numpy as np
from matplotlib import pyplot as plt
from nicegui import ui, app, run


async def choose_file():
    if app.native.main_window:
        files = await app.native.main_window.create_file_dialog(allow_multiple=True)
        for file in files:
            ui.notify(file)


ui.button("choose file", on_click=choose_file)


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
    row.style(
        """
        position: absolute;
        right:0px;
        """
    )
    with ui.pyplot(figsize=(3, 2)) as g:
        x = np.linspace(0.0, 5.0)
        y = np.cos(2 * np.pi * x) * np.exp(-x)
        plt.plot(x, y, "-")
        g.on("click", lambda x: app.shutdown())


ui.run(
    title="test",
    native=True,
    fullscreen=False,
    window_size=(1000, 800),
    reload=False,
    on_air=None,
    prod_js=False,
    tailwind=False,
)
