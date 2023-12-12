from datetime import datetime

from nicegui import ui, app


# test = ui.html()

# test.classes("fixed-center")
# test.classes("absolute-left")

# test.set_content("<h1>[exit]</h1>")

# with ui.element(tag="code") as div:
#     ui.label("clock")
#     tick = ui.html()
#     num = 0

#     def inc():
#         global num
#         num += 1
#         return num

#     ui.timer(1, lambda: tick.set_content(f"<h2>{inc()}</h2>"))


# test.on("click", app.shutdown)


# with ui.row().classes('w-full  .inline'):
# with ui.row().classes("items-center"):

#     with ui.radio(["x", "y", "z"], value="x") as radio:
#         # ui.row()
#         # radio.tailwind.background_color("green-100")
#         radio.classes("bg-blue")

#     with ui.radio(["x", "y", "z"], value="x") as radio:
#         # ui.row()
#         # radio.tailwind.background_color("green-100")
#         radio.classes("bg-blue")


# # # .props('inline color=green')
#     ui.button(icon='touch_app').props('outline round').classes('shadow-lg')
# # ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')


# app.native.start_args["debug"] = True


from typing import Callable, Dict, Union

from nicegui import background_tasks, helpers, ui


class RouterFrame(ui.element, component="router_frame.js"):
    pass


class Router:
    def __init__(self) -> None:
        self.routes: Dict[str, Callable] = {}
        self.content: ui.element | None = None

    def add(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = func
            return func

        return decorator

    def open(self, target: Union[Callable, str]) -> None:
        if isinstance(target, str):
            path = target
            builder = self.routes[target]
        else:
            path = {v: k for k, v in self.routes.items()}[target]
            builder = target

        async def build() -> None:
            with self.content:
                ui.run_javascript(
                    f"""
                    if (window.location.pathname !== "{path}") {{
                        history.pushState({{page: "{path}"}}, "", "{path}");
                    }}
                """
                )
                result = builder()
                if helpers.is_coroutine_function(builder):
                    await result

        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        self.content = RouterFrame().on("open", lambda e: self.open(e.args))
        return self.content


@ui.page("/")  # normal index page (e.g. the entry point of the app)
@ui.page(
    "/{_:path}"
)  # all other pages will be handled by the router but must be registered to also show the SPA index page
def main():
    router = Router()

    @router.add("/")
    def show_one():
        ui.label("Content One").classes("text-2xl")

    @router.add("/two")
    def show_two():
        ui.label("Content Two").classes("text-2xl")

    @router.add("/three")
    def show_three():
        ui.label("Content Three").classes("text-2xl")

    # adding some navigation buttons to switch between the different pages
    with ui.row():
        ui.button("One", on_click=lambda: router.open(show_one)).classes("w-32")
        ui.button("Two", on_click=lambda: router.open(show_two)).classes("w-32")
        ui.button("Three", on_click=lambda: router.open(show_three)).classes("w-32")

    # this places the content which should be displayed
    router.frame().classes("w-full p-4 bg-gray-100")


ui.run(
    # frameless=True,
    native=True,
    # prod_js=False,
    tailwind=True,
    reload=False,
)
