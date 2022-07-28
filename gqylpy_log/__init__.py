"""
─────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████───████████──████████─██████─────────██████████████─████████──████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░██──██░░░░██─██░░██─────────██░░░░░░░░░░██─██░░░░██──██░░░░██─
─██░░██████████─██░░██████░░██───████░░██──██░░████─██░░██─────────██░░██████░░██─████░░██──██░░████─
─██░░██─────────██░░██──██░░██─────██░░░░██░░░░██───██░░██─────────██░░██──██░░██───██░░░░██░░░░██───
─██░░██─────────██░░██──██░░██─────████░░░░░░████───██░░██─────────██░░██████░░██───████░░░░░░████───
─██░░██──██████─██░░██──██░░██───────████░░████─────██░░██─────────██░░░░░░░░░░██─────████░░████─────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██████████───────██░░██───────
─██░░██──██░░██─██░░██──██░░██─────────██░░██───────██░░██─────────██░░██───────────────██░░██───────
─██░░██████░░██─██░░██████░░████───────██░░██───────██░░██████████─██░░██───────────────██░░██───────
─██░░░░░░░░░░██─██░░░░░░░░░░░░██───────██░░██───────██░░░░░░░░░░██─██░░██───────────────██░░██───────
─██████████████─████████████████───────██████───────██████████████─██████───────────────██████───────
─────────────────────────────────────────────────────────────────────────────────────────────────────

Copyright (c) 2022 GQYLPY <http://gqylpy.com>. All rights reserved.

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
__version__ = 1, 0, 2, 'alpha1'
__author__ = '竹永康 <gqylpy@outlook.com>'
__source__ = 'https://github.com/gqylpy/gqylpy-log'

NOTSET   = 'NOTSET'
DEBUG    = 'DEBUG'
INFO     = 'INFO'
WARN     = 'WARN'
WARNING  = 'WARNING'
ERROR    = 'ERROR'
CRITICAL = 'CRITICAL'
FATAL    = 'FATAL'

level   = NOTSET
output  = 'stream'
logfile = '/var/log/{default is your startup filename}.log'
datefmt = '%F %T'
logfmt  = '[%(asctime)s] [%(module)s.%(funcName)s.' \
          'line%(lineno)d] [%(levelname)s] %(message)s'


def __init__(
        name:    str,
        *,
        level:   str = None,
        output:  str = None,
        logfmt:  str = None,
        datefmt: str = None,
        logfile: str = None,
        gname:   str = None
) -> 'logging.Logger':
    """Get a logging.Logger instance.

    @param name:    The name is required and will be passed directly
                    to logging.Logger, one string is recommended.
    @param level:   Log level, default "NOTSET".
    @param output:  Log output mode, stream or file, default "stream",
                    optional values are ["stream", "file", "stream,file"].
    @param logfmt:  Passed to logging.Formatter, default "[%(asctime)s] [%(module)s.
                    %(funcName)s.line%(lineno)d] [%(levelname)s] %(message)s"
    @param datefmt: Passed to logging.Formatter, default "%F %T"
    @param logfile: Default is "/var/log/{your startup filename}.log",
                    if "file" in output.
    @param gname:   Create a pointer to the logging.Logger instance
                    in the gqylpy_log module, if not None.
    """


def debug    (msg: str, *, gname: 'Union[str, logging.Logger]' = None, **kw): ...
def info     (msg: str, *, gname: 'Union[str, logging.Logger]' = None, **kw): ...
def warning  (msg: str, *, gname: 'Union[str, logging.Logger]' = None, **kw): ...
def error    (msg: str, *, gname: 'Union[str, logging.Logger]' = None, **kw): ...
def exception(msg: str, *, gname: 'Union[str, logging.Logger]' = None, **kw): ...
def critical (msg: str, *, gname: 'Union[str, logging.Logger]' = None, **kw): ...
def fatal    (msg: str, *, gname: 'Union[str, logging.Logger]' = None, **kw): ...


class _______歌________琪________怡_______玲_______萍_______云_______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            gfunc = getattr(gcode, gname)
            gfunc.__module__ = __package__
            setattr(gpack, gname, gfunc)

    setattr(gpack, '__init__', gcode.__init__)


import logging
from typing import Union
