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

from typing import TypeVar, Optional, Literal, Callable, Union

Logger     = TypeVar("Logger", str, logging.Logger)
Closure    = TypeVar("Closure", bound=Callable)
OutputMode = Literal["stream", "file", "stream,file"]

__first__: logging.Logger

gpack = sys.modules[__package__]
gcode = sys.modules[__name__]


def __init__(
        name:    str,
        *,
        level:   Union[int, str] = "NOTSET",
        output:  OutputMode      = "stream",
        logfmt:  Optional[str]   = None,
        datefmt: Optional[str]   = None,
        logfile: Optional[str]   = None,
        gname:   Optional[str]   = None
) -> logging.Logger:
    if output.replace(" ", "") not in \
            ("stream", "file", "stream,file", "file,stream"):
        raise TypeError(
            "parameter 'output' can only be 'stream', 'file', or "
            f"'stream,file', not '{output}'."
        )

    logger    = logging.Logger(name, level)
    formatter = logging.Formatter(logfmt, datefmt)

    if "stream" in output:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if "file" in output:
        if logfile is None:
            starter: str = os.path.basename(sys.argv[0])
            logfile: str = f"/var/log/{starter[:-3]}.log"

        logdir: str = os.path.dirname(os.path.abspath(logfile))
        os.path.isdir(logdir) or os.makedirs(logdir)

        handler = logging.FileHandler(logfile, encoding="utf8")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if gname:
        if not hasattr(gcode, "__first__") or \
                gcode.__first__.name == "builtin":
            gcode.__first__ = logger
        setattr(gpack, gname, logger)

    return logger


def __getattr__(method: str) -> Closure:
    if not hasattr(logging.Logger, method):
        raise AttributeError(
            f"module '{__package__}' has no attribute '{method}'"
        )

    def logger(
            *msg,
            sep:     str           = " ",
            oneline: bool          = False,
            linesep: str           = "; ",
            gname:   Union[Logger] = None,
            **kw
    ) -> None:
        if gname is None:
            if not hasattr(gcode, "__first__"):
                gobj: logging.Logger = __init__(
                    name="builtin",
                    level=gpack.level,
                    output=gpack.output,
                    logfmt=gpack.logfmt,
                    datefmt=gpack.datefmt,
                    **({"logfile": gpack.logfile} if gpack.logfile !=
                        "/var/log/{default is your startup filename}.log"
                       else {}),
                    gname="builtin"
                )
                setattr(gcode, "__first__", gobj)
            gobj: logging.Logger = __first__
        elif gname.__class__ is str:
            gobj: logging.Logger = getattr(gpack, gname, None)
            if gobj.__class__ is not logging.Logger:
                raise NameError(f"gname '{gname}' not in '{__package__}'.")
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
