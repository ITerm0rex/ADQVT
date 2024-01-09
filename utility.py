from nicegui import ui
from nicegui.functions.refreshable import _P, _T
from typing import Callable, Coroutine, Union


def Idempotence(f: ui.refreshable[_P, _T]):  # type: ignore
    """
    The `Idempotence` function is a decorator that ensures a function is only executed once, and
    subsequent calls to the function will refresh the UI elements created by the function.

    :param f: The parameter `f` is a function that takes some arguments (`_P`) and returns a value
    (`_T`). It is also refreshable, meaning it has a `refresh` method that can be called to update the
    UI elements created by the function
    :type f: ui.refreshable[_P, _T]
    :return: The function `Idempotence` returns a wrapped version of the input function `f`. The wrapped
    function has the same signature as `f` and can be called with the same arguments.
    """
    flag = True

    def wrap(*args: _P.args, **kwargs: _P.kwargs):
        nonlocal flag
        if flag:
            flag = False
            return f(*args, **kwargs)
        """
        Refresh the UI elements created by this function.
        This method accepts the same arguments as the function itself or a subset of them.
        It will combine the arguments passed to the function with the arguments passed to this method.
        """
        return f.refresh(*args, **kwargs)

    w: Callable[_P, Union[_T, Coroutine[None, None, _T]]] = wrap  # type: ignore
    return w