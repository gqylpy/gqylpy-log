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

Copyright © 2022 GQYLPY. 竹永康 <gqylpy@outlook.com>

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
__version__ = 1, 0, 'dev1'

NOTSET, DEBUG, INFO, WARNING, WARN, ERROR, CRITICAL, FATAL = \
    'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'WARN', 'ERROR', 'CRITICAL', 'FATAL'

level:   str = NOTSET
output:  str = 'stream'  # set('stream', 'file')
logfile: str = '/var/log/{default is your startup filename}.log'
datefmt: str = '%F %T'
logfmt:  str = '[%(asctime)s] [%(levelname)s] %(message)s'


def __init__(gname: str = None, **params) -> 'logging.Logger':
    """Get a logging.Logger object.

    @param gname:
        Assigns the initialized logging.Logger object
        to a variable in the current module, if not None.

    @param params:
        Initialization parameters of logging.Logger, sample:
            level='NOTSET',
            output='stream,file',
            handler='/var/log/gqylpy.log',
            datefmt='%F %T',
            logfmt='[%(asctime)s] [%(levelname)s] %(message)s'

    @return: logging.Logger(**@param(params))
    """


def debug(msg: str, *, gname: 'logging.Logger' = None):
    pass


def info(msg: str, *, gname: 'logging.Logger' = None):
    pass


def warning(msg: str, *, gname: 'logging.Logger' = None):
    pass


def warn(msg: str, *, gname: 'logging.Logger' = None):
    warnings.warn(
        "The 'warn' function is deprecated, use 'warning' instead",
        DeprecationWarning, 2)
    warning(msg, gname=gname)


def error(msg: str, *, gname: 'logging.Logger' = None):
    pass


def critical(msg: str, *, gname: 'logging.Logger' = None):
    pass


def fatal(msg: str, *, gname: 'logging.Logger' = None):
    critical(msg, gname=gname)


class _______歌________琪________怡_______玲_______萍_______云_______:
    import sys

    __import__(f'{__name__}.g {__name__[7:]}')
    gpack = sys.modules[__name__]
    gcode = globals()[f'g {__name__[7:]}']

    for gname in globals():
        if gname[0] != '_' and hasattr(gcode, gname):
            setattr(gpack, gname, getattr(gcode, gname))

    setattr(gpack, '__init__', gcode.__init__)


import logging
import warnings
