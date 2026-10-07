# tb_hide/__init__.py
"""Provide a function to hide designated traceback frame(s).

This module contains a decorator `tb_hide` and a few mode enums
to hide designated traceback frame(s).

Attributes
----------
HideMode : type[Enum]
    The type of mode to designate traceback frame(s) to be hidden.

Functions
---------
tb_hide : Callable
    The decorator to hide traceback frame(s).
"""

from functools import wraps
from typing import Any, Callable, Iterable, overload

from .hide import HIDE, HideMode

__version__ = '0.1.1'
__author__ = 'YXProtocol'


@overload
def tb_hide(func: Callable, /, *,
            exceptions: Iterable[type[Exception]] = (Exception,),
            mode: HideMode = HideMode.HERE
            ) -> Callable:
    ...


@overload
def tb_hide(*,
            exceptions: Iterable[type[Exception]] = (Exception,),
            mode: HideMode = HideMode.HERE
            ) -> Callable[[Callable], Callable]:
    ...


def tb_hide(function: Callable | None = None, /, *,
            exceptions: Iterable[type[Exception]] = (Exception,),
            mode: HideMode = HideMode.HERE
            ) -> Callable | Callable[[Callable], Callable]:
    """Decorator to hide traceback frame(s).

    A decorator to hide traceback frame(s).
    There are two ways to use this decorator:

    @tb_hide
    def decorated_function(*args, **kwargs):
        ...

    @tb_hide(...)
    def decorated_function(*args, **kwargs):
        ...

    Parameters
    ----------
    function : Callable
        Function where you want to hide traceback frame(s).
    exceptions : Iterable[type[Exception]]
        Exceptions of which you want to hide traceback frame(s).
        Default value: `(Exception,)`.
    mode : HideMode
        The mode to designate the way of hiding traceback frame(s).
        Default value: `HideMode.HERE`.
    """
    exc_tuple: tuple[type[Exception], ...] = tuple(exceptions)

    def deco(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            try:
                return func(*args, **kwargs)
            except exc_tuple as exc:
                exc.__traceback__ = exc.__traceback__.tb_next  # type: ignore
                HIDE[mode](exc, func)
                raise
            except Exception as exc:
                exc.__traceback__ = exc.__traceback__.tb_next  # type: ignore
                raise
        return wrapper

    if function is not None:
        return deco(function)
    return deco


__all__ = ["HideMode", "tb_hide"]
