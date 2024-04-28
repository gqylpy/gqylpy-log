"""
Secondary encapsulation `logging`, more convenient and fast to create the
logger. Use this module can quickly create instances of `logging.Logger` and
complete a series of log configuration, make your code cleaner.

    >>> import gqylpy_log as glog
    >>> glog.info(...)

    @version: 2.0
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-log

────────────────────────────────────────────────────────────────────────────────
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
import sys
import logging

from typing import \
    TypeVar, Optional, TypedDict, Union, Callable, Mapping, Dict, List, Any

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

Logger: TypeAlias = TypeVar("Logger", str, logging.Logger)
Level:  TypeAlias = TypeVar("Level", int, str)


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


class DefaultLoggerConfig(TypedDict, total=False):
    level:     Level
    formatter: Formatter
    filters:   List[Filter]
    options:   Options
    handlers:  List[Handler]


NOTSET   = 0
DEBUG    = 10
INFO     = 20
WARNING  = 30
WARN     = WARNING
ERROR    = 40
CRITICAL = 50
FATAL    = CRITICAL

default: Annotated[DefaultLoggerConfig, """
    The default logger config.

    The default logger is built into this module, with a configuration as
    follows: a level of `NOTSET`, a general log output format, and a
    `StreamHandler` processing handler.

    You can adjust the configuration of the default logger as needed, but please
    note that the default logger is created when the logging method is first
    called. Only modifications made before this point will take effect.

    Additionally, when you initialize a custom logger using `__init__` for the
    first time and specify the `gname` parameter, the default logger will be
    overwritten and permanently disabled. From then on, your first custom logger
    will be used as the default logger.
