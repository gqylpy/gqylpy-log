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
import os
import sys
import uuid
import logging

__default__: logging.Logger

gcode = sys.modules[__name__]
gpack = sys.modules[__name__[:-6]]


def __init__(gname: str = None, **params) -> logging.Logger:
    logger = logging.Logger(gname or uuid.uuid4().hex, params['level'])
    formatter = logging.Formatter(params['logfmt'], params['datefmt'])

    if 'stream' in params['output']:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if 'file' in params['output']:
        try:
            logfile: str = params['logfile']
        except KeyError:
            starter: str = os.path.basename(sys.argv[0])
            logfile: str = f'/var/log/{starter[:-3]}.log'

        logdir: str = os.path.dirname(os.path.abspath(logfile))
        os.path.isdir(logdir) or os.makedirs(logdir)

        handler = logging.FileHandler(logfile, encoding='UTF-8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if gname:
        if not hasattr(gcode, '__default__') or gcode.__default__.name == 'builtins':
            gcode.__default__ = logger
        setattr(gpack, gname, logger)

    return logger


def debug(msg: str, *, gname: logging.Logger = None):
    log('debug', msg, gname)


def info(msg: str, *, gname: logging.Logger = None):
    log('info', msg, gname)


def warning(msg: str, *, gname: logging.Logger = None):
    log('warning', msg, gname)


def error(msg: str, *, gname: logging.Logger = None):
    log('error', msg, gname)


def critical(msg: str, *, gname: logging.Logger = None):
    log('critical', msg, gname)


def log(level: str, msg: str, gname: logging.Logger = None):
    try:
        logger = gname or __default__
    except NameError:
        logger = __init__(
            gname='builtins',
            level=gpack.level,
            output=gpack.output,
            **({'logfile': gpack.logfile}
               if gpack.logfile != '/var/log/{default is your startup filename}.log'
               else {}),
            datefmt=gpack.datefmt,
            logfmt=gpack.logfmt
        )
    getattr(logger, level)(msg)

# '[%(asctime)s] [%(module)s.%(funcName)s line:%(lineno)d] [%(levelname)s] %(message)s'
