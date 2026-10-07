# tb_hide/hide.py

from enum import Enum
from typing import Callable


class HideMode(Enum):
    """Enum used to designate the way of hiding traceback frame(s).

    Attributes
    ----------
    HERE
        only hide frame(s) of decorated function.
    RECURSIVE
        hide all frame(s) of decorated function
        and the functions called by it.
    """
    HERE = 1
    RECURSIVE = 2


def hide_here(
        exc: Exception,
        func: Callable
        ) -> None:
    tb = exc.__traceback__
    code = None
    while code is None:
        try:
            code = func.__code__  # type: ignore
        except AttributeError:
            func = func.__call__  # type: ignore
    while tb is not None:
        if tb.tb_frame.f_code is not code:
            break
        tb = tb.tb_next
    exc.__traceback__ = tb


def hide_recursive(
        exc: Exception,
        _: Callable
        ) -> None:
    exc.__traceback__ = None


HIDE: dict[
    HideMode,
    Callable[[Exception, Callable], None]
] = {
    HideMode.HERE: hide_here,
    HideMode.RECURSIVE: hide_recursive
}

__all__ = ['HIDE', 'HideMode']
