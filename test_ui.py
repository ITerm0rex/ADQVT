from datetime import datetime

from nicegui import ui, app


test = ui.html()

test.classes("fixed-center")

test.set_content("<h1>[exit]</h1>")

with ui.element(tag="code") as div:
    ui.label("clock")
    tick = ui.html()
    num = 0

    def inc():
        global num
        num += 1
        return num

    ui.timer(1, lambda: tick.set_content(f"<h2>{inc()}</h2>"))


test.on("click", app.shutdown)


app.native.start_args["debug"] = True

ui.run(
    frameless=True,
    native=True,
    prod_js=False,
    tailwind=False,
    reload=False,
)
