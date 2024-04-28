"""
Copyright (c) 2022-2024 GQYLPY <http://gqylpy.com>. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import sys
import logging

from logging import handlers as logging_handlers

from types import ModuleType

from typing import (
    TypeVar, Type, Final, Optional, TypedDict, Union, Callable, Mapping, Dict,
    List, Any
)

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    class Annotated(metaclass=type('', (type,), {
        '__new__': lambda *a: type.__new__(*a)()
    })):
        def __getitem__(self, *a): ...

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    TypeAlias = TypeVar("TypeAlias")

Logger:  TypeAlias = TypeVar("Logger", str, logging.Logger)
Level:   TypeAlias = TypeVar("Level", int, str)
Closure: TypeAlias = TypeVar("Closure", bound=Callable)


class DictFormatter(TypedDict, total=False):
    fmt:      str
    datefmt:  str
    style:    str
    validate: bool

    if sys.version_info >= (3, 10):
        defaults: Mapping[str, Any]


class Options(TypedDict, total=False):
    onlyRecordCurrentLevel: bool


Formatter: TypeAlias = Union[DictFormatter, logging.Formatter]

Filter: TypeAlias = Union[
    Callable[[logging.LogRecord], bool], logging.Filter, logging.Filterer
]

Handler: TypeAlias = Union[Dict[str, Any], logging.Handler]

default: Annotated[logging.Logger, "built-in default logger"]

gpack: Final[ModuleType] = sys.modules[__package__]
gcode: Final[ModuleType] = sys.modules[__name__]

logging_handlers.Handler       = logging.Handler
logging_handlers.StreamHandler = logging.StreamHandler
logging_handlers.FileHandler   = logging.FileHandler


def __init__(
        name:      str,
        *,
        level:     Level         = 0,
        formatter: Formatter     = logging.Formatter(),
        filters:   List[Filter]  = [],
        options:   Options       = {},
        handlers:  List[Handler] = [],
        gname:     Optional[str] = None
) -> logging.Logger:
    logger = logging.Logger(name, level)

    if formatter.__class__ is dict:
        formatter = logging.Formatter(**formatter)

    for handler_or_params in handlers:
        if isinstance(handler_or_params, logging.Handler):
            logger.addHandler(handler_or_params)
            continue

        if "formatter" in handler_or_params:
            the_formatter: Formatter = handler_or_params.pop("formatter")
            if the_formatter.__class__ is dict:
                the_formatter = logging.Formatter(**the_formatter)
        else:
            the_formatter = formatter

        the_level:   Level        = handler_or_params.pop("level", level)
        the_filters: List[Filter] = handler_or_params.pop("filters", filters)
        the_options: Options      = handler_or_params.pop("options", options)

        handler_type: Type[logging.Handler] = \
            getattr(logging_handlers, handler_or_params.pop("name"))

        if issubclass(handler_type, logging.FileHandler):
            filename: str = handler_or_params["filename"]
            logdir:   str = os.path.dirname(os.path.abspath(filename))
            os.makedirs(logdir, exist_ok=True)

        handler: logging.Handler = handler_type(**handler_or_params)
        handler.setLevel(the_level)
        handler.setFormatter(the_formatter)
        handler.filters.extend(
            x for x in the_filters if x not in handler.filters
        )

        if the_options.get("onlyRecordCurrentLevel"):
            handler.addFilter(only_record_current_level(handler.level))

        logger.addHandler(handler)

    if gname:
        if not hasattr(gcode, "default") or gcode.default.name == "default":
            gcode.default = logger
        setattr(gpack, gname, logger)

    return logger


def only_record_current_level(
        levelno: int
) -> Callable[[logging.LogRecord], bool]:
    return lambda record: record.levelno == levelno


def __getattr__(method: str) -> Closure:
    if not hasattr(logging.Logger, method):
        raise AttributeError(
            f"module '{__package__}' has no attribute '{method}'"
        )

    def logger(
            *msg,
            sep:     str              = " ",
            oneline: bool             = False,
            linesep: str              = "; ",
            gname:   Optional[Logger] = None,
            **kw
    ) -> None:
        if gname is None:
            if not hasattr(gcode, "default"):
                __init__("default", **gpack.default, gname="default")
            gobj: logging.Logger = default
        elif gname.__class__ is str:
            gobj: logging.Logger = getattr(gpack, gname, None)
            if gobj.__class__ is not logging.Logger:
                raise NameError(
                    f"gname '{gname}' not found in '{__package__}'."
                )
        elif gname.__class__ is logging.Logger:
            gobj: logging.Logger = gname
        else:
            raise TypeError(
                "parameter 'gname' type must be 'str' or 'logging.Logger', "
                f"not '{gname.__class__.__name__}'."
            )

        if sys.version_info >= (3, 8):
            if "stacklevel" in kw:
                if kw["stacklevel"].__class__ is not int:
                    if not kw["stacklevel"].isdigit():
                        raise TypeError(
                            "parameter 'stacklevel' type must be 'int', "
                            f"not '{kw['stacklevel'].__class__.__name__}'."
                        )
                    kw["stacklevel"] = int(kw["stacklevel"])
                if kw["stacklevel"] < 2:
                    kw["stacklevel"] = 2
            else:
                kw["stacklevel"] = 2

        msg: str = sep.join(str(m) for m in msg)

        if oneline:
            msg: str = linesep.join(
                m.strip() for m in msg.split("\n") if m and not m.isspace()
            )

        getattr(gobj, method)(msg, **kw)

    return logger