"""] = {
    "level": NOTSET,
    "formatter": {
        "fmt": "[%(asctime)s] [%(module)s.%(funcName)s.line%(lineno)d] "
               "[%(levelname)s] %(message)s",
        "datefmt": "%F %T"
    },
    "handlers": [{"name": "StreamHandler"}]
}


def __init__(
        name:      str,
        *,
        level:     Optional[Level]         = None,
        formatter: Optional[Formatter]     = None,
        filters:   Optional[List[Filter]]  = None,
        options:   Optional[Options]       = None,
        handlers:  Optional[List[Handler]] = None,
        gname:     Optional[str]           = None
) -> logging.Logger:
    """Get a `logging.Logger` instance, or initialize it into this module.

    @param name:
        The name is required and will be passed directly to `logging.Logger`. A
        string is recommended.

    @param level:
        The default logging level, which will be passed as an initialization
        parameter to `logging.Logger`. If no level is defined in `handlers`,
        this level will be used. If the logging level in `handlers` is lower
        than this level, this level will prevail.

    @param formatter:
        The default log format. If no log format is defined in `handlers`,
        this format will be used. The log format can be an instance of
        `logging.Formatter` or a dictionary, such as:

            >>> {"fmt": "[%(message)s", "datefmt": "%c", ...}

        All key-value pairs in the dictionary will be passed as keyword
        arguments to `logging.Formatter` to instantiate an instance.

    @param filters:
        The default list of log filters. If no log filters are defined in
        `handlers`, these filters will be used. Log filters can be instances
        of `logging.Filter` or `logging.Filterer`, or any callable object that
        satisfies the type `Callable[[logging.LogRecord], bool]`.

    @param options:
        The default logging options. If no logging options are defined in
        `handlers`, these options will be used. Logging options are defined
        by this module, not natively by `logging`. Their purpose is to
        conveniently add some logging processing functions, such as adding
        filters. Options are passed in the form of a dictionary, where the key
        is the option name and the value is typically True, indicating that
        this option is enabled. All options default to False. The supported
        options are as follows:

        =============================== OPTIONS ================================
        | Option                 | Description                                 |
        ------------------------------------------------------------------------
        | onlyRecordCurrentLevel | Handlers only record logs at the current    |
        |                        | level, silently ignoring logs at non-current|
        |                        | levels                                      |
        ------------------------------------------------------------------------
        | ...                    | ...                                         |
        ------------------------------------------------------------------------

    @param handlers:
        A list of log handlers to create. Log handlers can be instances of
        `logging.Handler` or dictionaries specifying the log handler to create
        and all its initialization parameters. For example, the following will
        create three log handlers:

            >>> [
            >>>     {
            >>>         "name": "StreamHandler",
            >>>         "level": "DEBUG"
            >>>     },
            >>>     {
            >>>         "name": "FileHandler",
            >>>         "level": "ERROR",
            >>>         "filename": "/var/log/alpha/error.log",
            >>>         "encoding": "UTF-8",
            >>>         "formatter": {"fmt": "[%(asctime)s] %(message)s"},
            >>>         "options": {"onlyRecordCurrentLevel": True}
            >>>     },
            >>>     {
            >>>         "name": "TimedRotatingFileHandler",
            >>>         "level": "INFO",
            >>>         "filename": "/var/log/alpha/alpha.log",
            >>>         "encoding": "UTF-8",
            >>>         "when": "D",
            >>>         "interval": 1,
            >>>         "backupCount": 7
            >>>     },
            >>> ]

        Among them, the "name" field is used to specify the (class) name of the
        handler to be created, which can be viewed in the `logging` and
        `logging.handlers` modules. Other fields will be used as parameters or
        options.

    @param gname:
        If not None, a pointer named `gname` will be created in the current
        module, pointing to the newly created `logging.Logger` instance. This
        allows you to easily call it within this module. Additionally, the first
        specified `gname` will override the default built-in logger.
    """


def __call__(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    """
    Record a log entry.

    @param msg:
        Log messages, supporting almost any object.

    @param sep:
        A string inserted between log messages, defaulting to a space.

    @param oneline:
        Make the output log content always one line, defaulting to False. If the
        log message is multi-line, line breaks will be replaced with the
        character specified by the `linesep` parameter.

    @param linesep:
        This parameter is used in conjunction with another parameter `oneline`.
        It specifies the string used to replace line breaks, with a default
        value of a semicolon followed by a space "; ".

    @param gname:
        When `gname` is None, the default logger will be called. If it's not
        None, the function will look for a `logging.Logger` instance with a
        pointer name of `gname` under the current module and use it. If not
        found, it will raise a `NameError` exception.

        The `gname` is specified when you call `__init__`: call `__init__` to
        create the `gname` pointer, and then call this function to use the
        `gname` pointer.

        The `gname` can also be specified as a `logging.Logger` instance.

    @param kw:
        All other keyword arguments are passed to the relevant logger method.
        For example, when the previous level in the stack is the `debug`
        function, `kw` will be passed to the `debug` method of the
        `logging.Logger` instance.
    """


def debug(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    __call__(*msg, sep=sep, oneline=oneline, linesep=linesep, gname=gname, **kw)


def info(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    __call__(*msg, sep=sep, oneline=oneline, linesep=linesep, gname=gname, **kw)


def warning(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    __call__(*msg, sep=sep, oneline=oneline, linesep=linesep, gname=gname, **kw)


def error(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    __call__(*msg, sep=sep, oneline=oneline, linesep=linesep, gname=gname, **kw)


def exception(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    __call__(*msg, sep=sep, oneline=oneline, linesep=linesep, gname=gname, **kw)


def critical(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    __call__(*msg, sep=sep, oneline=oneline, linesep=linesep, gname=gname, **kw)


def fatal(
        *msg:    Any,
        sep:     Optional[str]    = None,
        oneline: Optional[bool]   = None,
        linesep: Optional[str]    = None,
        gname:   Optional[Logger] = None,
        **kw
) -> None:
    __call__(*msg, sep=sep, oneline=oneline, linesep=linesep, gname=gname, **kw)


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    gpack = globals()
    gcode = __import__(f"{__name__}.g {__name__[7:]}", fromlist=...)

    for gname, gfunc in gpack.copy().items():
        if gname[0] != "_" and callable(gfunc):
            del gpack[gname]

    __init__, __getattr__ = gcode.__init__, gcode.__getattr__

    __init__.__module__ = __getattr__.__module__ = __package__

    gpack["__init__"], gpack["__getattr__"] = __init__, __getattr__
